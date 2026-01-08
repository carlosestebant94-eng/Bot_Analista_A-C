#!/usr/bin/env python3
"""
test_gemini_profesional.py
Prueba del nuevo AIEngine v2.0 con Instrucción Maestra Profesional
Demuestra análisis determinista y profesional con Gemini
"""

import sys
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from ia.ai_engine import AIEngine
from dotenv import load_dotenv
import json

# Cargar variables de entorno
load_dotenv()


def test_analisis_profesional():
    """Prueba análisis profesional de ticker"""
    print("\n" + "="*80)
    print("🧪 TEST: ANÁLISIS PROFESIONAL CON INSTRUCCIÓN MAESTRA")
    print("="*80)
    
    # Inicializar motor IA
    ai_engine = AIEngine()
    
    if not ai_engine.enabled:
        print("❌ IA no está configurada. Verifica GOOGLE_API_KEY en .env")
        return
    
    print("✅ AIEngine inicializado correctamente")
    print(f"   Modelo: Gemini 2.5 Pro")
    print(f"   Modo: INSTRUCCIÓN MAESTRA PROFESIONAL")
    
    # Datos de ejemplo: Apple (AAPL)
    ticker = "AAPL"
    
    datos_tecnicos = {
        "Precio Actual": "$228.55",
        "SMA(20)": "$225.30",
        "RSI(14)": "62.5",
        "MACD": "Cruce alcista en progreso",
        "Stochastic": "68.2 (cerca sobrecompra)",
        "Soporte": "$225.00",
        "Resistencia": "$232.00",
        "Volumen vs Promedio": "110%"
    }
    
    datos_fundamentales = {
        "P/E Ratio": "32.5",
        "Sector P/E Promedio": "20.5",
        "Market Cap": "$3.2T",
        "Debt-to-Equity": "1.8",
        "ROE": "92%",
        "PEG Ratio": "1.85",
        "Dividend Yield": "0.42%",
        "Forecast EPS Growth": "8-12% anual"
    }
    
    datos_macro = {
        "VIX": "14.5 (Bajando - Riesgo reducido)",
        "Rendimiento T10Y": "4.25%",
        "Tasa Fed": "5.25-5.50%",
        "Inflación": "3.2% YoY",
        "Sentimiento Mercado": "Neutral-Alcista",
        "SPY Performance": "+2.5% últimas 2 semanas"
    }
    
    contexto_libro = """
De libros de trading profesional:
- Divergencia Bullish: cuando precio toca nuevo mínimo pero oscilador sube = Posible reversión alcista
- Entrada en Sobreventa: RSI < 30 puede generar rebote rápido
- Confirmación: Precio + Volumen + Oscilador deben alinearse en la misma dirección
- Risk Management: Stop Loss siempre 2-3% debajo del entry
- Gestión de Posición: Take Profit en resistencias claves
    """
    
    print("\n📊 INICIANDO ANÁLISIS PROFESIONAL...")
    print(f"   Ticker: {ticker}")
    print(f"   Temperatura: 0.2 (Determinista)")
    print(f"   Sistema: Instrucción Maestra Completa")
    
    # Llamar método de análisis profesional
    resultado = ai_engine.analizar_ticker_profesional(
        ticker=ticker,
        datos_tecnicos=datos_tecnicos,
        datos_fundamentales=datos_fundamentales,
        datos_macro=datos_macro,
        contexto_conocimiento=contexto_libro
    )
    
    print("\n" + "="*80)
    print(f"📈 REPORTE ANALÍTICO: {ticker}")
    print("="*80)
    
    if resultado.get("error"):
        print(f"❌ Error: {resultado.get('respuesta')}")
        return
    
    print(resultado.get("respuesta"))
    
    print("\n" + "="*80)
    print("📋 METADATA DE RESPUESTA")
    print("="*80)
    print(f"Modo: {resultado.get('modo', 'N/A')}")
    print(f"Modelo: {resultado.get('modelo', 'N/A')}")
    print(f"Confianza: {resultado.get('confianza', 0.0)*100:.0f}%")
    print(f"Fuente: {resultado.get('fuente', 'N/A')}")
    print(f"Proveedor: {resultado.get('proveedor', 'N/A')}")
    

def test_razonamiento_profesional():
    """Prueba razonamiento con instrucción maestra"""
    print("\n" + "="*80)
    print("🧠 TEST: RAZONAMIENTO PROFESIONAL")
    print("="*80)
    
    ai_engine = AIEngine()
    
    if not ai_engine.enabled:
        print("❌ IA no está configurada")
        return
    
    pregunta = """
Un stock tiene:
- RSI = 28 (Sobreventa)
- Precio toca SMA20
- Earnings en 3 días
- Volumen 150% del promedio
- Insider buying la semana pasada

¿Qué recomendación debe darse según análisis determinista?
    """
    
    print("\n❓ PREGUNTA:")
    print(pregunta)
    
    print("\n🔄 Procesando con Instrucción Maestra (Temperatura: 0.2)...")
    
    resultado = ai_engine.razonar(
        pregunta=pregunta,
        temperatura=0.2,
        usar_instruccion_maestra=True
    )
    
    print("\n💡 RESPUESTA PROFESIONAL:")
    print("="*80)
    print(resultado.get("respuesta"))
    print("="*80)
    
    print(f"\nConfianza: {resultado.get('confianza', 0.0)*100:.0f}%")
    print(f"Modo: {resultado.get('modo', 'N/A')}")


def test_comparacion_temperaturas():
    """Compara respuestas con diferentes temperaturas"""
    print("\n" + "="*80)
    print("🌡️  TEST: IMPACTO DE TEMPERATURA EN DETERMINISMO")
    print("="*80)
    
    ai_engine = AIEngine()
    
    if not ai_engine.enabled:
        print("❌ IA no está configurada")
        return
    
    pregunta = "¿Cuál es el RSI óptimo para entrada en compra? Da una respuesta binaria y determinista."
    
    for temp in [0.1, 0.3, 0.7]:
        print(f"\n🔹 TEMPERATURA: {temp}")
        print("-" * 80)
        
        resultado = ai_engine.razonar(
            pregunta=pregunta,
            temperatura=temp,
            usar_instruccion_maestra=True
        )
        
        respuesta = resultado.get("respuesta", "")
        # Mostrar solo primeras 200 caracteres
        print(respuesta[:200] + "..." if len(respuesta) > 200 else respuesta)


if __name__ == "__main__":
    try:
        # Test 1: Análisis Profesional
        test_analisis_profesional()
        
        # Test 2: Razonamiento Profesional
        test_razonamiento_profesional()
        
        # Test 3: Comparación de Temperaturas
        test_comparacion_temperaturas()
        
        print("\n" + "="*80)
        print("✅ TODOS LOS TESTS COMPLETADOS")
        print("="*80)
        print("\n📝 NOTAS:")
        print("- La Instrucción Maestra garantiza respuestas deterministas")
        print("- Temperatura baja (0.1-0.3) = Máximo determinismo")
        print("- Formato Markdown estructurado en todas las respuestas")
        print("- Veredictos binarios (COMPRA/VENTA/ESPERA)")
        print("- Análisis profesional e institucional")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrumpido por usuario")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
