# 🚀 GUÍA RÁPIDA - NUEVAS FEATURES v2.1

## Inicio Rápido (5 minutos)

### 1. Instalar dependencias nuevas
```bash
pip install -r requirements.txt
```

### 2. Ejecutar tests para validar
```bash
python test_enhanced_features.py
```

**Output esperado:**
```
✅ PASSED: Datos Macroeconómicos
✅ PASSED: Análisis Fundamental
✅ PASSED: Correlaciones
✅ PASSED: Predicción ML
✅ PASSED: Enhanced Analyzer

Total: 5/5 pruebas pasadas
🎉 ¡TODAS LAS MEJORAS FUNCIONAN CORRECTAMENTE!
```

### 3. El bot sigue funcionando igual
```bash
python main.py
```

---

## 📚 Ejemplos de Uso

### Ejemplo 1: Análisis 360 Completo
```python
from analisis import EnhancedAnalyzer

analyzer = EnhancedAnalyzer()

# Análisis completo de una acción
resultado = analyzer.analizar_360("AAPL")

# Acceder a componentes
print(f"Recomendación: {resultado['recomendacion']}")
print(f"Precio actual: ${resultado['analisis']['mercado']['precio']}")
print(f"Volatilidad: {resultado['analisis']['volatilidad_riesgo']['volatilidad']}")
print(f"Predicción 30d: ${resultado['analisis']['predicciones']['corto_plazo_30d']}")
```

### Ejemplo 2: Análisis de Cartera
```python
from analisis import EnhancedAnalyzer

analyzer = EnhancedAnalyzer()

# Analizar diversificación de cartera
cartera = analyzer.analizar_cartera(["AAPL", "MSFT", "GOOGL", "AMZN"])

print(f"Puntaje diversificación: {cartera['diversificacion']['puntaje_diversificacion']}/100")
print(f"Correlación promedio: {cartera['diversificacion']['correlacion_promedio']:.2f}")
print(f"Recomendación: {cartera['diversificacion']['recomendacion']}")
```

### Ejemplo 3: Comparar Dos Acciones
```python
from analisis import EnhancedAnalyzer

analyzer = EnhancedAnalyzer()

# Comparar AAPL vs MSFT
comparativa = analyzer.comparar_activos("AAPL", "MSFT")

print(f"Ganador: {comparativa['ganador']}")
print(f"P/E Ratio AAPL: {comparativa['analisis_1']['analisis']['fundamental']['info']['valuacion']['pe_ratio']}")
print(f"P/E Ratio MSFT: {comparativa['analisis_2']['analisis']['fundamental']['info']['valuacion']['pe_ratio']}")
```

### Ejemplo 4: Datos Macroeconómicos
```python
from data_sources import MacroeconomicDataManager

macro = MacroeconomicDataManager()

# Obtener contexto macroeconómico actual
contexto = macro.obtener_contexto_macro_resumido()

print(f"Tasa 10Y: {contexto['tasas_interes']['10y']}%")
print(f"Desempleo: {contexto['desempleo']:.2f}%")
print(f"Inflación: {contexto['inflacion']:.2f}%")
print(f"Sentimiento: {contexto['sentimiento_consumidor']}")
```

### Ejemplo 5: Análisis Fundamental Detallado
```python
from data_sources import FundamentalAnalyzer

fundamental = FundamentalAnalyzer()

# Información fundamental
info = fundamental.obtener_info_fundamental("AAPL")

print(f"Empresa: {info['empresa']['nombre']}")
print(f"Sector: {info['empresa']['sector']}")
print(f"P/E Ratio: {info['valuacion']['pe_ratio']}")
print(f"ROE: {info['rentabilidad']['roe']:.2f}%")
print(f"Deuda/Capital: {info['endeudamiento']['ratio_deuda_capital']}")

# Comparar dos empresas
comp = fundamental.comparar_pares("AAPL", "MSFT")
print(f"\nComparación:")
print(f"AAPL P/E: {comp['empresa1']['pe_ratio']} vs MSFT: {comp['empresa2']['pe_ratio']}")
```

### Ejemplo 6: Correlaciones y Diversificación
```python
from analisis import CorrelationAnalyzer

corr = CorrelationAnalyzer()

# Calcular correlaciones
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]
resultado = corr.calcular_correlacion_activos(tickers)

print(f"Pares altamente correlacionados:")
for par in resultado['pares_altamente_correlacionados']:
    print(f"  {par[0]} - {par[1]}: {par[2]:.2f}")

# Analizar diversificación
diversificacion = corr.analizar_diversificacion(tickers)
print(f"\nScore diversificación: {diversificacion['puntaje_diversificacion']}/100")
print(f"Recomendación: {diversificacion['recomendacion']}")
```

