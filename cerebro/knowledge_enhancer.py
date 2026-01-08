"""
cerebro/knowledge_enhancer.py
Motor de mejora continua del conocimiento
Busca, valida e integra nueva información alineada con los principios fundamentales
"""

import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional
from .core_principles import CorePrinciples


class KnowledgeEnhancer:
    """Mejora continua del conocimiento del bot"""
    
    def __init__(self, db_path: str = "data/memory.db"):
        """
        Inicializa el motor de mejora
        
        Args:
            db_path: Ruta de la base de datos
        """
        self.db_path = db_path
        self.core_principles = CorePrinciples(db_path)
        self._inicializar_tablas()
    
    def _inicializar_tablas(self):
        """Inicializa las tablas para mejora continua"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tabla de fuentes externas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS fuentes_externas (
                    id INTEGER PRIMARY KEY,
                    tipo TEXT,
                    titulo TEXT,
                    url TEXT,
                    autor TEXT,
                    fecha_descubrimiento TIMESTAMP,
                    relevancia_potencial REAL,
                    estado TEXT,
                    resumen TEXT
                )
            ''')
            
            # Tabla de conocimiento integrado
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conocimiento_integrado (
                    id INTEGER PRIMARY KEY,
                    fuente_id INTEGER,
                    tema TEXT,
                    contenido TEXT,
                    alineamiento_principios REAL,
                    fecha_integracion TIMESTAMP,
                    validado BOOLEAN,
                    confianza REAL,
                    FOREIGN KEY (fuente_id) REFERENCES fuentes_externas(id)
                )
            ''')
            
            # Tabla de análisis multi-tipo
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analisis_multitipo (
                    id INTEGER PRIMARY KEY,
                    tipo_analisis TEXT,
                    entrada TEXT,
                    resultado TEXT,
                    principios_usados TEXT,
                    confianza REAL,
                    fecha_analisis TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error inicializando tablas de mejora: {str(e)}")
    
    def agregar_fuente_externa(self, tipo: str, titulo: str, 
                              url: Optional[str] = None, 
                              autor: Optional[str] = None,
                              relevancia_potencial: float = 0.8) -> bool:
        """
        Añade una fuente externa para integrar
        
        Args:
            tipo: Tipo de fuente (artículo, libro, informe, análisis, etc)
            titulo: Título de la fuente
            url: URL si aplica
            autor: Autor de la fuente
            relevancia_potencial: Puntuación inicial de relevancia
            
        Returns:
            True si fue exitoso
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO fuentes_externas
                (tipo, titulo, url, autor, fecha_descubrimiento, relevancia_potencial, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (tipo, titulo, url, autor, datetime.now(), relevancia_potencial, "pendiente"))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error añadiendo fuente: {str(e)}")
            return False
    
    def integrar_conocimiento(self, fuente_id: int, tema: str, 
                             contenido: str, confianza: float = 0.85) -> Dict[str, Any]:
        """
        Integra conocimiento de una fuente externa
        
        Args:
            fuente_id: ID de la fuente
            tema: Tema del conocimiento
            contenido: Contenido a integrar
            confianza: Nivel de confianza (0-1)
            
        Returns:
            Resultado de integración con validación
        """
        # Validar contra principios
        validacion = self.core_principles.validar_contra_principios(contenido)
        
        if validacion["alineamiento_con_principios"] < 0.3:
            return {
                "integrado": False,
                "razon": "No alineado con principios fundamentales",
                "alineamiento": validacion["alineamiento_con_principios"],
                "confianza": 0.0
            }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Calcular confianza final
            confianza_final = confianza * validacion["confianza"]
            
            cursor.execute('''
                INSERT INTO conocimiento_integrado
                (fuente_id, tema, contenido, alineamiento_principios, 
                 fecha_integracion, validado, confianza)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (fuente_id, tema, contenido, validacion["alineamiento_con_principios"],
                  datetime.now(), 1, confianza_final))
            
            # Actualizar estado de fuente
            cursor.execute('''
                UPDATE fuentes_externas
                SET estado = ?
                WHERE id = ?
            ''', ("integrada", fuente_id))
            
            conn.commit()
            conn.close()
            
            return {
                "integrado": True,
                "confianza_final": confianza_final,
                "alineamiento": validacion["alineamiento_con_principios"],
                "principios_relacionados": len(validacion["principios_relacionados"])
            }
            
        except Exception as e:
            print(f"Error integrando conocimiento: {str(e)}")
            return {"integrado": False, "error": str(e)}
    
    def realizar_analisis_multitipo(self, consulta: str, contexto: str = "") -> Dict[str, Any]:
        """
        Realiza múltiples tipos de análisis sobre una consulta
        
        Args:
            consulta: Pregunta o tema a analizar
            contexto: Contexto adicional
            
        Returns:
            Análisis multi-tipo con múltiples perspectivas
        """
        tipos_analisis = {
            "tecnico": {
                "descripcion": "Análisis técnico de patrones, soportes, resistencias",
                "enfoque": "Gráficos, velas, indicadores técnicos"
            },
            "fundamental": {
                "descripcion": "Análisis fundamental de valor intrínseco",
                "enfoque": "Earnings, ratios, balance general"
            },
            "psicologia": {
                "descripcion": "Análisis psicológico del mercado",
                "enfoque": "Sentimiento, comportamiento del trader"
            },
            "riesgo": {
                "descripcion": "Análisis de gestión de riesgos",
                "enfoque": "Stop loss, posición, correlaciones"
            },
            "estrategia": {
                "descripcion": "Análisis de estrategia operativa",
                "enfoque": "Setup, entrada, salida, reward/risk"
            }
        }
        
        analisis_resultados = {}
        
        for tipo, info in tipos_analisis.items():
            resultado = {
                "tipo": tipo,
                "descripcion": info["descripcion"],
                "enfoque": info["enfoque"],
                "estado": "pendiente_ia"
            }
            analisis_resultados[tipo] = resultado
        
        return {
            "consulta": consulta,
            "analisis_multitipo": analisis_resultados,
            "principios_aplicables": self.core_principles.obtener_principios(),
            "recomendacion": "Usar IA Gemini para ejecutar cada tipo de análisis"
        }
    
    def obtener_resumen_mejora(self) -> Dict[str, Any]:
        """
        Obtiene resumen del estado de mejora del cerebro
        
        Returns:
            Resumen detallado
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Fuentes externas
            cursor.execute("SELECT COUNT(*) FROM fuentes_externas WHERE estado = 'pendiente'")
            fuentes_pendientes = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM fuentes_externas WHERE estado = 'integrada'")
            fuentes_integradas = cursor.fetchone()[0]
            
            # Conocimiento integrado
            cursor.execute("SELECT COUNT(*) FROM conocimiento_integrado WHERE validado = 1")
            conocimientos_validados = cursor.fetchone()[0]
            
            cursor.execute("SELECT AVG(confianza) FROM conocimiento_integrado WHERE validado = 1")
            confianza_promedio = cursor.fetchone()[0] or 0.0
            
            # Análisis realizados
            cursor.execute("SELECT COUNT(*) FROM analisis_multitipo")
            analisis_realizados = cursor.fetchone()[0]
            
            cursor.execute("SELECT AVG(confianza) FROM analisis_multitipo")
            confianza_analisis = cursor.fetchone()[0] or 0.0
            
            conn.close()
            
            cerebro_stats = self.core_principles.obtener_resumen_cerebro()
            
            return {
                **cerebro_stats,
                "mejora_continua": {
                    "fuentes_pendientes": fuentes_pendientes,
                    "fuentes_integradas": fuentes_integradas,
                    "conocimientos_validados": conocimientos_validados,
                    "confianza_promedio_conocimiento": round(confianza_promedio, 2),
                    "analisis_realizados": analisis_realizados,
                    "confianza_promedio_analisis": round(confianza_analisis, 2)
                },
                "salud_cerebro": "Óptima" if conocimientos_validados > 50 else "Buena" if conocimientos_validados > 10 else "En desarrollo"
            }
            
        except Exception as e:
            print(f"Error obteniendo resumen: {str(e)}")
            return {}
