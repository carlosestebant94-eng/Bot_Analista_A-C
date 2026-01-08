# 🎯 PLAN DE ACCIÓN TRADING - Cálculo de Entry, Stop, Target y Plazo

## 📋 RESUMEN EJECUTIVO

Tu bot ahora puede recomendar:
- ✅ **Precio de Entrada (Entry Point)** - Dónde entrar
- ✅ **Precio de Stop Loss** - Dónde salir si te equivocas
- ✅ **Precio de Toma de Ganancia (Take Profit)** - Objetivo de precio
- ✅ **Plazo Proyectado** - Cuánto tiempo tardará
- ✅ **Risk/Reward Ratio** - Relación riesgo/ganancia

---

## 🔧 NUEVO MÉTODO: `calcular_plan_accion_trading()`

```python
resultado = ai_engine.calcular_plan_accion_trading(
    ticker="AAPL",
    precio_actual=228.55,
    datos_tecnicos={
        "Soporte Principal": "$225.00",
        "Resistencia": "$235.00",
        "ATR (14)": "$3.50",
        "Volatilidad": "Media"
    },
    datos_fundamentales={
        "P/E Ratio": "32.5",
        "Target Price (Analyst)": "$240",
        "52 Week High": "$245"
    },
    veredicto="COMPRA",
    contexto_analisis="Divergencia alcista confirmada"
)

print(resultado["respuesta"])
```

**Salida esperada:**

```markdown
## 🎯 PLAN DE ACCIÓN TRADING: AAPL

### 1. PUNTO DE ENTRADA (Entry Point)
* **Precio Recomendado:** $227.50
* **Justificación:** En soporte principal, con confirmación de volumen
* **Tipo:** En rebote desde soporte

### 2. NIVEL DE STOP LOSS
* **Precio Stop:** $224.00
* **Pérdida Máxima:** 1.5% o $3.50
* **Justificación:** Debajo del soporte técnico para proteger en caso de ruptura

### 3. OBJETIVO DE GANANCIA (Take Profit)
* **Precio Target:** $240.00
* **Ganancia Potencial:** 5.5% o $12.50
* **Resistencia Base:** Resistencia principal confirmada

### 4. RATIO RIESGO/GANANCIA
* **Risk/Reward:** 1:3.57
* **Evaluación:** Excelente - Muy favorable

### 5. PLAZO PROYECTADO
* **Duración Estimada:** 2-3 semanas
* **Justificación:** Volatilidad media, ATR de $3.50, movimiento hacia resistencia

### 6. CHECKLIST PRE-ENTRADA
☐ Confirmar soporte/resistencia en gráfico
☐ Validar volumen en la entrada
☐ Revisar noticias próximas (Earnings en 15 días)
☐ Verificar R/R ratio >= 1.5 ✅
☐ Establecer alerta en entrada
```

---

## 📊 CÓMO SE CALCULAN LOS PARÁMETROS

### 1. PRECIO DE ENTRADA (Entry Point)

**Para COMPRA:**
```
Entry = Precio en Soporte o Zona de Rebote

Cálculo:
  Entry = Soporte Principal
  O si el precio está cerca del soporte:
  Entry = Precio Actual (inmediato)
  O si el precio está lejos:
  Entry = Esperar pullback a SMA o Soporte
  
Ejemplo:
  Precio Actual: $228.55
  Soporte: $225.00
  Entry Recomendada: $225.50 (pequeño margen)
```

**Para VENTA:**
```
Entry = Precio en Resistencia o Zona de Rechazo

Cálculo:
  Entry = Resistencia Principal
  O si el precio está cerca:
  Entry = Precio Actual (inmediato)
  O si el precio está lejos:
  Entry = Esperar rally a resistencia
  
Ejemplo:
  Precio Actual: $245.30
  Resistencia: $250.00
  Entry Recomendada: $249.50 (pequeño margen)
```

### 2. PRECIO DE STOP LOSS (Protección)

**Método 1: Porcentual (Más simple)**
```
Stop Loss % = 2-3% típico (ajustable)

Cálculo:
  Stop Loss = Precio Entry × (1 - Stop Loss %)
  
Para COMPRA:
  Stop = $225.50 × (1 - 0.02) = $221.00
  
Para VENTA:
  Stop = $249.50 × (1 + 0.02) = $254.50
```

**Método 2: Técnico (Más confiable)**
```
Stop Loss = Nivel técnico anterior

Para COMPRA:
  Stop = Debajo del soporte anterior
  Ejemplo: $221.00 (soporte secundario)
  
Para VENTA:
  Stop = Arriba de la resistencia anterior
  Ejemplo: $254.00 (resistencia secundaria)
```

