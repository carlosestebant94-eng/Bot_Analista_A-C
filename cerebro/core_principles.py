"""
cerebro/core_principles.py
Extrae y gestiona los principios fundamentales del cerebro
Basados en los libros que alimentan la IA
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path


class CorePrinciples:
    """Gestiona los principios fundamentales extraídos de los PDFs"""
    
    def __init__(self, db_path: str = "data/memory.db"):
        """
        Inicializa el gestor de principios
        
        Args:
            db_path: Ruta de la base de datos
        """
        self.db_path = db_path
        self._inicializar_tablas()
    
    def _inicializar_tablas(self):
        """Inicializa las tablas necesarias para principios"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tabla de principios fundamentales
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS principios_fundamentales (
                    id INTEGER PRIMARY KEY,
                    titulo TEXT UNIQUE,
                    descripcion TEXT,
                    categoria TEXT,
                    libro_origen TEXT,
                    paginas TEXT,
                    relevancia REAL,
                    fecha_extraccion TIMESTAMP,
                    es_ideal BOOLEAN DEFAULT 1
                )
            ''')
            
            # Tabla de estrategias derivadas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS estrategias_derivadas (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT,
                    principio_id INTEGER,
                    descripcion TEXT,
                    metodos TEXT,
                    casos_uso TEXT,
                    confianza REAL,
                    fecha_creacion TIMESTAMP,
                    FOREIGN KEY (principio_id) REFERENCES principios_fundamentales(id)
                )
            ''')
            
            # Tabla de indicadores clave
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS indicadores_clave (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT,
                    tipo TEXT,
                    formula TEXT,
                    uso_recomendado TEXT,
                    principios_relacionados TEXT,
                    fecha_creacion TIMESTAMP
                )
            ''')
            
            # Tabla de patrones validados
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS patrones_validados (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT,
                    descripcion TEXT,
                    señales TEXT,
                    confiabilidad REAL,
                    principios_respaldados TEXT,
                    fecha_descubrimiento TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error inicializando tablas de principios: {str(e)}")
    
    def extraer_principios_pdf(self, contenido_pdf: str, nombre_libro: str) -> List[Dict]:
        """
        Extrae principios fundamentales de un PDF
        
        Args:
            contenido_pdf: Texto completo del PDF
            nombre_libro: Nombre del libro
            
        Returns:
            Lista de principios extraídos
        """
        principios = []
        
        # Palabras clave que indican principios
        palabras_clave_principios = [
            "principio", "ley", "regla", "estrategia fundamental", 
            "concepto clave", "base", "fundamento", "esencial",
            "máxima", "patrón", "norma", "criterio"
        ]
        
        lineas = contenido_pdf.split('\n')
        
        for i, linea in enumerate(lineas):
            # Detectar líneas que contengan palabras clave
            if any(palabra in linea.lower() for palabra in palabras_clave_principios):
                # Extraer contexto (línea anterior y siguientes)
                inicio = max(0, i - 1)
                fin = min(len(lineas), i + 3)
                contexto = '\n'.join(lineas[inicio:fin])
                
                principio = {
                    "titulo": linea.strip()[:100],
                    "descripcion": contexto,
                    "libro_origen": nombre_libro,
                    "relevancia": 0.8,
                    "es_ideal": True
                }
                principios.append(principio)
        
        return principios
    
    def agregar_principio(self, titulo: str, descripcion: str, 
                         categoria: str, libro_origen: str,
                         relevancia: float = 1.0) -> bool:
        """
        Añade un principio fundamental a la base de datos
        
        Args:
            titulo: Título del principio
            descripcion: Descripción detallada
            categoria: Categoría (análisis técnico, fundamental, psicología, etc)
            libro_origen: Libro de donde viene
            relevancia: Puntuación de relevancia (0-1)
            
        Returns:
            True si fue exitoso
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO principios_fundamentales
                (titulo, descripcion, categoria, libro_origen, relevancia, fecha_extraccion, es_ideal)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (titulo, descripcion, categoria, libro_origen, relevancia, datetime.now(), 1))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error añadiendo principio: {str(e)}")
            return False
    
    def obtener_principios(self, categoria: str = None) -> List[Dict]:
        """
        Obtiene los principios fundamentales
        
        Args:
            categoria: Filtrar por categoría (opcional)
            
        Returns:
            Lista de principios
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if categoria:
                cursor.execute('''
                    SELECT id, titulo, descripcion, categoria, libro_origen, relevancia
                    FROM principios_fundamentales
                    WHERE categoria = ? AND es_ideal = 1
                    ORDER BY relevancia DESC
                ''', (categoria,))
            else:
                cursor.execute('''
                    SELECT id, titulo, descripcion, categoria, libro_origen, relevancia
                    FROM principios_fundamentales
                    WHERE es_ideal = 1
                    ORDER BY relevancia DESC
                ''')
            
            resultados = cursor.fetchall()
            conn.close()
            
            return [
                {
                    "id": r[0],
                    "titulo": r[1],
                    "descripcion": r[2],
                    "categoria": r[3],
                    "libro_origen": r[4],
                    "relevancia": r[5]
                } for r in resultados
            ]
            
        except Exception as e:
            print(f"Error obteniendo principios: {str(e)}")
            return []
    
    def crear_estrategia_desde_principio(self, principio_id: int, 
                                        nombre: str, descripcion: str,
                                        metodos: List[str]) -> bool:
        """
        Crea una estrategia derivada de un principio fundamental
        
        Args:
            principio_id: ID del principio base
            nombre: Nombre de la estrategia
            descripcion: Descripción
            metodos: Lista de métodos a usar
            
        Returns:
            True si fue exitoso
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO estrategias_derivadas
                (nombre, principio_id, descripcion, metodos, confianza, fecha_creacion)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nombre, principio_id, descripcion, json.dumps(metodos), 0.85, datetime.now()))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error creando estrategia: {str(e)}")
            return False
    
    def validar_contra_principios(self, informacion_nueva: str) -> Dict[str, Any]:
        """
        Valida nueva información contra los principios fundamentales
        
        Args:
            informacion_nueva: Información a validar
            
        Returns:
            Resultado de validación con alineamiento
        """
        principios = self.obtener_principios()
        
        coincidencias = []
        for principio in principios:
            # Búsqueda simple de coincidencias de palabras clave
            palabras_principio = principio["titulo"].lower().split()
            palabras_info = informacion_nueva.lower().split()
            
            coincidencias_encontradas = sum(1 for p in palabras_principio 
                                            if p in palabras_info)
            
            if coincidencias_encontradas > 0:
                coincidencias.append({
                    "principio": principio["titulo"],
                    "coincidencias": coincidencias_encontradas,
                    "relevancia": principio["relevancia"]
                })
        
        alineamiento = sum(c["coincidencias"] * c["relevancia"] 
                          for c in coincidencias) / max(len(coincidencias), 1)
        
        return {
            "validada": True,
            "alineamiento_con_principios": min(alineamiento, 1.0),
            "principios_relacionados": coincidencias,
            "confianza": 0.85 if coincidencias else 0.4
        }
    
    def obtener_resumen_cerebro(self) -> Dict[str, Any]:
        """
        Obtiene un resumen del estado del cerebro
        
        Returns:
            Resumen con estadísticas
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM principios_fundamentales WHERE es_ideal = 1")
            principios_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM estrategias_derivadas")
            estrategias_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM indicadores_clave")
            indicadores_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM patrones_validados")
            patrones_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT AVG(relevancia) FROM principios_fundamentales WHERE es_ideal = 1")
            relevancia_promedio = cursor.fetchone()[0] or 0.0
            
            conn.close()
            
            return {
                "principios_fundamentales": principios_count,
                "estrategias_derivadas": estrategias_count,
                "indicadores_clave": indicadores_count,
                "patrones_validados": patrones_count,
                "relevancia_promedio": round(relevancia_promedio, 2),
                "estado": "Cerebro optimizado" if principios_count > 0 else "Cerebro en desarrollo"
            }
            
        except Exception as e:
            print(f"Error obteniendo resumen: {str(e)}")
            return {}
