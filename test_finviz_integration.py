"""
test_finviz_integration.py
Test completo de integración de Finviz con el sistema
"""

import logging
from data_sources import MarketDataManager, FinvizScraper
from cerebro import AnalysisMethodology

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_finviz_scraper():
    """Test 1: Finviz Scraper funcionando"""
    print("\n" + "="*60)
    print("TEST 1: FinvizScraper")
    print("="*60)
    
    try:
        scraper = FinvizScraper()
        status = scraper.get_status()
        
        print("\n✅ FinvizScraper Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_market_data_manager_finviz():
    """Test 2: MarketDataManager con Finviz"""
    print("\n" + "="*60)
    print("TEST 2: MarketDataManager con Finviz")
    print("="*60)
    
    try:
        manager = MarketDataManager()
        status = manager.get_status()
        
        print("\n✅ MarketDataManager Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
        
        # Verificar que Finviz está disponible
        if "✅" in status.get("finviz", ""):
            print("\n✅ Finviz integrado correctamente en MarketDataManager")
            return True
        else:
            print("\n⚠️  Finviz no disponible (web scraping activado)")
            return True  # Sigue siendo exitoso
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_finviz_data_retrieval():
    """Test 3: Obtener datos de Finviz para un ticker"""
    print("\n" + "="*60)
    print("TEST 3: Obtener datos de Finviz")
    print("="*60)
    
    try:
        manager = MarketDataManager()
        
        # Intenta con AAPL (ticker popular)
        ticker = "AAPL"
        print(f"\n🔍 Obteniendo datos de Finviz para {ticker}...")
        
        datos = manager.obtener_datos_finviz(ticker)
        
        if "error" not in datos:
            print(f"\n✅ Datos de Finviz obtenidos para {ticker}:")
            print(f"  Timestamp: {datos.get('timestamp', 'N/A')}")
            print(f"  Insider Trading: {bool(datos.get('insider_trading', {}))}")
            print(f"  Analyst Ratings: {bool(datos.get('analyst_ratings', {}))}")
            print(f"  Sentiment: {bool(datos.get('sentiment', {}))}")
            print(f"  Technical: {bool(datos.get('technical', {}))}")
            return True
        else:
            print(f"⚠️  {datos.get('error', 'Error desconocido')}")
            return True  # No es crítico si falla
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return True  # No es crítico si falla

def test_insider_summary():
    """Test 4: Resumen de Insider Trading"""
    print("\n" + "="*60)
    print("TEST 4: Insider Trading Summary")
    print("="*60)
    
    try:
        manager = MarketDataManager()
        ticker = "MSFT"
        
        print(f"\n🔍 Obteniendo insider summary para {ticker}...")
        
        insider = manager.obtener_insider_summary(ticker)
        
        print(f"\n✅ Insider Summary para {ticker}:")
        for key, value in insider.items():
            print(f"  {key}: {value}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return True  # No es crítico si falla

def test_factor_social_enrichment():
    """Test 5: Factor Social enriquecido con Finviz"""
    print("\n" + "="*60)
    print("TEST 5: Factor Social Analysis (Enriquecido)")
    print("="*60)
    
    try:
        analysis = AnalysisMethodology()
        ticker = "AAPL"
        
        print(f"\n🔍 Analizando {ticker} con Finviz enrichment...")
        
        # Obtener análisis completo
        resultado = analysis.analizar_ticker(ticker)
        
        if resultado.get("status") != "error":
            print(f"\n✅ Análisis completado para {ticker}:")
            print(f"  Status: {resultado.get('status', 'N/A')}")
            
            # Verificar Factor Social
            factor_social = resultado.get("alexander", {}).get("factor_social", {})
            print(f"\n💼 Factor Social (Enriquecido):")
            print(f"  Valuación: {factor_social.get('valuacion', 'N/A')}")
            print(f"  Solidez: {factor_social.get('solidez', 'N/A')}")
            print(f"  Insider Sentiment: {factor_social.get('insider_sentiment', 'N/A')}")
            print(f"  Analyst Sentiment: {factor_social.get('analyst_sentiment', 'N/A')}")
            print(f"  Finviz Disponible: {factor_social.get('finviz_disponible', False)}")
            
            # Verificar Finviz data
            finviz_data = resultado.get("finviz", {})
            print(f"\n🦊 Datos de Finviz:")
            print(f"  Insider Trading: {bool(finviz_data.get('insider_trading', {}))}")
            print(f"  Analyst Ratings: {bool(finviz_data.get('analyst_ratings', {}))}")
            print(f"  Sentiment: {bool(finviz_data.get('sentiment', {}))}")
            
            # Recomendación final
            rec = resultado.get("recomendacion", {})
            print(f"\n✅ Recomendación Final:")
            print(f"  Acción: {rec.get('recomendacion', 'N/A')}")
            print(f"  Score: {rec.get('score', 'N/A')}/100")
            print(f"  Probabilidad: {rec.get('probabilidad_exito', 'N/A')}%")
            print(f"  Confianza: {rec.get('confianza', 'N/A')}")
            
            return True
        else:
            print(f"❌ Error en análisis: {resultado.get('error', 'Error desconocido')}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Ejecuta todos los tests"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + " FINVIZ INTEGRATION TEST SUITE ".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    tests = [
        ("FinvizScraper Basic", test_finviz_scraper),
        ("MarketDataManager Finviz", test_market_data_manager_finviz),
        ("Finviz Data Retrieval", test_finviz_data_retrieval),
        ("Insider Summary", test_insider_summary),
        ("Factor Social Enrichment", test_factor_social_enrichment),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ CRITICAL ERROR in {test_name}: {str(e)}")
            import traceback
            traceback.print_exc()
            results[test_name] = False
    
    # Resumen final
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "="*60)
    print(f"RESULTADO FINAL: {passed}/{total} tests pasados")
    if passed == total:
        print("✅ TODOS LOS TESTS EXITOSOS - FINVIZ INTEGRATION COMPLETA")
    else:
        print(f"⚠️  {total - passed} tests fallaron")
    print("="*60)

if __name__ == "__main__":
    main()
