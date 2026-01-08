#!/usr/bin/env python3
"""
ejemplo_plan_accion_trading.py
Demuestra cómo calcular plan de acción (Entry, Stop, Target, Plazo)
basado en análisis técnicos y fundamentales
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ia.ai_engine import AIEngine
from dotenv import load_dotenv

load_dotenv()


def ejemplo_plan_compra():
    """Ejemplo: Plan de acción para COMPRA"""
    print("\n" + "="*80)
    print("📈 EJEMPLO 1: PLAN DE ACCIÓN - SEÑAL DE COMPRA")
    print("="*80)
    
    ai_engine = AIEngine()
    
    if not ai_engine.enabled:
        print("❌ IA no configurada")
        return
    
    # Datos del análisis
    ticker = "AAPL"
    precio_actual = 228.55
    
    datos_tecnicos = {
        "RSI(14)": "62.5 (Neutral)",
        "MACD": "Cruce alcista",
        "Soporte Principal": "$225.00",
        "Resistencia": "$235.00",
        "ATR (14)": "$3.50",
        "Volatilidad": "Media",
        "Volumen": "110% del promedio"
    }
    
    datos_fundamentales = {
        "P/E Ratio": "32.5",
        "Sector P/E": "20.5",
        "Target Price (Analyst)": "$240",
        "52 Week High": "$245",
        "52 Week Low": "$150",
        "Dividend Yield": "0.42%"
    }
    
    # Calcular plan de acción
    print(f"\n🎯 Calculando plan de acción para {ticker}...")
    print(f"   Precio Actual: ${precio_actual}")
    print(f"   Veredicto: COMPRA")
    
    resultado = ai_engine.calcular_plan_accion_trading(
        ticker=ticker,
        precio_actual=precio_actual,
        datos_tecnicos=datos_tecnicos,
        datos_fundamentales=datos_fundamentales,
        veredicto="COMPRA",
        contexto_analisis="Análisis técnico muestra divergencia alcista, momentum positivo"
    )
    
    print("\n" + "="*80)
    print("📋 PLAN DE ACCIÓN GENERADO:")
    print("="*80)
    
    if resultado.get("error"):
        print(f"❌ Error: {resultado.get('respuesta')}")
        return
    
    print(resultado.get("respuesta"))


def ejemplo_plan_venta():
    """Ejemplo: Plan de acción para VENTA"""
    print("\n" + "="*80)
    print("📉 EJEMPLO 2: PLAN DE ACCIÓN - SEÑAL DE VENTA")
    print("="*80)
    
    ai_engine = AIEngine()
    
    if not ai_engine.enabled:
        print("❌ IA no configurada")
        return
    
    # Datos del análisis
    ticker = "TSLA"
    precio_actual = 245.30
    
    datos_tecnicos = {
        "RSI(14)": "75.2 (Sobrecompra)",
        "MACD": "Cruce bajista",
        "Soporte Principal": "$235.00",
        "Resistencia": "$250.00",
        "ATR (14)": "$4.20",
        "Volatilidad": "Alta",
        "Volumen": "120% del promedio"
    }
    
    datos_fundamentales = {
        "P/E Ratio": "65.0",
        "Sector P/E": "25.0",
        "Target Price (Analyst)": "$220",
        "52 Week High": "$280",
        "52 Week Low": "$120",
        "Debt-to-Equity": "2.5 (Alto)"
    }
    
    print(f"\n🎯 Calculando plan de acción para {ticker}...")
    print(f"   Precio Actual: ${precio_actual}")
    print(f"   Veredicto: VENTA")
    
    resultado = ai_engine.calcular_plan_accion_trading(
        ticker=ticker,
        precio_actual=precio_actual,
        datos_tecnicos=datos_tecnicos,
        datos_fundamentales=datos_fundamentales,
        veredicto="VENTA",
        contexto_analisis="RSI en sobrecompra, MACD en cruce bajista, P/E muy elevado"
    )
    
    print("\n" + "="*80)
    print("📋 PLAN DE ACCIÓN GENERADO:")
    print("="*80)
    
    if resultado.get("error"):
        print(f"❌ Error: {resultado.get('respuesta')}")
        return
    
    print(resultado.get("respuesta"))


def ejemplo_plan_multiticket():
    """Ejemplo: Planes para múltiples tickers"""
    print("\n" + "="*80)
    print("📊 EJEMPLO 3: PLANES PARA MÚLTIPLES TICKERS")
    print("="*80)
    
    ai_engine = AIEngine()
    
    if not ai_engine.enabled:
        print("❌ IA no configurada")
        return
    
    tickers_analisis = [
        {
            "ticker": "MSFT",
            "precio": 385.45,
            "veredicto": "COMPRA",
            "soporte": 380.00,
            "resistencia": 395.00,
            "pe": 35.2
        },
        {
            "ticker": "GOOGL",
            "precio": 156.80,
            "veredicto": "ESPERA",
            "soporte": 150.00,
            "resistencia": 165.00,
            "pe": 28.5
        },
        {
            "ticker": "AMZN",
            "precio": 194.20,
            "veredicto": "COMPRA",
            "soporte": 188.00,
            "resistencia": 205.00,
            "pe": 42.1
        }
    ]
    
    for i, ticker_data in enumerate(tickers_analisis, 1):
        print(f"\n{'─'*80}")
        print(f"Ticket {i}/{len(tickers_analisis)}: {ticker_data['ticker']}")
        print(f"{'─'*80}")
        
        datos_tech = {
            "Soporte Principal": f"${ticker_data['soporte']:.2f}",
            "Resistencia": f"${ticker_data['resistencia']:.2f}",
            "ATR (14)": f"${(ticker_data['resistencia'] - ticker_data['soporte']) / 2:.2f}",
            "Volatilidad": "Media"
        }
        
        datos_fund = {
            "P/E Ratio": str(ticker_data['pe']),
            "Sector P/E": "25.0",
            "52 Week High": f"${ticker_data['precio'] * 1.15:.2f}",
            "52 Week Low": f"${ticker_data['precio'] * 0.80:.2f}"
        }
        
        resultado = ai_engine.calcular_plan_accion_trading(
            ticker=ticker_data['ticker'],
            precio_actual=ticker_data['precio'],
            datos_tecnicos=datos_tech,
            datos_fundamentales=datos_fund,
            veredicto=ticker_data['veredicto'],
            contexto_analisis=f"Análisis profesional para {ticker_data['ticker']}"
        )
        
        if not resultado.get("error"):
            # Mostrar solo resumen (primeras 600 caracteres)
            respuesta = resultado.get("respuesta", "")
            print(respuesta[:600] + "...\n" if len(respuesta) > 600 else respuesta)


def ejemplo_comparativa_risk_reward():
    """Ejemplo: Comparar risk/reward de diferentes entradas"""
    print("\n" + "="*80)
    print("⚖️  EJEMPLO 4: COMPARATIVA DE RISK/REWARD RATIOS")
    print("="*80)
    
    ai_engine = AIEngine()
    
    if not ai_engine.enabled:
        print("❌ IA no configurada")
        return
    
    print("""
