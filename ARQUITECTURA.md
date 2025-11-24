# ARQUITECTURA TÉCNICA - Bot Analista A&C

## 📐 Diagrama General de Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    USUARIO (Telegram)                    │
└────────────────────────┬────────────────────────────────┘
                         │
                    [Mensajes]
                         │
┌────────────────────────▼────────────────────────────────┐
│           TELEGRAM BOT (telegram_bot/bot.py)            │
│  ├─ Manejadores de comandos                            │
│  ├─ Procesamiento de mensajes                          │
│  ├─ Manejo de imágenes                                 │
│  └─ Coordinación de módulos                            │
└────────────────────────┬────────────────────────────────┘
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
    ┌─────────┐   ┌──────────┐   ┌──────────────┐
    │ CEREBRO │   │ ANÁLISIS │   │   IMÁGENES   │
    │ ─────── │   │ ──────── │   │ ────────────│
    │ -PDF    │   │ -Análisis│   │ -OCR        │
    │ -Base   │   │ -Datos   │   │ -Formas     │
    │  Datos  │   │ -Comp.   │   │ -Gráficos   │
    │ -Cache  │   │          │   │ -Colores    │
    └────┬────┘   └────┬─────┘   └──────┬──────┘
         │             │                │
         └─────────────┼────────────────┘
                       │
         ┌─────────────▼────────────────┐
         │   BASE DE DATOS (SQLite)     │
         │   ───────────────────────── │
         │   • Documentos              │
         │   • Conocimiento            │
         │   • Análisis (histórico)    │
         │   • Aprendizajes            │
         └─────────────────────────────┘
```

---

## 🧠 Módulo del Cerebro (Pillar Principal)

### Estructura

```python
cerebro/
├── pdf_processor.py      # Extrae info de PDFs
├── knowledge_manager.py  # Gestiona BD de conocimiento
└── memory.db             # SQLite - Base de datos
```

### Funcionalidades

#### 1. **PDFProcessor**
```
procesar_pdf()          → Extrae contenido de un PDF
procesar_todos_pdfs()   → Procesa todos los PDFs del directorio
extraer_texto_completo() → Concatena todo el texto
buscar_en_documentos()  → Búsqueda de términos
guardar_procesamiento() → Exporta a JSON
```

**Salida**: Documento estructurado con:
- Metadatos (fecha, título, etc.)
- Texto por página
- Tablas detectadas
- Texto completo concatenado

#### 2. **KnowledgeManager**
```
inicializar_bd()        → Crea tablas SQLite
cargar_documento()      → Agrega PDF a BD
agregar_conocimiento()  → Almacena conocimiento estructurado
buscar_conocimiento()   → Búsqueda por relevancia
registrar_analisis()    → Guarda análisis para aprendizaje
obtener_estadisticas()  → Métricas de la BD
```

**Tablas SQLite**:
1. **documentos**: Almacena PDFs cargados
2. **conocimiento**: Información extraída (tema, contenido, relevancia)
3. **analisis_realizados**: Histórico de análisis
4. **aprendizajes**: Patrones y mejoras detectadas

---

## 📊 Módulo de Análisis

### Estructura

```python
analisis/
├── analyzer.py          # Motor de análisis
└── image_processor.py   # Procesamiento visual
```

### Funcionalidades

#### 1. **Analyzer**
```
analizar_datos()        → Análisis cuantitativo
├─ Busca conocimiento relevante
├─ Detecta patrones
├─ Genera recomendaciones
└─ Registra para aprendizaje

analizar_comparativa()  → Compara dos datasets
generar_reporte()       → Resumen de análisis
```

**Flujo de análisis**:
```
Datos de entrada
     ↓
Búsqueda en conocimiento (cerebro)
     ↓
Análisis de patrones
     ↓
Generación de hallazgos
     ↓
Recomendaciones
     ↓
Registro en BD
     ↓
Respuesta al usuario
```

#### 2. **ImageProcessor**
```
cargar_imagen()        → Lee archivo de imagen
extraer_texto_ocr()    → OCR con pytesseract
detectar_formas()      → Detecta geometría
analizar_colores()     → Análisis de paleta
detectar_graficos()    → Clasifica tipo de gráfico
analisis_completo()    → Análisis integral
```

**Procesamiento de imagen**:
```
Imagen entrada
     ↓
