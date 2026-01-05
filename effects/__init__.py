from .photo_movement import photo_movement
from .stop_motion import stop_motion

# Dynamic selection dictionary by name
EFFECTS = {
    "photo_movement": photo_movement,
    "stop_motion": stop_motion,
}


def apply_effects(effect_names):
    """
    Returns a single function that applies multiple effects in sequence to a frame.

    Args:
        effect_names (list): List of effect names (strings), e.g., ["photo_movement", "stop_motion"].

    Returns:
        function: A combined function that takes a frame and applies all effects.
    """

    effect_instances = [EFFECTS[name]() for name in effect_names]

    def apply_all(get_frame, t):
        for e in effect_instances:
            frame = e(get_frame, t)
        return frame

    return apply_all
