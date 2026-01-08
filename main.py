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
from logging_audit import setup_centralized_logging


def main():
    """Función principal"""
    
    # Inicializar logging centralizado (Phase 5A Integration)
    setup_centralized_logging("BotAnalystMain", "INFO")
    
    # Crear directorios
    Settings.crear_directorios()
    
    # Mostrar configuración
    Settings.mostrar_configuracion()
    
    # Validar configuración
    if not Settings.validar_configuracion():
        print("[ERROR] Configuracion incompleta. Revisa el archivo .env")
        return
    
    # Inicializar bot
    try:
        bot = TelegramAnalystBot()
        bot.iniciar()
    except KeyboardInterrupt:
        print("\n\n[INFO] Bot detenido por el usuario")
    except Exception as e:
        print(f"[ERROR] Error: {str(e)}")
        raise


if __name__ == "__main__":
    keep_alive()
    print("Iniciando servidor web falso...")
    main()
