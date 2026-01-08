# Solución de Errores en Render - Bot Analista A&C

## 📋 Resumen de Problemas Identificados

### 1. ❌ "Too Many Requests" en YFinance
- **Causa**: Múltiples solicitudes simultáneas a la API de Yahoo Finance
- **Síntoma**: `Error obteniendo TSLA: Too Many Requests. Rate limited. Try after a while.`

### 2. ❌ "Conflict: terminated by other getUpdates request"
- **Causa**: Múltiples instancias del bot ejecutándose con el mismo token
- **Síntoma**: El bot intenta conectarse a Telegram pero otro proceso ya está usando el token

---

## ✅ Soluciones Implementadas

### Solución 1: Rate Limiting y Caché en YFinance

**Archivo**: `data_sources/market_data.py`

#### Cambios:
- ✅ Añadido sistema de **rate limiting** con espera mínima entre solicitudes (500ms)
- ✅ Implementado **caché de datos** con TTL de 60 segundos
- ✅ Lock de thread para evitar race conditions
- ✅ Reintentos inteligentes con exponential backoff

#### Funciones agregadas:
```python
@classmethod
def _aplicar_rate_limit(cls, ticker: str) -> None
    """Espera entre solicitudes para evitar rate limiting"""

@classmethod
def _obtener_cache(cls, ticker: str) -> Optional[Dict[str, Any]]
    """Obtiene datos del caché si son válidos"""

@classmethod
def _guardar_cache(cls, ticker: str, datos: Dict[str, Any]) -> None
    """Guarda datos en caché con timestamp"""
```

#### Métodos mejorados:
- `obtener_datos_actuales()`: Ahora verifica caché primero
- `obtener_historico()`: Aplica rate limiting
- `obtener_fundamentales()`: Aplica rate limiting

### Solución 2: Protección contra Instancias Múltiples

**Archivo**: `main.py`

#### Cambios:
- ✅ Añadido mecanismo de **lock file** (``.bot_lock``)
- ✅ Verifica si hay instancia anterior ejecutándose
- ✅ Intenta detener instancia anterior de forma segura
- ✅ Limpia el lock file al terminar

#### Funciones agregadas:
```python
def verificar_instancia_unica()
    """Verifica que solo haya una instancia ejecutándose"""

def limpiar_lock_file()
    """Limpia el archivo lock al detener el bot"""
```

### Solución 3: Manejo Robusto de Conflictos en Telegram

**Archivo**: `telegram_bot/bot.py` → Método `iniciar()`

#### Cambios:
- ✅ Implementado **error handler** específico para conflictos
- ✅ Reintentos automáticos (hasta 3 intentos)
- ✅ Esperas inteligentes para diferentes tipos de errores
- ✅ Detección de "Conflict: terminated by other getUpdates request"
- ✅ Detección de "Too Many Requests" de Telegram

#### Comportamiento:
| Error | Acción |
|-------|--------|
| Conflict | Espera 5 segundos, reinicia polling |
| Too Many Requests | Espera 60 segundos, reinicia |
| Otro error | Log y re-lanza excepción |

---

## 🚀 Cómo Usar en Render

### Paso 1: Asegurar instalación limpia

```bash
# En Render, ir a Settings > Deploy y ejecutar:
pip install --upgrade -r requirements.txt
```

### Paso 2: Asegurar que no hay instancias anteriores

```bash
# En Render, Settings > Restart instance
# Esto mata todos los procesos anteriores
```

### Paso 3: Iniciar el bot

```bash
python main.py
```

### Paso 4: Verificar logs

En Render, los logs mostrarán:
```
[OK] Gestor de datos inicializado con Rate Limiting
✅ Cache válido para TSLA  <-- Si usa caché
⏱️  Rate limit: Esperando 0.45s para AAPL  <-- Si aplica rate limiting
```

---

## 🔍 Diagnóstico

### Para verificar que el caché funciona:
- Ejecutar: `/analizar AAPL` dos veces en 60 segundos
- Debería ver: `📦 Usando datos en caché para AAPL` en la segunda solicitud

