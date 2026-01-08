###############################################################################
#                    INSTALAR PYTHON LIMPIO (PYTHON.ORG)                    #
#                                                                             #
#  Este script descarga e instala Python 3.12 de python.org                 #
###############################################################################

Write-Host "`n" -ForegroundColor Cyan
Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║         INSTALAR PYTHON 3.12 - PASO 2 DE 4                      ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host "`n"

# Verificar que estamos en Windows
if ($PSVersionTable.Platform -ne "Win32NT" -and $PSVersionTable.Platform -ne $null) {
    Write-Host "❌ Este script solo funciona en Windows" -ForegroundColor Red
    exit 1
}

###############################################################################
# PASO 1: DESCARGAR PYTHON
###############################################################################

Write-Host "PASO 1: Descargando Python 3.12..." -ForegroundColor Yellow

$pythonUrl = "https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe"
$downloadPath = "$env:TEMP\python-3.12.7-amd64.exe"

Write-Host "  📥 Descargando desde: python.org" -ForegroundColor Cyan
Write-Host "  📍 Destino: $downloadPath" -ForegroundColor Gray

try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    $progressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri $pythonUrl -OutFile $downloadPath -UseBasicParsing
    
    if (Test-Path $downloadPath) {
        $fileSize = (Get-Item $downloadPath).Length / 1MB
        Write-Host "  ✅ Descarga completada ($([Math]::Round($fileSize, 2)) MB)" -ForegroundColor Green
    } else {
        throw "El archivo no se descargó correctamente"
    }
} catch {
    Write-Host "  ❌ Error en descarga: $_" -ForegroundColor Red
    Write-Host "  💡 Descarga manual: $pythonUrl" -ForegroundColor Yellow
    Read-Host "Presiona Enter para continuar"
    exit 1
}

###############################################################################
# PASO 2: INSTALAR PYTHON
###############################################################################

Write-Host "`nPASO 2: Instalando Python..." -ForegroundColor Yellow
Write-Host "  ⚙️  Ejecutando instalador..." -ForegroundColor Cyan
Write-Host "  💡 Se abrirá el asistente de instalación" -ForegroundColor Gray
Write-Host "`n     IMPORTANTE: Marca ✅ 'Add Python to PATH'" -ForegroundColor Yellow
Write-Host "     (opción abajo a la izquierda)" -ForegroundColor Yellow
Write-Host "`n"

# Ejecutar instalador
& $downloadPath

# Esperar a que termine la instalación
Start-Sleep -Seconds 5
while (Get-Process python* -ErrorAction SilentlyContinue) {
    Start-Sleep -Seconds 1
}
Start-Sleep -Seconds 3

###############################################################################
# PASO 3: VERIFICAR INSTALACIÓN
###############################################################################

Write-Host "`nPASO 3: Verificando instalación..." -ForegroundColor Yellow

# Refrescar variables de entorno
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCmd) {
    $pythonVersion = & python --version 2>&1
    Write-Host "  ✅ Python encontrado: $pythonVersion" -ForegroundColor Green
    Write-Host "     Ubicación: $($pythonCmd.Source)" -ForegroundColor Gray
} else {
    Write-Host "  ⚠️  Python no encontrado en PATH" -ForegroundColor Yellow
    Write-Host "  💡 Intenta reiniciar PowerShell" -ForegroundColor Cyan
    
    # Intentar ubicación estándar
    $pythonExe = "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python312\python.exe"
    if (Test-Path $pythonExe) {
        Write-Host "  ✅ Encontrado en: $pythonExe" -ForegroundColor Green
    } else {
        Write-Host "  ❌ No se encontró Python en ubicación estándar" -ForegroundColor Red
        Read-Host "Presiona Enter"
        exit 1
    }
}

###############################################################################
# PASO 4: INSTALAR PIP
###############################################################################

Write-Host "`nPASO 4: Instalando/Actualizando PIP..." -ForegroundColor Yellow

try {
    & python -m pip install --upgrade pip -q
    Write-Host "  ✅ PIP actualizado" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  Error actualizando PIP: $_" -ForegroundColor Yellow
}

###############################################################################
# PASO 5: VERIFICAR PIP
###############################################################################

Write-Host "`nPASO 5: Verificando PIP..." -ForegroundColor Yellow

try {
    $pipVersion = & python -m pip --version
    Write-Host "  ✅ $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  Error verificando PIP" -ForegroundColor Yellow
}

###############################################################################
# FINALIZACIÓN
###############################################################################

Write-Host "`n" -ForegroundColor Cyan
Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║         INSTALACIÓN DE PYTHON COMPLETADA                         ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Green

Write-Host "`n📋 PRÓXIMO PASO:" -ForegroundColor Yellow
Write-Host "   ▶️  Ejecuta: 3_INSTALAR_SPYDER_STANDALONE.ps1" -ForegroundColor Cyan
Write-Host "`n"

# Limpiar archivo descargado
if (Test-Path $downloadPath) {
    Remove-Item -Path $downloadPath -Force -ErrorAction SilentlyContinue
}

Read-Host "Presiona Enter para continuar"
