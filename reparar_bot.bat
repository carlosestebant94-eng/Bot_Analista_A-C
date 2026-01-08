@echo off
REM =============================================================================
REM SOLUCIÓN DEFINITIVA: Limpiar Anaconda y configurar Python limpio
REM =============================================================================
REM Este script:
REM 1. Identifica si Anaconda está interfiriendo
REM 2. Proporciona instrucciones para eliminarla
REM 3. Restaura Python limpio del venv
REM =============================================================================

setlocal enabledelayedexpansion

cls
echo.
echo =============================================================================
echo DIAGNÓSTICO Y SOLUCIÓN DEL PROBLEMA CON ANACONDA
echo =============================================================================
echo.

REM Verificar si Anaconda está en el PATH
echo Buscando Anaconda en el sistema...
where conda >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo PROBLEMA ENCONTRADO: Anaconda está instalado en el sistema
    echo.
    echo Anaconda interfiere con el venv porque:
    echo   1. Sus librerías .pyd están compiladas para versiones específicas
    echo   2. Carga desde C:\ProgramData\anaconda3 en lugar del venv
    echo   3. Causa conflictos con numpy, pandas, beautifulsoup4, etc.
    echo.
    echo SOLUCIÓN: Tienes 2 opciones
    echo =============================================================================
    echo.
    echo OPCIÓN 1: USAR DOCKER (RECOMENDADO - Sin instalar nada más)
    echo ─────────────────────────────────────────────────────────────────────────────
    echo Requisitos: Descargar Docker Desktop https://www.docker.com/products/docker-desktop
    echo.
    echo Pasos:
    echo   1. Instala Docker Desktop
    echo   2. Ejecuta en PowerShell (como administrador):
    echo.
    echo      docker build -t bot-analista:latest .
    echo      docker run --env-file .env bot-analista:latest
    echo.
    echo El bot funcionará sin problemas en un contenedor aislado.
    echo.
    echo =============================================================================
    echo.
    echo OPCIÓN 2: DESINSTALAR ANACONDA (Más manual pero permanente)
    echo ─────────────────────────────────────────────────────────────────────────────
    echo Pasos:
    echo   1. Ir a: Configuración ^> Apps ^> Programas y características
    echo   2. Buscar "Anaconda3" y desinstalar completamente
    echo   3. Reiniciar Windows
    echo   4. Luego ejecutar este script de nuevo
    echo.
    echo =============================================================================
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Anaconda no encontrado en PATH
    echo Procediendo con venv limpio...
    echo.
)

REM Configurar environment limpio
set PYTHONHOME=
set PYTHONPATH=
set CONDA_DEFAULT_ENV=
set CONDA_PREFIX=
set CONDA_PREFIX_1=
set PATH=C:\Windows\System32;C:\Windows;C:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C\venv_bot\Scripts

REM Cambiar directorio
cd /d "C:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C"

echo Iniciando bot con ambiente limpio...
echo.

python main.py

pause
