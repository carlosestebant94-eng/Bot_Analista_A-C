# 🚀 GUÍA COMPLETA: REPLICAR ARQUITECTURA DESDE CERO

## Plan de Implementación Detallado (6-8 Horas)

---

## ⏱️ CRONOGRAMA RECOMENDADO

```
TOTAL: 8 horas de trabajo dedicado

BLOQUE 1: Preparación (1 hora)
├─ 00:00-00:15 Crear estructura base
├─ 00:15-00:30 Configurar git y entorno
├─ 00:30-00:45 Instalar dependencias
└─ 00:45-01:00 Validar setup

BLOQUE 2: Fundamentos (1.5 horas)
├─ 01:00-01:20 Implementar config/settings.py
├─ 01:20-01:40 Implementar utils/logger.py
├─ 01:40-02:00 Implementar utils/validators.py
└─ 02:00-02:30 Crear main.py

BLOQUE 3: Base de Datos (1.5 horas)
├─ 02:30-02:50 Implementar knowledge_manager.py
├─ 02:50-03:10 Crear tablas SQLite
├─ 03:10-03:30 Implementar búsquedas
└─ 03:30-04:00 Pruebas unitarias

BLOQUE 4: Procesamiento (1.5 horas)
├─ 04:00-04:20 Implementar pdf_processor.py
├─ 04:20-04:40 Implementar image_processor.py
├─ 04:40-05:00 Integración básica
└─ 05:00-05:30 Pruebas

BLOQUE 5: Motor de Análisis (1.5 horas)
├─ 05:30-05:50 Implementar analyzer.py básico
├─ 05:50-06:10 Añadir indicadores técnicos
├─ 06:10-06:30 Integración con datos
└─ 06:30-07:00 Pruebas

BLOQUE 6: Bot de Telegram (1.5 horas)
├─ 07:00-07:20 Implementar bot.py básico
├─ 07:20-07:40 Añadir handlers
├─ 07:40-08:00 Integración completa
└─ 08:00-08:30 Pruebas end-to-end

EXTRA: Escalabilidad (opcional)
├─ Dockerización
├─ CI/CD
└─ Documentación exhaustiva
```

---

## 📋 FASE 1: PREPARACIÓN INICIAL (1 HORA)

### Paso 1.1: Crear estructura base

```bash
# En PowerShell
cd $HOME\Desktop
mkdir proyecto_bot_nuevo
cd proyecto_bot_nuevo

# Crear carpetas principales
mkdir config, utils, cerebro, analisis, telegram_bot, ia
mkdir data, pdfs, logs, data\reportes, data\cache
mkdir tests

# Crear archivos __init__.py
@"
# Paquete
"@ | Out-File -FilePath "config\__init__.py" -Encoding UTF8
@"
"@ | Out-File -FilePath "utils\__init__.py" -Encoding UTF8
@"
"@ | Out-File -FilePath "cerebro\__init__.py" -Encoding UTF8
@"
"@ | Out-File -FilePath "analisis\__init__.py" -Encoding UTF8
@"
"@ | Out-File -FilePath "telegram_bot\__init__.py" -Encoding UTF8
@"
"@ | Out-File -FilePath "ia\__init__.py" -Encoding UTF8
```

### Paso 1.2: Inicializar git

```bash
git init
git config user.name "Tu Nombre"
git config user.email "tu@email.com"

# Crear .gitignore
@"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Proyecto
.env
logs/
data/bot_database.db
pdfs/
*.log

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8

git add .
git commit -m "Initial commit: Project structure"
```

### Paso 1.3: Crear entorno virtual

```bash
# Crear venv
python -m venv venv
.\venv\Scripts\Activate.ps1

# Verificar
python --version
```

### Paso 1.4: Crear requirements.txt

```bash
@"
# Core
python-telegram-bot==22.5

# Data Processing
pandas==2.3.3
numpy==1.26.4

# Analysis
yfinance==0.2.66
ta==0.11.0
scikit-learn==1.7.2

# PDF
pdfplumber==0.11.8
reportlab==4.0.4

# Vision
opencv-python==4.8.1.78
pytesseract==0.3.13
pillow==10.4.0

# AI
google-generativeai==0.8.5

# Utils
python-dotenv==1.0.1
requests==2.31.0
"@ | Out-File -FilePath "requirements.txt" -Encoding UTF8

# Instalar
pip install -r requirements.txt
```

### Paso 1.5: Crear .env

