# 🚀 RAILWAY DEPLOYMENT - GUÍA PASO A PASO

## ✅ PASO 1: VERIFICAR ARCHIVOS NECESARIOS

Necesitas estos archivos en tu proyecto (ya están listos):

- ✅ `requirements.txt` - Dependencias Python
- ✅ `Procfile` - Configuración de ejecución
- ✅ `main.py` - Punto de entrada
- ✅ `.env` - Variables de entorno (NO se sube a Git)

## ✅ PASO 2: CREAR REPOSITORIO GIT (Opcional pero recomendado)

Si tienes Git instalado:

```bash
cd "C:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C"
git init
git add .
git commit -m "Initial commit: Bot Analista A&C"
```

Si no tienes Git, puedes subir directamente desde Railway.

## ✅ PASO 3: REGISTRARSE EN RAILWAY

1. Ve a: https://railway.app/
2. Click en "Sign Up"
3. Opción A: Regístrate con GitHub (recomendado)
4. Opción B: Email tradicional

## ✅ PASO 4: CREAR NUEVO PROYECTO

1. En el dashboard, click en "Create New Project"
2. Selecciona una de las opciones:
   - A) "Deploy from GitHub" (si usas GitHub)
   - B) "Deploy from File" (si no)

### Opción A: Deploy desde GitHub

```
1. Autoriza a Railway acceder a tu GitHub
2. Selecciona tu repositorio
3. Selecciona rama: main
4. Railway automáticamente detecta Procfile
```

### Opción B: Deploy desde ZIP

```
1. Comprime tu proyecto: Bot_Analist_A&C.zip
2. En Railway, drag & drop el ZIP
3. Railway extrae y detecta Procfile automáticamente
```

## ✅ PASO 5: CONFIGURAR VARIABLES DE ENTORNO

En el dashboard de Railway:

1. En tu proyecto, click en el servicio (debe decir "web" o "worker")
2. Click en la pestaña "Variables"
3. Agrega estas variables:

```

LOG_LEVEL=INFO
```

**NO AGREGUES LA CARPETA `/data` o `/logs` - Railway las crea automáticamente**

## ✅ PASO 6: DEPLOY

1. Railway automáticamente inicia el deploy cuando configurado
2. Espera a que termine (2-5 minutos)
3. Verás mensajes en la consola
4. Cuando termina, muestra: "Deployment successful"

## ✅ PASO 7: VERIFICAR QUE FUNCIONA

1. En el dashboard, ve a la sección "Logs"
2. Deberías ver algo como:

```
==================================================
🤖 BOT ANALISTA A&C
==================================================
✅ Bot en funcionamiento. Presiona Ctrl+C para detener.
==================================================
```

3. Abre Telegram
4. Busca tu bot
5. Escribe `/start`
6. Si responde, ¡está funcionando! ✅

## 🎯 RESUMEN DE PASOS

| Paso | Acción | Tiempo |
|------|--------|--------|
| 1 | Registrarse en Railway | 2 min |
| 2 | Crear proyecto | 1 min |
| 3 | Subir código | 2 min |
| 4 | Configurar variables | 1 min |
| 5 | Deploy automático | 3 min |
| 6 | Probar en Telegram | 1 min |
| **TOTAL** | | **10 minutos** |

## 📊 WHAT HAPPENS AFTER DEPLOY

- ✅ Tu bot corre 24/7 en servidores de Railway
- ✅ No necesitas tu máquina encendida
- ✅ Railway maneja escalado automático
- ✅ Puedes ver logs en tiempo real desde el dashboard
- ✅ Puedes pausar/reanudar desde Railway

## 💾 NOTAS IMPORTANTES

### Base de datos
- Tu archivo `data/memory.db` se mantiene en Railway
- Puedes descargarlo desde el dashboard
- Se sincroniza automáticamente

### PDFs
- Los PDFs están dentro del proyecto
- Se suben automáticamente con el código
- Se mantienen en el servidor de Railway

### Logs
- Los logs se muestran en tiempo real en el dashboard
- También se guardan en `logs/bot_analista.log`

## 🆘 TROUBLESHOOTING

### El bot no responde
1. Verifica logs en Railway dashboard
2. Confirma que `TELEGRAM_TOKEN` es correcto
3. Reinicia el deploy

### Error de API Key
1. Copia exactamente tu `GOOGLE_API_KEY`
2. Sin espacios antes/después
3. Verifica que no haya caracteres extras

### Base de datos no se sincroniza
1. Comprueba que `data/memory.db` existe localmente
2. Sube el archivo nuevamente
3. Reinicia el deployment

## 📈 PRÓXIMOS PASOS

Una vez en Railway:

1. **Monitoreo**: Crea alertas si el bot cae
2. **Backups**: Descarga `data/memory.db` regularmente
3. **Actualizaciones**: Sube nuevas versiones fácilmente
4. **Escalado**: Railway puede manejar más usuarios automáticamente

## 💰 PRECIOS RAILWAY

- **Gratis**: Primeros $5 USD en créditos iniciales
- **Después**: Pay-as-you-go (~$0.000347/hora)
- **Estimado para bot**: ~$5-10 USD/mes

---

## 🎬 ¿LISTO?

Sigue los 7 pasos anteriores y en 10 minutos tu bot estará 24/7 en Railway.

Si necesitas ayuda, puedo:
1. Crear el ZIP del proyecto
2. Guiarte paso a paso por el dashboard
3. Verificar que todo funciona

¿Empezamos?
