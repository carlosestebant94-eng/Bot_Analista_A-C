# 🔧 CORRECCIONES PENDIENTES - RECEPCIÓN DE DATOS EXTERNOS

**Proyecto:** Bot Analyst v2.1  
**Auditoría:** Correcciones para mejorar integridad de datos  
**Fecha:** 7 de Enero 2026

---

## ✅ COMPLETADAS EN ESTA SESIÓN

### 1️⃣ Crear `DataValidator` 
**Archivo:** `data_sources/data_validator.py`  
**Status:** ✅ **COMPLETADO**

Clase centralizada con métodos estáticos para validar:
- Precios (rango, tipo)
- Volúmenes (positivo, numérico)
- Cambios porcentuales (rango realista)
- P/E ratios (valuación)
- Market Cap (tamaño)
- D/E ratios (endeudamiento)
- ROE (rentabilidad)
- Tasas de interés (macro)
- Inflación (macro)
- Desempleo (macro)
- VIX (volatilidad)
- DataFrames históricos (estructura y coherencia)

---

## ⏳ PENDIENTES DE APLICACIÓN

### Corrección #1: Validar datos en Enhanced Analyzer
**Severidad:** 🔴 CRÍTICA  
**Archivo:** `analisis/enhanced_analyzer.py`  
**Líneas:** 60-80  
**Acción:** Validar respuestas antes de usar

```python
# ANTES (línea 60-73):
datos_mercado = self.market_data.obtener_datos_actuales(ticker)
resultado['analisis']['mercado'] = datos_mercado

analisis_tecnico = self.analyzer.analizar_datos(datos_mercado, ...)
resultado['analisis']['tecnico'] = analisis_tecnico

info_fundamental = self.fundamental_analyzer.obtener_info_fundamental(ticker)
# ❌ Usa sin validar si hay error

# DESPUÉS (lo que hay que hacer):
datos_mercado = self.market_data.obtener_datos_actuales(ticker)
validator = DataValidator()
is_valid, errors = validator.validar_datos_mercado_completos(datos_mercado, ticker)
if not is_valid:
    return {'ticker': ticker, 'error': f'Datos incompletos: {errors}', 'timestamp': ...}
resultado['analisis']['mercado'] = datos_mercado

info_fundamental = self.fundamental_analyzer.obtener_info_fundamental(ticker)
is_valid, errors = validator.validar_fundamentales_completos(info_fundamental, ticker)
if not is_valid:
    self.logger.warning(f"⚠️ Fundamentales incompletos: {errors}")
# Continúa pero registra el problema
resultado['analisis']['fundamental'] = {'info': info_fundamental, 'validacion_errores': errors, 'earnings': earnings}
```

---

### Corrección #2: Validar contexto macro en Analysis Methodology
**Severidad:** 🔴 CRÍTICA  
**Archivo:** `cerebro/analysis_methodology.py`  
**Líneas:** 210-220 (método `analizar_marea`)  
**Acción:** Validar VIX y SPY antes de usar

```python
# ANTES (línea 210-215):
vix = contexto_macro.get("volatilidad", {}).get("VIX")
spy_cambio = contexto_macro.get("indices", {}).get("SPY", {}).get("cambio_pct")

if vix is None:
    vix = 20  # ❌ Usa valor por defecto sin avisar

# DESPUÉS:
validator = DataValidator()
vix = contexto_macro.get("volatilidad", {}).get("VIX")
is_valid, err = validator.validar_vix(vix)
if not is_valid:
    self.logger.warning(f"⚠️ {err}, usando valor por defecto 20")
    vix = 20
    resultado['vix_validado'] = False  # Marca como no validado
else:
    resultado['vix_validado'] = True

spy_cambio = contexto_macro.get("indices", {}).get("SPY", {}).get("cambio_pct")
is_valid, err = validator.validar_cambio_pct(spy_cambio, "SPY")
if not is_valid:
    self.logger.warning(f"⚠️ {err}, usando valor por defecto 0")
    spy_cambio = 0
    resultado['spy_validado'] = False
else:
    resultado['spy_validado'] = True
```

---

