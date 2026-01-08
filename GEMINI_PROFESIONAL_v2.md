# 🚀 AIEngine v2.0 - Gemini con Instrucción Maestra Profesional

## 📋 RESUMEN DE MEJORAS IMPLEMENTADAS

Tu bot ahora tiene un **motor IA completamente rediseñado** que garantiza respuestas **deterministas, precisas y profesionales**. Esto es lo que cambió:

---

## 🎯 CAMBIOS PRINCIPALES

### 1. **Instrucción Maestra Completa** (`INSTRUCCION_MAESTRA_PROFESIONAL`)
- ✅ Definida como constante de clase en `AIEngine`
- ✅ Se pasa directamente a `genai.GenerativeModel()` como `system_instruction`
- ✅ Garantiza que Gemini SIEMPRE siga las mismas reglas

**Reglas implementadas:**
```
ROL: Motor de Análisis Financiero Cuantitativo (NO creativo)
OBJETIVO: Determinista + Preciso + Profesional

CHAIN OF THOUGHT (Razonamiento Interno):
1. Validación de Eventos (Earnings < 5 días = ESPERA obligatorio)
2. Análisis Técnico Binario (Divergencias: presente/ausente, NO "casi presentes")
3. Fundamentales vs Sector (P/E, Valuación)
4. Factor Social (Insider, Analyst, Sentiment)
5. Scoring de Confianza (80-100%=Alto, 50-79%=Medio, <50%=Bajo)

FORMATO: Markdown estructurado con tablas
VEREDICTO: COMPRA / VENTA / ESPERA (Binario)
```

### 2. **Método Nuevo: `analizar_ticker_profesional()`**

```python
resultado = ai_engine.analizar_ticker_profesional(
    ticker="AAPL",
    datos_tecnicos={...},      # RSI, MACD, precios, soportes
    datos_fundamentales={...}, # P/E, Market Cap, ROE
    datos_macro={...},         # VIX, Fed Rate, Inflación
    contexto_conocimiento="Principios extraídos de libros"
)
```

**Genera reporte profesional con:**
- 🚦 Veredicto del algoritmo (COMPRA/VENTA/ESPERA)
- 🌊 Entorno macro y riesgo
- 🧬 Tabla técnica con análisis binario
- 💎 Fundamentales y valuación
- 👥 Factor social y sentimiento
- 🎯 Plan de acción (Entry, Stop Loss, Target)

### 3. **Temperatura Reducida para Determinismo**

| Parámetro | Antes | Ahora | Beneficio |
|-----------|-------|-------|-----------|
| Temperatura | 0.7 | 0.2-0.3 | Mayor determinismo |
| top_k | 40 | 20 | Menos variabilidad |
| top_p | 0.95 | 0.9 | Respuestas más binarias |
| max_tokens | 2000 | 3000 | Análisis más completo |

**Resultado:** Ante los mismos datos → MISMA respuesta (determinista)

### 4. **Parámetro `usar_instruccion_maestra`**

Se puede activar/desactivar según necesidad:

```python
# Modo PROFESIONAL (Instrucción Maestra + Temperatura baja)
resultado = ai_engine.razonar(
    pregunta="...",
    usar_instruccion_maestra=True,  # Análisis profesional
    temperatura=0.2
)

# Modo ESTÁNDAR (Más creativo, sin instrucción maestra)
resultado = ai_engine.razonar(
    pregunta="...",
    usar_instruccion_maestra=False,  # Más flexible
    temperatura=0.7
)
```

---

## 📊 ESTRUCTURA DEL REPORTE PROFESIONAL

Cada análisis genera un reporte Markdown estructurado:

```markdown
## 📊 REPORTE ANALÍTICO: AAPL

### 1. 🚦 VEREDICTO DEL ALGORITMO
* **Señal Maestra:** COMPRA / VENTA / ESPERA
* **Factor Determinante:** (Ej. "Anulación por Earnings próximos")
* **Nivel de Confianza:** Alto (85%)

### 2. 🌊 ENTORNO Y RIESGO (MACRO)
* **Contexto VIX/SPY:** [valores y análisis]
* **Riesgo de Evento:** [datos económicos próximos]

### 3. 🧬 ANÁLISIS TÉCNICO (HECHOS, NO OPINIONES)
| Indicador | Valor | Estado (Obj.) | Interpretación |
| Precio vs SMA | $228.55 vs $225.30 | Encima | Tendencia Alcista |
| RSI (14) | 62.5 | Neutral | Momentum alcista |
| MACD | Cruce progreso | Cruce Alcista | Señal de compra |

### 4. 💎 FUNDAMENTALES & VALOR
* **Valuación:** P/E Ratio [X] vs sector [Y] = [Caro/Justo/Barato]
* **Tesis de Inversión:** [Resumen breve]
* **Riesgos:** [2-3 riesgos específicos]

### 5. 👥 FACTOR SOCIAL & SENTIMIENTO
* **Insider Activity:** [Compras/ventas recientes]
* **Analyst Consensus:** [Ratings promedio]
* **Sentiment Score:** [Positivo/Negativo/Neutral]

### 6. 🎯 PLAN DE ACCIÓN
* **Entry Point:** $XXX
* **Stop Loss:** $XXX
* **Target Profit:** $XXX
* **Plazo:** [Corto/Medio/Largo plazo]
```

---

## 🔧 CÓMO USAR LA NUEVA VERSION

### En el Bot de Telegram

Cuando el usuario envíe `/analizar AAPL`, ahora el proceso es:

1. **MarketDataManager** obtiene datos técnicos, fundamentales, macro
2. **AIEngine.analizar_ticker_profesional()** procesa con instrucción maestra
3. **Gemini responde DETERMINISTA** = mismo análisis cada vez
4. **Reporte formateado** en Markdown profesional

