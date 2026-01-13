from dataclasses import dataclass

from moviepy.Clip import Clip
from moviepy.Effect import Effect

BARS = 3
GAP_RATIO = 0.02
BAR_RATIO = 0.30


@dataclass
class ThreeBlocks(Effect):
    """
    Makes the clip progressively appear from another clip over time.

    The effect divides the clip into horizontal blocks that progressively
    reveal the underlying clip. Can also be used for masks.

    Args:
        transition_to (Clip): The clip from which to reveal frames.
    """

    transition_to: Clip

    def __post_init__(self):
        """Precompute block positions and cropped frames."""
        frame = self.transition_to.get_frame(0)
        h, w = frame.shape[:2]
        self.y1, self.y2 = int(0.33 * h), int(0.66 * h)
        gap = int(GAP_RATIO * w)
        block = int(BAR_RATIO * w)

        used = BARS * block + (BARS - 1) * gap
        remainder = w - used
        left_pad = remainder // 2

        xs = []
        cursor = left_pad
        for _ in range(BARS):
            x1, x2 = cursor, cursor + block
            xs.append((x1, x2))
            cursor = x2 + gap

        self.xs = xs
        self.frame_crops = [frame[self.y1 : self.y2, x1:x2] for x1, x2 in xs]

    def apply(self, clip: Clip) -> Clip:
        def filter(get_frame, t):
            frame = get_frame(t)
            frame_index = int(t * clip.fps)

            # Reveal first bar
            if frame_index >= 50:
                frame = frame.copy()
                frame[self.y1 : self.y2, self.xs[0][0] : self.xs[0][1]] = (
                    self.frame_crops[0]
                )

            # Reveal first two bars
            if frame_index >= 70:
                frame = frame.copy()
                for i in range(2):
                    x1, x2 = self.xs[i]
                    frame[self.y1 : self.y2, x1:x2] = self.frame_crops[i]

            # Reveal all three bars
            if frame_index >= 100:
                frame = frame.copy()
                for i in range(3):
                    x1, x2 = self.xs[i]
                    frame[self.y1 : self.y2, x1:x2] = self.frame_crops[i]

            return frame

        return clip.transform(filter, apply_to="mask")
