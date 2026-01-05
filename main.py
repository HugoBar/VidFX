import typer
from typing_extensions import Annotated
from moviepy import VideoFileClip
from filters import apply_filters

app = typer.Typer()


@app.command()
def edit(
    path: Annotated[str, typer.Argument()],
    filters: Annotated[str, typer.Option()] = "",
    output: Annotated[str, typer.Option()] = "video",
):
    """
    Apply filters to a video and save the result in a new file.

    path: path to the input video
    filters: list of filters to apply
    output: base filename for the output video
    """

    print(f"Editing video: {path}")

    # Create video object
    clip = VideoFileClip(path).subclipped(0, 5)
    processed_clip = clip

    filter_list = filters.split(",")
    print(f"You selected the {filter_list} filters!")

    if not filter_list or filter_list == [""]:
        print("No filters selected, continuing...")
    else:
        # Apply filters to each frame of the video
        filter_queue = apply_filters(filter_list)
        processed_clip = clip.image_transform(filter_queue)


    # Save video result
    filtered_clip.write_videofile(
        f"{output}.mp4",
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
        preset="medium",
        threads=4,
    )


if __name__ == "__main__":
    app()
