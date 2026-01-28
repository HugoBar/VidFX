"""
VidFX: A CLI tool for applying video filters and effects using MoviePy.

This module provides a command-line interface to edit videos by applying
various filters (e.g., greyscale, film) and effects (e.g., stop_motion, photo_movement),
and to merge multiple videos with optional transitions.
"""

import typer
from commands.edit import edit
from commands.merge import merge

app = typer.Typer()

app.command(help="Apply filters and effects to a video.")(edit)
app.command(help="Merge multiple video files into a single video.")(merge)

if __name__ == "__main__":
    app()
