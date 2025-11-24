"""
utils/logger.py
Sistema centralizado de logging
"""

import logging
import os
from datetime import datetime


def setup_logger(nombre: str = "BotAnalista", 
                 nivel: int = logging.INFO,
                 archivo: str = "logs/bot_analista.log") -> logging.Logger:
    """
    Configura un logger centralizado
    
    Args:
        nombre: Nombre del logger
        nivel: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        archivo: Ruta del archivo de log
        
    Returns:
        Logger configurado
    """
    
    # Crear directorio de logs si no existe
    os.makedirs(os.path.dirname(archivo), exist_ok=True)
    
    # Crear logger
    logger = logging.getLogger(nombre)
    logger.setLevel(nivel)
    
    # Formato de logs
    formato = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para archivo
    archivo_handler = logging.FileHandler(archivo, encoding='utf-8')
    archivo_handler.setLevel(nivel)
    archivo_handler.setFormatter(formato)
    logger.addHandler(archivo_handler)
    
    # Handler para consola
    consola_handler = logging.StreamHandler()
    consola_handler.setLevel(nivel)
    consola_handler.setFormatter(formato)
    logger.addHandler(consola_handler)
    
    return logger


class LoggerContexto:
    """Context manager para logging con contexto"""
    
    def __init__(self, logger: logging.Logger, mensaje: str):
        self.logger = logger
        self.mensaje = mensaje
    
    def __enter__(self):
        self.logger.info(f"[INICIO] {self.mensaje}")
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.logger.info(f"[FIN] {self.mensaje} - Completado exitosamente")
        else:
            self.logger.error(f"[ERROR] {self.mensaje} - {exc_val}")
        return False
