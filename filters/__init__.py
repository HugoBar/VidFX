from .film import film
from .greyscale import greyscale
from .high_contrast import high_contrast
from .purpleish import purpleish
from .hue import hue
from .pink_future import pink_future

# Registry of available filters by name
# Allows dynamic lookup of filters for validation and application
FILTER_REGISTRY = {
    "film": film,
    "greyscale": greyscale,
    "high_contrast": high_contrast,
    "purpleish": purpleish,
    "hue": hue,
    "pink_future": pink_future,
}


def validate_filters(filter_names):
    """
    Validate that all requested filter names exist in the FILTER_REGISTRY.

    Args:
        filter_names (list): List of filter names (strings).

    Raises:
        ValueError: If any filter name is not recognized.
    """
    # Get the set of valid filter names
    valid_filters = set(FILTER_REGISTRY.keys())

    # Identify any invalid filter names provided by the user
    invalid_filters = [name for name in filter_names if name not in valid_filters]

    # Raise an error if there are unrecognized filters
    if invalid_filters:
        error_message = (
            f"Invalid filters: {', '.join(invalid_filters)}. "
            f"Valid filters are: {', '.join(valid_filters)}"
        )
        raise ValueError(error_message)


def apply_filters(filter_names):
    """
    Create a single function that applies multiple filters in sequence to a video frame.

    Args:
        filter_names (list): List of filter names (strings), e.g., ["film", "greyscale"].

    Returns:
        function: A combined function that takes a single frame (numpy array) and applies
                  all requested filters in order.

    Notes:
        - Filters are applied sequentially, in the order they appear in filter_names.
        - Each filter is assumed to be a callable that modifies the frame and returns it.
    """
    # Instantiate each filter class/function based on the user-selected names
    filter_instances = [FILTER_REGISTRY[name]() for name in filter_names]

    # Combined function that applies all filters to a frame
    def apply_all(frame):
        # Apply each filter in sequence
        for f in filter_instances:
            frame = f(frame)
        return frame

    return apply_all
