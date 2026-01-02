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


def apply_filters(filter_names):
    """
    Returns a single function that applies multiple filters in sequence to a
    frame.

    filter_names: list of strings, e.g., ["film", "greyscale"]
    """

    filter_instances = [FILTERS[name]() for name in filter_names]

    def apply_all(frame):
        for f in filter_instances:
            frame = f(frame)
        return frame

    return apply_all
