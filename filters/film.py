import numpy as np


def film(grain_std=10, warm=(1.4, 1.3, 0.95), sat_factor=1.2):
    """
    Returns a filter function that adds film-like grain, warmth, and saturation to a frame.

    Args:
        grain_std (float): Standard deviation for grain/noise (default: 10). Higher = more grain.
        warm (tuple): RGB multipliers for warmth adjustment (default: (1.4, 1.3, 0.95)).
        sat_factor (float): Saturation boost factor (default: 1.2). Higher = more vivid colors.

    Returns:
        function: A filter function that takes a frame (numpy array) and returns the modified frame.
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
