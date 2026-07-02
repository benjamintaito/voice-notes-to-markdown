"""
Processes pending audio files with Whisper (faster-whisper), generates a
.md note per audio file (title + transcript) and moves the audio to the
processed folder.

Usage:
    python process.py
"""
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.yaml"


def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def slugify_title(stem: str) -> str:
    title = re.sub(r"[_\-]+", " ", stem).strip()
    return title if title else "Voice note"


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    counter = 2
    while True:
        candidate = path.with_stem(f"{path.stem} ({counter})")
        if not candidate.exists():
            return candidate
        counter += 1


def build_markdown(title: str, source_filename: str, created: datetime, transcript: str) -> str:
    frontmatter = (
        "---\n"
        f"title: \"{title}\"\n"
        f"date: {created.strftime('%Y-%m-%d %H:%M')}\n"
        f"source_audio: \"{source_filename}\"\n"
        "tags: [voice-note]\n"
        "---\n\n"
    )
    body = (
        f"# {title}\n\n"
        "## Transcript\n\n"
        f"{transcript.strip()}\n"
    )
    return frontmatter + body


def main():
    config = load_config()

    pending_dir = BASE_DIR / config["paths"]["pending"]
    processed_dir = BASE_DIR / config["paths"]["processed"]
    notes_dir = BASE_DIR / config["paths"]["notes"]
    for d in (pending_dir, processed_dir, notes_dir):
        d.mkdir(parents=True, exist_ok=True)

    extensions = set(e.lower() for e in config["supported_extensions"])
    audio_files = sorted(
        p for p in pending_dir.iterdir()
        if p.is_file() and p.suffix.lower() in extensions
    )

    if not audio_files:
        print(f"No new audio files found in {pending_dir}")
        return

    print(f"Found {len(audio_files)} audio file(s). Loading Whisper model "
          f"({config['whisper']['model_size']})... (this may take a while the first time)")

    from faster_whisper import WhisperModel

    model = WhisperModel(
        config["whisper"]["model_size"],
        device=config["whisper"]["device"],
        compute_type=config["whisper"]["compute_type"],
    )

    for audio_path in audio_files:
        print(f"\nProcessing: {audio_path.name}")
        try:
            segments, info = model.transcribe(
                str(audio_path),
                language=config["whisper"]["language"],
                vad_filter=True,
            )
            transcript = " ".join(segment.text.strip() for segment in segments)

            if not transcript.strip():
                print("  WARNING: empty transcript, leaving the audio file in place.")
                continue

            title = slugify_title(audio_path.stem)
            created = datetime.fromtimestamp(audio_path.stat().st_mtime)
            md_content = build_markdown(title, audio_path.name, created, transcript)

            md_path = unique_path(notes_dir / f"{audio_path.stem}.md")
            md_path.write_text(md_content, encoding="utf-8")
            print(f"  Note created: {md_path}")

            destination = unique_path(processed_dir / audio_path.name)
            shutil.move(str(audio_path), str(destination))
            print(f"  Audio moved to: {destination}")

        except Exception as exc:
            print(f"  ERROR processing {audio_path.name}: {exc}", file=sys.stderr)
            print("  The audio file is left in the pending folder to retry later.")

    print("\nDone.")


if __name__ == "__main__":
    main()
