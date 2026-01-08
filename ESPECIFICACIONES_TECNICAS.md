# 🔧 ESPECIFICACIONES TÉCNICAS DETALLADAS

## Guía Completa para Replicación de Arquitectura

---

## PARTE 1: ESTRUCTURA DE DIRECTORIOS RECOMENDADA

```
proyecto_nuevo/
│
├── config/
│   ├── __init__.py
│   ├── settings.py              # ✅ Clase Settings centralizada
│   └── constants.py             # Constantes globales
│
├── utils/
│   ├── __init__.py
│   ├── logger.py                # ✅ Logger global
│   ├── validators.py            # ✅ Validadores
│   ├── exceptions.py            # Excepciones personalizadas
│   └── decorators.py            # Decoradores reutilizables
│
├── cerebro/
│   ├── __init__.py
│   ├── knowledge_manager.py     # ✅ Gestión de BD + búsqueda
│   └── pdf_processor.py         # ✅ Extracción de PDFs
│
├── analisis/
│   ├── __init__.py
│   ├── analyzer.py              # ✅ Motor central de análisis
│   ├── technical_analyzer.py    # Indicadores técnicos
│   ├── fundamental_analyzer.py  # Análisis fundamental
│   ├── risk_calculator.py       # Cálculos de R/R
│   └── data_manager.py          # Obtención de datos (yfinance)
│
├── telegram_bot/
│   ├── __init__.py
│   └── bot.py                   # ✅ Handlers + orquestación
│
├── ia/
│   ├── __init__.py
│   └── ai_engine.py             # Integración con Gemini/OpenAI
│
├── data/                        # Directorio de datos
│   ├── bot_database.db          # SQLite
│   ├── cache/                   # Caché temporal
│   └── reportes/                # PDFs generados
│
├── pdfs/                        # Documentos de entrada
│
├── logs/                        # Archivos de log
│
├── .env.example                 # Variables de entorno (template)
├── .env                         # Variables de entorno (actual)
├── .gitignore                   # Exclusiones de git
├── requirements.txt             # Dependencias de Python
├── setup.py                     # Instalación del paquete
│
├── main.py                      # 🚀 Punto de entrada
├── README.md                    # Documentación principal
├── ARQUITECTURA.md              # Diseño del sistema
└── CAMBIOS.md                   # Log de cambios
```

---

## PARTE 2: ARCHIVO ESENCIAL #1 - config/settings.py

```python
# config/settings.py
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Settings:
    """Configuración centralizada del proyecto"""
    
    # Rutas
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    PDFS_DIR = BASE_DIR / "pdfs"
    REPORTES_DIR = DATA_DIR / "reportes"
    DB_PATH = DATA_DIR / "bot_database.db"
    
    # Telegram
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    # APIs
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Configuración
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    @staticmethod
    def crear_directorios():
        """Crear directorios necesarios si no existen"""
        for dir_path in [
            Settings.DATA_DIR,
            Settings.LOGS_DIR,
            Settings.PDFS_DIR,
            Settings.REPORTES_DIR
        ]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def validar_configuracion():
        """Validar que todos los parámetros necesarios estén configurados"""
        errores = []
        
        if not Settings.TELEGRAM_TOKEN:
            errores.append("❌ TELEGRAM_TOKEN no configurado")
        if not Settings.GEMINI_API_KEY:
            errores.append("⚠️ GEMINI_API_KEY no configurado")
        
        if errores:
            for error in errores:
                print(error)
            if any("❌" in e for e in errores):
                sys.exit(1)
        
        print("✅ Configuración validada")
    
    @staticmethod
    def mostrar_configuracion():
        """Mostrar configuración actual (ocultar datos sensibles)"""
        print("\n" + "="*50)
        print("⚙️ CONFIGURACIÓN DEL SISTEMA")
        print("="*50)
        print(f"Base dir: {Settings.BASE_DIR}")
        print(f"Debug: {Settings.DEBUG}")
        print(f"Log level: {Settings.LOG_LEVEL}")
        print(f"Token Telegram: {Settings.TELEGRAM_TOKEN[:10]}...")
        print(f"API Gemini: {Settings.GEMINI_API_KEY[:10]}...")
        print("="*50 + "\n")

# Instancia global
settings = Settings()
```

