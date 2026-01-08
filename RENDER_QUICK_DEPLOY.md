# ⚡ INSTRUCCIONES RÁPIDAS - Render Deploy (5 minutos)

## 🎯 Problemas que se solucionaron:
- ❌ `Too Many Requests` en YFinance → ✅ Caché inteligente
- ❌ `Conflict: terminated by other getUpdates` → ✅ Lock file
- ❌ Múltiples instancias → ✅ Verificación automática

---

## 📋 Checklist Pre-Deploy

- [ ] Archivo `main.py` actualizado (con lock file)
- [ ] Archivo `data_sources/market_data.py` actualizado (con rate limiting)
- [ ] Archivo `telegram_bot/bot.py` actualizado (con error handlers)
- [ ] Confirmar cambios en Git
- [ ] Token de Telegram válido en `.env`

---

## 🚀 Deploy en Render (3 pasos)

### 1️⃣ Actualizar en Render

**En Render Dashboard:**
1. Ir a tu servicio del Bot
2. Ir a **Settings** > **Source**
3. Hacer clic en **Redeploy**
4. Esperar a que compile (~2 minutos)

### 2️⃣ Reiniciar servicio (importante)

**En Render Dashboard:**
1. Ir a **Overview** 
2. Hacer clic en **Restart instance**
3. Esperar a que se reinicie

### 3️⃣ Verificar logs

**En Render Dashboard:**
1. Ir a **Logs**
2. Buscar:
   - `✅ Gestor de datos inicializado con Rate Limiting`
   - `✅ Bot inicializado correctamente`
   - `✅ Enhanced Analyzer inicializado`

---

## ✅ Señales de Éxito

Verás en los logs:
```
[OK] Gestor de datos inicializado con Rate Limiting
[OK] Gestor de datos inicializado
✅ Cache válido para AAPL
⏱️  Rate limit: Esperando 0.45s para MSFT
✅ Bot inicializado correctamente
[OK] Bot en funcionamiento
```

---

## ❌ Si algo falla:

### Error: "Conflict: terminated by other getUpdates"
```
→ Ir a Render > Restart instance
→ Esperar 30 segundos
→ Debería funcionar ahora
```

### Error: "Too Many Requests"
```
→ El caché debería evitar esto
→ Si persiste: aumentar CACHE_TTL de 60 a 120 segundos
→ Redeploy
```

### Error: "No module named..."
```
→ Ir a Render > Build Command
→ Asegurar que dice: pip install -r requirements.txt
→ Redeploy
```

---

## 🧪 Test Inmediato (Telegram)

Una vez que el bot esté en Render:

1. Enviar comando: `/start`
   - Debería responder con bienvenida

2. Enviar comando: `/analizar AAPL`
   - Debería hacer análisis exitosamente

3. Enviar comando: `/analizar AAPL` (otra vez)
   - Debería ser más rápido (usando caché)

4. Enviar comando: `/screener INTRADAY`
   - Debería analizar múltiples tickers sin errores

---

## 📊 Parámetros Clave

Si necesitas ajustar:

**En `data_sources/market_data.py` (línea ~32):**
```python
_cache_ttl_seconds = 60          # Más = más caché, menos = más actualizados
_min_request_interval = 0.5      # Espera mínima entre requests (segundos)
```

**En `telegram_bot/bot.py` (línea ~1440):**
```python
max_reintentos = 3               # Reintentos ante conflictos
time.sleep(5)                    # Espera para conflictos de Telegram
time.sleep(60)                   # Espera para rate limits de Telegram
```

---

## 💡 Pro Tips

1. **Usar dyno Standard-1X**: Los dyno Free tienen muchas limitaciones
2. **Monitorear primeros 10 minutos**: Ahí se ve si hay problemas
3. **Cache de 60s es seguro**: Los datos de bolsa no cambian tan rápido
4. **Logs son tu amigo**: Siempre revisar logs antes de escalar

---

## 🔄 Rollback (si algo sale mal)

```bash
git revert <commit-hash>
git push
# En Render, hacer Redeploy
```

---

## 📞 Soporte

Errores más comunes y soluciones:

| Error | Solución |
|-------|----------|
| Conflict getUpdates | Restart instance |
| Too Many Requests | Aumentar cache TTL |
| ModuleNotFoundError | Redeploy con build command |
| Memory exceeded | Cambiar a dyno más grande |
| Timeout | Aumentar timeout en YFinance |

---

## ✨ Con estas soluciones:

- ✅ El bot no se colgará por "Too Many Requests"
- ✅ No habrá conflictos de instancias múltiples
- ✅ Los análisis serán más rápidos (caché)
- ✅ Recuperación automática de errores
- ✅ Logs claros para debugging

---

**¡Listo para producción!** 🚀

Tiempo total: ~5-10 minutos
Confiabilidad: ⭐⭐⭐⭐⭐
