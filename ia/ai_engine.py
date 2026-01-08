"""
ia/ai_engine.py
Motor de IA independiente con Gemini (Google AI Studio)
PILAR FUNDAMENTAL - Sin dependencias cruzadas

VERSIÓN 2.0: Instrucción Maestra Completa (Análisis Determinista y Profesional)
- System Instructions para garantizar respuestas consistentes
- Formato Markdown estructurado
- Chain of Thought para lógica rigurosa
- Reglas binarias (NO creativas) para análisis técnico
"""

import os
import logging
import threading
from typing import Optional, Dict, Any, List

try:
    import google.generativeai as genai
    from google.generativeai.types import GenerationConfig
except ImportError:
    genai = None
    GenerationConfig = None


class AIEngine:
    """Motor de IA con Gemini (Google AI Studio) - Versión 2.0 con Instrucción Maestra"""
    
    # INSTRUCCIÓN MAESTRA COMPLETA - Se pasa como system_instruction a Gemini
    INSTRUCCION_MAESTRA_PROFESIONAL = """
### ROL PRINCIPAL
Actúa como un "Motor de Análisis Financiero Cuantitativo y Algorítmico" (Trading Bot).
Tu objetivo NO es ser creativo. Tu objetivo es ser DETERMINISTA, PRECISO y PROFESIONAL.
Ante los mismos datos de entrada (Input), debes generar siempre la misma conclusión de salida (Output).

### REGLAS DE PROCESAMIENTO LÓGICO (CHAIN OF THOUGHT)
Antes de generar el reporte final, sigue estos pasos internamente para garantizar consistencia:

1. VALIDACIÓN DE EVENTOS (Regla Maestra):
   - Si hay "Earnings" (Resultados) en < 5 días: La recomendación OBLIGATORIA es "ESPERA / HOLD". 
     Esto anula cualquier señal técnica alcista o bajista.
   - Si hay noticias críticas próximas (Fed, datos económicos): Evalúa riesgo de volatilidad.

2. ANÁLISIS TÉCNICO OBJETIVO (Binario):
   - Divergencias: Compara estrictamente los mínimos del precio vs. mínimos del oscilador (RSI/MACD).
     * ¿Precio hace Mínimo Más Bajo (LL) Y Oscilador hace Mínimo Más Alto (HL)? = SÍ es Divergencia Alcista.
     * Si no cumple la condición exacta = NO es Divergencia (no inventes "casi divergencias").
   - Sobreventa/Sobrecompra: Usa umbrales fijos (ej. RSI < 30 = Sobreventa, RSI > 70 = Sobrecompra).
   - Cruces de Medias: SMA/EMA debe estar claramente por encima o debajo, no zonas grises.

3. ANÁLISIS FUNDAMENTAL & MACRO:
   - Cruza datos: P/E Ratio vs Sector promedio. VIX vs Sentimiento General.
   - Valuation: Si P/E > 25 y crecimiento < 5% = Caro. Si P/E < 15 = Barato.
   - Contexto: Tasa de interés FED, rendimiento de bonos, inflación.

4. FACTOR SOCIAL (Sentimiento + Micro eventos):
   - Insider Trading: Insider buying = Señal alcista. Insider selling = Señal bajista.
   - Analyst Ratings: Mayoría "Buy" = Alcista. Mayoría "Sell" = Bajista.
   - Sentiment: News positivas/negativas, movimientos inusuales de volumen.

### REGLAS DE CONFIANZA (SCORING)
* **Alto (80-100%):** 3+ confirmaciones (técnica + fundamental + macro), sin eventos próximos.
* **Medio (50-79%):** 2 confirmaciones o 1 con márgenes estrechos.
* **Bajo (20-49%):** 1 confirmación o múltiples desacuerdos entre factores.
* **Muy Bajo (<20%):** Datos insuficientes o contradicciones fuertes.

### FORMATO DE RESPUESTA (ESTRUCTURA RÍGIDA)
Usa SIEMPRE esta estructura Markdown. Mantén un tono profesional, institucional y directo.

## 📊 REPORTE ANALÍTICO: [Símbolo]

### 1. 🚦 VEREDICTO DEL ALGORITMO
* **Señal Maestra:** [COMPRA / VENTA / ESPERA / HOLD]
* **Factor Determinante:** (Ej. "Anulación por Earnings próximos" o "Rebote por Sobreventa Técnica").
* **Nivel de Confianza:** [Bajo/Medio/Alto] ([XX]%)

### 2. 🌊 ENTORNO Y RIESGO (MACRO)
* **Contexto VIX/SPY:** [Interpretación neutral/alcista/bajista con valores]
* **Riesgo de Evento:** [Detalle sobre Earnings, Fed, datos económicos próximos]

### 3. 🧬 ANÁLISIS TÉCNICO (HECHOS, NO OPINIONES)
Genera una tabla Markdown con los valores exactos:
| Indicador | Valor | Estado (Obj.) | Interpretación |
| :--- | :--- | :--- | :--- |
| **Precio vs SMA** | [Valor] | [Debajo/Encima] | [Tendencia] |
| **RSI (14)** | [Valor] | [Neutral/Sobreventa/Sobrecompra] | [Potencial] |
| **MACD** | [Valor] | [Cruce/No cruce] | [Dirección] |
| **Divergencia** | [Detectada/No detectada] | -- | [Comentario estricto] |
| **Volumen** | [Valor vs promedio] | [Encima/Debajo] | [Validación] |

### 4. 💎 FUNDAMENTALES & VALOR
* **Valuación:** P/E Ratio [X], vs sector [Y]. Target Price: [Z]. Outlook: [Caro/Justo/Barato].
* **Tesis de Inversión:** (Resumen breve de por qué es atractivo o peligroso a largo plazo).
* **Riesgos:** Enumera 2-3 riesgos específicos.

### 5. 👥 FACTOR SOCIAL & SENTIMIENTO
* **Insider Activity:** [Descripción de compras/ventas recientes].
* **Analyst Consensus:** [Resumen de ratings].
* **Sentiment Score:** [Positivo/Negativo/Neutral] based on news.

### 6. 🎯 PLAN DE ACCIÓN
* **Entry Point:** [Si COMPRA, especifica precio].
* **Stop Loss:** [Nivel definido].
* **Target Profit:** [Objetivo de precio].
* **Plazo:** [Corto/Medio/Largo plazo].

---
**NOTA IMPORTANTE:** Este reporte se basa en reglas algorítmicas estrictas. 
No es asesoría financiera. Úsalo como herramienta de apoyo en tu decisión de inversión.
Responsabilidad del usuario: Validar contra tu propia investigación.
"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el motor de IA con Gemini
        
        Args:
            api_key: Clave de API de Google AI Studio. Si no se proporciona, la obtiene del .env
        """
        self.logger = logging.getLogger("AIEngine")
        
        # Obtener API key de Google AI Studio
        if not api_key:
            api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            self.logger.warning("⚠️  GOOGLE_API_KEY no configurada. IA deshabilitada.")
            self.api_key = None
            self.enabled = False
            self.provider = "gemini"
            return
        
        self.api_key = api_key
        self.enabled = True
        self.provider = "gemini"
        
        # Configurar Gemini (Google AI Studio)
        if genai:
            try:
                # Ejecutar con timeout para evitar bloqueos
                result_container = []
                def run_configure():
                    try:
                        genai.configure(api_key=self.api_key)
                        result_container.append(True)
                    except Exception as e:
                        self.logger.error(f"Error configurando Gemini: {str(e)}")
                        result_container.append(False)
                
                thread = threading.Thread(target=run_configure, daemon=True)
                thread.start()
                thread.join(timeout=5)  # Timeout de 5 segundos
                
                if thread.is_alive():
                    self.logger.warning("⚠️  Timeout configurando Gemini (> 5s)")
                    self.enabled = False
                elif result_container and result_container[0]:
                    self.logger.info("✅ Motor IA inicializado con Gemini (Google AI Studio)")
                else:
                    self.enabled = False
                    
            except Exception as e:
                self.logger.error(f"Error crítico con Gemini: {str(e)}")
                self.enabled = False
        else:
            self.logger.warning("⚠️  Librería google-generativeai no instalada. Instala con: pip install google-generativeai")
            self.enabled = False
    
    def razonar(
        self,
        pregunta: str,
        contexto: str = "",
        historial: Optional[List[Dict[str, str]]] = None,
        modelo: str = "gemini-2.5-pro",
        temperatura: float = 0.0,  # MÁXIMO DETERMINISMO (0.0)
        usar_instruccion_maestra: bool = True
    ) -> Dict[str, Any]:
        """
        Razonamiento lógico con Gemini (Google AI Studio)
        CON INSTRUCCIÓN MAESTRA PROFESIONAL
        
        Args:
            pregunta: Pregunta del usuario
            contexto: Información del cerebro (PDFs) para contextualizar
            historial: Conversación anterior (no usado en este momento)
            modelo: Modelo de Gemini ('gemini-1.5-flash' o 'gemini-2.5-pro')
            temperatura: Creatividad (0.0-1.0) - BAJA = Determinista
            usar_instruccion_maestra: Si True, usa instrucción maestra para análisis profesional
        
        Returns:
            Dict con respuesta, confianza y metadata
        """
        if not self.enabled:
            return {
                "respuesta": "❌ IA no configurada. Añade GOOGLE_API_KEY al .env",
                "confianza": 0.0,
                "fuente": "local",
                "error": True
            }
        
        if not genai:
            return {
                "respuesta": "❌ Librería google-generativeai no instalada",
                "confianza": 0.0,
                "fuente": "local",
                "error": True
            }
        
        try:
            # Validar entrada
            if not pregunta or not isinstance(pregunta, str):
                return {
                    "respuesta": "❌ La pregunta debe ser un texto válido",
                    "confianza": 0.0,
                    "error": True
                }
            
            # Crear modelo CON o SIN instrucción maestra
            if usar_instruccion_maestra:
                # MODO PROFESIONAL: Con instrucción maestra para determinismo
                model = genai.GenerativeModel(
                    model_name=modelo,
                    system_instruction=self.INSTRUCCION_MAESTRA_PROFESIONAL,
                    generation_config=GenerationConfig(
                        temperature=temperatura,  # Bajo para determinismo
                        top_p=0.9,
                        top_k=20,  # Reduce variabilidad
                        max_output_tokens=3000,
                    )
                )
                self.logger.info(f"✅ Usando INSTRUCCIÓN MAESTRA PROFESIONAL (Temperatura: {temperatura})")
            else:
                # MODO ESTÁNDAR: Sin instrucción maestra (más creativo)
                sistema = "Eres un asistente experto en análisis financiero y trading. "
                if contexto and isinstance(contexto, str):
                    sistema += f"Tienes acceso a información de libros sobre trading:\n\n{contexto}\n\n"
                sistema += "Proporciona análisis profundos, lógicos y bien fundamentados."
                
                model = genai.GenerativeModel(
                    model_name=modelo,
                    generation_config=GenerationConfig(
                        temperature=temperatura,
                        top_p=0.95,
                        top_k=40,
                        max_output_tokens=2000,
                    )
                )
                pregunta = f"{sistema}\n\nPregunta del usuario: {pregunta}"
            
            # Generar respuesta con reintentos
            respuesta = None
            for intento in range(3):  # Reintentar hasta 3 veces
                try:
                    respuesta = model.generate_content(pregunta)
                    if respuesta and respuesta.text:
                        break
                except Exception as retry_error:
                    self.logger.warning(f"Intento {intento + 1} falló: {str(retry_error)}")
                    if intento == 2:  # Último intento
                        raise
                    import time
                    time.sleep(1)  # Esperar antes de reintentar
            
            if not respuesta or not respuesta.text:
                return {
                    "respuesta": "⚠️  Gemini generó una respuesta vacía. Intenta reformular tu pregunta.",
                    "confianza": 0.0,
                    "error": True
                }
            
            return {
                "respuesta": respuesta.text,
                "confianza": 0.93,  # Gemini es muy confiable
                "fuente": "gemini",
                "modelo": modelo,
                "proveedor": "Google AI Studio",
                "modo": "PROFESIONAL (Instrucción Maestra)" if usar_instruccion_maestra else "ESTÁNDAR",
                "error": False,
                "tokens_usados": 0  # Gemini no expone tokens públicamente
            }
        
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Error en razonamiento con Gemini: {error_msg}")
            
            # Proporcionar mensajes de error más útiles basados en el tipo de error
            if "429" in error_msg or "quota" in error_msg.lower() or "exceeded" in error_msg.lower():
                respuesta_error = """⚠️  **CUOTA EXCEDIDA**

Tu API de Gemini ha alcanzado el límite de solicitudes gratuitas.

**Opciones:**
1. ⏳ Espera 5+ segundos y vuelve a intentar
2. 💳 Actualiza a plan pago: https://ai.google.dev/billing
3. 🔄 Cambiar de modelo en config/settings.py

Por ahora, intenta en unos segundos. El bot funcionará nuevamente cuando se renueve la cuota."""
            elif "API key" in error_msg or "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
                respuesta_error = """❌ **ERROR DE AUTENTICACIÓN**

Tu GOOGLE_API_KEY no es válida o no está configurada.

**Solución:**
1. Verifica tu .env tiene: GOOGLE_API_KEY=tu_clave
2. Obtén una nueva clave: https://ai.google.dev
3. Reinicia el bot después de actualizar"""
            elif "timeout" in error_msg.lower() or "deadline" in error_msg.lower():
                respuesta_error = "⏱️  **TIMEOUT**\n\nLa solicitud tardó demasiado. Intenta una pregunta más corta o simple."
            elif "not found" in error_msg.lower() or "invalid model" in error_msg.lower():
                respuesta_error = "❌ **MODELO NO DISPONIBLE**\n\nVerifica que el modelo en config/settings.py esté disponible.\nModelos válidos: gemini-1.5-flash, gemini-2.5-pro"
            else:
                respuesta_error = f"❌ **ERROR EN GEMINI**\n\n{error_msg[:150]}"
            
            return {
                "respuesta": respuesta_error,
                "confianza": 0.0,
                "fuente": "local",
                "error": True
            }
    
    def analizar_ticker_profesional(
        self,
        ticker: str,
        datos_tecnicos: Dict[str, Any],
        datos_fundamentales: Dict[str, Any],
        datos_macro: Dict[str, Any],
        contexto_conocimiento: str = ""
    ) -> Dict[str, Any]:
        """
        NUEVO MÉTODO: Análisis Profesional de Ticker con Instrucción Maestra
        Genera reporte estructurado 📊 REPORTE ANALÍTICO
        
        Args:
            ticker: Símbolo del ticker (ej: "AAPL")
            datos_tecnicos: Dict con RSI, MACD, precios, soportes/resistencias
            datos_fundamentales: Dict con P/E, Market Cap, Debt/Equity, ROE
            datos_macro: Dict con VIX, rendimiento de bonos, tasa Fed, etc
            contexto_conocimiento: Principios extraídos de libros
        
        Returns:
            Análisis profesional con veredicto, señal y plan de acción
        """
        if not self.enabled:
            return {
                "error": True,
                "respuesta": "❌ IA no configurada"
            }
        
        # Construir prompt estructurado CON los datos reales
        prompt_profesional = f"""
## DATOS DE ENTRADA - TICKER: {ticker}

### DATOS TÉCNICOS
{self._formatear_dict_tabla(datos_tecnicos)}

### DATOS FUNDAMENTALES
{self._formatear_dict_tabla(datos_fundamentales)}

### CONTEXTO MACRO
{self._formatear_dict_tabla(datos_macro)}

{f'### CONTEXTO (Principios de Libros)\\n{contexto_conocimiento}' if contexto_conocimiento else ''}

---

## INSTRUCCIÓN
Analiza el ticker {ticker} siguiendo estrictamente las reglas de la instrucción maestra.
Genera un reporte estructurado en Markdown con:
1. Veredicto (COMPRA/VENTA/ESPERA)
2. Entorno y riesgo
3. Tabla técnica con análisis binario
4. Fundamentales y valuación
5. Factor social
6. Plan de acción

No inventes datos. Usa SOLO los proporcionados arriba.
Si falta información, señálalo explícitamente.
        """
        
        # Usar razonar CON instrucción maestra Y TEMPERATURA 0.0
        resultado = self.razonar(
            pregunta=prompt_profesional,
            contexto=contexto_conocimiento,
            temperatura=0.0,  # MÁXIMO DETERMINISMO
            usar_instruccion_maestra=True
        )
        
        return resultado
    
    def _formatear_dict_tabla(self, datos: Dict[str, Any]) -> str:
        """Formatea un dict como tabla Markdown para legibilidad"""
        if not datos:
            return "*(Sin datos)*"
        
        lineas = []
        lineas.append("| Métrica | Valor |")
        lineas.append("|:---|:---|")
        for clave, valor in datos.items():
            lineas.append(f"| {clave} | {valor} |")
        return "\n".join(lineas)
    
    def calcular_plan_accion_trading(
        self,
        ticker: str,
        precio_actual: float,
        datos_tecnicos: Dict[str, Any],
        datos_fundamentales: Dict[str, Any],
        veredicto: str,
        contexto_analisis: str = ""
    ) -> Dict[str, Any]:
        """
        NUEVO MÉTODO: Calcula plan de trading con Entry, Stop Loss, Take Profit y plazo
        
        Args:
            ticker: Símbolo del ticker
            precio_actual: Precio actual del activo
            datos_tecnicos: Dict con soportes, resistencias, volatilidad, ATR
            datos_fundamentales: Dict con P/E, Target Price, etc
            veredicto: "COMPRA", "VENTA" o "ESPERA"
            contexto_analisis: Información adicional del análisis
        
        Returns:
            Dict con plan de acción: Entry, Stop Loss, Take Profit, Plazo, Risk/Reward
        """
        if not self.enabled:
            return {
                "error": True,
                "respuesta": "❌ IA no configurada"
            }
        
        # Extraer datos clave si están disponibles
        soporte = datos_tecnicos.get("Soporte Principal", precio_actual * 0.97)
        resistencia = datos_tecnicos.get("Resistencia", precio_actual * 1.03)
        atr = datos_tecnicos.get("ATR", abs(resistencia - soporte) / 2)
        volatilidad = datos_tecnicos.get("Volatilidad", "Media")
        
        # Convertir a float si es posible
        try:
            soporte = float(str(soporte).replace("$", ""))
            resistencia = float(str(resistencia).replace("$", ""))
            atr = float(str(atr).replace("$", ""))
        except:
            soporte = precio_actual * 0.97
            resistencia = precio_actual * 1.03
            atr = (resistencia - soporte) / 2
        
        # Construir prompt para Gemini
        prompt_plan_accion = f"""
INSTRUCCIÓN: Calcula un plan de trading PROFESIONAL y PRECISO basado en estos datos:

TICKER: {ticker}
PRECIO ACTUAL: ${precio_actual:.2f}
VEREDICTO: {veredicto}

DATOS TÉCNICOS:
- Soporte Principal: ${soporte:.2f}
- Resistencia: ${resistencia:.2f}
- ATR (Average True Range): ${atr:.2f}
- Volatilidad: {volatilidad}
{contexto_analisis}

DATOS FUNDAMENTALES:
{self._formatear_dict_tabla(datos_fundamentales)}

---

REQUERIMIENTOS DEL PLAN:

1. PRECIO DE ENTRADA (Entry Point):
   - Si COMPRA: Usa soporte o zona de rebote
   - Si VENTA: Usa resistencia o zona de rechazo
   - Justifica basado en soporte/resistencia

2. STOP LOSS (Precio de Protección):
   - Calcula como porcentaje fijo (2-3% normalmente)
   - O usa nivel técnico (soporte/resistencia anterior)
   - Debe minimizar pérdida máxima

3. TAKE PROFIT (Precio de Ganancia):
   - Usa resistencia siguiente si es COMPRA
   - Usa soporte siguiente si es VENTA
   - Calcula basado en risk/reward ratio (1:2 o mejor)

4. PLAZO PROYECTADO:
   - Corto plazo: 1-5 días (volatilidad alta)
   - Medio plazo: 1-4 semanas (volatilidad media)
   - Largo plazo: 1-3 meses (volatilidad baja)
   - Justifica basado en ATR y volatilidad

5. RATIO RISK/REWARD:
   - Calcula ganancia potencial / pérdida potencial
   - Debe ser >= 1:1.5 para ser viable

---

FORMATO DE RESPUESTA (Markdown estructurado):

## 🎯 PLAN DE ACCIÓN TRADING: {ticker}

### 1. PUNTO DE ENTRADA (Entry Point)
* **Precio Recomendado:** $XXX
* **Justificación:** [Basada en soporte/resistencia]
* **Tipo:** Inmediato / En rebote / En pullback

### 2. NIVEL DE STOP LOSS
* **Precio Stop:** $XXX
* **Pérdida Máxima:** XX% o $XX
* **Justificación:** [Técnica o porcentual]

### 3. OBJETIVO DE GANANCIA (Take Profit)
* **Precio Target:** $XXX
* **Ganancia Potencial:** XX% o $XX
* **Resistencia Base:** [Describe resistencia usada]

### 4. RATIO RIESGO/GANANCIA
* **Risk/Reward:** 1:{ratio:.1f}
* **Evaluación:** [Excelente/Bueno/Aceptable]

### 5. PLAZO PROYECTADO
* **Duración Estimada:** [5 días / 2 semanas / 1 mes]
* **Justificación:** [Basada en volatilidad y ATR]

### 6. CHECKLIST PRE-ENTRADA
☐ Confirmar soporte/resistencia en gráfico
☐ Validar volumen en la entrada
☐ Revisar noticias próximas
☐ Verificar R/R ratio >= 1.5
☐ Establecer alerta en entrada

---

Sé DETERMINISTA y PRECISO. Usa SOLO los datos proporcionados.
Si falta información (Target Price, ATR), cálcalo aproximadamente.
Recuerda: Risk Management es lo más importante.
        """
        
        # Llamar a Gemini CON instrucción maestra
        resultado = self.razonar(
            pregunta=prompt_plan_accion,
            contexto=contexto_analisis,
            temperatura=0.0,  # MÁXIMO DETERMINISMO
            usar_instruccion_maestra=True
        )
        
        return resultado
    
    def analizar_datos(
        self,
        datos: Dict[str, Any],
        contexto: str = "",
        tipo_analisis: str = "general",
        usar_instruccion_maestra: bool = True
    ) -> Dict[str, Any]:
        """
        Análisis de datos con contexto de trading
        MEJORADO: Ahora usa instrucción maestra para determinismo
        
        Args:
            datos: Datos a analizar (precios, volúmenes, etc)
            contexto: Información del cerebro
            tipo_analisis: 'general', 'tecnico', 'fundamental'
            usar_instruccion_maestra: Si True, análisis profesional y determinista
        
        Returns:
            Análisis con hallazgos y recomendaciones
        """
        if not self.enabled:
            return {
                "hallazgos": ["IA no configurada"],
                "recomendaciones": [],
                "confianza": 0.0,
                "error": True
            }
        
        import json
        
        pregunta = f"""
Analiza los siguientes datos de trading ({tipo_analisis}):

DATOS:
{json.dumps(datos, indent=2)}

{f'CONTEXTO DE LIBROS:' + contexto if contexto else ''}

Proporciona:
1. Hallazgos clave (solo hechos objetivos)
2. Patrones observados (binarios: presente/ausente)
3. Recomendaciones accionables
4. Nivel de confianza (0-100%) con justificación
        """
        
        resultado = self.razonar(
            pregunta, 
            contexto=contexto,
            temperatura=0.0,  # MÁXIMO DETERMINISMO
            usar_instruccion_maestra=usar_instruccion_maestra
        )
        
        if resultado.get("error"):
            return resultado
        
        return {
            "respuesta": resultado.get("respuesta"),
            "hallazgos": resultado.get("respuesta").split("\n")[:5],
            "recomendaciones": [],
            "confianza": resultado.get("confianza", 0.0),
            "modo": "PROFESIONAL" if usar_instruccion_maestra else "ESTÁNDAR",
            "error": False
        }
    
    def generar_prompts(
        self,
        tema: str,
        cantidad: int = 5
    ) -> Dict[str, Any]:
        """
        Genera prompts para entrenar o validar el sistema
        
        Args:
            tema: Tema para generar prompts
            cantidad: Número de prompts
        
        Returns:
            Lista de prompts generados
        """
        if not self.enabled:
            return {"prompts": [], "error": True}
        
        pregunta = f"Genera {cantidad} preguntas sobre '{tema}' para entrenar un bot de análisis de trading."
        resultado = self.razonar(pregunta)
        
        return resultado
    
    def validar_respuesta(
        self,
        respuesta: str,
        criterios: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Valida la calidad de una respuesta
        
        Args:
            respuesta: Respuesta a validar
            criterios: Criterios de validación
        
        Returns:
            Validación con puntuación
        """
        if not self.enabled:
            return {"valido": False, "puntuacion": 0.0, "error": True}
        
        criterios = criterios or ["claridad", "precisión", "utilidad"]
        
        pregunta = f"""
Valida esta respuesta según estos criterios: {', '.join(criterios)}

RESPUESTA:
{respuesta}

Proporciona:
1. Evaluación por criterio
2. Puntuación total (0-100)
3. Comentarios
        """
        
        resultado = self.razonar(pregunta)
        return resultado
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene estado del motor IA"""
        return {
            "habilitado": self.enabled,
            "tiene_api_key": bool(self.api_key),
            "proveedor": "Google AI Studio (Gemini)",
            "libreria_disponible": genai is not None,
            "mensaje": "✅ IA operativa (Gemini)" if self.enabled else "⚠️  IA deshabilitada"
        }
