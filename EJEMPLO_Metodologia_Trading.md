# EJEMPLO: Mi Metodología de Trading

## Capítulo 1: INDICADORES TÉCNICOS

### RSI (Relative Strength Index)

El RSI mide el momentum del mercado en una escala de 0-100.

**Interpretación:**
- **RSI > 70**: Sobrecompra
  - Posible reversión bajista
  - Señal de VENTA considerando otros factores
  - Mayor riesgo de caída inminente

- **RSI 50-70**: Tendencia alcista moderada
  - Compra con cautela
  - Confirmar con MACD y volumen

- **RSI 30-50**: Zona neutral
  - Esperar señales adicionales
  - No operar en rango

- **RSI < 30**: Sobreventa
  - Posible reversión alcista
  - Oportunidad de COMPRA
  - Buscar confirmación

**Regla de Entrada:**
```
SI RSI < 30 Y MACD positivo Y Volumen > promedio
ENTONCES: Considerar COMPRA
STOP: 2% por debajo
TARGET: Resistencia o 3:1 RR
```

### MACD (Moving Average Convergence Divergence)

El MACD mide la relación entre dos medias móviles exponenciales.

**Componentes:**
- **Línea MACD**: EMA(12) - EMA(26)
- **Línea de Señal**: EMA(9) del MACD
- **Histogram**: MACD - Signal Line

**Interpretación:**
- **MACD > Signal y Creciente**: Momentum alcista fuerte
- **MACD < Signal y Decreciente**: Momentum bajista fuerte
- **Cruce de 0**: Cambio de tendencia importante

### Bollinger Bands

Las bandas de Bollinger usan desviación estándar (típicamente 20 períodos, 2 desviaciones).

**Uso:**
- **Precio en banda inferior**: Presión compradora, sobreventa
- **Precio en banda superior**: Presión vendedora, sobrecompra
- **Squeeze**: Baja volatilidad, movimiento grande próximo
- **Expansión**: Alta volatilidad, confirmación de tendencia

## Capítulo 2: MEDIAS MÓVILES

### Sistema de Medias Móviles

Utilizo un sistema de tres medias móviles para confirmar tendencia:

**Corto Plazo:** SMA(20) - Tendencia inmediata
**Mediano Plazo:** EMA(50) - Dirección media
**Largo Plazo:** SMA(200) - Tendencia principal

**Señal de Compra:**
```
SMA(20) > EMA(50) > SMA(200)
Y precio arriba de los 3 promedios
```

**Señal de Venta:**
```
SMA(20) < EMA(50) < SMA(200)
Y precio abajo de los 3 promedios
```

## Capítulo 3: SOPORTES Y RESISTENCIAS

### Identificación Manual

**Soporte**: Nivel donde el precio rebota múltiples veces hacia arriba
**Resistencia**: Nivel donde el precio se detiene múltiples veces hacia abajo

**Regla del 3**: Un nivel es válido si ha sido probado 3 veces

### Puntos Pivot

Utilizo la fórmula estándar:
```
Pivot = (Alto + Bajo + Cierre) / 3
R1 = (Pivot × 2) - Bajo
S1 = (Pivot × 2) - Alto
R2 = Pivot + (Alto - Bajo)
S2 = Pivot - (Alto - Bajo)
```

## Capítulo 4: ENTRADA Y SALIDA

### Regla de Entrada - COMPRA

**Condiciones que deben cumplirse:**
1. ✅ Precio > SMA(200) - Tendencia alcista principal
2. ✅ SMA(20) > EMA(50) - Confirmación de movimiento
3. ✅ RSI < 40 ó RSI entre 40-60 - No sobrecompra
4. ✅ MACD positivo - Momentum alcista
5. ✅ Volumen > volumen promedio 20d - Confirmación
6. ✅ Precio rebota en soporte identificado

**Punto de Entrada:**
- Idealmente en rebote de soporte
- O en ruptura de resistencia con volumen
- Confirmar con vela de cierre

### Regla de Entrada - VENTA

**Condiciones que deben cumplirse:**
1. ✅ Precio < SMA(200) - Tendencia bajista principal
2. ✅ SMA(20) < EMA(50) - Confirmación de movimiento
3. ✅ RSI > 60 ó RSI entre 40-60 - No sobreventa
4. ✅ MACD negativo - Momentum bajista
5. ✅ Volumen > volumen promedio 20d - Confirmación
6. ✅ Precio rechaza en resistencia identificada

