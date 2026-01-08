@echo off
REM Script para iniciar el bot sin interferencia de Anaconda
REM =========================================================

REM Limpiar todas las variables de entorno de Python/Anaconda
set PYTHONHOME=
set PYTHONPATH=
set CONDA_DEFAULT_ENV=
set CONDA_PREFIX=
set CONDA_PREFIX_1=

REM Limpiar PATH de rutas de Anaconda
setlocal enabledelayedexpansion
set "PATH=C:\Windows\System32;C:\Windows"

REM Agregar solo el path del venv
set "PATH=C:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C\venv_bot\Scripts;!PATH!"

REM Cambiar al directorio del bot
cd /d "C:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C"

REM Iniciar el bot
echo ============================================================
echo Iniciando Bot Analista A^&C sin interferencia de Anaconda
echo ============================================================
echo.

python main.py

pause
