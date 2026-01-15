import numpy as np


def greyscale(weights=(0.299, 0.587, 0.114), contrast_factor=1.3):
    """
    Returns a filter function that converts a frame to greyscale with adjustable contrast.

    Args:
        weights (tuple):         RGB weights for luminance calculation (default: (0.299, 0.587, 0.114)).
        contrast_factor (float): Factor to increase contrast (default: 1.3). Higher = stronger contrast.

    Returns:
        function: A filter function that takes a frame (numpy array) and returns the modified frame.
    """

    def apply(frame):
        # Convert RGB frame to greyscale using luminance weights
        grey = np.dot(frame[..., :3], weights)

        # Apply contrast adjustment
        grey = (grey - 128) * contrast_factor + 128

        # Clip values to 0-255 and convert to uint8
        grey = np.clip(grey, 0, 255).astype("uint8")

        # Repeat greyscale across all RGB channels
        return np.repeat(grey[..., None], 3, axis=2)

    return apply
