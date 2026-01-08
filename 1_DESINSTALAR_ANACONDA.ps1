###############################################################################
#                    DESINSTALAR ANACONDA LIMPIAMENTE                        #
#                                                                             #
#  Este script desinstala Anaconda de forma segura sin romper nada más      #
###############################################################################

Write-Host "`n" -ForegroundColor Cyan
Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║         DESINSTALAR ANACONDA - PASO 1 DE 4                       ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host "`n"

# Verificar que estamos en Windows
if ($PSVersionTable.Platform -ne "Win32NT" -and $PSVersionTable.Platform -ne $null) {
    Write-Host "❌ Este script solo funciona en Windows" -ForegroundColor Red
    exit 1
}

# Verificar permisos de administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "⚠️  Este script necesita ejecutarse como ADMINISTRADOR" -ForegroundColor Yellow
    Write-Host "   Haz clic derecho en PowerShell y selecciona 'Ejecutar como administrador'" -ForegroundColor Yellow
    Read-Host "Presiona Enter para cerrar"
    exit 1
}

Write-Host "✅ Ejecutando como administrador" -ForegroundColor Green
Write-Host "`n"

###############################################################################
# PASO 1: DETENER PROCESOS PYTHON
###############################################################################

Write-Host "PASO 1: Deteniendo procesos Python..." -ForegroundColor Yellow

$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    Write-Host "  Encontrados procesos Python ejecutándose..." -ForegroundColor Gray
    Stop-Process -Name python -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    Write-Host "  ✅ Procesos detenidos" -ForegroundColor Green
} else {
    Write-Host "  ✅ No hay procesos Python ejecutándose" -ForegroundColor Green
}

###############################################################################
# PASO 2: CREAR BACKUP DE ARCHIVOS IMPORTANTES
###############################################################################

Write-Host "`nPASO 2: Creando backup..." -ForegroundColor Yellow

$backupPath = "C:\Users\$env:USERNAME\Anaconda_Backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Write-Host "  📦 Backup se guardará en: $backupPath" -ForegroundColor Cyan

# Verificar si existen ambientes conda personalizados
$condaEnvsPath = "C:\Users\$env:USERNAME\anaconda3\envs"
if (Test-Path $condaEnvsPath) {
    $customEnvs = Get-ChildItem $condaEnvsPath -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -ne "base" }
    if ($customEnvs.Count -gt 0) {
        Write-Host "  ⚠️  Se encontraron ambientes conda personalizados:" -ForegroundColor Yellow
        $customEnvs | ForEach-Object { Write-Host "     - $($_.Name)" -ForegroundColor Gray }
        
        Write-Host "  📦 Se harán copias de seguridad..." -ForegroundColor Cyan
        New-Item -ItemType Directory -Path $backupPath -Force -ErrorAction SilentlyContinue | Out-Null
        Copy-Item -Path $condaEnvsPath -Destination "$backupPath\envs" -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "  ✅ Backup de ambientes creado" -ForegroundColor Green
    }
}

###############################################################################
# PASO 3: DESINSTALAR ANACONDA VÍA REGISTRY
###############################################################################

Write-Host "`nPASO 3: Desinstalando Anaconda..." -ForegroundColor Yellow

# Buscar Anaconda en el registro
$anacondaKey = Get-Item "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*" -ErrorAction SilentlyContinue | 
    Where-Object { $_.GetValue("DisplayName") -like "*Anaconda*" }

if ($anacondaKey) {
    $uninstallString = $anacondaKey.GetValue("UninstallString")
    $displayName = $anacondaKey.GetValue("DisplayName")
    
    Write-Host "  🔍 Encontrado: $displayName" -ForegroundColor Cyan
    Write-Host "  🗑️  Ejecutando desinstalador..." -ForegroundColor Gray
    
    # Ejecutar desinstalador silenciosamente
    if ($uninstallString -like "*MsiExec*") {
        # Es un MSI
        $msiPath = $uninstallString -replace '/I|/X', '' -replace '\s+/.*', ''
        Write-Host "  ℹ️  MSI encontrado" -ForegroundColor Gray
        
        cmd /c $uninstallString /quiet /norestart 2>$null
        Start-Sleep -Seconds 10
    } else {
        # Es un ejecutable
        Write-Host "  ℹ️  Ejecutable encontrado" -ForegroundColor Gray
        & cmd /c $uninstallString /S 2>$null
        Start-Sleep -Seconds 10
    }
    
    Write-Host "  ✅ Desinstalador ejecutado" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  No se encontró Anaconda en el registro" -ForegroundColor Yellow
    Write-Host "  💡 Nota: Es posible que ya esté desinstalado" -ForegroundColor Cyan
}

###############################################################################
# PASO 4: LIMPIAR CARPETAS RESTANTES
###############################################################################

Write-Host "`nPASO 4: Eliminando carpetas residuales..." -ForegroundColor Yellow

$pathsToClean = @(
    "C:\Users\$env:USERNAME\anaconda3",
    "C:\Users\$env:USERNAME\.anaconda",
    "C:\Users\$env:USERNAME\.conda",
    "C:\ProgramData\anaconda3",
    "C:\ProgramData\.anaconda",
    "C:\ProgramData\.conda"
)

foreach ($path in $pathsToClean) {
    if (Test-Path $path) {
        Write-Host "  🗑️  Eliminando: $path" -ForegroundColor Gray
        Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "  ✅ Eliminado" -ForegroundColor Green
    }
}

