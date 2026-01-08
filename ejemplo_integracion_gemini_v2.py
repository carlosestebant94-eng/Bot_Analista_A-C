#!/usr/bin/env python3
"""
ejemplo_integracion_gemini_v2.py
Muestra cómo integrar el nuevo AIEngine v2.0 en tu bot
"""

from ia.ai_engine import AIEngine
from data_sources.market_data import MarketDataManager
import json


def ejemplo_1_analisis_profesional():
    """Ejemplo 1: Análisis profesional de ticker"""
    print("\n" + "="*80)
    print("EJEMPLO 1: ANÁLISIS PROFESIONAL DE TICKER")
    print("="*80)
    
    # Inicializar
    ai_engine = AIEngine()
    market_manager = MarketDataManager()
    
    # Obtener datos reales
    ticker = "AAPL"
    
    # Datos técnicos (ejemplo simplificado)
    datos_technicos = {
        "Precio Actual": "$228.55",
        "SMA(20)": "$225.30",
        "RSI(14)": "62.5",
        "MACD": "Cruce alcista",
        "Stochastic": "68.2",
        "Soporte Principal": "$225.00",
        "Resistencia": "$232.00",
        "Volumen vs Promedio": "110%"
    }
    
    # Datos fundamentales
    datos_fundamentales = {
        "P/E Ratio": "32.5",
        "Sector P/E": "20.5",
        "Market Cap": "$3.2T",
        "Debt-to-Equity": "1.8",
        "ROE": "92%",
        "Dividend Yield": "0.42%"
    }
    
    # Datos macro
    datos_macro = {
        "VIX": "14.5 (bajando)",
        "Fed Rate": "5.25-5.50%",
        "Inflación": "3.2%",
        "Sentimiento": "Neutral-Alcista"
    }
    
    # LLAMAR NUEVO MÉTODO PROFESIONAL
    resultado = ai_engine.analizar_ticker_profesional(
        ticker=ticker,
        datos_tecnicos=datos_technicos,
        datos_fundamentales=datos_fundamentales,
        datos_macro=datos_macro,
        contexto_conocimiento="Análisis basado en principios de trading profesional"
    )
    
    print("\n📊 REPORTE GENERADO:\n")
    print(resultado.get("respuesta", "Error al generar reporte"))
    

def ejemplo_2_razonamiento_profesional():
    """Ejemplo 2: Razonamiento profesional con instrucción maestra"""
    print("\n" + "="*80)
    print("EJEMPLO 2: RAZONAMIENTO PROFESIONAL")
    print("="*80)
    
    ai_engine = AIEngine()
    
    pregunta = """
    Un stock tiene estas características:
    - RSI = 28 (Sobreventa)
    - Precio toca SMA20
    - Earnings en 3 días
    - Volumen 150% del promedio
    - Insider buying la semana pasada
    
    ¿Cuál debe ser la recomendación según análisis determinista?
    Justifica cada paso del razonamiento.
    """
    
    print("\n❓ PREGUNTA:")
    print(pregunta)
    
    # USAR MÉTODO razonar CON INSTRUCCIÓN MAESTRA
    resultado = ai_engine.razonar(
        pregunta=pregunta,
        temperatura=0.2,  # BAJO para máximo determinismo
        usar_instruccion_maestra=True  # ACTIVAR instrucción maestra
    )
    
    print("\n💡 RESPUESTA PROFESIONAL:")
    print("─" * 80)
    print(resultado.get("respuesta"))
    print("─" * 80)
    print(f"\nConfianza: {resultado.get('confianza')*100:.0f}%")
    print(f"Modo: {resultado.get('modo', 'N/A')}")


