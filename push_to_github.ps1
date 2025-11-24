# Script para enlazar el proyecto a GitHub y hacer push

Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host "           ENLAZAR PROYECTO A GITHUB" -ForegroundColor Cyan
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host ""

# Paso 1: Configurar usuario de git
Write-Host "PASO 1: Configurar usuario de Git..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Ingresa tu email de GitHub (ej: tu.email@gmail.com):" -ForegroundColor White
$email = Read-Host "Email"

Write-Host "Ingresa tu nombre (ej: Tu Nombre):" -ForegroundColor White
$name = Read-Host "Nombre"

git config --global user.email "$email"
git config --global user.name "$name"

Write-Host "Verificando configuracion..." -ForegroundColor Green
git config --global --list | Select-String "user\."

Write-Host ""

# Paso 2: Inicializar repositorio local
Write-Host "PASO 2: Inicializar repositorio local..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    git init
    Write-Host "Repositorio inicializado" -ForegroundColor Green
} else {
    Write-Host "Repositorio ya existe" -ForegroundColor Green
}
Write-Host ""

# Paso 3: Agregar archivos
Write-Host "PASO 3: Agregando archivos al repositorio..." -ForegroundColor Yellow
git add .
Write-Host "Archivos agregados" -ForegroundColor Green
Write-Host ""

# Paso 4: Crear commit inicial
Write-Host "PASO 4: Creando commit inicial..." -ForegroundColor Yellow
git commit -m "Bot Analista A&C - Listo para GitHub y Google IDX"
Write-Host "Commit creado" -ForegroundColor Green
Write-Host ""

# Paso 5: Crear rama main
Write-Host "PASO 5: Configurando rama principal..." -ForegroundColor Yellow
git branch -M main
Write-Host "Rama main configurada" -ForegroundColor Green
Write-Host ""

# Paso 6: Agregar URL remota
Write-Host "PASO 6: Agregar URL del repositorio remoto..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Necesitas la URL de tu repositorio GitHub." -ForegroundColor White
Write-Host "Para obtenerla:" -ForegroundColor Cyan
Write-Host "  1. Ve a https://github.com/new" -ForegroundColor Cyan
Write-Host "  2. Nombre: Bot_Analist_A&C" -ForegroundColor Cyan
Write-Host "  3. Descripcion: Bot de Telegram para analisis financiero con IA" -ForegroundColor Cyan
Write-Host "  4. Selecciona 'Public'" -ForegroundColor Cyan
Write-Host "  5. Click 'Create repository'" -ForegroundColor Cyan
Write-Host "  6. Copia la URL (ej: https://github.com/tu_usuario/Bot_Analist_A&C.git)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ingresa la URL de tu repositorio GitHub:" -ForegroundColor White
$repo_url = Read-Host "URL"

$existing_remote = git remote get-url origin 2>$null
if ($existing_remote) {
    git remote set-url origin "$repo_url"
    Write-Host "URL remota actualizada" -ForegroundColor Green
} else {
    git remote add origin "$repo_url"
    Write-Host "URL remota agregada" -ForegroundColor Green
}
Write-Host ""

# Paso 7: Hacer push
Write-Host "PASO 7: Subiendo codigo a GitHub..." -ForegroundColor Yellow
Write-Host "Esto puede tomar un minuto..." -ForegroundColor White
git push -u origin main
Write-Host "Codigo subido a GitHub" -ForegroundColor Green
Write-Host ""

Write-Host "=======================================================================" -ForegroundColor Green
Write-Host "           PROYECTO ENLAZADO A GITHUB EXITOSAMENTE" -ForegroundColor Green
Write-Host "=======================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "URL de tu repositorio: $repo_url" -ForegroundColor Cyan
Write-Host ""
Write-Host "PROXIMOS PASOS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. OPCION A: Desarrollar en Google IDX" -ForegroundColor White
Write-Host "   URL: https://idx.google.com/import" -ForegroundColor Cyan
Write-Host "   Pega tu URL: $repo_url" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. OPCION B: Desplegar en Railway (24/7)" -ForegroundColor White
Write-Host "   URL: https://railway.app/" -ForegroundColor Cyan
Write-Host "   Sube el archivo: Bot_Analista_Railway.zip" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. OPCION C: Seguir desarrollando localmente" -ForegroundColor White
Write-Host "   Comando: git push (despues de hacer cambios)" -ForegroundColor Cyan
Write-Host ""
Write-Host "=======================================================================" -ForegroundColor Green
