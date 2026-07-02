# Voice Notes

Transcribe notas de voz (reuniones, ideas, apuntes personales, etc.) de forma
**100% local**, usando el modelo [Whisper de OpenAI](https://github.com/openai/whisper)
para reconocer el audio, y genera automáticamente una nota en Markdown lista
para usar en [Obsidian](https://obsidian.md/), con título, resumen y
transcript.

Al ser local, el audio nunca se envía a ningún servicio en la nube.

## ¿Cómo funciona?

1. Se colocan los audios en la carpeta `audios_pendientes/`.
2. Se ejecuta el script.
3. Por cada audio se genera una nota `.md` en `notas/` y el audio se mueve a
   `audios_procesados/`.

## Requisitos

- Python 3.10 o superior.
- [ffmpeg](https://ffmpeg.org/) instalado en el sistema.

## Instalación

```bash
git clone https://github.com/benjamintaito/voice-notes.git
cd voice-notes
```

Instalar ffmpeg:

```bash
winget install ffmpeg      # Windows
brew install ffmpeg        # macOS
sudo apt install ffmpeg    # Linux (Debian/Ubuntu)
```

Crear el entorno virtual e instalar las dependencias (incluye `faster-whisper`,
la librería que corre el modelo Whisper de forma local):

```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt   # Windows
.venv/bin/pip install -r requirements.txt       # macOS/Linux
```

## Uso

Colocar los audios en `audios_pendientes/` y ejecutar:

```bash
.venv\Scripts\python.exe process.py   # Windows (o doble clic en procesar.bat)
.venv/bin/python process.py           # macOS/Linux
```

Las notas quedan en `notas/` y los audios ya procesados en
`audios_procesados/`.

## Configuración (`config.yaml`)

- `paths.notas`: se puede apuntar directo a una carpeta del vault de Obsidian.
- `whisper.model_size`: `tiny`, `base`, `small`, `medium` o `large-v3`. Más
  grande = mejor calidad, pero más lento.
- `whisper.language`: idioma del audio (por defecto `es`).
- `whisper.device` / `compute_type`: `cpu` / `int8` sin GPU; `cuda` /
  `float16` con GPU NVIDIA para acelerar el procesamiento.

## Sobre el resumen

Por ahora la sección `## Resumen` queda como marcador (`_(pendiente)_`) para
completar manualmente. Más adelante se puede conectar un modelo de lenguaje
(local vía [Ollama](https://ollama.com/), o una API externa) que lo genere
automáticamente a partir del transcript.

## Notas adicionales

- La primera vez que se ejecuta el script, se descarga el modelo Whisper
  elegido y queda cacheado localmente para las próximas ejecuciones.
- El nombre del archivo de audio se usa como título de la nota.

## Contribuciones

Sugerencias, reportes de errores y pull requests son bienvenidos.
