# 📚 GUÍA PRÁCTICA: CASOS DE USO Y EJEMPLOS

## Ejemplos Reales de Implementación

---

## CASO 1: FLUJO COMPLETO DE ANÁLISIS

### Escenario
Usuario envía comando `/analizar AAPL` al bot.

### Paso a Paso

#### 1️⃣ Usuario envía comando
```
Usuario en Telegram:
/analizar AAPL
```

#### 2️⃣ Bot recibe y procesa
```python
# telegram_bot/bot.py
async def comando_analizar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejador del comando /analizar"""
    
    # Validar entrada
    if not context.args:
        await update.message.reply_text("❌ Formato: /analizar TICKER")
        return
    
    ticker = context.args[0].upper()
    
    # Mostrar que está procesando
    procesando = await update.message.reply_text(
        f"⏳ Analizando {ticker}..."
    )
    
    try:
        # Llama al motor de análisis
        resultado = await self.analyzer.analizar_ticker(ticker)
        
        # Busca en cerebro
        conocimiento = self.knowledge_manager.buscar_conocimiento(ticker)
        
        # Genera respuesta
        respuesta = self.formatear_respuesta(resultado, conocimiento)
        
        # Registra el análisis
        self.knowledge_manager.registrar_analisis(
            tipo="ticker",
            datos={"ticker": ticker},
            resultado=resultado,
            confianza=resultado.get("confianza", 0.5)
        )
        
        # Envía resultado
        await procesando.edit_text(respuesta)
        
        logger.info(f"✅ Análisis {ticker} completado")
        
    except Exception as e:
        await procesando.edit_text(f"❌ Error: {str(e)}")
        logger.error(f"Error analizando {ticker}: {e}")
```

#### 3️⃣ Analyzer obtiene datos
```python
# analisis/analyzer.py
async def analizar_ticker(self, ticker: str) -> Dict:
    """Análisis completo de un ticker"""
    
    try:
        # 1. Obtener datos históricos
        datos = yf.download(ticker, period="1y")
        
        # 2. Calcular indicadores técnicos
        indicadores = self.calcular_indicadores(datos)
        
        # 3. Análisis fundamental
        fundamental = self.analizar_fundamental(ticker)
        
        # 4. Generar señales
        señales = self.generar_señales(indicadores, fundamental)
        
        # 5. Buscar en cerebro
        contexto = self.knowledge_manager.buscar_conocimiento(ticker)
        
        # 6. Generar recomendación
        recomendacion = self.generar_recomendacion(
            señales, contexto
        )
        
        return {
            "ticker": ticker,
            "indicadores": indicadores,
            "fundamental": fundamental,
            "señales": señales,
            "recomendacion": recomendacion,
            "confianza": self.calcular_confianza(señales),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error en análisis: {e}")
        raise
```

#### 4️⃣ Respuesta formateada
```
📊 ANÁLISIS: AAPL

📈 INDICADORES TÉCNICOS
├─ RSI(14): 65.3 ⚠️ (Sobrecompra cercana)
├─ MACD: POSITIVO 📗
├─ Banda Bollinger: MEDIA 📍
└─ Volumen: ALTO 📊

💼 ANÁLISIS FUNDAMENTAL
├─ P/E Ratio: 28.5
├─ Crecimiento: 12% YoY
└─ Salud Financiera: FUERTE ✅

🎯 SEÑALES
├─ Tecnica: COMPRA (70% confianza)
├─ Fundamental: RETENCIÓN (60% confianza)
└─ Combinado: COMPRA MODERADA

💡 CONOCIMIENTO RELACIONADO
├─ Sector tecnología en tendencia alcista
├─ Apple lidera mercado de dispositivos
└─ Tendencia: Resistencia en 185

📋 RECOMENDACIÓN
Acción: COMPRA A RETRACCIÓN
├─ Entry: $175 (retracción de Fibonacci)
├─ Stop Loss: $170 (-2.9%)
├─ Take Profit: $190 (+8.6%)
└─ Risk/Reward: 1:3

✅ Análisis registrado en base de datos
```

---

## CASO 2: CARGA DE CONOCIMIENTO DESDE PDF

### Escenario
Usuario carga un PDF con información de mercado.

### Código Ejemplo

