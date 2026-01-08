"""
demo_finviz_enrichment.py
Demostración de análisis enriquecido con datos de Finviz
"""

import sys
import os

# Configurar encoding UTF-8 para Windows
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from data_sources import MarketDataManager
from cerebro import AnalysisMethodology
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def print_separator(title):
    print("\n" + "="*70)
    print(f" {title}".center(70))
    print("="*70 + "\n")

def demo_análisis_enriquecido():
    """Demostración de análisis con Finviz enrichment"""
    
    print_separator("DEMO: ANÁLISIS 360° CON FINVIZ ENRICHMENT")
    
    tickers = ["AAPL", "MSFT", "GOOGL"]
    
    for ticker in tickers:
        print(f"\n{'-'*70}")
        print(f"ANALIZANDO: {ticker}")
        print(f"{'-'*70}\n")
        
        analysis = AnalysisMethodology()
        resultado = analysis.analizar_ticker(ticker)
        
        if resultado.get("status") == "error":
            print(f"❌ Error: {resultado.get('error')}")
            continue
        
        # Datos actuales
        datos = resultado.get("datos_actuales", {})
        print(f"💰 Precio Actual: ${datos.get('precio_actual', 'N/A')}")
        print(f"   Cambio: {datos.get('cambio_pct', 'N/A')}%")
        print(f"   Volumen: {datos.get('volumen', 'N/A'):,}")
        
        # Análisis Alexander
        alexander = resultado.get("alexander", {})
        factor_social = alexander.get("factor_social", {})
        
        print(f"\n📈 Factor Social (Base):")
        print(f"   Valuación: {factor_social.get('valuacion', 'N/A')}")
        print(f"   Tamaño: {factor_social.get('tamaño', 'N/A')}")
        print(f"   Solidez: {factor_social.get('solidez', 'N/A')}")
        print(f"   P/E Ratio: {factor_social.get('pe_ratio', 'N/A')}")
        
        # NUEVA: Enriquecimiento con Finviz
        print(f"\n🦊 Factor Social (Enriquecido con Finviz):")
        print(f"   Insider Sentiment: {factor_social.get('insider_sentiment', 'N/A')}")
        print(f"   Analyst Sentiment: {factor_social.get('analyst_sentiment', 'N/A')}")
        print(f"   Sentimiento General: {factor_social.get('sentimiento_general', 'N/A')}")
        print(f"   Finviz Disponible: {'✅ Sí' if factor_social.get('finviz_disponible') else '❌ No'}")
        
        # Datos crudos de Finviz
        finviz_data = resultado.get("finviz", {})
        if finviz_data and not finviz_data.get("error"):
            insider = finviz_data.get("insider_trading", {})
            analyst = finviz_data.get("analyst_ratings", {})
            
            if insider:
                print(f"\n📋 Insider Trading Data:")
                for key, value in list(insider.items())[:3]:
                    print(f"   {key}: {value}")
            
            if analyst:
                print(f"\n⭐ Analyst Ratings Data:")
                for key, value in list(analyst.items())[:3]:
                    print(f"   {key}: {value}")
        
        # Indicadores técnicos
        tecnico = resultado.get("tecnico", {})
        indicadores = tecnico.get("indicadores", {})
        
        print(f"\n📊 Indicadores Técnicos:")
        if "RSI" in indicadores:
            rsi = indicadores["RSI"]
            print(f"   RSI(14): {rsi.get('valor', 'N/A')} → {rsi.get('señal', 'N/A')}")
        if "MACD" in indicadores:
            macd = indicadores["MACD"]
            print(f"   MACD: {macd.get('señal', 'N/A')}")
        if "STOCHASTIC" in indicadores:
            stoch = indicadores["STOCHASTIC"]
            print(f"   Stochastic: {stoch.get('señal', 'N/A')}")
        
        # Alexander scores
        marea = alexander.get("marea", {})
        movimiento = alexander.get("movimiento", {})
        
        print(f"\n🧭 Alexander Methodology:")
        print(f"   Marea: {marea.get('marea_general', 'N/A')} (VIX: {marea.get('vix', 'N/A')})")
        print(f"   Movimiento: {movimiento.get('movimiento', 'N/A')} ({movimiento.get('consenso', 'N/A')}%)")
        print(f"   Factor Social: {factor_social.get('sentimiento_general', 'N/A')}")
        
        # Recomendación final
        rec = resultado.get("recomendacion", {})
        score = rec.get("score", 0)
        
        # Barra de progreso
        barra_length = 30
        filled = int(barra_length * score / 100)
        bar = "|" + ("=" * filled) + ("-" * (barra_length - filled)) + "|"
        
        print(f"\nRECOMENDACION FINAL:")
        print(f"   Accion: {rec.get('recomendacion', 'N/A')}")
        print(f"   Score: {bar} {score}/100")
        print(f"   Probabilidad de exito: {rec.get('probabilidad_exito', 'N/A')}%")
        print(f"   Confianza: {rec.get('confianza', 'N/A')}")
        
        # Soportes y Resistencias
        sr = resultado.get("soportes_resistencias", {})
        print(f"\nSoportes y Resistencias (Pivot Points):")
        print(f"   R2: ${sr.get('resistencia_2', 'N/A')}")
        print(f"   R1: ${sr.get('resistencia_1', 'N/A')}")
        print(f"   Pivot: ${sr.get('pivot', 'N/A')}")
        print(f"   S1: ${sr.get('soporte_1', 'N/A')}")
        print(f"   S2: ${sr.get('soporte_2', 'N/A')}")

def print_summary():
    """Resumen de la integración"""
    
    print_separator("RESUMEN DE INTEGRACIÓN FINVIZ")
    
    print("""
✅ FINVIZ INTEGRATION COMPLETADA

📦 Módulos Implementados:
   1. FinvizScraper (data_sources/finviz_scraper.py)
      └─ Web scraping de Finviz.com
      └─ Insider trading data
      └─ Analyst ratings
      └─ Sentiment scores
   
   2. MarketDataManager Enhancement
      └─ obtener_datos_finviz(ticker)
      └─ obtener_insider_summary(ticker)
      └─ Integración automática
   
   3. AlexanderAnalyzer Enhancement
      └─ analizar_factor_social() enriquecido
      └─ Insider sentiment integration
      └─ Analyst rating integration
   
   4. TelegramBot Enhancement
      └─ Visualización de datos Finviz
      └─ Insider trading en reportes
      └─ Analyst ratings en recomendaciones

🔄 Flujo de Datos:
   AAPL → YFinance (precio, histórico, fundamentos)
        → Finviz (insider, analyst, sentiment)
        → AlexanderAnalyzer (análisis + scoring)
        → Recomendación final enriquecida

📊 Factor Social Mejorado:
   Antes: Valuación + Tamaño + Solidez
   Ahora: + Insider Sentiment + Analyst Ratings + Sentiment Score

🎯 Casos de Uso:
   • Detectar movimientos de insiders (ALCISTA vs BAJISTA)
   • Integrar ratings de analistas en recomendaciones
   • Mejorar confianza del Factor Social
   • Análisis más holístico y robusto

⚙️ Configuración:
   • Web scraping como método principal
   • Fallback automático si falla
   • Rate limiting integrado (1 seg entre requests)
   • Logging detallado de operaciones

📈 Próximos Pasos Opcionales:
   1. Implementar Polygon.io para datos premium
   2. Agregar machine learning para predicciones
   3. Crear alertas basadas en insider activity
   4. Dashboard web con gráficos enriquecidos
    """)
    
    print("="*70 + "\n")

if __name__ == "__main__":
    demo_análisis_enriquecido()
    print_summary()
