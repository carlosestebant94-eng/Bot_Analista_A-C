#!/usr/bin/env python3
"""
test_bot_simple.py
Prueba simple de inicialización del bot
"""

import sys
import traceback

print("🔍 Probando imports...")

try:
    print("  1. Importando config...")
    from config import Settings
    print("     ✅ config OK")
    
    print("  2. Importando cerebro...")
    from cerebro import KnowledgeManager
    print("     ✅ cerebro OK")
    
    print("  3. Importando analisis...")
    from analisis import Analyzer
    print("     ✅ analisis OK")
    
    print("  4. Importando ia...")
    from ia import AIEngine
    print("     ✅ ia OK")
    
    print("  5. Importando utils...")
    from utils import setup_logger
    print("     ✅ utils OK")
    
    print("  6. Importando PDFReportGenerator...")
    from utils.pdf_generator import PDFReportGenerator
    print("     ✅ pdf_generator OK")
    
    print("  7. Importando telegram_bot...")
    from telegram_bot import TelegramAnalystBot
    print("     ✅ telegram_bot OK")
    
    print("\n✅ TODOS LOS IMPORTS CORRECTOS")
    print("\nAhora inicializando bot...")
    
    bot = TelegramAnalystBot()
    print("✅ Bot inicializado sin errores")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    traceback.print_exc()
    sys.exit(1)
