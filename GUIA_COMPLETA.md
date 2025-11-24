# GUÍA COMPLETA - Bot Analista A&C

## 🎯 Descripción General

Bot de Telegram especializado en análisis de datos financieros y procesamiento de documentos. Cuenta con un "cerebro" entrenado con conocimiento de PDFs locales que le permite realizar análisis más precisos y contextualmente relevantes.

### Características Principales

✅ **Cerebro Inteligente**: Base de conocimiento alimentada por PDFs locales  
✅ **Análisis en Tiempo Real**: Análisis de datos financieros y de mercado  
✅ **Visión Computacional**: Análisis de imágenes y gráficas  
✅ **OCR Integrado**: Extracción de texto de imágenes  
✅ **Aprendizaje Continuo**: Mejora con cada análisis realizado  
✅ **Modular y Escalable**: Fácil de expandir con nuevas funcionalidades  

---

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes Python)
- Una cuenta de Telegram
- Token de bot de Telegram (de @BotFather)

---

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd "c:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C"
```

### 2. Crear un entorno virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Nota**: La primera instalación puede tardar un tiempo debido a las dependencias.

### 4. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
copy .env.example .env

# O crear manualmente un archivo .env con:
TELEGRAM_TOKEN=tu_token_aqui
```

---

## 🔑 Obtener Token de Telegram

1. Abre Telegram y busca al usuario **@BotFather**
2. Envía el comando `/newbot`
3. Sigue las instrucciones para crear tu bot
4. Copia el token proporcionado
5. Pégalo en el archivo `.env`

```env
TELEGRAM_TOKEN=123456789:ABCdefGHIjklmnoPQRstuvWXYZabcdefgh
```

---

## 📚 Estructura del Proyecto

```
Bot_Analist_A&C/
│
├── cerebro/                    # Base de conocimiento
│   ├── __init__.py
│   ├── knowledge_manager.py    # Gestor de base de datos
│   └── pdf_processor.py        # Procesador de PDFs
│
├── telegram_bot/               # Bot principal
│   ├── __init__.py
│   └── bot.py                  # Lógica del bot
│
├── analisis/                   # Motor de análisis
│   ├── __init__.py
│   ├── analyzer.py            # Análisis de datos
│   └── image_processor.py     # Análisis de imágenes
│
├── utils/                      # Utilidades
│   ├── __init__.py
│   ├── logger.py              # Sistema de logs
│   └── validators.py          # Validadores de archivos
│
├── config/                     # Configuración
│   ├── __init__.py
│   └── settings.py            # Configuración centralizada
│
├── pdfs/                       # 📂 Carpeta para PDFs de entrenamiento
├── data/                       # 📂 Datos y base de datos SQLite
├── logs/                       # 📂 Archivos de log
│
├── main.py                     # Punto de entrada del bot
├── test_example.py            # Script de pruebas
├── requirements.txt           # Dependencias
├── .env.example               # Plantilla de configuración
├── .gitignore                 # Archivos a ignorar
└── README.md                  # Este archivo
```

---

## 💾 Usar PDFs para Entrenar el Bot

### 1. Agregar PDFs

```bash
# Coloca tus archivos PDF en:
pdfs/
```

Ejemplo:
```
pdfs/
├── manual_analisis_financiero.pdf
├── tecnicas_trading.pdf
└── economia_basica.pdf
```

### 2. Cargar PDFs al Cerebro

**Opción A: Desde el Bot (Telegram)**
```
/cargar_pdfs
```

**Opción B: Con el script de pruebas**
```bash
python test_example.py
```

El bot extraerá todo el contenido del PDF y lo almacenará como conocimiento.

---

## ▶️ Ejecutar el Bot

### Opción 1: Ejecutar el bot (recomendado)

```bash
python main.py
```

Deberías ver:
```
==================================================
🤖 BOT ANALISTA A&C
==================================================
⚙️  CONFIGURACIÓN DEL BOT
...
✅ Bot en funcionamiento. Presiona Ctrl+C para detener.
==================================================
```

### Opción 2: Ejecutar pruebas

```bash
python test_example.py
```

Esto ejecuta pruebas sin necesidad de Telegram.

---

## 📱 Usar el Bot en Telegram

### Comandos Principales

| Comando | Descripción |
|---------|-------------|
| `/start` | Inicia el bot y muestra bienvenida |
| `/ayuda` | Muestra guía de uso |
| `/status` | Estado actual del bot |
| `/cargar_pdfs` | Carga PDFs del cerebro |
| `/analizar` | Modo de análisis |
| `/estadisticas` | Estadísticas del sistema |

### Ejemplos de Uso

#### 1. Análisis de Datos

Envía datos en formato JSON:

```json
{
    "tendencia": "al_alza",
    "volatilidad": 0.15,
    "valores": [100, 105, 110, 108, 115, 120]
}
```

El bot responderá con:
- Hallazgos detectados
- Recomendaciones
- Nivel de confianza
- Fuentes utilizadas

#### 2. Análisis de Imágenes

Simplemente envía una imagen del bot en Telegram:
- Detectará texto (OCR)
- Identificará el tipo de gráfico
- Analizará colores y formas
- Extraerá información relevante

