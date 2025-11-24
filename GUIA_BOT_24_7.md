# 🚀 GUÍA: EJECUTAR BOT 24/7 SIN MÁQUINA CONECTADA

## 📊 Comparativa de Opciones

| Opción | Costo | Dificultad | Uptime | Recomendado |
|--------|-------|-----------|--------|------------|
| **1. Servidor en Nube (AWS/Google Cloud)** | $5-15/mes | Media | 99.9% | ⭐⭐⭐⭐⭐ |
| **2. Heroku (PaaS)** | Gratis-$50/mes | Fácil | 99.5% | ⭐⭐⭐⭐ |
| **3. Render/Railway** | Gratis-$20/mes | Fácil | 99.9% | ⭐⭐⭐⭐ |
| **4. Replit** | Gratis-$20/mes | Muy fácil | 95% | ⭐⭐⭐ |
| **5. Servidor Dedicado/VPS** | $20-100/mes | Alta | 99.99% | ⭐⭐⭐⭐ |
| **6. Raspberry Pi Local** | $50-100 | Media | 98% | ⭐⭐⭐ |

---

## 🥇 OPCIÓN 1: RAILWAY.APP (RECOMENDADO - GRATIS Y FÁCIL)

### ¿Por qué Railway?
✅ Muy fácil de usar
✅ Gratis para empezar ($5 crédito inicial)
✅ Uptime excelente
✅ Soporte para Python nativo
✅ GitHub integration
✅ Base de datos incluida

### Pasos:

#### 1. Preparar proyecto para Railway
Tu proyecto ya está listo, pero necesitas:
- `requirements.txt` con todas las dependencias
- `Procfile` para indicar cómo ejecutar el bot

#### 2. Crear `requirements.txt`
```bash
cd "C:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C"
pip freeze > requirements.txt
```

#### 3. Crear `Procfile`
```
worker: python main.py
```

#### 4. Crear proyecto en Railway
1. Ve a: https://railway.app/
2. Click en "Start a New Project"
3. Selecciona "Deploy from GitHub" O "Deploy from File"
4. Sube tu código

#### 5. Configurar variables de entorno
En Railway Dashboard:
```
TELEGRAM_TOKEN=8065924513:AAHcI033x83E9r2fztwWJ-EFMdgUWj4ARJI
GOOGLE_API_KEY=AIzaSyCMXs2CGhTgnFB6bHMxB3aDWXCH_dnDn7Y
LOG_LEVEL=INFO
```

#### 6. Deploy
Railway automáticamente detecta `Procfile` y ejecuta el bot

**Ventaja:** En 5 minutos tu bot está 24/7

---

## 🥈 OPCIÓN 2: GOOGLE CLOUD RUN (BARATO - $0.40/mes)

### ¿Por qué Google Cloud Run?
✅ Muy barato (~$0.40/mes para bot)
✅ Serverless (sin preocuparte por servidor)
✅ Escala automática
✅ Integración con Google (ya tienes API key)

### Pasos:

#### 1. Crear `requirements.txt`
```bash
pip freeze > requirements.txt
```

#### 2. Crear `Dockerfile`
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

#### 3. Crear `.dockerignore`
```
.env
venv_bot/
__pycache__/
*.pyc
.git
logs/
```

#### 4. Subir a Google Cloud
```bash
gcloud run deploy bot-analista --source . --platform managed --region us-central1
```

---

## 🥉 OPCIÓN 3: AWS (ROBUSTO - $5-10/mes)

### Usar EC2 Micro (Gratis el primer año con Free Tier)

#### 1. Crear instancia EC2
- Ubuntu 22.04 LTS
- t2.micro (gratis primer año)

#### 2. Conectarse por SSH
```bash
ssh -i tu-clave.pem ubuntu@tu-ip-publica
```

#### 3. Instalar dependencias
```bash
sudo apt update
sudo apt install python3.12 python3-pip screen -y
```

