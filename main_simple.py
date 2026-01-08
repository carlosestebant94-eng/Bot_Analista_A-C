#!/usr/bin/env python3
"""
main_simple.py
Versión simplificada del bot sin módulos problemáticos
Solo carga lo esencial para que el bot responda
"""

import asyncio
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración básica
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not TELEGRAM_TOKEN:
    print("❌ ERROR: TELEGRAM_BOT_TOKEN no configurado en .env")
    exit(1)

if not GOOGLE_API_KEY:
    print("❌ ERROR: GOOGLE_API_KEY no configurado en .env")
    exit(1)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("BotSimple")

print("=" * 60)
print("🤖 BOT ANALISTA A&C - VERSIÓN SIMPLIFICADA")
print("=" * 60)
print(f"✅ Telegram Token: Configurado")
print(f"✅ Google API Key: Configurado")
print("=" * 60)
print("✅ Bot en funcionamiento. Esperando mensajes...")
print("=" * 60)

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    await update.message.reply_text(
        "🤖 ¡Hola! Soy el Bot Analista A&C.\n\n"
        "Comandos disponibles:\n"
        "/ayuda - Ver todos los comandos\n"
        "/analizar AAPL - Analizar un símbolo\n"
        "/exportar_pdf - Exportar último análisis a PDF"
    )

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /ayuda"""
    await update.message.reply_text(
        "📚 **AYUDA DEL BOT**\n\n"
        "Comandos:\n"
        "/start - Inicio\n"
        "/ayuda - Esta pantalla\n"
        "/analizar SIMBOLO - Analizar un símbolo (ej: /analizar AAPL)\n"
        "/exportar_pdf - Exportar análisis a PDF\n"
        "/status - Estado del bot"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /status"""
    await update.message.reply_text(
        "✅ **ESTADO DEL BOT**\n\n"
        "🟢 Bot en línea\n"
        "✅ Telegram: Conectado\n"
        "✅ Google AI: Configurado\n"
        "📚 Base de datos: Lista"
    )

async def analizar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /analizar"""
    if not context.args:
        await update.message.reply_text(
            "❌ Por favor especifica un símbolo.\n"
            "Ejemplo: /analizar AAPL"
        )
        return
    
    simbolo = context.args[0].upper()
    await update.message.reply_text(
        f"⏳ Analizando {simbolo}...\n\n"
        "✅ Análisis completado\n\n"
        "📊 Plan de Acción Trading:\n"
        "• Entry: Pendiente\n"
        "• Stop Loss: Pendiente\n"
        "• Take Profit: Pendiente\n"
        "• Recomendación: Espera módulo completo\n\n"
        "💾 Puedes exportar a PDF con: /exportar_pdf"
    )

async def exportar_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /exportar_pdf"""
    await update.message.reply_text(
        "📄 Función de PDF pendiente del módulo completo"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejo de mensajes de texto"""
    await update.message.reply_text(
        "Mensaje recibido. Usa /ayuda para ver los comandos disponibles."
    )

async def main():
    """Función principal"""
    # Crear aplicación
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Registrar handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("analizar", analizar))
    app.add_handler(CommandHandler("exportar_pdf", exportar_pdf))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Iniciar
    async with app:
        await app.start()
        logger.info("🤖 Bot iniciado correctamente")
        await app.updater.start_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        exit(1)
