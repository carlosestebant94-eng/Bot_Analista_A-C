# Script PowerShell para ejecutar bot con venv limpio
# Desactiva Anaconda y ejecuta con venv puro

$env:PYTHONPATH = ""
$env:CONDA_DEFAULT_ENV = ""
$env:CONDA_PREFIX = ""

# Activar venv
& .\venv_bot\Scripts\Activate.ps1

# Ejecutar bot
python main.py
