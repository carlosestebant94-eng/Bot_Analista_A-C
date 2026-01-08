"""
iniciar_bot_debug.py
Script para iniciar el bot con debugging mejorado
"""

import sys
import os
from pathlib import Path

# Configurar encoding
os.environ["PYTHONIOENCODING"] = "utf-8"

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("INICIANDO BOT ANALISTA A&C CON DEBUG")
print("=" * 80)

try:
    print("\n✅ Paso 1: Importar configuración...")
    from config import Settings
    print("   ✓ Settings importado")
    
    print("\n✅ Paso 2: Crear directorios...")
    Settings.crear_directorios()
    print("   ✓ Directorios creados")
    
    print("\n✅ Paso 3: Mostrar configuración...")
    Settings.mostrar_configuracion()
    
    print("\n✅ Paso 4: Validar configuración...")
    if not Settings.validar_configuracion():
        print("❌ Configuración incompleta. Revisa el archivo .env")
        print("\nVariables requeridas:")
        print("  - TELEGRAM_TOKEN")
        print("  - GOOGLE_API_KEY")
        sys.exit(1)
    print("   ✓ Configuración válida")
    
    print("\n✅ Paso 5: Importar bot...")
    from telegram_bot import TelegramAnalystBot
    print("   ✓ Bot importado")
    
    print("\n✅ Paso 6: Inicializar bot...")
    bot = TelegramAnalystBot()
    print("   ✓ Bot inicializado")
    
    print("\n" + "=" * 80)
    print("🚀 BOT INICIANDO...")
    print("=" * 80)
    print("\n✅ Bot en funcionamiento")
    print("   Escuchando mensajes en Telegram...")
    print("   Presiona Ctrl+C para detener\n")
    
    # Iniciar bot
    bot.iniciar()
    
except KeyboardInterrupt:
    print("\n\n👋 Bot detenido por el usuario")
    sys.exit(0)
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}")
    print(f"   Mensaje: {str(e)}")
    print(f"\n📋 Traceback completo:")
    import traceback
    traceback.print_exc()
    sys.exit(1)