```python
# telegram_bot/bot.py
async def comando_cargar_pdfs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejador para cargar PDFs"""
    
    procesando = await update.message.reply_text(
        "⏳ Cargando PDFs del directorio..."
    )
    
    try:
        # 1. Procesar todos los PDFs
        resultados = self.pdf_processor.procesar_todos_pdfs()
        
        # 2. Para cada PDF procesado
        for pdf_info in resultados:
            # Cargar documento en BD
            self.knowledge_manager.cargar_documento(
                nombre=pdf_info["nombre"],
                contenido=pdf_info["texto"],
                metadatos={
                    "num_paginas": pdf_info["num_paginas"],
                    "tablas": len(pdf_info["tablas"])
                }
            )
            
            # Extraer temas del contenido
            temas = self.extraer_temas(pdf_info["texto"])
            
            # Guardar conocimiento por tema
            for tema in temas:
                contenido_tema = self.extraer_contenido_tema(
                    pdf_info["texto"], tema
                )
                
                self.knowledge_manager.agregar_conocimiento(
                    tema=tema,
                    contenido=contenido_tema,
                    relevancia=self.calcular_relevancia(tema, contenido_tema),
                    documento_id=self.get_doc_id(pdf_info["nombre"])
                )
        
        # 3. Responder
        await procesando.edit_text(
            f"✅ {len(resultados)} PDFs cargados\n"
            f"💾 Cerebro entrenado con éxito"
        )
        
        logger.info(f"Cargados {len(resultados)} PDFs")
        
    except Exception as e:
        await procesando.edit_text(f"❌ Error: {str(e)}")
        logger.error(f"Error cargando PDFs: {e}")
```

---

## CASO 3: PROCESAMIENTO DE IMAGEN CON OCR

### Escenario
Usuario envía una captura de pantalla de un gráfico.

### Código Ejemplo

```python
# telegram_bot/bot.py
async def manejador_imagen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Procesar imágenes enviadas por usuario"""
    
    # Descargar imagen
    photo_file = await update.message.photo[-1].get_file()
    ruta_temporal = f"/tmp/{photo_file.file_id}.jpg"
    await photo_file.download_to_drive(ruta_temporal)
    
    procesando = await update.message.reply_text(
        "🔍 Analizando imagen..."
    )
    
    try:
        # 1. Análisis visual completo
        analisis_visual = self.image_processor.analisis_completo(
            ruta_temporal
        )
        
        # 2. Extraer texto (OCR)
        texto_extraido = analisis_visual["texto_ocr"]
        
        # 3. Detectar gráfico
        tipo_grafico = analisis_visual["tipo_grafico"]
        
        # 4. Si es un gráfico de trading, procesar
        if tipo_grafico in ["candlestick", "linea", "barras"]:
            
            # Extraer datos visuales
            datos = self.extraer_datos_grafico(analisis_visual)
            
            # Analizar visualmente
            analisis = self.analyzer.analizar_datos_visuales(
                datos, texto_extraido
            )
            
            respuesta = f"""
🖼️ ANÁLISIS DE IMAGEN

📊 Tipo de Gráfico: {tipo_grafico}

🔤 Texto Detectado:
{texto_extraido[:500]}...

📈 Análisis Visuales
├─ Tendencia: {analisis['tendencia']}
├─ Puntos Clave: {', '.join(analisis['puntos_clave'])}
└─ Recomendación: {analisis['recomendacion']}

✅ Imagen procesada
            """
        else:
            respuesta = f"""
🖼️ ANÁLISIS DE IMAGEN

📊 Tipo: {tipo_grafico}
🔤 Texto detectado: {len(texto_extraido)} caracteres
🎨 Colores principales: {', '.join(analisis_visual['colores'])}
            """
        
        # 5. Registrar en BD
        self.knowledge_manager.registrar_analisis(
            tipo="imagen",
            datos={"tipo": tipo_grafico},
            resultado=analisis_visual,
            confianza=analisis_visual.get("confianza", 0.6)
        )
        
        await procesando.edit_text(respuesta)
        
    except Exception as e:
        await procesando.edit_text(f"❌ Error: {str(e)}")
        logger.error(f"Error procesando imagen: {e}")
    finally:
        # Limpiar archivo temporal
        os.remove(ruta_temporal)
```

---

## CASO 4: EXPORTAR REPORTE EN PDF

### Escenario
Usuario solicita reporte del último análisis.

### Código Ejemplo

