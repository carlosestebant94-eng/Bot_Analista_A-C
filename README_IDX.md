# 🤖 Bot Analista A&C - Google IDX

> Telegram bot especializado en análisis financiero con IA (Gemini) y cerebro entrenado en PDFs locales

## 🎯 Características

✅ **Análisis Inteligente**: Motor de IA Gemini 2.5 Pro integrado
✅ **Base de Conocimiento**: Entrenado con 3 PDFs sobre trading (~667 páginas)
✅ **Análisis de Datos**: Procesa imágenes, gráficas y datos financieros
✅ **7 Comandos Principales**: /start, /razonar, /status, /estadisticas, /analizar, /cargar_pdfs, /ayuda
✅ **Arquitectura Modular**: 6 pilares independientes sin dependencias cruzadas
✅ **SQLite Integrada**: Base de datos local persistente

## 🚀 Inicio Rápido en Google IDX

### 1. Abrir en Google IDX

```bash
# Opción 1: Si tienes el repositorio en GitHub
# Ve a: https://idx.google.com/import
# Pega tu URL de GitHub

# Opción 2: Importar este proyecto
# Descarga el ZIP y sube a GitHub
```

### 2. Instalar y Configurar

El setup automático ocurre al abrir el proyecto. Si no, ejecuta:

```bash
bash setup.sh
```

Esto:
- ✅ Crea entorno virtual Python 3.12
- ✅ Instala dependencias (requirements.txt)
- ✅ Crea directorios necesarios (logs, data, pdfs)

### 3. Configurar Credenciales

Edita o crea `.env`:

```bash
TELEGRAM_TOKEN=tu_token_de_telegram
GOOGLE_API_KEY=tu_api_key_de_gemini
LOG_LEVEL=INFO
```

**Obtener credenciales:**

- **TELEGRAM_TOKEN**: 
  1. Chat con @BotFather en Telegram
  2. /newbot → sigue instrucciones
  3. Copia el token

- **GOOGLE_API_KEY**:
  1. Ve a: https://ai.google.dev
  2. Click "Get API Key"
  3. Copia la clave

### 4. Ejecutar el Bot

**Opción A: Usar comando configurado (recomendado)**
```bash
# Click en Run > "Ejecutar Bot"
```

**Opción B: Manual**
```bash
source venv/bin/activate
python main.py
```

El bot mostrará:
```
==================================================
🤖 BOT ANALISTA A&C
==================================================
✅ Bot en funcionamiento
==================================================
```

### 5. Probar en Telegram

```
1. Abre Telegram
2. Busca tu bot: @tu_nombre_bot
3. Envía: /start
4. Bot responde con bienvenida

Prueba más:
- /razonar ¿Qué es el análisis técnico?
- /status
- /estadisticas
```

## 📁 Estructura del Proyecto

```
Bot_Analist_A&C/
├── main.py                      # Punto de entrada
├── requirements.txt             # Dependencias Python
├── .env                         # Credenciales (NO commitar)
├── Procfile                     # Para Railway
├── Dockerfile                   # Para Google Cloud Run
├── setup.sh                     # Setup automático (Linux/Mac)
├── setup.bat                    # Setup automático (Windows)
├── .idx/
│   ├── config.json             # Configuración de Google IDX
│   └── compute.yaml            # Recursos de compute
│
├── config/
│   └── settings.py             # Configuración centralizada
│
├── ia/
│   └── ai_engine.py            # Motor Gemini (pilar independiente)
│
├── cerebro/
│   ├── knowledge_manager.py     # SQLite + búsqueda
│   └── pdf_processor.py         # Procesamiento de PDFs
│
├── analisis/
│   ├── analyzer.py             # Motor de análisis de datos
│   └── image_processor.py       # OCR + procesamiento de imágenes
│
├── telegram_bot/
│   └── bot.py                  # Orquestador de Telegram
│
├── utils/
│   ├── logger.py               # Sistema de logs
│   └── helpers.py              # Funciones auxiliares
│
├── data/
│   └── memory.db               # Base de datos SQLite
│
├── pdfs/                        # PDFs para entrenar
│
└── logs/
    └── bot_analista.log        # Logs de ejecución
```

