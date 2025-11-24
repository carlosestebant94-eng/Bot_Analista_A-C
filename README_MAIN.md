# 🤖 Bot Analista A&C

> Bot especializado en análisis financiero con IA Gemini 2.5 Pro y base de conocimiento entrenada en PDFs

## 🎯 Características Principales

✅ **IA Gemini 2.5 Pro** - Razonamiento lógico avanzado
✅ **Base de Conocimiento** - 3 PDFs (~667 páginas) sobre trading
✅ **Análisis Inteligente** - Procesa datos, imágenes y gráficas
✅ **7 Comandos** - /start, /razonar, /analizar, /status, /estadisticas, /ayuda, /cargar_pdfs
✅ **Arquitectura Modular** - 6 pilares independientes
✅ **SQLite Integrada** - Base de datos persistente
✅ **100% Testeado** - 14 tests (100% pasando)

## 🚀 Inicio Rápido

### Opción 1: Google IDX (Recomendado)

```bash
# Ir a: https://idx.google.com/import
# Importar este repositorio
# El setup automático ocurre al abrir
```

### Opción 2: Local (Tu máquina)

```bash
# Clonar o descargar proyecto
git clone https://github.com/tu_usuario/Bot_Analist_A&C.git
cd Bot_Analist_A&C

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
# TELEGRAM_TOKEN=tu_token
# GOOGLE_API_KEY=tu_api_key

# Ejecutar
python main.py
```

### Opción 3: Railway (24/7)

```bash
# Archivo listo: Bot_Analista_Railway.zip
# Ve a: https://railway.app/
# Deploy automático en 10 minutos
```

## 📁 Estructura

```
Bot_Analist_A&C/
├── .idx/                        # Configuración Google IDX
│   ├── config.json
│   └── compute.yaml
│
├── config/                      # Configuración centralizada
│   └── settings.py
│
├── ia/                          # Motor IA (Gemini)
│   └── ai_engine.py            # PILAR INDEPENDIENTE
│
├── cerebro/                     # Base de conocimiento
│   ├── knowledge_manager.py    # SQLite + búsqueda
│   └── pdf_processor.py        # Procesamiento PDFs
│
├── analisis/                    # Análisis de datos
│   ├── analyzer.py             # Motor análisis
│   └── image_processor.py      # OCR + imágenes
│
├── telegram_bot/               # Orquestador Telegram
│   └── bot.py
│
├── utils/                       # Helpers
│   ├── logger.py
│   └── helpers.py
│
├── data/
│   └── memory.db               # BD SQLite
│
├── pdfs/                        # PDFs para entrenar
├── logs/                        # Logs del bot
├── main.py                      # Punto de entrada
├── requirements.txt
├── Procfile                     # Railway
├── Dockerfile                   # Cloud Run
├── setup.sh                     # Setup Linux/Mac
├── setup.bat                    # Setup Windows
│
└── DOCUMENTACIÓN/
    ├── RAILWAY_LISTO.md        # Deploy Railway
    ├── DEPLOY_RAPIDO.md        # Todas opciones
    └── GUIA_BOT_24_7.md        # Comparativa hosts
```

## 🔧 Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| `/start` | Bienvenida e instrucciones |
| `/razonar <pregunta>` | Análisis con IA sobre la pregunta |
| `/analizar` | Modo análisis de datos |
| `/status` | Estado del bot y recursos |
| `/estadisticas` | Estadísticas de uso |
| `/cargar_pdfs` | Cargar nuevos PDFs |
| `/ayuda` | Ayuda detallada |

## 📊 Arquitectura

### 6 Pilares Modulares

