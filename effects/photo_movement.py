def photo_movement(duplicate_every=4):
    """
    Factory function for the photo_movement effect.

    Creates a transform function that duplicates frames to create a stuttering or freeze-frame effect.
    Every (duplicate_every + 1) frames, the current frame is duplicated 'duplicate_every' times.

    Args:
        duplicate_every (int): Number of additional duplicates for each triggered frame (default: 4).
                               Total frames shown per trigger: 1 (original) + duplicate_every.

    Returns:
        function: A transform function suitable for clip.transform().
    """
    previous_frame = None
    duplicate_count = 0
    last_index = -1

    def apply(get_frame, t):
        nonlocal previous_frame, duplicate_count, last_index

        frame = get_frame(t)

        frame_index = last_index + 1
        last_index = frame_index

        # If we are in a duplication window, return the previous frame
        if duplicate_count > 0:
            duplicate_count -= 1
            return previous_frame

        # Trigger duplication every (duplicate_every + 1) frames
        if frame_index % (duplicate_every + 1) == 0:
            previous_frame = frame
            duplicate_count = duplicate_every
            return frame

        return frame

    return apply
