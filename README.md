# Bot Analista A&C - Telegram Expert Analyst Bot

## Descripción
Bot de Telegram especializado en análisis de datos y documentos con capacidad de aprendizaje continuo basado en PDFs locales.

## Arquitectura del Proyecto

```
Bot_Analist_A&C/
├── cerebro/                 # Base de conocimiento del bot
│   ├── __init__.py
│   ├── knowledge_manager.py # Gestor de conocimiento
│   ├── pdf_processor.py     # Procesamiento de PDFs
│   └── memory.db            # Base de datos SQLite
├── telegram_bot/            # Módulo principal del bot
│   ├── __init__.py
│   ├── bot.py              # Lógica principal
│   └── handlers.py         # Manejadores de comandos
├── analisis/               # Módulo de análisis
│   ├── __init__.py
│   ├── analyzer.py         # Motor de análisis
│   └── image_processor.py  # Procesamiento de imágenes
├── utils/                  # Utilidades compartidas
│   ├── __init__.py
│   ├── logger.py          # Sistema de logging
│   └── validators.py      # Validadores
├── config/                # Configuración
│   ├── __init__.py
│   └── settings.py        # Configuraciones globales
├── pdfs/                  # Carpeta para PDFs de entrenamiento
├── data/                  # Datos procesados y resultados
├── logs/                  # Archivos de log
├── requirements.txt       # Dependencias
└── main.py               # Punto de entrada
```

## Pilares del Proyecto

### 1. **Cerebro (Knowledge Base)**
- Extrae información de PDFs locales
- Almacena conocimiento en SQLite
- Sistema de recuperación de información (RAG)
- Capacidad de aprendizaje continuo

### 2. **Procesamiento de Imágenes**
- Análisis de gráficas
- OCR para textos en imágenes
- Procesamiento visual

### 3. **Análisis en Tiempo Real**
- Análisis de datos usando conocimiento del cerebro
- Generación de reportes
- Predicciones basadas en el conocimiento

### 4. **Bot de Telegram**
- Interfaz de usuario
- Manejo de comandos
- Transmisión de resultados

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración

1. Crea un archivo `.env` en la raíz del proyecto:
```
TELEGRAM_TOKEN=tu_token_aqui
OPENAI_API_KEY=tu_clave_aqui (opcional)
```

2. Coloca tus PDFs en la carpeta `pdfs/`

## Uso

```bash
python main.py
```

## Comandos del Bot

- `/start` - Inicia el bot
- `/ayuda` - Muestra ayuda
- `/analizar` - Realiza análisis de datos
- `/cargar_pdf` - Carga nuevo PDF al cerebro
- `/status` - Estado del sistema

## Roadmap

- [ ] Fase 1: Estructura base y cerebro
- [ ] Fase 2: Análisis básico
- [ ] Fase 3: Visión computacional
- [ ] Fase 4: Machine Learning
- [ ] Fase 5: Predicciones avanzadas
