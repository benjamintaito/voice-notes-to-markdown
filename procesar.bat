@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
    echo No se encontro el entorno virtual .venv. Ejecutar primero:
    echo   python -m venv .venv
    echo   .venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)
.venv\Scripts\python.exe process.py
pause
