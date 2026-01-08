"""
data_sources/market_data_integrated.py
Versión integrada de MarketDataManager con:
- UnifiedResponse (PUNTO 4: Consistencia)
- Cache centralizado (PUNTO 5: Performance)
- AuditLogger (PUNTO 6: Logs)

Este archivo sirve como adapter/wrapper que integra la clase MarketDataManager
original con las nuevas infraestructuras sin cambiar el archivo original aún.
"""

import logging
import time
from typing import Dict, Optional, Any, List
from datetime import datetime

# Nuevas infraestructuras
from data_sources.response_schema import (
    UnifiedResponse, ResponseStatus, PriceData, normalize_timestamp, normalize_percentage
)
from cache import get_unified_cache
from logging_audit import AuditLogger, get_performance_monitor

# Clase original
from .market_data import MarketDataManager as MarketDataManagerOriginal


class MarketDataManagerIntegrated(MarketDataManagerOriginal):
    """
    Versión extendida de MarketDataManager con integración de:
    1. UnifiedResponse para respuestas consistentes
    2. Caché centralizado (2 capas)
    3. AuditLogger para trazabilidad
    4. PerformanceMonitor para métricas
    """
    
    def __init__(self, polygon_api_key: Optional[str] = None, 
                 alpha_vantage_key: Optional[str] = None):
        """Inicializa con infraestructuras integradas"""
        super().__init__(polygon_api_key, alpha_vantage_key)
        
        # Nuevas infraestructuras
        self.cache = get_unified_cache()
        self.audit = AuditLogger("market_data")
        self.perf = get_performance_monitor()
        
        self.logger.info("✅ MarketDataManager integrado (Puntos 4, 5, 6)")
    
    def obtener_datos_actuales_integrated(self, ticker: str) -> UnifiedResponse:
        """
        Obtiene datos actuales con integración de:
        - Cache centralizado (hit/miss tracking)
        - AuditLogger (data fetch events)
        - PerformanceMonitor (latency tracking)
        - UnifiedResponse (consistent schema)
        
        Args:
            ticker: Símbolo del instrumento (AAPL, MSFT, etc)
        
        Returns:
            UnifiedResponse con PriceData o error
        """
        start_time = time.time()
        
        try:
            # 1. INTENTAR OBTENER DEL CACHÉ (PUNTO 5)
            cached_data = self.cache.get("market_data", ticker, ttl_seconds=3600)
            
            if cached_data is not None:
                duration_ms = (time.time() - start_time) * 1000
                self.perf.record_operation("obtener_datos_actuales", duration_ms, success=True)
                self.audit.log_data_fetch(
                    identifier=ticker,
                    source="cache",
                    status="success",
                    records=1,
                    duration_ms=duration_ms
                )
                
                # Retornar desde caché como UnifiedResponse
                price_data = PriceData(**cached_data)
                response = UnifiedResponse(ResponseStatus.SUCCESS, price_data, "market_data")
                response.set_cache_info(hit=True, ttl_seconds=3600)
                return response
            
            # 2. OBTENER DE YFINANCE ORIGINAL
            original_data = super().obtener_datos_actuales(ticker)
            
            # Validar que no es un error
            if isinstance(original_data, dict) and "error" in original_data:
                duration_ms = (time.time() - start_time) * 1000
                self.perf.record_operation("obtener_datos_actuales", duration_ms, success=False)
                self.audit.log_error_event(
                    error_type="DATA_FETCH_ERROR",
                    error_msg=original_data.get("error", "Unknown error"),
                    severity="warning"
                )
                
                response = UnifiedResponse(ResponseStatus.ERROR, {}, "market_data")
                response.add_error(original_data.get("error", "Failed to fetch data"))
                return response
            
            # 3. NORMALIZAR A PRICEDATA
            price_data_dict = {
                "ticker": ticker,
                "current_price_usd": float(original_data.get("currentPrice", 0)),
                "volume_units": int(original_data.get("volume", 0)),
                "change_percent": float(original_data.get("regularMarketChangePercent", 0)),
                "market_cap_usd": original_data.get("marketCap"),
                "pe_ratio": original_data.get("trailingPE"),
                "source": "yfinance"
            }
            
            price_data = PriceData(**price_data_dict)
            
            # 4. GUARDAR EN CACHÉ (PUNTO 5)
            self.cache.set(
                "market_data",
                ticker,
                price_data_dict,
                ttl_seconds=3600,
                source="yfinance"
            )
            
            # 5. REGISTRAR EN AUDIT (PUNTO 6)
            duration_ms = (time.time() - start_time) * 1000
            self.perf.record_operation("obtener_datos_actuales", duration_ms, success=True)
            self.audit.log_data_fetch(
                identifier=ticker,
                source="yfinance",
                status="success",
                records=1,
                duration_ms=duration_ms
            )
            
            # 6. RETORNAR COMO UNIFIED RESPONSE (PUNTO 4)
            response = UnifiedResponse(ResponseStatus.SUCCESS, price_data, "market_data")
            response.set_cache_info(hit=False, ttl_seconds=3600)
            
            self.logger.info(f"✅ Datos obtenidos: {ticker} ({duration_ms:.1f}ms)")
            return response
        
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            self.perf.record_operation("obtener_datos_actuales", duration_ms, success=False)
            self.audit.log_error_event(
                error_type="UNEXPECTED_ERROR",
                error_msg=str(e),
                severity="error",
                context={"ticker": ticker}
            )
            
            response = UnifiedResponse(ResponseStatus.ERROR, {}, "market_data")
            response.add_error(f"Unexpected error: {str(e)}")
            return response
    
    def obtener_datos_multiples_integrated(self, tickers: List[str]) -> UnifiedResponse:
        """
        Obtiene datos de múltiples tickers
        Usa batching + caché para optimizar (PUNTO 5)
        
        Args:
            tickers: Lista de tickers
        
        Returns:
            UnifiedResponse con Dict[ticker -> PriceData]
        """
        start_time = time.time()
        resultados = {}
        errores = []
        
        try:
            # Intentar obtener todos del caché primero
            for ticker in tickers:
                cached_data = self.cache.get("market_data", ticker, ttl_seconds=3600)
                if cached_data is not None:
                    resultados[ticker] = PriceData(**cached_data)
                else:
                    # Si no está en caché, obtener de YFinance
                    response = self.obtener_datos_actuales_integrated(ticker)
                    if response.status == ResponseStatus.SUCCESS:
                        resultados[ticker] = response.data
                    else:
                        errores.extend(response.errors)
            
            duration_ms = (time.time() - start_time) * 1000
            self.perf.record_operation("obtener_datos_multiples", duration_ms, success=len(errores) == 0)
            
            # Retornar como UnifiedResponse
            status = ResponseStatus.SUCCESS if len(errores) == 0 else ResponseStatus.PARTIAL
            response = UnifiedResponse(status, resultados, "market_data")
            
            if errores:
                for error in errores:
                    response.add_error(error)
            
            self.logger.info(f"✅ {len(resultados)}/{len(tickers)} datos obtenidos ({duration_ms:.1f}ms)")
            return response
        
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            response = UnifiedResponse(ResponseStatus.ERROR, {}, "market_data")
            response.add_error(f"Error obtaining multiple data: {str(e)}")
            return response
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas del caché (PUNTO 5)"""
        return self.cache.get_stats()
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas de performance (PUNTO 6)"""
        return self.perf.get_all_stats()
    
    # Métodos privados auxiliares
    def _from_dict_to_price_data(self, data: Dict) -> Optional[PriceData]:
        """Convierte dict a PriceData con normalización"""
        try:
            return PriceData(
                ticker=data.get("ticker"),
                current_price_usd=float(data.get("currentPrice", 0)),
                volume_units=int(data.get("volume", 0)),
                change_percent=normalize_percentage(data.get("regularMarketChangePercent", 0), "decimal"),
                market_cap_usd=data.get("marketCap"),
                pe_ratio=data.get("trailingPE"),
                source=data.get("source", "unknown")
            )
        except Exception as e:
            self.logger.error(f"Error converting to PriceData: {str(e)}")
            return None


