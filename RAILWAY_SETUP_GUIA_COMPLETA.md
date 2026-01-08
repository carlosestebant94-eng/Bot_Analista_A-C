# 🚀 DESPLIEGUE EN RAILWAY - GUÍA COMPLETA

## 📋 RESUMEN EJECUTIVO

Tu proyecto **Bot Analista A&C** ha sido preparado y subido a GitHub de forma **SEGURA** (sin APIs). Ahora está listo para funcionar **24/7 en la nube con Railway**.

### Repositorio GitHub
- **URL:** `https://github.com/carlosestebant94-eng/Bot_Analista_A-C`
- **Privacidad:** Privado (solo tú tienes acceso)
- **Rama principal:** `main`
- **Cuenta vinculada:** `carlosestebant94-eng`

---

## ⚠️ SEGURIDAD: APIs Protegidas

### Lo que se subió a GitHub
✅ Código fuente completo
✅ Configuración (sin valores sensibles)
✅ `.env.example` (plantilla de variables)
✅ Documentación

### Lo que NO se subió a GitHub
❌ `.env` (archivo con tokens)
❌ TELEGRAM_TOKEN
❌ GOOGLE_API_KEY
✅ En su lugar: Variables de entorno en Railway

---

## 🚂 PASO A PASO: CONFIGURAR EN RAILWAY

### 1️⃣ CREAR CUENTA EN RAILWAY
1. Ve a https://railway.app
2. Click en "Start Project"
3. Inicia sesión con GitHub (autoriza railway.app)
4. Conecta tu repositorio (Bot_Analista_A-C)

### 2️⃣ CREAR NUEVO PROYECTO
```
1. Dashboard → New Project
2. Select "GitHub Repo"
3. Busca: "Bot_Analista_A-C"
4. Click "Deploy Now"
```

### 3️⃣ CONFIGURAR VARIABLES DE ENTORNO
Una vez creado el proyecto en Railway:

1. Ve a la pestaña **"Variables"**
2. Haz click en **"Add Variable"**
3. Agrega EXACTAMENTE estas dos variables:

```
TELEGRAM_TOKEN = <tu_token_aqui>
GOOGLE_API_KEY = <tu_api_key_aqui>
```

**Dónde obtener tus tokens:**

#### TELEGRAM_TOKEN
1. Abre Telegram y busca: `@BotFather`
2. Envía: `/start`
3. Envía: `/newbot`
4. Sigue las instrucciones
5. Copia el token que genera (se parece a esto):
   d1E
   ```

#### GOOGLE_API_KEY
1. Ve a https://aistudio.google.com/apikey
2. Click en "Create API Key"
3. Selecciona "Create API key in new project"
4. Copia la clave generada

### 4️⃣ CONFIGURAR LA APLICACIÓN

En Railway, asegúrate de que:

**Start Command:**
```
python main.py
```

**Python Version:**
```
3.12
```

### 5️⃣ DEPLOY AUTOMÁTICO

Railway detectará automáticamente:
- ✅ `requirements.txt` (dependencias)
- ✅ `main.py` (punto de entrada)
- ✅ `Procfile` (si existe)

El despliegue comenzará automáticamente.

---

## 🔍 VERIFICAR QUE FUNCIONA

### En Railway:
1. Ve a **"Deployments"**
2. Busca el estado: Debería mostrar "Success" ✅
3. Los logs deberían mostrar mensajes como:
   ```
   INFO - Bot inicializado correctamente
   INFO - Esperando mensajes...
   ```

### En Telegram:
1. Busca tu bot por username (que creaste en BotFather)
2. Envía: `/start`
3. El bot debería responder

### Probar análisis:
```
/analizar AAPL
/analizar QQQ
/screener corto
```

---

## 📊 ARQUITECTURA EN RAILWAY

```
┌─────────────────┐
│    RAILWAY      │
│   Container     │
└────────┬────────┘
         │
    ┌────┴────────────────────┐
    │                         │
    ├─ Bot Python            ├─ Telegram API
    ├─ main.py               │  (mensajes)
    ├─ Telegram Bot           │
    └────┬────────────────────┘
         │
         ├─ YFinance API (precios)
         ├─ Google Gemini API (análisis IA)
         ├─ Finviz (datos fundamentales)
         └─ SQLite Database (data local)
