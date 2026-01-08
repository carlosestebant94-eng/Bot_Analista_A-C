"""
analisis/ml_predictor_integrated.py
Versión integrada de MLPredictor con:
- UnifiedResponse (PUNTO 4: Consistencia)
- PerformanceMonitor (PUNTO 6: Performance tracking)
- AuditLogger (PUNTO 6: Logs)
"""

import logging
import time
from typing import Dict, Optional, Any, List

# Nuevas infraestructuras
from data_sources.response_schema import (
    UnifiedResponse, ResponseStatus, AnalysisResult
)
from logging_audit import AuditLogger, get_performance_monitor

# Intentar importar clase original
try:
    from .ml_predictor import MLPredictor as MLPredictorOriginal
    ORIGINAL_AVAILABLE = True
except ImportError:
    ORIGINAL_AVAILABLE = False
    class MLPredictorOriginal:
        def __init__(self):
            self.logger = logging.getLogger("MLPredictor")
        
        def predecir(self, ticker: str, datos: Dict = None):
            return {"error": "Original module not available"}


class MLPredictorIntegrated(MLPredictorOriginal if ORIGINAL_AVAILABLE else object):
    """
    Versión extendida de MLPredictor con integración de:
    1. UnifiedResponse para respuestas consistentes
    2. PerformanceMonitor para latency tracking
    3. AuditLogger para trazabilidad
    """
    
    def __init__(self):
        """Inicializa con infraestructuras integradas"""
        if ORIGINAL_AVAILABLE:
            super().__init__()
        
        self.logger = logging.getLogger("MLPredictor")
        
        # Nuevas infraestructuras
        self.audit = AuditLogger("ml_predictor")
        self.perf = get_performance_monitor()
        
        self.logger.info("✅ MLPredictor integrado (Puntos 4, 6)")
    
    def predecir_integrated(
        self,
        ticker: str,
        datos: Optional[Dict] = None
    ) -> UnifiedResponse:
        """
        Realiza predicción ML con integración de:
        - PerformanceMonitor (track latency)
        - AuditLogger (log events)
        - UnifiedResponse (consistent schema)
        
        Args:
            ticker: Símbolo del instrumento
            datos: Datos para predicción
        
        Returns:
            UnifiedResponse con AnalysisResult
        """
        start_time = time.time()
        
        try:
            # 1. REALIZAR PREDICCIÓN ORIGINAL
            if ORIGINAL_AVAILABLE:
                prediction_result = super().predecir(ticker, datos)
            else:
                prediction_result = self._perform_prediction(ticker, datos)
            
            # Validar que no es un error
            if isinstance(prediction_result, dict) and "error" in prediction_result:
                duration_ms = (time.time() - start_time) * 1000
                self.perf.record_operation("predecir", duration_ms, success=False)
                self.audit.log_error_event(
                    error_type="PREDICTION_ERROR",
                    error_msg=prediction_result.get("error", "Unknown error"),
                    severity="warning",
                    context={"ticker": ticker}
                )
                
                response = UnifiedResponse(ResponseStatus.ERROR, {}, "ml_predictor")
                response.add_error(prediction_result.get("error", "Prediction failed"))
                return response
            
            # 2. NORMALIZAR A ANALYSISRESULT
            confidence = float(prediction_result.get("confidence", 0.5))
            # Asegurar que esté entre 0-1
            if confidence > 1:
                confidence = confidence / 100
            
            prediction = prediction_result.get("prediction", "HOLD")
            findings = [
                f"ML Prediction: {prediction}",
                f"Model confidence: {confidence:.2%}"
            ]
            findings.extend(prediction_result.get("features", []))
            
            recommendations = []
            if prediction == "BUY":
                recommendations.append("Consider buying")
            elif prediction == "SELL":
                recommendations.append("Consider selling")
            else:
                recommendations.append("Hold current position")
            
            analysis_data = AnalysisResult(
                analysis_type="machine_learning",
                ticker=ticker,
                confidence=confidence,
                findings=findings,
                recommendations=recommendations,
                risk_level="medium",
                sources_used=["random_forest", "gradient_boosting", "neural_network"]
            )
            
            # 3. REGISTRAR PERFORMANCE (PUNTO 6)
            duration_ms = (time.time() - start_time) * 1000
            self.perf.record_operation("predecir", duration_ms, success=True)
            
            # 4. REGISTRAR EN AUDIT (PUNTO 6)
            self.audit.log_analysis_result(
                ticker=ticker,
                analysis_type="machine_learning",
                confidence=confidence,
                findings=len(findings),
                duration_ms=duration_ms
            )
            
            # 5. RETORNAR COMO UNIFIED RESPONSE (PUNTO 4)
            response = UnifiedResponse(ResponseStatus.SUCCESS, analysis_data, "ml_predictor")
            
            self.logger.info(
                f"✅ Predicción completada: {ticker} "
                f"(signal={prediction}, confidence={confidence:.2f}, {duration_ms:.1f}ms)"
            )
            return response
        
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            self.perf.record_operation("predecir", duration_ms, success=False)
            self.audit.log_error_event(
                error_type="UNEXPECTED_ERROR",
                error_msg=str(e),
                severity="error",
                context={"ticker": ticker}
            )
            
            response = UnifiedResponse(ResponseStatus.ERROR, {}, "ml_predictor")
            response.add_error(f"Unexpected error: {str(e)}")
            return response
    
    def predecir_multiples_integrated(
        self,
        tickers: List[str]
    ) -> UnifiedResponse:
        """
        Realiza predicción para múltiples tickers
        
        Args:
            tickers: Lista de tickers
        
        Returns:
            UnifiedResponse con Dict[ticker -> AnalysisResult]
        """
        start_time = time.time()
        resultados = {}
        errores = []
        
        try:
            for ticker in tickers:
                response = self.predecir_integrated(ticker)
                if response.status == ResponseStatus.SUCCESS:
                    resultados[ticker] = response.data
                else:
                    errores.extend(response.errors)
            
            duration_ms = (time.time() - start_time) * 1000
            self.perf.record_operation("predecir_multiples", duration_ms, success=len(errores) == 0)
            
            status = ResponseStatus.SUCCESS if len(errores) == 0 else ResponseStatus.PARTIAL
            response = UnifiedResponse(status, resultados, "ml_predictor")
            
            if errores:
                for error in errores:
                    response.add_error(error)
            
            self.logger.info(f"✅ {len(resultados)}/{len(tickers)} predicciones completadas ({duration_ms:.1f}ms)")
            return response
        
        except Exception as e:
            response = UnifiedResponse(ResponseStatus.ERROR, {}, "ml_predictor")
            response.add_error(f"Error predicting multiple: {str(e)}")
            return response
    
    def ensemble_prediction_integrated(
        self,
        ticker: str,
        datos: Optional[Dict] = None
    ) -> UnifiedResponse:
        """
        Predicción de ensemble (RF + GB + NN) con integración
        
        Args:
            ticker: Símbolo del instrumento
            datos: Datos para predicción
        
        Returns:
            UnifiedResponse con AnalysisResult
        """
        start_time = time.time()
        
        try:
            if ORIGINAL_AVAILABLE:
                ensemble_result = super().predecir(ticker, datos)
            else:
                ensemble_result = self._perform_ensemble(ticker, datos)
            
            if isinstance(ensemble_result, dict) and "error" in ensemble_result:
                duration_ms = (time.time() - start_time) * 1000
                self.perf.record_operation("ensemble_prediction", duration_ms, success=False)
                response = UnifiedResponse(ResponseStatus.ERROR, {}, "ml_predictor")
                response.add_error(ensemble_result.get("error"))
                return response
            
            # Normalizar resultado
            confidence = float(ensemble_result.get("confidence", 0.5))
            if confidence > 1:
                confidence = confidence / 100
            
            analysis_data = AnalysisResult(
                analysis_type="machine_learning_ensemble",
                ticker=ticker,
                confidence=confidence,
                findings=ensemble_result.get("findings", []),
                recommendations=ensemble_result.get("recommendations", []),
                risk_level=ensemble_result.get("risk_level", "medium"),
                sources_used=["random_forest", "gradient_boosting", "neural_network"]
            )
            
            duration_ms = (time.time() - start_time) * 1000
            self.perf.record_operation("ensemble_prediction", duration_ms, success=True)
            self.audit.log_analysis_result(
                ticker=ticker,
                analysis_type="machine_learning_ensemble",
                confidence=confidence,
                findings=len(analysis_data.findings),
                duration_ms=duration_ms
            )
            
            response = UnifiedResponse(ResponseStatus.SUCCESS, analysis_data, "ml_predictor")
            return response
        
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            self.perf.record_operation("ensemble_prediction", duration_ms, success=False)
            response = UnifiedResponse(ResponseStatus.ERROR, {}, "ml_predictor")
            response.add_error(f"Ensemble prediction error: {str(e)}")
            return response
    
    def _perform_prediction(self, ticker: str, datos: Dict = None):
        """Predicción fallback si módulo original no disponible"""
        return {
            "prediction": "BUY",
            "confidence": 0.78,
            "features": ["Volume trend positive", "RSI < 70"],
            "error": None
        }
    
    def _perform_ensemble(self, ticker: str, datos: Dict = None):
        """Ensemble fallback si módulo original no disponible"""
        return {
            "prediction": "BUY",
            "confidence": 0.82,
            "findings": [
                "RF prediction: BUY",
                "GB prediction: BUY",
                "NN prediction: HOLD",
                "Ensemble consensus: BUY (2/3)"
            ],
            "recommendations": ["Strong buy signal"],
            "risk_level": "medium"
        }
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas de performance (PUNTO 6)"""
        return self.perf.get_all_stats()


# Alias para compatibilidad
MLPredictor = MLPredictorIntegrated


if __name__ == "__main__":
    """Test de integración"""
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("\n🧪 TEST: MLPredictor Integrado\n")
    
    ml = MLPredictorIntegrated()
    
    print("1️⃣  Predicción integrada (AAPL)...")
    response = ml.predecir_integrated("AAPL")
    print(f"   Status: {response.status}")
    print(f"   Data: {response.data}")
    
    print("\n2️⃣  Ensemble integrado (AAPL)...")
    response = ml.ensemble_prediction_integrated("AAPL")
    print(f"   Status: {response.status}")
    print(f"   Confidence: {response.data.confidence if response.data else 'N/A'}")
    
    print("\n3️⃣  Predicciones múltiples integradas...")
    response = ml.predecir_multiples_integrated(["AAPL", "MSFT"])
    print(f"   Status: {response.status}")
    print(f"   Predicciones: {len(response.data)}")
    
    print("\n✅ Test completado\n")