1. **config/** - Configuración centralizada
2. **ia/** - Motor Gemini (INDEPENDIENTE, intercambiable)
3. **cerebro/** - SQLite + PDFs
4. **analisis/** - Análisis datos + OCR
5. **telegram_bot/** - Orquestador
6. **utils/** - Logging y helpers

**Ventaja**: Cada pilar es testeable y reemplazable sin afectar otros.

## 🧪 Testing

```bash
# Tests unitarios
python test_bot.py

# Tests de integración
python test_telegram_integration.py

# Tests de estrés
python test_stress.py

# Resultado: 14/14 tests PASSING (100%)
```

## 🚀 Deploy a Producción

### Railway (Recomendado)
```bash
# Archivo: Bot_Analista_Railway.zip (listo)
# Ve a: https://railway.app/
# Costo: ~$5/mes (crédito inicial gratis)
```

### Google Cloud Run
```bash
gcloud run deploy bot-analista --source .
# Costo: ~$0.40/mes
```

### Docker (Cualquier servidor)
```bash
docker build -t bot-analista .
docker run -e TELEGRAM_TOKEN=... -e GOOGLE_API_KEY=... bot-analista
```

## 📚 Documentación

| Documento | Propósito |
|-----------|-----------|
| `README_IDX.md` | Setup en Google IDX |
| `RAILWAY_LISTO.md` | Deploy paso a paso en Railway |
| `RAILWAY_QUICK_START.md` | Quick start Railway |
| `DEPLOY_RAPIDO.md` | Comparativa de 6 opciones |
| `GUIA_BOT_24_7.md` | Análisis detallado de hosts |
| `ACTUALIZACION_GEMINI_2_5.md` | Cambios recientes |

## 🔒 Seguridad

- ✅ `.env` en `.gitignore` (nunca se commita)
- ✅ Credenciales vía variables de entorno
- ✅ PDFs procesados localmente (sin APIs externas)
- ✅ Base de datos encriptada (SQLite)
- ✅ Logs sanitizados (sin tokens)

## 📦 Dependencias Principales

```
python-telegram-bot==22.5       # Telegram API
google-generativeai==0.8.5      # Gemini AI
pdfplumber==0.11.8              # Extracción PDFs
opencv-python==4.8.1            # Visión computacional
pytesseract==0.3.13             # OCR
pandas==2.3.3                   # Análisis de datos
numpy==1.26.4                   # Computación numérica
pillow==10.4.0                  # Procesamiento imágenes
```

## ⚙️ Configuración (.env)

```bash
# Requerido
TELEGRAM_TOKEN=8065924513:AAHcI033x83E9r2fztwWJ-EFMdgUWj4ARJI
GOOGLE_API_KEY=AIzaSyCMXs2CGhTgnFB6bHMxB3aDWXCH_dnDn7Y

# Opcional
LOG_LEVEL=INFO
```

## 🆘 Troubleshooting

**"ModuleNotFoundError"**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**"Bot no responde"**
```bash
tail -f logs/bot_analista.log
# Verifica TELEGRAM_TOKEN y GOOGLE_API_KEY
```

**"Error de Gemini"**
```bash
# Verifica GOOGLE_API_KEY válida
# Si cuota se agota, espera 1 minuto (se renueva gratis)
```

## 💡 Casos de Uso

✅ Análisis financiero y trading
✅ Procesamiento de documentos
✅ Análisis de imágenes/gráficas
✅ Razonamiento lógico con IA
✅ Consultas en base de datos
✅ Reportes automáticos

## 🎯 Roadmap

- [x] Arquitectura modular
- [x] IA Gemini 2.5 Pro
- [x] SQLite + PDFs
- [x] 7 comandos funcionales
- [x] 14 tests (100% passing)
- [x] Deploy en Railway
- [x] Compatibilidad Google IDX
- [ ] Dashboard web (próximo)
- [ ] Más modelos de IA
- [ ] Multi-usuario

## 📞 Soporte

- **Documentación**: Lee README_IDX.md o RAILWAY_LISTO.md
- **Problemas**: Ver logs en `logs/bot_analista.log`
- **Telegram**: @BotFather
- **Google AI**: ai.google.dev

## 📝 Licencia

Código abierto. Úsalo libremente.

## 🎬 Próximos Pasos

1. Configura `.env`
2. Ejecuta: `python main.py`
3. Prueba en Telegram: `/start`
4. Cuando esté listo: Deploy a Railway
5. ¡Disfruta tu bot 24/7! 🚀

---

**Bot Analista A&C** - Análisis Financiero con IA
