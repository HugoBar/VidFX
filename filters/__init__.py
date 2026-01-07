from .film import film
from .greyscale import greyscale
from .high_contrast import high_contrast
from .purpleish import purpleish
from .hue import hue

# Dynamic selection dictionary by name
FILTERS = {
    "film": film,
    "greyscale": greyscale,
    "high-contrast": high_contrast,
    "purpleish": purpleish,
    "hue": hue,
}


def validate_filters(filter_names):
    """
    Validates a list of filter names against available filters.

    Args:
        filter_names (list): List of filter names (strings).

    Raises:
        ValueError: If any filter name is invalid.
    """
    valid_filters = set(FILTERS.keys())
    invalid_filters = [name for name in filter_names if name not in valid_filters]

    if invalid_filters:
        error_message = f"Invalid filters: {', '.join(invalid_filters)}. Valid filters are: {', '.join(valid_filters)}"
        raise ValueError(error_message)


def apply_filters(filter_names):
    """
    Returns a single function that applies multiple filters in sequence to a frame.

    Args:
        filter_names (list): List of filter names (strings), e.g., ["film", "greyscale"].

    Returns:
        function: A combined function that takes a frame (numpy array) and applies all filters.
    """
    filter_instances = [FILTERS[name]() for name in filter_names]

    def apply_all(frame):
        for f in filter_instances:
            frame = f(frame)
        return frame

    return apply_all