```

---

## ⚙️ CONFIGURACIÓN AVANZADA (OPCIONAL)

### A. Aumentar Recursos (si es necesario)
```
Railway → Settings → Resources
- CPU: Upgrade a 0.5 - 1 CPU
- RAM: Upgrade a 512 MB - 1 GB
```

### B. Logs Persistentes
```
Railway → Logs:
- Todos los logs se guardan automáticamente
- Visible en el dashboard
```

### C. Base de Datos Persistente
Railway automáticamente crea volúmenes para:
- `/data` (base de datos SQLite)
- `/pdfs` (PDFs analizados)
- `/logs` (historial de logs)

### D. Configurar Dominio Personalizado (Opcional)
```
Railway → Settings → Domain
- Railway genera URL automática
- Puedes configurar dominio personalizado
```

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### ❌ El bot no responde
**Solución:**
1. Verifica que TELEGRAM_TOKEN es correcto en Railway
2. Revisa los logs en Railway Dashboard
3. Busca errores con formato: `ERROR:`

### ❌ Error: "API Key inválida"
**Solución:**
1. Verifica GOOGLE_API_KEY en Railway
2. Asegúrate de copiar la KEY completa (sin espacios)
3. Regenera la clave en aistudio.google.com si es necesario

### ❌ Bot se detiene después de 1 hora
**Solución:**
1. Railway tiene limpieza automática de procesos inactivos
2. El bot funciona 24/7 si sigue recibiendo mensajes
3. Configura un "ping" automático o envía mensajes de prueba

### ❌ Falta memoria o CPU
**Solución:**
1. Upgrade los recursos en Railway Settings
2. El plan gratuito incluye ciertos límites
3. Consulta https://docs.railway.app para planes

---

## 📝 VARIABLES DE ENTORNO DISPONIBLES

Todas estas variables se pueden configurar en Railway:

```
# REQUERIDAS
TELEGRAM_TOKEN=tu_token_aqui
GOOGLE_API_KEY=tu_api_key_aqui

# OPCIONALES (ya tienen valores por defecto)
LOG_LEVEL=INFO                    # DEBUG, INFO, WARNING, ERROR
DATABASE_PATH=./data/bot.db       # Ruta base de datos
PDFS_DIR=./pdfs                   # Directorio PDFs
DATA_DIR=./data                   # Directorio datos
```

---

## 🔐 CHECKLIST DE SEGURIDAD

Antes de publicar, verifica:

✅ El archivo `.env` NO está en GitHub (está en `.gitignore`)
✅ `.env.example` contiene SOLO la estructura (sin valores)
✅ TELEGRAM_TOKEN está SOLO en Railway (no en código)
✅ GOOGLE_API_KEY está SOLO en Railway (no en código)
✅ El repositorio GitHub es PRIVADO
✅ Nadie más tiene acceso a las variables de Railway

---

## 📞 MONITOREO Y MANTENIMIENTO

### Revisar Logs Regularmente
```
Railway Dashboard → Logs
- Busca "ERROR" para problemas
- Busca "WARNING" para advertencias
```

### Actualizar el Código
```
git add .
git commit -m "Actualización"
git push origin main
```
Railway redesplegará automáticamente.

### Reiniciar el Bot
```
Railway Dashboard → Deploy
Click en el botón "Redeploy"
```

---

## 🎯 PRÓXIMOS PASOS

1. **Ahora:** Crea cuenta en Railway
2. **Luego:** Conecta tu GitHub (autoriza railway.app)
3. **Después:** Agrega las 2 variables de entorno
4. **Finalmente:** ¡Deja que el bot funcione 24/7!

---

## 📚 REFERENCIAS ÚTILES

- **Railway Docs:** https://docs.railway.app
- **Bot Telegram API:** https://core.telegram.org/bots/api
- **Google Gemini API:** https://ai.google.dev/
- **GitHub Setup:** https://docs.github.com/en/get-started

---

## 👤 INFORMACIÓN DE LA CUENTA GITHUB

**Usuario:** carlosestebant94-eng
**Repositorio:** Bot_Analista_A-C
**Acceso:** Privado
**URL:** https://github.com/carlosestebant94-eng/Bot_Analista_A-C

---

## ✨ LISTO PARA PRODUCCIÓN

Tu bot está completamente preparado. Solo necesitas:
1. Cuenta en Railway
2. Dos API keys (Telegram + Google)
3. ¡Eso es todo!

El bot estará **operativo 24/7** sin necesidad de que dejes tu computadora encendida.

---

**Fecha de preparación:** 7 de Enero, 2026
**Estado:** ✅ LISTO PARA RAILWAY
**Versión:** 2.1 (Optimizado para Producción)
