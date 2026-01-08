# 🎬 COMANDOS EXACTOS - Copia y Pega

## Opción A: Deploy Inmediato (recomendado)

### Paso 1: Verificar cambios localmente (1 minuto)

```powershell
# En tu terminal PowerShell, en la carpeta del bot:
cd "c:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C"

# Ejecutar prueba:
"C:/Users/sk894/OneDrive/Carlos/OneDrive/Escritorio/Bot_Analist_A&C/venv_bot/Scripts/python.exe" test_bot_startup.py
```

**Esperado:**
```
✅ TODAS LAS PRUEBAS PASARON
🚀 El bot está listo para ejecutarse en Render
```

---

### Paso 2: Commit y Push (1 minuto)

```bash
# En la carpeta del bot:
cd "c:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C"

# Ver cambios:
git status

# Agregar cambios:
git add .

# Hacer commit:
git commit -m "Fix: Implementar rate limiting, caché y protección de instancias únicas

- Agregar rate limiting a YFinance (500ms entre solicitudes)
- Implementar caché inteligente (60s TTL)
- Protección contra instancias múltiples (lock file)
- Error handler robusto con reintentos automáticos
- Documentación completa de la solución"

# Hacer push:
git push
```

**Esperado:**
```
1 file changed, 150 insertions(+)
...
 To github.com:tu-repo/bot.git
```

---

### Paso 3: Deploy en Render (2 minutos)

1. Ir a: https://dashboard.render.com/
2. Seleccionar tu servicio del bot
3. Click en: **Settings** (pestaña arriba a la derecha)
4. Scroll down hasta: **Build & Deploy**
5. Click en: **Redeploy latest commit** (botón azul)
6. Esperar a que termine el deploy (2 minutos)

**Puedes ver el progreso en la pestaña "Logs"**

---

### Paso 4: Verificar (2 minutos)

En Render Dashboard:
1. Click en la pestaña **"Logs"**
2. Busca estas líneas:
```
✅ Gestor de datos inicializado con Rate Limiting
✅ Bot inicializado correctamente
```

En Telegram:
```
/analizar AAPL
↓
Debería funcionar sin errores
```

---

## Opción B: Si Algo Sale Mal (Rollback)

```bash
# En la carpeta del bot:
git revert HEAD

# Confirm the revert (salva y cierra el editor)

git push
```

**En Render:**
1. Dashboard → Tu servicio
2. Settings → Redeploy
3. Esperar 2 minutos

---

## Opción C: Probar Localmente ANTES de Render (5 minutos)

```bash
# Abrir terminal PowerShell en la carpeta del bot:
cd "c:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C"

# Activar virtual env:
& ".\venv_bot\Scripts\Activate.ps1"

# Ejecutar prueba:
python test_bot_startup.py
```

**Esperado:**
```
✅ Logging inicializado
✅ Configuración válida
✅ Módulo 'cerebro' OK
✅ Módulo 'analisis' OK
✅ Módulo 'data_sources' OK
✅ Módulo 'ia' OK
✅ MarketDataManager inicializado
✅ Sistema de caché funciona
✅ Sistema de lock file funciona

==================================================
✅ TODAS LAS PRUEBAS PASARON
==================================================

🚀 El bot está listo para ejecutarse en Render
```

---

## Verificación: Qué Buscar en Logs de Render

### ✅ Señales de Éxito:

```
✅ Gestor de datos inicializado con Rate Limiting
✅ Bot inicializado correctamente
✅ Enhanced Analyzer inicializado
[OK] Bot en funcionamiento
```

### Cuando ejecutas `/analizar AAPL`:

```
⏱️  Rate limit: Esperando 0.45s para AAPL
✅ Datos actuales obtenidos para AAPL: $236.50
✅ Análisis completado exitosamente
```

### Cuando ejecutas `/analizar AAPL` otra vez (mismo 60s):

```
📦 Usando datos en caché para AAPL
✅ Análisis completado exitosamente
```

---

## Variables Que Puedes Ajustar (Opcional)

### Si necesitas más caché (más rápido):

**Archivo**: `data_sources/market_data.py` línea 32

Buscar:
```python
_cache_ttl_seconds = 60
```

Cambiar a:
```python
_cache_ttl_seconds = 120
```