###############################################################################
# PASO 5: LIMPIAR VARIABLES DE ENTORNO
###############################################################################

Write-Host "`nPASO 5: Limpiando variables de entorno..." -ForegroundColor Yellow

# Obtener PATH actual
$pathVar = [Environment]::GetEnvironmentVariable("Path", "Machine")
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")

# Eliminar referencias a Anaconda
$newPath = $pathVar -split ";" | Where-Object { $_ -notlike "*anaconda*" -and $_ -notlike "*conda*" } | Join-String -Separator ";"
$newUserPath = $userPath -split ";" | Where-Object { $_ -notlike "*anaconda*" -and $_ -notlike "*conda*" } | Join-String -Separator ";"

if ($newPath -ne $pathVar) {
    [Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
    Write-Host "  ✅ Variable PATH de sistema limpiada" -ForegroundColor Green
}

if ($newUserPath -ne $userPath) {
    [Environment]::SetEnvironmentVariable("Path", $newUserPath, "User")
    Write-Host "  ✅ Variable PATH de usuario limpiada" -ForegroundColor Green
}

# Eliminar otras variables Anaconda
$anacondaVars = Get-ChildItem Env: | Where-Object { $_.Name -like "*CONDA*" -or $_.Name -like "*ANACONDA*" }
foreach ($var in $anacondaVars) {
    [Environment]::SetEnvironmentVariable($var.Name, $null, "User")
    Write-Host "  ✅ Eliminada variable: $($var.Name)" -ForegroundColor Green
}

###############################################################################
# PASO 6: LIMPIAR INICIO RÁPIDO
###############################################################################

Write-Host "`nPASO 6: Limpiando accesos directos..." -ForegroundColor Yellow

$shortcutsPath = "C:\Users\$env:USERNAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"
$anacondaShortcuts = Get-ChildItem $shortcutsPath -Filter "*Anaconda*" -ErrorAction SilentlyContinue
$anacondaShortcuts += Get-ChildItem $shortcutsPath -Filter "*conda*" -ErrorAction SilentlyContinue
$anacondaShortcuts += Get-ChildItem $shortcutsPath -Filter "*Spyder*" -ErrorAction SilentlyContinue

foreach ($shortcut in $anacondaShortcuts) {
    Write-Host "  🗑️  Eliminando: $($shortcut.Name)" -ForegroundColor Gray
    Remove-Item -Path $shortcut.FullName -Force -ErrorAction SilentlyContinue
    Write-Host "  ✅ Eliminado" -ForegroundColor Green
}

###############################################################################
# PASO 7: LIMPIAR REGISTRO
###############################################################################

Write-Host "`nPASO 7: Limpiando registro..." -ForegroundColor Yellow

$regPaths = @(
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\Anaconda*",
    "HKCU:\Software\Continuum",
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\MountPoints2\*anaconda*"
)

foreach ($regPath in $regPaths) {
    try {
        $items = Get-Item $regPath -ErrorAction SilentlyContinue
        if ($items) {
            foreach ($item in $items) {
                Write-Host "  🗑️  Eliminando clave: $($item.Name)" -ForegroundColor Gray
                Remove-Item -Path $item.PSPath -Recurse -Force -ErrorAction SilentlyContinue
                Write-Host "  ✅ Eliminado" -ForegroundColor Green
            }
        }
    } catch {
        # Ignorar errores de registro
    }
}

###############################################################################
# PASO 8: VERIFICACIÓN
###############################################################################

Write-Host "`nPASO 8: Verificando..." -ForegroundColor Yellow

$anacondaStillExists = Test-Path "C:\Users\$env:USERNAME\anaconda3"
$condaCmd = Get-Command conda -ErrorAction SilentlyContinue

if ($anacondaStillExists -or $condaCmd) {
    Write-Host "  ⚠️  Anaconda aún está presente en el sistema" -ForegroundColor Yellow
    Write-Host "  💡 Necesitarás reiniciar Windows para aplicar los cambios" -ForegroundColor Cyan
} else {
    Write-Host "  ✅ Anaconda completamente eliminado" -ForegroundColor Green
}

###############################################################################
# FINALIZACIÓN
###############################################################################

Write-Host "`n" -ForegroundColor Cyan
Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║              DESINSTALACIÓN COMPLETADA                           ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Green

Write-Host "`n📋 PRÓXIMOS PASOS:" -ForegroundColor Yellow
Write-Host "   1. ⚡ REINICIA Windows completamente" -ForegroundColor Cyan
Write-Host "   2. ▶️  Ejecuta: 2_INSTALAR_PYTHON.ps1" -ForegroundColor Cyan
Write-Host "   3. ▶️  Ejecuta: 3_INSTALAR_SPYDER_STANDALONE.ps1" -ForegroundColor Cyan
Write-Host "   4. ▶️  Ejecuta: 4_INICIAR_BOT.ps1" -ForegroundColor Cyan

Write-Host "`n📂 BACKUP:" -ForegroundColor Yellow
if (Test-Path $backupPath) {
    Write-Host "   ✅ Guardado en: $backupPath" -ForegroundColor Green
} else {
    Write-Host "   (Sin ambientes conda personalizados que respaldar)" -ForegroundColor Gray
}

Write-Host "`n"
Read-Host "Presiona Enter para REINICIAR Windows"

# Reiniciar
shutdown /r /t 30 /c "Desinstalación de Anaconda completada. Reiniciando en 30 segundos..."
