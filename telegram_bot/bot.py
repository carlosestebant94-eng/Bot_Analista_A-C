"""
telegram_bot/bot.py
Bot principal de Telegram
Coordina todos los módulos y maneja la comunicación con el usuario
"""

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction
import logging
from pathlib import Path
import json

from config import Settings
from cerebro import KnowledgeManager, PDFProcessor
from analisis import Analyzer, ImageProcessor
from ia import AIEngine
from utils import setup_logger, validate_pdf, validate_image


class TelegramAnalystBot:
    """Bot Telegram especializado en análisis"""
    
    def __init__(self):
        """Inicializa el bot"""
        # Configuración
        Settings.crear_directorios()
        self.settings = Settings
        
        # Logger
        self.logger = setup_logger("TelegramAnalystBot", archivo=str(self.settings.LOG_FILE))
        self.logger.info("Inicializando Bot Analista...")
        
        # Módulos principales (PILARES INDEPENDIENTES)
        self.knowledge_manager = KnowledgeManager(str(self.settings.DATABASE_PATH))
        self.pdf_processor = PDFProcessor(str(self.settings.PDFS_DIR))
        self.analyzer = Analyzer(self.knowledge_manager)
        self.image_processor = ImageProcessor()
        
        # Pilar IA (completamente independiente)
        # Usa Google API Key en lugar de OpenAI
        self.ai_engine = AIEngine(self.settings.GOOGLE_API_KEY)
        
        # Aplicación de Telegram
        self.app = Application.builder().token(self.settings.TELEGRAM_TOKEN).build()
        
        # Registrar handlers
        self._registrar_handlers()
        
        self.logger.info("✅ Bot inicializado correctamente")
    
    def _registrar_handlers(self):
        """Registra los manejadores de comandos"""
        # Comandos
        self.app.add_handler(CommandHandler("start", self.comando_start))
        self.app.add_handler(CommandHandler("ayuda", self.comando_ayuda))
        self.app.add_handler(CommandHandler("status", self.comando_status))
        self.app.add_handler(CommandHandler("cargar_pdfs", self.comando_cargar_pdfs))
        self.app.add_handler(CommandHandler("analizar", self.comando_analizar))
        self.app.add_handler(CommandHandler("razonar", self.comando_razonar))
        self.app.add_handler(CommandHandler("estadisticas", self.comando_estadisticas))
        
        # Mensajes de texto
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_texto))
        
        # Imágenes
        self.app.add_handler(MessageHandler(filters.PHOTO, self.handle_imagen))
        
        self.logger.info("Handlers registrados correctamente")
    
    async def comando_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        mensaje = """
🤖 ¡Bienvenido al Bot Analista A&C!

Soy un bot especializado en análisis de datos financieros y documentos.
Mi "cerebro" fue entrenado con conocimiento de PDFs locales.
Mi "inteligencia" corre en motor de IA avanzado para razonamiento profundo.

📚 Mis capacidades:
• 📊 Análisis de datos en tiempo real
• 📄 Procesamiento de documentos PDF
• 🖼️ Análisis de imágenes y gráficas
• 🧠 Razonamiento lógico con IA avanzada
• 💡 Aprendizaje continuo basado en experiencias

🎯 Comandos principales:
• /ayuda - Muestra ayuda completa
• /razonar <pregunta> - Razonamiento con IA
• /status - Estado del bot
• /cargar_pdfs - Cargar PDFs al cerebro
• /estadisticas - Ver estadísticas

🚀 Prueba: /razonar ¿Cuál es la mejor estrategia de trading?
        """
        await update.message.reply_text(mensaje)
        self.logger.info(f"Usuario iniciado: {update.effective_user.first_name}")
    
    async def comando_ayuda(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /ayuda"""
        mensaje = """
📖 AYUDA - Bot Analista A&C

**MÓDULOS PRINCIPALES:**

🧠 **Cerebro (Knowledge Base)**
El bot cuenta con una base de conocimiento almacenada en PDFs locales.
Utiliza esta información para realizar análisis más certeros.

📊 **Análisis de Datos**
Puedes enviar datos en formato:
- Tendencias (al_alza/a_la_baja)
- Volatilidad (0-1)
- Valores (lista de números)

Ejemplo: /analizar

🖼️ **Procesamiento de Imágenes**
Envía una imagen o gráfica y el bot:
- Detectará texto (OCR)
- Identificará formas y patrones
- Clasificará el tipo de gráfico
- Analizará colores y composición

📄 **PDFs**
Coloca tus PDFs de entrenamiento en la carpeta "pdfs/"
Usa /cargar_pdfs para alimentar el cerebro del bot

🧠 **Motor de IA (NUEVO)**
Usa /razonar para acceder al motor de inteligencia artificial
El bot razonará usando tanto su cerebro (PDFs) como IA avanzada

**EJEMPLOS:**
1. Envía una imagen de una gráfica
2. Escribe datos para análisis
3. Usa /razonar para análisis profundos con IA
4. El bot responderá con análisis basado en su conocimiento

¿Necesitas algo específico?
        """
        await update.message.reply_text(mensaje)
    
    async def comando_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status"""
        await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
        
        estadisticas = self.knowledge_manager.obtener_estadisticas()
        reporte = self.analyzer.generar_reporte()
        
        mensaje = f"""
📊 **ESTADO DEL BOT**

🧠 **Cerebro:**
• Documentos cargados: {estadisticas.get('documentos_cargados', 0)}
• Conocimientos almacenados: {estadisticas.get('conocimientos_almacenados', 0)}
• Confianza promedio: {estadisticas.get('confianza_promedio', 0.0)}

📈 **Análisis:**
• Análisis realizados: {reporte.get('total_analisis_realizados', 0)}
• Confianza promedio: {reporte.get('confianza_promedio', 0.0)}
• Último análisis: {reporte.get('ultimo_analisis', 'N/A')}

✅ El bot está operativo y listo para análisis
        """
        await update.message.reply_text(mensaje)
        self.logger.info(f"Status consultado por {update.effective_user.first_name}")
    
    async def comando_cargar_pdfs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /cargar_pdfs"""
        await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
        
        self.logger.info("Iniciando carga de PDFs...")
        
        documentos = self.pdf_processor.procesar_todos_pdfs()
        
        if not documentos:
            mensaje = "❌ No se encontraron PDFs en la carpeta 'pdfs/'\n\nColoca tus PDFs en esa carpeta e intenta de nuevo."
            await update.message.reply_text(mensaje)
            self.logger.warning("No se encontraron PDFs para cargar")
            return
        
        # Cargar en la base de conocimiento
        for doc in documentos:
            self.knowledge_manager.cargar_documento(
                nombre=doc["nombre"],
                ruta=doc["ruta"],
                tipo="pdf",
                contenido=doc["texto_completo"]
            )
            
            # Agregar como conocimiento
            self.knowledge_manager.agregar_conocimiento(
                tema=doc["nombre"],
                contenido=doc["texto_completo"],
                relevancia=0.95
            )
        
        mensaje = f"""
✅ **PDFs Cargados Exitosamente**

📚 Documentos procesados: {len(documentos)}
{chr(10).join([f'• {doc["nombre"]} ({doc["total_paginas"]} páginas)' for doc in documentos])}

🧠 El cerebro del bot ha sido actualizado con este conocimiento.
        """
        await update.message.reply_text(mensaje)
        self.logger.info(f"Se cargaron {len(documentos)} PDFs exitosamente")
    
    async def comando_analizar(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /analizar"""
        mensaje = """
📊 **Modo Análisis**

¿Qué tipo de análisis deseas realizar?

1️⃣ Envía una imagen/gráfica para análisis visual
2️⃣ Envía datos en formato JSON para análisis cuantitativo
3️⃣ Escribe una consulta para búsqueda en la base de conocimiento

**Ejemplo de datos JSON:**
```
{
    "tendencia": "al_alza",
    "volatilidad": 0.15,
    "valores": [100, 105, 110, 108, 115]
}
```

¿Qué datos tienes?
        """
        await update.message.reply_text(mensaje)
    
    async def comando_estadisticas(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /estadisticas"""
        await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
        
        stats = self.knowledge_manager.obtener_estadisticas()
        reporte = self.analyzer.generar_reporte()
        
        mensaje = f"""
📈 **ESTADÍSTICAS DEL BOT**

**Base de Conocimiento:**
• Total de documentos: {stats.get('documentos_cargados', 0)}
• Conocimientos: {stats.get('conocimientos_almacenados', 0)}
• Confianza promedio: {stats.get('confianza_promedio', 0)}

**Análisis Realizados:**
• Total: {reporte.get('total_analisis_realizados', 0)}
• Confianza promedio: {reporte.get('confianza_promedio', 0)}
• Tipos: {reporte.get('distribucion_por_tipo', {})}

**Información del Sistema:**
• Base de datos: {str(self.settings.DATABASE_PATH)}
• PDFs almacenados: {str(self.settings.PDFS_DIR)}
        """
        await update.message.reply_text(mensaje)
    
    async def handle_texto(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja mensajes de texto"""
        await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
        
        texto = update.message.text
        self.logger.info(f"Mensaje recibido: {texto[:50]}...")
        
        # Intentar parsear como JSON
        try:
            import json
            datos = json.loads(texto)
            
            # Realizar análisis
            resultado = self.analyzer.analizar_datos(datos, contexto=texto)
            
            mensaje_respuesta = f"""
📊 **ANÁLISIS COMPLETADO**

**Hallazgos:**
{chr(10).join([f"• {h}" for h in resultado['hallazgos']])}

**Recomendaciones:**
{chr(10).join([f"• {r}" for r in resultado['recomendaciones']])}

**Confianza:** {resultado['confianza']:.0%}
**Fuentes utilizadas:** {', '.join(resultado['fuentes_utilizadas']) or 'Base general'}
            """
        except:
            # Búsqueda en conocimiento
            resultados = self.knowledge_manager.buscar_conocimiento(texto, limite=3)
            
            if resultados:
                mensaje_respuesta = f"""
🔍 **BÚSQUEDA EN CONOCIMIENTO**

Encontré {len(resultados)} resultado(s) relevante(s):

"""
                for i, res in enumerate(resultados, 1):
                    mensaje_respuesta += f"{i}. **{res['tema']}** (Relevancia: {res['relevancia']:.0%})\n"
                    contenido_preview = res['contenido'][:100] + "..." if len(res['contenido']) > 100 else res['contenido']
                    mensaje_respuesta += f"   {contenido_preview}\n\n"
            else:
                mensaje_respuesta = """
❌ No encontré información relevante sobre ese tema en mi base de conocimiento.

💡 Sugerencias:
• Carga más PDFs usando /cargar_pdfs
• Verifica que los PDFs contengan información sobre el tema
• Intenta con palabras clave diferentes
                """
        
        await update.message.reply_text(mensaje_respuesta)
    
    async def handle_imagen(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja imágenes enviadas"""
        await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
        
        try:
            # Descargar imagen
            photo = update.message.photo[-1]
            archivo = await context.bot.get_file(photo.file_id)
            
            # Guardar temporalmente
            ruta_temp = Path(self.settings.DATA_DIR) / f"temp_{photo.file_id}.jpg"
            await archivo.download_to_drive(ruta_temp)
            
            # Validar
            es_valida, msg = validate_image(str(ruta_temp))
            if not es_valida:
                await update.message.reply_text(f"❌ Imagen no válida: {msg}")
                ruta_temp.unlink()
                return
            
            # Analizar imagen
            analisis = self.image_processor.analisis_completo_imagen(str(ruta_temp))
            
            # Preparar respuesta
            mensaje = """
🖼️ **ANÁLISIS DE IMAGEN**

**Dimensiones:** {0}x{1}px
            """.format(analisis['dimensiones'][0], analisis['dimensiones'][1])
            
            # Texto OCR
            if analisis['texto_extraido']:
                texto_preview = analisis['texto_extraido'][:100] + "..." if len(analisis['texto_extraido']) > 100 else analisis['texto_extraido']
                mensaje += f"\n**Texto detectado:**\n```{texto_preview}```"
            
            # Tipo de gráfico
            if analisis['tipo_grafico'].get('tipo_grafico_probable'):
                mensaje += f"\n**Tipo de gráfico:** {analisis['tipo_grafico']['tipo_grafico_probable']}"
                mensaje += f"\n**Confianza:** {analisis['tipo_grafico']['confianza']:.0%}"
            
            # Formas
            if analisis['formas_detectadas'].get('total_contornos'):
                fd = analisis['formas_detectadas']
                mensaje += f"\n**Formas detectadas:**"
                if fd['rectangulos'] > 0:
                    mensaje += f"\n• Rectángulos: {fd['rectangulos']}"
                if fd['circulos'] > 0:
                    mensaje += f"\n• Círculos: {fd['circulos']}"
                if fd['triangulos'] > 0:
                    mensaje += f"\n• Triángulos: {fd['triangulos']}"
            
            # Análisis de colores
            if analisis['analisis_colores']:
                ac = analisis['analisis_colores']
                mensaje += f"\n**Análisis de colores:**"
                mensaje += f"\n• Colores dominantes: {ac['colores_dominantes']}"
                mensaje += f"\n• Brillo promedio: {ac['brillo_promedio']:.0%}"
            
            await update.message.reply_text(mensaje)
            
            # Limpiar
            ruta_temp.unlink()
            
            self.logger.info("Imagen analizada exitosamente")
            
        except Exception as e:
            self.logger.error(f"Error procesando imagen: {str(e)}")
            await update.message.reply_text(f"❌ Error procesando imagen: {str(e)}")
    
    async def comando_razonar(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /razonar - Usa el motor de IA para razonamiento lógico"""
        await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
        
        # Obtener la pregunta del comando
        # Los argumentos pueden venir en context.args o en el texto después del comando
        if not context.args:
            mensaje = """
❓ **Comando /razonar**

Uso: `/razonar <tu pregunta>`

Ejemplo:
`/razonar ¿Cuál es la mejor estrategia de entrada al mercado?`

Este comando usa el motor de IA con el conocimiento de los PDFs cargados para darte análisis profundos y razonado.
            """
            await update.message.reply_text(mensaje)
            return
        
        pregunta = " ".join(context.args) if context.args else ""
        
        # Si no hay pregunta, intentar obtenerla del mensaje completo
        if not pregunta and update.message.text:
            # Remover el comando del texto
            pregunta = update.message.text.replace("/razonar", "").strip()
        
        if not pregunta:
            await update.message.reply_text("❌ Por favor, proporciona una pregunta. Ejemplo: `/razonar ¿Qué es el análisis técnico?`")
            return
        self.logger.info(f"Razonamiento solicitado: {pregunta[:50]}...")
        
        # Obtener contexto del cerebro (PDFs)
        documentos_relevantes = self.knowledge_manager.buscar_conocimiento(pregunta, limite=3)
        contexto = ""
        
        if documentos_relevantes:
            contexto = "\n".join([
                f"📖 {doc['documento']}: {doc['contenido'][:200]}..."
                for doc in documentos_relevantes
            ])
        
        # Usar motor de IA (PILAR INDEPENDIENTE)
        resultado = self.ai_engine.razonar(
            pregunta=pregunta,
            contexto=contexto
        )
        
        if resultado.get("error"):
            mensaje = f"❌ {resultado['respuesta']}"
        else:
            respuesta = resultado.get("respuesta", "Sin respuesta")
            
            # Limitar a 4096 caracteres (límite de Telegram)
            if len(respuesta) > 4000:
                respuesta = respuesta[:3997] + "..."
            
            confianza = resultado.get("confianza", 0.0)
            modelo = resultado.get("modelo", "desconocido")
            tokens = resultado.get("tokens_usados", 0)
            
            mensaje = f"""
🧠 **ANÁLISIS CON IA**

**Pregunta:**
{pregunta}

**Respuesta:**
{respuesta}

---
📊 **Metadata:**
• Confianza: {confianza:.0%}
• Modelo: {modelo}
• Tokens usados: {tokens}
• Basado en conocimiento de PDFs cargados
            """
        
        await update.message.reply_text(mensaje)
        self.logger.info(f"Razonamiento completado con confianza {resultado.get('confianza', 0):.0%}")
    
    def iniciar(self):
        """Inicia el bot"""
        self.logger.info("🚀 Iniciando bot de Telegram...")
        print("=" * 50)
        print("🤖 BOT ANALISTA A&C")
        print("=" * 50)
        self.settings.mostrar_configuracion()
        print("✅ Bot en funcionamiento. Presiona Ctrl+C para detener.")
        print("=" * 50)
        
        self.app.run_polling()
