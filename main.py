"""
VidFX: A CLI tool for applying video filters and effects using MoviePy.

This module provides a command-line interface to edit videos by applying
various filters (e.g., greyscale, film) and effects (e.g., stop_motion, photo_movement).
"""

import os
import typer
from typing_extensions import Annotated
from moviepy import VideoFileClip
import moviepy as mp
from filters import apply_filters, validate_filters, FILTERS
from effects import apply_effects, validate_effects, EFFECTS
from transitions import resolve_transitions
from logger import logger

app = typer.Typer()


@app.command(help="Apply filters and effects to a video.")
def edit(
    path: Annotated[str, typer.Argument(help="Path to the input video file. (.mp4)")],
    filters: Annotated[
        str,
        typer.Option(
            help="Comma-separated list of filters to apply. Use --list-filters to see available filters."
        ),
    ] = "",
    effects: Annotated[
        str,
        typer.Option(
            help="Comma-separated list of effects to apply. Use --list-effects to see available effects."
        ),
    ] = "",
    list_filters: Annotated[
        bool,
        typer.Option(
            help="List all available filters and exit the program immediately.",
            is_flag=True,
        ),
    ] = False,
    list_effects: Annotated[
        bool,
        typer.Option(
            help="List all available effects and exit the program immediately.",
            is_flag=True,
        ),
    ] = False,
    output: Annotated[
        str,
        typer.Option(
            help="Base filename for the output video. Will be saved as <output>.mp4 in the current directory."
        ),
    ] = "video",
):
    """
    Apply filters and effects to a video and save the result in a new file.

    Args:
        path (str):             Path to the input video file.
        filters (str):          Comma-separated list of filters to apply (e.g., "greyscale,film").
                                Available filters: greyscale, film, high_contrast, hue, purpleish.
        effects (str):          Comma-separated list of effects to apply (e.g., "stop_motion,photo_movement").
                                Available effects: stop_motion, photo_movement.
        list_filters (bool):    If set, lists all available filters and exits.
        list_effects (bool):    If set, lists all available effects and exits.
        output (str):           Base filename for the output video (default: "video"). Saves as .mp4.

    Note:
        - The video is subclipped to the first 5 seconds for processing.
        - Filters are applied per-frame, effects are applied as clip transforms.
        - Requires MoviePy and the filters/effects modules.

    Example:
        python main.py edit input.mp4 --filters greyscale --effects photo_movement --output edited
        python main.py edit input.mp4 --filters film
        python main.py edit input.mp4 --effects stop_motion
    """

    if list_filters:
        logger.info(", ".join(FILTERS))
        raise typer.Exit()

    if list_effects:
        logger.info(", ".join(EFFECTS))
        raise typer.Exit()

    logger.info("Starting video editing process...")

    # Validate input file path
    logger.info("Validating input file path...")
    isFile = os.path.isfile(path)
    if not isFile:
        logger.error(
            f"The file {path} does not exist. Please provide a valid video file path."
        )
        raise typer.Exit(code=1)

    logger.info("Input file path is valid.")

    # Create video object
    logger.info(f"Loading video from {path}...\n")
    clip = VideoFileClip(path).subclipped(0, 5)
    processed_clip = clip

    # --- FILTERS ---

    filter_list = filters.split(",")

    if not filter_list or filter_list == [""]:
        logger.info("No filters selected, continuing...")
    else:
        try:
            validate_filters(filter_list)
        except ValueError as e:
            logger.error(str(e))
            raise typer.Exit(code=1)
        logger.info(f"You selected the {filter_list} filters!")

        # Attach filters to each frame of the video
        filter_queue = apply_filters(filter_list)
        processed_clip = clip.image_transform(filter_queue)

    # --- EFFECTS ---

    effects_list = effects.split(",")

    if not effects_list or effects_list == [""]:
        logger.info("No effects selected, continuing...")
    else:
        try:
            validate_effects(effects_list)
        except ValueError as e:
            logger.error(str(e))
            raise typer.Exit(code=1)
        logger.info(f"You selected the {effects_list} effects!")

        # Attach effects to video clip
        effect_queue = apply_effects(effects_list)
        processed_clip = processed_clip.transform(effect_queue, apply_to=["video"])

    # --- SAVE VIDEO ---
    save_video(processed_clip, output)


@app.command(help="Merge multiple video files into a single video.")
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
            help="Comma-separated list of transitions to apply between videos. Use --list-transitions to see available transitions."
        ),
    ] = [],
    output: Annotated[
        str,
        typer.Option(
            help="Base filename for the output video. Will be saved as <output>.mp4 in the current directory."
        ),
    ] = "merged",
):
    """
    Merge multiple video files into a single video.

    Args:
        paths (list[str]):       List of paths to input video files.
        transitions (list[str]): List of transitions to apply between videos (default: none).
        output (str):            Base filename for the output merged video (default: "merged"). Saved as <output>.mp4.

    Example:
        python main.py merge video1.mp4 video2.mp4
        python main.py merge clip1.mp4 clip2.mp4 clip3.mp4 --output final_video
        python main.py merge clip1.mp4 clip2.mp4 --transitions three_blocks --transitions crossfade --output final_video
    """
    logger.info(f"Merging videos: {paths}")

    clips = [VideoFileClip(path) for path in paths]

    # --- TRANSITIONS ---
    try:
        transition_classes = resolve_transitions(transitions)
    except ValueError as e:
        logger.error(str(e))
        raise typer.Exit(code=1)

    if transition_classes:
        logger.info(f"You selected the {transitions} transitions!")

        # Attach transitions to each clip (except the last one)
        for i in range(len(clips) - 1):
            clips[i] = clips[i].with_effects(
                [transition_classes[i](transition_to=clips[i + 1])]
            )
    else:
        logger.info("No transitions selected, continuing...")

    concat_clip = mp.concatenate_videoclips(clips)

    # --- SAVE VIDEO ---
    save_video(concat_clip, output)


def save_video(clip, output):
    """
    Save the given video clip to a file.

    Args:
        clip (VideoFileClip): The video clip to save.
        output (str):         Base filename for the output video. Saves as .mp4.
    """
    clip.write_videofile(
        f"{output}.mp4",
        codec="libx264",
        audio=False,
        preset="medium",
        threads=4,
    )


if __name__ == "__main__":
    app()
