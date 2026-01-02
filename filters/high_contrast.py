import numpy as np


def high_contrast(contrast_factor=1.5):
    """
    Returns a filter function that increases contrast.

    contrast_factor: how much to increase contrast (higher = stronger effect)
    """

    def apply(frame):
        # convert to float for calculations
        out = frame.copy().astype(np.float32)

        rgb = out[..., :3] / 255.0
        rgb = 0.5 + (rgb - 0.5) * contrast_factor
        out[..., :3] = np.clip(rgb * 255, 0, 255)

        return out.astype(np.uint8)

    return apply