# Alias para compatibilidad
MarketDataManager = MarketDataManagerIntegrated


if __name__ == "__main__":
    """Test de integración"""
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("\n🧪 TEST: MarketDataManager Integrado\n")
    
    manager = MarketDataManagerIntegrated()
    
    print("1️⃣  Obtener precio integrado (AAPL)...")
    response = manager.obtener_datos_actuales_integrated("AAPL")
    print(f"   Status: {response.status}")
    print(f"   Data: {response.data}")
    print(f"   Errors: {response.errors}")
    
    print("\n2️⃣  Obtener múltiples integrado...")
    response = manager.obtener_datos_multiples_integrated(["AAPL", "MSFT", "GOOGL"])
    print(f"   Status: {response.status}")
    print(f"   Tickers obtenidos: {len(response.data)}")
    
    print("\n3️⃣  Cache stats...")
    stats = manager.get_cache_stats()
    print(f"   Hit rate: {stats.get('hit_rate_percent')}%")
    print(f"   Total entries: {stats.get('memory_entries')}")
    
    print("\n4️⃣  Performance stats...")
    perf_stats = manager.get_performance_stats()
    if "obtener_datos_actuales" in perf_stats:
        print(f"   Operaciones: {perf_stats['obtener_datos_actuales']['count']}")
        print(f"   Promedio: {perf_stats['obtener_datos_actuales']['avg_ms']:.2f}ms")
    
    print("\n✅ Test completado\n")
