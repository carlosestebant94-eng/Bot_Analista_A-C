#!/usr/bin/env python3
"""
Script de diagnóstico para error en QQQ
Verifica obtención de datos y validación
"""

import sys
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Intentar importar yfinance
try:
    import yfinance as yf
    print("✅ yfinance importado correctamente")
except ImportError as e:
    print(f"❌ Error importando yfinance: {e}")
    sys.exit(1)

# Intentar obtener datos de QQQ
print("\n" + "="*60)
print("DIAGNÓSTICO DE DATOS PARA QQQ")
print("="*60)

ticker_symbol = "QQQ"
print(f"\n1. Intentando obtener datos brutos de {ticker_symbol}...")

try:
    stock = yf.Ticker(ticker_symbol)
    print(f"   ✅ Objeto Ticker creado")
    
    # Obtener info completa
    print(f"\n2. Obteniendo info completa...")
    info = stock.info
    print(f"   ✅ Info obtenida ({len(info)} campos)")
    
    # Imprimir campos relevantes
    print(f"\n3. Campos de precio disponibles:")
    precio_fields = [
        'currentPrice',
        'regularMarketPrice',
        'last',
        'open',
        'dayHigh',
        'dayLow',
        'fiftyTwoWeekHigh',
        'fiftyTwoWeekLow'
    ]
    
    for field in precio_fields:
        value = info.get(field)
        print(f"   - {field:25} = {value}")
    
    # Detectar precio actual
    precio = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("last")
    print(f"\n4. Precio detectado: {precio}")
    
    if precio is None or precio == 0:
        print(f"   ⚠️  Precio es None/0, intentando histórico...")
        hist = stock.history(period="1d")
        if not hist.empty:
            precio = hist['Close'].iloc[-1]
            print(f"   ✅ Precio del histórico: {precio}")
        else:
            print(f"   ❌ No hay histórico disponible")
    
    # Validar precio
    print(f"\n5. Validación de precio:")
    
    from data_sources.data_validator import DataValidator
    validator = DataValidator()
    is_valid, error_msg = validator.validar_precio(precio, ticker_symbol)
    
    print(f"   - Precio: {precio}")
    print(f"   - Válido: {is_valid}")
    if error_msg:
        print(f"   - Error: {error_msg}")
    
    # Información adicional
    print(f"\n6. Información adicional:")
    print(f"   - Nombre: {info.get('longName', 'N/A')}")
    print(f"   - Sector: {info.get('sector', 'N/A')}")
    print(f"   - Market Cap: {info.get('marketCap', 'N/A')}")
    print(f"   - Volumen: {info.get('volume', 'N/A')}")
    print(f"   - Cambio %: {info.get('regularMarketChangePercent', 'N/A')}")
    
    # Probar con otros tickers
    print(f"\n7. Pruebas comparativas:")
    
    test_tickers = ["AAPL", "SPY", "IWM"]
    for test_ticker in test_tickers:
        try:
            test_stock = yf.Ticker(test_ticker)
            test_info = test_stock.info
            test_precio = test_info.get("currentPrice") or test_info.get("regularMarketPrice")
            is_valid_test, _ = validator.validar_precio(test_precio, test_ticker)
            print(f"   - {test_ticker}: Precio={test_precio}, Válido={is_valid_test}")
        except Exception as e:
            print(f"   - {test_ticker}: Error - {e}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("FIN DEL DIAGNÓSTICO")
print("="*60)