---

## PARTE 3: ARCHIVO ESENCIAL #2 - utils/logger.py

```python
# utils/logger.py
import logging
import sys
from pathlib import Path
from config.settings import settings

class Logger:
    """Logger centralizado para todo el proyecto"""
    
    _logger = None
    
    @classmethod
    def get_logger(cls, name: str = "bot_analista"):
        """Obtener logger configurado"""
        if cls._logger:
            return cls._logger
        
        cls._logger = logging.getLogger(name)
        cls._logger.setLevel(settings.LOG_LEVEL)
        
        # Formato
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Handler de archivo
        log_path = settings.LOGS_DIR / "bot_analista.log"
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(settings.LOG_LEVEL)
        file_handler.setFormatter(formatter)
        cls._logger.addHandler(file_handler)
        
        # Handler de consola
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(settings.LOG_LEVEL)
        console_handler.setFormatter(formatter)
        cls._logger.addHandler(console_handler)
        
        return cls._logger

# Uso global
logger = Logger.get_logger()
```

---

## PARTE 4: ARCHIVO ESENCIAL #3 - cerebro/knowledge_manager.py

```python
# cerebro/knowledge_manager.py
import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional
from utils.logger import logger
from config.settings import settings

class KnowledgeManager:
    """Gestión de base de datos de conocimiento"""
    
    def __init__(self):
        self.db_path = settings.DB_PATH
        self.inicializar_bd()
    
    def inicializar_bd(self):
        """Crear tablas si no existen"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tabla: documentos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documentos (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT UNIQUE,
                    ruta TEXT,
                    fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    contenido TEXT,
                    metadatos JSON
                )
            """)
            
            # Tabla: conocimiento
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conocimiento (
                    id INTEGER PRIMARY KEY,
                    tema TEXT,
                    contenido TEXT,
                    relevancia REAL,
                    documento_id INTEGER,
                    FOREIGN KEY(documento_id) REFERENCES documentos(id)
                )
            """)
            
            # Tabla: análisis_realizados
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analisis_realizados (
                    id INTEGER PRIMARY KEY,
                    tipo TEXT,
                    datos JSON,
                    resultado JSON,
                    confianza REAL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabla: aprendizajes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS aprendizajes (
                    id INTEGER PRIMARY KEY,
                    patron TEXT,
                    frecuencia INTEGER,
                    validez REAL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("✅ Base de datos inicializada")
        except Exception as e:
            logger.error(f"❌ Error al inicializar BD: {e}")
    
    def cargar_documento(self, nombre: str, contenido: str, metadatos: dict = None):
        """Cargar documento a la BD"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO documentos (nombre, ruta, contenido, metadatos)
                VALUES (?, ?, ?, ?)
            """, (nombre, str(settings.PDFS_DIR / nombre), contenido, 
                  json.dumps(metadatos or {})))
            
            conn.commit()
            conn.close()
            logger.info(f"✅ Documento '{nombre}' cargado")
        except Exception as e:
            logger.error(f"❌ Error al cargar documento: {e}")
    
    def buscar_conocimiento(self, query: str, limite: int = 5) -> List[Dict]:
        """Buscar conocimiento relevante"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT tema, contenido, relevancia FROM conocimiento
                WHERE tema LIKE ? OR contenido LIKE ?
                ORDER BY relevancia DESC
                LIMIT ?
            """, (f"%{query}%", f"%{query}%", limite))
            
            resultados = [
                {
                    "tema": row[0],
                    "contenido": row[1],
                    "relevancia": row[2]
                }
                for row in cursor.fetchall()
            ]
            
            conn.close()
            return resultados
        except Exception as e:
            logger.error(f"❌ Error en búsqueda: {e}")
            return []
    
    def registrar_analisis(self, tipo: str, datos: dict, 
                          resultado: dict, confianza: float):
        """Registrar análisis realizado"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO analisis_realizados 
                (tipo, datos, resultado, confianza)
                VALUES (?, ?, ?, ?)
            """, (tipo, json.dumps(datos), json.dumps(resultado), confianza))
            
            conn.commit()
            conn.close()
            logger.info(f"✅ Análisis {tipo} registrado")
        except Exception as e:
            logger.error(f"❌ Error al registrar análisis: {e}")

# Instancia global
knowledge_manager = KnowledgeManager()
```