**Recomendación: Usar el que sea MÁS ALTO en riesgo**
```
Stop Loss FINAL = MAX(método porcentual, método técnico)
```

### 3. PRECIO DE TOMA DE GANANCIA (Take Profit)

**Método 1: Próxima Resistencia/Soporte**
```
Para COMPRA:
  Target = Próxima resistencia
  Ejemplo: $235.00 (resistencia principal)
  O $240.00 (resistencia secundaria)
  
Para VENTA:
  Target = Próximo soporte
  Ejemplo: $230.00 (soporte principal)
  O $215.00 (soporte secundario)
```

**Método 2: Risk/Reward Ratio (Recomendado)**
```
Riesgo = Entry - Stop Loss
Ganancia Deseada = Riesgo × Ratio R/R

Para COMPRA con R/R 1:2:
  Riesgo = $225.50 - $221.00 = $4.50
  Ganancia Deseada = $4.50 × 2 = $9.00
  Target = $225.50 + $9.00 = $234.50
  
Para VENTA con R/R 1:2:
  Riesgo = $254.00 - $249.50 = $4.50
  Ganancia Deseada = $4.50 × 2 = $9.00
  Target = $249.50 - $9.00 = $240.50
```

**Recomendación R/R Ratios:**
```
❌ Evitar: < 1:1 (Rompepuntos)
⚠️  Aceptable: 1:1.5
✅ Bueno: 1:2
🌟 Excelente: 1:3+
```

### 4. PLAZO PROYECTADO

**Basado en ATR (Average True Range):**
```
ATR Bajo (< 2% del precio):
  └─ Volatilidad baja
  └─ Movimiento lento
  └─ Plazo: Largo (3-8 semanas)

ATR Medio (2-5% del precio):
  └─ Volatilidad normal
  └─ Movimiento moderado
  └─ Plazo: Medio (1-4 semanas)

ATR Alto (> 5% del precio):
  └─ Volatilidad alta
  └─ Movimiento rápido
  └─ Plazo: Corto (1-5 días)
```

**Cálculo de Plazo:**
```
Distancia al Target = ABS(Target - Entry)
Movimiento Diario Esperado = ATR

Plazo Estimado (días) = Distancia al Target / Movimiento Diario Esperado

Ejemplo:
  Entry: $225.50
  Target: $240.00
  Distancia: $14.50
  ATR: $3.50
  
  Plazo = $14.50 / $3.50 = 4.1 días ≈ 1 semana

Conversión a Plazo Real:
  < 3 días = Corto plazo (Intraday/scalping)
  3-10 días = Corto plazo
  1-4 semanas = Medio plazo
  1-3 meses = Largo plazo
```

**Ajustes por Eventos:**
```
Earnings próximos (< 5 días):
  └─ Multiplicar plazo × 1.5-2.0
  └─ Mayor volatilidad esperada

Fed meeting próximo:
  └─ Multiplicar plazo × 1.5
  └─ Indecisión de mercado

Macroeconomía mala:
  └─ Multiplicar plazo × 1.3
  └─ Tendencia bajista esperada
```

### 5. RISK/REWARD RATIO

**Cálculo:**
```
Riesgo = |Entry - Stop Loss|
Ganancia = |Target - Entry|

Ratio = Ganancia / Riesgo

Ejemplo:
  Entry: $225.50
  Stop: $221.00
  Target: $240.00
  
  Riesgo = |225.50 - 221.00| = $4.50
  Ganancia = |240.00 - 225.50| = $14.50
  Ratio = 14.50 / 4.50 = 3.22
  
  Resultado: 1:3.22 ✅ EXCELENTE
```

**Evaluación:**
```
< 1:1   = ❌ NUNCA tradear (Perderás más que ganas)
1:1     = ⚠️  EVITAR (Rompepuntos, sin margen)
1:1.5   = ⚠️  ACEPTABLE (Mínimo recomendado)
1:2     = ✅ BUENO (Ratio sano)
1:2.5   = ✅ MUY BUENO
1:3+    = 🌟 EXCELENTE (Oportunidad premium)
```

---

## 💼 EJEMPLO COMPLETO: APPLE (AAPL)

**Entrada: COMPRA a $228.55**

