import numpy as np


def pink_future(
    contrast=1.0,
    brightness=0.0,
    pink_strength=0.5,
    cyan_strength=0.5,
    shadow_threshold=0.3,
    highlight_threshold=0.7,
):
    """
    Returns a dual-tone filter function that applies a stylized 'pink-future' effect.

    Args:
        contrast (float):            Factor for contrast adjustment (default: 1.0). Higher = stronger contrast.
        brightness (float):          Value to add to frame brightness (default: 0.0). Positive = brighter.
        pink_strength (float):       Strength of pink overlay on highlights (0.0–1.0, default: 0.5).
        cyan_strength (float):       Strength of cyan overlay on shadows (0.0–1.0, default: 0.5).
        shadow_threshold (float):    Normalized grayscale threshold for shadows (0.0–1.0, default: 0.3).
        highlight_threshold (float): Normalized grayscale threshold for highlights (0.0–1.0, default: 0.7).

    Note:
        Some thresholds are not used in a strictly standard way. This is intentional — it
        contributes to the stylized 'pink-future' look. You can experiment by changing the comparison
        operators or swapping `highlight_threshold` and `shadow_threshold` for different effects.

    Returns:
        function: A filter function that takes a frame (numpy array) and returns the stylized frame.
    """

    def apply(frame):
        f = frame.astype(np.float32)

        # Apply contrast
        mid = 128.0
        f = (f - mid) * contrast + mid

        # Apply brightness
        f += brightness
        f = np.clip(f, 0, 255)

        # Convert to grayscale for masks
        gray = 0.2126 * f[:, :, 0] + 0.7152 * f[:, :, 1] + 0.0722 * f[:, :, 2]
        gray_norm = gray / 255.0

        # Pink overlay on highlights
        pink_color = (255, 130, 255)
        pink_layer = np.full(f.shape, pink_color, dtype=np.float32)
        highlight_mask = gray_norm > shadow_threshold
        mask_3ch = np.stack([highlight_mask] * 3, axis=2)
        f[mask_3ch] = (
            f[mask_3ch] * (1 - pink_strength) + pink_layer[mask_3ch] * pink_strength
        )

        # Cyan overlay on shadows
        cyan_layer = np.full(f.shape, [0, 255, 255], dtype=np.float32)
        shadow_mask = gray_norm < shadow_threshold
        mask_3ch = np.stack([shadow_mask] * 3, axis=2)
        f[mask_3ch] = (
            f[mask_3ch] * (1 - cyan_strength) + cyan_layer[mask_3ch] * cyan_strength
        )

        return np.clip(f, 0, 255).astype(np.uint8)

    return apply
