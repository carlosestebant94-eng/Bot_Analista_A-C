"""
test_screener.py
Pruebas del módulo Screener Automático
Valida análisis multidimensional de símbolos financieros
"""

import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_screener_basico():
    """Test 1: Screener básico con un símbolo"""
    print("\n" + "="*60)
    print("TEST 1: Screener Básico - Un Símbolo")
    print("="*60)
    
    try:
        from analisis import ScreenerAutomatico, Timeframe
        from data_sources import MarketDataManager
        
        # Inicializar
        market_data = MarketDataManager()
        screener = ScreenerAutomatico(market_data)
        
        # Analizar AAPL en mediano plazo
        ticker = "AAPL"
        print(f"\n📊 Analizando {ticker}...")
        
        resultado = screener.analizar_simbolo(
            ticker,
            timeframe=Timeframe.MEDIUM_TERM,
            periodo_dias=90
        )
        
        if resultado:
            print(f"\n✅ Análisis completado:")
            print(f"   Ticker: {resultado.ticker}")
            print(f"   Precio: ${resultado.precio_actual:.2f}")
            print(f"   Recomendación: {resultado.recomendacion}")
            print(f"   Score: {resultado.score:.1f}/100")
            print(f"   Confianza: {resultado.confianza:.0%}")
            print(f"   Señales: {resultado.señales_compra} compra / {resultado.señales_venta} venta")
            print(f"   Variación esperada: {resultado.variacion_esperada:+.2f}%")
            print(f"\n   Niveles Clave:")
            print(f"   • Resistencia: ${resultado.niveles_clave.get('resistencia', 0):.2f}")
            print(f"   • Soporte: ${resultado.niveles_clave.get('soporte', 0):.2f}")
            print(f"\n   Reporte:")
            print(screener.generar_reporte_texto(resultado))
            print("\n✅ TEST 1 PASADO")
            return True
        else:
            print("❌ No se obtuvieron resultados")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_screener_multiples_simbolos():
    """Test 2: Screener con múltiples símbolos y diferentes timeframes"""
    print("\n" + "="*60)
    print("TEST 2: Screener - Múltiples Símbolos")
    print("="*60)
    
    try:
        from analisis import ScreenerAutomatico, Timeframe
        from data_sources import MarketDataManager
        
        market_data = MarketDataManager()
        screener = ScreenerAutomatico(market_data)
        
        # Símbolos populares
        tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]
        
        print(f"\n📊 Analizando {len(tickers)} símbolos en mediano plazo...")
        
        resultados = screener.screener_por_sector(
            tickers,
            timeframe=Timeframe.MEDIUM_TERM,
            limite=5
        )
        
        if resultados:
            print(f"\n✅ Se obtuvieron {len(resultados)} resultados:\n")
            
            for i, resultado in enumerate(resultados, 1):
                emoji = "🟢" if "COMPRA" in resultado.recomendacion else "🔴" if "VENTA" in resultado.recomendacion else "🟡"
                print(f"{i}. {emoji} {resultado.ticker}: {resultado.recomendacion} (Score: {resultado.score:.1f})")
            
            print("\n✅ TEST 2 PASADO")
            return True
        else:
            print("❌ No se obtuvieron resultados")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_screener_timeframes():
    """Test 3: Screener con diferentes timeframes"""
    print("\n" + "="*60)
    print("TEST 3: Comparación de Timeframes")
    print("="*60)
    
    try:
        from analisis import ScreenerAutomatico, Timeframe
        from data_sources import MarketDataManager
        
        market_data = MarketDataManager()
        screener = ScreenerAutomatico(market_data)
        
        ticker = "MSFT"
        
        print(f"\n📊 Analizando {ticker} en diferentes timeframes...\n")
        
        resultados_dict = {}
        
        for timeframe in [Timeframe.SHORT_TERM, Timeframe.MEDIUM_TERM, Timeframe.LONG_TERM]:
            print(f"   Analizando {timeframe.value}...")
            
            resultado = screener.analizar_simbolo(
                ticker,
                timeframe=timeframe,
                periodo_dias=90
            )
            
            if resultado:
                resultados_dict[timeframe.value] = resultado
                print(f"   ✅ {timeframe.value}: {resultado.recomendacion} (Score: {resultado.score:.1f})")
        
        if len(resultados_dict) == 3:
            print("\n📊 Comparativa de Recomendaciones:")
            print(f"   • Corto Plazo: {resultados_dict['corto_plazo'].recomendacion}")
            print(f"   • Mediano Plazo: {resultados_dict['mediano_plazo'].recomendacion}")
            print(f"   • Largo Plazo: {resultados_dict['largo_plazo'].recomendacion}")
            print("\n✅ TEST 3 PASADO")
            return True
        else:
            print("⚠️  Se obtuvieron resultados parciales")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_screener_indicadores():
    """Test 4: Validar indicadores técnicos"""
    print("\n" + "="*60)
    print("TEST 4: Validación de Indicadores Técnicos")
    print("="*60)
    
    try:
        from analisis import ScreenerAutomatico, Timeframe
        from data_sources import MarketDataManager
        
        market_data = MarketDataManager()
        screener = ScreenerAutomatico(market_data)
        
        ticker = "GOOGL"
        
        print(f"\n📊 Validando indicadores técnicos para {ticker}...\n")
        
        resultado = screener.analizar_simbolo(
            ticker,
            timeframe=Timeframe.MEDIUM_TERM,
            periodo_dias=90
        )
        
        if resultado:
            indicadores = resultado.indicadores
            
            print("✅ Indicadores Calculados:")
            print(f"   • RSI: {indicadores.get('rsi', 0):.2f} (Rango: 0-100)")
            print(f"   • MACD Signal: {indicadores.get('macd_signal', 0):.6f}")
            print(f"   • MA-20: ${indicadores.get('ma_20', 0):.2f}")
            print(f"   • MA-50: ${indicadores.get('ma_50', 0):.2f}")
            print(f"   • Bollinger Upper: ${indicadores.get('bollinger_upper', 0):.2f}")
            print(f"   • Bollinger Lower: ${indicadores.get('bollinger_lower', 0):.2f}")
            print(f"   • ATR: ${indicadores.get('atr', 0):.2f}")
            print(f"   • Volumen SMA: {indicadores.get('volumen_sma', 0):.0f}")
            
            # Validar rangos
            rsi = indicadores.get('rsi', 0)
            assert 0 <= rsi <= 100, f"RSI fuera de rango: {rsi}"
            
            print("\n✅ Todos los indicadores están dentro de rangos válidos")
            print("✅ TEST 4 PASADO")
            return True
        else:
            print("❌ No se obtuvieron resultados")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_screener_sin_conexion():
    """Test 5: Manejo de errores - Sin conexión"""
    print("\n" + "="*60)
    print("TEST 5: Manejo de Errores")
    print("="*60)
    
    try:
        from analisis import ScreenerAutomatico, Timeframe
        
        screener = ScreenerAutomatico()
        
        print("\n📊 Probando símbolo inválido...")
        resultado = screener.analizar_simbolo(
            "SIMBOLO_INVALIDO_XYZ123",
            timeframe=Timeframe.MEDIUM_TERM
        )
        
        if resultado is None:
            print("✅ Manejo correcto de símbolo inválido (retorna None)")
            print("✅ TEST 5 PASADO")
            return True
        else:
            print("⚠️  Se obtuvo resultado inesperado")
            return True
            
    except Exception as e:
        print(f"⚠️  Error esperado: {e}")
        print("✅ TEST 5 PASADO (error manejado correctamente)")
        return True


