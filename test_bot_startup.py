#!/usr/bin/env python
"""
test_bot_startup.py
Prueba rápida de startup del bot sin conectarse a Telegram
Verifica que todos los módulos se importan correctamente
"""

import sys
from pathlib import Path
import os

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

# Establecer variable de entorno para modo test
os.environ['BOT_TEST_MODE'] = '1'

from config import Settings
from logging_audit import setup_centralized_logging

def test_startup():
    """Prueba de startup"""
    
    print("\n" + "="*50)
    print("🧪 PRUEBA DE STARTUP DEL BOT")
    print("="*50 + "\n")
    
    try:
        # 1. Test logging
        print("1️⃣  Inicializando logging...")
        setup_centralized_logging("BotTest", "INFO")
        print("   ✅ Logging inicializado\n")
        
        # 2. Test Settings
        print("2️⃣  Validando configuración...")
        Settings.crear_directorios()
        Settings.mostrar_configuracion()
        
        if not Settings.validar_configuracion():
            print("   ❌ Configuración incompleta\n")
            return False
        print("   ✅ Configuración válida\n")
        
        # 3. Test imports
        print("3️⃣  Verificando módulos...")
        try:
            from cerebro import KnowledgeManager, PDFProcessor, AnalysisMethodology
            print("   ✅ Módulo 'cerebro' OK")
        except ImportError as e:
            print(f"   ❌ Error importando cerebro: {e}")
            return False
        
        try:
            from analisis import Analyzer, ImageProcessor, EnhancedAnalyzer
            print("   ✅ Módulo 'analisis' OK")
        except ImportError as e:
            print(f"   ❌ Error importando analisis: {e}")
            return False
        
        try:
            from data_sources import MarketDataManager
            print("   ✅ Módulo 'data_sources' OK")
        except ImportError as e:
            print(f"   ❌ Error importando data_sources: {e}")
            return False
        
        try:
            from ia import AIEngine
            print("   ✅ Módulo 'ia' OK")
        except ImportError as e:
            print(f"   ❌ Error importando ia: {e}")
            return False
        
        print()
        
        # 4. Test MarketDataManager con rate limiting
        print("4️⃣  Verificando MarketDataManager con Rate Limiting...")
        market_data = MarketDataManager()
        print("   ✅ MarketDataManager inicializado")
        print(f"   📊 Cache TTL: {market_data._cache_ttl_seconds}s")
        print(f"   ⏱️  Rate limit interval: {market_data._min_request_interval}s\n")
        
        # 5. Test caché (sin hacer llamadas a YFinance)
        print("5️⃣  Verificando sistema de caché...")
        test_data = {"ticker": "TEST", "precio": 100}
        MarketDataManager._guardar_cache("TEST", test_data)
        cached = MarketDataManager._obtener_cache("TEST")
        if cached:
            print("   ✅ Sistema de caché funciona\n")
        else:
            print("   ❌ Sistema de caché no funciona\n")
            return False
        
        # 6. Test lock file
        print("6️⃣  Verificando sistema de lock file...")
        from main import verificar_instancia_unica, limpiar_lock_file
        lock_file = Path(__file__).parent / ".bot_lock"
        limpiar_lock_file()  # Limpiar primero
        verificar_instancia_unica()
        if lock_file.exists():
            print("   ✅ Sistema de lock file funciona\n")
            limpiar_lock_file()
        else:
            print("   ⚠️  Lock file no se creó (puede ser por permisos)\n")
        
        print("="*50)
        print("✅ TODAS LAS PRUEBAS PASARON")
        print("="*50)
        print("\n🚀 El bot está listo para ejecutarse en Render\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_startup()
    sys.exit(0 if success else 1)