#### 3. Búsqueda de Conocimiento

Escribe una pregunta o término, y el bot buscará en su base de conocimiento:

```
¿Qué es el análisis técnico?
```

---

## 🔧 Configuración Avanzada

### Modificar Parámetros

En `config/settings.py` puedes modificar:

```python
# Tamaño máximo de archivos
MAX_FILE_SIZE_PDF = 100 * 1024 * 1024  # 100 MB
MAX_FILE_SIZE_IMAGE = 50 * 1024 * 1024  # 50 MB

# Análisis
MIN_CONFIDENCE = 0.5
MAX_RESULTS_SEARCH = 10

# OCR
OCR_LANGUAGE = "spa+eng"  # Español e Inglés

# Procesamiento de imágenes
CANNY_THRESHOLD1 = 50
CANNY_THRESHOLD2 = 150
```

### Usar APIs Externas

Opcionalmente, puedes agregar OpenAI para análisis más avanzados:

```env
OPENAI_API_KEY=tu_clave_aqui
```

---

## 📊 Base de Datos

El bot utiliza SQLite para almacenar:

- **Documentos**: PDFs cargados
- **Conocimiento**: Información extraída de PDFs
- **Análisis**: Histórico de análisis realizados
- **Aprendizajes**: Mejoras y patrones detectados

```
data/memory.db
```

### Ver contenido de la BD

```bash
# Usar herramienta SQLite GUI o:
sqlite3 data/memory.db
```

---

## 📝 Logs y Debugging

Los logs se guardan en:

```
logs/bot_analista.log
```

Cambiar nivel de log en `.env`:

```env
LOG_LEVEL=DEBUG    # Para máximo detalle
LOG_LEVEL=INFO     # Normal
LOG_LEVEL=WARNING  # Solo advertencias
```

---

## 🛠️ Troubleshooting

### Error: "ModuleNotFoundError"

```bash
# Asegúrate de estar en el entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstala dependencias
pip install -r requirements.txt
```

### Error: "TELEGRAM_TOKEN no configurado"

```bash
# Verifica que el archivo .env existe y contiene:
TELEGRAM_TOKEN=tu_token_aqui

# Sin espacios adicionales
```

### El bot no responde

1. Verifica que el token sea correcto
2. Asegúrate de tener conexión a internet
3. Revisa los logs en `logs/bot_analista.log`

### Error con PDFs

1. Verifica que sean archivos PDF válidos
2. Colócalos en la carpeta `pdfs/`
3. Ejecuta `/cargar_pdfs` de nuevo

---

## 🚀 Expandir el Proyecto

### Agregar Nuevos Comandos

En `telegram_bot/bot.py`:

```python
async def comando_nuevo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tu nuevo comando"""
    await update.message.reply_text("Respuesta del bot")

# Registrar en _registrar_handlers()
self.app.add_handler(CommandHandler("nuevo", self.comando_nuevo))
```

### Agregar Nuevos Módulos de Análisis

Crea nuevos archivos en `analisis/`:

```python
# analisis/financial_analyzer.py
class FinancialAnalyzer:
    def analizar_portafolio(self, datos):
        # Tu lógica aquí
        pass
```

### Integrar APIs Externas

```python
from cerebro import KnowledgeManager

# En tu módulo nuevo
def usar_api_externa(self, datos):
    # Llamar API
    respuesta = requests.get(url, headers=headers)
    return respuesta.json()
```

---

## 📚 Recursos Útiles

- [Documentación python-telegram-bot](https://python-telegram-bot.readthedocs.io/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [LangChain Docs](https://python.langchain.com/)
- [SQLite Tutorial](https://www.sqlite.org/docs.html)

---

## 🤝 Contribuir

Para mejorar el proyecto:

1. Agrega nuevas funcionalidades
2. Mejora el análisis
3. Optimiza el rendimiento
4. Documenta cambios

---

## 📄 Licencia

Este proyecto es de uso libre y puede ser modificado según tus necesidades.

---

## ❓ Preguntas Frecuentes

**P: ¿Cuántos PDFs puedo cargar?**
R: Depende de tu espacio en disco. Recomendamos máximo 1-2 GB de PDFs.

**P: ¿El bot aprende de nuevo cada vez?**
R: Sí, el bot registra cada análisis para mejorar futuras predicciones.

**P: ¿Puedo usar el bot sin internet?**
R: No, necesitas conexión a internet para Telegram.

**P: ¿Cómo elimino el conocimiento cargado?**
R: Simplemente borra el archivo `data/memory.db` y reinicia el bot.

---

## 📞 Soporte

Si encuentras problemas:

1. Revisa los logs en `logs/bot_analista.log`
2. Verifica la configuración en `.env`
3. Ejecuta `test_example.py` para diagnosticar

---

## 🎉 ¡Listo!

Tu bot está configurado y listo para usar. ¡Comienza a entrenar tu cerebro con PDFs y realiza análisis fascinantes!

Escribe en Telegram:
```
/start
```

¡Bienvenido al futuro del análisis automatizado! 🚀