### Ejemplo en código:

```python
from ia.ai_engine import AIEngine
from data_sources.market_data import MarketDataManager

# Inicializar
ai_engine = AIEngine()
market_manager = MarketDataManager()

# Obtener datos
ticker = "AAPL"
datos_tech = market_manager.obtener_datos_tecnicos(ticker)
datos_fund = market_manager.obtener_fundamentales(ticker)
datos_macro = market_manager.obtener_contexto_macro()

# Analizar PROFESIONALMENTE
resultado = ai_engine.analizar_ticker_profesional(
    ticker=ticker,
    datos_tecnicos=datos_tech,
    datos_fundamentales=datos_fund,
    datos_macro=datos_macro
)

print(resultado["respuesta"])  # Reporte profesional
```

---

## 📈 REGLAS DE ANÁLISIS BINARIO (DETERMINISTA)

### Divergencias
```
✅ DIVERGENCIA ALCISTA: Precio hace LL AND Oscilador hace HL
❌ NO es divergencia: Si no cumple ambas condiciones exactas
```

### Sobreventa/Sobrecompra
```
RSI < 30  = SOBREVENTA (Posible rebote)
RSI > 70  = SOBRECOMPRA (Posible corrección)
RSI 30-70 = NEUTRAL (Sin extremo)
```

### Earnings
```
Earnings < 5 días = ESPERA OBLIGATORIO
(Anula cualquier señal técnica alcista o bajista)
```

### Análisis Técnico vs Fundamental
```
3+ confirmaciones = Confianza ALTA (80-100%)
2 confirmaciones = Confianza MEDIA (50-79%)
1 confirmación = Confianza BAJA (20-49%)
Contradicciones = Muy Baja (<20%)
```

---

## 🎯 VENTAJAS DEL NUEVO SISTEMA

| Aspecto | Antes | Ahora |
|--------|-------|-------|
| **Determinismo** | Baja (Temp 0.7) | Alta (Temp 0.2-0.3) |
| **Formato** | Texto libre | Markdown estructurado |
| **Veredicto** | Ambiguo | Binario (COMPRA/VENTA/ESPERA) |
| **Confianza** | No explícita | 80%/50%/20% categorizadas |
| **Tabla Técnica** | No | Sí, con valores objetivos |
| **Plan de Acción** | Sugerencias | Entry/Stop/Target precisos |
| **Chain of Thought** | Implícito | Explícito en instrucción |
| **Validación de Eventos** | No | Sí (Earnings, Fed, etc) |

---

## ⚠️ LIMITACIONES Y CONSIDERACIONES

### 1. **Cuota de API Gemini**
- Modelo `gemini-2.5-pro`: 2 solicitudes/minuto (gratuito)
- Solución: Usar `gemini-1.5-flash` (más rápido, menos cuota)
- Plan pago: Acceso ilimitado

### 2. **Temperatura y Creatividad**
- **Temp 0.2** = Determinista pero menos flexible
- **Temp 0.7** = Más flexible pero menos consistente
- **Recomendación**: Usar 0.2-0.3 para análisis profesional

### 3. **Datos de Entrada**
- Precisión = Precisión del análisis
- Si no proporcionas Earnings próximos, Gemini no puede aplicar regla
- Siempre incluir contexto completo

---

## 📝 ARCHIVOS MODIFICADOS

### ✅ `ia/ai_engine.py` (ACTUALIZADO)
- Añadida `INSTRUCCION_MAESTRA_PROFESIONAL` como constante
- Actualizado método `razonar()` con parámetro `usar_instruccion_maestra`
- Nuevo método `analizar_ticker_profesional()`
- Método helper `_formatear_dict_tabla()`
- Temperatura reducida a 0.2-0.3 por defecto

### ✅ `test_gemini_profesional.py` (NUEVO)
- Test de análisis profesional
- Test de razonamiento con instrucción maestra
- Comparación de temperaturas
- Ejemplo completo con datos de AAPL

---

## 🚀 PRÓXIMOS PASOS

### 1. Integrar en Telegram Bot
```python
# En telegram_bot/bot.py, método handle_analizar()
resultado = self.ai_engine.analizar_ticker_profesional(
    ticker=ticker,
    datos_tecnicos=datos_tech,
    datos_fundamentales=datos_fund,
    datos_macro=datos_macro,
    contexto_conocimiento=contexto_libro
)
```

### 2. Crear Dashboar con Reportes
- Cada reporte se guarda en base de datos
- Dashboard muestra historial de análisis
- Comparar veredictos vs precio real (backtesting)

### 3. Validación de Precisión
- Rastrear aciertos de COMPRA vs precio
- Calcular hit rate del modelo
- Mejorar continuo

---

## 📞 SOPORTE Y DEBUGGING

Si hay error de cuota:
```
Error: 429 You exceeded your current quota
Solución: Espera 5-8 segundos o usa gemini-1.5-flash
```

Si hay error de autenticación:
```
Error: API key not valid
Solución: Verifica GOOGLE_API_KEY en .env
```

---

## 🎓 CONCLUSIÓN

Tu bot ahora tiene un **motor IA profesional** que:
- ✅ Es **determinista** (mismos datos = misma conclusión)
- ✅ Es **profesional** (formato Markdown, tablas, veredictos binarios)
- ✅ Es **riguroso** (Chain of Thought, reglas binarias)
- ✅ Es **confiable** (scoring explícito, plan de acción)

**Listo para análisis profesionales de trading.**

---

*Versión 2.0 | Noviembre 27, 2025 | Gemini API v1*
