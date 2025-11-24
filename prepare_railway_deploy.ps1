#!/usr/bin/env powershell
# prepare_railway_deploy.ps1
# Prepara el proyecto para deploy en Railway

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "  PREPARANDO PROYECTO PARA RAILWAY DEPLOYMENT" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

# Directorio actual
$projectDir = Get-Location
Write-Host "`nDirectorio del proyecto: $projectDir" -ForegroundColor Yellow

# Verificar archivos necesarios
Write-Host "`nVerificando archivos necesarios..." -ForegroundColor Green

$requiredFiles = @(
    "main.py",
    "requirements.txt",
    "Procfile",
    ".env",
    "config",
    "ia",
    "cerebro",
    "analisis",
    "telegram_bot",
    "utils"
)

$allFilesExist = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  OK $file" -ForegroundColor Green
    } else {
        Write-Host "  ERROR: $file (FALTA)" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if (!$allFilesExist) {
    Write-Host "`nFaltan archivos. Verifica que estés en la carpeta correcta." -ForegroundColor Red
    exit 1
}

# Crear lista de archivos a excluir
Write-Host "`nPreparando archivos para upload..." -ForegroundColor Green

# Archivos/carpetas a excluir
$excludePatterns = @(
    "venv_bot",
    ".git",
    "__pycache__",
    "*.pyc",
    ".env",
    "logs",
    ".vscode",
    ".idea",
    "*.egg-info"
)

# Crear ZIP
$zipName = "Bot_Analista_Railway.zip"
$zipPath = Join-Path $projectDir $zipName

Write-Host "`nCreando archivo ZIP: $zipName..." -ForegroundColor Yellow

# Eliminar ZIP anterior si existe
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
    Write-Host "  Archivo anterior eliminado" -ForegroundColor Gray
}

# Crear ZIP con archivos necesarios
$filesToZip = Get-ChildItem -Path $projectDir -Recurse -File | Where-Object {
    $fullPath = $_.FullName
    $skip = $false
    
    foreach ($pattern in $excludePatterns) {
        if ($fullPath -like "*$pattern*") {
            $skip = $true
            break
        }
    }
    
    -not $skip
}

Compress-Archive -Path ($filesToZip.FullName) -DestinationPath $zipPath -Force

$zipSize = (Get-Item $zipPath).Length / 1MB
Write-Host "  OK ZIP creado: $zipSize MB" -ForegroundColor Green

# Resumen
Write-Host "`n====================================================" -ForegroundColor Cyan
Write-Host "  OK PREPARACION COMPLETADA" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Cyan

Write-Host "`n PROXIMOS PASOS:" -ForegroundColor Cyan
Write-Host "  1. Ve a https://railway.app/" -ForegroundColor White
Write-Host "  2. Click en 'Create New Project'" -ForegroundColor White
Write-Host "  3. Selecciona 'Deploy from File'" -ForegroundColor White
Write-Host "  4. Sube este archivo: $zipName" -ForegroundColor Magenta
Write-Host "  5. En Variables, agrega:" -ForegroundColor White
Write-Host "     - TELEGRAM_TOKEN=..." -ForegroundColor Gray
Write-Host "     - GOOGLE_API_KEY=..." -ForegroundColor Gray
Write-Host "  6. Listo! Tu bot corre 24/7" -ForegroundColor Yellow

Write-Host "`n NOTA:" -ForegroundColor Cyan
Write-Host "  El archivo ZIP se encuentra en: $zipPath" -ForegroundColor Gray
Write-Host "  Puedes descargarlo a tu computadora para subirlo a Railway" -ForegroundColor Gray

Write-Host "`n"