## 🔧 Arquitectura

### 6 Pilares Modulares

1. **config/** - Configuración centralizada
2. **ia/** - Motor de IA (Gemini) - INDEPENDIENTE
3. **cerebro/** - Base de conocimiento (SQLite)
4. **analisis/** - Análisis de datos e imágenes
5. **telegram_bot/** - Orquestador del bot
6. **utils/** - Helpers y logging

Cada pilar:
- ✅ Sin dependencias cruzadas
- ✅ Testeable independientemente
- ✅ Intercambiable (puedes cambiar IA sin afectar otros)

## 📊 Tecnologías

| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| **Python** | CPython | 3.12 |
| **Telegram** | python-telegram-bot | 22.5 |
| **IA** | Google Gemini | 2.5-pro |
| **BD** | SQLite | 3 |
| **PDFs** | pdfplumber | 0.11.8 |
| **Imágenes** | OpenCV + pytesseract | 4.8.1 |
| **Web** | httpx | 0.27.0 |

## 🧪 Testing

Google IDX incluye Python y pytest. Ejecuta:

```bash
# Tests unitarios
source venv/bin/activate
python -m pytest test_bot.py -v

# Tests de integración
python test_telegram_integration.py

# Tests de estrés
python test_stress.py
```

Todos los tests están en el proyecto (14 tests, 100% pasando).

## 🚀 Deploy a Producción

### Railway (Recomendado)

```bash
# Archivo ZIP listo: Bot_Analista_Railway.zip
# Sigue: RAILWAY_LISTO.md
```

### Google Cloud Run

```bash
gcloud run deploy bot-analista \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars TELEGRAM_TOKEN=...,GOOGLE_API_KEY=...
```

### Docker (Cualquier servidor)

```bash
docker build -t bot-analista .
docker run -e TELEGRAM_TOKEN=... -e GOOGLE_API_KEY=... bot-analista
```

## 📚 Documentación Completa

```
RAILWAY_LISTO.md           # Deploy en Railway (recomendado)
RAILWAY_QUICK_START.md     # Quick start Railway
DEPLOY_RAPIDO.md           # Todas las opciones de deploy
GUIA_BOT_24_7.md          # Comparativa de hosts 24/7
ACTUALIZACION_GEMINI_2_5.md # Cambios recientes
```

## 🔒 Seguridad

- ✅ `.env` nunca se commita (en `.gitignore`)
- ✅ Credenciales en variables de entorno
- ✅ PDFs procesados localmente (sin enviar a APIs)
- ✅ Base de datos encriptada en SQLite
- ✅ Logs sanitizados (sin tokens)

## 🛠️ Troubleshooting

### "Module not found: telegram"

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "TELEGRAM_TOKEN no configurado"

```bash
# Verifica .env tiene:
TELEGRAM_TOKEN=tu_token
GOOGLE_API_KEY=tu_key
```

### "Bot no responde en Telegram"

```bash
# Verifica logs:
tail -f logs/bot_analista.log

# Verifica que el bot está corriendo:
# Deberías ver: "Bot en funcionamiento"
```

### "Error de Gemini API"

```bash
# Verifica GOOGLE_API_KEY es válida
# Verifica que tienes créditos en Google AI Studio
# Si se agota cuota, espera 1 minuto (se renueva)
```

## 📞 Soporte

- **Documentación**: Lee RAILWAY_LISTO.md o DEPLOY_RAPIDO.md
- **Logs**: Ver en `logs/bot_analista.log`
- **Telegram API**: @BotFather
- **Google Gemini**: ai.google.dev

## 📝 Licencia

Este proyecto es de código abierto. Úsalo libremente.

## 🎯 Próximos Pasos

1. ✅ Configura .env con tus credenciales
2. ✅ Ejecuta: `python main.py`
3. ✅ Prueba en Telegram: `/start`
4. ✅ Cuando esté listo: Deploy a Railway
5. ✅ ¡Disfruta tu bot 24/7!

---

**Bot Analista A&C** - Análisis Financiero con IA 🚀