```python
# telegram_bot/bot.py
async def comando_exportar_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Exportar análisis a PDF"""
    
    procesando = await update.message.reply_text(
        "📄 Generando PDF..."
    )
    
    try:
        # 1. Obtener último análisis de la BD
        ultimo_analisis = self.knowledge_manager.obtener_ultimo_analisis()
        
        if not ultimo_analisis:
            await procesando.edit_text(
                "❌ No hay análisis anterior para exportar"
            )
            return
        
        # 2. Generar PDF con ReportLab
        ruta_pdf = self.generar_reporte_pdf(ultimo_analisis)
        
        # 3. Enviar archivo al usuario
        with open(ruta_pdf, 'rb') as pdf_file:
            await update.message.reply_document(
                document=pdf_file,
                filename="Analisis_Completo.pdf"
            )
        
        await procesando.edit_text("✅ PDF enviado")
        logger.info("PDF exportado")
        
    except Exception as e:
        await procesando.edit_text(f"❌ Error: {str(e)}")
        logger.error(f"Error exportando PDF: {e}")

# utils/pdf_generator.py
class PDFReportGenerator:
    """Generar reportes en PDF"""
    
    @staticmethod
    def generar_reporte(analisis: Dict) -> str:
        """Generar PDF con análisis completo"""
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
        
        # Crear documento
        ruta = settings.REPORTES_DIR / f"reporte_{datetime.now().timestamp()}.pdf"
        doc = SimpleDocTemplate(str(ruta), pagesize=letter)
        
        # Contenido
        story = []
        
        # Título
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='#1f77b4',
            spaceAfter=30
        )
        
        story.append(Paragraph(
            f"📊 Análisis de {analisis['ticker']}",
            title_style
        ))
        
        story.append(Spacer(1, 12))
        
        # Indicadores técnicos
        story.append(Paragraph("Indicadores Técnicos", styles['Heading2']))
        
        indicadores_data = [
            ["RSI", str(analisis['indicadores']['rsi'])],
            ["MACD", analisis['indicadores']['macd_signal']],
            ["Banda Bollinger", analisis['indicadores']['bollinger']],
        ]
        
        tabla_indicadores = Table(indicadores_data)
        story.append(tabla_indicadores)
        
        story.append(Spacer(1, 20))
        
        # Recomendación
        story.append(Paragraph("Recomendación", styles['Heading2']))
        story.append(Paragraph(
            analisis['recomendacion'],
            styles['BodyText']
        ))
        
        # Generar
        doc.build(story)
        
        return str(ruta)
```

---

## CASO 5: SISTEMA DE APRENDIZAJE CONTINUO

### Escenario
El bot aprende de cada análisis realizado.

### Código Ejemplo

```python
# cerebro/knowledge_manager.py
def registrar_aprendizaje(self, patron: str, resultado: bool, 
                         confianza: float):
    """Registrar patrones aprendidos"""
    try:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verificar si ya existe el patrón
        cursor.execute(
            "SELECT id, frecuencia, validez FROM aprendizajes WHERE patron = ?",
            (patron,)
        )
        
        fila = cursor.fetchone()
        
        if fila:
            # Actualizar
            id_aprendizaje, frecuencia, validez_anterior = fila
            
            # Recalcular validez (promedio móvil)
            nueva_validez = (validez_anterior * frecuencia + confianza) / (frecuencia + 1)
            
            cursor.execute("""
                UPDATE aprendizajes
                SET frecuencia = frecuencia + 1, validez = ?
                WHERE id = ?
            """, (nueva_validez, id_aprendizaje))
            
        else:
            # Crear nuevo
            cursor.execute("""
                INSERT INTO aprendizajes (patron, frecuencia, validez)
                VALUES (?, 1, ?)
            """, (patron, confianza))
        
        conn.commit()
        conn.close()
        
        logger.info(f"✅ Aprendizaje registrado: {patron}")
        
    except Exception as e:
        logger.error(f"Error registrando aprendizaje: {e}")

# En analyzer.py, después de cada análisis:
for patron in patrones_detectados:
    self.knowledge_manager.registrar_aprendizaje(
        patron=patron,
        resultado=bool_resultado,
        confianza=confianza_analisis
    )
```

---

## CASO 6: BÚSQUEDA INTELIGENTE EN CEREBRO

### Escenario
Usuario pregunta por algo relacionado con un análisis anterior.

### Código Ejemplo

