# 🌐 Bot en Google IDX - Guía Completa

## ¿Qué es Google IDX?

Google IDX es un IDE basado en nube (navegador) creado por Google para desarrollo full-stack. Permite:

✅ Desarrollar sin instalar nada en tu máquina
✅ Acceder desde cualquier dispositivo
✅ Servidor compute incluido (gratis mientras desarrollas)
✅ Integraciones con GitHub
✅ Terminal Linux completa
✅ Extensiones VS Code

---

## 🚀 OPCIÓN 1: Importar desde GitHub (Recomendado)

### Paso 1: Subir a GitHub

```bash
# Crear repositorio en GitHub
git init
git add .
git commit -m "Bot Analista A&C - Inicial"
git remote add origin https://github.com/tu_usuario/Bot_Analist_A&C.git
git branch -M main
git push -u origin main
```

### Paso 2: Abrir en Google IDX

1. Ve a: https://idx.google.com/import
2. Pega tu URL de GitHub:
   ```
   https://github.com/tu_usuario/Bot_Analist_A&C.git
   ```
3. Click "Import"
4. Espera a que se cargue (~2 minutos)

### Paso 3: El proyecto se abre automáticamente

- ✅ Python 3.12 preinstalado
- ✅ Configuración `.idx/config.json` aplicada
- ✅ Setup automático disponible

---

## 🚀 OPCIÓN 2: Subir archivo ZIP

### Paso 1: Crear ZIP sin venv

```powershell
cd "C:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C"

# Comprimir sin carpetas grandes
Compress-Archive -Path (Get-ChildItem -Recurse -File -Exclude "venv*", ".git*", "__pycache__*", "*.pyc" | % FullName) -DestinationPath Bot_Analist_A&C.zip
```

### Paso 2: Crear repositorio vacío en GitHub

```bash
1. Ve a: https://github.com/new
2. Nombre: Bot_Analist_A&C
3. Click "Create repository"
```

### Paso 3: Subir ZIP a GitHub

```bash
# En Google Cloud o tu máquina:
git init
unzip Bot_Analist_A&C.zip -d .
git add .
git commit -m "Bot Analista A&C"
git remote add origin https://github.com/tu_usuario/Bot_Analist_A&C.git
git push -u origin main
```

### Paso 4: Importar a IDX

```
https://idx.google.com/import?url=https://github.com/tu_usuario/Bot_Analist_A&C.git
```

---

## 📦 Setup en Google IDX

### Automático (Recomendado)

El archivo `.idx/config.json` automáticamente:

1. ✅ Abre Terminal
2. ✅ Ejecuta `bash setup.sh` (Linux/Mac) o `setup.bat` (Windows)
3. ✅ Instala todas las dependencias
4. ✅ Crea directorios necesarios

**Tiempo**: ~3 minutos

### Manual

Si el automático no funciona:

```bash
# En Terminal de IDX:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mkdir -p logs data pdfs
```

---

## ⚙️ Configurar Credenciales

### Paso 1: Obtener tokens

**TELEGRAM_TOKEN:**
```
Telegram > @BotFather
/newbot
Sigue instrucciones
Copia el token
```

**GOOGLE_API_KEY:**
```
https://ai.google.dev
Click "Get API Key"
Copia la clave
```

### Paso 2: En Google IDX

**Opción A: Archivo .env**
```bash
# En Terminal de IDX:
nano .env

# Pega:
TELEGRAM_TOKEN=tu_token
GOOGLE_API_KEY=tu_api_key
LOG_LEVEL=INFO

# Ctrl+X > Y > Enter
```

**Opción B: Variables de entorno**
```bash
export TELEGRAM_TOKEN="tu_token"
export GOOGLE_API_KEY="tu_api_key"
```

---

## 🚀 Ejecutar el Bot

### Opción 1: Usar configuración pre-hecha

```bash
# En IDX, Click en "Run" menu
# Selecciona: "Ejecutar Bot"
# ¡Listo! Bot corre en terminal
```

### Opción 2: Manual

```bash
# En Terminal de IDX:
source venv/bin/activate
python main.py
```

### Deberías ver:

```
==================================================
🤖 BOT ANALISTA A&C
==================================================
Base Directory: /root/workspace/Bot_Analist_A&C
✅ Bot en funcionamiento
==================================================
```

---

## 🔌 Webhooks (Soporte para IDX)

Google IDX proporciona URLs públicas para webhooks:

```
https://idxXXXXXXXX.us-central1.idx.run/
```

Puedes usar esto para:
- Webhooks de Telegram
- APIs expuestas
- Testing local

---

## 🧪 Testing en IDX