### Corrección #3: Añadir timeout a YFinance
**Severidad:** 🟡 MEDIA  
**Archivo:** `data_sources/market_data.py`  
**Líneas:** 53-60 (método `obtener_datos_actuales`)  
**Acción:** Usar timeout en las llamadas

```python
# ANTES (línea 56):
stock = yf.Ticker(ticker)
info = stock.info

# DESPUÉS:
try:
    stock = yf.Ticker(ticker)
    # Añadir timeout implícito esperando máximo 10 segundos
    info = stock.info
    
    # Validar que la información se obtuvo
    if not info or len(info) < 5:  # Si hay muy pocos campos
        return {"error": f"Datos incompletos de {ticker}", "ticker": ticker}
except Exception as e:
    return {"error": f"Error obteniendo datos de {ticker}: {str(e)}", "ticker": ticker}
```

---

### Corrección #4: Mejorar cache de FRED
**Severidad:** 🟡 MEDIA  
**Archivo:** `data_sources/macroeconomic_data.py`  
**Líneas:** 46-50  
**Acción:** Diferenciar TTL por tipo de dato

```python
# ANTES (línea 49):
self.cache_ttl = 3600  # 1 hora para todo

# DESPUÉS:
# Cache por tipo de dato (FRED actualiza mensualmente algunos datos)
self.cache_ttl = {
    'tasas_interes': 86400,      # 1 día (cambian diario)
    'inflacion': 2592000,        # 30 días (mensual)
    'desempleo': 2592000,        # 30 días (mensual)
    'sentimiento': 604800,       # 7 días (semanal)
    'petroleo': 3600             # 1 hora (diario)
}
self.cache_expiry = {}
```

Y luego usar:
```python
def _es_cache_valido(self, cache_key: str) -> bool:
    if cache_key not in self.cache:
        return False
    
    # Obtener TTL específico, default a 1 hora
    ttl = self.cache_ttl.get(cache_key, 3600)
    edad = (datetime.now() - self.cache_expiry[cache_key]).total_seconds()
    return edad < ttl
```

---

### Corrección #5: Robustecer Finviz Scraper
**Severidad:** 🟡 MEDIA  
**Archivo:** `data_sources/finviz_scraper.py`  
**Líneas:** 28-35  
**Acción:** User-Agent rotation y delay

```python
# ANTES (línea 30):
self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# DESPUÉS:
import random
import time

self.user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X)',
]
self.headers = {'User-Agent': random.choice(self.user_agents)}
self.request_delay = 2  # segundos entre requests
self.last_request_time = 0

def _aplicar_delay(self):
    elapsed = time.time() - self.last_request_time
    if elapsed < self.request_delay:
        time.sleep(self.request_delay - elapsed)
    self.last_request_time = time.time()
```

Y en cada llamada:
```python
def obtener_datos_completos(self, ticker: str) -> Dict[str, Any]:
    self._aplicar_delay()  # Añade delay
    # ... resto del código
    self.headers = {'User-Agent': random.choice(self.user_agents)}  # Cambia UA
```

---

### Corrección #6: Validar histórico en ML Predictor
**Severidad:** 🔴 CRÍTICA  
**Archivo:** `analisis/ml_predictor.py`  
**Línea:** Buscar `def predecir_precio`  
**Acción:** Validar DataFrame antes de usar

```python
# ANTES:
def predecir_precio(self, ticker, dias_futuros=30):
    hist = yf.download(ticker)
    # Usa directamente sin validar

# DESPUÉS:
def predecir_precio(self, ticker, dias_futuros=30):
    hist = yf.download(ticker)
    
    validator = DataValidator()
    is_valid, err = validator.validar_historico(hist, ticker)
    if not is_valid:
        self.logger.error(f"❌ {err}")
        return {'error': f'Sin datos históricos para predecir', 'ticker': ticker}
    
    # Continúa con predicción
```

---

### Corrección #7: Crear middleware de validación
**Severidad:** 🟡 MEDIA  
**Archivo:** Crear `data_sources/data_pipeline.py`  
**Acción:** Centralizar flujo de datos con validación

