# 📊 FINVIZ.COM COMO FUENTE DE DATOS

## ✅ SÍ, Se puede usar Finviz

Finviz es **excelente** para obtener datos que YFinance no tiene o tiene con retraso.

---

## 📈 DATOS QUE OFRECE FINVIZ

### 1. DATOS TÉCNICOS (¡No requiere API key!)
```
• Precio actual
• Cambio % día
• Volumen
• P/E Ratio
• Market Cap
• Dividend Yield
• 52 Week High/Low
• RSI
• SMA (20, 50, 200)
• 200-Day Moving Average
```

### 2. DATOS FUNDAMENTALES
```
• P/E, PEG, P/B, P/S
• ROE, ROA
• Debt/Equity
• Revenue
• Earnings Growth
• Dividend Payout
```

### 3. SENTIMIENTO DEL MERCADO (¡Muy útil!)
```
• Insider Trading (Compras/Ventas)
• Institutional Ownership
• Short Float %
• Analyst Rating (Fuerte Compra/Compra/Mantener/Venta)
• Target Price
• News Headlines
• Social Sentiment
```

### 4. DATOS DE SCREENING
```
• IPO Info
• Sector/Industry
• Market Rank
• Earnings Dates
• Earnings Surprises
• Relative Strength (vs Sector)
```

---

## 🔧 IMPLEMENTACIÓN (3 OPCIONES)

### OPCIÓN 1: PYTHON-FINVIZ (RECOMENDADA - Más fácil)
```bash
pip install finviz
```

**Uso simple:**
```python
from finviz.screener import Screener

# Obtener datos de un stock
stock = Screener("AAPL")
print(stock.price)           # Precio
print(stock.pe)              # P/E Ratio
print(stock.rsi)             # RSI
print(stock.insider_buy)      # Compras de insiders
print(stock.analyst_rating)   # Rating analistas
```

### OPCIÓN 2: YFINANCE + FINVIZ COMBO (MEJOR COBERTURA)
```python
import yfinance as yf
from finviz.screener import Screener

# Datos YFinance
yf_data = yf.Ticker("AAPL")

# Datos Finviz
fv_data = Screener("AAPL")

# Combinar ambos
datos_completos = {
    "precio_yf": yf_data.info["currentPrice"],
    "rsi_fv": fv_data.rsi,
    "insider_buying_fv": fv_data.insider_buy,
    "pe_yf": yf_data.info["trailingPE"]
}
```

### OPCIÓN 3: WEB SCRAPING DIRECTO (Más control)
```python
import requests
from bs4 import BeautifulSoup

url = f"https://finviz.com/quote.ashx?t=AAPL"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extraer datos específicos
# (requiere análisis HTML)
```

---

## ⚡ VENTAJAS DE FINVIZ vs YFINANCE

| Característica | YFinance | Finviz | Winner |
|---|---|---|---|
| **Precio en vivo** | 20 min retraso | En vivo | Finviz ✅ |
| **Insider Trading** | ❌ | ✅ | Finviz ✅ |
| **Analyst Rating** | Limited | Completo | Finviz ✅ |
| **Social Sentiment** | ❌ | ✅ | Finviz ✅ |
| **Datos históricos** | ✅ | ❌ | YFinance ✅ |
| **Sin API Key** | ✅ | ✅ | Ambos ✅ |
| **Velocidad** | Rápido | Muy rápido | Finviz ✅ |

---

## 🎯 INTEGRACIÓN RECOMENDADA PARA TU BOT

Agregar Finviz a tu `MarketDataManager`:

```python
def obtener_datos_finviz(self, ticker: str) -> Dict[str, Any]:
    """Datos adicionales de Finviz para análisis más completo"""
    try:
        from finviz.screener import Screener
        fv = Screener(ticker)
        
        return {
            "rsi_finviz": fv.rsi,
            "insider_buy": fv.insider_buy,
            "insider_sell": fv.insider_sell,
            "analyst_rating": fv.analyst_rating,
            "target_price": fv.price_target,
            "52_week_high": fv.week_52_high,
            "52_week_low": fv.week_52_low,
            "short_float": fv.short_float,
            "short_ratio": fv.short_ratio,
            "relative_strength": fv.relative_strength
        }
    except Exception as e:
        self.logger.warning(f"Error obteniendo datos Finviz: {e}")
        return {}
```

---

## 📋 CHECKLIST DE INSTALACIÓN

```bash
# 1. Instalar Finviz
pip install finviz

# 2. Instalar dependencias
pip install requests beautifulsoup4

# 3. Test rápido
python -c "from finviz.screener import Screener; s = Screener('AAPL'); print(s.price)"
```

---

## ⚠️ LIMITACIONES DE FINVIZ

- ❌ Finviz **no tiene datos históricos** (OHLCV)
- ❌ No permite **acceso a API oficial** (web scraping)
- ⚠️ Puede tener **throttling** si haces muchas solicitudes rápido
- ⚠️ Formato HTML cambia ocasionalmente (puede romper scraper)

**Solución:** Usar **Finviz + YFinance** juntos:
- YFinance → Datos históricos, OHLCV, cálculos
- Finviz → Datos en vivo, insider, sentimiento, analyst

---

## 🚀 MI RECOMENDACIÓN PARA TU BOT

**Crear estructura con 2 capas:**

```python
class MarketDataManager:
    
    def obtener_datos_completos(self, ticker: str):
        """Combina YFinance + Finviz para máxima información"""
        
        # Capa 1: YFinance (histórico + fundamentos)
        yf_datos = self.obtener_historico(ticker)
        yf_fundamentales = self.obtener_fundamentales(ticker)
        
        # Capa 2: Finviz (en vivo + sentimiento + insider)
        fv_datos = self.obtener_datos_finviz(ticker)
        
        # Merge
        return {
            "yfinance": yf_datos,
            "finviz": fv_datos,
            "analisis_completo": {
                "insider_buying": fv_datos.get("insider_buy"),
                "analyst_rating": fv_datos.get("analyst_rating"),
                "target_price": fv_datos.get("target_price")
            }
        }
```

---

## ✅ DECISIÓN

**¿Agregar Finviz a tu bot?**

| Escenario | Recomendación |
|-----------|---------------|
| Solo análisis técnico | YFinance solo está bien |
| Incluir sentimiento/insider | Agregar Finviz ✅ |
| Máxima información profesional | YFinance + Finviz combo ✅ |

**Mi sugerencia:** Agregar Finviz como **capa opcional** en `MarketDataManager` para enriquecer el análisis Alexander con datos de insider + analyst rating.

---

¿Quieres que **integre Finviz** en el `MarketDataManager` para que el bot tenga acceso a:
- Insider trading data
- Analyst ratings
- Sentiment scores
- Target prices

?

