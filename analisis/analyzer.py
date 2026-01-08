"""
analisis/analyzer.py
Motor de análisis - Realiza análisis basado en el conocimiento del bot
Incluye caché y optimizaciones de performance
"""

from typing import Dict, List, Any
from datetime import datetime


class Analyzer:
    """Motor de análisis que utiliza el conocimiento del cerebro"""
    
    def __init__(self, knowledge_manager: 'Any | None' = None):
        """
        Inicializa el analizador
        
        Args:
            knowledge_manager: Referencia al gestor de conocimiento
        """
        self.knowledge_manager = knowledge_manager
        self.historial_analisis = []
        self.cache_analisis = {}
        self.cache_ttl = 3600  # 1 hora (estandarizado)
        self.cache_expiry = {}
        self.MAX_HISTORIAL = 1000  # PUNTO 1: Aumentado de 100 para mejor auditoría
        self.CONOCIMIENTO_LIMIT = 8  # PUNTO 1: Aumentado de 3 para más contexto
    
    def analizar_datos(self, datos: Dict[str, Any], contexto: str = "") -> Dict[str, Any]:
        """
        Realiza análisis de datos en tiempo real con caché
        
        Args:
            datos: Diccionario con datos a analizar
            contexto: Contexto adicional del análisis
            
        Returns:
            Resultado del análisis
        """
        # Verificar cache
        cache_key = self._generar_cache_key(datos, contexto)
        if self._es_cache_valido(cache_key):
            return self.cache_analisis[cache_key]
        
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
        
        # Buscar conocimiento relevante (PUNTO 1: aumentado a 8 de 3)
        if self.knowledge_manager:
            consulta = contexto or str(datos.keys())
            conocimiento_relevante = self.knowledge_manager.buscar_conocimiento(consulta, limite=self.CONOCIMIENTO_LIMIT)
            
            resultado["fuentes_utilizadas"] = [k["tema"] for k in conocimiento_relevante]
            resultado["hallazgos"].append(f"Se encontraron {len(conocimiento_relevante)} fuentes relevantes")
        
        # Análisis básico de datos
        hallazgos = self._analizar_patrones(datos)
        resultado["hallazgos"].extend(hallazgos["hallazgos"])
        resultado["confianza"] = hallazgos["confianza"]
        
        # Generar recomendaciones
        resultado["recomendaciones"] = self._generar_recomendaciones(datos, hallazgos)
        
        # Registrar análisis (sin bloquear)
        if self.knowledge_manager:
            try:
                self.knowledge_manager.registrar_analisis(
                    tipo_analisis=resultado["tipo_analisis"],
                    entrada=resultado["entrada"],
                    resultado=str(resultado["hallazgos"]),
                    confianza=resultado["confianza"],
                    fuentes=resultado["fuentes_utilizadas"]
                )
            except Exception:
                pass  # No bloquear si falla el registro
        
        # Guardar en cache
        self.cache_analisis[cache_key] = resultado
        self.cache_expiry[cache_key] = datetime.now()
        
        # Guardar en historial (PUNTO 1: aumentado a 1000 para auditoría)
        self.historial_analisis.append(resultado)
        if len(self.historial_analisis) > self.MAX_HISTORIAL:
            self.historial_analisis.pop(0)
        
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
            if len(valores) > 1:
                import numpy as np
                promedio = np.mean(valores)
                maximo = max(valores)
                minimo = min(valores)
                
                hallazgos.append(f"Promedio: {promedio:.2f}, Máximo: {maximo}, Mínimo: {minimo}")
                
                # Confianza basada en variabilidad de datos (mejor que lineal)
                desv_std = np.std(valores)
                coef_variacion = desv_std / abs(promedio) if promedio != 0 else 1.0
                
                # Confianza inversamente proporcional a variabilidad
                confianza_base = max(0.3, 1.0 - (coef_variacion * 0.3))
                
                # Aumentar con tamaño de muestra (saturación logarítmica para mejor scaling)
                factor_tamaño = min(0.4, np.log10(len(valores) + 1) / 8)
                confianza = min(0.95, confianza_base + factor_tamaño)
            elif len(valores) == 1:
                promedio = valores[0]
                hallazgos.append(f"Valor único: {promedio:.2f}")
                confianza = 0.4  # Muy baja confianza con un solo dato
        
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
    
    def _generar_cache_key(self, datos: Dict[str, Any], contexto: str) -> str:
        """Genera una clave de caché única"""
        import hashlib
        contenido = str(sorted(datos.items())) + contexto
        return hashlib.md5(contenido.encode()).hexdigest()
    
    def _es_cache_valido(self, key: str) -> bool:
        """Verifica si un cache es válido"""
        if key not in self.cache_analisis or key not in self.cache_expiry:
            return False
        
        tiempo_desde_cache = (datetime.now() - self.cache_expiry[key]).total_seconds()
        return tiempo_desde_cache < self.cache_ttl
    
    def limpiar_cache(self) -> None:
        """Limpia el caché de análisis"""
        self.cache_analisis.clear()
        self.cache_expiry.clear()

