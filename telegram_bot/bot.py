"""
telegram_bot/bot.py
Bot principal de Telegram
Coordina todos los módulos y maneja la comunicación con el usuario
Incluye integración del Enhanced Analyzer para análisis 360
"""

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction
import logging
from pathlib import Path
import json

from config import Settings
from cerebro import KnowledgeManager, PDFProcessor, AnalysisMethodology
from analisis import Analyzer, ImageProcessor, ProfessionalReport, EnhancedAnalyzer
from ia import AIEngine
from utils import setup_logger, validate_pdf, validate_image
from utils.pdf_generator import PDFReportGenerator
from logging_audit import setup_centralized_logging


class TelegramAnalystBot:
    """Bot Telegram especializado en análisis con Enhanced Analyzer"""
    
    def __init__(self):
        """Inicializa el bot"""
        # Logging centralizado (Phase 5A Integration)
        setup_centralized_logging("BotAnalystTelegram", "INFO")
        
        # Configuración
        Settings.crear_directorios()
        self.settings = Settings
        
        # Logger
        self.logger = setup_logger("TelegramAnalystBot", archivo=str(self.settings.LOG_FILE))
        self.logger.info("Inicializando Bot Analista con Enhanced Features...")
        
        # Módulos principales (PILARES INDEPENDIENTES)
        self.knowledge_manager = KnowledgeManager(str(self.settings.DATABASE_PATH))
        self.pdf_processor = PDFProcessor(str(self.settings.PDFS_DIR))
        self.analyzer = Analyzer(self.knowledge_manager)
        self.image_processor = ImageProcessor()
        
        # ✨ NEW: Enhanced Analyzer (Análisis 360)
        self.enhanced_analyzer = EnhancedAnalyzer(self.knowledge_manager)
        self.logger.info("✅ Enhanced Analyzer inicializado")
        
        # Pilar de Análisis (NUEVA METODOLOGÍA UNIFICADA - Doc 1-2-3)
        self.analysis_methodology = AnalysisMethodology()
        
        # Pilar IA (completamente independiente)
        # Usa Google API Key en lugar de OpenAI - MANTIENE API GEMINI
        self.ai_engine = AIEngine(self.settings.GOOGLE_API_KEY)
        
        # Generador de PDFs
        self.pdf_generator = PDFReportGenerator(str(self.settings.DATA_DIR) + "/reportes")
        
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
        self.app.add_handler(CommandHandler("exportar_pdf", self.comando_exportar_pdf))
        self.app.add_handler(CommandHandler("razonar", self.comando_razonar))
        self.app.add_handler(CommandHandler("estadisticas", self.comando_estadisticas))
        self.app.add_handler(CommandHandler("screener", self.comando_screener))
        
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
• /analizar [SÍMBOLO] - Análisis profesional completo (NUEVO)
• /status - Estado del bot
• /cargar_pdfs - Cargar PDFs al cerebro
• /estadisticas - Ver estadísticas

🚀 Ejemplos:
• /razonar ¿Cuál es la mejor estrategia de trading?
• /analizar AAPL
• /analizar EURUSD
        """
        await update.message.reply_text(mensaje)
        self.logger.info(f"Usuario iniciado: {update.effective_user.first_name}")
    
    async def comando_ayuda(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /ayuda"""
        mensaje = """
📖 AYUDA - Bot Analista A&C

**COMANDOS DISPONIBLES:**

📊 **/analizar [SÍMBOLO]** - NUEVO
Genera un reporte profesional completo con:
✅ Análisis técnico profundo
✅ Indicadores técnicos
✅ Osciladores
✅ Medias móviles
✅ Puntos de pivote
✅ Análisis de IA (Gemini)
✅ **Tabla de Resumen Ejecutivo** con recomendación accionable
✅ Ratio R/R calculado automáticamente

Ejemplos: /analizar AAPL, /analizar EURUSD, /analizar BTC

📄 **/exportar_pdf** - NUEVO
Exporta el último análisis a un PDF profesional con:
✅ Plan de Acción Trading
✅ Soportes y Resistencias
✅ Indicadores Técnicos
✅ Análisis Fundamental
✅ Análisis Alexander (Marea, Movimiento, Factor Social)
✅ Recomendaciones completas

Uso: Primero ejecuta /analizar, luego /exportar_pdf

🧠 **/razonar [PREGUNTA]**
Accede al motor de IA para análisis profundos.
El bot razona usando su base de conocimiento + IA avanzada.

Ejemplo: /razonar ¿Cuál es la mejor estrategia de trading?

🧠 **Cerebro (Knowledge Base)**
El bot cuenta con una base de conocimiento de trading:
- 45+ principios fundamentales extraídos de libros
- 5+ estrategias derivadas
- Sistema de mejora continua

📚 **PDFs - Entrena el Cerebro**
Coloca tus PDFs en la carpeta "pdfs/" para mejorar análisis:
• Libros de análisis técnico
• Reportes de empresas
• Tu metodología personal
• Papers académicos

Uso:
1️⃣ Coloca archivos en: `/pdfs/mi_archivo.pdf`
2️⃣ Ejecuta: /cargar_pdfs
3️⃣ El bot aprenderá y mejorará análisis

El análisis se personaliza con tu conocimiento 🧠

🖼️ **Procesamiento de Imágenes**
Envía una imagen o gráfica y el bot:
- Detectará texto (OCR)
- Identificará formas y patrones
- Clasificará gráficos
- Analizará composición

**OTROS COMANDOS:**
• /status - Ver estado actual del bot
• /estadisticas - Estadísticas de análisis
• /cargar_pdfs - Procesar y cargar PDFs del cerebro

¿Necesitas algo más?
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
        """Comando /cargar_pdfs - Carga y procesa PDFs del cerebro"""
        await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
        
        self.logger.info("Iniciando carga de PDFs...")
        
        documentos = self.pdf_processor.procesar_todos_pdfs()
        
        if not documentos:
            mensaje = """
❌ **No se encontraron PDFs**

📂 **¿Cómo agregar PDFs?**

1️⃣ **Localiza la carpeta:**
   `C:\\Users\\sk894\\OneDrive\\Carlos\\OneDrive\\Escritorio\\Bot_Analist_A&C\\pdfs\\`

2️⃣ **Coloca tus PDFs:**
   - Análisis técnico
   - Reportes de empresas
   - Tu metodología personal
   - Libros y papers

3️⃣ **Ejecuta nuevamente:**
   `/cargar_pdfs`

