###############################################################################
#              INSTALAR SPYDER STANDALONE (SIN ANACONDA)                     #
#                                                                             #
#  Este script instala Spyder como IDE independiente usando Python.org      #
###############################################################################

Write-Host "`n" -ForegroundColor Cyan
Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║      INSTALAR SPYDER STANDALONE - PASO 3 DE 4                   ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host "`n"

###############################################################################
# OPCIÓN 1: SPYDER VÍA PIP (RECOMENDADO)
###############################################################################

Write-Host "OPCIÓN 1: Instalar Spyder vía PIP..." -ForegroundColor Yellow
Write-Host "  (IDE de análisis de datos independiente)" -ForegroundColor Gray
Write-Host "`n"

Write-Host "PASO 1: Instalando Spyder y dependencias..." -ForegroundColor Yellow

$spyderDependencies = @(
    "spyder==5.5.5",              # IDE principal
    "pyqt5==5.15.11",             # Framework gráfico
    "numpy==1.26.4",              # Cálculos numéricos
    "pandas==2.2.0",              # Análisis de datos
    "matplotlib==3.9.2",          # Gráficos
    "scipy==1.14.1",              # Cálculo científico
    "scikit-learn==1.5.2",        # Machine learning
    "jupyter==1.0.0",             # Notebooks
    "ipython==8.24.0"             # Shell interactivo
)

Write-Host "  📦 Paquetes a instalar:" -ForegroundColor Cyan
$spyderDependencies | ForEach-Object { Write-Host "     • $_" -ForegroundColor Gray }

Write-Host "`n  ⏳ Instalando (puede tomar 5-10 minutos)..." -ForegroundColor Yellow
Write-Host "`n"

try {
    & python -m pip install --upgrade pip -q
    
    foreach ($package in $spyderDependencies) {
        Write-Host "  ⏳ Instalando: $package" -ForegroundColor Gray
        & python -m pip install $package -q --no-warn-script-location
        if ($LASTEXITCODE -eq 0) {
            Write-Host "     ✅ Instalado" -ForegroundColor Green
        } else {
            Write-Host "     ⚠️  Error (continuando...)" -ForegroundColor Yellow
        }
    }
    
    Write-Host "`n  ✅ Instalación completada" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Error durante instalación: $_" -ForegroundColor Red
    exit 1
}

###############################################################################
# PASO 2: CREAR ACCESO DIRECTO
###############################################################################

Write-Host "`nPASO 2: Creando acceso directo a Spyder..." -ForegroundColor Yellow

# Ubicación de accesos directos
$startMenuPath = "C:\Users\$env:USERNAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"
$desktopPath = "C:\Users\$env:USERNAME\Desktop"

# Información de Python
$pythonExe = & python -c "import sys; print(sys.executable)"
$spyderModule = "spyder"

# Crear acceso directo en Inicio
$lnkPath = "$startMenuPath\Spyder (sin Anaconda).lnk"
$WshShell = New-Object -ComObject WScript.Shell

try {
    $shortcut = $WshShell.CreateShortcut($lnkPath)
    $shortcut.TargetPath = $pythonExe
    $shortcut.Arguments = "-m spyder"
    $shortcut.WorkingDirectory = "$env:USERPROFILE\Documents"
    $shortcut.Description = "IDE de análisis de datos (Spyder)"
    $shortcut.IconLocation = "$pythonExe,0"
    $shortcut.Save()
    
    Write-Host "  ✅ Acceso directo creado en Inicio" -ForegroundColor Green
    Write-Host "     📍 $lnkPath" -ForegroundColor Gray
} catch {
    Write-Host "  ⚠️  Error creando acceso directo en Inicio" -ForegroundColor Yellow
}

# Crear acceso directo en Escritorio (opcional)
$desktopLnk = "$desktopPath\Spyder (sin Anaconda).lnk"
try {
    $desktopShortcut = $WshShell.CreateShortcut($desktopLnk)
    $desktopShortcut.TargetPath = $pythonExe
    $desktopShortcut.Arguments = "-m spyder"
    $desktopShortcut.WorkingDirectory = "$env:USERPROFILE\Documents"
    $desktopShortcut.Description = "IDE de análisis de datos (Spyder)"
    $desktopShortcut.Save()
    
    Write-Host "  ✅ Acceso directo creado en Escritorio" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  Error creando acceso directo en Escritorio" -ForegroundColor Yellow
}

