import numpy as np


def greyscale(weights=(0.299, 0.587, 0.114), contrast_factor=1.3):
    """
    Returns a filter function that converts frame to greyscale with optional contrast.

    weights: RGB weights for calculating greyscale (default = standard luminance)
    contrast_factor: how much to increase contrast (higher = stronger effect)
    """

    def apply(frame):
        # Convert to greyscale
        grey = np.dot(frame[..., :3], weights)

        # Apply contrast
        grey = (grey - 128) * contrast_factor + 128

        # Clip and convert to uint8
        grey = np.clip(grey, 0, 255).astype("uint8")

        # Repeat across RGB channels
        return np.repeat(grey[..., None], 3, axis=2)

    return apply