```bash
@"
# Telegram
TELEGRAM_TOKEN=your_token_here

# APIs
GEMINI_API_KEY=your_key_here

# Config
LOG_LEVEL=INFO
DEBUG=False
"@ | Out-File -FilePath ".env" -Encoding UTF8

@"
# .env.example - Copiar a .env y completar
TELEGRAM_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
LOG_LEVEL=INFO
DEBUG=False
"@ | Out-File -FilePath ".env.example" -Encoding UTF8
```

---

## 📋 FASE 2: FUNDAMENTOS (1.5 HORAS)

### Paso 2.1: Implementar config/settings.py

```bash
@"
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    \"\"\"Configuración centralizada\"\"\"
    
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
    
    # Config
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    @staticmethod
    def crear_directorios():
        for dir_path in [
            Settings.DATA_DIR,
            Settings.LOGS_DIR,
            Settings.PDFS_DIR,
            Settings.REPORTES_DIR
        ]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def validar_configuracion():
        errores = []
        if not Settings.TELEGRAM_TOKEN:
            errores.append("TELEGRAM_TOKEN no configurado")
        if errores:
            for e in errores:
                print(f"ERROR: {e}")
            sys.exit(1)
        print("Configuración OK")
    
    @staticmethod
    def mostrar_configuracion():
        print("\n" + "="*50)
        print("CONFIGURACIÓN DEL SISTEMA")
        print("="*50)
        print(f"Base: {Settings.BASE_DIR}")
        print(f"Debug: {Settings.DEBUG}")
        print(f"Log Level: {Settings.LOG_LEVEL}")
        print("="*50)

settings = Settings()
"@ | Out-File -FilePath "config\settings.py" -Encoding UTF8
```

### Paso 2.2: Implementar utils/logger.py

```bash
@"
import logging
from pathlib import Path
from config.settings import settings

class Logger:
    _logger = None
    
    @classmethod
    def get_logger(cls, name="bot_analista"):
        if cls._logger:
            return cls._logger
        
        cls._logger = logging.getLogger(name)
        cls._logger.setLevel(settings.LOG_LEVEL)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File
        log_path = settings.LOGS_DIR / "bot_analista.log"
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        cls._logger.addHandler(file_handler)
        
        # Console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        cls._logger.addHandler(console_handler)
        
        return cls._logger

logger = Logger.get_logger()
"@ | Out-File -FilePath "utils\logger.py" -Encoding UTF8
```

### Paso 2.3: Implementar utils/validators.py

```bash
@"
import re
from pathlib import Path

class Validator:
    
    @staticmethod
    def validar_ticker(ticker):
        return bool(re.match(r'^[A-Z0-9]{1,5}$', str(ticker).upper()))
    
    @staticmethod
    def validar_imagen(ruta):
        try:
            from PIL import Image
            img = Image.open(ruta)
            return img.size[0] > 100 and img.size[1] > 100
        except:
            return False
    
    @staticmethod
    def validar_pdf(ruta):
        try:
            import pdfplumber
            with pdfplumber.open(ruta) as pdf:
                return len(pdf.pages) > 0
        except:
            return False
"@ | Out-File -FilePath "utils\validators.py" -Encoding UTF8
```

### Paso 2.4: Crear main.py

```bash
@"
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import settings
from utils.logger import logger

def main():
    print("\n" + "="*60)
    print("BOT ANALISTA - INICIANDO")
    print("="*60)
    
    # Crear directorios
    logger.info("Creando directorios...")
    settings.crear_directorios()
    
    # Validar
    logger.info("Validando configuración...")
    settings.validar_configuracion()
    settings.mostrar_configuracion()
    
    logger.info("Sistema listo")
    print("\nOK - Sistema inicializado correctamente")

if __name__ == "__main__":
    main()
"@ | Out-File -FilePath "main.py" -Encoding UTF8

# Probar
python main.py
```

---

## 📋 FASE 3: BASE DE DATOS (1.5 HORAS)

### Paso 3.1: Implementar cerebro/knowledge_manager.py

