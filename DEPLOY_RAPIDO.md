# 🚀 GUÍA RÁPIDA: DEPLOYER BOT EN DIFERENTES PLATAFORMAS

## ⚡ OPCIÓN 1: RAILWAY.APP (RECOMENDADO - 5 MIN)

### Paso 1: Crear cuenta en Railway
```
https://railway.app/
```
Regístrate con GitHub (recomendado)

### Paso 2: Nuevo Proyecto
1. Click en "Create New Project"
2. Selecciona "Deploy from GitHub"
3. Conecta tu repositorio o sube ZIP

### Paso 3: Configurar variables de entorno
En el dashboard de Railway, agrega estas variables:
```
TELEGRAM_TOKEN=8065924513:AAHcI033x83E9r2fztwWJ-EFMdgUWj4ARJI
GOOGLE_API_KEY=AIzaSyCMXs2CGhTgnFB6bHMxB3aDWXCH_dnDn7Y
LOG_LEVEL=INFO
```

### Paso 4: Deploy
Railway detecta automáticamente `Procfile` y despliega el bot.

**¡Listo! Tu bot corre 24/7**

---

## 🌥️ OPCIÓN 2: GOOGLE CLOUD RUN (BARATO - 15 MIN)

### Paso 1: Instalar Google Cloud CLI
```bash
# Descarga desde: https://cloud.google.com/sdk/docs/install
```

### Paso 2: Autenticarse
```bash
gcloud auth login
gcloud config set project tu-proyecto-id
```

### Paso 3: Deploy
```bash
cd "C:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C"

gcloud run deploy bot-analista \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars TELEGRAM_TOKEN=tu_token,GOOGLE_API_KEY=tu_key \
  --timeout 3600
```

### Paso 4: Verificar
```bash
gcloud run services list
```

**Costo:** ~$0.40/mes para un bot siempre corriendo

---

## 🔧 OPCIÓN 3: AWS EC2 (ROBUSTO)

### Paso 1: Crear instancia EC2
1. Ve a AWS Console: https://console.aws.amazon.com/
2. EC2 > Instances > Launch Instance
3. Selecciona: Ubuntu 22.04 LTS
4. Tipo: t2.micro (Free Tier)
5. Configura grupo de seguridad (abre puerto SSH)

### Paso 2: Conectarse
```bash
ssh -i tu-clave.pem ubuntu@tu-ip-publica
```

### Paso 3: Instalar y ejecutar
```bash
sudo apt update
sudo apt install python3.12 python3-pip git screen -y

git clone tu-repositorio
cd tu-proyecto
pip install -r requirements.txt

# Ejecutar en background
screen -S bot
python main.py
# Presiona Ctrl+A luego D

# Para reconectar:
# screen -r bot
```

---

## 📦 OPCIÓN 4: HEROKU (SIMPLE)

### Paso 1: Descargar Heroku CLI
```
https://devcenter.heroku.com/articles/heroku-cli
```

### Paso 2: Autenticarse
```bash
heroku login
```

### Paso 3: Crear app
```bash
heroku create tu-bot-nombre
```

### Paso 4: Agregar variables
```bash
heroku config:set TELEGRAM_TOKEN=tu_token
heroku config:set GOOGLE_API_KEY=tu_key
```

### Paso 5: Deploy
```bash
git push heroku main
```

---

## 🖥️ OPCIÓN 5: REPLIT (MÁS FÁCIL)

### Paso 1: Ir a Replit
```
https://replit.com/
```

### Paso 2: Importar GitHub O crear nuevo
- Crear nuevo "Python Repl"
- O importar desde GitHub

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Agregar variables de entorno
En la sección "Secrets" (candadito):
```
TELEGRAM_TOKEN=...
GOOGLE_API_KEY=...
```

### Paso 5: Ejecutar
Click en "Run"

**Nota:** Usa uptimerobot.com (gratis) para mantener activo

---

## 🏠 OPCIÓN 6: RASPBERRY PI LOCAL (PRIVACIDAD)

### Paso 1: Instalar OS
- Descargar Raspberry Pi Imager
- Instalar Ubuntu Server 22.04

### Paso 2: SSH desde tu PC
```bash
ssh ubuntu@tu-ip-raspberry
```

### Paso 3: Instalar Python
```bash
sudo apt update
sudo apt install python3.12 python3-pip git screen -y
```

### Paso 4: Clonar y ejecutar
```bash
git clone tu-repo
cd tu-proyecto
pip install -r requirements.txt

screen -S bot
python main.py
```

### Paso 5: Mantener activo (opcional)
Si tu router tiene UPnP, el bot será accesible desde Telegram automáticamente.

---

## 📊 COMPARATIVA DE TIEMPO Y COSTO

| Plataforma | Setup | Costo Mensual | Uptime | Recomendado |
|-----------|-------|--------------|--------|------------|
| Railway | 5 min | $5-20 | 99.9% | ⭐⭐⭐⭐⭐ |
| Google Cloud Run | 15 min | $0.40 | 99.99% | ⭐⭐⭐⭐⭐ |
| AWS EC2 | 20 min | $5-10 | 99.99% | ⭐⭐⭐⭐ |
| Heroku | 10 min | Discontinuado | - | ❌ |
| Replit | 5 min | $0-20 | 95% | ⭐⭐⭐ |
| Raspberry Pi | 30 min | $0.50 | 98% | ⭐⭐⭐⭐ |

---

## 🎯 MI RECOMENDACIÓN

**Para empezar inmediatamente:** Railway.app
- Más fácil
- Interfaz hermosa
- Perfecto para desarrollo

**Para producción:** Google Cloud Run
- Más barato
- Altamente escalable
- Integrado con Google

**Para máxima privacidad:** Raspberry Pi
- Control total
- Datos locales
- Bajo costo energético

---

## 💾 ARCHIVOS NECESARIOS

Ya están listos en tu proyecto:
✅ `requirements.txt` - Dependencias Python
✅ `Procfile` - Configuración para Heroku/Railway
✅ `Dockerfile` - Contenedor para Google Cloud/AWS
✅ `.dockerignore` - Archivos a excluir

---

## ⚠️ IMPORTANTE: VARIABLES DE ENTORNO

**Nunca** commits `.env` a Git. En cada plataforma:

### Railway
Dashboard > Variables

### Google Cloud
```bash
--set-env-vars VAR=valor
```

### AWS EC2
Crear `.env` manualmente en la instancia

### Replit
Secrets (candadito)

---

## 🆘 PREGUNTAS FRECUENTES

**¿Qué pasa con mi base de datos?**
- En nube: Se sincroniza con Cloud Storage
- En local: Copia antes de deployer
- En Raspberry: Datos siempre locales

**¿Puedo cambiar de plataforma después?**
- Sí, completamente reversible
- Solo necesitas el código y el .env

**¿Cómo monitoreo logs?**
- Railway: Panel web
- Google Cloud: Cloud Logging
- AWS: CloudWatch
- Replit: Consola
- Raspberry: SSH + tail logs

**¿Cuál es la más confiable?**
- Google Cloud Run: 99.99% uptime
- AWS: 99.99% uptime
- Railway: 99.9% uptime

---

## 🚀 PRÓXIMOS PASOS

1. Elige tu plataforma preferida
2. Sigue los pasos correspondientes
3. Confirma que el bot responde en Telegram
4. ¡Disfruta de tu bot 24/7!

¿Necesitas ayuda con alguna plataforma específica?
