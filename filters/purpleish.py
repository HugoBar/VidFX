import numpy as np


def purpleish(red_boost_blue=100, green_reduction=0.8, grey_red=40, grey_blue=30):
    """
    Returns a filter function that tints blue and grey pixels toward purple.

    Args:
        red_boost_blue (int): Amount of red to add to bright blue pixels (default: 100). Higher = more purple.
        green_reduction (float): Factor to reduce green in blue pixels (default: 0.8). Lower = more reduction.
        grey_red (int): Amount of red to add to grey/dark pixels (default: 40).
        grey_blue (int): Amount of blue to add to grey/dark pixels (default: 30).

    Returns:
        function: A filter function that takes a frame (numpy array) and returns the modified frame.
    """

    def apply(frame):
        f = frame.astype(np.float32)

        # Original blue mask (bright blue areas)
        blue_mask = (
            (f[:, :, 2] > 100) & (f[:, :, 2] > f[:, :, 0]) & (f[:, :, 2] > f[:, :, 1])
        )

        # Apply blue → purple on bright blue pixels
        f[:, :, 0][blue_mask] += red_boost_blue  # increase red
        f[:, :, 1][blue_mask] *= green_reduction  # reduce green slightly

        # Grey/darker pixels mask (low saturation)
        grey_mask = (
            (np.abs(f[:, :, 0] - f[:, :, 1]) < 20)
            & (np.abs(f[:, :, 0] - f[:, :, 2]) < 20)
            & (f[:, :, 2] > 30)
        )

        # Apply subtle purple tint to grey/dark pixels
        f[:, :, 0][grey_mask] += grey_red
        f[:, :, 2][grey_mask] += grey_blue

        # Clip values
        f = np.clip(f, 0, 255)

        return f.astype(np.uint8)

    return apply
