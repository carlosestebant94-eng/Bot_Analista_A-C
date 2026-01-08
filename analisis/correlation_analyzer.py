"""
analisis/correlation_analyzer.py
Analizador de correlaciones entre activos y análisis de sentimiento
"""

import logging
import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from scipy.stats import pearsonr, spearmanr
import json
import requests


class CorrelationAnalyzer:
    """Analizador de correlaciones entre activos"""
    
    def __init__(self):
        """Inicializa el analizador de correlaciones"""
        self.logger = logging.getLogger("CorrelationAnalyzer")
        self.cache = {}
        self.cache_ttl = 3600  # 1 hora (estandarizado)
        self.cache_expiry = {}
        self.SENTIMIENTO_LIMIT = 10  # PUNTO 1: Aumentado para mejor análisis
        self.logger.info("✅ Analizador de correlaciones inicializado")
    
    def calcular_correlacion_activos(
        self, 
        tickers: List[str], 
        periodo: str = '1y'
    ) -> Dict[str, Any]:
        """
        Calcula la matriz de correlación entre activos
        
        Args:
            tickers: Lista de tickers (ej: ['AAPL', 'MSFT', 'GOOGL'])
            periodo: Periodo de datos ('1y', '6mo', '3mo', etc)
            
        Returns:
            Diccionario con matriz y análisis
        """
        try:
            cache_key = f"correlation_{'_'.join(sorted(tickers))}_{periodo}"
            if self._es_cache_valido(cache_key):
                return self.cache[cache_key]
            
            # Obtener datos históricos
            datos = yf.download(tickers, period=periodo, progress=False)['Adj Close']
            
            # Si es solo un ticker, yfinance retorna Series
            if isinstance(datos, pd.Series):
                datos = datos.to_frame(tickers[0]) if tickers else datos
            
            # Calcular retornos diarios
            retornos = datos.pct_change().dropna()
            
            # Matriz de correlación (método pearson por defecto)
            correlacion = retornos.corr()
            
            # Matriz de correlación Spearman (más robusta)
            correlacion_spearman = retornos.corr(method='spearman')
            
            # Volatilidades claras: diaria y anualizada
            volatilidad_diaria = retornos.std()
            volatilidad_anualizada = volatilidad_diaria * np.sqrt(252)
            
            resultado = {
                'timestamp': datetime.now().isoformat(),
                'tickers': tickers,
                'periodo': periodo,
                'correlacion_pearson': correlacion.to_dict(),
                'correlacion_spearman': correlacion_spearman.to_dict(),
                'pares_altamente_correlacionados': self._encontrar_altas_correlaciones(correlacion, 0.7),
                'pares_descorrelacionados': self._encontrar_bajas_correlaciones(correlacion, 0.3),
                'volatilidad_diaria_pct': (volatilidad_diaria * 100).to_dict(),
                'volatilidad_anualizada_pct': (volatilidad_anualizada * 100).to_dict()
            }
            
            self.cache[cache_key] = resultado
            self.cache_expiry[cache_key] = datetime.now()
            
            return resultado
            
        except Exception as e:
            self.logger.warning(f"Error calculando correlaciones: {e}")
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def calcular_beta(self, ticker: str, benchmark: str = '^GSPC', periodo: str = '1y') -> Optional[float]:
        """
        Calcula el beta de un activo respecto a un benchmark
        
        Args:
            ticker: Ticker del activo
            benchmark: Benchmark (default: S&P 500)
            periodo: Periodo de cálculo
            
        Returns:
            Valor de beta
        """
        try:
            cache_key = f"beta_{ticker}_{benchmark}_{periodo}"
            if self._es_cache_valido(cache_key):
                return self.cache[cache_key]
            
            # Obtener datos
            datos = yf.download([ticker, benchmark], period=periodo, progress=False)['Adj Close']
            
            # Calcular retornos
            retornos = datos.pct_change().dropna()
            
            # Calcular covarianza y varianza
            cov = retornos[[ticker, benchmark]].cov().iloc[0, 1]
            var_benchmark = retornos[benchmark].var()
            
            beta = cov / var_benchmark if var_benchmark != 0 else np.nan
            
            self.cache[cache_key] = beta
            self.cache_expiry[cache_key] = datetime.now()
            
            return beta
            
        except Exception as e:
            self.logger.warning(f"Error calculando beta: {e}")
            return None
    
    def analizar_diversificacion(self, tickers: List[str]) -> Dict[str, Any]:
        """
        Analiza el potencial de diversificación de una cartera
        
        Args:
            tickers: Lista de tickers en la cartera
            
        Returns:
            Análisis de diversificación
        """
        try:
            correlaciones = self.calcular_correlacion_activos(tickers, '1y')
            
            if 'error' in correlaciones:
                return correlaciones
            
            # Calcular correlación promedio
            corr_matrix = pd.DataFrame(correlaciones['correlacion_pearson'])
            
            # Correlación promedio (excluyendo diagonal)
            corr_promedio = []
            for i in range(len(tickers)):
                for j in range(i+1, len(tickers)):
                    corr_promedio.append(corr_matrix.iloc[i, j])
            
            corr_promedio_valor = np.mean(corr_promedio) if corr_promedio else 0
            
            resultado = {
                'timestamp': datetime.now().isoformat(),
                'cartera': tickers,
                'correlacion_promedio': corr_promedio_valor,
                'puntaje_diversificacion': self._calcular_puntaje_diversificacion(corr_promedio_valor),
                'recomendacion': self._generar_recomendacion_diversificacion(corr_promedio_valor),
                'pares_altamente_correlacionados': correlaciones.get('pares_altamente_correlacionados', []),
                'activos_redundantes': [p for p in correlaciones.get('pares_altamente_correlacionados', []) if p[0] in tickers]
            }
            
            return resultado
            
        except Exception as e:
            self.logger.warning(f"Error analizando diversificación: {e}")
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def detectar_contagio_sistematico(self, ticker: str, mercado: str = '^GSPC') -> Dict[str, Any]:
        """
        Detecta si un activo es sensible a movimientos de mercado (riesgo sistemático)
        
        Args:
            ticker: Ticker a analizar
            mercado: Índice de mercado
            
        Returns:
            Análisis de riesgo sistemático
        """
        try:
            beta = self.calcular_beta(ticker, mercado, '1y')
            
            if beta is None:
                return {'error': 'No se pudo calcular beta', 'timestamp': datetime.now().isoformat()}
            
            resultado = {
                'ticker': ticker,
                'beta': beta,
                'timestamp': datetime.now().isoformat(),
                'interpretacion': self._interpretar_beta(beta),
                'riesgo_sistematico': 'Alto' if abs(beta) > 1.2 else ('Bajo' if abs(beta) < 0.8 else 'Medio'),
                'recomendacion': self._recomendar_segun_beta(beta)
            }
            
            return resultado
            
        except Exception as e:
            self.logger.warning(f"Error detectando contagio: {e}")
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def _encontrar_altas_correlaciones(self, corr_matrix: pd.DataFrame, umbral: float = 0.7) -> List[tuple]:
        """Encuentra pares altamente correlacionados"""
        pares = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) > umbral:
                    pares.append((
                        corr_matrix.columns[i],
                        corr_matrix.columns[j],
                        float(corr_matrix.iloc[i, j])
                    ))
        return sorted(pares, key=lambda x: abs(x[2]), reverse=True)
    
    def _encontrar_bajas_correlaciones(self, corr_matrix: pd.DataFrame, umbral: float = 0.3) -> List[tuple]:
        """Encuentra pares descorrelacionados (buenos para diversificación)"""
        pares = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) < umbral:
                    pares.append((
                        corr_matrix.columns[i],
                        corr_matrix.columns[j],
                        float(corr_matrix.iloc[i, j])
                    ))
        return sorted(pares, key=lambda x: abs(x[2]))
    
    def _calcular_puntaje_diversificacion(self, corr_promedio: Union[float, np.floating]) -> float:
        """Calcula puntaje de diversificación (0-100)"""
        # Mientras menor la correlación, mejor la diversificación
        corr_float = float(corr_promedio)
        puntaje = max(0, min(100, (1 - corr_float) * 100))
        return round(puntaje, 2)
    
    def _generar_recomendacion_diversificacion(self, corr_promedio: Union[float, np.floating]) -> str:
        """Genera recomendación basada en correlación"""
        corr_float = float(corr_promedio)
        if corr_float < 0.3:
            return "✅ Cartera bien diversificada"
        elif corr_float < 0.6:
            return "⚠️ Diversificación moderada, considere agregar activos descorrelacionados"
        else:
            return "❌ Baja diversificación, muchos activos correlacionados"
    
    def _interpretar_beta(self, beta: float) -> str:
        """Interpreta el valor de beta"""
        if beta > 1.2:
            return "Muy agresivo - 20%+ más volátil que el mercado"
        elif beta > 1:
            return "Agresivo - Más volátil que el mercado"
        elif beta > 0.8:
            return "Moderado - Similar al mercado"
        elif beta > 0:
            return "Defensivo - Menos volátil que el mercado"
        else:
            return "Contra-cíclico - Movimiento inverso al mercado"
    
    def _recomendar_segun_beta(self, beta: float) -> str:
        """Recomendación según beta"""
        if beta > 1.5:
            return "Alto riesgo: Solo para carteras agresivas"
        elif beta > 1:
            return "Riesgo moderado-alto: Incluir en carteras balanceadas"
        elif beta > 0:
            return "Riesgo moderado: Apto para carteras conservadoras"
        else:
            return "Potencial cobertura: Considerar para hedge"
    
    def _es_cache_valido(self, key: str) -> bool:
        """Verifica si cache es válido"""
        if key not in self.cache or key not in self.cache_expiry:
            return False
        
        tiempo_desde_cache = (datetime.now() - self.cache_expiry[key]).total_seconds()
        return tiempo_desde_cache < self.cache_ttl
    
    def limpiar_cache(self):
        """Limpia el cache"""
        self.cache.clear()
        self.cache_expiry.clear()
        self.logger.info("Cache de correlaciones limpiado")
