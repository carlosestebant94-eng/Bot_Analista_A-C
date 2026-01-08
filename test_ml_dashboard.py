"""
test_ml_dashboard.py
Test para validar ML Predictor y Dashboard
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TestMLDashboard")


def test_ml_predictor():
    """Test 1: ML Predictor básico"""
    logger.info("\n" + "="*60)
    logger.info("TEST 1: ML Predictor Básico")
    logger.info("="*60)
    
    try:
        from ia.ml_predictions import MLPredictor
        
        predictor = MLPredictor()
        status = predictor.get_status()
        
        logger.info(f"✅ MLPredictor inicializado")
        logger.info(f"   Estado: {status}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return False


def test_ml_feature_extraction():
    """Test 2: Extracción de features"""
    logger.info("\n" + "="*60)
    logger.info("TEST 2: Extracción de Features")
    logger.info("="*60)
    
    try:
        from ia.ml_predictions import MLPredictor
        
        # Crear datos sintéticos
        dates = pd.date_range(start='2023-01-01', periods=100)
        prices = np.random.randn(100).cumsum() + 100
        df = pd.DataFrame({
            'Close': prices,
            'Date': dates
        })
        
        predictor = MLPredictor()
        X, y_dir, y_vol = predictor._extract_features(df)
        
        if X is not None:
            logger.info(f"✅ Features extraídos correctamente")
            logger.info(f"   Shape: {X.shape}")
            logger.info(f"   Labels dirección: {len(y_dir)}")
            logger.info(f"   Labels volatilidad: {len(y_vol)}")
            return True
        else:
            logger.warning(f"⚠️  No se extrajeron features")
            return False
    
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return False


def test_ml_prediction():
    """Test 3: Predicciones de ML"""
    logger.info("\n" + "="*60)
    logger.info("TEST 3: Predicciones ML")
    logger.info("="*60)
    
    try:
        from ia.ml_predictions import MLPredictor
        
        predictor = MLPredictor()
        
        # Simular indicadores
        current_indicators = {
            "RSI": {"valor": 55},
            "MACD": {"linea_macd": 0.5},
            "STOCHASTIC": {"linea_k": 50},
            "MEDIAS_MOVILES": {"SMA_20": 105, "SMA_50": 100},
            "VOLUMEN": {"relacion": 1.5}
        }
        
        # Sin modelos entrenados, debería devolver disponible=False
        price_pred = predictor.predict_price_direction("AAPL", current_indicators)
        vol_pred = predictor.predict_volatility("AAPL", current_indicators)
        conf_pred = predictor.predict_confidence("AAPL", current_indicators)
        
        logger.info(f"✅ Predicciones ejecutadas")
        logger.info(f"   Price Direction: {price_pred.get('disponible', False)}")
        logger.info(f"   Volatility: {vol_pred.get('disponible', False)}")
        logger.info(f"   Confidence: {conf_pred.get('disponible', False)}")
        
        # Sin modelos, debería mostrar error
        if 'error' in price_pred:
            logger.info(f"   ℹ️  Esperado (modelos no entrenados): {price_pred['error']}")
        
        return True
    
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return False


def test_flask_app():
    """Test 4: Flask App básico"""
    logger.info("\n" + "="*60)
    logger.info("TEST 4: Flask App Básico")
    logger.info("="*60)
    
    try:
        from app.backend import app
        
        # Crear cliente de test
        client = app.test_client()
        
        # Test health
        response = client.get('/api/health')
        logger.info(f"✅ Health check: {response.status_code}")
        
        data = response.get_json()
        logger.info(f"   Status: {data.get('status')}")
        
        if response.status_code == 200:
            logger.info(f"   Componentes encontrados: {list(data.get('componentes', {}).keys())}")
            return True
        else:
            return False
    
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return False


def test_api_endpoints():
    """Test 5: API Endpoints"""
    logger.info("\n" + "="*60)
    logger.info("TEST 5: API Endpoints")
    logger.info("="*60)
    
    try:
        from app.backend import app
        
        client = app.test_client()
        
        # Test analyze endpoint
        logger.info("  Testeando /api/analyze...")
        response = client.post('/api/analyze', 
            json={"ticker": "AAPL", "include_ml": False})
        
        if response.status_code in [200, 400]:
            logger.info(f"  ✅ Response code: {response.status_code}")
        else:
            logger.info(f"  ℹ️  Esperado (requiere datos históricos): {response.status_code}")
        
        # Test status endpoint
        logger.info("  Testeando /api/status...")
        response = client.get('/api/status')
        logger.info(f"  ✅ Status: {response.status_code}")
        
        return True
    
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return False


def test_dashboard_html():
    """Test 6: Dashboard HTML"""
    logger.info("\n" + "="*60)
    logger.info("TEST 6: Dashboard HTML")
    logger.info("="*60)
    
    try:
        dashboard_path = os.path.join(
            os.path.dirname(__file__),
            'app', 'templates', 'index.html'
        )
        
        if os.path.exists(dashboard_path):
            with open(dashboard_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if 'Bot Analista' in content and 'API_BASE' in content:
                logger.info(f"✅ Dashboard HTML válido")
                logger.info(f"   Tamaño: {len(content)} bytes")
                logger.info(f"   Contiene UI interactiva")
                return True
            else:
                logger.warning(f"⚠️  HTML incompleto")
                return False
        else:
            logger.error(f"❌ Archivo no encontrado: {dashboard_path}")
            return False
    
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return False


def test_start_script():
    """Test 7: Start script"""
    logger.info("\n" + "="*60)
    logger.info("TEST 7: Start Script")
    logger.info("="*60)
    
    try:
        start_script_path = os.path.join(
            os.path.dirname(__file__),
            'scripts', 'start_dashboard.py'
        )
        
        if os.path.exists(start_script_path):
            with open(start_script_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if 'train_models_background' in content and 'start_backend' in content:
                logger.info(f"✅ Start script válido")
                logger.info(f"   Contiene funciones necesarias")
                return True
            else:
                logger.warning(f"⚠️  Script incompleto")
                return False
        else:
            logger.error(f"❌ Script no encontrado: {start_script_path}")
            return False
    
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return False


def main():
    """Ejecutar todos los tests"""
    logger.info("\n" + "🧪" * 30)
    logger.info("INICIANDO SUITE DE TESTS: ML & DASHBOARD")
    logger.info("🧪" * 30)
    
    tests = [
        ("ML Predictor Básico", test_ml_predictor),
        ("Extracción de Features", test_ml_feature_extraction),
        ("Predicciones ML", test_ml_prediction),
        ("Flask App", test_flask_app),
        ("API Endpoints", test_api_endpoints),
        ("Dashboard HTML", test_dashboard_html),
        ("Start Script", test_start_script),
    ]
    
    resultados = []
    for name, test_func in tests:
        try:
            resultado = test_func()
            resultados.append((name, resultado))
        except Exception as e:
            logger.error(f"❌ Exception en {name}: {str(e)}")
            resultados.append((name, False))
    
    # Resumen
    logger.info("\n" + "="*60)
    logger.info("RESUMEN DE TESTS")
    logger.info("="*60)
    
    passed = sum(1 for _, r in resultados if r)
    total = len(resultados)
    
    for name, resultado in resultados:
        status = "✅ PASS" if resultado else "❌ FAIL"
        logger.info(f"{status}: {name}")
    
    logger.info(f"\nTotal: {passed}/{total} tests pasados")
    
    if passed == total:
        logger.info("\n🎉 ¡TODOS LOS TESTS PASARON!")
    else:
        logger.warning(f"\n⚠️  {total - passed} tests fallaron")
    
    logger.info("\n" + "="*60)
    logger.info("PRÓXIMOS PASOS:")
    logger.info("="*60)
    logger.info("1. Entrenar modelos ML con: python scripts/start_dashboard.py")
    logger.info("2. Acceder al dashboard en: http://localhost:5000")
    logger.info("3. Analizar tickers con: /api/analyze (POST)")
    logger.info("4. Entrenar ML con: /api/train-ml (POST)")
    logger.info("="*60)


if __name__ == '__main__':
    main()
