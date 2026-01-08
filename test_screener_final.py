#!/usr/bin/env python3
"""
Validación final del screener antes de lanzamiento
"""
print("="*60)
print("VALIDACION FINAL DEL SCREENER")
print("="*60)

# Test 1: Importar el screener
try:
    from analisis import ScreenerAutomatico, Timeframe
    print("\n1. Importacion del screener: OK")
except Exception as e:
    print(f"\n1. ERROR importando: {e}")
    exit(1)

# Test 2: Crear instancia
try:
    screener = ScreenerAutomatico()
    print("2. Inicializacion del screener: OK")
except Exception as e:
    print(f"2. ERROR: {e}")
    exit(1)

# Test 3: Analizar un simbolo
try:
    resultado = screener.analizar_simbolo('AAPL', Timeframe.MEDIUM_TERM)
    if resultado:
        print(f"3. Analisis AAPL: OK")
        print(f"   - Precio: ${resultado.precio_actual:.2f}")
        print(f"   - Recomendacion: {resultado.recomendacion}")
        print(f"   - Score: {resultado.score:.1f}/100")
        print(f"   - Confianza: {resultado.confianza:.0%}")
    else:
        print("3. ERROR: No se obtuvo resultado")
        exit(1)
except Exception as e:
    print(f"3. ERROR: {e}")
    exit(1)

# Test 4: Bot integration
try:
    from telegram_bot import TelegramAnalystBot
    print("4. Integracion con bot: OK")
except Exception as e:
    print(f"4. ERROR: {e}")
    exit(1)

print("\n" + "="*60)
print("TODOS LOS TESTS PASARON - SCREENER LISTO")
print("="*60)
