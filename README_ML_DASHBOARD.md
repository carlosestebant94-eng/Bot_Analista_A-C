# 🚀 INICIO RÁPIDO: ML + DASHBOARD

## Paso 1: Instalar dependencias
```bash
pip install flask flask-cors scikit-learn
```

## Paso 2: Iniciar Dashboard
```bash
python scripts/start_dashboard.py
```

Verás:
```
✅ Backend iniciado en http://localhost:5000
🤖 Iniciando entrenamiento de modelos en background...
📥 Descargando datos históricos...
```

## Paso 3: Abrir Dashboard
Abre el navegador en: **http://localhost:5000**

## Paso 4: Usar el Dashboard

### 📊 Analizar un Ticker
```
1. Escribir: AAPL
2. Click: "🔍 Analizar"
3. Ver resultados en vivo con ML predictions
```

### 🤖 Entrenar Modelos (opcional)
```
1. Click: "🤖 Entrenar ML"
2. Esperar 2-5 minutos
3. Modelos listos para predicciones precisas
```

### ⚖️ Comparar Tickers
```
1. Click: "⚖️ Comparar"
2. Ingresar: AAPL,MSFT,GOOGL
3. Ver tabla comparativa ordenada por score
```

---

## 📋 Qué Incluye

### Machine Learning (Paso 2)
- ✅ 4 modelos de predicción entrenables
- ✅ Predicción de dirección de precio (ALCISTA/BAJISTA)
- ✅ Predicción de volatilidad (BAJA/MEDIA/ALTA)
- ✅ Predicción de confianza de recomendación
- ✅ Análisis de accuracy de analistas

### Web Dashboard (Paso 4)
- ✅ Interfaz responsive (Desktop/Tablet/Mobile)
- ✅ Gráficos interactivos con Plotly
- ✅ Análisis en tiempo real
- ✅ Integración con Finviz
- ✅ Histórico de análisis
- ✅ Comparador de tickers
- ✅ 7 API endpoints REST

---

## 🔍 Validación

Todos los tests pasaron:
```
✅ TEST 1: ML Predictor Básico
✅ TEST 2: Extracción de Features  
✅ TEST 3: Predicciones ML
✅ TEST 4: Flask App Básico
✅ TEST 5: API Endpoints
✅ TEST 6: Dashboard HTML
✅ TEST 7: Start Script

Total: 7/7 tests ✅ PASADOS
```

Ejecutar tests: `python test_ml_dashboard.py`

---

## 📚 Documentación Completa

Ver: **ML_DASHBOARD_COMPLETED.md**

---

## ✨ Casos de Uso

### 1. Trader Activo
```
Usa el dashboard para análisis rápido
Combina ML predictions + análisis técnico
Toma decisiones más informadas
```

### 2. Inversor Long-term
```
Entrena ML con datos históricos
Analiza tendencias a largo plazo
Recibe recomendaciones fundamentales
```

### 3. Bot Trader Automático
```
API /api/analyze para automatización
ML predictions integradas
Histórico para backtesting
```

---

## 🆘 Soporte

**¿No aparece el dashboard?**
- Verificar: `http://localhost:5000`
- Ver logs en terminal
- Esperar a que terminen descargas iniciales

**¿Los modelos ML no predicen?**
- Ejecutar: `python scripts/start_dashboard.py`
- Esperar entrenamiento (2-5 min)
- Modelos en carpeta `models/`

**¿Error en análisis?**
- Revisa conexión a internet
- Verifica API key de Gemini en .env
- Comprueba YFinance disponible

---

**Estado**: 🚀 LISTO PARA PRODUCCIÓN
