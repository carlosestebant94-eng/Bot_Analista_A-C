#!/usr/bin/env python3
"""
main_isolado.py
Versión de main que evita imports problemáticos de Anaconda
Carga modules under demanda para evitar conflictos
"""

import sys
import os

# Limpiar paths de Anaconda ANTES de hacer imports
original_path = sys.path.copy()
sys.path = [p for p in sys.path if 'anaconda' not in p.lower() and 'conda' not in p.lower()]

# Agregar solo el venv
venv_site_packages = os.path.join(
    os.path.dirname(__file__),
    'venv_bot', 'Lib', 'site-packages'
)
if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)

print("=" * 70)
print("🤖 BOT ANALISTA A&C - MODO AISLADO DE ANACONDA")
print("=" * 70)
print(f"✅ Python ejecutable: {sys.executable}")
print(f"✅ Paths limpios: Se removieron {len(original_path) - len(sys.path)} rutas de Anaconda")
print("")

try:
    # Import crítico: Cargamos lo mínimo necesario
    print("📦 Cargando módulos...")
    
    from pathlib import Path
    print("  ✓ pathlib")
    
    from dotenv import load_dotenv
    print("  ✓ dotenv")
    
    load_dotenv()
    
    import logging
    print("  ✓ logging")
    
    # Ahora cargamos el bot
    print("  ✓ Preparando bot...")
    from config import Settings
    print("  ✓ config")
    
    from telegram_bot import TelegramAnalystBot
    print("  ✓ telegram_bot")
    
    print("")
    print("=" * 70)
    
    # Configurar
    Settings.crear_directorios()
    
    # Crear y arrancar bot
    print("⚙️  Inicializando bot...")
    print("")
    
    bot = TelegramAnalystBot()
    print("✅ Bot inicializado correctamente")
    print("")
    print("=" * 70)
    print("🚀 Iniciando bot de Telegram...")
    print("=" * 70)
    print("")
    
    bot.iniciar()
    
except KeyboardInterrupt:
    print("\n\n👋 Bot detenido por el usuario")
    sys.exit(0)
    
except ImportError as e:
    print(f"\n❌ ERROR DE IMPORTACIÓN: {str(e)}")
    print("\nPosibles soluciones:")
    print("1. Desinstala Anaconda completamente")
    print("2. Usa Docker (recomendado)")
    print("3. Crea una máquina virtual limpia")
    sys.exit(1)
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
