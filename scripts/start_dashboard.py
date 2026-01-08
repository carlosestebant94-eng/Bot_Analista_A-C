"""
scripts/start_dashboard.py
Script para iniciar el dashboard y entrenar modelos de ML
"""

import sys
import os
import logging
from pathlib import Path

# Agregar ruta al módulo
sys.path.insert(0, str(Path(__file__).parent.parent))

from ia.ml_predictions import MLPredictor
from data_sources import MarketDataManager
import threading
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("StartDashboard")


def train_models_background():
    """Entrena modelos en background"""
    logger.info("🤖 Iniciando entrenamiento de modelos en background...")
    
    try:
        ml_predictor = MLPredictor()
        market_data = MarketDataManager()
        
        # Descargar datos históricos
        logger.info("📥 Descargando datos históricos...")
        historical_data = {}
        
        tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN']
        for ticker in tickers:
            try:
                logger.info(f"  Descargando {ticker}...")
                df = market_data.obtener_datos_historicos(ticker, dias=252)
                if df is not None and len(df) > 0:
                    historical_data[ticker] = df
                    logger.info(f"  ✅ {ticker}: {len(df)} registros")
            except Exception as e:
                logger.warning(f"  ⚠️  Error con {ticker}: {str(e)}")
        
        if historical_data:
            # Entrenar modelos
            resultado = ml_predictor.train_models(historical_data)
            logger.info(f"✅ Entrenamiento completado: {resultado}")
        else:
            logger.warning("⚠️  No se pudieron descargar datos históricos")
    
    except Exception as e:
        logger.error(f"❌ Error en entrenamiento: {str(e)}")


def start_backend():
    """Inicia el backend Flask"""
    logger.info("🚀 Iniciando backend Flask...")
    
    try:
        from app.backend import app
        
        # Ejecutar en thread
        flask_thread = threading.Thread(
            target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, threaded=True),
            daemon=True
        )
        flask_thread.start()
        logger.info("✅ Backend iniciado en http://localhost:5000")
        
        # Mantener app vivo
        while True:
            time.sleep(1)
    
    except Exception as e:
        logger.error(f"❌ Error iniciando backend: {str(e)}")


def main():
    """Función principal"""
    logger.info("=" * 60)
    logger.info("🎯 Bot Analista - Dashboard & ML Startup")
    logger.info("=" * 60)
    
    # Entrenar modelos en background (puede tomar unos minutos)
    ml_thread = threading.Thread(target=train_models_background, daemon=True)
    ml_thread.start()
    
    # Esperar un poco para que comience el entrenamiento
    time.sleep(2)
    
    # Iniciar backend
    try:
        start_backend()
    except KeyboardInterrupt:
        logger.info("👋 Cerrando aplicación...")


if __name__ == '__main__':
    main()
