"""
test_enhanced_features.py
Script de prueba para validar las nuevas características mejoradas
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from analisis.enhanced_analyzer import EnhancedAnalyzer
from data_sources import MacroeconomicDataManager, FundamentalAnalyzer
from analisis import CorrelationAnalyzer, MLPredictor

def test_macroeconomic_data():
    """Prueba el módulo macroeconómico"""
    print("\n" + "="*60)
    print("🌍 PRUEBA: Datos Macroeconómicos")
    print("="*60)
    
    try:
        macro = MacroeconomicDataManager()
        print("✅ MacroeconomicDataManager inicializado")
        
        # Obtener contexto
        contexto = macro.obtener_contexto_macro_resumido()
        print("\n📊 Contexto Macroeconómico:")
        print(f"  • Tasas de Interés: {contexto.get('tasas_interes', {})}")
        print(f"  • Desempleo: {contexto.get('desempleo', 'N/A')}")
        print(f"  • Inflación: {contexto.get('inflacion', 'N/A')}")
        print(f"  • Sentimiento Consumidor: {contexto.get('sentimiento_consumidor', 'N/A')}")
        print(f"  • Precio Petróleo: ${contexto.get('precio_petroleo', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_fundamental_analyzer():
    """Prueba el analizador fundamental"""
    print("\n" + "="*60)
    print("💰 PRUEBA: Análisis Fundamental")
    print("="*60)
    
    try:
        fundamental = FundamentalAnalyzer()
        print("✅ FundamentalAnalyzer inicializado")
        
        # Probar con AAPL
        print("\n📱 Analizando AAPL...")
        info = fundamental.obtener_info_fundamental("AAPL")
        
        if 'error' not in info:
            print(f"  • Empresa: {info.get('empresa', {}).get('nombre', 'N/A')}")
            print(f"  • P/E Ratio: {info.get('valuacion', {}).get('pe_ratio', 'N/A')}")
            print(f"  • ROE: {info.get('rentabilidad', {}).get('roe', 'N/A')}")
            print(f"  • Market Cap: ${info.get('valuacion', {}).get('capitalizacion', 'N/A')}")
            return True
        else:
            print(f"  ⚠️  Error: {info.get('error', 'Unknown')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_correlation_analyzer():
    """Prueba el analizador de correlaciones"""
    print("\n" + "="*60)
    print("📊 PRUEBA: Análisis de Correlaciones")
    print("="*60)
    
    try:
        corr = CorrelationAnalyzer()
        print("✅ CorrelationAnalyzer inicializado")
        
        # Calcular correlación
        print("\n🔗 Calculando correlaciones entre AAPL, MSFT, GOOGL...")
        tickers = ['AAPL', 'MSFT', 'GOOGL']
        resultado = corr.calcular_correlacion_activos(tickers, periodo='6mo')
        
        if 'error' not in resultado:
            print(f"  • Correlación promedio: {resultado.get('pares_altamente_correlacionados', [])}")
            print(f"  • Pares alt. correlacionados: {len(resultado.get('pares_altamente_correlacionados', []))}")
            return True
        else:
            print(f"  ⚠️  Error: {resultado.get('error', 'Unknown')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ml_predictor():
    """Prueba el predictor ML"""
    print("\n" + "="*60)
    print("🤖 PRUEBA: Predicción con ML")
    print("="*60)
    
    try:
        ml = MLPredictor()
        print("✅ MLPredictor inicializado")
        
        # Predicción
        print("\n🔮 Prediciendo precio de AAPL (30 días)...")
        prediccion = ml.predecir_precio("AAPL", dias_futuros=30)
        
        if 'error' not in prediccion:
            print(f"  • Precio Actual: ${prediccion.get('precio_actual', 'N/A'):.2f}")
            print(f"  • Predicción: ${prediccion.get('predicciones', {}).get('ensemble', 'N/A'):.2f}")
            print(f"  • Confianza: {prediccion.get('confianza_ensemble', 'N/A')}%")
            print(f"  • Tendencia: {prediccion.get('tendencia', 'N/A')}")
            return True
        else:
            print(f"  ⚠️  Error: {prediccion.get('error', 'Unknown')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_enhanced_analyzer():
    """Prueba el analizador mejorado integrado"""
    print("\n" + "="*60)
    print("🚀 PRUEBA: Enhanced Analyzer (Integración Completa)")
    print("="*60)
    
    try:
        analyzer = EnhancedAnalyzer()
        print("✅ EnhancedAnalyzer inicializado")
        
        print("\n🔍 Ejecutando análisis 360 de AAPL...")
        print("   (Esto puede tomar 1-2 minutos)...\n")
        
        analisis = analyzer.analizar_360("AAPL")
        
        if 'error' not in analisis:
            print("  ✅ Análisis 360 completado")
            print(f"  • Timestamp: {analisis.get('timestamp', 'N/A')}")
            print(f"  • Recomendación: {analisis.get('recomendacion', 'N/A')}")
            
            print("\n📋 Módulos ejecutados:")
            analisis_dict = analisis.get('analisis', {})
            modulos = list(analisis_dict.keys())
            for modulo in modulos:
                print(f"     ✓ {modulo.upper()}")
            
            return True
        else:
            print(f"  ⚠️  Error: {analisis.get('error', 'Unknown')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "="*60)
    print("🧪 SUITE DE PRUEBAS - MEJORAS DEL PROYECTO")
    print("="*60)
    
    results = {
        'Datos Macroeconómicos': test_macroeconomic_data(),
        'Análisis Fundamental': test_fundamental_analyzer(),
        'Correlaciones': test_correlation_analyzer(),
        'Predicción ML': test_ml_predictor(),
        'Enhanced Analyzer': test_enhanced_analyzer()
    }
    
    print("\n" + "="*60)
    print("📊 RESUMEN DE RESULTADOS")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<30} {status}")
    
    print(f"\nTotal: {passed}/{total} pruebas pasadas")
    
    if passed == total:
        print("\n🎉 ¡TODAS LAS MEJORAS FUNCIONAN CORRECTAMENTE!")
    else:
        print(f"\n⚠️  {total - passed} prueba(s) fallaron - Revisar logs")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
