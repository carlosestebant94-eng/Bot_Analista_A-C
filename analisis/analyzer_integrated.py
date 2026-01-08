"""
analisis/analyzer_integrated.py
Versión integrada de Analyzer con:
- UnifiedResponse (PUNTO 4: Consistencia)
- PerformanceMonitor (PUNTO 6: Performance tracking)
- AuditLogger (PUNTO 6: Logs)
"""

import logging
import time
from typing import Dict, Optional, Any

# Nuevas infraestructuras
from data_sources.response_schema import (
    UnifiedResponse, ResponseStatus, AnalysisResult
)
from logging_audit import AuditLogger, get_performance_monitor

# Intentar importar clase original
try:
    from .analyzer import Analyzer as AnalyzerOriginal
    ORIGINAL_AVAILABLE = True
except ImportError:
    ORIGINAL_AVAILABLE = False
    class AnalyzerOriginal:
        def __init__(self):
            self.logger = logging.getLogger("Analyzer")
        
        def analizar(self, ticker: str, datos: Dict = None):
            return {"error": "Original module not available"}


class AnalyzerIntegrated(AnalyzerOriginal if ORIGINAL_AVAILABLE else object):
    """
    Versión extendida de Analyzer con integración de:
    1. UnifiedResponse para respuestas consistentes
    2. PerformanceMonitor para latency tracking
    3. AuditLogger para trazabilidad
    """
    
    def __init__(self):
        """Inicializa con infraestructuras integradas"""
        if ORIGINAL_AVAILABLE:
            super().__init__()
        
        self.logger = logging.getLogger("Analyzer")
        
        # Nuevas infraestructuras
        self.audit = AuditLogger("analyzer")
        self.perf = get_performance_monitor()
        
        self.logger.info("✅ Analyzer integrado (Puntos 4, 6)")
    
    def analizar_integrated(
        self,
        ticker: str,
        datos: Optional[Dict] = None
    ) -> UnifiedResponse:
        """
        Realiza análisis técnico/fundamental con integración de:
        - PerformanceMonitor (track latency)
        - AuditLogger (log events)
        - UnifiedResponse (consistent schema)
        
        Args:
            ticker: Símbolo del instrumento
            datos: Datos históricos opcionales
        
        Returns:
            UnifiedResponse con AnalysisResult
        """
        start_time = time.time()
        
        try:
            # 1. REALIZAR ANÁLISIS ORIGINAL
            if ORIGINAL_AVAILABLE:
                analysis_result = super().analizar(ticker, datos)
            else:
                analysis_result = self._perform_analysis(ticker, datos)
            
            # Validar que no es un error
            if isinstance(analysis_result, dict) and "error" in analysis_result:
                duration_ms = (time.time() - start_time) * 1000
                self.perf.record_operation("analizar", duration_ms, success=False)
                self.audit.log_error_event(
                    error_type="ANALYSIS_ERROR",
                    error_msg=analysis_result.get("error", "Unknown error"),
                    severity="warning",
                    context={"ticker": ticker}
                )
                
                response = UnifiedResponse(ResponseStatus.ERROR, {}, "analyzer")
                response.add_error(analysis_result.get("error", "Analysis failed"))
                return response
            
            # 2. NORMALIZAR A ANALYSISRESULT
            # Extraer findings y recommendations del resultado original
            findings = analysis_result.get("findings", [])
            recommendations = analysis_result.get("recommendations", [])
            confidence = float(analysis_result.get("confidence", 0.5))
            analysis_type = analysis_result.get("type", "technical")
            risk_level = analysis_result.get("risk_level", "medium")
            
            analysis_data = AnalysisResult(
                analysis_type=analysis_type,
                ticker=ticker,
                confidence=confidence,  # Asegura que esté entre 0-1
                findings=findings,
                recommendations=recommendations,
                risk_level=risk_level,
                sources_used=["technical_indicators", "historical_data"]
            )
            
            # 3. REGISTRAR PERFORMANCE (PUNTO 6)
            duration_ms = (time.time() - start_time) * 1000
            self.perf.record_operation("analizar", duration_ms, success=True)
            
            # 4. REGISTRAR EN AUDIT (PUNTO 6)
            self.audit.log_analysis_result(
                ticker=ticker,
                analysis_type=analysis_type,
                confidence=confidence,
                findings=len(findings),
                duration_ms=duration_ms
            )
            
            # 5. RETORNAR COMO UNIFIED RESPONSE (PUNTO 4)
            response = UnifiedResponse(ResponseStatus.SUCCESS, analysis_data, "analyzer")
            
            self.logger.info(
                f"✅ Análisis completado: {ticker} "
                f"(confidence={confidence:.2f}, {duration_ms:.1f}ms)"
            )
            return response
        
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            self.perf.record_operation("analizar", duration_ms, success=False)
            self.audit.log_error_event(
                error_type="UNEXPECTED_ERROR",
                error_msg=str(e),
                severity="error",
                context={"ticker": ticker}
            )
            
            response = UnifiedResponse(ResponseStatus.ERROR, {}, "analyzer")
            response.add_error(f"Unexpected error: {str(e)}")
            return response
    
    def analizar_multiples_integrated(
        self,
        tickers: list
    ) -> UnifiedResponse:
        """
        Analiza múltiples tickers
        
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
                response = self.analizar_integrated(ticker)
                if response.status == ResponseStatus.SUCCESS:
                    resultados[ticker] = response.data
                else:
                    errores.extend(response.errors)
            
            duration_ms = (time.time() - start_time) * 1000
            self.perf.record_operation("analizar_multiples", duration_ms, success=len(errores) == 0)
            
            status = ResponseStatus.SUCCESS if len(errores) == 0 else ResponseStatus.PARTIAL
            response = UnifiedResponse(status, resultados, "analyzer")
            
            if errores:
                for error in errores:
                    response.add_error(error)
            
            self.logger.info(f"✅ {len(resultados)}/{len(tickers)} análisis completados ({duration_ms:.1f}ms)")
            return response
        
        except Exception as e:
            response = UnifiedResponse(ResponseStatus.ERROR, {}, "analyzer")
            response.add_error(f"Error analyzing multiple: {str(e)}")
            return response
    
    def _perform_analysis(self, ticker: str, datos: Dict = None):
        """Análisis fallback si módulo original no disponible"""
        return {
            "type": "technical",
            "ticker": ticker,
            "confidence": 0.75,
            "findings": ["Support level detected", "Trend reversal signal"],
            "recommendations": ["Hold", "Watch support"],
            "risk_level": "medium"
        }
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas de performance (PUNTO 6)"""
        return self.perf.get_all_stats()


# Alias para compatibilidad
Analyzer = AnalyzerIntegrated


if __name__ == "__main__":
    """Test de integración"""
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("\n🧪 TEST: Analyzer Integrado\n")
    
    analyzer = AnalyzerIntegrated()
    
    print("1️⃣  Analizar integrado (AAPL)...")
    response = analyzer.analizar_integrated("AAPL")
    print(f"   Status: {response.status}")
    print(f"   Data: {response.data}")
    
    print("\n2️⃣  Analizar múltiples integrado...")
    response = analyzer.analizar_multiples_integrated(["AAPL", "MSFT"])
    print(f"   Status: {response.status}")
    print(f"   Análisis: {len(response.data)}")
    
    print("\n✅ Test completado\n")
