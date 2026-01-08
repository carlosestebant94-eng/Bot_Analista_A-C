"""
cerebro/knowledge_manager.py
Gestor de conocimiento - Maneja la base de datos de conocimiento del bot
Proporciona búsqueda, almacenamiento y recuperación de información
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import os


class KnowledgeManager:
    """Gestor centralizado del conocimiento del bot"""
    
    def __init__(self, db_path: str = "data/memory.db"):
        """
        Inicializa el gestor de conocimiento
        
        Args:
            db_path: Ruta de la base de datos SQLite
        """
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.inicializar_bd()
        
        # Inicializar gestor de datos de mercado (lazy loading)
        self.market_data = None
    
    def _obtener_market_data(self):
        """Obtiene o inicializa el gestor de datos de mercado (lazy loading)"""
        if self.market_data is None:
            try:
                from data_sources import MarketDataManager
                self.market_data = MarketDataManager()
            except Exception as e:
                print(f"⚠️  No se pudo inicializar MarketDataManager: {e}")
        return self.market_data
    
    @property
    def market_data_property(self):
        """Property para acceder al gestor de datos de mercado"""
        return self._obtener_market_data()
    
    def inicializar_bd(self):
        """Inicializa la estructura de la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # PRAGMA para optimización
            cursor.execute("PRAGMA journal_mode = WAL")
            cursor.execute("PRAGMA synchronous = NORMAL")
            cursor.execute("PRAGMA cache_size = -64000")
            
            # Tabla de documentos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS documentos (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT UNIQUE,
                    ruta TEXT,
                    tipo TEXT,
                    fecha_carga TIMESTAMP,
                    contenido TEXT
                )
            ''')
            
            # Índices para documentos
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_documentos_nombre 
                ON documentos(nombre)
            ''')
            
            # Tabla de conocimiento
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conocimiento (
                    id INTEGER PRIMARY KEY,
                    documento_id INTEGER,
                    tema TEXT,
                    contenido TEXT,
                    relevancia REAL,
                    fecha_creacion TIMESTAMP,
                    FOREIGN KEY (documento_id) REFERENCES documentos(id)
                )
            ''')
            
            # Índices para conocimiento (críticos para búsqueda)
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_conocimiento_tema 
                ON conocimiento(tema)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_conocimiento_relevancia 
                ON conocimiento(relevancia DESC)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_conocimiento_documento 
                ON conocimiento(documento_id)
            ''')
            
            # Tabla de análisis realizados
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analisis_realizados (
                    id INTEGER PRIMARY KEY,
                    tipo_analisis TEXT,
                    entrada TEXT,
                    resultado TEXT,
                    confianza REAL,
                    fecha_analisis TIMESTAMP,
                    fuentes TEXT
                )
            ''')
            
            # Índices para análisis
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_analisis_tipo 
                ON analisis_realizados(tipo_analisis)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_analisis_fecha 
                ON analisis_realizados(fecha_analisis)
            ''')
            
            # Tabla de aprendizaje
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS aprendizajes (
                    id INTEGER PRIMARY KEY,
                    tipo TEXT,
                    descripcion TEXT,
                    valor TEXT,
                    fecha_aprendizaje TIMESTAMP
                )
            ''')
            
            # Índices para aprendizajes
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_aprendizajes_tipo 
                ON aprendizajes(tipo)
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error inicializando BD: {str(e)}")
    
    def cargar_documento(self, nombre: str, ruta: str, tipo: str, contenido: str) -> bool:
        """
        Carga un documento en la base de datos
        
        Args:
            nombre: Nombre del documento
            ruta: Ruta del documento
            tipo: Tipo de documento (pdf, imagen, etc)
            contenido: Contenido del documento
            
        Returns:
            True si fue exitoso
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO documentos 
                (nombre, ruta, tipo, fecha_carga, contenido)
                VALUES (?, ?, ?, ?, ?)
            ''', (nombre, ruta, tipo, datetime.now(), contenido))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error cargando documento: {str(e)}")
            return False
    
    def agregar_conocimiento(self, tema: str, contenido: str, 
                            documento_id: Optional[int] = None, 
                            relevancia: float = 1.0) -> bool:
        """
        Agrega conocimiento a la base de datos
        
        Args:
            tema: Tema del conocimiento
            contenido: Contenido del conocimiento
            documento_id: ID del documento de origen
            relevancia: Puntuación de relevancia (0-1)
            
        Returns:
            True si fue exitoso
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO conocimiento 
                (documento_id, tema, contenido, relevancia, fecha_creacion)
                VALUES (?, ?, ?, ?, ?)
            ''', (documento_id, tema, contenido, relevancia, datetime.now()))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error agregando conocimiento: {str(e)}")
            return False
    
    def buscar_conocimiento(self, consulta: str, limite: int = 5) -> List[Dict[str, Any]]:
        """
        Busca conocimiento relacionado con una consulta
        
        Args:
            consulta: Término de búsqueda
            limite: Número máximo de resultados
            
        Returns:
            Lista de resultados encontrados
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            consulta_sql = '''
                SELECT id, tema, contenido, relevancia, fecha_creacion
                FROM conocimiento
                WHERE tema LIKE ? OR contenido LIKE ?
                ORDER BY relevancia DESC
                LIMIT ?
            '''
            
            termino = f"%{consulta}%"
            cursor.execute(consulta_sql, (termino, termino, limite))
            resultados = cursor.fetchall()
            conn.close()
            
            return [
                {
                    "id": r[0],
                    "tema": r[1],
                    "contenido": r[2],
                    "relevancia": r[3],
                    "fecha": r[4]
                } for r in resultados
            ]
            
        except Exception as e:
            print(f"Error buscando conocimiento: {str(e)}")
            return []
    
    def registrar_analisis(self, tipo_analisis: str, entrada: str, 
                          resultado: str, confianza: float = 0.0, 
                          fuentes: Optional[List[str]] = None) -> bool:
        """
        Registra un análisis realizado para aprendizaje continuo
        
        Args:
            tipo_analisis: Tipo de análisis realizado
            entrada: Datos de entrada del análisis
            resultado: Resultado del análisis
            confianza: Nivel de confianza (0-1)
            fuentes: Fuentes utilizadas en el análisis
            
        Returns:
            True si fue exitoso
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            fuentes_json = json.dumps(fuentes) if fuentes else "[]"
            
            cursor.execute('''
                INSERT INTO analisis_realizados
                (tipo_analisis, entrada, resultado, confianza, fecha_analisis, fuentes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (tipo_analisis, entrada, resultado, confianza, datetime.now(), fuentes_json))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error registrando análisis: {str(e)}")
            return False
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de la base de conocimiento
        
        Returns:
            Diccionario con estadísticas
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM documentos")
            num_docs = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM conocimiento")
            num_conocimientos = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM analisis_realizados")
            num_analisis = cursor.fetchone()[0]
            
            cursor.execute("SELECT AVG(confianza) FROM analisis_realizados")
            confianza_promedio = cursor.fetchone()[0] or 0.0
            
            conn.close()
            
            return {
                "documentos_cargados": num_docs,
                "conocimientos_almacenados": num_conocimientos,
                "analisis_realizados": num_analisis,
                "confianza_promedio": round(confianza_promedio, 2)
            }
            
        except Exception as e:
            print(f"Error obteniendo estadísticas: {str(e)}")
            return {}
    
    def limpiar_bd(self):
        """Limpia y reinicia la base de datos"""
        try:
            if os.path.exists(self.db_path):
                os.remove(self.db_path)
            self.inicializar_bd()
            print("Base de datos limpiada y reiniciada")
        except Exception as e:
            print(f"Error limpiando BD: {str(e)}")
    
    def guardar_analisis_screener(
        self,
        timeframe: str,
        total_simbolos: int,
        resultados_count: int,
        simbolos_recomendados: List[str]
    ) -> bool:
        """
        Guarda resultados del análisis de screener en la base de datos
        
        Args:
            timeframe: Horizonte temporal (corto_plazo, mediano_plazo, largo_plazo)
            total_simbolos: Total de símbolos analizados
            resultados_count: Cantidad de resultados principales retornados
            simbolos_recomendados: Lista de símbolos con mejores recomendaciones
            
        Returns:
            True si fue exitoso
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            valor = json.dumps({
                'total_analizado': total_simbolos,
                'resultados_principales': resultados_count,
                'simbolos': simbolos_recomendados
            })
            
            cursor.execute('''
                INSERT INTO aprendizajes (tipo, descripcion, valor, fecha_aprendizaje)
                VALUES (?, ?, ?, ?)
            ''', (
                'screener_resultado',
                f'Screener automático - {timeframe}',
                valor,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error guardando screener: {str(e)}")
            return False
    
    def obtener_screener_historial(self, timeframe: Optional[str] = None, limite: int = 10) -> List[Dict]:
        """
        Obtiene historial de análisis screener
        
        Args:
            timeframe: Filtrar por horizonte temporal (opcional)
            limite: Cantidad máxima de resultados
            
        Returns:
            Lista de análisis screener previos
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if timeframe:
                cursor.execute('''
                    SELECT descripcion, valor, fecha_aprendizaje FROM aprendizajes
                    WHERE tipo = 'screener_resultado' AND descripcion LIKE ?
                    ORDER BY fecha_aprendizaje DESC
                    LIMIT ?
                ''', (f'%{timeframe}%', limite))
            else:
                cursor.execute('''
                    SELECT descripcion, valor, fecha_aprendizaje FROM aprendizajes
                    WHERE tipo = 'screener_resultado'
                    ORDER BY fecha_aprendizaje DESC
                    LIMIT ?
                ''', (limite,))
            
            resultados = []
            for row in cursor.fetchall():
                resultados.append({
                    'descripcion': row[0],
                    'datos': json.loads(row[1]),
                    'fecha': row[2]
                })
            
            conn.close()
            return resultados
            
        except Exception as e:
            print(f"Error obteniendo historial screener: {str(e)}")
            return []