def ejemplo_3_integracion_bot_telegram():
    """Ejemplo 3: Cómo integrar en bot de Telegram"""
    print("\n" + "="*80)
    print("EJEMPLO 3: INTEGRACIÓN EN BOT DE TELEGRAM")
    print("="*80)
    
    codigo_ejemplo = '''
# En telegram_bot/bot.py, modificar el manejador de /analizar

async def handle_analizar(self, update, context):
    """Manejador de /analizar TICKER"""
    
    user_input = " ".join(context.args)
    ticker = user_input.upper()
    
    # Validar
    if not ticker:
        await self.send_message(chat_id, "Uso: /analizar AAPL")
        return
    
    # Obtener datos
    datos_tech = self.market_manager.obtener_datos_tecnicos(ticker)
    datos_fund = self.market_manager.obtener_fundamentales(ticker)
    datos_macro = self.market_manager.obtener_contexto_macro()
    
    # NUEVO: ANÁLISIS PROFESIONAL CON v2.0
    resultado = self.ai_engine.analizar_ticker_profesional(
        ticker=ticker,
        datos_tecnicos=datos_tech,
        datos_fundamentales=datos_fund,
        datos_macro=datos_macro,
        contexto_conocimiento=self.obtener_principios_conocimiento()
    )
    
    # Responder al usuario CON REPORTE PROFESIONAL
    if resultado.get("error"):
        mensaje = f"❌ Error: {resultado.get('respuesta')}"
    else:
        mensaje = resultado.get("respuesta")  # Markdown profesional
    
    await self.send_message(
        chat_id=chat_id,
        text=mensaje,
        parse_mode="Markdown"  # Para soportar tablas y emojis
    )
    '''
    
    print(codigo_ejemplo)


def ejemplo_4_comparacion_temperaturas():
    """Ejemplo 4: Mostrar diferencia de temperaturas"""
    print("\n" + "="*80)
    print("EJEMPLO 4: IMPACTO DE TEMPERATURA EN DETERMINISMO")
    print("="*80)
    
    ai_engine = AIEngine()
    
    pregunta = "¿Cuál es el umbral óptimo de RSI para entrada en compra? Sé binario y determinista."
    
    print("\nPregunta:", pregunta)
    print("\n" + "─"*80)
    
    # Con temperatura BAJA (determinista)
    print("\n🔹 CON TEMPERATURA BAJA (0.2) - DETERMINISTA:")
    resultado_bajo = ai_engine.razonar(
        pregunta=pregunta,
        temperatura=0.2,
        usar_instruccion_maestra=True
    )
    print(resultado_bajo.get("respuesta", "Error")[:300] + "...")
    
    # Con temperatura MEDIA (más flexible)
    print("\n\n🔹 CON TEMPERATURA MEDIA (0.5) - MAS FLEXIBLE:")
    resultado_medio = ai_engine.razonar(
        pregunta=pregunta,
        temperatura=0.5,
        usar_instruccion_maestra=True
    )
    print(resultado_medio.get("respuesta", "Error")[:300] + "...")
    
    print("\n" + "─"*80)
    print("✅ Observación: Temperatura baja = Respuestas más consistentes")


def ejemplo_5_modo_profesional_vs_estandar():
    """Ejemplo 5: Comparar modo profesional vs estándar"""
    print("\n" + "="*80)
    print("EJEMPLO 5: MODO PROFESIONAL vs MODO ESTÁNDAR")
    print("="*80)
    
    ai_engine = AIEngine()
    pregunta = "¿Debería comprar AAPL a $228?"
    
    print("\nPregunta:", pregunta)
    
    # MODO PROFESIONAL (con instrucción maestra)
    print("\n🔹 MODO PROFESIONAL (Instrucción Maestra):")
    resultado_prof = ai_engine.razonar(
        pregunta=pregunta,
        temperatura=0.2,
        usar_instruccion_maestra=True
    )
    print(resultado_prof.get("respuesta", "Error")[:250] + "...")
    print(f"Modo: {resultado_prof.get('modo')}")
    
    # MODO ESTÁNDAR (sin instrucción maestra)
    print("\n🔹 MODO ESTÁNDAR (Sin Instrucción Maestra):")
    resultado_std = ai_engine.razonar(
        pregunta=pregunta,
        temperatura=0.7,
        usar_instruccion_maestra=False
    )
    print(resultado_std.get("respuesta", "Error")[:250] + "...")
    print(f"Modo: {resultado_std.get('modo')}")
    
    print("\n✅ Diferencia:")
    print("   - Profesional: Determinista, binario, estructurado")
    print("   - Estándar: Más creativo, flexible, conversacional")


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                  EJEMPLOS DE INTEGRACIÓN - GEMINI v2.0                    ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Ejecutar ejemplos
    try:
        # Descomentar los que quieras ejecutar
        
        # ejemplo_1_analisis_profesional()
        ejemplo_2_razonamiento_profesional()
        ejemplo_3_integracion_bot_telegram()
        # ejemplo_4_comparacion_temperaturas()
        # ejemplo_5_modo_profesional_vs_estandar()
        
        print("\n" + "="*80)
        print("✅ EJEMPLOS COMPLETADOS")
        print("="*80)
        
    except KeyboardInterrupt:
        print("\n⚠️  Interrumpido por usuario")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