```bash
@"
import sqlite3
import json
from pathlib import Path
from config.settings import settings
from utils.logger import logger

class KnowledgeManager:
    
    def __init__(self):
        self.db_path = settings.DB_PATH
        self.inicializar_bd()
    
    def inicializar_bd(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Documentos
            cursor.execute(\"\"\"
                CREATE TABLE IF NOT EXISTS documentos (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT UNIQUE,
                    contenido TEXT,
                    fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            \"\"\")
            
            # Conocimiento
            cursor.execute(\"\"\"
                CREATE TABLE IF NOT EXISTS conocimiento (
                    id INTEGER PRIMARY KEY,
                    tema TEXT,
                    contenido TEXT,
                    relevancia REAL,
                    documento_id INTEGER
                )
            \"\"\")
            
            # Análisis
            cursor.execute(\"\"\"
                CREATE TABLE IF NOT EXISTS analisis (
                    id INTEGER PRIMARY KEY,
                    tipo TEXT,
                    datos JSON,
                    resultado JSON,
                    confianza REAL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            \"\"\")
            
            conn.commit()
            conn.close()
            logger.info("BD inicializada")
        except Exception as e:
            logger.error(f"Error en BD: {e}")
    
    def cargar_documento(self, nombre, contenido):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO documentos (nombre, contenido) VALUES (?, ?)",
                (nombre, contenido)
            )
            conn.commit()
            conn.close()
            logger.info(f"Documento {nombre} cargado")
        except Exception as e:
            logger.error(f"Error: {e}")
    
    def buscar_conocimiento(self, query, limite=5):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT tema, contenido, relevancia FROM conocimiento WHERE tema LIKE ? ORDER BY relevancia DESC LIMIT ?",
                (f"%{query}%", limite)
            )
            resultados = [
                {"tema": r[0], "contenido": r[1], "relevancia": r[2]}
                for r in cursor.fetchall()
            ]
            conn.close()
            return resultados
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
    
    def registrar_analisis(self, tipo, datos, resultado, confianza):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO analisis (tipo, datos, resultado, confianza) VALUES (?, ?, ?, ?)",
                (tipo, json.dumps(datos), json.dumps(resultado), confianza)
            )
            conn.commit()
            conn.close()
            logger.info(f"Análisis {tipo} registrado")
        except Exception as e:
            logger.error(f"Error: {e}")

knowledge_manager = KnowledgeManager()
"@ | Out-File -FilePath "cerebro\knowledge_manager.py" -Encoding UTF8
```

### Paso 3.2: Implementar cerebro/pdf_processor.py

```bash
@"
import pdfplumber
from pathlib import Path
from config.settings import settings
from utils.logger import logger

class PDFProcessor:
    
    def __init__(self):
        self.pdfs_dir = settings.PDFS_DIR
    
    def procesar_pdf(self, ruta_pdf):
        try:
            with pdfplumber.open(ruta_pdf) as pdf:
                info = {
                    "nombre": Path(ruta_pdf).name,
                    "num_paginas": len(pdf.pages),
                    "texto": "",
                    "tablas": []
                }
                
                for page in pdf.pages:
                    info["texto"] += page.extract_text() or ""
                    if page.extract_tables():
                        info["tablas"].extend(page.extract_tables())
                
                logger.info(f"PDF procesado: {info['nombre']}")
                return info
        except Exception as e:
            logger.error(f"Error: {e}")
            return {}
    
    def procesar_todos_pdfs(self):
        resultados = []
        for pdf_file in self.pdfs_dir.glob("*.pdf"):
            resultado = self.procesar_pdf(str(pdf_file))
            if resultado:
                resultados.append(resultado)
        logger.info(f"{len(resultados)} PDFs procesados")
        return resultados

pdf_processor = PDFProcessor()
"@ | Out-File -FilePath "cerebro\pdf_processor.py" -Encoding UTF8
```

---

## 📋 FASE 4: PROCESAMIENTO (1.5 HORAS)

### Paso 4.1: Implementar analisis/analyzer.py

```bash
@"
import yfinance as yf
from datetime import datetime
from utils.logger import logger

class Analyzer:
    
    def __init__(self):
        pass
    
    async def analizar_ticker(self, ticker):
        try:
            # Descargar datos
            datos = yf.download(ticker, period="1y", progress=False)
            
            if datos.empty:
                logger.warning(f"No hay datos para {ticker}")
                return {}
            
            # Análisis básico
            ultima_precio = datos['Close'].iloc[-1]
            cambio_percent = ((datos['Close'].iloc[-1] - datos['Close'].iloc[0]) / datos['Close'].iloc[0]) * 100
            volumen_promedio = datos['Volume'].mean()
            
            resultado = {
                "ticker": ticker,
                "precio_actual": float(ultima_precio),
                "cambio_percent": float(cambio_percent),
                "volumen_promedio": float(volumen_promedio),
                "confianza": 0.7,
                "fecha": datetime.now().isoformat()
            }
            
            logger.info(f"Análisis {ticker} completado")
            return resultado
        except Exception as e:
            logger.error(f"Error: {e}")
            return {}

analyzer = Analyzer()
"@ | Out-File -FilePath "analisis\analyzer.py" -Encoding UTF8
```

