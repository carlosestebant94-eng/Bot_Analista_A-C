"""
analisis/ml_predictor.py
Predictor mejorado con Machine Learning
Usa múltiples modelos para proyecciones más precisas
"""

import logging
import numpy as np
import pandas as pd
import yfinance as yf
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import warnings

warnings.filterwarnings('ignore')


class MLPredictor:
    """Predictor de precios usando Machine Learning"""
    
    def __init__(self):
        """Inicializa el predictor ML"""
        self.logger = logging.getLogger("MLPredictor")
        self.scaler = MinMaxScaler()
        self.cache = {}
        self.cache_ttl = 3600
        self.cache_expiry = {}
        self.logger.info("[OK] Predictor ML inicializado")
    
    def predecir_precio(
        self, 
        ticker: str, 
        dias_futuros: int = 30,
        usar_ensemble: bool = True
    ) -> Dict[str, Any]:
        """
        Predice el precio futuro de un activo
        
        Args:
            ticker: Ticker del activo
            dias_futuros: Días a predecir (default: 30)
            usar_ensemble: Usar múltiples modelos (default: True)
            
        Returns:
            Predicción con confianza
        """
        try:
            # IMPORTAR VALIDADOR
            from data_sources import DataValidator
            validator = DataValidator()
            
            cache_key = f"prediccion_{ticker}_{dias_futuros}"
            if self._es_cache_valido(cache_key):
                return self.cache[cache_key]
            
            # Obtener datos históricos
            stock = yf.Ticker(ticker)
            datos = yf.download(ticker, period='2y', progress=False)
            
            # VALIDAR HISTÓRICO
            is_valid, err = validator.validar_historico(datos, ticker)
            if not is_valid:
                self.logger.error(f"❌ {err}")
                return {'error': f'Datos históricos inválidos: {err}', 
                       'ticker': ticker,
                       'timestamp': datetime.now().isoformat()}
            
            # Preparar features
            X, y, precio_actual = self._preparar_features(datos)
            
            if X is None:
                return {'error': 'Datos insuficientes para ML', 
                       'ticker': ticker,
                       'timestamp': datetime.now().isoformat()}
            
            resultado = {
                'ticker': ticker,
                'timestamp': datetime.now().isoformat(),
                'precio_actual': float(precio_actual),
                'dias_prediccion': dias_futuros,
                'predicciones': {}
            }
            
            if usar_ensemble:
                # Ensemble de modelos
                predicciones = self._ensemble_prediction(X, y, dias_futuros)
                resultado['predicciones']['ensemble'] = predicciones['prediccion']
                resultado['confianza_ensemble'] = predicciones['confianza']
                resultado['rango'] = {
                    'minimo': predicciones['rango_min'],
                    'maximo': predicciones['rango_max']
                }
            else:
                # Modelo individual
                prediccion = self._predecir_con_random_forest(X, y, dias_futuros)
                resultado['predicciones']['random_forest'] = prediccion['prediccion']
                resultado['confianza'] = prediccion['confianza']
            
            # Análisis de tendencia
            resultado['tendencia'] = self._analizar_tendencia_prediccion(
                float(precio_actual), 
                resultado['predicciones']
            )
            
            self.cache[cache_key] = resultado
            self.cache_expiry[cache_key] = datetime.now()
            
            return resultado
            
        except Exception as e:
            self.logger.warning(f"Error en predicción de {ticker}: {e}")
            return {'error': str(e), 'ticker': ticker, 
                   'timestamp': datetime.now().isoformat()}
    
    def calcular_volatilidad_implicita(self, ticker: str) -> Dict[str, Any]:
        """
        Calcula la volatilidad esperada basada en datos históricos
        
        Args:
            ticker: Ticker del activo
            
        Returns:
            Volatilidad en diferentes períodos
        """
        try:
            datos = yf.download(ticker, period='2y', progress=False)
            
            retornos = datos['Adj Close'].pct_change().dropna()
            
            # Volatilidad en diferentes períodos (anualizada en porcentaje)
            # Fórmula: σ_diaria * √252 * 100 (para convertir a porcentaje anualizado)
            volatilidad_30d = (retornos.rolling(window=30).std().iloc[-1] * np.sqrt(252)) * 100
            volatilidad_60d = (retornos.rolling(window=60).std().iloc[-1] * np.sqrt(252)) * 100
            volatilidad_anual = (retornos.std() * np.sqrt(252)) * 100
            
            resultado = {
                'ticker': ticker,
                'timestamp': datetime.now().isoformat(),
                'volatilidad_30d': round(volatilidad_30d, 2),
                'volatilidad_60d': round(volatilidad_60d, 2),
                'volatilidad_anual': round(volatilidad_anual, 2),
                'volatilidad_promedio': round(np.mean([volatilidad_30d, volatilidad_60d, volatilidad_anual]), 2),
                'interpretacion': self._interpretar_volatilidad(volatilidad_anual)
            }
            
            return resultado
            
        except Exception as e:
            self.logger.warning(f"Error calculando volatilidad: {e}")
            return {'error': str(e), 'ticker': ticker}
    
    def analizar_riesgo_downside(self, ticker: str, dias: int = 30) -> Dict[str, Any]:
        """
        Analiza el riesgo de caída (worst-case scenario)
        
        Args:
            ticker: Ticker del activo
            dias: Período de análisis
            
        Returns:
            Análisis de riesgo downside
        """
        try:
            datos = yf.download(ticker, period='2y', progress=False)
            retornos = datos['Adj Close'].pct_change().dropna()
            
            # Percentiles de pérdida
            var_95 = np.percentile(retornos, 5) * 100  # Value at Risk 95%
            var_99 = np.percentile(retornos, 1) * 100  # Value at Risk 99%
            peor_dia = retornos.min() * 100
            promedio_dias_bajos = retornos[retornos < retornos.quantile(0.25)].mean() * 100
            
            precio_actual = datos['Adj Close'].iloc[-1]
            precio_var_95 = precio_actual * (1 + var_95/100)
            precio_var_99 = precio_actual * (1 + var_99/100)
            
            resultado = {
                'ticker': ticker,
                'timestamp': datetime.now().isoformat(),
                'precio_actual': float(precio_actual),
                'riesgo_downside': {
                    'var_95': round(var_95, 2),
                    'var_99': round(var_99, 2),
                    'peor_dia_historico': round(peor_dia, 2),
                    'promedio_dias_bajos': round(promedio_dias_bajos, 2)
                },
                'precio_esperado_95': round(precio_var_95, 2),
                'precio_esperado_99': round(precio_var_99, 2),
                'recomendacion': self._recomendar_segun_riesgo(var_95)
            }
            
            return resultado
            
        except Exception as e:
            self.logger.warning(f"Error analizando riesgo downside: {e}")
            return {'error': str(e), 'ticker': ticker}
    
    def proyeccion_largo_plazo(self, ticker: str, anos: int = 5) -> Dict[str, Any]:
        """
        Proyección a largo plazo con incertidumbre
        
        Args:
            ticker: Ticker del activo
            anos: Años a proyectar
            
        Returns:
            Proyección a largo plazo
        """
        try:
            stock = yf.Ticker(ticker)
            datos = yf.download(ticker, period='5y', progress=False)
            
            if datos.empty:
                return {'error': 'Datos insuficientes'}
            
            # Retorno anual promedio
            retorno_anual = (datos['Adj Close'].iloc[-1] / datos['Adj Close'].iloc[0]) ** (1/5) - 1
            volatilidad = datos['Adj Close'].pct_change().std() * np.sqrt(252)
            
            precio_actual = datos['Adj Close'].iloc[-1]
            
            # Proyecciones usando intervalo de confianza (±1.96σ para 95%)
            # Fórmula más robusta que sumar/restar volatilidad: P_base * exp(±z * σ_acumulada)
            precio_base = precio_actual * ((1 + retorno_anual) ** anos)
            
            # Volatilidad acumulada para n años: σ_acumulada = σ_anual * √(n años)
            volatilidad_acumulada = volatilidad * np.sqrt(anos)
            
            # Rango usando intervalo de confianza (±1.96σ para 95%)
            escenarios = {
                'bullish': precio_base * np.exp(1.96 * volatilidad_acumulada),
                'base': precio_base,
                'bearish': precio_base * np.exp(-1.96 * volatilidad_acumulada)
            }
            
            resultado = {
                'ticker': ticker,
                'timestamp': datetime.now().isoformat(),
                'precio_actual': float(precio_actual),
                'anos_proyeccion': anos,
                'retorno_anual_historico': round(retorno_anual * 100, 2),
                'volatilidad_anual': round(volatilidad * 100, 2),
                'escenarios': {
                    'bullish': round(escenarios['bullish'], 2),
                    'base': round(escenarios['base'], 2),
                    'bearish': round(escenarios['bearish'], 2)
                },
                'rango_esperado': {
                    'minimo': round(escenarios['bearish'], 2),
                    'maximo': round(escenarios['bullish'], 2)
                }
            }
            
            return resultado
            
        except Exception as e:
            self.logger.warning(f"Error en proyección largo plazo: {e}")
            return {'error': str(e), 'ticker': ticker}
    
    def _preparar_features(self, datos: pd.DataFrame) -> Tuple[Optional[np.ndarray], Optional[np.ndarray], Optional[float]]:
        """Prepara features para el modelo"""
        try:
            close = datos['Adj Close'].values
            
            if len(close) < 30:
                return None, None, None
            
            # Crear features técnicos
            X_list = []
            y_list = []
            
            for i in range(30, len(close) - 1):
                # Últimos 30 precios normalizados
                ventana = close[i-30:i]
                ventana_norm = (ventana - ventana.min()) / (ventana.max() - ventana.min() + 1e-8)
                
                # Features adicionales
                cambio_pct = (close[i] - close[i-1]) / close[i-1]
                volatilidad = np.std(ventana) / np.mean(ventana)
                tendencia = (close[i] - close[i-30]) / close[i-30]
                
                features = np.concatenate([
                    ventana_norm,
                    [cambio_pct, volatilidad, tendencia, close[i]/np.mean(ventana)]
                ])
                
                X_list.append(features)
                y_list.append(close[i+1])
            
            X = np.array(X_list)
            y = np.array(y_list)
            precio_actual = close[-1]
            
            return X, y, precio_actual
            
        except Exception as e:
            self.logger.warning(f"Error preparando features: {e}")
            return None, None, None
    
    def _predecir_con_random_forest(self, X: np.ndarray, y: np.ndarray, 
                                    dias_futuros: int) -> Dict[str, Any]:
        """Predicción con Random Forest"""
        try:
            # PUNTO 1: Aumentado max_depth de 15 a 20 para mejor precisión
            rf = RandomForestRegressor(n_estimators=100, max_depth=20, random_state=42)
            rf.fit(X, y)
            
            # Último feature para predicción
            ultimo_feature = X[-1].reshape(1, -1)
            prediccion = rf.predict(ultimo_feature)[0]
            
            # Score
            y_pred = rf.predict(X[-100:])
            r2 = r2_score(y[-100:], y_pred)
            confianza = max(0, min(100, (r2 + 1) * 50))
            
            return {
                'prediccion': float(prediccion),
                'confianza': round(confianza, 2)
            }
        except:
            return {'prediccion': None, 'confianza': 0}
    
    def _ensemble_prediction(self, X: np.ndarray, y: np.ndarray, 
                            dias_futuros: int) -> Dict[str, Any]:
        """Predicción con ensemble de múltiples modelos"""
        try:
            predicciones = []
            confianzas = []
            
            # Random Forest
            # PUNTO 1: Aumentado max_depth de 15 a 20
            rf = RandomForestRegressor(n_estimators=100, max_depth=20, random_state=42)
            rf.fit(X, y)
            pred_rf = rf.predict(X[-1:].reshape(1, -1))[0]
            predicciones.append(pred_rf)
            
            y_pred_rf = rf.predict(X[-100:])
            r2_rf = r2_score(y[-100:], y_pred_rf)
            confianzas.append(max(0.1, (r2_rf + 1) * 50))
            
            # Gradient Boosting
            # PUNTO 1: Aumentado max_depth de 7 a 10
            gb = GradientBoostingRegressor(n_estimators=100, max_depth=10, random_state=42)
            gb.fit(X, y)
            pred_gb = gb.predict(X[-1:].reshape(1, -1))[0]
            predicciones.append(pred_gb)
            
            y_pred_gb = gb.predict(X[-100:])
            r2_gb = r2_score(y[-100:], y_pred_gb)
            confianzas.append(max(0.1, (r2_gb + 1) * 50))
            
            # Linear Regression
            lr = LinearRegression()
            lr.fit(X, y)
            pred_lr = lr.predict(X[-1:].reshape(1, -1))[0]
            predicciones.append(pred_lr)
            
            y_pred_lr = lr.predict(X[-100:])
            r2_lr = r2_score(y[-100:], y_pred_lr)
            confianzas.append(max(0.1, (r2_lr + 1) * 50))
            
            # Promedio ponderado
            confianzas = np.array(confianzas)
            pesos = confianzas / confianzas.sum()
            prediccion_ensemble = np.average(predicciones, weights=pesos)
            confianza_promedio = np.mean(confianzas)
            
            # Rango
            rango_min = np.min(predicciones)
            rango_max = np.max(predicciones)
            
            return {
                'prediccion': float(prediccion_ensemble),
                'confianza': round(confianza_promedio, 2),
                'rango_min': float(rango_min),
                'rango_max': float(rango_max),
                'predicciones_individuales': {
                    'random_forest': float(pred_rf),
                    'gradient_boosting': float(pred_gb),
                    'linear_regression': float(pred_lr)
                }
            }
        except Exception as e:
            self.logger.warning(f"Error en ensemble: {e}")
            return {'prediccion': None, 'confianza': 0, 'rango_min': None, 'rango_max': None}
    
    def _analizar_tendencia_prediccion(self, precio_actual: float, 
                                      predicciones: Dict) -> str:
        """Analiza la tendencia de la predicción"""
        if 'ensemble' in predicciones:
            pred = predicciones['ensemble']
        else:
            pred = list(predicciones.values())[0]
        
        if pred is None:
            return "Indeterminada"
        
        cambio = ((pred - precio_actual) / precio_actual) * 100
        
        if cambio > 5:
            return f"Alcista ({cambio:+.2f}%)"
        elif cambio < -5:
            return f"Bajista ({cambio:+.2f}%)"
        else:
            return f"Lateral ({cambio:+.2f}%)"
    
    def _interpretar_volatilidad(self, volatilidad: float) -> str:
        """Interpreta el nivel de volatilidad"""
        if volatilidad > 40:
            return "Muy Alta - Activo muy volátil"
        elif volatilidad > 25:
            return "Alta - Movimientos amplios esperados"
        elif volatilidad > 15:
            return "Moderada - Variabilidad normal"
        else:
            return "Baja - Activo estable"
    
    def _recomendar_segun_riesgo(self, var_95: float) -> str:
        """Recomendación según riesgo downside"""
        if var_95 < -10:
            return "Alto riesgo: Solo para carteras de riesgo alto"
        elif var_95 < -5:
            return "Riesgo moderado: Considerar posición defensiva"
        else:
            return "Riesgo bajo: Apto para carteras conservadoras"
    
    def _es_cache_valido(self, key: str) -> bool:
        """Verifica cache"""
        if key not in self.cache or key not in self.cache_expiry:
            return False
        
        tiempo = (datetime.now() - self.cache_expiry[key]).total_seconds()
        return tiempo < self.cache_ttl
    
    def limpiar_cache(self):
        """Limpia cache"""
        self.cache.clear()
        self.cache_expiry.clear()
        self.logger.info("Cache ML limpiado")