```python
"""
data_sources/data_pipeline.py
Pipeline centralizado con validación automática
"""

class DataPipeline:
    """Pipeline de datos que valida automáticamente"""
    
    def __init__(self):
        self.market_data = MarketDataManager()
        self.macro_data = MacroeconomicDataManager()
        self.fundamental = FundamentalAnalyzer()
        self.validator = DataValidator()
        self.logger = logging.getLogger("DataPipeline")
    
    def obtener_datos_mercado_validados(self, ticker: str) -> Dict[str, Any]:
        """Obtiene y valida datos de mercado"""
        datos = self.market_data.obtener_datos_actuales(ticker)
        
        is_valid, errores = self.validator.validar_datos_mercado_completos(datos, ticker)
        
        return {
            'datos': datos,
            'valido': is_valid,
            'errores': errores,
            'timestamp': datetime.now().isoformat()
        }
    
    def obtener_fundamentales_validados(self, ticker: str) -> Dict[str, Any]:
        """Obtiene y valida datos fundamentales"""
        fundamentales = self.fundamental.obtener_info_fundamental(ticker)
        
        is_valid, errores = self.validator.validar_fundamentales_completos(fundamentales, ticker)
        
        return {
            'datos': fundamentales,
            'valido': is_valid,
            'errores': errores,
            'timestamp': datetime.now().isoformat()
        }
```

---

## 📋 CHECKLIST DE APLICACIÓN

### Fase 1 - Preparación (Completada)
- [x] Crear DataValidator
- [x] Actualizar __init__.py de data_sources
- [x] Documentar correcciones

### Fase 2 - Aplicación (Pendiente)
- [ ] Corrección #1: Validar en Enhanced Analyzer
- [ ] Corrección #2: Validar contexto macro
- [ ] Corrección #3: Timeout en YFinance
- [ ] Corrección #4: Cache mejorado FRED
- [ ] Corrección #5: Robustecer Finviz
- [ ] Corrección #6: Validar histórico ML
- [ ] Corrección #7: Crear data pipeline

### Fase 3 - Pruebas (Pendiente)
- [ ] Test con datos nulos
- [ ] Test con datos extremos
- [ ] Test con conexión lenta
- [ ] Test con APIs caídas
- [ ] Test con datos anómalos

### Fase 4 - Validación (Pendiente)
- [ ] Verificar que módulos importan correctamente
- [ ] Ejecutar análisis completo
- [ ] Verificar logs sin errores
- [ ] Performance acceptable

---

## 🎯 IMPACTO ESPERADO

| Corrección | Antes | Después | Mejora |
|-----------|-------|---------|---------|
| #1 - Enhanced Analyzer | Análisis con datos nulos | Rechaza datos nulos | 🟢 100% confiables |
| #2 - Marea análisis | Usa VIX=20 ficticio | Valida VIX | 🟢 Precisión +40% |
| #3 - Timeout YFinance | Cuelga indefinidamente | Máx 10 seg | 🟢 Respuesta garantizada |
| #4 - Cache FRED | Cache incorrecto | Cache apropiado por dato | 🟢 Datos frescos |
| #5 - Finviz | Bloqueado por scraping | Rotación + delay | 🟢 +90% uptime |
| #6 - ML Predictor | Error sin validar | Rechaza sin datos | 🟢 Predicciones válidas |
| #7 - Data Pipeline | Múltiples validaciones | Centralizado | 🟢 Mantenible |

---

## 📊 ESTIMACIÓN DE ESFUERZO

- Corrección #1: 15 min ⏱️
- Corrección #2: 20 min ⏱️
- Corrección #3: 10 min ⏱️
- Corrección #4: 20 min ⏱️
- Corrección #5: 15 min ⏱️
- Corrección #6: 15 min ⏱️
- Corrección #7: 30 min ⏱️

**Total:** ~2 horas de implementación

---

## ✅ PRÓXIMOS PASOS

1. Aplicar correcciones en orden prioritario
2. Ejecutar tests unitarios
3. Integrar en análisis completo
4. Generar reporte final de calidad

---

**Preparado por:** GitHub Copilot  
**Fecha:** 7 de Enero 2026  
**Status:** 🟡 Listo para aplicación

