from dataclasses import dataclass
from moviepy.Clip import Clip
from moviepy.Effect import Effect

# Constants controlling the number and spacing of horizontal blocks
BARS = 3
GAP_RATIO = 0.02
BAR_RATIO = 0.30


@dataclass
class Blink(Effect):
    """
    Makes the clip progressively appear from another clip over time.

    The effect divides the clip into horizontal blocks that progressively
    reveal the underlying clip. Can also be used for masks.

    Args:
        transition_to (Clip): The clip from which to reveal frames.
    """

    transition_to: Clip

    def apply(self, clip: Clip) -> Clip:
        """
        Apply the ThreeBlocks effect to the given clip.

        Args:
            clip (Clip): The clip to which the effect will be applied.

        Returns:
            Clip: Transformed clip with progressive horizontal block reveal.
        """
        last_index = -1

        print("Applying Blink transition...")

        # TODO: Optimize by precomputing block positions instead of per-frame calculations
        # TODO: Change transition timing to be relative to end of clip
        def filter(get_frame, t):
            nonlocal last_index

            frame = get_frame(t)

            frame_index = last_index + 1
            last_index = frame_index

            transition_start_frame = 3.75 * 60
            frame_i = frame_index - transition_start_frame

            time_in_seconds = frame_index / 60

            # Reveal the first bar after frame 50
            if (
                (frame_i >= 0 and frame_i < 12)
                or (frame_i >= 24 and frame_i < 36)
                or (frame_i >= 48 and frame_i < 60)
            ):
                frame = self.transition_to.get_frame(time_in_seconds)

            return frame

        # Apply the filter as a mask transformation
        return clip.transform(filter, apply_to="mask")