### Ejemplo 7: Predicciones ML
```python
from analisis import MLPredictor

ml = MLPredictor()

# Predicción a 30 días
prediccion = ml.predecir_precio("AAPL", dias_futuros=30)

print(f"Precio actual: ${prediccion['precio_actual']:.2f}")
print(f"Predicción 30d: ${prediccion['predicciones']['ensemble']:.2f}")
print(f"Rango: ${prediccion['rango']['minimo']:.2f} - ${prediccion['rango']['maximo']:.2f}")
print(f"Confianza: {prediccion['confianza_ensemble']}%")
print(f"Tendencia: {prediccion['tendencia']}")

# Análisis de riesgo
riesgo = ml.analizar_riesgo_downside("AAPL")
print(f"\nRiesgo Downside:")
print(f"VaR 95%: {riesgo['riesgo_downside']['var_95']:.2f}%")
print(f"VaR 99%: {riesgo['riesgo_downside']['var_99']:.2f}%")

# Proyección a largo plazo
proyeccion = ml.proyeccion_largo_plazo("AAPL", anos=5)
print(f"\nProyección 5 años:")
print(f"Escenario base: ${proyeccion['escenarios']['base']:.2f}")
print(f"Bullish: ${proyeccion['escenarios']['bullish']:.2f}")
print(f"Bearish: ${proyeccion['escenarios']['bearish']:.2f}")
```

---

## 🔍 Módulos Disponibles

### `data_sources.MacroeconomicDataManager`
Datos macroeconómicos de FRED
- `obtener_tasa_desempleo()`
- `obtener_inflacion()`
- `obtener_tasas_interes()`
- `obtener_sentimiento_consumidor()`
- `obtener_produccion_industrial()`
- `obtener_precio_petroleo()`
- `obtener_tipo_cambio_usd_eur()`

### `data_sources.FundamentalAnalyzer`
Análisis fundamental de acciones
- `obtener_info_fundamental(ticker)`
- `obtener_reporte_earnings(ticker)`
- `obtener_balance_sheet(ticker)`
- `comparar_pares(ticker1, ticker2)`

### `analisis.CorrelationAnalyzer`
Análisis de correlaciones
- `calcular_correlacion_activos(tickers, periodo)`
- `calcular_beta(ticker, benchmark, periodo)`
- `analizar_diversificacion(tickers)`
- `detectar_contagio_sistematico(ticker, mercado)`

### `analisis.MLPredictor`
Predicciones con Machine Learning
- `predecir_precio(ticker, dias_futuros, usar_ensemble)`
- `calcular_volatilidad_implicita(ticker)`
- `analizar_riesgo_downside(ticker, dias)`
- `proyeccion_largo_plazo(ticker, anos)`

### `analisis.EnhancedAnalyzer`
Integrador central de todos los módulos
- `analizar_360(ticker)` - Análisis completo
- `analizar_cartera(tickers)` - Análisis de cartera
- `comparar_activos(ticker1, ticker2)` - Comparativa

---

## 📊 Estructura de Respuesta

### Análisis 360
```python
{
    'ticker': 'AAPL',
    'timestamp': '2024-01-07T...',
    'analisis': {
        'mercado': {...},          # Datos actuales
        'tecnico': {...},          # Análisis técnico
        'fundamental': {...},      # Datos fundamental
        'macroeconomico': {...},   # Contexto macro
        'volatilidad_riesgo': {...},  # Riesgo/volatilidad
        'predicciones': {...}      # Predicciones ML
    },
    'resumen_ejecutivo': 'Texto resumen',
    'recomendacion': '🟢 BUY / 🔴 SELL / 🟡 HOLD'
}
```

---

## 🎯 Tips y Buenas Prácticas

1. **Cachés automáticos**: Los datos se cachean automáticamente
   - Macro: 1 hora
   - Fundamental: 24 horas
   - ML: 1 hora
   - Correlaciones: 1 hora

2. **Limpiar cachés si es necesario**:
   ```python
   analyzer.limpiar_caches()
   ```

3. **Para mejor performance**:
   - Usar análisis 360 para acciones principales
   - Usar predicción simple para backtesting
   - Reutilizar objetos (no crear uno nuevo cada vez)

4. **Error handling**:
   ```python
   resultado = analyzer.analizar_360("TICKER_INVALIDO")
   if 'error' in resultado:
       print(f"Error: {resultado['error']}")
   ```

---

## 📞 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'pandas_datareader'"
**Solución**: 
```bash
pip install pandas-datareader scipy
```

### Error: "No se pueden obtener datos para TICKER"
**Causa**: Ticker inválido o sin datos en yfinance
**Solución**: Verificar que el ticker sea correcto (ej: "AAPL" no "Apple")

### Error: "Datos insuficientes"
**Causa**: No hay suficientes datos históricos
**Solución**: Usar un ticker con más historial (acciones grandes)

---

## 📖 Documentación Completa

Para más detalles:
- `MEJORAS_IMPLEMENTADAS_v2_1.md` - Detalles técnicos
- `VALIDACION_FINAL_MEJORAS.md` - Validación y testing
- `test_enhanced_features.py` - Test suite

---

**¡Disfruta las nuevas features! 🚀**