Conversión a escala de grises
     ↓
Detección de bordes (Canny)
     ↓
Detección de contornos
     ↓
├─ Formas geométricas
├─ Tipo de gráfico
├─ OCR de texto
└─ Análisis de colores
     ↓
Resultado integrado
```

---

## 🤖 Módulo del Bot de Telegram

### Estructura

```python
telegram_bot/
└── bot.py              # Clase TelegramAnalystBot
```

### Flujo de Comandos

```
Usuario envía comando
        ↓
Bot recibe en update
        ↓
Handler específico
        ↓
Procesa con módulos
        ↓
Consulta cerebro
        ↓
Realiza análisis
        ↓
Genera respuesta
        ↓
Envía a usuario
        ↓
Registra en BD
```

### Comandos Disponibles

| Comando | Handler | Acción |
|---------|---------|--------|
| `/start` | comando_start | Bienvenida |
| `/ayuda` | comando_ayuda | Muestra ayuda |
| `/status` | comando_status | Estado del bot |
| `/cargar_pdfs` | comando_cargar_pdfs | Entrena cerebro |
| `/analizar` | comando_analizar | Inicia análisis |
| `/estadisticas` | comando_estadisticas | Métricas |

### Manejo de Contenido

```
Texto      → handle_texto()      → Análisis o búsqueda
    ↓
Imagen     → handle_imagen()     → OCR + análisis visual
    ↓
Resultado  → registra_analisis() → BD
```

---

## 🔌 Integración de Módulos

### Inicialización

```python
# En main.py o bot.py
bot = TelegramAnalystBot()

# Dentro de __init__:
self.knowledge_manager = KnowledgeManager()  # 🧠 Cerebro
self.pdf_processor = PDFProcessor()          # 📄 PDFs
self.analyzer = Analyzer(km)                 # 📊 Análisis
self.image_processor = ImageProcessor()      # 🖼️ Imágenes
self.app = Application()                     # 🤖 Bot
```

### Flujo de Datos

```
Usuario
  ↓
Telegram API
  ↓
TelegramAnalystBot
  ├─→ KnowledgeManager   (Busca)
  ├─→ PDFProcessor       (Procesa)
  ├─→ Analyzer           (Analiza)
  ├─→ ImageProcessor     (Visual)
  └─→ Logger             (Registra)
  ↓
SQLite DB
  ↓
Respuesta
  ↓
Usuario
```

---

## 💾 Base de Datos

### Esquema SQLite

```sql
-- Tabla de documentos
CREATE TABLE documentos (
    id INTEGER PRIMARY KEY,
    nombre TEXT UNIQUE,
    ruta TEXT,
    tipo TEXT,
    fecha_carga TIMESTAMP,
    contenido TEXT
);

-- Tabla de conocimiento
CREATE TABLE conocimiento (
    id INTEGER PRIMARY KEY,
    documento_id INTEGER,
    tema TEXT,
    contenido TEXT,
    relevancia REAL,
    fecha_creacion TIMESTAMP,
    FOREIGN KEY (documento_id) REFERENCES documentos(id)
);

-- Tabla de análisis realizados
CREATE TABLE analisis_realizados (
    id INTEGER PRIMARY KEY,
    tipo_analisis TEXT,
    entrada TEXT,
    resultado TEXT,
    confianza REAL,
    fecha_analisis TIMESTAMP,
    fuentes TEXT
);

-- Tabla de aprendizajes
CREATE TABLE aprendizajes (
    id INTEGER PRIMARY KEY,
    tipo TEXT,
    descripcion TEXT,
    valor TEXT,
    fecha_aprendizaje TIMESTAMP
);
```

### Operaciones Principales

**Inserción de Conocimiento**:
```python
knowledge_manager.cargar_documento(nombre, ruta, tipo, contenido)
knowledge_manager.agregar_conocimiento(tema, contenido, relevancia)
```

**Búsqueda**:
```python
resultados = knowledge_manager.buscar_conocimiento("query")
# Retorna: [{"tema", "contenido", "relevancia", "fecha"}]
```

**Análisis**:
```python
knowledge_manager.registrar_analisis(
    tipo_analisis="analisis_datos",
    entrada="JSON",
    resultado="hallazgos",
    confianza=0.85,
    fuentes=["tema1", "tema2"]
)
```

---

## 🔄 Flujo de Aprendizaje Continuo

```
PDF Cargado
    ↓
