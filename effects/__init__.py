from .photo_movement import photo_movement
from .stop_motion import stop_motion

# Dynamic selection dictionary by name (registry pattern)
EFFECTS_REGISTRY = {
    "photo_movement": photo_movement,
    "stop_motion": stop_motion,
}


def validate_effects(effect_names):
    """
    Validates a list of effect names against available effects.

    Args:
        effect_names (list): List of effect names (strings).

    Raises:
        ValueError: If any effect name is invalid.
    """
    valid_effects = set(EFFECTS_REGISTRY.keys())
    invalid_effects = [name for name in effect_names if name not in valid_effects]

    if invalid_effects:
        error_message = (
            f"Invalid effects: {', '.join(invalid_effects)}. "
            f"Valid effects are: {', '.join(valid_effects)}"
        )
        raise ValueError(error_message)


def apply_effects(effect_names):
    """
    Returns a single function that applies multiple effects in sequence to a frame.

    Args:
        effect_names (list): List of effect names (strings), e.g., ["photo_movement", "stop_motion"].

    Returns:
        function: A combined function that takes a frame (get_frame, t) and applies all effects in order.
    """
    # Instantiate effect functions for all selected effects
    effect_instances = [EFFECTS_REGISTRY[name]() for name in effect_names]

    def apply_all(get_frame, t):
        frame = get_frame(t)
        # Apply each effect sequentially
        for e in effect_instances:
            frame = e(lambda _: frame, t)
        return frame

    return apply_all