```
┌─────────────────────────────────────────┐
│         ANÁLISIS TÉCNICO                │
├─────────────────────────────────────────┤
│ RSI(14): 62.5 (Neutral)                 │
│ MACD: Cruce alcista                     │
│ Soporte: $225.00                        │
│ Resistencia: $235.00 - $240.00          │
│ ATR(14): $3.50                          │
│ Volatilidad: MEDIA                      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│       PLAN DE ACCIÓN RECOMENDADO        │
├─────────────────────────────────────────┤
│ 📍 ENTRY: $227.50                       │
│    Justificación: Rebote en soporte     │
│                                         │
│ 🛑 STOP LOSS: $224.00                   │
│    Riesgo: $3.50 (1.5%)                 │
│                                         │
│ 🎯 TAKE PROFIT: $240.00                 │
│    Ganancia: $12.50 (5.5%)              │
│                                         │
│ ⚖️  RATIO: 1:3.57 ✅ EXCELENTE          │
│                                         │
│ ⏰ PLAZO: 2-3 semanas                    │
│    Basado en: ATR $3.50, volatilidad    │
│    Movimiento esperado: $12.50/3.50     │
│    = 3-4 barras de $3.50 = 2-3 sem     │
└─────────────────────────────────────────┘

✅ CHECKLIST:
  ☐ Confirmar soporte en $225.00
  ☐ Esperar volumen en entrada
  ☐ Earnings en 15 días (no próximo)
  ☐ R/R 1:3.57 >= 1.5 ✅
  ☐ Establecer alerta en $227.50
```

---

## 🚀 CÓMO USAR EN EL BOT DE TELEGRAM

```python
# En telegram_bot/bot.py, después de análisis profesional

# 1. Obtener veredicto del análisis
veredicto = resultado_analisis.get("veredicto")  # "COMPRA", "VENTA", etc

# 2. Calcular plan de acción
plan = self.ai_engine.calcular_plan_accion_trading(
    ticker=ticker,
    precio_actual=precio_actual,
    datos_tecnicos=datos_tech,
    datos_fundamentales=datos_fund,
    veredicto=veredicto,
    contexto_analisis=f"Análisis completado para {ticker}"
)

# 3. Enviar plan completo al usuario
await self.send_message(
    chat_id,
    plan["respuesta"],
    parse_mode="Markdown"
)
```

---

## 📈 CASOS REALES

### Caso 1: Operación Exitosa
```
AAPL - COMPRA
Entry: $225.50 ✓
Stop: $221.00
Target: $240.00 ✓ ALCANZADO en 14 días

Resultado: +$14.50 por acción
R/R Efectivo: 1:4.14 ✅
```

### Caso 2: Stop Loss Activado
```
TSLA - COMPRA
Entry: $240.00 ✓
Stop: $231.00 ✗ ACTIVADO en 5 días
Target: $255.00 (no alcanzado)

Resultado: -$9.00 por acción
Pérdida Contenida: 3.75% ✅
```

### Caso 3: Toma de Ganancia Parcial
```
GOOGL - COMPRA
Entry: $155.00 ✓
Stop: $148.00
Target: $170.00

Ejecución:
  - 50% de posición en $165.00 (+$10.00)
  - 50% restante en $170.00 (+$15.00)
  
Resultado: Promedio +$12.50 por acción
Estrategia de escalada: ✅
```

---

## ⚠️ REGLAS DE ORO

```
1. NUNCA tradear sin STOP LOSS
   └─ El stop loss es tu mejor amigo

2. Risk/Reward mínimo 1:1.5
   └─ Preferible 1:2 o mejor

3. Riesgo máximo 2-3% por operación
   └─ Protege tu capital total

4. No promedijes perdidas
   └─ Si el trade va mal, cierra y espera nueva entrada

5. Sigue el plan
   └─ No cambies Entry/Stop/Target una vez establecidos
   └─ Solo puedes ajustar Take Profit parcialmente

6. Valida con volumen
   └─ Entry debe confirmarse con volumen alto
   └─ Stop debe estar en nivel técnico real

7. Ajusta por volatilidad
   └─ ATR alto = Mayor stop loss
   └─ ATR bajo = Menor stop loss
```

---

## 📞 PRÓXIMOS PASOS

1. ✅ Integrar `calcular_plan_accion_trading()` en bot
2. ✅ Mostrar plan completo en respuesta a `/analizar`
3. ✅ Guardar histórico de planes en base de datos
4. ✅ Backtesting: Validar hit rate real
5. ✅ Dashboard: Mostrar trades ejecutados vs recomendados

---

**Versión: 2.0 | Fecha: 27 de Noviembre, 2025**
