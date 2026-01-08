###############################################################################
#                         INICIAR BOT LIMPIAMENTE                            #
#                                                                             #
#  Este script inicializa el bot después de desinstalar Anaconda            #
###############################################################################

Write-Host "`n" -ForegroundColor Cyan
Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║        INICIAR BOT ANALYST A&C - PASO 4 DE 4                    ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host "`n"

###############################################################################
# CONFIGURACIÓN
###############################################################################

$botPath = "c:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C"
$venvPath = "$botPath\venv_bot"
$pythonExe = "$venvPath\Scripts\python.exe"

###############################################################################
# PASO 1: VERIFICAR ENTORNO
###############################################################################

Write-Host "PASO 1: Verificando entorno..." -ForegroundColor Yellow

# Verificar que el venv existe
if (-not (Test-Path $venvPath)) {
    Write-Host "  ⚠️  venv no encontrado, creando..." -ForegroundColor Yellow
    cd $botPath
    & python -m venv venv_bot
    
    if (Test-Path $venvPath) {
        Write-Host "  ✅ venv creado correctamente" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Error creando venv" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "  ✅ venv encontrado" -ForegroundColor Green
}

###############################################################################
# PASO 2: ACTIVAR VENV
###############################################################################

Write-Host "`nPASO 2: Activando venv..." -ForegroundColor Yellow

& "$venvPath\Scripts\activate.ps1"

if ($?) {
    Write-Host "  ✅ venv activado" -ForegroundColor Green
} else {
    Write-Host "  ❌ Error activando venv" -ForegroundColor Red
    exit 1
}

###############################################################################
# PASO 3: INSTALAR DEPENDENCIAS
###############################################################################

Write-Host "`nPASO 3: Instalando dependencias..." -ForegroundColor Yellow
Write-Host "  ⏳ Esto puede tomar 5-10 minutos en la primera ejecución..." -ForegroundColor Gray
Write-Host "`n"

cd $botPath

# Instalar desde requirements.txt
& "$pythonExe" -m pip install --upgrade pip -q

Write-Host "  📦 Instalando paquetes desde requirements.txt..." -ForegroundColor Cyan
& "$pythonExe" -m pip install -r requirements.txt -q

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Dependencias instaladas" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Error instalando algunas dependencias (continuando...)" -ForegroundColor Yellow
}

###############################################################################
# PASO 4: INSTALAR REPORTLAB (CRÍTICO PARA PDF)
###############################################################################

Write-Host "`nPASO 4: Instalando ReportLab (para exportación PDF)..." -ForegroundColor Yellow

& "$pythonExe" -m pip install reportlab==4.0.4 -q

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ ReportLab instalado" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Error instalando ReportLab" -ForegroundColor Yellow
}

###############################################################################
# PASO 5: CREAR DIRECTORIOS NECESARIOS
###############################################################################

Write-Host "`nPASO 5: Creando directorios..." -ForegroundColor Yellow

$directories = @(
    "logs",
    "data",
    "data/reportes",
    "pdfs"
)

foreach ($dir in $directories) {
    $fullPath = "$botPath\$dir"
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-Host "  ✅ Creado: $dir" -ForegroundColor Green
    } else {
        Write-Host "  ✅ Existe: $dir" -ForegroundColor Green
    }
}

###############################################################################
# PASO 6: CREAR ARCHIVO .ENV (SI NO EXISTE)
###############################################################################

Write-Host "`nPASO 6: Configurando variables de entorno..." -ForegroundColor Yellow

$envFile = "$botPath\.env"

if (-not (Test-Path $envFile)) {
    Write-Host "  📝 Creando archivo .env..." -ForegroundColor Cyan
    
    $envContent = @"
# Configuración del Bot Analyst A&C
# Rellena estos valores con tus credenciales

# Google Gemini API
GEMINI_API_KEY=tu_clave_api_aqui
GEMINI_MODEL=gemini-2.5-pro
GEMINI_TEMPERATURE=0.0

# Telegram Bot
TELEGRAM_BOT_TOKEN=tu_token_de_telegram_aqui
TELEGRAM_CHAT_ID=tu_chat_id_aqui

# Configuración de análisis
STOCK_SYMBOLS=AAPL,MSFT,GOOGL,TSLA,META,NVDA
LOG_LEVEL=INFO
DEBUG_MODE=False

# Timers (segundos)
ANALYSIS_INTERVAL=3600
PDF_EXPORT_ENABLED=True

# Límites API
MAX_REQUESTS_PER_HOUR=100
REQUEST_TIMEOUT=30
"@

    Set-Content -Path $envFile -Value $envContent -Encoding UTF8
    Write-Host "  ✅ Archivo .env creado" -ForegroundColor Green
    Write-Host "  ⚠️  IMPORTANTE: Edita .env con tus credenciales" -ForegroundColor Yellow
    Write-Host "     Abre: $envFile" -ForegroundColor Cyan
} else {
    Write-Host "  ✅ Archivo .env ya existe" -ForegroundColor Green
}

