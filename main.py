"""
main.py
Punto de entrada principal del Bot Analista A&C
Con protección contra múltiples instancias ejecutándose simultáneamente
"""
from keep_alive import keep_alive

import sys
from pathlib import Path
import os
import time

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from config import Settings
from telegram_bot import TelegramAnalystBot
from logging_audit import setup_centralized_logging


def verificar_instancia_unica():
    """
    Verifica que solo haya una instancia del bot ejecutándose
    Previene el error: "Conflict: terminated by other getUpdates request"
    """
    lock_file = Path(__file__).parent / ".bot_lock"
    
    if lock_file.exists():
        try:
            # Leer el PID del archivo lock
            with open(lock_file, 'r') as f:
                old_pid = int(f.read().strip())
            
            # Verificar si el proceso antiguo aún está activo
            try:
                # Intentar acceder a /proc para verificar si el proceso existe
                if os.path.exists(f"/proc/{old_pid}"):
                    print(f"[ERROR] Ya hay una instancia del bot en ejecución (PID: {old_pid})")
                    print("[ERROR] Deteniendo instancia anterior...")
                    try:
                        os.kill(old_pid, 9)
                        time.sleep(2)
                    except:
                        pass
            except:
                # En Windows, esto no funcionará, así que solo lo intentamos
                pass
        except:
            pass
    
    # Crear nuevo lock file con el PID actual
    try:
        with open(lock_file, 'w') as f:
            f.write(str(os.getpid()))
    except:
        pass


def limpiar_lock_file():
    """Limpia el archivo lock al detener el bot"""
    lock_file = Path(__file__).parent / ".bot_lock"
    try:
        if lock_file.exists():
            lock_file.unlink()
    except:
        pass


def main():
    """Función principal"""
    
    # NUEVO: Verificar instancia única
    verificar_instancia_unica()
    
    # Inicializar logging centralizado (Phase 5A Integration)
    setup_centralized_logging("BotAnalystMain", "INFO")
    
    # Crear directorios
    Settings.crear_directorios()
    
    # Mostrar configuración
    Settings.mostrar_configuracion()
    
    # Validar configuración
    if not Settings.validar_configuracion():
        print("[ERROR] Configuracion incompleta. Revisa el archivo .env")
        limpiar_lock_file()
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
    finally:
        # NUEVO: Limpiar lock file
        limpiar_lock_file()


if __name__ == "__main__":
    keep_alive()
    print("Iniciando servidor web falso...")
    main()
