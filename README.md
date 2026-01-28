# VidFX – CLI Video Editing Tool

VidFX is a Python command-line tool for applying filters, effects, and transitions to videos, enabling users to enhance and transform their footage easily.

---

## Features

- **Edit videos** with filters and effects (listable via CLI)
- **Merge multiple videos** with optional transitions (listable via CLI)
- **Simple CLI workflow** – no GUI needed

---

## Installation

### Prerequisites
- Python 3.8+  

### Steps
1. Clone the repository:

    ```
    git clone https://github.com/HugoBar/VidFX.git
    cd VidFX
    ```

3. Install dependencies using pip (or another Python package manager):

   ```
   pip install -r requirements.txt
   ``` 

> The `requirements.txt` file lists all the necessary Python libraries for VidFX.  

---

## Usage

VidFX has two main commands: `edit` and `merge`.

### 1. Edit a Video
Apply filters and effects to a single video.

    python3 main.py edit <path_to_video> [options]

**Options:**
- `--filters` – Comma-separated list of filters  
- `--effects` – Comma-separated list of effects  
- `--list-filters` – List all available filters  
- `--list-effects` – List all available effects  
- `--output` – Output filename (default: `video.mp4`)

**Example:**
    
    python3 main.py edit input.mp4 --filters greyscale --effects photo_movement --output edited

---

### 2. Merge Videos
Combine multiple clips with optional transitions and background music.

    python3 main.py merge <video1> <video2> ... [options]

**Options:**
- `--transitions` – List of transitions in the format `<transition_name>@<clip_number>`  
- `--list-transitions` – List all available transitions  
- `--song-path` – Path to an audio file to use as background music  
- `--output` – Output filename (default: `merged.mp4`)

**Note:**  
Users are responsible for ensuring that any audio files used are legally permitted. This tool does not provide any license or rights to use copyrighted music.

**Example:**

    python3 main.py merge clip1.mp4 clip2.mp4 --transitions three_blocks@2 --song-path background.mp3 --output final_video

---

## Development / Contributing

This project is a personal project and currently under development.  
Planned features and improvements are tracked in [TODO.md](TODO.md).

---
