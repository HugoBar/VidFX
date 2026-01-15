import numpy as np
import cv2  # OpenCV simplifies RGB ↔ HSV conversions


def hue(degrees=50):
    """
    Returns a filter function that shifts the hue of a frame.

    Args:
        degrees (int): Degrees to shift the hue (default: 50). Positive = clockwise, negative = counterclockwise.

    Returns:
        function: A filter function that takes a frame (numpy array) and returns the modified frame.
    """

    def apply(frame):
        # Convert RGB to HSV for easy hue manipulation (OpenCV uses BGR by default)
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV).astype(np.float32)

        # Shift hue (OpenCV hue range: 0-179)
        hsv[..., 0] = (hsv[..., 0] + (degrees / 360.0) * 180) % 180

        # Convert back to RGB uint8
        hsv = hsv.astype(np.uint8)
        rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        return rgb

    return apply
