"""
analisis/analyzer.py
Motor de análisis - Realiza análisis basado en el conocimiento del bot
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


class Analyzer:
    """Motor de análisis que utiliza el conocimiento del cerebro"""
    
    def __init__(self, knowledge_manager=None):
        """
        Inicializa el analizador
        
        Args:
            knowledge_manager: Referencia al gestor de conocimiento
        """
        self.knowledge_manager = knowledge_manager
        self.historial_analisis = []
    
    def analizar_datos(self, datos: Dict[str, Any], contexto: str = "") -> Dict[str, Any]:
        """
        Realiza análisis de datos en tiempo real
        
        Args:
            datos: Diccionario con datos a analizar
            contexto: Contexto adicional del análisis
            
        Returns:
            Resultado del análisis
        """
        resultado = {
            "timestamp": datetime.now().isoformat(),
            "tipo_analisis": "analisis_datos",
            "entrada": str(datos),
            "contexto": contexto,
            "hallazgos": [],
            "recomendaciones": [],
            "confianza": 0.0,
            "fuentes_utilizadas": []
        }
        
        # Buscar conocimiento relevante
        if self.knowledge_manager:
            consulta = contexto or str(datos.keys())
            conocimiento_relevante = self.knowledge_manager.buscar_conocimiento(consulta, limite=3)
            
            resultado["fuentes_utilizadas"] = [k["tema"] for k in conocimiento_relevante]
            resultado["hallazgos"].append(f"Se encontraron {len(conocimiento_relevante)} fuentes relevantes")
        
        # Análisis básico de datos
        hallazgos = self._analizar_patrones(datos)
        resultado["hallazgos"].extend(hallazgos["hallazgos"])
        resultado["confianza"] = hallazgos["confianza"]
        
        # Generar recomendaciones
        resultado["recomendaciones"] = self._generar_recomendaciones(datos, hallazgos)
        
        # Registrar análisis
        if self.knowledge_manager:
            self.knowledge_manager.registrar_analisis(
                tipo_analisis=resultado["tipo_analisis"],
                entrada=resultado["entrada"],
                resultado=str(resultado["hallazgos"]),
                confianza=resultado["confianza"],
                fuentes=resultado["fuentes_utilizadas"]
            )
        
        self.historial_analisis.append(resultado)
        return resultado
    
    def _analizar_patrones(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analiza patrones en los datos
        
        Args:
            datos: Datos a analizar
            
        Returns:
            Diccionario con hallazgos y confianza
        """
        hallazgos = []
        confianza = 0.5
        
        # Análisis de claves
        if "tendencia" in datos:
            if datos["tendencia"] == "al_alza":
                hallazgos.append("Tendencia al alza detectada")
                confianza += 0.2
            elif datos["tendencia"] == "a_la_baja":
                hallazgos.append("Tendencia a la baja detectada")
                confianza += 0.2
        
        # Análisis de volatilidad
        if "volatilidad" in datos:
            volatilidad = datos["volatilidad"]
            if volatilidad > 0.3:
                hallazgos.append(f"Alta volatilidad detectada ({volatilidad:.2%})")
            elif volatilidad < 0.05:
                hallazgos.append(f"Baja volatilidad detectada ({volatilidad:.2%})")
        
        # Análisis de promedio
        if isinstance(datos.get("valores"), list):
            valores = [v for v in datos["valores"] if isinstance(v, (int, float))]
            if valores:
                promedio = sum(valores) / len(valores)
                maximo = max(valores)
                minimo = min(valores)
                
                hallazgos.append(f"Promedio: {promedio:.2f}, Máximo: {maximo}, Mínimo: {minimo}")
                confianza = min(0.9, 0.5 + len(valores) * 0.05)
        
        return {
            "hallazgos": hallazgos,
            "confianza": min(1.0, confianza)
        }
    
    def _generar_recomendaciones(self, datos: Dict[str, Any], 
                                hallazgos: Dict[str, Any]) -> List[str]:
        """
        Genera recomendaciones basadas en hallazgos
        
        Args:
            datos: Datos originales
            hallazgos: Hallazgos del análisis
            
        Returns:
            Lista de recomendaciones
        """
        recomendaciones = []
        
        # Recomendaciones basadas en tendencia
        if "tendencia" in datos:
            if datos["tendencia"] == "al_alza":
                recomendaciones.append("Considere mantener o aumentar posiciones alcistas")
            elif datos["tendencia"] == "a_la_baja":
                recomendaciones.append("Considere tomar medidas defensivas")
        
        # Recomendaciones basadas en volatilidad
        if "volatilidad" in datos:
            if datos["volatilidad"] > 0.3:
                recomendaciones.append("Alta volatilidad: Use órdenes de stop-loss")
            elif datos["volatilidad"] < 0.05:
                recomendaciones.append("Baja volatilidad: Mercado está tranquilo, analice posibles quiebres")
        
        if not recomendaciones:
            recomendaciones.append("Continúe monitoreando el comportamiento del mercado")
        
        return recomendaciones
    
    def analizar_comparativa(self, activo1: Dict[str, Any], activo2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compara dos activos o conjuntos de datos
        
        Args:
            activo1: Primer conjunto de datos
            activo2: Segundo conjunto de datos
            
        Returns:
            Análisis comparativo
        """
        resultado = {
            "timestamp": datetime.now().isoformat(),
            "tipo_analisis": "analisis_comparativo",
            "comparacion": {},
            "recomendacion": ""
        }
        
        # Extraer valores para comparación
        valores1 = activo1.get("valores", [])
        valores2 = activo2.get("valores", [])
        
        if valores1 and valores2:
            promedio1 = sum(valores1) / len(valores1)
            promedio2 = sum(valores2) / len(valores2)
            
            resultado["comparacion"]["promedio_activo1"] = promedio1
            resultado["comparacion"]["promedio_activo2"] = promedio2
            resultado["comparacion"]["diferencia_porcentual"] = ((promedio1 - promedio2) / promedio2 * 100) if promedio2 != 0 else 0
            
            if promedio1 > promedio2:
                resultado["recomendacion"] = "Activo 1 muestra mejor desempeño"
            elif promedio2 > promedio1:
                resultado["recomendacion"] = "Activo 2 muestra mejor desempeño"
            else:
                resultado["recomendacion"] = "Ambos activos tienen similar desempeño"
        
        self.historial_analisis.append(resultado)
        return resultado
    
    def obtener_historial(self, limite: int = 10) -> List[Dict[str, Any]]:
        """
        Obtiene el historial de análisis realizados
        
        Args:
            limite: Número máximo de análisis a retornar
            
        Returns:
            Lista de análisis realizados
        """
        return self.historial_analisis[-limite:]
    
    def generar_reporte(self) -> Dict[str, Any]:
        """
        Genera un reporte resumen de análisis realizados
        
        Returns:
            Reporte resumen
        """
        if not self.historial_analisis:
            return {"mensaje": "No hay análisis realizados aún"}
        
        total_analisis = len(self.historial_analisis)
        confianza_promedio = sum(a.get("confianza", 0) for a in self.historial_analisis) / total_analisis
        
        tipos_analisis = {}
        for analisis in self.historial_analisis:
            tipo = analisis.get("tipo_analisis", "desconocido")
            tipos_analisis[tipo] = tipos_analisis.get(tipo, 0) + 1
        
        return {
            "total_analisis_realizados": total_analisis,
            "confianza_promedio": round(confianza_promedio, 2),
            "distribucion_por_tipo": tipos_analisis,
            "ultimo_analisis": self.historial_analisis[-1]["timestamp"]
        }