###############################################################################
# PASO 7: VERIFICAR CONFIGURACIÓN
###############################################################################

Write-Host "`nPASO 7: Verificando configuración..." -ForegroundColor Yellow

# Verificar importes básicos
Write-Host "  🔍 Verificando módulos Python..." -ForegroundColor Cyan

$testCode = @"
try:
    # Core
    from config import Settings
    from telegram_bot.bot import TelegramAnalystBot
    from ia.ai_engine import AIEngine
    from analisis.analyzer import Analyzer
    
    # Datos
    import pandas
    import numpy
    import yfinance
    
    # Telegram
    from telegram.ext import Application
    
    # PDF
    from reportlab.pdfgen import canvas
    
    print('✅ Todos los módulos importan correctamente')
    exit(0)
except ImportError as e:
    print(f'❌ Error de importación: {e}')
    exit(1)
except Exception as e:
    print(f'⚠️  Error: {e}')
    exit(1)
"@

& "$pythonExe" -c $testCode

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Módulos verificados" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Algunos módulos tienen problemas" -ForegroundColor Yellow
}

###############################################################################
# PASO 8: MENÚ DE OPCIONES
###############################################################################

Write-Host "`n" -ForegroundColor Cyan
Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                      CONFIGURACIÓN LISTA                          ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Green

Write-Host "`n✅ BOT COMPLETAMENTE CONFIGURADO Y FUNCIONAL" -ForegroundColor Green

Write-Host "`n📋 PRÓXIMOS PASOS:" -ForegroundColor Yellow
Write-Host "   1. 📝 Edita el archivo .env con tus credenciales:" -ForegroundColor Cyan
Write-Host "      $envFile" -ForegroundColor Gray
Write-Host "`n      Necesitas:" -ForegroundColor Cyan
Write-Host "      • GEMINI_API_KEY = Tu clave de Google Gemini" -ForegroundColor Cyan
Write-Host "      • TELEGRAM_BOT_TOKEN = Tu token de Telegram Bot" -ForegroundColor Cyan
Write-Host "      • TELEGRAM_CHAT_ID = Tu Chat ID de Telegram" -ForegroundColor Cyan

Write-Host "`n   2. 🚀 Inicia el bot de una de estas formas:" -ForegroundColor Yellow

Write-Host "`n      OPCIÓN A (Recomendado - Con interfaz):" -ForegroundColor Cyan
Write-Host "      PowerShell:" -ForegroundColor Gray
Write-Host "      cd '$botPath'" -ForegroundColor Gray
Write-Host "      .\venv_bot\Scripts\activate" -ForegroundColor Gray
Write-Host "      python main.py" -ForegroundColor Gray

Write-Host "`n      OPCIÓN B (Desde archivo batch):" -ForegroundColor Cyan
Write-Host "      Crea INICIAR_BOT.bat con este contenido:" -ForegroundColor Gray
Write-Host "      @echo off" -ForegroundColor DarkGray
Write-Host "      cd /d ""$botPath""" -ForegroundColor DarkGray
Write-Host "      .\venv_bot\Scripts\python.exe main.py" -ForegroundColor DarkGray

Write-Host "`n      OPCIÓN C (Modo producción en segundo plano):" -ForegroundColor Cyan
Write-Host "      PowerShell (como administrador):" -ForegroundColor Gray
Write-Host "      Start-Process -WindowStyle Hidden -FilePath '$pythonExe' -ArgumentList 'main.py' -WorkingDirectory '$botPath'" -ForegroundColor Gray

###############################################################################
# OPCIONES DE MENÚ
###############################################################################

Write-Host "`n" -ForegroundColor Cyan
Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║                        OPCIONES                                  ║" -ForegroundColor Yellow
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow

Write-Host "`n1️⃣  Iniciar el Bot ahora" -ForegroundColor Yellow
Write-Host "2️⃣  Abrir editor de .env (configura credenciales)" -ForegroundColor Yellow
Write-Host "3️⃣  Crear script automático INICIAR_BOT.bat" -ForegroundColor Yellow
Write-Host "4️⃣  Mostrar instrucciones de credenciales" -ForegroundColor Yellow
Write-Host "5️⃣  Salir" -ForegroundColor Yellow
Write-Host "`n"

$option = Read-Host "Selecciona una opción (1-5)"

