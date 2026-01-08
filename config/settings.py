"""
config/settings.py
Configuración centralizada del proyecto
"""

import os
from dotenv import load_dotenv
from pathlib import Path


# Cargar variables de entorno
load_dotenv()


class Settings:
    """Clase para centralizar toda la configuración"""
    
    # Directorios
    BASE_DIR = Path(__file__).resolve().parent.parent
    PDFS_DIR = BASE_DIR / "pdfs"
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Telegram
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
    
    # Base de datos
    DATABASE_PATH = DATA_DIR / "memory.db"
    
    # APIs externas - Google AI Studio (Gemini)
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")
    
    # Configuración del procesamiento
    MAX_FILE_SIZE_PDF = 100 * 1024 * 1024  # 100 MB
    MAX_FILE_SIZE_IMAGE = 50 * 1024 * 1024  # 50 MB
    SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    
    # Configuración del análisis
    MIN_CONFIDENCE = 0.5
    MAX_RESULTS_SEARCH = 10
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = LOGS_DIR / "bot_analista.log"
    
    # Reconocimiento OCR
    OCR_LANGUAGE = "spa+eng"
    
    # Análisis de imágenes
    CANNY_THRESHOLD1 = 50
    CANNY_THRESHOLD2 = 150
    MIN_CONTOUR_AREA = 100
    
    @classmethod
    def crear_directorios(cls):
        """Crea los directorios necesarios si no existen"""
        for directorio in [cls.PDFS_DIR, cls.DATA_DIR, cls.LOGS_DIR]:
            directorio.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def validar_configuracion(cls) -> bool:
        """
        Valida que la configuración necesaria esté en orden
        
        Returns:
            True si la configuración es válida
        """
        errores = []
        
        if not cls.TELEGRAM_TOKEN:
            errores.append("⚠️ TELEGRAM_TOKEN no está configurado en .env")
        
        if not all([cls.PDFS_DIR.exists(), cls.DATA_DIR.exists(), cls.LOGS_DIR.exists()]):
            print("📁 Creando directorios necesarios...")
            cls.crear_directorios()
        
        if errores:
            for error in errores:
                print(error)
            return False
        
        return True
    
    @classmethod
    def mostrar_configuracion(cls):
        """Muestra la configuración actual (sin datos sensibles)"""
        print("=" * 50)
        print("[*] CONFIGURACION DEL BOT")
        print("=" * 50)
        print(f"Base Directory: {cls.BASE_DIR}")
        print(f"PDFs Directory: {cls.PDFS_DIR}")
        print(f"Data Directory: {cls.DATA_DIR}")
        print(f"Logs Directory: {cls.LOGS_DIR}")
        print(f"Database: {cls.DATABASE_PATH}")
        print(f"Log Level: {cls.LOG_LEVEL}")
        print(f"Telegram Token: {'OK - Configurado' if cls.TELEGRAM_TOKEN else 'ERROR - No configurado'}")
        print(f"Google AI (Gemini): {'OK - Configurado' if cls.GOOGLE_API_KEY else 'ERROR - No configurado'}")
        print("=" * 50)
