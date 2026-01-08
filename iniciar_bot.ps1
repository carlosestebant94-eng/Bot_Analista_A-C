# Script PowerShell para iniciar el bot sin Anaconda
# =======================================================

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Iniciando Bot Analista A&C sin interferencia de Anaconda" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Limpiar entorno
$env:PYTHONHOME = ""
$env:PYTHONPATH = ""
$env:CONDA_DEFAULT_ENV = ""
$env:CONDA_PREFIX = ""
$env:CONDA_PREFIX_1 = ""

# Configurar PATH solo con lo esencial + venv
$venvPath = "C:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C\venv_bot\Scripts"
$basePath = @(
    $venvPath,
    "C:\Windows\System32",
    "C:\Windows"
) -join ";"

$env:PATH = $basePath

# Cambiar directorio
Set-Location -Path "C:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C"

Write-Host "Entorno preparado:" -ForegroundColor Yellow
Write-Host "  PYTHONHOME: (vacío)" -ForegroundColor Gray
Write-Host "  PYTHONPATH: (vacío)" -ForegroundColor Gray
Write-Host "  PATH: venv_bot/Scripts primero" -ForegroundColor Gray
Write-Host ""
Write-Host "Ejecutando bot..." -ForegroundColor Cyan
Write-Host ""

# Iniciar el bot con el Python del venv
& "C:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C\venv_bot\Scripts\python.exe" main.py

Write-Host ""
Write-Host "Bot detenido" -ForegroundColor Red
