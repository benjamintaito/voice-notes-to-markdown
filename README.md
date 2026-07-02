# voice-notes

Transcribe tus notas de voz (reuniones, ideas, etc.) usando Whisper local
(`faster-whisper`) y genera una nota `.md` lista para Obsidian con título,
resumen (pendiente de completar) y transcript.

## Cómo funciona

1. Dejás tus audios en `audios_pendientes/`.
2. Corrés el script.
3. Por cada audio se crea un `.md` en `notas/` (título + sección de resumen
   vacía + transcript completo) y el audio se mueve a `audios_procesados/`.

Si algo falla al procesar un audio en particular, se deja en
`audios_pendientes/` para reintentar y el script sigue con el resto.

## Instalación

Requisitos: Python 3.10+ (probado hasta 3.13; con 3.14 puede haber problemas
de compatibilidad con dependencias de `faster-whisper`/`ctranslate2` — si te
falla la instalación, probá con una versión de Python un poco más vieja) y
**ffmpeg** instalado y en el PATH.

```powershell
# Instalar ffmpeg si no lo tenés
winget install ffmpeg

# Crear entorno virtual e instalar dependencias
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

## Uso

```powershell
.venv\Scripts\python.exe process.py
```

O simplemente doble click en `procesar.bat`.

## Configuración (`config.yaml`)

- `paths.notas`: podés apuntar esta carpeta directo a una subcarpeta de tu
  vault de Obsidian para que las notas aparezcan ahí automáticamente.
- `whisper.model_size`: `tiny` / `base` / `small` / `medium` / `large-v3`.
  Más grande = mejor calidad pero más lento. `small` es un buen balance en CPU.
- `whisper.language`: `es` por default.
- `whisper.device` / `compute_type`: dejar `cpu` / `int8` si no tenés GPU
  NVIDIA; si tenés GPU con CUDA podés usar `cuda` / `float16` para que sea
  mucho más rápido.

## Sobre el resumen

Por ahora el script deja la sección `## Resumen` con un placeholder
`_(pendiente)_` — la idea es completarlo a mano o, más adelante, conectar un
modelo (local vía Ollama, o la API de OpenAI) que lo genere automáticamente
a partir del transcript.

## Notas

- La primera vez que corrés el script, `faster-whisper` descarga el modelo
  elegido (unos cientos de MB a un par de GB según el tamaño) y lo cachea
  localmente para las próximas corridas.
- El primer nombre de archivo de audio se usa como título de la nota
  (guiones/underscores se convierten en espacios). Renombrá el audio antes
  de procesarlo si querés un título más prolijo.