### Para verificar rate limiting:
- Ejecutar `/screener` (analiza múltiples tickers)
- Ver pausas entre solicitudes en los logs

### Para verificar protección de instancias:
- El archivo `.bot_lock` debe existir mientras el bot está activo
- Al detener el bot, se limpia automáticamente

---

## 📝 Parámetros Ajustables

Si quieres cambiar los tiempos:

**En `data_sources/market_data.py`:**
```python
_cache_ttl_seconds = 60  # Aumentar para caché más largo
_min_request_interval = 0.5  # Aumentar si aún hay rate limiting
```

**En `telegram_bot/bot.py`:**
```python
max_reintentos = 3  # Cambiar número de reintentos
time.sleep(5)  # Cambiar espera para conflictos
time.sleep(60)  # Cambiar espera para rate limits
```

---

## ⚠️ Consideraciones Importantes

### Para Render:
1. **Usar dyno tipo `Standard-1X` o superior** (el `Free` tiene límites muy bajos)
2. **Establecer un cron job** que reinicia el servicio cada 6 horas:
   ```
   Settings > Cron Jobs > Add > 0 */6 * * * * deploy
   ```
3. **Monitorear los logs** en los primeros 10 minutos después de deploy

### Para YFinance:
- El caché de 60 segundos es agresivo pero seguro
- Los datos de mercado rara vez cambian en 1 minuto
- Si necesitas datos más frescos, cambiar `_cache_ttl_seconds` a 30

### Para Telegram:
- Solo puede haber **una instancia** con el mismo TOKEN
- Si ves "Conflict", es que hay otra instancia colgada
- La protección de lock file resuelve esto automáticamente

---

## 🧪 Prueba Local Antes de Render

```bash
# En tu máquina local
python main.py

# En otra terminal, probar:
# /analizar AAPL
# /analizar AAPL  (otra vez, debería usar caché)
# /screener INTRADAY
```

---

## 📞 Troubleshooting

### Problema: "Conflict: terminated by other getUpdates request"
**Solución**: 
1. Ir a Render > Resources > Restart all
2. Esperar 30 segundos
3. El bot debería iniciar sin problemas

### Problema: "Too Many Requests" en YFinance
**Solución**:
1. El caché debería haber solucionado esto
2. Si persiste, aumentar `_cache_ttl_seconds` a 120
3. O reducir frecuencia de solicitudes

### Problema: El bot se detiene aleatoriamente
**Solución**:
1. Ver logs para el error específico
2. Si es conexión de Telegram, aumentar reintentos
3. Si es YFinance, aumentar cache TTL

---

## 📊 Cambios en Resumen

| Archivo | Cambios | Beneficio |
|---------|---------|-----------|
| `main.py` | Lock file + verificación | Sin instancias duplicadas |
| `telegram_bot/bot.py` | Error handler + reintentos | Recuperación automática |
| `data_sources/market_data.py` | Rate limiting + caché | Sin "Too Many Requests" |

---

## ✨ Beneficios de la Solución

✅ **Eliminación del error**: "Too Many Requests" de YFinance
✅ **Eliminación del error**: "Conflict: terminated by other getUpdates"  
✅ **Mejor performance**: Datos en caché se sirven instantáneamente
✅ **Mayor confiabilidad**: Reintentos automáticos ante errores
✅ **Mejor escalabilidad**: Protección contra condiciones de carrera

---

## 🚀 Próximos Pasos

1. **Commit estos cambios** a tu repositorio
2. **Deployar a Render** (Settings > Deploy)
3. **Monitorear logs** por 10 minutos
4. **Probar análisis** (Telegram: `/analizar AAPL`)
5. **Probar screener** (Telegram: `/screener INTRADAY`)

Si todo funciona correctamente, verás:
```
✅ Cache válido para AAPL
✅ Datos actuales obtenidos para TSLA
⏱️  Rate limit: Esperando 0.35s para JD
✅ Bot inicializado correctamente
```

---

**Generado**: Enero 8, 2026  
**Versión**: 1.0 - Solución Completa de Rate Limiting y Conflictos