ESCENARIO: Entrada en AAPL a $228.55

Opción 1: Entry AGRESIVA
  Entry: $230 (cerca del precio actual)
  Stop: $224 (2% riesgo)
  Target: $240 (4.3% ganancia)
  R/R: 1:2.15 ✅ BUENO

Opción 2: Entry CONSERVADORA
  Entry: $225 (en soporte)
  Stop: $221 (1.8% riesgo)
  Target: $240 (6.7% ganancia)
  R/R: 1:3.7 ✅ EXCELENTE

Opción 3: Entry PULLBACK
  Entry: $220 (pullback a SMA)
  Stop: $215 (2.3% riesgo)
  Target: $245 (11.4% ganancia)
  R/R: 1:4.96 ✅ MÁS QUE EXCELENTE
    """)
    
    print("💡 CONCLUSIÓN:")
    print("   La mejor opción depende de:")
    print("   ├─ Tu tolerancia al riesgo")
    print("   ├─ Tu plazo de inversión")
    print("   ├─ La volatilidad actual")
    print("   └─ Tu experiencia como trader")


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║          EJEMPLOS: PLAN DE ACCIÓN TRADING CON IA v2.0                    ║
║                                                                            ║
║  Entry Point + Stop Loss + Take Profit + Plazo + Risk/Reward Ratio       ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Ejecutar ejemplos (descomenta los que quieras)
        ejemplo_plan_compra()
        # ejemplo_plan_venta()
        # ejemplo_plan_multiticket()
        ejemplo_comparativa_risk_reward()
        
        print("\n" + "="*80)
        print("✅ EJEMPLOS COMPLETADOS")
        print("="*80)
        
        print("""
📝 NOTAS:

1. ENTRY POINT (Precio de Entrada)
   └─ Usa soportes/resistencias técnicas
   └─ Considera esperar confirmación de volumen
   └─ Para COMPRA: Preferir entrada en soporte
   └─ Para VENTA: Preferir entrada en resistencia

2. STOP LOSS (Protección)
   └─ NUNCA tradear sin stop loss
   └─ Típico: 2-3% del capital por operación
   └─ Coloca debajo de soporte (COMPRA) o arriba de resistencia (VENTA)

3. TAKE PROFIT (Ganancia)
   └─ Usa próxima resistencia/soporte
   └─ Calcula basado en R/R ratio 1:1.5 mínimo
   └─ Considera trailing stop para maximizar ganancias

4. PLAZO PROYECTADO
   └─ ATR alto = Mayor volatilidad = Plazo corto
   └─ ATR bajo = Menor volatilidad = Plazo largo
   └─ Earnings/eventos macro = Modificar plazo

5. RISK/REWARD RATIO
   └─ 1:1 = Rompepuntos (evitar)
   └─ 1:1.5 = Aceptable
   └─ 1:2 = Bueno
   └─ 1:3+ = Excelente
    """)
        
    except KeyboardInterrupt:
        print("\n⚠️  Interrumpido por usuario")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
