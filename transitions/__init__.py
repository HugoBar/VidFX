from .three_blocks import ThreeBlocks

# Dynamic selection dictionary by name
TRANSITION_REGISTRY = {
    "three_blocks": ThreeBlocks,
}


def resolve_transitions(transition_names):
    """
    Resolves a list of transition names to their corresponding classes.

    Args:
        transition_names (list): List of transition names (strings), e.g., ["three_blocks"].
                                 All names must exist in the transition registry.

    Returns:
        list: A list of transition classes corresponding to the provided names.

    Raises:
        ValueError: If any transition name is invalid.
    """
    valid_transitions = set(TRANSITION_REGISTRY.keys())

    invalid = [name for name in transition_names if name not in valid_transitions]
    if invalid:
        raise ValueError(
            f"Invalid transitions: {', '.join(invalid)}. Valid transitions are: {', '.join(valid_transitions)}"
        )
    return [TRANSITION_REGISTRY[name] for name in transition_names]
