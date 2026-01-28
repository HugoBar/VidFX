import typer
from typing_extensions import Annotated
from logger import logger
import os
from moviepy import VideoFileClip
from filters import FILTER_REGISTRY, apply_filters, validate_filters
from effects import EFFECTS_REGISTRY, apply_effects, validate_effects


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
        path (str):                       Path to the input video file.
        filters (str, optional):          Comma-separated list of filters to apply (e.g., "greyscale,film").
                                          Available filters: greyscale, film, high_contrast, hue, purpleish.
        effects (str, optional):          Comma-separated list of effects to apply (e.g., "stop_motion,photo_movement").
                                          Available effects: stop_motion, photo_movement.
        list_filters (bool, optional):    If set, lists all available filters and exits.
        list_effects (bool, optional):    If set, lists all available effects and exits.
        output (str, optional):           Base filename for the output video (default: "video"). Saves as .mp4.

    Note:
        - The video is subclipped to the first 5 seconds for processing.
        - Filters are applied per-frame, effects are applied as clip transforms.
        - Requires MoviePy and the filters/effects modules.

    Example usage:
        python main.py edit input.mp4 --filters greyscale --effects photo_movement --output edited
        python main.py edit input.mp4 --filters film
        python main.py edit input.mp4 --effects stop_motion
    """

    # If requested, list available filters and exit
    if list_filters:
        logger.info(", ".join(FILTER_REGISTRY))
        raise typer.Exit()

    # If requested, list available effects and exit
    if list_effects:
        logger.info(", ".join(EFFECTS_REGISTRY))
        raise typer.Exit()

    logger.info("Starting video editing process...")

    # Validate input file path exists
    logger.info("Validating input file path...")
    if not os.path.isfile(path):
        logger.error(
            f"The file {path} does not exist. Please provide a valid video file path."
        )
        raise typer.Exit(code=1)

    logger.info("Input file path is valid.")

    # Load the video and subclip first 5 seconds for processing
    logger.info(f"Loading video from {path}...\n")
    clip = VideoFileClip(path).subclipped(0, 5)
    processed_clip = clip

    # --- FILTERS ---

    filter_list = filters.split(",")

    # Skip filters if none specified
    if not filter_list or filter_list == [""]:
        logger.info("No filters selected, continuing...")
    else:
        try:
            # Validate that all requested filters exist
            validate_filters(filter_list)
        except ValueError as e:
            logger.error(str(e))
            raise typer.Exit(code=1)
        logger.info(f"You selected the {filter_list} filters!")

        # Apply filters to each frame of the video
        filter_queue = apply_filters(filter_list)
        processed_clip = clip.image_transform(filter_queue)

    # --- EFFECTS ---

    effects_list = effects.split(",")

    # Skip effects if none specified
    if not effects_list or effects_list == [""]:
        logger.info("No effects selected, continuing...")
    else:
        try:
            # Validate that all requested effects exist
            validate_effects(effects_list)
        except ValueError as e:
            logger.error(str(e))
            raise typer.Exit(code=1)
        logger.info(f"You selected the {effects_list} effects!")

        # Apply effects to the video clip
        effect_queue = apply_effects(effects_list)
        processed_clip = processed_clip.transform(effect_queue, apply_to=["video"])

    # --- SAVE VIDEO ---
    processed_clip.write_videofile(
        f"{output}.mp4",
        codec="libx264",
        audio=False,
        preset="medium",
        threads=4,
    )