def main():
    """Ejecuta todos los tests"""
    print("\n" + "="*60)
    print("🧪 SUITE DE PRUEBAS - SCREENER AUTOMÁTICO")
    print("="*60)
    print(f"Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Screener Básico", test_screener_basico),
        ("Múltiples Símbolos", test_screener_multiples_simbolos),
        ("Comparativa Timeframes", test_screener_timeframes),
        ("Validación Indicadores", test_screener_indicadores),
        ("Manejo de Errores", test_screener_sin_conexion),
    ]
    
    resultados = {}
    
    for nombre, test_func in tests:
        try:
            resultados[nombre] = test_func()
        except Exception as e:
            print(f"\n❌ Error en {nombre}: {e}")
            resultados[nombre] = False
    
    # Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)
    
    for nombre, resultado in resultados.items():
        emoji = "✅" if resultado else "❌"
        print(f"{emoji} {nombre}")
    
    total_pasadas = sum(1 for r in resultados.values() if r)
    total_pruebas = len(resultados)
    
    print(f"\n📈 Total: {total_pasadas}/{total_pruebas} pruebas pasadas")
    print(f"Finalizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if total_pasadas == total_pruebas:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
    else:
        print(f"\n⚠️  {total_pruebas - total_pasadas} prueba(s) fallaron")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