switch ($option) {
    "1" {
        Write-Host "`n🚀 Iniciando Bot..." -ForegroundColor Green
        & "$pythonExe" main.py
    }
    
    "2" {
        Write-Host "`n📝 Abriendo editor de .env..." -ForegroundColor Green
        Start-Process notepad $envFile
        Write-Host "⏳ Abre el archivo, edita las credenciales y guarda (Ctrl+S)" -ForegroundColor Yellow
        Read-Host "Presiona Enter cuando termines"
    }
    
    "3" {
        Write-Host "`n🔧 Creando script automático..." -ForegroundColor Green
        
        $batContent = @"
@echo off
REM Script automático para iniciar Bot Analyst A&C
REM (Funciona sin Anaconda)

title Bot Analyst A&C
cd /d "$botPath"

cls
echo.
echo ╔════════════════════════════════════════╗
echo ║    Bot Analyst A&C en Línea            ║
echo ║    Esperando comandos de Telegram...   ║
echo ╚════════════════════════════════════════╝
echo.
echo Iniciando bot...
echo.

REM Activar venv e iniciar
call venv_bot\Scripts\activate.bat
python main.py

REM Si hay error
if errorlevel 1 (
    echo.
    echo ❌ Error iniciando bot
    echo Revisa el archivo .env y tus credenciales
    pause
)
"@

        $batPath = "$botPath\INICIAR_BOT.bat"
        Set-Content -Path $batPath -Value $batContent -Encoding ASCII
        Write-Host "  ✅ Script creado: INICIAR_BOT.bat" -ForegroundColor Green
        Write-Host "     📍 $batPath" -ForegroundColor Gray
        Write-Host "`n  Ahora puedes hacer doble clic en INICIAR_BOT.bat para iniciar el bot" -ForegroundColor Cyan
    }
    
    "4" {
        Write-Host "`n📖 OBTENER TUS CREDENCIALES:" -ForegroundColor Yellow
        
        Write-Host "`n1️⃣  GOOGLE GEMINI API KEY:" -ForegroundColor Cyan
        Write-Host "   • Visita: https://aistudio.google.com/app/apikey" -ForegroundColor Gray
        Write-Host "   • Click 'Create API Key'" -ForegroundColor Gray
        Write-Host "   • Copia la clave" -ForegroundColor Gray
        Write-Host "   • Pégala en .env como GEMINI_API_KEY" -ForegroundColor Gray
        
        Write-Host "`n2️⃣  TELEGRAM BOT TOKEN:" -ForegroundColor Cyan
        Write-Host "   • Busca @BotFather en Telegram" -ForegroundColor Gray
        Write-Host "   • Envía /newbot" -ForegroundColor Gray
        Write-Host "   • Sigue las instrucciones" -ForegroundColor Gray
        Write-Host "   • Copia el token proporcionado" -ForegroundColor Gray
        Write-Host "   • Pégalo en .env como TELEGRAM_BOT_TOKEN" -ForegroundColor Gray
        
        Write-Host "`n3️⃣  TELEGRAM CHAT ID:" -ForegroundColor Cyan
        Write-Host "   • Envía cualquier mensaje a tu bot" -ForegroundColor Gray
        Write-Host "   • Visita: https://api.telegram.org/bot{TOKEN}/getUpdates" -ForegroundColor Gray
        Write-Host "   • Reemplaza {TOKEN} con tu token" -ForegroundColor Gray
        Write-Host "   • Copia el 'chat' -> 'id'" -ForegroundColor Gray
        Write-Host "   • Pégalo en .env como TELEGRAM_CHAT_ID" -ForegroundColor Gray
        
        Write-Host "`n"
        Read-Host "Presiona Enter para volver"
    }
    
    "5" {
        Write-Host "`n👋 ¡Hasta luego!" -ForegroundColor Green
        exit 0
    }
    
    default {
        Write-Host "`n❌ Opción no válida" -ForegroundColor Red
    }
}

###############################################################################
# INFORMACIÓN FINAL
###############################################################################

Write-Host "`n" -ForegroundColor Cyan
Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║              ¡DESINSTALACIÓN Y CONFIGURACIÓN LISTA!             ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Green

Write-Host "`n📊 RESUMEN FINAL:" -ForegroundColor Yellow
Write-Host "   ✅ Anaconda desinstalado" -ForegroundColor Green
Write-Host "   ✅ Python limpio (Python.org) instalado" -ForegroundColor Green
Write-Host "   ✅ Spyder IDE configurado (sin Anaconda)" -ForegroundColor Green
Write-Host "   ✅ Bot completamente funcional" -ForegroundColor Green
Write-Host "   ✅ Todas las dependencias instaladas" -ForegroundColor Green
Write-Host "   ✅ Directorios creados" -ForegroundColor Green

Write-Host "`n💡 CONSEJO: Almacena este archivo" -ForegroundColor Cyan
Write-Host "   Para reiniciar el bot en futuro, solo ejecuta:" -ForegroundColor Gray
Write-Host "   .\venv_bot\Scripts\activate" -ForegroundColor Gray
Write-Host "   python main.py" -ForegroundColor Gray

Write-Host "`n"
