import numpy as np
import cv2  # OpenCV makes RGB ↔ HSV easy


def hue(degrees=50):
    """
    Returns a filter function that shifts the hue of an image.

    degrees: how much to shift the hue (positive or negative)
    """

    def apply(frame):
        # Convert RGB to HSV (OpenCV uses BGR by default, so swap channels)
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV).astype(np.float32)

        # Shift hue (OpenCV hue range: 0-179)
        hsv[..., 0] = (hsv[..., 0] + (degrees / 360.0) * 180) % 180

        # Convert back to uint8 and RGB
        hsv = hsv.astype(np.uint8)
        rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        return rgb

    return apply
