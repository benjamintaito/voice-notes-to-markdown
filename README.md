# Voice Notes to Markdown

Transcribes voice notes (meetings, ideas, personal notes, etc.) using the
[OpenAI Whisper](https://github.com/openai/whisper) model for speech
recognition, and automatically generates a Markdown note ready to use in
[Obsidian](https://obsidian.md/), with title and transcript.

The audio is never sent to any cloud service.

## How it works

1. Drop audio files into the `pending_audio/` folder.
2. Run the script.
3. For each audio file, a `.md` note is created in `notes/` and the audio is
   moved to `processed_audio/`.

## Requirements

- Python 3.10 or higher.
- [ffmpeg](https://ffmpeg.org/) installed on your system.

## Installation

```bash
git clone https://github.com/benjamintaito/voice-notes-to-markdown.git
cd voice-notes-to-markdown
```

Install ffmpeg:

```bash
winget install ffmpeg      # Windows
brew install ffmpeg        # macOS
sudo apt install ffmpeg    # Linux (Debian/Ubuntu)
```

Create a virtual environment and install the dependencies (includes
`faster-whisper`, the library that runs the Whisper model):

```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt   # Windows
.venv/bin/pip install -r requirements.txt       # macOS/Linux
```

## Usage

Drop the audio files to transcribe into `pending_audio/` and run:

```bash
.venv\Scripts\python.exe process.py   # Windows (or double-click process.bat)
.venv/bin/python process.py           # macOS/Linux
```

Notes end up in `notes/` and processed audio files in `processed_audio/`.

## Configuration (`config.yaml`)

- `paths.notes`: can be pointed directly to a folder inside your Obsidian
  vault.
- `whisper.model_size`: `tiny`, `base`, `small`, `medium` or `large-v3`.
  Bigger models give better quality but run slower.
- `whisper.language`: language of the audio (defaults to `es`).
- `whisper.device` / `compute_type`: `cpu` / `int8` without a GPU; `cuda` /
  `float16` with an NVIDIA GPU to speed up processing.

## Additional notes

- The first time the script runs, it downloads the selected Whisper model
  and caches it for future runs.
- The audio filename is used as the note title.
