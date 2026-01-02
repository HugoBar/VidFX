import numpy as np


def purpleish(red_boost_blue=100, green_reduction=0.8, grey_red=40, grey_blue=30):
    """
    Returns a filter function that tints blue and grey pixels toward purple.

    red_boost_blue: how much red to add to bright blue pixels (higher = more purple)
    green_reduction: factor to reduce green in blue pixels (0-1, lower = greener reduced more)
    grey_red: how much red to add to grey/dark pixels
    grey_blue: how much blue to add to grey/dark pixels
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
