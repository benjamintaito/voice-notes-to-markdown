"""
Procesa audios pendientes con Whisper (faster-whisper), genera una nota
.md por cada audio (titulo + transcript) y mueve el audio a procesados.

Uso:
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
    return title if title else "Nota de voz"


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
        "tags: [nota-de-voz]\n"
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

    pendientes_dir = BASE_DIR / config["paths"]["pendientes"]
    procesados_dir = BASE_DIR / config["paths"]["procesados"]
    notas_dir = BASE_DIR / config["paths"]["notas"]
    for d in (pendientes_dir, procesados_dir, notas_dir):
        d.mkdir(parents=True, exist_ok=True)

    extensiones = set(e.lower() for e in config["extensiones_soportadas"])
    audios = sorted(
        p for p in pendientes_dir.iterdir()
        if p.is_file() and p.suffix.lower() in extensiones
    )

    if not audios:
        print(f"No hay audios nuevos en {pendientes_dir}")
        return

    print(f"Encontrados {len(audios)} audio(s). Cargando modelo Whisper "
          f"({config['whisper']['model_size']})... (puede demorar la primera vez)")

    from faster_whisper import WhisperModel

    model = WhisperModel(
        config["whisper"]["model_size"],
        device=config["whisper"]["device"],
        compute_type=config["whisper"]["compute_type"],
    )

    for audio_path in audios:
        print(f"\nProcesando: {audio_path.name}")
        try:
            segments, info = model.transcribe(
                str(audio_path),
                language=config["whisper"]["language"],
                vad_filter=True,
            )
            transcript = " ".join(segment.text.strip() for segment in segments)

            if not transcript.strip():
                print("  ADVERTENCIA: transcripción vacía, se deja el audio sin mover.")
                continue

            title = slugify_title(audio_path.stem)
            created = datetime.fromtimestamp(audio_path.stat().st_mtime)
            md_content = build_markdown(title, audio_path.name, created, transcript)

            md_path = unique_path(notas_dir / f"{audio_path.stem}.md")
            md_path.write_text(md_content, encoding="utf-8")
            print(f"  Nota creada: {md_path}")

            destino = unique_path(procesados_dir / audio_path.name)
            shutil.move(str(audio_path), str(destino))
            print(f"  Audio movido a: {destino}")

        except Exception as exc:
            print(f"  ERROR procesando {audio_path.name}: {exc}", file=sys.stderr)
            print("  El audio se deja en la carpeta de pendientes para reintentar.")

    print("\nListo.")


if __name__ == "__main__":
    main()