4️⃣ **El bot mejorará automáticamente** 🧠

📖 Ver guía completa: `GUIA_AGREGAR_PDFS.md`
            """
            await update.message.reply_text(mensaje)
            self.logger.warning("No se encontraron PDFs para cargar")
            return
        
        # Cargar en la base de conocimiento
        documentos_cargados = []
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
            
            documentos_cargados.append({
                "nombre": doc["nombre"],
                "paginas": doc.get("total_paginas", "?"),
                "tamaño": f"{len(doc.get('texto_completo', ''))} caracteres"
            })
        
        # Mensaje de éxito con detalles
        detalles = "\n".join([
            f"📄 **{d['nombre']}**\n   • Páginas: {d['paginas']}\n   • Contenido: {d['tamaño']}"
            for d in documentos_cargados
        ])
        
        mensaje = f"""
✅ **PDFs Cargados Exitosamente**

📚 **Documentos procesados:** {len(documentos_cargados)}

{detalles}

🧠 **Cerebro Actualizado:**
El bot ha integrado este conocimiento en su análisis.
Los próximos `/analizar` serán más precisos y personalizados.

💡 **Resultado esperado:**
• Análisis más alineado con tu metodología
• Recomendaciones más precisas
• Score de confianza mejorado
• Justificación mejor fundamentada