```python
# telegram_bot/bot.py
async def manejador_mensaje_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Procesar mensajes de texto del usuario"""
    
    texto = update.message.text.lower()
    
    # Si es una pregunta, buscar en cerebro
    if any(p in texto for p in ["?", "qué", "cómo", "cuál", "dónde"]):
        
        procesando = await update.message.reply_text("🔍 Buscando en cerebro...")
        
        try:
            # Buscar conocimiento relevante
            resultados = self.knowledge_manager.buscar_conocimiento(
                query=texto,
                limite=3
            )
            
            if not resultados:
                await procesando.edit_text(
                    "❌ No encontré información relacionada"
                )
                return
            
            # Construir respuesta
            respuesta = "📚 Información encontrada:\n\n"
            
            for i, resultado in enumerate(resultados, 1):
                respuesta += f"{i}. **{resultado['tema']}**\n"
                respuesta += f"   {resultado['contenido'][:100]}...\n"
                respuesta += f"   Relevancia: {resultado['relevancia']:.1%}\n\n"
            
            # Usar IA para síntesis (opcional)
            if settings.GEMINI_API_KEY:
                sintesis = self.ai_engine.sintetizar(respuesta)
                respuesta = sintesis
            
            await procesando.edit_text(respuesta)
            
        except Exception as e:
            await procesando.edit_text(f"❌ Error: {str(e)}")
```

---

## CASO 7: VALIDACIÓN DE ENTRADA

### Escenario
Asegurar que los datos sean válidos antes de procesarlos.

### Código Ejemplo

```python
# utils/validators.py
class Validator:
    """Validadores centralizados"""
    
    @staticmethod
    def validar_ticker(ticker: str) -> bool:
        """Validar formato de ticker"""
        # Debe ser 1-5 caracteres alfanuméricos
        return bool(re.match(r'^[A-Z0-9]{1,5}$', ticker.upper()))
    
    @staticmethod
    def validar_imagen(ruta: str) -> bool:
        """Validar que sea una imagen válida"""
        try:
            from PIL import Image
            img = Image.open(ruta)
            # Verificar dimensiones mínimas
            return img.size[0] > 100 and img.size[1] > 100
        except:
            return False
    
    @staticmethod
    def validar_pdf(ruta: str) -> bool:
        """Validar que sea un PDF válido"""
        try:
            import pdfplumber
            with pdfplumber.open(ruta) as pdf:
                return len(pdf.pages) > 0
        except:
            return False

# Uso en telegram_bot/bot.py:
ticker = context.args[0]

if not Validator.validar_ticker(ticker):
    await update.message.reply_text(
        "❌ Ticker inválido\nFormato: /analizar AAPL"
    )
    return
```

---

## CASO 8: MANEJO ROBUSTO DE ERRORES

### Escenario
Capturar y manejar errores elegantemente.

### Código Ejemplo

```python
# utils/exceptions.py
class BotException(Exception):
    """Excepción base del bot"""
    pass

class AnalisysError(BotException):
    """Error en análisis"""
    pass

class DatabaseError(BotException):
    """Error en base de datos"""
    pass

class ValidationError(BotException):
    """Error en validación"""
    pass

# telegram_bot/bot.py
async def comando_analizar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Análisis con manejo de errores"""
    
    try:
        if not context.args:
            raise ValidationError("Ticker requerido")
        
        ticker = context.args[0].upper()
        
        if not Validator.validar_ticker(ticker):
            raise ValidationError("Ticker inválido")
        
        # Procesar
        resultado = await self.analyzer.analizar_ticker(ticker)
        
        if not resultado:
            raise AnalisysError("Análisis no disponible")
        
        # Responder
        await update.message.reply_text(self.formatear(resultado))
        
    except ValidationError as e:
        await update.message.reply_text(f"⚠️ {str(e)}")
        logger.warning(f"Validación fallida: {e}")
    
    except AnalisysError as e:
        await update.message.reply_text(f"📊 {str(e)}")
        logger.error(f"Error de análisis: {e}")
    
    except Exception as e:
        await update.message.reply_text("❌ Error inesperado")
        logger.error(f"Error no manejado: {e}")
```

---

## RESUMEN DE PATRONES

| Caso | Patrón | Ubicación |
|------|--------|-----------|
| 1 | Orquestación | telegram_bot/bot.py |
| 2 | Pipeline | cerebro/pdf_processor.py |
| 3 | Procesamiento | analisis/image_processor.py |
| 4 | Generación | utils/pdf_generator.py |
| 5 | Aprendizaje | cerebro/knowledge_manager.py |
| 6 | Búsqueda | cerebro/knowledge_manager.py |
| 7 | Validación | utils/validators.py |
| 8 | Errores | utils/exceptions.py |

Todos estos patrones son **independientes** y pueden ser **combinados** para crear flujos complejos.

