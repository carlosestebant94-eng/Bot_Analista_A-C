# 📊 FUENTES DE DATOS EN TIEMPO REAL - Bot Analista A&C

## Estado Actual: GAPS DE DATOS

El bot **actualmente NO tiene acceso a datos de precios en tiempo real**. 

### ❌ Lo que FALTA:
- Precios históricos (OHLCV)
- Datos de volumen
- Indicadores técnicos calculados
- Datos fundamentales (P/E, Market Cap, etc)
- Contexto macro (SPY, VIX, etc)
- Transacciones de insiders

### ✅ Lo que SÍ tiene:
- Gemini AI para razonamiento
- Base de datos SQLite3 para conocimiento
- Framework para procesar datos

---

## 🔧 OPCIONES RECOMENDADAS (de menor a mayor costo)

### OPCIÓN 1: YFINANCE (GRATUITA - RECOMENDADA PARA EMPEZAR)
**Costo:** Gratuito
**Límite:** ~2000 req/hora
**Ideal para:** Testing, desarrollo, bots personales

```python
import yfinance as yf
import pandas as pd

# Descargar datos históricos
stock = yf.Ticker("AAPL")
hist = stock.history(period="1y")  # 1 año de datos
info = stock.info  # Información fundamental

# Acceso a datos
print(hist[['Open', 'High', 'Low', 'Close', 'Volume']])
print(f"P/E: {info.get('trailingPE')}")
print(f"Market Cap: {info.get('marketCap')}")
```

**Ventajas:**
- Sin API key requerida
- Datos precisos (source: Yahoo Finance)
- Soporta múltiples mercados (NYSE, NASDAQ, crypto, etc)
- Información fundamental incluida

**Desventajas:**
- Retraso de ~20 minutos
- No es ideal para trading en vivo
- A veces tiene delays en respuesta

**Implementación en bot:**
```bash
pip install yfinance
```

---

### OPCIÓN 2: POLYGON.IO (FREEMIUM - RECOMENDADA PARA PRODUCCIÓN)
**Costo:** Gratuito hasta $250/mes de límites, luego pago
**Límite:** 5 req/minuto (free tier)
**Ideal para:** Producción con datos precisos

```python
import requests
from datetime import datetime, timedelta

API_KEY = "tu_polygon_api_key"

# Últimas barras (minuto actual)
url = f"https://api.polygon.io/v3/ags/ticker/AAPL/range/1/minute?timespan=minute&apiKey={API_KEY}"
resp = requests.get(url)
datos = resp.json()

# Múltiples timeframes
def obtener_datos(ticker, timespan="hour", limit=100):
    url = f"https://api.polygon.io/v3/ags/ticker/{ticker}/range/1/{timespan}?limit={limit}&apiKey={API_KEY}"
    return requests.get(url).json()
```

**Ventajas:**
- Datos muy precisos
- Múltiples timeframes
- Soporte técnico profesional
- Plan gratuito generoso

**Desventajas:**
- Límite de 5 req/min (free)
- Después requiere pago
- Setup más complejo

**Obtener API Key:**
1. Ir a https://polygon.io
2. Sign up (gratuito)
3. Copiar API key del dashboard

---

### OPCIÓN 3: ALPACA MARKETS (GRATUITA + TRADING)
**Costo:** Gratuito
**Límite:** Real-time si tienes cuenta
**Ideal para:** Integración con ejecución de órdenes

```python
from alpaca_trade_api.rest import REST

# Configurar
api = REST('api_key', 'secret_key')

# Obtener barras
barras = api.get_barset('AAPL', 'minute', limit=100)

# Información de posiciones
posiciones = api.list_positions()

# Enviar orden (si tienes cuenta)
api.submit_order(
    symbol='AAPL',
    qty=10,
    side='buy',
    type='market',
    time_in_force='day'
)
```

**Ventajas:**
- Datos reales
- Integración con trading real
- Historial de transacciones
- Gratuito

**Desventajas:**
- Requiere cuenta con depósito
- API más compleja
- Mejor para brokers

---

### OPCIÓN 4: ALPHA VANTAGE (GRATUITA - BUENA COBERTURA)
**Costo:** Gratuito (5 req/min), Premium $200/mes
**Datos:** Técnicos + Fundamentales completos
**Ideal para:** Análisis fundamental integrado

```python
import requests

API_KEY = "tu_alpha_vantage_key"

# Datos técnicos
url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey={API_KEY}"
datos_tecnicos = requests.get(url).json()

# Datos fundamentales
url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol=AAPL&apikey={API_KEY}"
datos_fundamentales = requests.get(url).json()
```

**Ventajas:**
- Datos fundamentales completos
- Múltiples indicadores técnicos
- Criptodivisas soportadas

**Desventajas:**
- Retraso de ~20 minutos
- Límite 5 req/min (free)
- Documentación menos clara

---

### OPCIÓN 5: IEXCLOUD (PREMIUM - EXCELENTE DATOS FUNDAMENTALES)
**Costo:** $9/mes (starter)
**Datos:** Muy completos y actualizados
**Ideal para:** Fondos, análisis fundamental profesional

```python
import requests

TOKEN = "tu_iexcloud_token"

# Cotización en tiempo real
url = f"https://cloud.iexapis.com/stable/data/CORE/QUOTE/AAPL?token={TOKEN}"
cotizacion = requests.get(url).json()

# Datos fundamentales extensos
url = f"https://cloud.iexapis.com/stable/data/core/FUNDAMENTALS/AAPL?token={TOKEN}"
fundamentales = requests.get(url).json()
```

