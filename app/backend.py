"""
app/backend.py
API Backend para Dashboard
Proporciona endpoints REST para análisis en tiempo real
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, Any
import json
import threading

# Agregar ruta al módulo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_sources import MarketDataManager
from cerebro import AnalysisMethodology
from ia.ml_predictions import MLPredictor
from config import settings

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DashboardBackend")

# Crear app Flask
app = Flask(__name__)
CORS(app)

# Inicializar componentes
market_data = MarketDataManager()
analysis_methodology = AnalysisMethodology()
ml_predictor = MLPredictor()

# Almacenamiento temporal de análisis
analysis_cache = {}
max_cache_size = 100


# ============ RUTAS API ============

@app.route('/api/health', methods=['GET'])
def health():
    """Health check del servidor"""
    return jsonify({
        "status": "✅ Backend activo",
        "timestamp": datetime.now().isoformat(),
        "modulos": {
            "market_data": "✅ Operativo",
            "analysis": "✅ Operativo",
            "ml_predictor": ml_predictor.get_status()
        }
    })


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Endpoint para analizar un ticker
    POST /api/analyze
    {
        "ticker": "AAPL",
        "include_ml": true,
        "include_finviz": true
    }
    """
    try:
        data = request.get_json()
        ticker = data.get('ticker', '').upper()
        include_ml = data.get('include_ml', True)
        include_finviz = data.get('include_finviz', True)
        
        if not ticker:
            return jsonify({"error": "Falta ticker"}), 400
        
        logger.info(f"📊 Analizando {ticker}...")
        
        # Análisis básico
        resultado = analysis_methodology.analizar_ticker(ticker)
        
        if "error" in resultado:
            return jsonify(resultado), 400
        
        # Agregar predicciones de ML
        if include_ml:
            logger.info(f"🤖 Agregando predicciones ML para {ticker}...")
            
            # Obtener indicadores actuales
            current_indicators = resultado.get("indicadores_tecnicos", {})
            
            # Predicciones
            price_pred = ml_predictor.predict_price_direction(ticker, current_indicators)
            vol_pred = ml_predictor.predict_volatility(ticker, current_indicators)
            conf_pred = ml_predictor.predict_confidence(ticker, current_indicators)
            
            resultado["ml_predictions"] = {
                "precio": price_pred,
                "volatilidad": vol_pred,
                "confianza": conf_pred
            }
        
        # Guardar en caché
        _add_to_cache(ticker, resultado)
        
        # Convertir a serializable
        resultado_serializable = _make_serializable(resultado)
        
        return jsonify({
            "status": "✅ Análisis completado",
            "ticker": ticker,
            "timestamp": datetime.now().isoformat(),
            "analisis": resultado_serializable
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error en análisis: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/analyze/batch', methods=['POST'])
def analyze_batch():
    """
    Analiza múltiples tickers
    POST /api/analyze/batch
    {
        "tickers": ["AAPL", "MSFT", "GOOGL"],
        "include_ml": true
    }
    """
    try:
        data = request.get_json()
        tickers = data.get('tickers', [])
        include_ml = data.get('include_ml', True)
        
        if not tickers:
            return jsonify({"error": "Falta lista de tickers"}), 400
        
        logger.info(f"📊 Analizando batch de {len(tickers)} tickers...")
        
        resultados = {}
        for ticker in tickers:
            try:
                resultado = analysis_methodology.analizar_ticker(ticker.upper())
                
                if include_ml and "error" not in resultado:
                    current_indicators = resultado.get("indicadores_tecnicos", {})
                    price_pred = ml_predictor.predict_price_direction(ticker, current_indicators)
                    resultado["ml_predictions"] = {
                        "precio": price_pred
                    }
                
                resultados[ticker.upper()] = resultado
                _add_to_cache(ticker.upper(), resultado)
                
            except Exception as e:
                logger.error(f"Error analizando {ticker}: {str(e)}")
                resultados[ticker.upper()] = {"error": str(e)}
        
        return jsonify({
            "status": "✅ Batch completado",
            "tickers_procesados": len(resultados),
            "timestamp": datetime.now().isoformat(),
            "resultados": _make_serializable(resultados)
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error en batch: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """Obtiene histórico de análisis guardados"""
    try:
        ticker = request.args.get('ticker', '').upper()
        limit = int(request.args.get('limit', 10))
        
        if not ticker:
            return jsonify({"error": "Falta ticker"}), 400
        
        history = analysis_cache.get(ticker, [])[-limit:]
        
        return jsonify({
            "status": "✅ Histórico obtenido",
            "ticker": ticker,
            "total_registros": len(history),
            "registros": _make_serializable(history)
        }), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo histórico: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/status', methods=['GET'])
def get_status():
    """Obtiene estado del sistema"""
    try:
        return jsonify({
            "status": "✅ Sistema operativo",
            "timestamp": datetime.now().isoformat(),
            "componentes": {
                "market_data": market_data.get_status(),
                "analysis": {
                    "modulo": "AnalysisMethodology",
                    "estado": "✅ Operativo"
                },
                "ml_predictor": ml_predictor.get_status()
            },
            "cache": {
                "tickers_analizados": len(analysis_cache),
                "total_analisis": sum(len(v) for v in analysis_cache.values())
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo estado: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/train-ml', methods=['POST'])
def train_ml():
    """Entrena los modelos de ML con datos históricos"""
    try:
        data = request.get_json()
        tickers = data.get('tickers', ['AAPL', 'MSFT', 'GOOGL', 'TSLA'])
        
        logger.info(f"🤖 Entrenando modelos ML con {len(tickers)} tickers...")
        
        # Descargar datos históricos
        historical_data = {}
        for ticker in tickers:
            try:
                logger.info(f"  📥 Descargando datos para {ticker}...")
                df = market_data.obtener_datos_historicos(ticker, dias=252)  # 1 año
                if df is not None and len(df) > 0:
                    historical_data[ticker] = df
            except Exception as e:
                logger.warning(f"  ⚠️  Error descargando {ticker}: {str(e)}")
        
        if not historical_data:
            return jsonify({"error": "No se pudieron descargar datos históricos"}), 400
        
        # Entrenar modelos
        resultado_entrenamiento = ml_predictor.train_models(historical_data)
        
        return jsonify({
            "status": "✅ Entrenamiento completado",
            "timestamp": datetime.now().isoformat(),
            "resultado": resultado_entrenamiento
        }), 200
        
    except Exception as e:
        logger.error(f"Error entrenando modelos: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/compare', methods=['POST'])
def compare_tickers():
    """
    Compara múltiples tickers
    POST /api/compare
    {
        "tickers": ["AAPL", "MSFT", "GOOGL"]
    }
    """
    try:
        data = request.get_json()
        tickers = data.get('tickers', [])
        
        if not tickers or len(tickers) < 2:
            return jsonify({"error": "Se necesitan al menos 2 tickers"}), 400
        
        logger.info(f"📊 Comparando {len(tickers)} tickers...")
        
        resultados = []
        for ticker in tickers:
            try:
                # Obtener datos actuales
                precio = market_data.obtener_precio_actual(ticker)
                cambio = market_data.obtener_cambio_diario(ticker)
                
                # Análisis
                analisis = analysis_methodology.analizar_ticker(ticker)
                
                resultados.append({
                    "ticker": ticker,
                    "precio": precio,
                    "cambio": cambio,
                    "recomendacion": analisis.get("recomendacion", "ESPERA"),
                    "score": analisis.get("score", 0),
                    "factor_tecnico": analisis.get("factor_tecnico", "NEUTRAL")
                })
                
            except Exception as e:
                logger.warning(f"Error comparando {ticker}: {str(e)}")
        
        # Ordenar por score
        resultados.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        return jsonify({
            "status": "✅ Comparación completada",
            "timestamp": datetime.now().isoformat(),
            "tickers_comparados": len(resultados),
            "resultados": resultados
        }), 200
        
    except Exception as e:
        logger.error(f"Error comparando: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ============ FUNCIONES AUXILIARES ============

def _add_to_cache(ticker: str, analisis: Dict):
    """Agrega análisis al caché"""
    if ticker not in analysis_cache:
        analysis_cache[ticker] = []
    
    # Limitar tamaño del caché
    if len(analysis_cache) > max_cache_size:
        oldest_ticker = next(iter(analysis_cache))
        del analysis_cache[oldest_ticker]
    
    # Agregar con timestamp
    analisis_con_timestamp = analisis.copy()
    analisis_con_timestamp['timestamp'] = datetime.now().isoformat()
    analysis_cache[ticker].append(analisis_con_timestamp)
    
    # Mantener últimos 20 análisis por ticker
    if len(analysis_cache[ticker]) > 20:
        analysis_cache[ticker] = analysis_cache[ticker][-20:]


def _make_serializable(obj: Any) -> Any:
    """Convierte objeto a formato JSON serializable"""
    if isinstance(obj, dict):
        return {k: _make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_make_serializable(item) for item in obj]
    elif isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    else:
        return str(obj)


# ============ MAIN ============

if __name__ == '__main__':
    logger.info("🚀 Iniciando Dashboard Backend...")
    logger.info("📊 Accede a http://localhost:5000")
    logger.info("📖 API docs en http://localhost:5000/api/health")
    
    # Iniciar servidor
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )
