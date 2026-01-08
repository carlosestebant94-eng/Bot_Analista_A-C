"""
PLAN_INTEGRACION_FASE_5A.py
Actualiza módulos para usar las nuevas infraestructuras (UnifiedResponse, Cache, Async, Logs)

Este archivo documenta los cambios a realizar en cada módulo
"""

# ============================================================================
# MÓDULO 1: market_data.py
# ============================================================================
# Cambios necesarios:
# 1. Importar UnifiedResponse, PriceData, ResponseStatus desde response_schema
# 2. Importar get_unified_cache para almacenar/recuperar precios
# 3. Importar AuditLogger para registrar data fetches
# 4. Cambiar retorno de obtener_datos_actuales() de Dict → UnifiedResponse(PriceData)
# 5. Cambiar retorno de obtener_datos_multiples() para usar AsyncDataBatcher

MARKET_DATA_CHANGES = {
    "new_imports": [
        "from data_sources.response_schema import UnifiedResponse, PriceData, ResponseStatus, normalize_timestamp, normalize_percentage",
        "from cache import get_unified_cache",
        "from logging_audit import AuditLogger",
        "from async_ops import AsyncDataBatcher, get_async_executor",
    ],
    "new_initialization": [
        "self.cache = get_unified_cache()",
        "self.audit = AuditLogger('market_data')",
        "self.batcher = AsyncDataBatcher(batch_size=100)",
    ],
    "method_updates": [
        {
            "method": "obtener_datos_actuales(ticker)",
            "before_return": "Dict[str, Any]",
            "after_return": "UnifiedResponse",
            "changes": [
                "1. Intentar obtener del caché: cache.get('market_data', ticker)",
                "2. Si hit: registrar audit, retornar UnifiedResponse con cache_metadata",
                "3. Si miss: obtener de yfinance",
                "4. Crear PriceData con datos normalizados",
                "5. Guardar en caché: cache.set('market_data', ticker, price_data)",
                "6. Registrar audit: audit.log_data_fetch(ticker, 'yfinance', 'success', ...)",
                "7. Retornar UnifiedResponse(ResponseStatus.SUCCESS, price_data)"
            ]
        }
    ]
}

# ============================================================================
# MÓDULO 2: macroeconomic_data.py
# ============================================================================
# Cambios necesarios:
# 1. Importar MacroData, UnifiedResponse, ResponseStatus
# 2. Importar caché centralizado
# 3. Importar AuditLogger
# 4. Retornar UnifiedResponse(MacroData) en lugar de Dict

MACRO_DATA_CHANGES = {
    "new_imports": [
        "from data_sources.response_schema import UnifiedResponse, MacroData, ResponseStatus, normalize_timestamp",
        "from cache import get_unified_cache",
        "from logging_audit import AuditLogger",
    ],
    "method_updates": [
        {
            "method": "obtener_indicador(indicator, start_date, end_date)",
            "changes": [
                "1. Intentar obtener del caché",
                "2. Si miss: obtener de FRED API",
                "3. Normalizar a MacroData (unit explícito)",
                "4. Guardar en caché (TTL más largo: 86400s = 24h)",
                "5. Retornar UnifiedResponse(MacroData)"
            ]
        }
    ]
}

# ============================================================================
# MÓDULO 3: analyzer.py
# ============================================================================
# Cambios necesarios:
# 1. Importar AnalysisResult, UnifiedResponse, ResponseStatus
# 2. Importar PerformanceMonitor para track análisis duración
# 3. Importar AuditLogger
# 4. Actualizar métodos para retornar UnifiedResponse(AnalysisResult)

ANALYZER_CHANGES = {
    "new_imports": [
        "from data_sources.response_schema import UnifiedResponse, AnalysisResult, ResponseStatus",
        "from logging_audit import AuditLogger, get_performance_monitor",
    ],
    "new_initialization": [
        "self.audit = AuditLogger('analyzer')",
        "self.perf = get_performance_monitor()",
    ],
    "method_updates": [
        {
            "method": "analizar(ticker)",
            "changes": [
                "1. Start timer: start_time = time.time()",
                "2. Realizar análisis normal",
                "3. Crear AnalysisResult con findings, recommendations, confidence",
                "4. Stop timer: duration_ms = (time.time() - start_time) * 1000",
                "5. Record performance: perf.record_operation('analizar', duration_ms)",
                "6. Log audit: audit.log_analysis_result(ticker, 'technical', confidence, len(findings))",
                "7. Retornar UnifiedResponse(ResponseStatus.SUCCESS, analysis_result)"
            ]
        }
    ]
}

# ============================================================================
# MÓDULO 4: ml_predictor.py
# ============================================================================
# Cambios necesarios:
# 1. Importar AnalysisResult, UnifiedResponse, ResponseStatus
# 2. Importar PerformanceMonitor
# 3. Actualizar retornos a UnifiedResponse(AnalysisResult)

ML_PREDICTOR_CHANGES = {
    "new_imports": [
        "from data_sources.response_schema import UnifiedResponse, AnalysisResult, ResponseStatus",
        "from logging_audit import AuditLogger, get_performance_monitor",
    ],
    "method_updates": [
        {
            "method": "predecir(ticker, data)",
            "changes": [
                "1. Track performance: start_time = time.time()",
                "2. Realizar predicción ML normal",
                "3. Crear AnalysisResult con confidence, findings",
                "4. Log: audit + perf monitor",
                "5. Retornar UnifiedResponse(ResponseStatus.SUCCESS, analysis_result)"
            ]
        }
    ]
}

# ============================================================================
# INTEGRACIÓN DE CACHÉ
# ============================================================================
# Reemplazar cache local en cada módulo con caché centralizado:

CACHE_INTEGRATION = """
# ANTES (cada módulo):
self.cache = {}
self.cache_ttl = 3600

def _get_from_cache(self, key):
    if key in self.cache:
        data, timestamp = self.cache[key]
        if datetime.now() - timestamp < timedelta(seconds=self.cache_ttl):
            return data
    return None

def _set_cache(self, key, value):
    self.cache[key] = (value, datetime.now())

# DESPUÉS (centralizado):
from cache import get_unified_cache

self.cache = get_unified_cache()

def _get_from_cache(self, key):
    return self.cache.get("market_data", key, ttl_seconds=3600)

def _set_cache(self, key, value):
    self.cache.set("market_data", key, value, ttl_seconds=3600, source="yfinance")
"""

# ============================================================================
# INTEGRACIÓN DE ASYNC OPERATIONS
# ============================================================================
# Para operaciones con múltiples tickers:

ASYNC_INTEGRATION = """
# ANTES (secuencial):
def obtener_multiples(self, tickers):
    resultados = {}
    for ticker in tickers:
        resultados[ticker] = self.obtener_datos_actuales(ticker)
    return resultados

# DESPUÉS (batching + async):
from async_ops import AsyncDataBatcher

async def obtener_multiples(self, tickers):
    batcher = AsyncDataBatcher(batch_size=100)
    
    async def fetch_fn(batch):
        resultados = {}
        for ticker in batch:
            data = self.obtener_datos_actuales(ticker)
            resultados[ticker] = data
        return resultados
    
    return await batcher.batch_fetch_prices(tickers, fetch_fn)
"""

# ============================================================================
# INTEGRACIÓN DE LOGGING
# ============================================================================
# Reemplazar print/logger.info con structured logging:

LOGGING_INTEGRATION = """
# ANTES:
self.logger = logging.getLogger("MarketDataManager")
self.logger.info("Obteniendo datos de %s", ticker)

# DESPUÉS:
from logging_audit import AuditLogger, setup_centralized_logging

# En main/__init__.py:
setup_centralized_logging("BotAnalyst", "INFO")

# En cada módulo:
self.audit = AuditLogger("market_data")
self.audit.log_data_fetch(
    identifier=ticker,
    source="yfinance",
    status="success",
    records=1,
    duration_ms=234.5
)
"""

# ============================================================================
# TESTING DE INTEGRACIÓN
# ============================================================================

TEST_PLAN = """
1. TEST_RESPONSE_SCHEMA.py
   - Verificar UnifiedResponse se crea correctamente
   - Verificar PriceData se normaliza
   - Verificar timestamps UTC
   - Verificar to_dict() JSON serializable

2. TEST_MARKET_DATA_INTEGRATED.py
   - Obtener precio con nueva UnifiedResponse
   - Verificar cache.get/set funciona
   - Verificar audit log se registra
   - Comparar performance antes/después

3. TEST_UNIFIED_CACHE.py
   - Guardar/obtener precios
   - Verificar TTL expiry
   - Verificar persistencia BD
   - Verificar hit rate

4. TEST_ASYNC_OPERATIONS.py
   - Batch 100 tickers
   - Comparar: secuencial vs batching
   - Medir latencia
   - Verificar resultados consistentes

5. TEST_STRUCTURED_LOGGING.py
   - Verificar JSON logs se crean
   - Parsear con jq
   - Verificar audit events
   - Verificar performance percentiles
"""

# ============================================================================
# ORDEN DE IMPLEMENTACIÓN
# ============================================================================

ORDER = """
SEMANA 1 (HOJE):
  1. ✅ Crear archivos de infraestructura (HECHO)
  2. → Integración PUNTO 4 (Consistencia)
     - Actualizar market_data.py → UnifiedResponse(PriceData)
     - Actualizar macroeconomic_data.py → UnifiedResponse(MacroData)
  3. → Integración PUNTO 5 (Performance)
     - Integrar cache centralizado en market_data
     - Integrar AsyncDataBatcher para múltiples tickers
  4. → Integración PUNTO 6 (Logs)
     - Integrar AuditLogger en módulos

SEMANA 2:
  5. → Integración analyzer.py y ml_predictor.py
  6. → Testing exhaustivo
  7. → Benchmarks before/after
  8. → Fix de bugs encontrados

SEMANA 3:
  9. → Stress testing (1000+ tickers)
  10. → Performance tuning
  11. → Validación compliance

SEMANA 4:
  12. → Documentación final
  13. → Deployment checklist
  14. → Production release
"""

print("PLAN DE INTEGRACIÓN CREADO")
print("=" * 80)
print(ORDER)