**Punto de Entrada:**
- Idealmente en rechazo de resistencia
- O en ruptura de soporte con volumen
- Confirmar con vela de cierre

### Stop Loss

**Regla Universal:**
```
Stop Loss = 2-3% del capital por operación
Ubicación técnica = Debajo de soporte local (compra)
                   Arriba de resistencia local (venta)
```

**Nunca**: Mover stop loss en contra de la posición

### Take Profit

**Ratio Risk/Reward: 1:3 mínimo**
```
Si Risk = $100
Entonces Target debe dar ganancia de $300+
```

**Ubicación:**
- Próxima resistencia/soporte confirmada
- O en Fibonacci 61.8%
- O cuando Risk/Reward es 1:2 y precio a favor

## Capítulo 5: FILTROS FUNDAMENTALES

### NO COMPRAR si:

- P/E > 50 (muy caro respecto ganancias)
- Deuda total > 2x equidad (muy apalancado)
- Caída de ingresos > 10% YoY (pérdida de negocio)
- Margen operativo < 5% (bajo margen)
- Free cash flow negativo (no genera caja)

### PREFERIR si:

- P/E entre 15-25 (valuación justa)
- Deuda < equidad (balance sano)
- Crecimiento de ingresos > 10% (expansión)
- ROE > 15% (retorna bien el capital)
- Free cash flow positivo (genera dinero)

### EVITAR:

- Cambios de CEO frecuentes (incertidumbre)
- Asuntos legales pendientes (riesgo)
- Deuda vencimiento < 1 año (refinanciamiento)
- Insider selling masivo (ellos se van)

## Capítulo 6: GESTIÓN DE RIESGO

### Posición Sizing

```
Tamaño máximo por operación = 2% del capital total
Máximo 5 operaciones simultáneas = 10% total riesgo
```

### Correlación

**Evitar**:
- Entrar en dos stocks del mismo sector
- Correlación > 0.7 con posición existente
- Si una falla, no deben fallar todas

### Diversificación Mínima

- 40% Acciones
- 20% Commodities
- 20% Forex
- 20% Crypto (opcional)

## Capítulo 7: SEÑALES DE ALERTA

Salir de posición si ocurren:

1. ⚠️ Cierre diario debajo de SMA(50) (ruptura de tendencia)
2. ⚠️ Volumen incrementa 3x sin confirmación de movimiento
3. ⚠️ Insider selling > 50% de compras
4. ⚠️ Caída de ingresos > 5% QoQ
5. ⚠️ Ruptura de soporte crítico en volumen

## Capítulo 8: CASOS DE ESTUDIO

### Caso 1: ENTRADA EXITOSA
**Fecha**: Ejemplo del análisis real
**Símbolo**: AAPL
**Setup**: SMA(20) > EMA(50), RSI 35, MACD positivo, rebote en soporte
**Entrada**: $150.25
**Stop**: $147.25 (2%)
**Target**: $157.50 (1:3 RR)
**Resultado**: Target hit en 8 días, +$7.25 (4.8%)

### Caso 2: SALIDA POR ALERTA
**Símbolo**: TSLA
**Entrada**: $220
**Stop**: $215
**Price reached**: $240 (good profit)
**Alerta**: Volumen spike sin movimiento direccional
**Salida**: $235 (lock gains)
**Resultado**: +$15 (6.8%)

## Capítulo 9: PSICOLOGÍA DEL TRADING

### Disciplina

1. **Follow the rules**: Siempre aplica tu sistema
2. **No oversizing**: Nunca más de 2% por operación
3. **No revenge trading**: Si pierdes, espera
4. **Trailing stops**: Mueve stop a break-even después de 1:2 RR

### Errores Comunes

- ❌ Entrar sin confirmar todos los criterios
- ❌ Mover stop loss por emoción
- ❌ Agregar a posición perdedora
- ❌ No tomar ganancias en target
- ❌ Operar sin plan

### Buenas Prácticas

- ✅ Mantén log de operaciones
- ✅ Revisa semanalmente errores
- ✅ Operaciones correctas 1:3 RR mínimo
- ✅ Descansa después de 3 pérdidas seguidas
- ✅ Celebra aciertos pequeños

---

**Última Revisión**: [Tu fecha]
**Versión**: 1.0
**Estado**: Operativo