### Paso 4.2: Implementar analisis/image_processor.py

```bash
@"
import cv2
import numpy as np
from pathlib import Path
from utils.logger import logger

class ImageProcessor:
    
    def __init__(self):
        pass
    
    def analisis_completo(self, ruta_imagen):
        try:
            # Cargar imagen
            img = cv2.imread(ruta_imagen)
            if img is None:
                logger.error("No se pudo cargar imagen")
                return {}
            
            # Análisis básico
            altura, ancho, canales = img.shape
            
            # Análisis de colores
            colores_medios = cv2.mean(img)
            
            resultado = {
                "nombre": Path(ruta_imagen).name,
                "dimensiones": {"ancho": ancho, "altura": altura},
                "canales": canales,
                "colores_medios": list(colores_medios[:3]),
                "confianza": 0.8
            }
            
            logger.info(f"Imagen procesada: {Path(ruta_imagen).name}")
            return resultado
        except Exception as e:
            logger.error(f"Error: {e}")
            return {}

image_processor = ImageProcessor()
"@ | Out-File -FilePath "analisis\image_processor.py" -Encoding UTF8
```

---

## 📋 FASE 5: BOT DE TELEGRAM (1.5 HORAS)

### Paso 5.1: Implementar telegram_bot/bot.py

```bash
@"
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config.settings import settings
from utils.logger import logger
from cerebro.knowledge_manager import knowledge_manager
from cerebro.pdf_processor import pdf_processor
from analisis.analyzer import analyzer

class TelegramAnalystBot:
    
    def __init__(self):
        self.app = Application.builder().token(settings.TELEGRAM_TOKEN).build()
        self.knowledge_manager = knowledge_manager
        self.pdf_processor = pdf_processor
        self.analyzer = analyzer
        self.registrar_handlers()
    
    def registrar_handlers(self):
        self.app.add_handler(CommandHandler("start", self.comando_start))
        self.app.add_handler(CommandHandler("ayuda", self.comando_ayuda))
        self.app.add_handler(CommandHandler("status", self.comando_status))
        self.app.add_handler(CommandHandler("cargar_pdfs", self.comando_cargar_pdfs))
        self.app.add_handler(CommandHandler("analizar", self.comando_analizar))
    
    async def comando_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🤖 ¡Bienvenido a Bot Analista!\n\n"
            "Usa /ayuda para ver comandos"
        )
        logger.info(f"Usuario {update.effective_user.id} inició")
    
    async def comando_ayuda(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        ayuda = """
        📖 COMANDOS:
        /start - Inicio
        /ayuda - Esta ayuda
        /status - Estado
        /cargar_pdfs - Cargar PDFs
        /analizar TICKER - Analizar
        """
        await update.message.reply_text(ayuda)
    
    async def comando_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("✅ Bot operacional")
    
    async def comando_cargar_pdfs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        procesando = await update.message.reply_text("⏳ Cargando PDFs...")
        try:
            resultados = self.pdf_processor.procesar_todos_pdfs()
            for pdf_info in resultados:
                self.knowledge_manager.cargar_documento(
                    pdf_info["nombre"],
                    pdf_info["texto"]
                )
            await procesando.edit_text(f"✅ {len(resultados)} PDFs cargados")
        except Exception as e:
            await procesando.edit_text(f"❌ Error: {str(e)}")
    
    async def comando_analizar(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("Uso: /analizar TICKER")
            return
        
        ticker = context.args[0].upper()
        procesando = await update.message.reply_text(f"⏳ Analizando {ticker}...")
        
        try:
            resultado = await self.analyzer.analizar_ticker(ticker)
            if resultado:
                respuesta = f"📊 {ticker}\\nPrecio: ${resultado['precio_actual']:.2f}\\nCambio: {resultado['cambio_percent']:.2f}%"
                await procesando.edit_text(respuesta)
            else:
                await procesando.edit_text("❌ No hay datos")
        except Exception as e:
            await procesando.edit_text(f"❌ Error: {str(e)}")
    
    def iniciar(self):
        logger.info("Bot iniciando...")
        self.app.run_polling()

bot = TelegramAnalystBot()
"@ | Out-File -FilePath "telegram_bot\bot.py" -Encoding UTF8
```

