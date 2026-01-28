import typer
from typing_extensions import Annotated
from logger import logger
from moviepy import VideoFileClip, AudioFileClip
import moviepy as mp
from transitions import resolve_transition, TRANSITION_REGISTRY


def merge(
    paths: Annotated[
        list[str],
        typer.Argument(
            help="Paths to input video files. You can specify two or more video files to merge."
        ),
    ],
    transitions: Annotated[
        list[str],
        typer.Option(
            help="List of transitions to apply between videos in the format <name>@<clip_number>. Use --list-transitions to see available transitions."
        ),
    ] = [],
    song_path: Annotated[
        str,
        typer.Option(
            help="Path to an audio file to use as background music for the merged video."
        ),
    ] = "",
    list_transitions: Annotated[
        bool,
        typer.Option(
            help="List all available transitions and exit the program immediately.",
            is_flag=True,
        ),
    ] = False,
    output: Annotated[
        str,
        typer.Option(
            help="Base filename for the output video. Will be saved as <output>.mp4 in the current directory."
        ),
    ] = "merged",
):
    """
    Merge multiple video files into a single video, optionally applying transitions
    between clips.

    Args:
        paths (list[str]):                     Paths to input video files. Provide two or more video files to merge.
        transitions (list[str], optional):     List of transitions to apply between videos. Each transition must
                                               specify the clip it starts at using the format <transition_name>@<clip_number>,
                                               where <clip_number> is **1-based** and indicates the clip from which the
                                               transition begins. Default is no transitions.
        song_path (str, optional):             Path to an audio file to use as background music for the merged video. Default is empty (no audio).
        list_transitions (bool, optional):     If set, lists all available transitions and exits.
        output (str, optional):                Base filename for the output video (default: "video"). Saves as .mp4.

    Note:
        Users are responsible for ensuring that any audio files used are legally permitted.
        This tool does not provide any license or rights to use copyrighted music.

    Example usage:
        python main.py merge video1.mp4 video2.mp4
        python main.py merge clip1.mp4 clip2.mp4 clip3.mp4 --output final_video
        python main.py merge clip1.mp4 clip2.mp4 --transitions crossfade@2 --output final_video
        python main.py merge clip1.mp4 clip2.mp4 --song-path background.mp3 --output final_with_music
    """
    # List available transitions and exit if requested
    if list_transitions:
        logger.info(", ".join(TRANSITION_REGISTRY.keys()))
        raise typer.Exit()

    logger.info(f"Merging videos: {paths}")

    # Load all clips
    clips = [VideoFileClip(path) for path in paths]

    # --- TRANSITIONS ---

    # Validate all transition syntax and clip numbers
    try:
        validate_indexes(transitions, len(clips))
    except ValueError as e:
        logger.error(str(e))
        raise typer.Exit(code=1)

    # Build list of (transition_name, clip_number) tuples
    indexed_transitions = [tuple(transition.split("@")) for transition in transitions]

    try:
        # Resolve transitions to their classes
        # Pair each resolved transition with the clip index
        # Note: clip indexes are zero-based internally, so we subtract 1 from user-provided clip numbers
        transition_classes = [
            (resolve_transition(transition), int(i) - 1)
            for transition, i in indexed_transitions
        ]
    except ValueError as e:
        logger.error(str(e))
        raise typer.Exit(code=1)

    if transition_classes:
        logger.info(f"You selected the {transitions} transitions!")

        # Apply each transition at the specified clip position
        for tc, idx in transition_classes:
            clips[idx] = clips[idx].with_effects([tc(transition_to=clips[idx + 1])])  # type: ignore

    # If no transitions, just concatenate clips directly
    elif not transition_classes:
        logger.info("No transitions selected, continuing...")

    # --- CONCATENATE CLIPS ---
    concat_clip = mp.concatenate_videoclips(clips, method="compose")

    # --- ADD BACKGROUND MUSIC ---
    # TODO: make subclipping times configurable
    if song_path:
        logger.info(f"Adding background music from {song_path}...")

        audio = (
            AudioFileClip(song_path).subclipped(5).with_duration(concat_clip.duration)
        )

        concat_clip = concat_clip.with_audio(audio)
    else:
        logger.info("No background music specified, continuing...")

    # --- SAVE VIDEO ---
    concat_clip.write_videofile(
        f"{output}.mp4",
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        threads=4,
    )


def validate_indexes(transitions_list, max_length):
    """
    Validate clip numbers in transitions to ensure correct usage.

    Args:
        transitions_list (list): List of transitions in the format <name>@<clip_number>.
        max_length (int):        Number of clips being merged.
    Raises:
        ValueError: If any index is invalid or duplicate.
    """
    used_transition_slots = []

    for transition in transitions_list:
        # Check that the transition contains a clip number (the "@N" syntax)
        if "@" not in transition or not transition.split("@")[1]:
            error_message = f"Transition is missing a clip number: {transition}. Use <transition_name>@<clip_number>."
            raise ValueError(error_message)

        # Split transition into name and starting clip number
        _, clip_position = transition.split("@")

        # Ensure the clip number is numeric
        if not clip_position.isdigit():
            error_message = f"Transition clip number must be a number: {transition}"
            raise ValueError(error_message)

        clip_position = int(clip_position)

        # Check that the clip number is within valid bounds (1-based)
        if not (1 <= clip_position < max_length):
            error_message = f"Transition clip number {clip_position} is out of bounds for {max_length} clips. Valid clip numbers are from 1 to {max_length - 1}."
            raise ValueError(error_message)

        # Ensure no duplicate clip numbers (each transition can only be applied once per clip)
        if clip_position in used_transition_slots:
            error_message = f"Transition clip number {clip_position} is already used. You can only use each clip number once."
            raise ValueError(error_message)

        # Track the used clip numbers
        used_transition_slots.append(clip_position)
