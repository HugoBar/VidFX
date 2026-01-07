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
from filters import apply_filters
from effects import apply_effects
from logger import logger

app = typer.Typer()


@app.command()
def edit(
    path: Annotated[str, typer.Argument()],
    filters: Annotated[str, typer.Option()] = "",
    effects: Annotated[str, typer.Option()] = "",
    output: Annotated[str, typer.Option()] = "video",
):
    """
    Apply filters and effects to a video and save the result in a new file.

    Args:
        path (str):     Path to the input video file.
        filters (str):  Comma-separated list of filters to apply (e.g., "greyscale,film").
                        Available filters: greyscale, film, high_contrast, hue, purpleish.
        effects (str):  Comma-separated list of effects to apply (e.g., "stop_motion,photo_movement").
                        Available effects: stop_motion, photo_movement.
        output (str):   Base filename for the output video (default: "video"). Saves as .mp4.

    Note:
        - The video is subclipped to the first 5 seconds for processing.
        - Filters are applied per-frame, effects are applied as clip transforms.
        - Requires MoviePy and the filters/effects modules.

    Example:
        python main.py edit input.mp4 --filters greyscale --effects photo_movement --output edited
    """

    logger.info("Starting video editing process...")


    # Create video object
    logger.info(f"Loading video from {path}...")
    clip = VideoFileClip(path).subclipped(0, 5)
    processed_clip = clip

    # --- FILTERS ---

    filter_list = filters.split(",")
    if not filter_list or filter_list == [""]:
        logger.info("No filters selected, continuing...")
    else:
        logger.info(f"You selected the {filter_list} filters!")

        # Attach filters to each frame of the video
        filter_queue = apply_filters(filter_list)
        processed_clip = clip.image_transform(filter_queue)

    # --- EFFECTS ---

    effects_list = effects.split(",")
    if not effects_list or effects_list == [""]:
        logger.info("No effects selected, continuing...")
    else:
        logger.info(f"You selected the {effects_list} effects!")

        # Attach effects to video clip
        effect_queue = apply_effects(effects_list)
        processed_clip = processed_clip.transform(effect_queue, apply_to=["video"])

    # Save video result
    save_video(processed_clip, output)


@app.command()
def merge(
    paths: Annotated[list[str], typer.Argument()],
    output: Annotated[str, typer.Option()] = "merged",
):
    """
    Merge multiple video files into a single video.

    Args:
        paths (list[str]): List of paths to input video files.
        output (str):      Base filename for the output merged video (default: "merged"). Saves as .mp4.

    Example:
        python main.py merge video1.mp4 video2.mp4 --output final_video
    """

    logger.info(f"Merging videos: {paths}")

    clips = [VideoFileClip(path) for path in paths]

    concat_clip = mp.concatenate_videoclips(clips)
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