#### 4. Clonar tu proyecto
```bash
git clone tu-repositorio
cd tu-proyecto
pip install -r requirements.txt
```

#### 5. Ejecutar en background con `screen`
```bash
screen -S bot
python main.py
# Presiona Ctrl+A luego D para desconectar
```

#### 6. Reconectar a la sesión
```bash
screen -r bot
```

---

## ⭐ OPCIÓN 4: REPLIT (MÁS SIMPLE - GRATIS)

### Pasos:
1. Ve a https://replit.com/
2. Click en "Create a Repl"
3. Selecciona "Python"
4. Sube tu código
5. Click en "Run"
6. Mantener vivo con uptimerobot.com (Gratis)

**Ventaja:** Súper simple, apenas configuración

---

## 🏠 OPCIÓN 5: RASPBERRY PI LOCAL (SI TIENES UNA)

### Ventajas:
✅ Control total
✅ Bajo costo energético (~$0.50/mes)
✅ Datos siempre locales
✅ Privacidad garantizada

### Necesitas:
- Raspberry Pi 4 (~$50-70)
- Tarjeta SD 32GB (~$10)
- Fuente USB-C (~$10)
- Router con puerto abierto

### Instalación:
```bash
# En Raspberry Pi
sudo apt update
sudo apt install python3.12 python3-pip screen -y

# Clonar proyecto
git clone tu-repo
cd tu-proyecto
pip install -r requirements.txt

# Ejecutar en background
screen -S bot
python main.py
```

---

## 📋 MI RECOMENDACIÓN (PASO A PASO)

### Para empezar rápido: **Railway.app** (10 minutos)
### Para producción: **Google Cloud Run** (30 minutos)
### Para máxima privacidad: **Raspberry Pi** (1-2 horas)

---

## ⚡ INICIO RÁPIDO: RAILWAY (RECOMENDADO)

### Paso 1: Crear `requirements.txt`
```powershell
cd "C:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C"
.\venv_bot\Scripts\Activate.ps1
pip freeze > requirements.txt
```

### Paso 2: Crear `Procfile`
```
worker: python main.py
```

### Paso 3: Registrarse en Railway
https://railway.app/

### Paso 4: Conectar GitHub O subir ZIP
- Opción A: Conectar tu GitHub
- Opción B: Descargar ZIP y subir a Railway

### Paso 5: Agregar variables de entorno
```
TELEGRAM_TOKEN=8065924513:AAHcI033x83E9r2fztwWJ-EFMdgUWj4ARJI
GOOGLE_API_KEY=AIzaSyCMXs2CGhTgnFB6bHMxB3aDWXCH_dnDn7Y
```

### Paso 6: Deploy
¡Listo! Tu bot corre 24/7 en servidores de Railway

---

## 🔧 ARCHIVOS A CREAR

Te voy a ayudar a crear estos archivos. Necesitas:

1. **requirements.txt** - Lista de dependencias
2. **Procfile** - Configuración de ejecución
3. **.gitignore** - Archivos a ignorar (opcional)

¿Cuál opción prefieres?
- A) Railway (Más fácil, recomendado)
- B) Google Cloud Run (Más barato)
- C) AWS (Más robusto)
- D) Raspberry Pi (Máxima privacidad)

Responde y te ayudaré con la configuración completa.

---

## 📞 PREGUNTAS COMUNES

**¿Qué pasa con la base de datos?**
- Los archivos se sincronizarán automáticamente si usas Google Drive
- O puedes mover `data/memory.db` a cada plataforma

**¿Qué pasa con los PDFs?**
- Se pueden empaquetar dentro del docker
- O sincronizar desde Google Drive/Dropbox

**¿Cómo accedo a logs?**
- Railway: Panel web
- Google Cloud: Cloud Logging
- AWS: CloudWatch

**¿Puedo volver a atrás?**
- Sí, simplemente sigue ejecutando en tu máquina
- Las plataformas son reversibles

