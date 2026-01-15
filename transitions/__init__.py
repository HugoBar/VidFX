from .three_blocks import ThreeBlocks

# Dictionary mapping transition names to their classes
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
    # Set of valid transition names
    valid_transitions = set(TRANSITION_REGISTRY.keys())

    # Find any invalid transition names
    invalid = [name for name in transition_names if name not in valid_transitions]
    if invalid:
        error_message = (
            f"Invalid transitions: {', '.join(invalid)}. "
            f"Valid transitions are: {', '.join(valid_transitions)}"
        )
        raise ValueError(error_message)

    # Return corresponding transition classes in order
    return [TRANSITION_REGISTRY[name] for name in transition_names]


def resolve_transition(transition_name):
    """
    Resolves a single transition name to its corresponding class.

    Args:
        transition_name (str): The name of the transition, e.g., "three_blocks".

    Returns:
        class: The transition class corresponding to the provided name.

    Raises:
        ValueError: If the transition name is invalid.
    """
    valid_transitions = set(TRANSITION_REGISTRY.keys())

    if transition_name not in valid_transitions:
        error_message = (
            f"Invalid transition: {transition_name}. "
            f"Valid transitions are: {', '.join(valid_transitions)}"
        )
        raise ValueError(error_message)

    # Return the class from the registry
    return TRANSITION_REGISTRY[transition_name]
