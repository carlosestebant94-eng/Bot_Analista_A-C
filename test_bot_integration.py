"""
test_bot_integration.py
Test de integración del bot con AnalysisMethodology
"""

import sys
from pathlib import Path

# Agregar el directorio al path
sys.path.insert(0, str(Path(__file__).parent))

print("="*80)
print("TEST DE INTEGRACION - Bot + AnalysisMethodology")
print("="*80)
print()

# Test 1: Verificar que el bot carga
print("1. Cargando TelegramAnalystBot...")
try:
    from telegram_bot.bot import TelegramAnalystBot
    print("   OK - Modulo importado correctamente")
except Exception as e:
    print(f"   ERROR: {e}")
    sys.exit(1)

# Test 2: Instanciar el bot
print()
print("2. Instanciando TelegramAnalystBot...")
try:
    bot = TelegramAnalystBot()
    print("   OK - Bot instanciado correctamente")
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Verificar que AnalysisMethodology está disponible
print()
print("3. Verificando AnalysisMethodology...")
try:
    if hasattr(bot, 'analysis_methodology'):
        print("   OK - analysis_methodology cargado en bot")
        status = bot.analysis_methodology.get_status()
        print(f"      Estado: {status['estado']}")
        print(f"      Metodologia: {status['metodologia']}")
    else:
        print("   ERROR - analysis_methodology NO encontrado en bot")
        sys.exit(1)
except Exception as e:
    print(f"   ERROR: {e}")
    sys.exit(1)

# Test 4: Verificar que el bot tiene el comando _generar_texto_indicadores
print()
print("4. Verificando metodo auxiliar...")
try:
    if hasattr(bot, '_generar_texto_indicadores'):
        print("   OK - _generar_texto_indicadores cargado")
    else:
        print("   ERROR - _generar_texto_indicadores NO encontrado")
        sys.exit(1)
except Exception as e:
    print(f"   ERROR: {e}")
    sys.exit(1)

print()
print("="*80)
print("OK - TODOS LOS TESTS PASARON - Bot integrado correctamente")
print("="*80)
print()
print("El bot esta listo para usar:")
print("  /analizar AAPL  -> Analisis completo con Metodologia Alexander")
print("  /analizar MSFT  -> Indicadores + Recomendacion + S/R")
print("  /analizar TSLA  -> Analisis 360")
print()
