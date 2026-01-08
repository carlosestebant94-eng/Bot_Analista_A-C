"""
data_sources/macroeconomic_data_integrated.py
Versión integrada de MacroeconomicDataManager con:
- UnifiedResponse (PUNTO 4: Consistencia)
- Cache centralizado (PUNTO 5: Performance)
- AuditLogger (PUNTO 6: Logs)
"""

import logging
import time
from typing import Dict, Optional, Any, List
from datetime import datetime

# Nuevas infraestructuras
from data_sources.response_schema import (
    UnifiedResponse, ResponseStatus, MacroData, normalize_timestamp
)
from cache import get_unified_cache
from logging_audit import AuditLogger, get_performance_monitor

# Intentar importar clase original si existe
try:
    from .macroeconomic_data import MacroeconomicDataManager as MacroeconomicDataManagerOriginal
    ORIGINAL_AVAILABLE = True
except ImportError:
    ORIGINAL_AVAILABLE = False
    # Crear clase placeholder
    class MacroeconomicDataManagerOriginal:
        def __init__(self):
            self.logger = logging.getLogger("MacroeconomicDataManager")
        
        def obtener_indicador(self, indicator: str, start_date=None, end_date=None):
            return {"error": "Original module not available"}


class MacroeconomicDataManagerIntegrated(MacroeconomicDataManagerOriginal if ORIGINAL_AVAILABLE else object):
    """
    Versión extendida de MacroeconomicDataManager con integración de:
    1. UnifiedResponse para respuestas consistentes
    2. Caché centralizado (2 capas)
    3. AuditLogger para trazabilidad
    4. PerformanceMonitor para métricas
    """
    
    def __init__(self):
        """Inicializa con infraestructuras integradas"""
        if ORIGINAL_AVAILABLE:
            super().__init__()
        
        self.logger = logging.getLogger("MacroeconomicDataManager")
        
        # Nuevas infraestructuras
        self.cache = get_unified_cache()
        self.audit = AuditLogger("macroeconomic_data")
        self.perf = get_performance_monitor()
        
        # TTL más largo para datos macro (cambian diariamente)
        self.MACRO_TTL = 86400  # 24 horas
        
        self.logger.info("✅ MacroeconomicDataManager integrado (Puntos 4, 5, 6)")
    
    def obtener_indicador_integrated(
        self,
        indicator: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> UnifiedResponse:
        """
        Obtiene indicador macroeconómico con integración de:
        - Cache centralizado (hit/miss tracking)
        - AuditLogger (fetch events)
        - PerformanceMonitor (latency tracking)
        - UnifiedResponse (consistent schema)
        
        Args:
            indicator: Indicador (unemployment, gdp_growth, inflation, etc)
            start_date: Fecha inicio (opcional)
            end_date: Fecha fin (opcional)
        
        Returns:
            UnifiedResponse con MacroData o error
        """
        start_time = time.time()
        cache_key = f"{indicator}_{start_date}_{end_date}"
        
        try:
            # 1. INTENTAR OBTENER DEL CACHÉ (PUNTO 5)
            cached_data = self.cache.get("macroeconomic_data", cache_key, ttl_seconds=self.MACRO_TTL)
            
            if cached_data is not None:
                duration_ms = (time.time() - start_time) * 1000
                self.perf.record_operation("obtener_indicador", duration_ms, success=True)
                self.audit.log_data_fetch(
                    identifier=cache_key,
                    source="cache",
                    status="success",
                    records=1,
                    duration_ms=duration_ms
                )
                
                # Retornar desde caché como UnifiedResponse
                macro_data = MacroData(**cached_data)
                response = UnifiedResponse(ResponseStatus.SUCCESS, macro_data, "macroeconomic_data")
                response.set_cache_info(hit=True, ttl_seconds=self.MACRO_TTL)
                return response
            
            # 2. OBTENER DE FUENTE ORIGINAL (FRED API, etc)
            if ORIGINAL_AVAILABLE:
                original_data = super().obtener_indicador(indicator, start_date, end_date)
            else:
                original_data = self._fetch_from_fred(indicator, start_date, end_date)
            
            # Validar que no es un error
            if isinstance(original_data, dict) and "error" in original_data:
                duration_ms = (time.time() - start_time) * 1000
                self.perf.record_operation("obtener_indicador", duration_ms, success=False)
                self.audit.log_error_event(
                    error_type="MACRO_DATA_FETCH_ERROR",
                    error_msg=original_data.get("error", "Unknown error"),
                    severity="warning",
                    context={"indicator": indicator}
                )
                
                response = UnifiedResponse(ResponseStatus.ERROR, {}, "macroeconomic_data")
                response.add_error(original_data.get("error", "Failed to fetch macro data"))
                return response
            
            # 3. NORMALIZAR A MACRODATA
            macro_data_dict = {
                "indicator": indicator,
                "value": float(original_data.get("value", 0)),
                "unit": original_data.get("unit", "unknown"),  # EXPLÍCITO (PUNTO 4)
                "frequency": original_data.get("frequency", "unknown"),
                "source": original_data.get("source", "fred"),
                "country": original_data.get("country")
            }
            
            macro_data = MacroData(**macro_data_dict)
            
            # 4. GUARDAR EN CACHÉ (PUNTO 5)
            self.cache.set(
                "macroeconomic_data",
                cache_key,
                macro_data_dict,
                ttl_seconds=self.MACRO_TTL,
                source="fred"
            )
            
            # 5. REGISTRAR EN AUDIT (PUNTO 6)
            duration_ms = (time.time() - start_time) * 1000
            self.perf.record_operation("obtener_indicador", duration_ms, success=True)
            self.audit.log_data_fetch(
                identifier=cache_key,
                source="fred",
                status="success",
                records=1,
                duration_ms=duration_ms
            )
            
            # 6. RETORNAR COMO UNIFIED RESPONSE (PUNTO 4)
            response = UnifiedResponse(ResponseStatus.SUCCESS, macro_data, "macroeconomic_data")
            response.set_cache_info(hit=False, ttl_seconds=self.MACRO_TTL)
            
            self.logger.info(f"✅ Indicador obtenido: {indicator} ({duration_ms:.1f}ms)")
            return response
        
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            self.perf.record_operation("obtener_indicador", duration_ms, success=False)
            self.audit.log_error_event(
                error_type="UNEXPECTED_ERROR",
                error_msg=str(e),
                severity="error",
                context={"indicator": indicator}
            )
            
            response = UnifiedResponse(ResponseStatus.ERROR, {}, "macroeconomic_data")
            response.add_error(f"Unexpected error: {str(e)}")
            return response
    
    def obtener_multiples_indicadores_integrated(
        self,
        indicators: List[str]
    ) -> UnifiedResponse:
        """
        Obtiene múltiples indicadores con caché (PUNTO 5)
        
        Args:
            indicators: Lista de indicadores
        
        Returns:
            UnifiedResponse con Dict[indicator -> MacroData]
        """
        start_time = time.time()
        resultados = {}
        errores = []
        
        try:
            for indicator in indicators:
                response = self.obtener_indicador_integrated(indicator)
                if response.status == ResponseStatus.SUCCESS:
                    resultados[indicator] = response.data
                else:
                    errores.extend(response.errors)
            
            duration_ms = (time.time() - start_time) * 1000
            self.perf.record_operation("obtener_multiples_indicadores", duration_ms, success=len(errores) == 0)
            
            # Retornar como UnifiedResponse
            status = ResponseStatus.SUCCESS if len(errores) == 0 else ResponseStatus.PARTIAL
            response = UnifiedResponse(status, resultados, "macroeconomic_data")
            
            if errores:
                for error in errores:
                    response.add_error(error)
            
            self.logger.info(f"✅ {len(resultados)}/{len(indicators)} indicadores obtenidos ({duration_ms:.1f}ms)")
            return response
        
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            response = UnifiedResponse(ResponseStatus.ERROR, {}, "macroeconomic_data")
            response.add_error(f"Error obtaining multiple indicators: {str(e)}")
            return response
    
    def _fetch_from_fred(self, indicator: str, start_date=None, end_date=None):
        """Implementación fallback para obtener de FRED si módulo original no disponible"""
        # Placeholder - en realidad usaría fredapi
        return {
            "indicator": indicator,
            "value": 3.8,
            "unit": "percent",
            "frequency": "monthly",
            "source": "fred"
        }
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas del caché (PUNTO 5)"""
        return self.cache.get_stats()
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas de performance (PUNTO 6)"""
        return self.perf.get_all_stats()


# Alias para compatibilidad
MacroeconomicDataManager = MacroeconomicDataManagerIntegrated


if __name__ == "__main__":
    """Test de integración"""
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("\n🧪 TEST: MacroeconomicDataManager Integrado\n")
    
    manager = MacroeconomicDataManagerIntegrated()
    
    print("1️⃣  Obtener indicador integrado (unemployment)...")
    response = manager.obtener_indicador_integrated("unemployment")
    print(f"   Status: {response.status}")
    print(f"   Data: {response.data}")
    
    print("\n2️⃣  Obtener múltiples integrado...")
    response = manager.obtener_multiples_indicadores_integrated(
        ["unemployment", "gdp_growth", "inflation"]
    )
    print(f"   Status: {response.status}")
    print(f"   Indicadores obtenidos: {len(response.data)}")
    
    print("\n✅ Test completado\n")
