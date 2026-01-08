"""
cerebro/expert_analyzer.py
Analizador experto multi-tipo
Realiza análisis técnico, fundamental, psicológico, de riesgos y estratégico
"""

from typing import Dict, Any, List, Optional
import json
from datetime import datetime


class ExpertAnalyzer:
    """Realizador de análisis experto multi-perspectiva"""
    
    def __init__(self, knowledge_manager, ai_engine):
        """
        Inicializa el analizador experto
        
        Args:
            knowledge_manager: Gestor de conocimiento
            ai_engine: Motor de IA (Gemini)
        """
        self.km = knowledge_manager
        self.ai_engine = ai_engine
    
    def analisis_tecnico(self, simbolo: str, datos: Dict[str, Any], 
                        contexto: str = "") -> Dict[str, Any]:
        """
        Análisis técnico: patrones, soportes, resistencias, indicadores
        
        Args:
            simbolo: Símbolo del instrumento (ej: EURUSD, BTC/USD)
            datos: Datos de precio/volumen
            contexto: Información de los PDFs sobre análisis técnico
            
        Returns:
            Análisis técnico detallado
        """
        prompt = f"""
Realiza un análisis técnico EXPERTO para {simbolo} con estos datos:
{json.dumps(datos, indent=2)}

ANÁLISIS REQUERIDO:
1. Identificación de PATRONES clave (velas, banderas, triángulos, etc)
2. NIVELES críticos (soportes, resistencias, pivotes)
3. INDICADORES relevantes (RSI, MACD, Bollinger, Media Móvil)
4. SEÑALES de entrada y salida potenciales
5. RIESGO/RECOMPENSA estimado

{f"Considera estos principios del análisis técnico: {contexto}" if contexto else ""}

Proporciona:
- Análisis estructurado
- Confianza en cada señal (0-100%)
- Recomendación accionable
        """
        
        resultado = self.ai_engine.razonar(prompt, contexto=contexto)
        
        return {
            "tipo": "tecnico",
            "simbolo": simbolo,
            "analisis": resultado.get("respuesta", ""),
            "confianza": resultado.get("confianza", 0.0),
            "fecha": datetime.now().isoformat(),
            "error": resultado.get("error", False)
        }
    
    def analisis_fundamental(self, instrumento: str, datos_financieros: Dict[str, Any],
                            contexto: str = "") -> Dict[str, Any]:
        """
        Análisis fundamental: valor intrínseco, ratios, tendencias
        
        Args:
            instrumento: Nombre del instrumento/empresa
            datos_financieros: Estados financieros disponibles
            contexto: Información de los PDFs sobre análisis fundamental
            
        Returns:
            Análisis fundamental profundo
        """
        prompt = f"""
Realiza análisis FUNDAMENTAL EXPERTO para {instrumento}:

DATOS FINANCIEROS:
{json.dumps(datos_financieros, indent=2)}

ANÁLISIS REQUERIDO:
1. Cálculo de RATIOS clave (P/E, P/B, Deuda/Capital, etc)
2. Evaluación de TENDENCIAS de ingresos y ganancias
3. Determinación de VALOR INTRÍNSECO (múltiples métodos)
4. Análisis FORTALEZAS y DEBILIDADES
5. COMPARACIÓN vs industria/competidores

{f"Aplica estos principios fundamentales: {contexto}" if contexto else ""}

Proporciona:
- Valuación detallada
- Justificación de precio objetivo
- Riesgos identificados
- Recomendación (Compra/Venta/Mantener)
        """
        
        resultado = self.ai_engine.razonar(prompt, contexto=contexto)
        
        return {
            "tipo": "fundamental",
            "instrumento": instrumento,
            "analisis": resultado.get("respuesta", ""),
            "confianza": resultado.get("confianza", 0.0),
            "fecha": datetime.now().isoformat(),
            "error": resultado.get("error", False)
        }
    
    def analisis_psicologia_mercado(self, consulta: str, 
                                   datos_sentimiento: Optional[Dict] = None,
                                   contexto: str = "") -> Dict[str, Any]:
        """
        Análisis psicológico: sentimiento, comportamiento, fases del mercado
        
        Args:
            consulta: Pregunta sobre psicología del mercado
            datos_sentimiento: Datos de sentimiento si están disponibles
            contexto: Información de los PDFs sobre psicología trading
            
        Returns:
            Análisis psicológico del mercado
        """
        prompt = f"""
Realiza análisis PSICOLÓGICO DEL MERCADO sobre: {consulta}

{f"DATOS DE SENTIMIENTO: {json.dumps(datos_sentimiento, indent=2)}" if datos_sentimiento else ""}

ANÁLISIS REQUERIDO:
1. Identificación de la FASE actual del mercado (acumulación, impulso, distribución, liquidación)
2. Análisis del SENTIMIENTO (miedo/avaricia)
3. Patrones de COMPORTAMIENTO del trader común y su impacto
4. CICLOS psicológicos y recurrencia histórica
5. Oportunidades de CONTRARIEDAD

{f"Usa estos principios psicológicos: {contexto}" if contexto else ""}

Proporciona:
- Interpretación del estado psicológico
- Probabilidades por escenario
- Recomendaciones basadas en psicología
- Patrones históricos similares
        """
        
        resultado = self.ai_engine.razonar(prompt, contexto=contexto)
        
        return {
            "tipo": "psicologia",
            "consulta": consulta,
            "analisis": resultado.get("respuesta", ""),
            "confianza": resultado.get("confianza", 0.0),
            "fecha": datetime.now().isoformat(),
            "error": resultado.get("error", False)
        }
    
    def analisis_riesgo(self, escenario: str, capital: float = 1000,
                       trades_planificados: List[Dict] = None,
                       contexto: str = "") -> Dict[str, Any]:
        """
        Análisis de gestión de riesgos: stop loss, posición, correlaciones
        
        Args:
            escenario: Descripción del escenario de inversión
            capital: Capital disponible
            trades_planificados: Lista de trades a analizar
            contexto: Información de los PDFs sobre gestión de riesgos
            
        Returns:
            Análisis de riesgos completo
        """
        trades_info = ""
        if trades_planificados:
            trades_info = f"\nTRADES PLANIFICADOS:\n{json.dumps(trades_planificados, indent=2)}"
        
        prompt = f"""
Realiza análisis EXPERTO DE GESTIÓN DE RIESGOS:

ESCENARIO: {escenario}
CAPITAL DISPONIBLE: ${capital}
{trades_info}

ANÁLISIS REQUERIDO:
1. Determinación de SIZE DE POSICIÓN óptimo (% del capital)
2. Cálculo de STOP LOSS y TAKE PROFIT levels
3. Análisis de CORRELACIONES entre activos
4. Cálculo de RATIO RIESGO/RECOMPENSA
5. Evaluación de PEOR CASO y probabilidades

{f"Aplica estos principios de riesgo: {contexto}" if contexto else ""}

Proporciona:
- Recomendaciones de posición
- Puntos clave (SL, TP, entry)
- Ratio R/R mínimo recomendado
- Límite de pérdida por sesión/mes
- Monitoreo sugerido
        """
        
        resultado = self.ai_engine.razonar(prompt, contexto=contexto)
        
        return {
            "tipo": "riesgo",
            "escenario": escenario,
            "capital": capital,
            "analisis": resultado.get("respuesta", ""),
            "confianza": resultado.get("confianza", 0.0),
            "fecha": datetime.now().isoformat(),
            "error": resultado.get("error", False)
        }
    
    def analisis_estrategia(self, estrategia_nombre: str, 
                           descripcion: str, condiciones_entrada: List[str],
                           condiciones_salida: List[str],
                           contexto: str = "") -> Dict[str, Any]:
        """
        Análisis de estrategia operativa completa
        
        Args:
            estrategia_nombre: Nombre de la estrategia
            descripcion: Descripción general
            condiciones_entrada: Condiciones para abrir posición
            condiciones_salida: Condiciones para cerrar posición
            contexto: Información de los PDFs sobre estrategias
            
        Returns:
            Análisis de estrategia detallado
        """
        prompt = f"""
Realiza análisis EXPERTO DE ESTRATEGIA OPERATIVA:

ESTRATEGIA: {estrategia_nombre}
DESCRIPCIÓN: {descripcion}

ENTRADA:
{json.dumps(condiciones_entrada, indent=2)}

SALIDA:
{json.dumps(condiciones_salida, indent=2)}

ANÁLISIS REQUERIDO:
1. EVALUACIÓN de lógica y coherencia de la estrategia
2. Identificación de FORTALEZAS y DEBILIDADES
3. Cálculo de ESTADÍSTICAS esperadas (win rate, factor de ganancia)
4. Análisis de CONDICIONES de mercado óptimas
5. OPTIMIZACIONES sugeridas

{f"Considera estos principios estratégicos: {contexto}" if contexto else ""}

Proporciona:
- Validación de la estrategia
- Expectativas realistas
- Ajustes sugeridos
- Condiciones de mercado ideales
- Advertencias y limitaciones
        """
        
        resultado = self.ai_engine.razonar(prompt, contexto=contexto)
        
        return {
            "tipo": "estrategia",
            "estrategia": estrategia_nombre,
            "analisis": resultado.get("respuesta", ""),
            "confianza": resultado.get("confianza", 0.0),
            "fecha": datetime.now().isoformat(),
            "error": resultado.get("error", False)
        }
    
    def analisis_completo_360(self, instrumento: str, datos: Dict[str, Any],
                             contexto_libros: str = "") -> Dict[str, Any]:
        """
        Análisis completo 360° de un instrumento
        
        Args:
            instrumento: Instrumento a analizar
            datos: Datos disponibles
            contexto_libros: Contexto de los PDFs
            
        Returns:
            Análisis multi-perspectiva integrado
        """
        
        analisis_360 = {
            "instrumento": instrumento,
            "fecha_analisis": datetime.now().isoformat(),
            "analisis_multitipo": {}
        }
        
        # Ejecutar múltiples tipos de análisis en paralelo
        # (En la práctica, se ejecutarían de forma coordinada con la IA)
        
        perspectivas = [
            ("técnico", self.analisis_tecnico(instrumento, datos, contexto_libros)),
            ("fundamental", self.analisis_fundamental(instrumento, datos, contexto_libros)),
            ("psicología", self.analisis_psicologia_mercado(f"Estado del mercado para {instrumento}", contexto=contexto_libros)),
            ("riesgo", self.analisis_riesgo(f"Inversión en {instrumento}", contexto=contexto_libros)),
        ]
        
        for nombre, resultado in perspectivas:
            analisis_360["analisis_multitipo"][nombre] = resultado
        
        # Calcular confianza promedio
        confianzas = [a["confianza"] for _, a in perspectivas if not a.get("error")]
        analisis_360["confianza_promedio"] = sum(confianzas) / len(confianzas) if confianzas else 0.0
        
        return analisis_360
