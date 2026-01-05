def stop_motion(remove_every=2):
    """
    Factory function for the stop_motion effect.

    Creates a transform function that replaces every Nth frame with the previous frame,
    simulating a stop-motion or stuttering effect.

    Note: This is not a real stop-motion effect yet—it's a basic frame replacement.

    Args:
        remove_every (int): Interval for frame replacement (default: 2).
                           Every 'remove_every'-th frame is replaced with the previous one.

    Returns:
        function: A transform function suitable for clip.transform().
    """

    previous_frame = None

    def apply(get_frame, t):
        nonlocal previous_frame

        frame = get_frame(t)
        frame_index = int(t * get_frame.__self__.fps)

        if frame_index % remove_every == 0:
            if previous_frame is not None:
                return previous_frame
            else:
                return frame
        previous_frame = frame
        return frame

    return apply