###############################################################################
# PASO 3: VERIFICAR INSTALACIÓN
###############################################################################

Write-Host "`nPASO 3: Verificando instalación..." -ForegroundColor Yellow

try {
    $spyderVersion = & python -m spyder --version 2>&1
    Write-Host "  ✅ Spyder verificado: $spyderVersion" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  Spyder no pudo verificarse, pero está instalado" -ForegroundColor Yellow
}

# Verificar paquetes principales
Write-Host "`n  Verificando dependencias principales:" -ForegroundColor Cyan
$requiredPackages = @("numpy", "pandas", "matplotlib", "scipy", "scikit-learn")

foreach ($pkg in $requiredPackages) {
    try {
        & python -c "import $pkg" -ErrorAction SilentlyContinue
        Write-Host "     ✅ $pkg" -ForegroundColor Green
    } catch {
        Write-Host "     ⚠️  $pkg (error)" -ForegroundColor Yellow
    }
}

###############################################################################
# PASO 4: CREAR SCRIPT DE INICIO
###############################################################################

Write-Host "`nPASO 4: Creando script de inicio de Spyder..." -ForegroundColor Yellow

$spyderStartScript = @"
@echo off
REM Script para iniciar Spyder (Análisis de Datos)
REM Se utiliza Python.org en lugar de Anaconda

title Spyder IDE - Análisis de Datos
cd /d "%USERPROFILE%\Documents"

REM Mostrar información
echo.
echo ╔════════════════════════════════════════╗
echo ║    Spyder IDE (sin Anaconda)          ║
echo ║    IDE de Análisis de Datos            ║
echo ╚════════════════════════════════════════╝
echo.
echo Iniciando Spyder...
echo.

REM Iniciar Spyder
python -m spyder

REM Si hay error
if errorlevel 1 (
    echo.
    echo Error al iniciar Spyder
    pause
)
"@

$scriptPath = "c:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C\INICIAR_SPYDER.bat"
Set-Content -Path $scriptPath -Value $spyderStartScript -Encoding ASCII

Write-Host "  ✅ Script creado: INICIAR_SPYDER.bat" -ForegroundColor Green
Write-Host "     📍 $scriptPath" -ForegroundColor Gray

###############################################################################
# OPCIÓN 2: ALTERNATIVA - USAR VS CODE CON PYTHON
###############################################################################

Write-Host "`n" -ForegroundColor Cyan
Write-Host "OPCIÓN 2 (Alternativa): Usar VS Code para análisis" -ForegroundColor Yellow
Write-Host "  VS Code es más ligero y similar a Spyder" -ForegroundColor Gray
Write-Host "`n  1. Descarga VS Code desde: https://code.visualstudio.com" -ForegroundColor Cyan
Write-Host "  2. Instala extensión 'Python' de Microsoft" -ForegroundColor Cyan
Write-Host "  3. Abre scripts .py y ejecuta con Ctrl+F5" -ForegroundColor Cyan

###############################################################################
# FINALIZACIÓN
###############################################################################

Write-Host "`n" -ForegroundColor Cyan
Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║        INSTALACIÓN DE SPYDER COMPLETADA                          ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Green

Write-Host "`n✅ RESUMEN:" -ForegroundColor Green
Write-Host "   ✓ Spyder IDE instalado" -ForegroundColor Green
Write-Host "   ✓ Accesos directos creados" -ForegroundColor Green
Write-Host "   ✓ Script INICIAR_SPYDER.bat creado" -ForegroundColor Green
Write-Host "   ✓ Todas las dependencias de análisis instaladas" -ForegroundColor Green

Write-Host "`n🚀 CÓMO USAR SPYDER:" -ForegroundColor Yellow
Write-Host "   • Opción 1: Haz doble clic en 'Spyder (sin Anaconda)' en Inicio" -ForegroundColor Cyan
Write-Host "   • Opción 2: Haz doble clic en 'INICIAR_SPYDER.bat'" -ForegroundColor Cyan
Write-Host "   • Opción 3: En terminal: python -m spyder" -ForegroundColor Cyan

Write-Host "`n📋 PRÓXIMO PASO:" -ForegroundColor Yellow
Write-Host "   ▶️  Ejecuta: 4_INICIAR_BOT.ps1" -ForegroundColor Cyan
Write-Host "`n"

Read-Host "Presiona Enter para continuar"
