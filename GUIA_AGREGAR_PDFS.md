# 📚 Guía: Agregar PDFs al Cerebro del Bot

## 🎯 Propósito

Los PDFs permiten al bot aprender de documentos específicos como:
- **Libros de análisis técnico**
- **Reportes de empresas**
- **Papers académicos**
- **Guías de trading**
- **Análisis de sectores**
- **Metodologías propias**

---

## 📂 ¿Cómo agregar PDFs?

### Opción 1: Carpeta Local (Recomendado)

1. **Localiza la carpeta de PDFs**
   ```
   C:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C\pdfs\
   ```

2. **Coloca tus PDFs allí**
   - Simplemente copia los archivos `.pdf` a esa carpeta
   - Ejemplo: `Analisis_Tecnico_Completo.pdf`

3. **El bot los cargará automáticamente**
   - Al reiniciar el bot, los PDFs se procesan
   - Se extraen textos y se indexan
   - Se integran en el análisis

### Opción 2: Comando Telegram (Próximamente)

```
/agregar_pdf [nombre_archivo.pdf]
```

---

## 📋 Qué PDFs Agregar

### ✅ Recomendados para Mejorar Análisis

| Tipo | Ejemplo | Beneficio |
|------|---------|-----------|
| **Análisis Técnico** | Murphy - Technical Analysis | RSI, MACD, Bollinger mejores |
| **Trading Systems** | Alexander Elder - Safe Trading | Entry/Stop/Target mejorados |
| **Fundamental** | Value Investing Principles | P/E, ROE analysis mejorado |
| **Sentimiento** | Market Psychology | Insider/Analyst scores mejor |
| **Metodología Propia** | Tu análisis personal | Personalización total |

---

## 🔄 Flujo de Procesamiento

```
1. PDF en carpeta /pdfs/
   ↓
2. Bot inicia (startup)
   ↓
3. PDFProcessor detecta archivos
   ↓
4. Extrae texto y metadatos
   ↓
5. KnowledgeManager indexa contenido
   ↓
6. EnhancedAnalyzer utiliza en análisis
   ↓
7. Respuestas mejoradas en Telegram
```

---

## 💡 Cómo Mejorar el Análisis con PDFs

### Antes (sin PDFs)
```
/analizar GOOGL
→ Análisis con Técnicos + Fundamentales genéricos
→ Recomendación IA estándar
```

### Después (con PDFs)
```
/analizar GOOGL
→ Análisis enriquecido con:
   - Tu metodología de trading
   - Patrones que documentaste
   - Criterios propios de entrada/salida
   - Perspectivas personalizadas
→ Recomendación personalizada IA + tu criterio
```

---

## 📖 Estructura de un PDF Ideal

El bot extrae mejor información de PDFs con:

1. **Títulos claros**
   - Facilitate búsquedas por tema
   - Estructura lógica

2. **Tablas de referencia**
   - Rangos de RSI, MACD
   - Límites de P/E por sector
   - Score matrices

3. **Ejemplos prácticos**
   - Casos de estudio
   - Análisis reales
   - Resultados históricos

4. **Reglas explícitas**
   - Si RSI > 70 → Hacer X
   - Si P/E < 15 → Hacer Y
   - Condiciones de entrada/salida

---

## 🚀 Ejemplo: Crear tu PDF Personalizado

Puedes crear un PDF simple con tus reglas:

```markdown
# MI METODOLOGÍA DE TRADING

## 1. INDICADORES TÉCNICOS

### RSI (Relative Strength Index)
- RSI > 70: Sobrecompra, posible VENTA
- RSI < 30: Sobreventa, posible COMPRA
- 30-70: Zona neutral, esperar señal

### MACD
- Cruce de 0: Cambio de tendencia
- Positivo + Creciente: Fuerza alcista
- Negativo + Decreciente: Fuerza bajista

## 2. ENTRADA/SALIDA

### Entrada COMPRA
- RSI < 40
- MACD positivo
- Precio > SMA200
- Volumen > promedio

### Stop Loss
- 2% por debajo de entrada
- O debajo de soporte local

### Take Profit
- 3:1 Risk/Reward ratio
- O en resistencia

## 3. FILTROS FUNDAMENTALES

### No Comprar si:
- P/E > 50
- Deuda > 2x equity
- Caída de ingresos > 10%

### Preferir si:
- ROE > 15%
- Crecimiento > 10%
- Posición competitiva fuerte
```

Guarda esto como `Mi_Metodologia.pdf` y colócalo en `/pdfs/`

---

## 🔍 Verificar que se Cargaron

En los logs del bot busca:
```
[INFO] PDFProcessor: Procesando PDF 'Mi_Metodologia.pdf'
[INFO] KnowledgeManager: Documento indexado
```

---

## ⚙️ Configuración Avanzada

### Cambiar directorio de PDFs

En `cerebro/pdf_processor.py`:
```python
self.pdfs_dir = "mi_carpeta_custom"
```

### Agregar PDFs por código

```python
from cerebro import PDFProcessor, KnowledgeManager

processor = PDFProcessor()
doc = processor.procesar_pdf("ruta/al/archivo.pdf")

km = KnowledgeManager()
km.agregar_documento(doc)
```

---

## ⚠️ Limitaciones

- **Máximo tamaño**: Preferiblemente <100MB
- **Formato**: Solo PDF (.pdf)
- **Idioma**: Mejor en español o inglés
- **Calidad**: Mejor si es texto, no escaneado

---

## 📊 Impacto en Análisis

| Componente | Sin PDFs | Con PDFs |
|-----------|----------|----------|
| Score Técnico | Genérico | Personalizado |
| Score Fundamental | Estándar | Según tu criterio |
| Score Sentimiento | General | Enriquecido |
| Entrada/Salida | Automático | Tu metodología |
| Confianza | 60-75% | 75-90%+ |

---

## 🎓 Próximos Pasos

1. **Identifica 1-2 PDFs** que quieras agregar
2. **Colócalos en `/pdfs/`**
3. **Reinicia el bot**
4. **Prueba**: `/analizar GOOGL`
5. **Verifica mejoras** en recomendaciones

---

## 📞 Ayuda

Si un PDF no se procesa:
1. Verifica que sea válido: `pdfplumber` puede abrirlo
2. Revisa logs: `logs/bot_analista.log`
3. Intenta con otro PDF para confirmar

---

**Resultado esperado**: Análisis más personalizado y alineado con tu estrategia 🎯