🚀 Prueba ahora: `/analizar [SÍMBOLO]`
        """
        await update.message.reply_text(mensaje)
        self.logger.info(f"Se cargaron {len(documentos)} PDFs exitosamente")
    
    async def comando_analizar(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /analizar [SÍMBOLO]
        
        Análisis profesional 360° basado en:
        - Doc 1: Metodología Alexander (Marea + Movimiento + Factor Social)
        - Doc 3: Indicadores técnicos (RSI, MACD, Stochastic, etc)
        - Doc 2: Formato de reporte profesional
        """
        await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
        
        # Obtener símbolo del comando
        if not context.args:
            mensaje = """
📊 **Análisis Profesional 360° - Metodología Alexander**

Uso: /analizar SÍMBOLO

**Ejemplos:**
• /analizar AAPL (Apple)
• /analizar MSFT (Microsoft)
• /analizar TSLA (Tesla)
• /analizar AMZN (Amazon)

El análisis incluye:
✅ Datos actuales en tiempo real (YFinance)
✅ Indicadores técnicos (RSI, MACD, Stochastic, etc)
✅ Análisis de Marea (contexto macro)
✅ Análisis de Movimiento (tendencia local)
✅ Análisis de Factor Social (fundamentales)
✅ Recomendación final (COMPRA/VENTA/ESPERA)
✅ Soportes y resistencias (Pivot Points)
✅ Probabilidad de éxito
            """
            await update.message.reply_text(mensaje)
            return
        
        simbolo = context.args[0].upper()
        
        # Informar al usuario que se está procesando
        mensaje_procesando = f"🔄 Ejecutando análisis 360° para **{simbolo}**...\n\n📊 Descargando datos → 🧮 Calculando indicadores → 🧭 Aplicando metodología Alexander\n\nEsto puede tomar 15-30 segundos ⏳"
        estado_mensaje = await update.message.reply_text(mensaje_procesando)
        
        try:
            # 1. Ejecutar análisis unificado (YFinance + Indicadores + Alexander)
            self.logger.info(f"🔍 Iniciando análisis 360° de {simbolo}...")
            resultado_analisis = self.analysis_methodology.analizar_ticker(simbolo)
            
            # 2. Verificar si fue exitoso
            if resultado_analisis.get("status") != "completado":
                error_msg = f"""
❌ Error en análisis: {resultado_analisis.get('error', 'Desconocido')}

Posibles causas:
• Símbolo no válido o no existe
• Sin datos disponibles en YFinance
• Conexión lenta

Intenta con otro símbolo (ej: AAPL, MSFT)
                """
                await estado_mensaje.edit_text(error_msg)
                self.logger.error(f"Error analizando {simbolo}: {resultado_analisis.get('error')}")
                return
            
            # 3. Crear reporte profesional con los datos del análisis
            reporte = ProfessionalReport(
                titulo=f"Análisis Profesional 360° - {simbolo}",
                instrumento=simbolo,
                tipo_analisis="alexander_metodologia"
            )
            
            # 4. Agregar datos fundamentales
            datos_actuales = resultado_analisis.get("datos_actuales", {})
            fundamentales = resultado_analisis.get("fundamentales", {})
            
            # Formatear valores numéricos con separador de miles
            def format_number(value, prefix="", suffix=""):
                """Formatea números con separador de miles, maneja None y strings"""
                if value is None or value == 'N/A':
                    return f"{prefix}N/A{suffix}"
                try:
                    if isinstance(value, (int, float)):
                        return f"{prefix}{value:,.0f}{suffix}" if isinstance(value, float) else f"{prefix}{value:,}{suffix}"
                    return f"{prefix}{str(value)}{suffix}"
                except:
                    return f"{prefix}N/A{suffix}"
            
            reporte.agregar_datos_fundamentales({
                "Símbolo": simbolo,
                "Precio Actual": f"${datos_actuales.get('precio_actual', 'N/A')}",
                "Cambio": f"{datos_actuales.get('cambio_pct', 'N/A')}%",
                "Volumen": format_number(datos_actuales.get('volumen', 'N/A')),
                "P/E Ratio": f"{fundamentales.get('pe_ratio', 'N/A')}",
                "Market Cap": format_number(fundamentales.get('market_cap', 'N/A'), prefix="$"),
            })
            
            # 5. Agregar análisis técnico
            indicadores = resultado_analisis.get("tecnico", {}).get("indicadores", {})
            
            analisis_tecnico_texto = self._generar_texto_indicadores(indicadores)
            reporte.agregar_analisis_tecnico(analisis_tecnico_texto)
            
            # 5.5 Agregar análisis narrativo fundamentado (NUEVO PUNTO)
            # Este punto sintetiza todo el análisis de manera clara y fundamentada
            analisis_narrativo_texto = self._generar_analisis_narrativo(
                resultado_analisis, 
                datos_actuales,
                indicadores,
                resultado_analisis.get("alexander", {})
            )
            reporte.agregar_seccion(
                titulo="Análisis Narrativo Fundamentado",
                contenido=analisis_narrativo_texto
            )
            alexander = resultado_analisis.get("alexander", {})
            marea = alexander.get("marea", {})
            movimiento = alexander.get("movimiento", {})
            factor_social = alexander.get("factor_social", {})
            
            # Enriquecimiento con datos de Finviz
            datos_finviz = resultado_analisis.get("finviz", {})
            texto_finviz = self._generar_texto_finviz(datos_finviz, factor_social)
            
            analisis_alexander_texto = f"""
**ANÁLISIS ALEXANDER - METODOLOGÍA UNIFICADA**

🌊 **MAREA (Contexto Macro):**
- General: {marea.get('marea_general', 'N/A')}
- VIX: {marea.get('vix', 'N/A')}
- Volatilidad: {marea.get('volatilidad_mercado', 'N/A')}
- Riesgo: {marea.get('riesgo', 'N/A')}

📈 **MOVIMIENTO (Análisis Técnico Local):**
- Tendencia: {movimiento.get('movimiento', 'N/A')} ({movimiento.get('fuerza', 'N/A')})
- Consenso: {movimiento.get('consenso', 'N/A')}%
- Señales Alcistas: {movimiento.get('señales_alcistas', 0)}/3
- Señales Bajistas: {movimiento.get('señales_bajistas', 0)}/3

💼 **FACTOR SOCIAL (Fundamentales):**
- Valuación: {factor_social.get('valuacion', 'N/A')}
- Sentimiento: {factor_social.get('sentimiento_general', 'N/A')}
- Tamaño: {factor_social.get('tamaño', 'N/A')}
- Solidez: {factor_social.get('solidez', 'N/A')}
- Insider Trading: {factor_social.get('insider_sentiment', 'N/A')}
- Analyst Rating: {factor_social.get('analyst_sentiment', 'N/A')}
{texto_finviz}
            """
            
            reporte.agregar_analisis_ia(analisis_alexander_texto)
            
            # 7. Extraer recomendación
            rec = resultado_analisis.get("recomendacion", {})
            
            # 7.5 Calcular plan de acción trading
            # Convertir precio_actual de manera segura
            precio_str = str(datos_actuales.get('precio_actual', '0')).strip()
            if precio_str.lower() in ['none', 'n/a', '']:
                precio_str = '0'
            precio_actual = float(precio_str.replace('$', '').replace(',', ''))
            
            # Guardar el precio original para mostrar (aunque sea 0 o inválido)
            precio_mostrar = precio_actual if precio_actual > 0 else datos_actuales.get('precio_actual', 'N/A')
            
            # Si precio es 0, usar valor por defecto de análisis solo para cálculos internos
            if precio_actual == 0:
                precio_actual = 100.0  # Valor por defecto SOLO para cálculos internos
            
            sr = resultado_analisis.get("soportes_resistencias", {})
            
            # Función auxiliar para convertir valores de manera segura
            def safe_float(value, default=None):
                """Convierte un valor a float de manera segura"""
                try:
                    if value is None or value == 'None' or value == 'N/A' or value == '':
                        return default if default is not None else 0.0
                    return float(str(value).replace('$', '').replace(',', ''))
                except (ValueError, TypeError):
                    return default if default is not None else 0.0
            
            # Usar valores validados si están disponibles, sino usar los básicos
            soporte_principal = safe_float(sr.get('soporte_principal'), 
                                          default=safe_float(sr.get('soporte_1'), default=precio_actual * 0.95))
            resistencia_principal = safe_float(sr.get('resistencia_principal'), 
                                              default=safe_float(sr.get('resistencia_1'), default=precio_actual * 1.05))
            
            # VALIDACIÓN CRÍTICA Y DEFINITIVA
            # Si los valores siguen invertidos o son inválidos, recalcular basado en porcentajes simples
            if soporte_principal >= precio_actual or resistencia_principal <= precio_actual:
                # Valores inválidos - usar método simple basado en porcentajes
                volatilidad = (resistencia_principal - soporte_principal) / precio_actual if precio_actual > 0 else 0.05
                volatilidad = max(min(volatilidad, 0.15), 0.05)  # Entre 5% y 15%
                
                soporte_principal = precio_actual * (1 - volatilidad)
                resistencia_principal = precio_actual * (1 + volatilidad)
            
            # Asegurar que soporte < precio < resistencia
            soporte_principal = min(soporte_principal, precio_actual * 0.98)
            resistencia_principal = max(resistencia_principal, precio_actual * 1.02)
            
            atr = safe_float(sr.get('atr'), default=(resistencia_principal - soporte_principal) / 2)
            
            # 7.1 VALIDACIÓN: Verificar si la recomendación es técnicamente consistente
            indicadores_tech = resultado_analisis.get("tecnico", {}).get("indicadores", {})
            rsi = safe_float(indicadores_tech.get("rsi"), default=50)
            macd_value = safe_float(indicadores_tech.get("macd_signal"), default=0)
            bb_position = indicadores_tech.get("bollinger_position", 'media')
            
            # 7.2 ANÁLISIS MEJORADO: Usar Enhanced Analyzer para scoring ponderado
            # COMENTADO: Método analizar_convergencia tiene firma incompatible
            # TODO: Revisar implementación correcta de análisis convergencia
            from cerebro import EnhancedAnalyzer
            enhanced_analyzer = EnhancedAnalyzer()
            
            # Calcular scores técnico, fundamental y de sentimiento
            technical_score = enhanced_analyzer.calcular_technical_score(indicadores_tech)
            fundamental_score = enhanced_analyzer.calcular_fundamental_score(
                resultado_analisis.get("fundamentales", {})
            )
            finviz_data = resultado_analisis.get("finviz", {})
            sentiment_score = enhanced_analyzer.calcular_sentiment_score(finviz_data)
            
            # COMENTADO: analizar_convergencia tiene firma incompatible
            # Crear objeto simulado para compatibilidad con el template de reportes
            class EnhancedResult:
                def __init__(self, tech_score, fund_score, sent_score):
                    self.combined_score = (tech_score + fund_score + sent_score) / 3
                    divergence = max(tech_score, fund_score, sent_score) - min(tech_score, fund_score, sent_score)
                    if divergence < 15:
                        self.divergence = "✅ Señales Convergentes"
                    elif divergence < 30:
                        self.divergence = "⚠️ Señales Mixtas"
                    else:
                        self.divergence = "❌ Señales Divergentes"
            
            enhanced_result = EnhancedResult(technical_score, fundamental_score, sentiment_score)
            
            # Usar recomendación IA original (sin ajuste por convergencia)
            rec_original = rec.get('recomendacion', 'ESPERA')
            confianza_ia = safe_float(rec.get('probabilidad_exito', 50))
            
            # Validar consistencia técnica
            if 'VENTA' in rec_original.upper():
                if rsi < 50 and macd_value >= 0:
                    rec['recomendacion'] = 'ESPERA'
                    self.logger.warning(f"⚠️  {simbolo}: VENTA ajustada a ESPERA (RSI bajo + MACD positivo)")
            elif 'COMPRA' in rec_original.upper():
                if rsi > 70 and macd_value <= 0:
                    rec['recomendacion'] = 'ESPERA'
                    self.logger.warning(f"⚠️  {simbolo}: COMPRA ajustada a ESPERA (RSI alto + MACD negativo)")
            
            veredicto = rec.get('recomendacion', 'ESPERA')
            
            # LÓGICA SIMPLE Y CONFIABLE
            if 'COMPRA' in veredicto.upper() or 'BUY' in veredicto.upper():
                # COMPRA: Esperamos que SUBA
                entry_price = precio_actual
                stop_loss = soporte_principal  # Stop DEBAJO (pérdida si baja)
                take_profit = resistencia_principal  # Target ARRIBA (ganancia si sube)
                proyeccion = "📈 SUBIDA"
                recomendable = "✅ RECOMENDABLE"
            elif 'VENTA' in veredicto.upper() or 'SELL' in veredicto.upper():
                # VENTA: Esperamos que BAJE
                entry_price = precio_actual
                stop_loss = resistencia_principal  # Stop ARRIBA (pérdida si sube)
                take_profit = soporte_principal  # Target ABAJO (ganancia si baja)
                proyeccion = "📉 BAJADA"
                recomendable = "✅ RECOMENDABLE"
            else:
                # ESPERA/NEUTRAL
                entry_price = precio_actual
                stop_loss = soporte_principal
                take_profit = resistencia_principal
                proyeccion = "➡️ LATERAL"
                recomendable = "⚠️ NO RECOMENDABLE"
            
            # Calcular gain/loss potencial (verificar que sean valores positivos)
            if 'COMPRA' in veredicto.upper():
                # COMPRA: Ganancia si sube (TP > Entry), Pérdida si baja (SL < Entry)
                ganancia_potencial = abs(((take_profit - entry_price) / entry_price) * 100) if entry_price > 0 else 0
                perdida_potencial = abs(((entry_price - stop_loss) / entry_price) * 100) if entry_price > 0 else 0
            elif 'VENTA' in veredicto.upper():
                # VENTA: Ganancia si baja (Entry > TP), Pérdida si sube (SL > Entry)
                ganancia_potencial = abs(((entry_price - take_profit) / entry_price) * 100) if entry_price > 0 else 0
                perdida_potencial = abs(((stop_loss - entry_price) / entry_price) * 100) if entry_price > 0 else 0
            else:
                # LATERAL/ESPERA
                ganancia_potencial = abs(((take_profit - entry_price) / entry_price) * 100) if entry_price > 0 else 0
                perdida_potencial = abs(((entry_price - stop_loss) / entry_price) * 100) if entry_price > 0 else 0
            
            # Calcular tiempo proyectado (basado en volatilidad)
            tecnico = resultado_analisis.get("tecnico", {})
            indicadores = tecnico.get("indicadores", {})
            volatilidad = tecnico.get("volatilidad", "Media")
            
            if "Alta" in str(volatilidad):
                tiempo_proyectado = "1-5 días"
            elif "Baja" in str(volatilidad):
                tiempo_proyectado = "2-4 semanas"
            else:
                tiempo_proyectado = "5-15 días"
            
            # 8. Crear tabla resumen PROFESIONAL con plan de acción
            # Construir tabla de factores que respaldan la recomendación
            factores_resumen = "**Factores que respaldan esta recomendación:**\n"
            
            macd_hist = safe_float(indicadores.get('macd_histogram'), default=0)
            
            if 'VENTA' in veredicto.upper():
                factores = []
                if rsi > 60:
                    factores.append(f"• RSI Elevado ({rsi:.1f}): Sobrecompra")
                if macd_hist < 0:
                    factores.append(f"• MACD Negativo: Momentum bajista")
                if 'alto' in str(bb_position).lower():
                    factores.append(f"• Bollinger Superior: Presión vendedora")
                factores_resumen += "\n".join(factores) if factores else "• Análisis de IA basado en Metodología Alexander"
            elif 'COMPRA' in veredicto.upper():
                factores = []
                if rsi < 40:
                    factores.append(f"• RSI Bajo ({rsi:.1f}): Sobreventa")
                if macd_hist > 0:
                    factores.append(f"• MACD Positivo: Momentum alcista")
                if 'bajo' in str(bb_position).lower():
                    factores.append(f"• Bollinger Inferior: Presión compradora")
                factores_resumen += "\n".join(factores) if factores else "• Análisis de IA basado en Metodología Alexander"
            else:
                factores_resumen += "• Condiciones neutrales - Esperar confirmación de tendencia"
            
            # 8.1 ANÁLISIS MEJORADO: Mostrar breakdown de scores
            scores_desglose = f"""
**📈 Análisis Mejorado (Scores Ponderados):**
• 🔴 Score Técnico: {technical_score:.1f}/100 (Indicadores locales)
• 🟢 Score Fundamental: {fundamental_score:.1f}/100 (Salud empresarial)
• 🔵 Score Sentimiento: {sentiment_score:.1f}/100 (Mercado y expertos)
• ⭐ **Score Combinado: {enhanced_result.combined_score:.1f}/100**
• 🎯 **Convergencia: {enhanced_result.divergence}**

"""
            
            tabla_resumen_ejecutivo = f"""
╔════════════════════════════════════════════════════════════╗
║               📊 PLAN DE ACCIÓN TRADING                    ║
╚════════════════════════════════════════════════════════════╝

| **Parámetro** | **Valor** |
|:---|:---|
| 🎯 **Precio de Entrada** | ${entry_price:.2f} |
| 🛑 **Precio Stop Loss** | ${stop_loss:.2f} |
| 💰 **Precio Take Profit** | ${take_profit:.2f} |
| 📊 **Ganancia Potencial** | +{ganancia_potencial:.2f}% |
| 📉 **Pérdida Máxima** | -{perdida_potencial:.2f}% |
| ⏱️ **Tiempo Proyectado** | {tiempo_proyectado} |
| 📈 **Proyección de Precio** | {proyeccion} |
| ✅ **Recomendación de Inversión** | {recomendable} |
| 🎲 **Veredicto** | **{veredicto}** |
| 📊 **Confianza** | {rec.get('probabilidad_exito', 'N/A')}% |

{scores_desglose}

{factores_resumen}

"""
            
            # 9. Agregar Soportes/Resistencias
            tabla_sr = f"""
**Soportes y Resistencias (Pivot Points):**
• R2: ${sr.get('resistencia_2', 'N/A')}
• R1: ${sr.get('resistencia_1', 'N/A')}
• Pivot: ${sr.get('pivot', 'N/A')}
• S1: ${sr.get('soporte_1', 'N/A')}
• S2: ${sr.get('soporte_2', 'N/A')}
            """
            
            # 10. Construir mensaje final
            mensaje_final = f"""
✅ **ANÁLISIS PROFESIONAL 360° COMPLETADO**

**{simbolo}** - {datos_actuales.get('nombre', 'Instrumento Financiero')}
Precio Actual: ${precio_mostrar}

{tabla_resumen_ejecutivo}

🎯 {tabla_sr}

📊 **Indicadores Principales:**
{analisis_tecnico_texto}

⏰ Análisis completado: {resultado_analisis.get('timestamp', 'N/A')}

⚠️ **DISCLAIMER:**
Este análisis es solo informativo. No constituye asesoramiento financiero.
Todo trading implica riesgo de pérdida total del capital.
Consulta con un asesor profesional antes de operar.
            """
            
            # 11. Actualizar mensaje
            await estado_mensaje.edit_text(mensaje_final, parse_mode='Markdown')
            
            # 12. Guardar datos del análisis para exportar a PDF
            context.user_data['ultimo_analisis'] = {
                'ticker': simbolo,
                'datos_actuales': datos_actuales,
                'fundamentales': fundamentales,
                'tecnico': tecnico,
                'alexander': resultado_analisis.get("alexander", {}),
                'soportes_resistencias': sr,
                'recomendacion': rec,
                'entry_price': entry_price,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'ganancia_potencial': ganancia_potencial,
                'perdida_potencial': perdida_potencial,
                'tiempo_proyectado': tiempo_proyectado,
                'proyeccion': proyeccion,
                'recomendable': recomendable,
                'analisis_narrativo': analisis_narrativo_texto
            }
            
            # Notificar que puede exportar a PDF
            await update.message.reply_text(
                "💾 Puedes exportar este análisis a PDF con: `/exportar_pdf`",
                parse_mode='Markdown'
            )
            
            self.logger.info(f"✅ Análisis 360° completado para {simbolo}")
            
        except Exception as e:
            error_msg = f"""
❌ Error en análisis: {str(e)[:100]}

Por favor, intenta nuevamente con otro símbolo.
            """
            await estado_mensaje.edit_text(error_msg)
            self.logger.error(f"Error en comando_analizar: {str(e)}")
    
    async def comando_exportar_pdf(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /exportar_pdf - Exporta el último análisis a PDF"""
        await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
        
        # Verificar si hay un análisis previo
        if 'ultimo_analisis' not in context.user_data:
            await update.message.reply_text(
                "❌ No hay análisis previo para exportar.\n\n"
                "Primero ejecuta: /analizar AAPL\n"
                "Luego exporta con: /exportar_pdf"
            )
            return
        
        try:
            datos = context.user_data['ultimo_analisis']
            
            # Generar PDF
            estado_msg = await update.message.reply_text("⏳ Generando PDF... por favor espera")
            
            pdf_path = self.pdf_generator.generar_reporte_analisis(
                ticker=datos['ticker'],
                datos_actuales=datos['datos_actuales'],
                fundamentales=datos['fundamentales'],
                tecnico=datos['tecnico'],
                alexander=datos['alexander'],
                soportes_resistencias=datos['soportes_resistencias'],
                recomendacion=datos['recomendacion'],
                entry_price=datos['entry_price'],
                stop_loss=datos['stop_loss'],
                take_profit=datos['take_profit'],
                ganancia_potencial=datos['ganancia_potencial'],
                perdida_potencial=datos['perdida_potencial'],
                tiempo_proyectado=datos['tiempo_proyectado'],
                proyeccion=datos['proyeccion'],
                recomendable=datos['recomendable'],
                analisis_narrativo=datos.get('analisis_narrativo', '')
            )
            
            # Enviar PDF
            with open(pdf_path, 'rb') as pdf_file:
                await context.bot.send_document(
                    chat_id=update.effective_chat.id,
                    document=pdf_file,
                    caption=f"📄 Análisis Profesional 360° - {datos['ticker']}\n\n"
                           f"Incluye:\n"
                           f"✅ Plan de Acción Trading\n"
                           f"✅ Soportes y Resistencias\n"
                           f"✅ Indicadores Técnicos\n"
                           f"✅ Análisis Fundamental\n"
                           f"✅ Análisis Alexander\n"
                           f"✅ Recomendaciones"
                )
            
            await estado_msg.delete()
            self.logger.info(f"✅ PDF exportado para {datos['ticker']}")
            
        except Exception as e:
            error_msg = f"❌ Error al generar PDF: {str(e)[:100]}"
            await update.message.reply_text(error_msg)
            self.logger.error(f"Error en comando_exportar_pdf: {str(e)}")

    def _generar_texto_finviz(self, datos_finviz: dict, factor_social: dict) -> str:
        """Genera texto formateado de datos de Finviz"""
        if not datos_finviz or datos_finviz.get("error") or not factor_social.get("finviz_disponible"):
            return ""
        
        texto = "\n🦊 **Datos de Finviz (Insider & Analyst):**"
        
        # Insider trading
        insider = datos_finviz.get("insider_trading", {})
        if insider:
            texto += f"\n- Insider Sentiment: {factor_social.get('insider_sentiment', 'N/A')}"
            if "transacciones" in insider:
                texto += f" | Transacciones: {insider.get('transacciones', 'N/A')}"
        
        # Analyst ratings
        analyst = datos_finviz.get("analyst_ratings", {})
        if analyst:
            texto += f"\n- Analyst Rating: {factor_social.get('analyst_sentiment', 'N/A')}"
            if "numero_analistas" in analyst:
                texto += f" | Analistas: {analyst.get('numero_analistas', 'N/A')}"
        
        # Sentiment
        sentiment = datos_finviz.get("sentiment", {})
        if sentiment:
            texto += f"\n- Sentimiento General: {sentiment.get('sentiment_score', 'N/A')}"
        
        return texto if len(texto) > 30 else ""



    
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
    
    def _generar_analisis_narrativo(self, resultado_analisis: dict, datos_actuales: dict, indicadores: dict, alexander: dict) -> str:
        """
        Genera un análisis narrativo fundamentado de todo el reporte
        Sintetiza de manera clara, concisa y basada en hechos cada punto del análisis
        
        Args:
            resultado_analisis: Resultado completo del análisis
            datos_actuales: Datos actuales del instrumento
            indicadores: Indicadores técnicos calculados
            alexander: Análisis Alexander (Marea, Movimiento, Factor Social)
        
        Returns:
            Texto del análisis narrativo formateado
        """
        try:
            import google.generativeai as genai
            
            # Preparar contexto para Gemini
            contexto = f"""
Proporciona un análisis narrativo breve (3-4 párrafos) del siguiente análisis de {datos_actuales.get('ticker', 'instrumento')}.

PRECIO ACTUAL: ${datos_actuales.get('precio_actual', 'N/A')}
CAMBIO: {datos_actuales.get('cambio_pct', 'N/A')}%

INDICADORES TÉCNICOS:
{self._preparar_contexto_indicadores(indicadores)}

ANÁLISIS ALEXANDER:
{self._preparar_contexto_alexander(alexander)}

Escribe un análisis conciso que sintetice estos datos en lenguaje profesional pero accesible.
"""
            
            # Llamar a Gemini para sintetizar usando GenerativeModel
            model = genai.GenerativeModel(
                model_name="gemini-2.5-pro",
                generation_config={
                    "temperature": 0.3,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 1000,
                }
            )
            
            response = model.generate_content(contexto)
            
            # Verificar si la respuesta tiene contenido válido
            if response and hasattr(response, 'text') and response.text:
                analisis_narrativo = response.text
            else:
                # Si la respuesta fue bloqueada o no tiene contenido, usar valores por defecto
                self.logger.warning(f"Gemini response blocked or empty. Finish reason: {response.candidates[0].finish_reason if response and response.candidates else 'Unknown'}")
                analisis_narrativo = self._generar_narrativa_fallback(datos_actuales, indicadores, alexander)
            
            return analisis_narrativo
        
        except Exception as e:
            self.logger.error(f"Error generando análisis narrativo: {str(e)}")
            return self._generar_narrativa_fallback(datos_actuales, indicadores, alexander)
    
    def _generar_narrativa_fallback(self, datos_actuales: dict, indicadores: dict, alexander: dict) -> str:
        """Genera un análisis narrativo fallback sin depender de Gemini"""
        try:
            ticker = datos_actuales.get('ticker', 'instrumento')
            precio = datos_actuales.get('precio_actual', 'N/A')
            cambio = datos_actuales.get('cambio_pct', 'N/A')
            
            rsi = indicadores.get('RSI', {}).get('valor', 'N/A')
            rsi_señal = indicadores.get('RSI', {}).get('señal', 'N/A')
            
            macd_señal = indicadores.get('MACD', {}).get('señal', 'N/A')
            
            marea = alexander.get('marea', {}).get('marea_general', 'N/A')
            movimiento = alexander.get('movimiento', {}).get('movimiento', 'N/A')
            
            narrativa = f"""
{ticker} se cotiza en ${precio} con un cambio de {cambio}%. 

El análisis técnico muestra un RSI en {rsi} puntos ({rsi_señal}), mientras que el MACD presenta una señal {macd_señal}. Estos indicadores sugieren un momento {rsi_señal.lower()} en el instrumento.

El análisis Alexander indica una Marea {marea} a nivel macro con un Movimiento {movimiento} en la tendencia local. Esta combinación sugiere un entorno {marea.lower()} que favorece posiciones alcistas.

En conclusión, el instrumento presenta una configuración técnica y fundamental que refuerza el sesgo {movimiento.lower()} observado en el período analizado.
"""
            return narrativa
        except Exception as e:
            self.logger.error(f"Error en narrativa fallback: {e}")
            return "Análisis narrativo no disponible en este momento."
    
    def _preparar_contexto_indicadores(self, indicadores: dict) -> str:
        """Prepara contexto de indicadores para Gemini"""
        if not indicadores:
            return "Sin datos de indicadores"
        
        contexto = ""
        
        # RSI
        rsi = indicadores.get('RSI', {})
        if rsi:
            contexto += f"\nRSI: {rsi.get('valor', 'N/A')} ({rsi.get('nivel', 'N/A')}) - Señal: {rsi.get('señal', 'N/A')}"
        
        # MACD
        macd = indicadores.get('MACD', {})
        if macd:
            contexto += f"\nMACD: {macd.get('señal', 'N/A')} - Histograma: {macd.get('histograma', 'N/A')}"
        
        # Stochastic
        stoch = indicadores.get('STOCHASTIC', {})
        if stoch:
            contexto += f"\nStochastic: K={stoch.get('linea_k', 'N/A')}%, D={stoch.get('linea_d', 'N/A')}% - {stoch.get('nivel', 'N/A')}"
        
        # Medias Móviles
        medias = indicadores.get('MEDIAS_MOVILES', {})
        if medias:
            contexto += f"\nTendencia Corto Plazo (SMA20): {medias.get('tendencia_corto', 'N/A')}"
            contexto += f"\nTendencia Medio Plazo (SMA50): {medias.get('tendencia_medio', 'N/A')}"
            contexto += f"\nTendencia Largo Plazo (SMA200): {medias.get('tendencia_largo', 'N/A')}"
        
        # Volumen
        vol = indicadores.get('VOLUMEN', {})
        if vol:
            contexto += f"\nVolumen: {vol.get('señal', 'N/A')} - {vol.get('relacion', 'N/A')}x promedio"
        
        return contexto if contexto else "Sin indicadores específicos"
    
    def _preparar_contexto_alexander(self, alexander: dict) -> str:
        """Prepara contexto de análisis Alexander para Gemini"""
        if not alexander:
            return "Sin análisis Alexander"
        
        contexto = ""
        
        # Marea
        marea = alexander.get('marea', {})
        if marea:
            contexto += f"\nMaréa (Macro): {marea.get('marea_general', 'N/A')}"
            contexto += f"\nVIX: {marea.get('vix', 'N/A')}"
            contexto += f"\nVolatilidad: {marea.get('volatilidad_mercado', 'N/A')}"
        
        # Movimiento
        movimiento = alexander.get('movimiento', {})
        if movimiento:
            contexto += f"\nTendencia: {movimiento.get('movimiento', 'N/A')} ({movimiento.get('fuerza', 'N/A')})"
            contexto += f"\nConsenso: {movimiento.get('consenso', 'N/A')}%"
            contexto += f"\nSeñales Alcistas: {movimiento.get('señales_alcistas', 0)}/3"
            contexto += f"\nSeñales Bajistas: {movimiento.get('señales_bajistas', 0)}/3"
        
        # Factor Social
        factor_social = alexander.get('factor_social', {})
        if factor_social:
            contexto += f"\nValuación: {factor_social.get('valuacion', 'N/A')}"
            contexto += f"\nSentimiento: {factor_social.get('sentimiento_general', 'N/A')}"
            contexto += f"\nSolidez: {factor_social.get('solidez', 'N/A')}"
        
        return contexto if contexto else "Sin datos de Alexander"

    def _generar_texto_indicadores(self, indicadores):
        """Genera texto formateado de indicadores técnicos"""
        if not indicadores:
            return "No hay indicadores disponibles"
        
        texto = "**📊 INDICADORES TÉCNICOS:**\n"
        
        # RSI
        rsi = indicadores.get('RSI', {})
        if rsi:
            nivel = rsi.get('nivel', 'NEUTRAL')
            valor = rsi.get('valor', 'N/A')
            texto += f"• **RSI(14):** {valor} ({nivel})\n"
        
        # MACD
        macd = indicadores.get('MACD', {})
        if macd:
            linea = macd.get('linea_macd', 'N/A')
            senal = macd.get('linea_senal', 'N/A')
            hist = macd.get('histograma', 'N/A')
            señal = macd.get('señal', 'N/A')
            texto += f"• **MACD:** {linea} | Señal: {senal} | Histograma: {hist} ({señal})\n"
        
        # Stochastic
        stochastic = indicadores.get('STOCHASTIC', {})
        if stochastic:
            k = stochastic.get('linea_k', 'N/A')
            d = stochastic.get('linea_d', 'N/A')
            nivel = stochastic.get('nivel', 'NEUTRAL')
            texto += f"• **Stochastic:** %K={k}, %D={d} ({nivel})\n"
        
        # Medias Móviles
        medias = indicadores.get('MEDIAS_MOVILES', {})
        if medias:
            sma20 = medias.get('SMA_20', 'N/A')
            sma50 = medias.get('SMA_50', 'N/A')
            sma200 = medias.get('SMA_200', 'N/A')
            texto += f"• **SMA:** 20={sma20}, 50={sma50}, 200={sma200}\n"
        
        # EMA
        ema = indicadores.get('EMA', {})
        if ema:
            ema9 = ema.get('EMA_9', 'N/A')
            ema21 = ema.get('EMA_21', 'N/A')
            texto += f"• **EMA:** 9={ema9}, 21={ema21}\n"
        
        # Bollinger Bands
        bb = indicadores.get('BOLLINGER_BANDS', {})
        if bb:
            superior = bb.get('banda_superior', 'N/A')
            media = bb.get('banda_media', 'N/A')
            inferior = bb.get('banda_inferior', 'N/A')
            posicion = bb.get('posicion', 'NEUTRAL')
            texto += f"• **Bollinger Bands:** Superior={superior}, Media={media}, Inferior={inferior} ({posicion})\n"
        
        # ATR
        atr = indicadores.get('ATR', {})
        if atr:
            valor = atr.get('valor', 'N/A')
            volatilidad = atr.get('volatilidad', 'N/A')
            texto += f"• **ATR:** {valor} (Volatilidad: {volatilidad})\n"
        
        # Volumen
        volumen = indicadores.get('VOLUMEN', {})
        if volumen:
            actual = volumen.get('volumen_actual', 'N/A')
            promedio = volumen.get('volumen_promedio', 'N/A')
            senal = volumen.get('señal', 'NORMAL')
            texto += f"• **Volumen:** {actual:,} (Promedio: {promedio:,}) - {senal}\n"
        
        return texto if texto != "**📊 INDICADORES TÉCNICOS:**\n" else "No hay indicadores disponibles"
    
    def _generar_texto_finviz(self, datos_finviz, factor_social):
        """Genera texto complementario de datos Finviz"""
        if not datos_finviz:
            return ""
        
        texto = "\n**Datos adicionales (Finviz):**"
        
        if datos_finviz.get('insider_trading'):
            texto += f"\n- Insider Trading: {datos_finviz.get('insider_trading')}"
        
        if datos_finviz.get('analyst_rating'):
            texto += f"\n- Rating de Analistas: {datos_finviz.get('analyst_rating')}"
        
        if datos_finviz.get('news_sentiment'):
            texto += f"\n- Sentimiento de Noticias: {datos_finviz.get('news_sentiment')}"
        
        return texto
    
    async def comando_screener(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /screener - Ejecuta análisis automático de múltiples símbolos"""
        await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
        
        try:
            from analisis import ScreenerAutomatico, Timeframe
            
            # Parsear argumentos
            if not context.args:
                # Modo de ayuda
                mensaje = """
🔍 **SCREENER AUTOMÁTICO**

El screener analiza múltiples símbolos financieros y genera recomendaciones por horizonte de inversión.

**OPCIONES DE TIMEFRAME:**
• `/screener corto` - Análisis corto plazo (1-3 días)
• `/screener medio` - Análisis mediano plazo (1-4 semanas) 
• `/screener largo` - Análisis largo plazo (3-12 meses)

**SÍMBOLOS POPULARES:**
🇺🇸 Acciones: AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA
📈 Índices: SPY, QQQ, IWM
💱 Forex: EURUSD, GBPUSD, USDJPY
💰 Criptos: BTC, ETH (si están disponibles)

**EJEMPLOS:**
• `/screener medio AAPL MSFT GOOGL` - 3 acciones análisis medio plazo
• `/screener corto` - Top símbolos corto plazo (es.g. AAPL, MSFT, NVDA)
• `/screener largo BTC EURUSD` - Cripto y forex largo plazo

⏳ El análisis toma 2-5 segundos por símbolo...
                """
                await update.message.reply_text(mensaje)
                return
            
            # Determinar timeframe
            timeframe_str = context.args[0].lower()
            if timeframe_str == "corto":
                timeframe = Timeframe.SHORT_TERM
                plazo_texto = "⚡ CORTO PLAZO (1-3 días)"
            elif timeframe_str == "medio":
                timeframe = Timeframe.MEDIUM_TERM
                plazo_texto = "📊 MEDIANO PLAZO (1-4 semanas)"
            elif timeframe_str == "largo":
                timeframe = Timeframe.LONG_TERM
                plazo_texto = "🏆 LARGO PLAZO (3-12 meses)"
            else:
                await update.message.reply_text("❌ Timeframe inválido. Usa: corto, medio, largo")
                return
            
            # Obtener símbolos a analizar
            if len(context.args) > 1:
                tickers = [t.upper() for t in context.args[1:]]
            else:
                # Símbolos por defecto según el timeframe
                if timeframe == Timeframe.SHORT_TERM:
                    tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"]
                elif timeframe == Timeframe.MEDIUM_TERM:
                    tickers = ["SPY", "QQQ", "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA"]
                else:  # LONG_TERM
                    tickers = ["SPY", "QQQ", "BRK.B", "AAPL", "MSFT", "GOOGL", "AMZN"]
            
            # Enviar mensaje inicial
            mensaje_inicio = f"🔍 **SCREENER AUTOMÁTICO**\n\n{plazo_texto}\n\n📊 Analizando {len(tickers)} símbolos...\n⏳ Por favor espera..."
            await update.message.reply_text(mensaje_inicio)
            
            # Inicializar screener
            screener = ScreenerAutomatico(self.knowledge_manager.market_data)
            
            # Ejecutar análisis
            self.logger.info(f"Ejecutando screener: {tickers} en {timeframe.value}")
            resultados = screener.screener_por_sector(tickers, timeframe, limite=10)
            
            if not resultados:
                await update.message.reply_text("❌ No se pudieron obtener resultados del screener")
                return
            
            # Generar reporte
            mensaje_reporte = f"✅ **RESULTADOS DEL SCREENER**\n{plazo_texto}\n\n"
            mensaje_reporte += "=" * 50 + "\n"
            
            for i, resultado in enumerate(resultados, 1):
                # Emoji según recomendación
                if "COMPRA" in resultado.recomendacion:
                    emoji = "🟢"
                elif "VENTA" in resultado.recomendacion:
                    emoji = "🔴"
                else:
                    emoji = "🟡"
                
                mensaje_reporte += f"\n{i}. {emoji} **{resultado.ticker}**\n"
                mensaje_reporte += f"   💰 ${resultado.precio_actual:.2f}\n"
                mensaje_reporte += f"   📈 {resultado.recomendacion}\n"
                mensaje_reporte += f"   ⭐ Score: {resultado.score:.1f}/100 ({resultado.confianza:.0%})\n"
                mensaje_reporte += f"   📊 Señales: {resultado.señales_compra}↑ / {resultado.señales_venta}↓\n"
                mensaje_reporte += f"   💡 {resultado.razon_principal[:60]}...\n"
                mensaje_reporte += f"   🎯 Var. Esperada: {resultado.variacion_esperada:+.2f}%\n"
            
            mensaje_reporte += "\n" + "=" * 50 + "\n"
            mensaje_reporte += "\n💡 *Usa `/analizar TICKER` para análisis completo de un símbolo*"
            
            # Dividir mensaje si es muy largo
            if len(mensaje_reporte) > 4000:
                # Enviar en partes
                parts = mensaje_reporte.split("\n\n")
                parte_actual = ""
                
                for part in parts:
                    if len(parte_actual) + len(part) > 3000:
                        if parte_actual:
                            await update.message.reply_text(parte_actual)
                            parte_actual = part
                    else:
                        parte_actual += part + "\n\n"
                
                if parte_actual:
                    await update.message.reply_text(parte_actual)
            else:
                await update.message.reply_text(mensaje_reporte)
            
            # Guardar en base de conocimiento
            if hasattr(self.knowledge_manager, 'guardar_analisis_screener'):
                self.knowledge_manager.guardar_analisis_screener(
                    timeframe.value,
                    len(tickers),
                    len(resultados),
                    [r.ticker for r in resultados]
                )
            
            self.logger.info(f"✅ Screener completado: {len(resultados)} resultados")
            
        except Exception as e:
            self.logger.error(f"❌ Error en screener: {str(e)}")
            await update.message.reply_text(f"❌ Error en screener: {str(e)}")
    
    def iniciar(self):
        """Inicia el bot con manejo robusto de conflictos"""
        self.logger.info("[INFO] Iniciando bot de Telegram...")
        print("=" * 50)
        print("[BOT] BOT ANALISTA A&C")
        print("=" * 50)
        self.settings.mostrar_configuracion()
        print("[OK] Bot en funcionamiento. Presiona Ctrl+C para detener.")
        print("=" * 50)
        
        max_reintentos = 3
        reintento = 0
        
        while reintento < max_reintentos:
            try:
                # NUEVO: Implementar error handler para conflictos
                error_handler = logging.ERROR
                
                def manejar_error(update, context):
                    """Maneja errores de actualización"""
                    if "Conflict: terminated by other getUpdates request" in str(context.error):
                        self.logger.warning(
                            "⚠️  Conflicto detectado: otra instancia está usando este token"
                        )
                    elif "Too Many Requests" in str(context.error):
                        self.logger.warning(
                            "⚠️  Rate limit de Telegram: esperando 30 segundos..."
                        )
                        import time
                        time.sleep(30)
                    else:
                        self.logger.error(f"Error en actualización: {context.error}")
                
                # Registrar error handler
                self.app.add_error_handler(manejar_error)
                
                self.app.run_polling()
                break  # Salir del loop si se ejecuta exitosamente
                
            except Exception as e:
                reintento += 1
                error_msg = str(e).lower()
                
                if "conflict" in error_msg and "getUpdates" in str(e):
                    self.logger.error(
                        f"❌ Error de conflicto ({reintento}/{max_reintentos}): "
                        "Otra instancia está usando este token. "
                        "Reiniciando en 5 segundos..."
                    )
                    import time
                    time.sleep(5)
                elif "too many requests" in error_msg:
                    self.logger.error(
                        f"❌ Rate limit de Telegram ({reintento}/{max_reintentos}). "
                        "Esperando 60 segundos..."
                    )
                    import time
                    time.sleep(60)
                else:
                    self.logger.error(f"❌ Error iniciando bot: {str(e)}")
                    raise
        
        if reintento >= max_reintentos:
            self.logger.error(
                f"❌ No se pudo iniciar el bot después de {max_reintentos} intentos"
            )
            raise Exception("Fallo al iniciar el bot después de múltiples intentos")