```bash
# Tests unitarios
source venv/bin/activate
python -m pytest test_bot.py -v

# Tests de integración
python test_telegram_integration.py -v

# Tests de estrés
python test_stress.py -v
```

---

## 📊 Debug en IDX

### Ver logs en tiempo real

```bash
tail -f logs/bot_analista.log
```

### Debugger de Python

```bash
python -m pdb main.py
```

### Ver variables de entorno

```bash
env | grep TELEGRAM
env | grep GOOGLE
```

---

## 🔄 Git en IDX

Google IDX tiene Git integrado:

```bash
# Ver cambios
git status

# Hacer commit
git add .
git commit -m "Cambios"

# Pushear
git push origin main

# Pullear
git pull origin main
```

---

## 🌐 Previsualizar Puerto

Google IDX puede previsualizar puertos:

```bash
# Si el bot expone un puerto (ej: 8000)
# Click en "Preview" tab
# Verás: https://idxXXXXXXXX.us-central1.idx.run/
```

---

## 💾 Persistencia de Datos

Los datos en IDX persisten:

✅ `data/memory.db` - Se mantiene entre sesiones
✅ `logs/` - Se mantienen
✅ `pdfs/` - Se mantienen

**Importante**: Si borras la sesión de IDX, los datos se pierden. Haz backup:

```bash
# Descargar database
# En Terminal: Click derecha en "data/memory.db" > Download
```

---

## 🚀 Deploy desde IDX

Una vez funcionando en IDX, puedes deployar a:

### Railway (desde IDX)

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Conectar
railway login

# Deploy
railway link
railway up
```

### Google Cloud Run (desde IDX)

```bash
# Instalar gcloud
curl https://sdk.cloud.google.com | bash

# Autenticar
gcloud auth login

# Deploy
gcloud run deploy bot-analista --source .
```

---

## 🆘 Troubleshooting en IDX

### "Python not found"
```bash
# IDX usa python3
python3 --version
python3 -m venv venv
```

### "Permission denied" en setup.sh
```bash
chmod +x setup.sh
bash setup.sh
```

### "No module named telegram"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Bot no responde en Telegram"
```bash
# Verifica logs:
tail -f logs/bot_analista.log

# Verifica variables:
echo $TELEGRAM_TOKEN
echo $GOOGLE_API_KEY
```

---

## 📊 Recursos en IDX

Google IDX otorga gratis:

- ✅ Máquina e2-medium (2 CPUs, 4GB RAM)
- ✅ 50GB almacenamiento
- ✅ Acceso a Internet
- ✅ URLs públicas para webhooks
- ✅ Terminal Linux
- ✅ VS Code completo

---

## 💡 Tips y Tricks

### 1. Tener múltiples terminales
```
Terminal Tab > "+" > Nueva terminal
```

### 2. Splitear pantalla
```
Click en archivos > Drag derecha
Ves terminal + código lado a lado
```

### 3. Extensiones útiles
```
En IDX, instala:
- Python (automático)
- Pylance (análisis código)
- Jupyter (notebooks)
- Git Graph (visualizar commits)
```

### 4. Shortcuts útiles
```
Ctrl+` = Abrir/cerrar terminal
Ctrl+P = Buscar archivo
Ctrl+H = Buscar/reemplazar
F5 = Debugger
```

---

## 🎯 Flujo Completo

1. **Crear repo en GitHub** (5 min)
2. **Importar a IDX** (https://idx.google.com/import) (2 min)
3. **Setup automático ocurre** (3 min)
4. **Configurar .env** (1 min)
5. **Ejecutar bot** (1 min)
6. **Probar en Telegram** (2 min)
7. **Pushear cambios** (1 min)
8. **Deploy a Railway** (cuando esté listo) (10 min)

**TOTAL: ~25 minutos para tener bot 100% funcional en la nube**

---

## 📞 Recursos

- **Google IDX Docs**: https://idx.google.com/docs
- **Python en IDX**: Python 3.12 preinstalado
- **Git**: Git preinstalado
- **Node.js**: Node 20 preinstalado (opcional)

---

## ✅ Ventajas de IDX vs Local

| Aspecto | Local | IDX |
|---------|-------|-----|
| **Setup** | 30 min | 5 min |
| **Dependencias** | Conflictos posibles | Aislado |
| **Acceso** | Solo esta máquina | Cualquier dispositivo |
| **Terminal** | Windows/Bash/PowerShell | Linux puro |
| **Git** | Manual | Integrado |
| **Storage** | Tu disco | 50GB en nube |
| **Costo** | Gratis | Gratis (mientras desarrollas) |

---

**¡Bot Analista A&C completamente compatible con Google IDX! 🚀**