Luego: `git add . && git commit -m "Ajustar cache TTL a 120s" && git push`

---

### Si aún tienes errores de rate limit:

**Archivo**: `data_sources/market_data.py` línea 34

Buscar:
```python
_min_request_interval = 0.5
```

Cambiar a:
```python
_min_request_interval = 1.0
```

Luego: `git add . && git commit -m "Ajustar rate limit a 1s" && git push`

---

### Si quieres más reintentos:

**Archivo**: `telegram_bot/bot.py` línea 1445

Buscar:
```python
max_reintentos = 3
```

Cambiar a:
```python
max_reintentos = 5
```

Luego: `git add . && git commit -m "Aumentar reintentos a 5" && git push`

---

## Troubleshooting: Comandos de Recuperación

### Si ves "Conflict: terminated by other getUpdates":

```bash
# En Render Dashboard:
# 1. Settings > Resources
# 2. Click "Restart instance"
# 3. Esperar 30 segundos
# 4. El bot debería iniciarse
```

---

### Si ves "Too Many Requests" de YFinance:

```bash
# En tu repositorio local:
git checkout -- data_sources/market_data.py

# Cambiar manualmente en `market_data.py`:
# Línea 32: _cache_ttl_seconds = 60  →  120
# Línea 34: _min_request_interval = 0.5  →  1.0

git add .
git commit -m "Ajustar rate limiting y cache"
git push

# En Render: Redeploy
```

---

### Si ves error de módulo:

```bash
# En Render Dashboard:
# 1. Settings > Build Command
# 2. Asegurar que dice:
#    pip install -r requirements.txt
# 3. Click "Redeploy"
```

---

## Resumen de Comandos (Orden Exacto)

```powershell
# 1. Ir a carpeta:
cd "c:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C"

# 2. Probar localmente:
"./venv_bot/Scripts/python.exe" test_bot_startup.py

# 3. Commit:
git add .
git commit -m "Fix: Rate limiting, caché y protección instancias"

# 4. Push:
git push

# 5. En Render Dashboard:
#    Settings > Build & Deploy > Redeploy latest commit

# 6. Esperar 2 minutos

# 7. Ver logs y validar
```

---

## Timeline Completo

```
T+0:00   Ejecutar: git add . && git commit -m "..." && git push
T+0:30   Push completado en GitHub
T+1:00   Render comienza deploy
T+2:00   Deploy completado, servicio reinicia
T+3:00   Ver logs: "✅ Bot inicializado"
T+5:00   Probar: /analizar AAPL en Telegram
T+6:00   Probar caché: /analizar AAPL otra vez (más rápido)
T+7:00   Probar múltiples: /screener INTRADAY
T+10:00  Validación completa ✅
```

**Tiempo total: 10 minutos**

---

## Comandos de Referencia Rápida

```bash
# Ver cambios:
git status

# Ver diferencias:
git diff

# Ver commit log:
git log --oneline -5

# Ver archivos modificados:
git diff --name-only

# Deshacer último commit (CUIDADO):
git revert HEAD

# Ver rama actual:
git branch

# Configuración Git:
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

---

## Confirmación Final

Antes de hacer push, verifica:

```powershell
# Confirmar que los archivos fueron modificados:
git status

# Debería mostrar:
# modified:   main.py
# modified:   data_sources/market_data.py
# modified:   telegram_bot/bot.py
# new file:   test_bot_startup.py
# new file:   RESUMEN_EJECUTIVO.md
# ... (otros archivos nuevos)
```

---

## ✅ Checklist Final Antes de Push

- [ ] Ejecuté `test_bot_startup.py` localmente
- [ ] Todas las pruebas pasaron
- [ ] Reviré los cambios en `git status`
- [ ] Los cambios incluyen los 3 archivos principales
- [ ] Hice commit con mensaje claro
- [ ] Hice push con éxito
- [ ] Confirmé en Render que comienza el deploy

---

## 🚀 Ya Estás Listo

Ejecuta los comandos de la **Opción A** y tu bot estará en producción en 10 minutos.

¿Preguntas? → Lee `RESUMEN_EJECUTIVO.md` o `INICIO_RAPIDO_ERRORES.md`

---

**Fecha**: Enero 8, 2026  
**Estado**: Listo para copiar y ejecutar ✨