Procesado → Almacenado en BD
    ↓
Usuario hace análisis
    ↓
Analyzer busca conocimiento relevante
    ↓
Realiza análisis con contexto
    ↓
Registra resultado
    ↓
Bot mejora con cada análisis
```

**Datos que se aprenden**:
- Patrones en análisis anteriores
- Fuentes más relevantes
- Confianza de predicciones
- Errores y correcciones

---

## ⚙️ Configuración del Sistema

### Archivo de Configuración

```python
# config/settings.py
class Settings:
    # Directorios
    PDFS_DIR = "pdfs/"
    DATA_DIR = "data/"
    
    # Telegram
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    # Base de datos
    DATABASE_PATH = "data/memory.db"
    
    # Análisis
    MIN_CONFIDENCE = 0.5
    MAX_RESULTS = 10
    
    # OCR
    OCR_LANGUAGE = "spa+eng"
```

---

## 🔐 Seguridad y Validación

### Validadores

```python
validate_pdf(ruta)      # Verifica extensión, tamaño, validez
validate_image(ruta)    # Verifica formato e integridad
listar_archivos_validos() # Scan seguro de directorios
```

### Límites

- Max PDF: 100 MB
- Max Imagen: 50 MB
- Max Resultados búsqueda: 10
- Confianza mínima: 0.5

---

## 📝 Logging y Debugging

### Logger Centralizado

```python
# utils/logger.py
logger = setup_logger("NombreDelModulo")

logger.info("Información")
logger.warning("Advertencia")
logger.error("Error")
```

**Archivos de log**:
```
logs/bot_analista.log
```

---

## 🚀 Escalabilidad

### Para Futuras Ampliaciones

1. **APIs Externas**:
   - OpenAI para análisis avanzados
   - APIs financieras (Yahoo Finance, etc.)

2. **Nuevos Módulos**:
   - `machine_learning/` - Predicciones
   - `trading/` - Automatización
   - `reporting/` - Generación de reportes

3. **Bases de Datos**:
   - PostgreSQL para producción
   - Redis para caché

4. **Interfaces**:
   - Web Dashboard
   - API REST

---

## 📊 Diagrama de Flujo Completo

```
START
  ↓
Crear directorios
  ↓
Inicializar Settings
  ↓
Crear KnowledgeManager
  ↓
Crear PDFProcessor
  ↓
Crear Analyzer
  ↓
Crear ImageProcessor
  ↓
Crear TelegramAnalystBot
  ↓
Registrar handlers
  ↓
Conectar a Telegram
  ↓
RUNNING → Escucha mensajes
  ├─ Comando?    → Handler específico
  ├─ Texto?      → Análisis/Búsqueda
  ├─ Imagen?     → OCR/Visual
  └─ Archivo?    → Procesar
  ↓
Procesa con módulos
  ├─ Consulta cerebro
  ├─ Realiza análisis
  └─ Procesa datos
  ↓
Registra en BD
  ↓
Envía respuesta
  ↓
¿Continuar?
  ├─ SÍ  → Vuelve a RUNNING
  └─ NO  → Limpieza y EXIT
```

---

## 🧪 Pruebas y Validación

### Archivos de Prueba

```bash
test_example.py
├─ test_cerebro()           # Módulo de cerebro
├─ test_analisis()          # Motor de análisis
├─ test_pdf_processor()     # Procesador PDFs
└─ test_image_processor()   # Procesador imágenes
```

### Ejecución

```bash
python test_example.py    # Pruebas locales
python main.py            # Bot activo
```

---

## 📈 Performance y Optimización

### Cachéo

- Búsquedas en BD con índices
- PDFs procesados y cacheados
- Resultados recientes en memoria

### Límites

- Máximo 10 resultados de búsqueda
- Máximo 50 MB por PDF
- Máximo 50 MB por imagen

---

## 📚 Referencias Técnicas

- **Telegram Bot API**: python-telegram-bot v20.3
- **PDF Processing**: pdfplumber 0.9.0
- **Computer Vision**: OpenCV 4.8.1.78
- **OCR**: pytesseract 0.3.10
- **Database**: SQLite 3
- **Data Analysis**: pandas 2.0.3, numpy 1.24.3

---

**Documento preparado para Bot Analista A&C v1.0**
