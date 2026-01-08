@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM               INICIAR SPYDER IDE (SIN ANACONDA)
REM ═══════════════════════════════════════════════════════════════════════════
REM 
REM Este script inicia Spyder directamente sin depender de Anaconda
REM Perfecto para análisis de datos y desarrollo científico
REM

color 0A
title Spyder IDE - Análisis de Datos

cls
echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                                                                        ║
echo ║              SPYDER IDE - ANÁLISIS DE DATOS                           ║
echo ║                                                                        ║
echo ║        IDE para análisis científico y desarrollo de datos             ║
echo ║                                                                        ║
echo ║              (Sin depender de Anaconda)                               ║
echo ║                                                                        ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.
echo.
echo 📂 Iniciando Spyder...
echo.

REM Cambiar al directorio de documentos
cd /d "%USERPROFILE%\Documents"

REM Iniciar Spyder
python -m spyder

REM Si hay error
if errorlevel 1 (
    echo.
    echo ╔════════════════════════════════════════════════════════════════════════╗
    echo ║                          ERROR                                         ║
    echo ╚════════════════════════════════════════════════════════════════════════╝
    echo.
    echo ❌ Error al iniciar Spyder
    echo.
    echo 💡 Posibles soluciones:
    echo    1. Abre PowerShell en el directorio del bot
    echo    2. Ejecuta: .\venv_bot\Scripts\activate
    echo    3. Luego: python -m spyder
    echo.
    echo 📝 Si necesitas reinstalar:
    echo    1. Abre PowerShell
    echo    2. Ejecuta: python -m pip install --upgrade spyder
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo ✅ Spyder cerrado
    echo.
)

exit /b 0
