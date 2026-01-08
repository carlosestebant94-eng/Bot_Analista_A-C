"""
main.py
Punto de entrada principal del Bot Analista A&C
"""
from keep_alive import keep_alive

import sys
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from config import Settings
from telegram_bot import TelegramAnalystBot


def main():
    """Función principal"""
    
    # Crear directorios
    Settings.crear_directorios()
    
    # Mostrar configuración
    Settings.mostrar_configuracion()
    
    # Validar configuración
    if not Settings.validar_configuracion():
        print("❌ Configuración incompleta. Revisa el archivo .env")
        return
    
    # Inicializar bot
    try:
        bot = TelegramAnalystBot()
        bot.iniciar()
    except KeyboardInterrupt:
        print("\n\n👋 Bot detenido por el usuario")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise


if __name__ == "__main__":
    keep_alive()
    print("Iniciando servidor web falso...")
    main()
