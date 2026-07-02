# Voice Notes

Transcribe notas de voz (reuniones, ideas, apuntes personales, etc.) usando
[Whisper](https://github.com/openai/whisper) de forma **100% local**, sin
enviar el audio a ningún servicio en la nube, y genera automáticamente una
nota en formato Markdown lista para usar en [Obsidian](https://obsidian.md/)
(o en cualquier editor de texto plano), con título, sección de resumen y
transcript completo.

## ¿Cómo funciona?

1. Se colocan los archivos de audio en la carpeta `audios_pendientes/`.
2. Se ejecuta el script.
3. Por cada audio se genera un archivo `.md` en `notas/` (título + sección de
   resumen + transcript) y el audio original se mueve a `audios_procesados/`.

Si ocurre un error al procesar un audio, ese archivo se deja en
`audios_pendientes/` para reintentar más tarde, y el script continúa con el
resto sin interrumpirse.

## Requisitos

- Python 3.10 o superior (probado hasta 3.13; con versiones muy nuevas,
  como 3.14, pueden surgir problemas de compatibilidad con las dependencias
  de `faster-whisper`; en ese caso se recomienda usar una versión anterior).
- [ffmpeg](https://ffmpeg.org/) instalado y disponible en el PATH del sistema.
- Git (solo para clonar el repositorio).

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/benjamintaito/voice-notes.git
cd voice-notes
```

### 2. Instalar ffmpeg

En Windows (con [winget](https://learn.microsoft.com/windows/package-manager/winget/)):

```powershell
winget install ffmpeg
```

En macOS (con [Homebrew](https://brew.sh/)):

```bash
brew install ffmpeg
```

En Linux (Debian/Ubuntu):

```bash
sudo apt install ffmpeg
```

### 3. Crear un entorno virtual e instalar las dependencias

En Windows:

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

En macOS/Linux:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Uso

Colocar los archivos de audio a transcribir dentro de la carpeta
`audios_pendientes/` y luego ejecutar:

En Windows:

```powershell
.venv\Scripts\python.exe process.py
```

O bien, hacer doble clic en `procesar.bat`.

En macOS/Linux:

```bash
.venv/bin/python process.py
```

Al finalizar, las notas generadas van a estar disponibles en la carpeta
`notas/` y los audios ya procesados en `audios_procesados/`.

## Configuración (`config.yaml`)

- `paths.notas`: se puede apuntar esta carpeta directamente a una subcarpeta
  del vault de Obsidian, para que las notas aparezcan ahí automáticamente.
- `whisper.model_size`: `tiny`, `base`, `small`, `medium` o `large-v3`. Un
  modelo más grande da mejor calidad pero es más lento. `small` es un buen
  punto de partida en CPU.
- `whisper.language`: idioma del audio (por defecto `es`).
- `whisper.device` / `whisper.compute_type`: mantener `cpu` / `int8` si no se
  cuenta con una GPU NVIDIA; con GPU compatible con CUDA se puede usar
  `cuda` / `float16` para acelerar el procesamiento.

## Sobre el resumen

Por el momento, el script deja la sección `## Resumen` con un texto de
marcador (`_(pendiente)_`) para completar manualmente. La idea es, en el
futuro, poder conectar un modelo de lenguaje (local, por ejemplo vía
[Ollama](https://ollama.com/), o mediante alguna API externa) que genere ese
resumen de forma automática a partir del transcript.

## Notas adicionales

- La primera vez que se ejecuta el script, `faster-whisper` descarga el
  modelo elegido (entre unos cientos de MB y un par de GB, según el tamaño)
  y lo guarda en caché local para las próximas ejecuciones.
- El nombre del archivo de audio se usa como título de la nota (los guiones
  y guiones bajos se convierten en espacios). Se recomienda renombrar el
  audio antes de procesarlo si se desea un título más prolijo.

## Contribuciones

Las sugerencias, reportes de errores y pull requests son bienvenidos. Este
proyecto es de código abierto y puede adaptarse libremente a otros flujos de
trabajo.

## Licencia

[MIT](LICENSE)