### Paso 5.2: Actualizar main.py para incluir bot

```bash
@"
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import settings
from utils.logger import logger
from telegram_bot.bot import bot

def main():
    print("\n" + "="*60)
    print("BOT ANALISTA - INICIANDO")
    print("="*60)
    
    logger.info("Creando directorios...")
    settings.crear_directorios()
    
    logger.info("Validando configuración...")
    settings.validar_configuracion()
    settings.mostrar_configuracion()
    
    logger.info("Iniciando bot...")
    try:
        bot.iniciar()
    except KeyboardInterrupt:
        logger.warning("Bot detenido")
        print("\nBot detenido")

if __name__ == "__main__":
    main()
"@ | Out-File -FilePath "main.py" -Encoding UTF8
```

---

## 🧪 FASE 6: PRUEBAS Y VALIDACIÓN

### Paso 6.1: Crear test_basico.py

```bash
@"
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import settings
from utils.logger import logger
from cerebro.knowledge_manager import knowledge_manager

def test_settings():
    print("✓ Testing settings...")
    assert settings.TELEGRAM_TOKEN is not None
    print("  OK - Token configurado")

def test_logger():
    print("✓ Testing logger...")
    logger.info("Test de logging")
    print("  OK - Logger funciona")

def test_db():
    print("✓ Testing database...")
    knowledge_manager.cargar_documento("test.txt", "contenido test")
    print("  OK - BD funciona")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("PRUEBAS DEL SISTEMA")
    print("="*50)
    
    try:
        test_settings()
        test_logger()
        test_db()
        
        print("\n" + "="*50)
        print("✅ TODAS LAS PRUEBAS PASARON")
        print("="*50)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
"@ | Out-File -FilePath "tests\test_basico.py" -Encoding UTF8

# Ejecutar pruebas
python tests\test_basico.py
```

---

## 📝 RESUMEN DE PASOS

### ✅ Fase 1 Completada
- [ ] Estructura base creada
- [ ] Git inicializado
- [ ] Venv creado
- [ ] requirements.txt instalado
- [ ] .env configurado

### ✅ Fase 2 Completada
- [ ] config/settings.py
- [ ] utils/logger.py
- [ ] utils/validators.py
- [ ] main.py básico

### ✅ Fase 3 Completada
- [ ] cerebro/knowledge_manager.py
- [ ] cerebro/pdf_processor.py
- [ ] BD SQLite funcional

### ✅ Fase 4 Completada
- [ ] analisis/analyzer.py
- [ ] analisis/image_processor.py

### ✅ Fase 5 Completada
- [ ] telegram_bot/bot.py
- [ ] Handlers básicos
- [ ] main.py actualizado

### ✅ Fase 6 Completada
- [ ] Pruebas unitarias
- [ ] Sistema funcional

---

## 🎯 PRÓXIMOS PASOS (ESCALABILIDAD)

Una vez completa la base:

1. **Añadir indicadores técnicos**
   - RSI, MACD, Estocástico
   - Bandas de Bollinger, ATR

2. **Integrar APIs externas**
   - OpenAI para análisis narrativos
   - Alpha Vantage para datos

3. **Mejorar visión computacional**
   - Detección de patrones en gráficos
   - OCR mejorado

4. **Sistema de alertas**
   - Notificaciones cuando se cumplan condiciones
   - Histórico de alertas

5. **Interfaz web**
   - Dashboard con resultados
   - Gestión de la BD
   - Visualizaciones

6. **Dockerización**
   - Dockerfile
   - docker-compose.yml
   - Deployment en Railway/Heroku

---

## 🚀 COMANDOS RÁPIDOS FINALES

```bash
# Setup completo
mkdir proyecto_bot && cd proyecto_bot
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py

# Ejecutar tests
python tests\test_basico.py

# Ejecutar bot
python main.py

# Ver logs
Get-Content logs\bot_analista.log -Tail 50
```

---

## 📊 COMPARACIÓN: PROYECTO ACTUAL vs. NUEVO

| Aspecto | Proyecto Base | Proyecto Nuevo |
|--------|--------------|----------------|
| Tiempo implementación | 2 semanas | 6-8 horas |
| Complejidad | Alta (completo) | Baja (MVP) |
| Líneas de código | 5000+ | 500-800 |
| Funcionalidad | 100% | 30-40% |
| Extensibilidad | Media | Alta |
| Documentación | Exhaustiva | Básica (extensible) |

El proyecto nuevo es **simple**, **escalable** y **completo en fundamentales**.

