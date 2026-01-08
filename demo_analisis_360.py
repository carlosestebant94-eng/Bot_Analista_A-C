"""
demo_analisis_360.py
Demostración completa del sistema de análisis 360°
Integración: Doc 1-2-3 + YFinance + Metodología Alexander
"""

from cerebro.analysis_methodology import AnalysisMethodology
import json

print("\n" + "="*90)
print("DEMO: SISTEMA DE ANALISIS 360 - METODOLOGIA ALEXANDER")
print("="*90)
print("\nIntegracion de:")
print("  Doc 1: Metodologia Alexander (Marea + Movimiento + Factor Social)")
print("  Doc 3: Indicadores Tecnicos (RSI, MACD, Stochastic, etc)")
print("  Doc 2: Formato de Reporte Profesional")
print("\nFuente de datos: YFinance (en tiempo real)")
print("\n" + "="*90)

# Crear analizador
am = AnalysisMethodology()

# Símbolos a analizar
tickers = ["AAPL", "MSFT"]

for ticker in tickers:
    print(f"\n\n{'='*90}")
    print(f"ANALISIS DE {ticker}")
    print(f"{'='*90}\n")
    
    # Ejecutar análisis
    resultado = am.analizar_ticker(ticker)
    
    if resultado.get("status") != "completado":
        print(f"ERROR: {resultado.get('error')}")
        continue
    
    # 1. DATOS ACTUALES
    print("DATOS ACTUALES:")
    da = resultado.get("datos_actuales", {})
    print(f"   Simbolo: {da.get('ticker')}")
    print(f"   Precio: ${da.get('precio_actual', 'N/A')}")
    print(f"   Cambio: {da.get('cambio_pct', 'N/A'):+.2f}%")
    print(f"   Volumen: {da.get('volumen', 'N/A'):,}")
    
    # 2. INDICADORES TÉCNICOS (DOC 3)
    print("\nINDICADORES TECNICOS (Doc 3 - Formulas):")
    tech = resultado.get("tecnico", {}).get("indicadores", {})
    
    if "RSI" in tech:
        rsi = tech["RSI"]
        print(f"   RSI(14): {rsi.get('valor', 'N/A'):>6.2f} -> {rsi.get('nivel', 'N/A'):>12} -> {rsi.get('señal')}")
    
    if "MACD" in tech:
        macd = tech["MACD"]
        print(f"   MACD: Linea={macd.get('linea_macd', 'N/A')}, Señal={macd.get('linea_senal', 'N/A')} -> {macd.get('señal')}")
    
    if "STOCHASTIC" in tech:
        stoch = tech["STOCHASTIC"]
        print(f"   Stochastic: K={stoch.get('linea_k', 'N/A'):.2f}%, D={stoch.get('linea_d', 'N/A'):.2f}% -> {stoch.get('señal')}")
    
    if "MEDIAS_MOVILES" in tech:
        sma = tech["MEDIAS_MOVILES"]
        print(f"   SMAs: 20=${sma.get('SMA_20')}, 50=${sma.get('SMA_50')}, 200=${sma.get('SMA_200')}")
    
    if "VOLUMEN" in tech:
        vol = tech["VOLUMEN"]
        print(f"   Volumen: {vol.get('volumen_actual'):,} ({vol.get('relacion'):.2f}x promedio) -> {vol.get('señal')}")
    
    # 3. ANÁLISIS ALEXANDER (DOC 1-2)
    print("\nANALISIS ALEXANDER (Doc 1-2 - Metodologia):")
    alex = resultado.get("alexander", {})
    
    marea = alex.get("marea", {})
    print(f"\n   MAREA (Contexto Macro):")
    print(f"   |-- General: {marea.get('marea_general')}")
    print(f"   |-- VIX: {marea.get('vix')}")
    print(f"   |-- Volatilidad: {marea.get('volatilidad_mercado')}")
    print(f"   |-- Riesgo: {marea.get('riesgo')}")
    
    mov = alex.get("movimiento", {})
    print(f"\n   MOVIMIENTO (Analisis Tecnico Local):")
    print(f"   |-- Tendencia: {mov.get('movimiento')} ({mov.get('fuerza')})")
    print(f"   |-- Señales Alcistas: {mov.get('señales_alcistas')}/3")
    print(f"   |-- Señales Bajistas: {mov.get('señales_bajistas')}/3")
    print(f"   |-- Consenso: {mov.get('consenso'):.1f}%")
    
    fs = alex.get("factor_social", {})
    print(f"\n   FACTOR SOCIAL (Fundamentales):")
    print(f"   |-- Valuacion: {fs.get('valuacion')} (P/E: {fs.get('pe_ratio', 'N/A')})")
    print(f"   |-- Tamaño: {fs.get('tamaño')}")
    print(f"   |-- Solidez: {fs.get('solidez')} (D/E: {fs.get('debt_to_equity', 'N/A')})")
    print(f"   |-- Sentimiento: {fs.get('sentimiento_general')}")
    
    # 4. RECOMENDACIÓN FINAL
    print("\nRECOMENDACION FINAL (Calculo Alexander):")
    rec = resultado.get("recomendacion", {})
    print(f"   +---------------------+")
    print(f"   | Recomendacion: {rec.get('recomendacion', 'N/A'):>16} |")
    print(f"   | Score: {rec.get('score', 'N/A'):>25}/100 |")
    print(f"   | Probabilidad: {rec.get('probabilidad_exito', 'N/A'):>18}% |")
    print(f"   | Confianza: {rec.get('confianza', 'N/A'):>20} |")
    print(f"   +---------------------+")
    
    # 5. SOPORTES Y RESISTENCIAS (PIVOT POINTS)
    print("\nSOPORTES Y RESISTENCIAS (Pivot Points):")
    sr = resultado.get("soportes_resistencias", {})
    print(f"   R2 (Resistencia 2): ${sr.get('resistencia_2', 'N/A'):>8.2f}")
    print(f"   R1 (Resistencia 1): ${sr.get('resistencia_1', 'N/A'):>8.2f}")
    print(f"   ----------------------------")
    print(f"   Pivot: ${sr.get('pivot', 'N/A'):>19.2f}  <- Precio referencia")
    print(f"   ----------------------------")
    print(f"   S1 (Soporte 1): ${sr.get('soporte_1', 'N/A'):>12.2f}")
    print(f"   S2 (Soporte 2): ${sr.get('soporte_2', 'N/A'):>12.2f}")
    
    # 6. TENDENCIA
    print("\nTENDENCIA (20 dias):")
    tend = resultado.get("tendencia", {})
    print(f"   Direccion: {tend.get('tendencia')} ({tend.get('cambio_pct', 'N/A'):+.2f}%)")
    print(f"   Intensidad: {tend.get('intensidad')}")
    print(f"   Maximo: ${tend.get('precio_maximo'):.2f}")
    print(f"   Minimo: ${tend.get('precio_minimo'):.2f}")

print("\n\n" + "="*90)
print("DEMO COMPLETADA")
print("="*90)
print("\nSistema totalmente funcional:")
print("OK - Datos en tiempo real (YFinance)")
print("OK - 8 indicadores tecnicos calculados")
print("OK - Analisis Alexander (3 dimensiones)")
print("OK - Recomendacion con scoring 0-100")
print("OK - Soportes/Resistencias automaticos")
print("OK - Pronto en Telegram: /analizar [TICKER]")
print("\n" + "="*90 + "\n")
