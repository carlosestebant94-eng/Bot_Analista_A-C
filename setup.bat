@echo off
REM Bot Analista A&C - Setup Script para Google IDX (Windows)

echo ==================================================
echo   Configurando Bot Analista A&C en Google IDX
echo ==================================================

REM Crear entorno virtual
echo.
echo Creando entorno virtual...
python -m venv venv

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo.
echo Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Crear directorios necesarios
echo.
echo Creando directorios...
if not exist logs mkdir logs
if not exist data mkdir data
if not exist pdfs mkdir pdfs

REM Mostrar instrucciones
echo.
echo ==================================================
echo   CONFIGURACION COMPLETADA
echo ==================================================
echo.
echo PROXIMOS PASOS:
echo 1. Configura tu .env con:
echo    TELEGRAM_TOKEN=tu_token
echo    GOOGLE_API_KEY=tu_api_key
echo.
echo 2. Ejecuta el bot:
echo    venv\Scripts\activate.bat
echo    python main.py
echo.
echo 3. O usa el comando de ejecucion: 'Ejecutar Bot'
echo.
pause