---

### OPCIÓN 6: TRADINGVIEW (MEJOR INDICADORES)
**Costo:** Freemium (datos gratis, API pago)
**Datos:** Indicadores pre-calculados
**Ideal para:** Si necesitas indicadores complejos

```python
# via unofficial API (riesgo de cambios)
import requests

def obtener_datos_tradingview(ticker):
    url = f"https://scanner.tradingview.com/america/scan"
    data = {
        "symbols": {
            "query": {"types": ["stock"]},
            "tickers": [ticker]
        },
        "columns": ["close", "volume", "change", "change_abs"]
    }
    return requests.post(url, json=data).json()
```

---

## 🚀 RECOMENDACIÓN PARA TU BOT

### FASE 1: DESARROLLO (AHORA)
```python
# requirements.txt
yfinance              # Datos gratis
pandas                # Análisis
numpy                 # Cálculos
ta-lib OR ta          # Indicadores técnicos
```

**Por qué:**
- ✅ Gratuito
- ✅ Sin API key compleja
- ✅ Suficiente para testing
- ✅ Rápido de implementar

---

### FASE 2: PRODUCCIÓN (RECOMENDADA)
```python
# Usar Polygon.io + Yfinance como fallback
polygon_io=True    # Datos precisos
yfinance=True      # Backup + fundamentales
```

**Por qué:**
- ✅ Datos precisos
- ✅ Plan gratuito generoso ($250/mes uso)
- ✅ Profesional
- ✅ Mejor que yfinance

---

## 📝 IMPLEMENTACIÓN PROPUESTA

Crear archivo `data_sources/market_data.py`:

```python
"""
Gestor unificado de fuentes de datos
Intenta Polygon.io → Yfinance → Alpha Vantage (fallback)
"""

class MarketDataManager:
    def __init__(self):
        self.providers = {
            'polygon': None,    # Polygon.io API
            'yfinance': None,   # yfinance
            'alpha': None       # Alpha Vantage
        }
    
    def obtener_cotizacion(self, ticker: str):
        """Obtiene precio actual"""
        try:
            return self._obtener_polygon(ticker)
        except:
            try:
                return self._obtener_yfinance(ticker)
            except:
                return self._obtener_alpha(ticker)
    
    def obtener_historico(self, ticker: str, dias: int = 250):
        """Obtiene datos históricos (1 año)"""
        # Implementación con Polygon como principal
        pass
    
    def obtener_fundamentales(self, ticker: str):
        """Obtiene P/E, Market Cap, etc"""
        # Implementación con Alpha Vantage
        pass
    
    def calcular_indicadores(self, datos):
        """Calcula RSI, MACD, Stochastic"""
        # Aquí van las fórmulas de Doc 3
        pass
```

---

## ⚡ ALTERNATIVA RÁPIDA: USAR GEMINI PARA OBTENER DATOS

**Opción ultra-rápida (sin APIs adicionales):**

```python
def obtener_datos_via_gemini(ticker: str):
    """
    Usa Gemini como fuente de datos
    ⚠️ NO RECOMENDADO para datos críticos
    """
    prompt = f"""
Proporciona los datos ACTUALES de {ticker}:
- Precio actual
- Máximo/Mínimo (52 semanas)
- P/E Ratio
- Market Cap
- Volumen promedio
- RSI (14)
- MACD
- Cambio % (día)

Formatea como JSON.
    """
    respuesta = self.ai_engine.razonar(prompt)
    return json.loads(respuesta['respuesta'])
```

**Problemas:**
- ❌ Gemini NO tiene datos en vivo
- ❌ Gemini da datos genéricos del conocimiento entrenado
- ❌ NO es confiable para trading

---

## 📋 CHECKLIST: QUÉ ELEGIR

| Necesidad | Recomendación | Costo |
|-----------|---------------|-------|
| Testing local | YFinance | Gratis |
| Bot personal 24/7 | Polygon.io free | Gratis |
| Análisis avanzado | Alpha Vantage | Gratis |
| Producción profesional | Polygon.io + IEXCloud | $9-50/mes |
| Trading automático | Alpaca Markets | Gratis (con broker) |
| Máxima precisión | IEXCloud + Polygon | $50-200/mes |

---

## 🎯 MI RECOMENDACIÓN FINAL

**Para tu bot AHORA:**
1. Implementar **YFinance** (5 minutos, gratuito)
2. Calcular indicadores con **ta-lib** o **ta** (fórmulas Doc 3)
3. Una vez funcione → migar a **Polygon.io** (mejor, profesional)

**Inicio rápido (hoy):**
```bash
pip install yfinance ta pandas
```

Luego crear `analisis/analysis_methodology.py` que:
1. ✅ Obtiene datos de YFinance
2. ✅ Calcula indicadores (RSI, MACD, Stochastic)
3. ✅ Aplica lógica Alexander (Doc 1-2)
4. ✅ Genera reporte (Doc 2 formato)

---

## ❓ PREGUNTAS FINALES

**¿Necesitas:**
- ✅ Trading en vivo (ejecutar órdenes)?
- ✅ Datos de cripto también?
- ✅ Latencia mínima (<1 segundo)?
- ✅ Múltiples mercados (NYSE, NASDAQ, etc)?

**Responde y ajusto la recomendación** 👆

