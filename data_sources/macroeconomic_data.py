"""
data_sources/macroeconomic_data.py
Gestor de datos macroeconómicos
Fuentes: Federal Reserve Economic Data (FRED), World Bank, etc.
"""

import logging
import pandas as pd
from typing import Dict, Optional, Any, List
from datetime import datetime, timedelta
import requests
import os

try:
    import pandas_datareader as pdr
    PANDAS_DATAREADER_AVAILABLE = True
except ImportError:
    PANDAS_DATAREADER_AVAILABLE = False


class MacroeconomicDataManager:
    """Gestor centralizado de datos macroeconómicos"""
    
    def __init__(self, fred_api_key: Optional[str] = None):
        """
        Inicializa el gestor de datos macroeconómicos
        
        Args:
            fred_api_key: API key de Federal Reserve (opcional, intenta desde env)
        """
        self.logger = logging.getLogger("MacroeconomicDataManager")
        
        # Obtener API key desde env si no se proporciona
        self.fred_api_key = fred_api_key or os.getenv('FRED_API_KEY')
        
        # Indicadores FRED importantes
        self.fred_indicators = {
            'DGS10': 'US 10-Year Treasury Yield',
            'DGS2': 'US 2-Year Treasury Yield',
            'UNRATE': 'US Unemployment Rate',
            'INFLATION': 'US Inflation Rate (CPI)',
            'CPIAUCSL': 'Consumer Price Index',
            'INDPRO': 'Industrial Production Index',
            'UMCSENT': 'Consumer Sentiment Index',
            'MORTGAGE30US': '30-Year Mortgage Rate',
            'DCOILWTICO': 'WTI Crude Oil Price',
            'DEXUSEU': 'USD/EUR Exchange Rate'
        }
        
        # Cache para evitar llamadas repetidas
        self.cache = {}
        self.cache_expiry = {}
        
        # DIFERENCIACIÓN DE TTL POR TIPO DE DATO
        # Datos diarios: 1 día de TTL
        # Datos mensuales: 30 días de TTL
        # Datos anuales: 365 días de TTL
        self.cache_ttl_map = {
            'DGS10': 86400,      # Tasas diarias: 1 día
            'DGS2': 86400,       # Tasas diarias: 1 día
            'UNRATE': 2592000,   # Desempleo mensual: 30 días
            'INFLATION': 2592000,# Inflación mensual: 30 días
            'CPIAUCSL': 2592000, # CPI mensual: 30 días
            'INDPRO': 2592000,   # Producción industrial mensual: 30 días
            'UMCSENT': 604800,   # Sentimiento semanal: 7 días
            'MORTGAGE30US': 86400,# Hipotecas diarias: 1 día
            'DCOILWTICO': 86400, # Petróleo diario: 1 día
            'DEXUSEU': 86400     # Tipo cambio diario: 1 día
        }
        
        self.logger.info("[OK] Gestor de datos macroeconómicos inicializado")
    
    def obtener_tasa_desempleo(self, dias_atras: int = 365) -> Optional[pd.DataFrame]:
        """
        Obtiene la tasa de desempleo de FRED
        
        Args:
            dias_atras: Número de días hacia atrás
            
        Returns:
            DataFrame con datos de desempleo
        """
        return self._obtener_indicador_fred('UNRATE', dias_atras)
    
    def obtener_inflacion(self, dias_atras: int = 365) -> Optional[pd.DataFrame]:
        """
        Obtiene datos de inflación (CPI)
        
        Args:
            dias_atras: Número de días hacia atrás
            
        Returns:
            DataFrame con datos de inflación
        """
        return self._obtener_indicador_fred('CPIAUCSL', dias_atras)
    
    def obtener_tasas_interes(self) -> Dict[str, float]:
        """
        Obtiene las tasas de interés principales
        
        Returns:
            Diccionario con tasas principales
        """
        try:
            cache_key = 'tasas_interes'
            
            # Verificar cache
            if self._es_cache_valido(cache_key):
                return self.cache[cache_key]
            
            tasas = {}
            
            # Tasa 10-year
            tasa_10y = self._obtener_indicador_fred('DGS10', 1)
            if tasa_10y is not None and not tasa_10y.empty:
                tasas['10y'] = float(tasa_10y.iloc[-1, 0])
            
            # Tasa 2-year
            tasa_2y = self._obtener_indicador_fred('DGS2', 1)
            if tasa_2y is not None and not tasa_2y.empty:
                tasas['2y'] = float(tasa_2y.iloc[-1, 0])
            
            # Yield curve slope
            if '10y' in tasas and '2y' in tasas:
                tasas['slope'] = tasas['10y'] - tasas['2y']
            
            # Guardar en cache
            if tasas:
                self.cache[cache_key] = tasas
                self.cache_expiry[cache_key] = datetime.now()
            
            return tasas
            
        except Exception as e:
            self.logger.warning(f"Error obteniendo tasas: {e}")
            return {}
    
    def obtener_sentimiento_consumidor(self, dias_atras: int = 90) -> Optional[float]:
        """
        Obtiene el índice de sentimiento del consumidor
        
        Args:
            dias_atras: Días hacia atrás
            
        Returns:
            Valor del sentimiento (float)
        """
        try:
            df = self._obtener_indicador_fred('UMCSENT', dias_atras)
            if df is not None and not df.empty:
                return float(df.iloc[-1, 0])
        except Exception as e:
            self.logger.warning(f"Error obteniendo sentimiento: {e}")
        
        return None
    
    def obtener_produccion_industrial(self, dias_atras: int = 90) -> Optional[float]:
        """
        Obtiene el índice de producción industrial
        
        Args:
            dias_atras: Días hacia atrás
            
        Returns:
            Valor del índice (float)
        """
        try:
            df = self._obtener_indicador_fred('INDPRO', dias_atras)
            if df is not None and not df.empty:
                return float(df.iloc[-1, 0])
        except Exception as e:
            self.logger.warning(f"Error obteniendo producción: {e}")
        
        return None
    
    def obtener_precio_petroleo(self) -> Optional[float]:
        """
        Obtiene el precio actual del petróleo WTI
        
        Returns:
            Precio en USD por barril
        """
        try:
            cache_key = 'precio_petroleo'
            
            if self._es_cache_valido(cache_key):
                return self.cache[cache_key]
            
            df = self._obtener_indicador_fred('DCOILWTICO', 1)
            if df is not None and not df.empty:
                precio = float(df.iloc[-1, 0])
                self.cache[cache_key] = precio
                self.cache_expiry[cache_key] = datetime.now()
                return precio
        except Exception as e:
            self.logger.warning(f"Error obteniendo precio petróleo: {e}")
        
        return None
    
    def obtener_tipo_cambio_usd_eur(self) -> Optional[float]:
        """
        Obtiene el tipo de cambio USD/EUR
        
        Returns:
            Tipo de cambio
        """
        try:
            cache_key = 'usd_eur'
            
            if self._es_cache_valido(cache_key):
                return self.cache[cache_key]
            
            df = self._obtener_indicador_fred('DEXUSEU', 1)
            if df is not None and not df.empty:
                cambio = float(df.iloc[-1, 0])
                self.cache[cache_key] = cambio
                self.cache_expiry[cache_key] = datetime.now()
                return cambio
        except Exception as e:
            self.logger.warning(f"Error obteniendo tipo de cambio: {e}")
        
        return None
    
    def obtener_contexto_macro_resumido(self) -> Dict[str, Any]:
        """
        Obtiene un resumen del contexto macroeconómico actual
        
        Returns:
            Diccionario con indicadores principales
        """
        contexto = {
            'timestamp': datetime.now().isoformat(),
            'tasas_interes': self.obtener_tasas_interes(),
            'desempleo': None,
            'inflacion': None,
            'sentimiento_consumidor': self.obtener_sentimiento_consumidor(),
            'produccion_industrial': self.obtener_produccion_industrial(),
            'precio_petroleo': self.obtener_precio_petroleo(),
            'tipo_cambio_usd_eur': self.obtener_tipo_cambio_usd_eur()
        }
        
        # Obtener últimos valores de desempleo e inflación
        desempleo = self.obtener_tasa_desempleo(30)
        if desempleo is not None and not desempleo.empty:
            contexto['desempleo'] = float(desempleo.iloc[-1, 0])
        
        inflacion = self.obtener_inflacion(30)
        if inflacion is not None and not inflacion.empty:
            contexto['inflacion'] = float(inflacion.iloc[-1, 0])
        
        return contexto
    
    def _obtener_indicador_fred(self, indicador: str, dias_atras: int = 365) -> Optional[pd.DataFrame]:
        """
        Obtiene un indicador de FRED
        
        Args:
            indicador: Código FRED del indicador
            dias_atras: Días hacia atrás desde hoy
            
        Returns:
            DataFrame con datos o None
        """
        try:
            if not PANDAS_DATAREADER_AVAILABLE:
                self.logger.warning("pandas_datareader no está instalado")
                return None
            
            fecha_inicio = datetime.now() - timedelta(days=dias_atras)
            
            # Intentar obtener del caché primero
            cache_key = f"fred_{indicador}_{dias_atras}"
            if self._es_cache_valido(cache_key):
                return self.cache[cache_key]
            
            # Si tenemos API key, usar eso
            if self.fred_api_key:
                df = pdr.get_data_fred(
                    indicador,
                    api_key=self.fred_api_key,
                    start=fecha_inicio
                )
            else:
                # Fallback: intentar sin API key (limitado)
                df = pdr.get_data_fred(
                    indicador,
                    start=fecha_inicio
                )
            
            if df is not None:
                # Guardar en cache
                self.cache[cache_key] = df
                self.cache_expiry[cache_key] = datetime.now()
                self.logger.info(f"✅ Indicador FRED {indicador} obtenido")
            
            return df
            
        except Exception as e:
            self.logger.warning(f"Error obteniendo indicador FRED {indicador}: {e}")
            return None
    
    def _es_cache_valido(self, key: str) -> bool:
        """
        Verifica si un cache es válido (no ha expirado)
        Usa TTL diferenciado según el tipo de dato
        
        Args:
            key: Clave del cache (formato: fred_INDICADOR_dias)
            
        Returns:
            True si es válido
        """
        if key not in self.cache or key not in self.cache_expiry:
            return False
        
        # Extraer el indicador de la clave
        try:
            indicador = key.split('_')[1]  # fred_INDICADOR_dias
        except (IndexError, ValueError):
            indicador = None
        
        # Obtener TTL para este tipo de datos
        ttl = self.cache_ttl_map.get(indicador, 3600)  # Default 1 hora
        
        tiempo_desde_cache = (datetime.now() - self.cache_expiry[key]).total_seconds()
        es_valido = tiempo_desde_cache < ttl
        
        if not es_valido and indicador:
            self.logger.debug(f"Cache para {indicador} ha expirado (TTL: {ttl}s, edad: {tiempo_desde_cache}s)")
        
        return es_valido
    
    def limpiar_cache(self):
        """Limpia el cache completamente"""
        self.cache.clear()
        self.cache_expiry.clear()
        self.logger.info("Cache limpiado")
