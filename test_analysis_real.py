"""
test_analysis_real.py
Test real con análisis de un ticker
"""

from cerebro.analysis_methodology import AnalysisMethodology
import json

print('='*80)
print('TEST REAL: Análisis de AAPL (Apple Inc)')
print('='*80)
print()

try:
    am = AnalysisMethodology()
    
    print('🔍 Analizando AAPL...')
    resultado = am.analizar_ticker("AAPL")
    
    # Mostrar resumen ejecutivo
    print()
    print('='*80)
    print('RESUMEN EJECUTIVO')
    print('='*80)
    print()
    
    if resultado.get("status") == "completado":
        print(f"✅ Status: {resultado['status']}")
        print()
        
        # Datos actuales
        if "datos_actuales" in resultado:
            da = resultado["datos_actuales"]
            print(f"💰 DATOS ACTUALES:")
            print(f"   Precio: ${da.get('precio_actual', 'N/A')}")
            print(f"   Cambio: {da.get('cambio_pct', 'N/A')}%")
            print(f"   Volumen: {da.get('volumen', 'N/A'):,}")
            print()
        
        # Técnico
        if "tecnico" in resultado:
            tech = resultado["tecnico"]["indicadores"]
            print(f"🔧 INDICADORES TÉCNICOS:")
            rsi = tech.get("RSI", {})
            print(f"   RSI(14): {rsi.get('valor', 'N/A')} → {rsi.get('señal', 'N/A')}")
            macd = tech.get("MACD", {})
            print(f"   MACD: {macd.get('señal', 'N/A')}")
            stoch = tech.get("STOCHASTIC", {})
            print(f"   Stochastic: {stoch.get('señal', 'N/A')}")
            print()
        
        # Alexander
        if "alexander" in resultado:
            alex = resultado["alexander"]
            marea = alex.get("marea", {})
            print(f"🧭 ANÁLISIS ALEXANDER:")
            print(f"   Marea: {marea.get('marea_general', 'N/A')} (VIX: {marea.get('vix', 'N/A')})")
            
            movimiento = alex.get("movimiento", {})
            print(f"   Movimiento: {movimiento.get('movimiento', 'N/A')} ({movimiento.get('fuerza', 'N/A')})")
            
            factor = alex.get("factor_social", {})
            print(f"   Factor Social: {factor.get('sentimiento_general', 'N/A')} (P/E: {factor.get('pe_ratio', 'N/A')})")
            print()
        
        # Recomendación
        if "recomendacion" in resultado:
            rec = resultado["recomendacion"]
            print(f"📊 RECOMENDACIÓN FINAL:")
            print(f"   Acción: {rec.get('recomendacion', 'N/A')}")
            print(f"   Probabilidad: {rec.get('probabilidad_exito', 'N/A')}%")
            print(f"   Confianza: {rec.get('confianza', 'N/A')}")
            print()
        
        # Tendencia
        if "tendencia" in resultado:
            tend = resultado["tendencia"]
            print(f"📈 TENDENCIA:")
            print(f"   Dirección: {tend.get('tendencia', 'N/A')} ({tend.get('cambio_pct', 'N/A')}%)")
            print(f"   Período: {tend.get('periodo_dias', 'N/A')} días")
            print()
        
        # S/R
        if "soportes_resistencias" in resultado:
            sr = resultado["soportes_resistencias"]
            print(f"🎯 SOPORTES / RESISTENCIAS:")
            print(f"   Resistencia 2: ${sr.get('resistencia_2', 'N/A')}")
            print(f"   Resistencia 1: ${sr.get('resistencia_1', 'N/A')}")
            print(f"   Pivot: ${sr.get('pivot', 'N/A')}")
            print(f"   Soporte 1: ${sr.get('soporte_1', 'N/A')}")
            print(f"   Soporte 2: ${sr.get('soporte_2', 'N/A')}")
            print()
        
        print('='*80)
        print('✅ ANÁLISIS COMPLETADO EXITOSAMENTE')
        print('='*80)
        
    else:
        print(f"❌ Error: {resultado.get('error', 'Desconocido')}")
        print(f"Status: {resultado.get('status', 'desconocido')}")

except Exception as e:
    print(f"❌ ERROR EN TEST: {e}")
    import traceback
    traceback.print_exc()
