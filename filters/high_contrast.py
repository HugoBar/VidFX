import numpy as np


def high_contrast(contrast_factor=1.5):
    """
    Returns a filter function that increases the contrast of a frame.

    Args:
        contrast_factor (float): Factor to increase contrast (default: 1.5). Higher = stronger effect.

    Returns:
        function: A filter function that takes a frame (numpy array) and returns the modified frame.
    """

    def apply(frame):
        # Convert to float for precise calculations
        out = frame.copy().astype(np.float32)

        # Normalize RGB to 0-1, apply contrast around midpoint 0.5
        rgb = out[..., :3] / 255.0
        rgb = 0.5 + (rgb - 0.5) * contrast_factor

        # Scale back to 0-255, clip, and convert to uint8
        out[..., :3] = np.clip(rgb * 255, 0, 255)
        return out.astype(np.uint8)

    return apply