---

## PARTE 5: ARCHIVO ESENCIAL #4 - cerebro/pdf_processor.py

```python
# cerebro/pdf_processor.py
import pdfplumber
from pathlib import Path
from utils.logger import logger
from config.settings import settings

class PDFProcessor:
    """Procesamiento de archivos PDF"""
    
    def __init__(self):
        self.pdfs_dir = settings.PDFS_DIR
    
    def procesar_pdf(self, ruta_pdf: str) -> Dict[str, any]:
        """Procesar un PDF individual"""
        try:
            with pdfplumber.open(ruta_pdf) as pdf:
                info = {
                    "nombre": Path(ruta_pdf).name,
                    "num_paginas": len(pdf.pages),
                    "texto": "",
                    "tablas": [],
                    "metadatos": pdf.metadata or {}
                }
                
                # Extraer texto
                for page in pdf.pages:
                    info["texto"] += page.extract_text() + "\n"
                
                # Extraer tablas
                for page in pdf.pages:
                    if page.extract_tables():
                        info["tablas"].extend(page.extract_tables())
                
                logger.info(f"✅ PDF procesado: {info['nombre']}")
                return info
        except Exception as e:
            logger.error(f"❌ Error procesando PDF: {e}")
            return {}
    
    def procesar_todos_pdfs(self) -> List[Dict]:
        """Procesar todos los PDFs del directorio"""
        resultados = []
        for pdf_file in self.pdfs_dir.glob("*.pdf"):
            resultado = self.procesar_pdf(str(pdf_file))
            if resultado:
                resultados.append(resultado)
        
        logger.info(f"✅ {len(resultados)} PDFs procesados")
        return resultados

# Instancia global
pdf_processor = PDFProcessor()
```

---

## PARTE 6: ARCHIVO ESENCIAL #5 - main.py

```python
# main.py
import sys
from pathlib import Path

# Agregar el directorio al path de Python
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import settings
from utils.logger import logger
from telegram_bot.bot import TelegramAnalystBot

def main():
    """Función principal de inicio"""
    
    print("\n" + "="*60)
    print("🤖 BOT ANALISTA A&C - INICIANDO")
    print("="*60 + "\n")
    
    # 1. Crear directorios
    logger.info("Creando directorios...")
    settings.crear_directorios()
    
    # 2. Validar configuración
    logger.info("Validando configuración...")
    settings.validar_configuracion()
    settings.mostrar_configuracion()
    
    # 3. Inicializar bot
    logger.info("Inicializando bot...")
    bot = TelegramAnalystBot()
    
    # 4. Iniciar bot
    logger.info("Iniciando bot...")
    try:
        bot.iniciar()
    except KeyboardInterrupt:
        logger.warning("Bot detenido por el usuario")
        print("\n✋ Bot detenido")

if __name__ == "__main__":
    main()
```

---

## PARTE 7: STACK MÍNIMO - requirements.txt

```
# Core
python-telegram-bot==22.5
asyncio-contextmanager==1.0.0

# Procesamiento de datos
pandas==2.3.3
numpy==1.26.4

# Análisis de datos
yfinance==0.2.66
ta==0.11.0
scikit-learn==1.7.2

# PDFs
pdfplumber==0.11.8
reportlab==4.0.4

# Visión computacional
opencv-python==4.8.1.78
pytesseract==0.3.13
pillow==10.4.0

# IA
google-generativeai==0.8.5

# Utilidades
python-dotenv==1.0.1
requests==2.31.0
cryptography==43.0.3
httpx==0.27.0
```

---

## PARTE 8: ARCHIVO DE CONFIGURACIÓN - .env.example

