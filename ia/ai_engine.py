"""
ia/ai_engine.py
Motor de IA independiente con Gemini (Google AI Studio)
PILAR FUNDAMENTAL - Sin dependencias cruzadas
"""

import os
import logging
from typing import Optional, Dict, Any, List

try:
    import google.generativeai as genai
    from google.generativeai.types import GenerationConfig
except ImportError:
    genai = None
    GenerationConfig = None


class AIEngine:
    """Motor de IA con Gemini (Google AI Studio)"""
    
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
                genai.configure(api_key=self.api_key)
                self.logger.info("✅ Motor IA inicializado con Gemini (Google AI Studio)")
            except Exception as e:
                self.logger.error(f"Error configurando Gemini: {str(e)}")
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
        temperatura: float = 0.7
    ) -> Dict[str, Any]:
        """
        Razonamiento lógico con Gemini (Google AI Studio)
        
        Args:
            pregunta: Pregunta del usuario
            contexto: Información del cerebro (PDFs) para contextualizar
            historial: Conversación anterior (no usado en este momento)
            modelo: Modelo de Gemini ('gemini-1.5-flash' o 'gemini-1.5-pro')
            temperatura: Creatividad (0.0-2.0)
        
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
            
            # Construir prompt
            sistema = "Eres un asistente experto en análisis financiero y trading. "
            if contexto and isinstance(contexto, str):
                sistema += f"Tienes acceso a información de libros sobre trading:\n\n{contexto}\n\n"
            sistema += "Proporciona análisis profundos, lógicos y bien fundamentados."
            
            prompt_completo = f"{sistema}\n\nPregunta del usuario: {pregunta}"
            
            # Crear instancia del modelo
            model = genai.GenerativeModel(
                model_name=modelo,
                generation_config=GenerationConfig(
                    temperature=temperatura,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=2000,
                )
            )
            
            # Generar respuesta con timeout y reintentos
            respuesta = None
            for intento in range(3):  # Reintentar hasta 3 veces
                try:
                    respuesta = model.generate_content(prompt_completo)
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
                respuesta_error = "❌ **MODELO NO DISPONIBLE**\n\nVerifica que el modelo en config/settings.py esté disponible.\nModelos válidos: gemini-1.5-flash, gemini-2.0-flash-exp"
            else:
                respuesta_error = f"❌ **ERROR EN GEMINI**\n\n{error_msg[:150]}"
            
            return {
                "respuesta": respuesta_error,
                "confianza": 0.0,
                "fuente": "local",
                "error": True
            }
    
    def analizar_datos(
        self,
        datos: Dict[str, Any],
        contexto: str = "",
        tipo_analisis: str = "general"
    ) -> Dict[str, Any]:
        """
        Análisis de datos con contexto de trading
        
        Args:
            datos: Datos a analizar (precios, volúmenes, etc)
            contexto: Información del cerebro
            tipo_analisis: 'general', 'tecnico', 'fundamental'
        
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
1. Hallazgos clave
2. Patrones observados
3. Recomendaciones accionables
4. Nivel de confianza (0-100%)
        """
        
        resultado = self.razonar(pregunta, contexto=contexto)
        
        if resultado.get("error"):
            return resultado
        
        return {
            "respuesta": resultado.get("respuesta"),
            "hallazgos": resultado.get("respuesta").split("\n")[:5],
            "recomendaciones": [],
            "confianza": resultado.get("confianza", 0.0),
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
