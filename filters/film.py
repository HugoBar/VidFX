import numpy as np


def film(grain_std=10, warm=(1.4, 1.3, 0.95), sat_factor=1.2):
    """
    Returns a filter function that adds grain and saturation.

    grain_std: how strong the grain/noise is (higher = more grain)
    warm: RGB multipliers to make the image warmer or cooler
    sat_factor: how much to boost saturation (higher = more vivid colors)
    """

    def apply(frame):
        # Add film grain
        grain = np.random.normal(0, grain_std, frame[..., :3].shape)
        frame = frame + grain

        # Warm color grading
        frame[..., 0] *= warm[0]  # red
        frame[..., 1] *= warm[1]  # green
        frame[..., 2] *= warm[2]  # blue

        # Increase saturation
        gray = np.dot(frame[..., :3], [0.299, 0.587, 0.114])[..., None]  # luminance
        frame = gray + (frame - gray) * sat_factor

        # Clip and convert to uint8
        frame = np.clip(frame, 0, 255).astype(np.uint8)
        return frame

    return apply