```bash
# .env.example
# Copiar a .env y rellenar con valores reales

# Telegram Bot
TELEGRAM_TOKEN=your_telegram_token_here

# APIs de IA
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Configuración del Sistema
LOG_LEVEL=INFO
DEBUG=False
```

---

## PARTE 9: INTERFAZ TELEGRA - telegram_bot/bot.py (Básico)

```python
# telegram_bot/bot.py
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    filters, ContextTypes
)
from utils.logger import logger
from config.settings import settings

class TelegramAnalystBot:
    """Bot principal de Telegram"""
    
    def __init__(self):
        self.app = Application.builder().token(
            settings.TELEGRAM_TOKEN
        ).build()
        self.registrar_handlers()
    
    def registrar_handlers(self):
        """Registrar manejadores de comandos"""
        self.app.add_handler(
            CommandHandler("start", self.comando_start)
        )
        self.app.add_handler(
            CommandHandler("ayuda", self.comando_ayuda)
        )
        self.app.add_handler(
            CommandHandler("status", self.comando_status)
        )
    
    async def comando_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejador del comando /start"""
        await update.message.reply_text(
            "🤖 ¡Bienvenido a Bot Analista A&C!\n\n"
            "Usa /ayuda para ver los comandos disponibles."
        )
        logger.info(f"Usuario {update.effective_user.id} inició")
    
    async def comando_ayuda(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejador del comando /ayuda"""
        ayuda_texto = """
        📖 COMANDOS DISPONIBLES:
        
        /start - Inicia el bot
        /ayuda - Muestra esta ayuda
        /status - Estado del sistema
        """
        await update.message.reply_text(ayuda_texto)
    
    async def comando_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejador del comando /status"""
        await update.message.reply_text("✅ Bot operacional")
        logger.info("Status consultado")
    
    def iniciar(self):
        """Iniciar el bot"""
        logger.info("Bot iniciando polling...")
        self.app.run_polling()
        logger.info("Bot detenido")
```

---

## PARTE 10: TABLA DE COMPONENTES MÍNIMOS REQUERIDOS

| Componente | Archivo | Líneas | Dependencia | Prioridad |
|-----------|---------|--------|------------|-----------|
| Settings | config/settings.py | 60 | Ninguna | 🔴 Alta |
| Logger | utils/logger.py | 40 | settings | 🔴 Alta |
| KnowledgeManager | cerebro/knowledge_manager.py | 150 | logger, settings | 🟡 Media |
| PDFProcessor | cerebro/pdf_processor.py | 50 | logger | 🟡 Media |
| Bot Principal | telegram_bot/bot.py | 80 | settings, logger | 🔴 Alta |
| Main | main.py | 30 | todos | 🔴 Alta |

---

## PARTE 11: FLUJO DE INSTALACIÓN INICIAL

```bash
# 1. Crear proyecto
mkdir proyecto_nuevo
cd proyecto_nuevo

# 2. Crear venv
python -m venv venv
./venv/Scripts/activate

# 3. Clonar estructura
# [Copiar carpetas y archivos básicos]

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar .env
cp .env.example .env
# [Editar .env con valores reales]

# 6. Ejecutar
python main.py
```

---

## PARTE 12: CHECKLIST DE VALIDACIÓN INICIAL

- [ ] Directorios creados
- [ ] config/settings.py funcionando
- [ ] utils/logger.py registrando logs
- [ ] cerebro/knowledge_manager.py con BD
- [ ] cerebro/pdf_processor.py extrayendo PDFs
- [ ] telegram_bot/bot.py conectando a Telegram
- [ ] main.py ejecutándose sin errores
- [ ] .env configurado correctamente
- [ ] logs/ conteniendo registros
- [ ] data/bot_database.db creada

---

## RESUMEN

Este documento proporciona la **base mínima viable** para replicar la arquitectura. Cada sección puede expandirse con:

- ✅ Validadores más complejos
- ✅ Más indicadores técnicos
- ✅ Integración con APIs externas
- ✅ Interfaz web
- ✅ Sistema de alertas
- ✅ Machine learning

**Tiempo estimado de implementación:** 2-3 horas para un MVP funcional.

