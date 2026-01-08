"""
analisis/enhanced_analyzer.py
Analizador mejorado que integra todos los módulos de análisis
Motor central de análisis 360
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from .analyzer import Analyzer
from .correlation_analyzer import CorrelationAnalyzer
from .ml_predictor import MLPredictor
from data_sources import (
    MarketDataManager,
    MacroeconomicDataManager,
    FundamentalAnalyzer
)


class EnhancedAnalyzer:
    """Analizador mejorado con integración completa de todos los módulos"""
    
    def __init__(self, knowledge_manager=None):
        """
        Inicializa el analizador mejorado
        
        Args:
            knowledge_manager: Gestor de conocimiento del cerebro
        """
        self.logger = logging.getLogger("EnhancedAnalyzer")
        
        # Módulos clave
        self.analyzer = Analyzer(knowledge_manager)
        self.correlation_analyzer = CorrelationAnalyzer()
        self.ml_predictor = MLPredictor()
        
        # Fuentes de datos
        self.market_data = MarketDataManager()
        self.macro_data = MacroeconomicDataManager()
        self.fundamental_analyzer = FundamentalAnalyzer()
        
        self.knowledge_manager = knowledge_manager
        self.logger.info("✅ Enhanced Analyzer inicializado")
    
    def analizar_360(self, ticker: str) -> Dict[str, Any]:
        """
        Análisis completo 360 de un activo
        Integra técnico, fundamental, macroeconómico y predicción
        
        Args:
            ticker: Símbolo del ticker
            
        Returns:
            Análisis comprensivo
        """
        try:
            resultado = {
                'ticker': ticker,
                'timestamp': datetime.now().isoformat(),
                'analisis': {}
            }
            
            # IMPORTAR VALIDADOR
            from data_sources import DataValidator
            validator = DataValidator()
            
            # 1. DATOS TÉCNICOS Y DE MERCADO
            self.logger.info(f"Obteniendo datos técnicos para {ticker}...")
            datos_mercado = self.market_data.obtener_datos_actuales(ticker)
            
            # VALIDAR DATOS DE MERCADO
            is_valid, errors = validator.validar_datos_mercado_completos(datos_mercado, ticker)
            if not is_valid:
                self.logger.error(f"❌ Datos de mercado inválidos: {errors}")
                return {'ticker': ticker, 'error': f'Datos de mercado incompletos: {errors}', 'timestamp': datetime.now().isoformat()}
            
            resultado['analisis']['mercado'] = datos_mercado
            
            # 2. ANÁLISIS TÉCNICO
            self.logger.info(f"Realizando análisis técnico para {ticker}...")
            analisis_tecnico = self.analyzer.analizar_datos(datos_mercado, f"Análisis técnico {ticker}")
            resultado['analisis']['tecnico'] = analisis_tecnico
            
            # 3. ANÁLISIS FUNDAMENTAL
            self.logger.info(f"Obteniendo datos fundamentales de {ticker}...")
            info_fundamental = self.fundamental_analyzer.obtener_info_fundamental(ticker)
            earnings = self.fundamental_analyzer.obtener_reporte_earnings(ticker)
            
            # VALIDAR FUNDAMENTALES
            is_valid, errors = validator.validar_fundamentales_completos(info_fundamental, ticker)
            if not is_valid:
                self.logger.warning(f"⚠️  Fundamentales incompletos: {errors}")
            
            resultado['analisis']['fundamental'] = {
                'info': info_fundamental,
                'earnings': earnings,
                'validacion_errores': errors if not is_valid else []
            }
            
            # 4. ANÁLISIS MACROECONÓMICO
            self.logger.info("Obteniendo contexto macroeconómico...")
            contexto_macro = self.macro_data.obtener_contexto_macro_resumido()
            resultado['analisis']['macroeconomico'] = contexto_macro
            
            # 5. VOLATILIDAD Y RIESGO
            self.logger.info(f"Analizando volatilidad y riesgo de {ticker}...")
            volatilidad = self.ml_predictor.calcular_volatilidad_implicita(ticker)
            riesgo_downside = self.ml_predictor.analizar_riesgo_downside(ticker)
            resultado['analisis']['volatilidad_riesgo'] = {
                'volatilidad': volatilidad,
                'riesgo_downside': riesgo_downside
            }
            
            # 6. PREDICCIÓN CON ML
            self.logger.info(f"Generando predicción para {ticker}...")
            prediccion_30d = self.ml_predictor.predecir_precio(ticker, dias_futuros=30)
            proyeccion_5y = self.ml_predictor.proyeccion_largo_plazo(ticker, anos=5)
            resultado['analisis']['predicciones'] = {
                'corto_plazo_30d': prediccion_30d,
                'largo_plazo_5y': proyeccion_5y
            }
            
            # 7. RESUMEN EJECUTIVO Y RECOMENDACIÓN
            resultado['resumen_ejecutivo'] = self._generar_resumen_ejecutivo(resultado)
            resultado['recomendacion'] = self._generar_recomendacion(resultado)
            
            return resultado
            
        except Exception as e:
            self.logger.error(f"Error en análisis 360: {e}")
            return {
                'ticker': ticker,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def analizar_cartera(self, tickers: List[str]) -> Dict[str, Any]:
        """
        Análisis de cartera con diversificación y correlaciones
        
        Args:
            tickers: Lista de tickers en la cartera
            
        Returns:
            Análisis de cartera
        """
        try:
            resultado = {
                'cartera': tickers,
                'timestamp': datetime.now().isoformat(),
                'analisis': {}
            }
            
            # Análisis individual
            self.logger.info(f"Analizando {len(tickers)} activos...")
            activos_analisis = {}
            for ticker in tickers:
                try:
                    analisis_360 = self.analizar_360(ticker)
                    activos_analisis[ticker] = {
                        'precio': analisis_360.get('analisis', {}).get('mercado', {}).get('precio'),
                        'tendencia': analisis_360.get('analisis', {}).get('tecnico', {}).get('hallazgos'),
                        'recomendacion': analisis_360.get('recomendacion')
                    }
                except Exception as e:
                    self.logger.warning(f"Error analizando {ticker}: {e}")
                    activos_analisis[ticker] = {'error': str(e)}
            
            resultado['activos'] = activos_analisis
            
            # Análisis de correlaciones
            self.logger.info("Analizando correlaciones...")
            correlaciones = self.correlation_analyzer.calcular_correlacion_activos(tickers)
            resultado['correlaciones'] = correlaciones
            
            # Análisis de diversificación
            self.logger.info("Analizando diversificación...")
            diversificacion = self.correlation_analyzer.analizar_diversificacion(tickers)
            resultado['diversificacion'] = diversificacion
            
            # Análisis de riesgo sistematico
            self.logger.info("Analizando riesgo sistematico...")
            riesgo_sistematico = {}
            for ticker in tickers[:5]:  # Limitado a 5 para performance
                riesgo_sistematico[ticker] = self.correlation_analyzer.detectar_contagio_sistematico(ticker)
            resultado['riesgo_sistematico'] = riesgo_sistematico
            
            # Resumen de cartera
            resultado['resumen_cartera'] = self._generar_resumen_cartera(resultado)
            
            return resultado
            
        except Exception as e:
            self.logger.error(f"Error analizando cartera: {e}")
            return {
                'cartera': tickers,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def comparar_activos(self, ticker1: str, ticker2: str) -> Dict[str, Any]:
        """
        Comparación detallada entre dos activos
        
        Args:
            ticker1: Primer ticker
            ticker2: Segundo ticker
            
        Returns:
            Comparativa
        """
        try:
            self.logger.info(f"Comparando {ticker1} vs {ticker2}...")
            
            # Análisis individual
            analisis_1 = self.analizar_360(ticker1)
            analisis_2 = self.analizar_360(ticker2)
            
            # Comparación fundamental
            comp_fundamental = self.fundamental_analyzer.comparar_pares(ticker1, ticker2)
            
            resultado = {
                'comparacion': {
                    'ticker1': ticker1,
                    'ticker2': ticker2
                },
                'timestamp': datetime.now().isoformat(),
                'analisis_1': analisis_1,
                'analisis_2': analisis_2,
                'comparacion_fundamental': comp_fundamental,
                'ganador': self._determinar_ganador(analisis_1, analisis_2)
            }
            
            return resultado
            
        except Exception as e:
            self.logger.error(f"Error comparando activos: {e}")
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def _generar_resumen_ejecutivo(self, analisis_360: Dict[str, Any]) -> str:
        """Genera un resumen ejecutivo basado en el análisis 360"""
        try:
            ticker = analisis_360.get('ticker', 'N/A')
            tecnico = analisis_360.get('analisis', {}).get('tecnico', {})
            fundamental = analisis_360.get('analisis', {}).get('fundamental', {})
            prediccion = analisis_360.get('analisis', {}).get('predicciones', {})
            
            resumen = f"""
📊 RESUMEN EJECUTIVO - {ticker}

🔍 ANÁLISIS TÉCNICO:
{str(tecnico.get('hallazgos', [])[:2])}

💰 ANÁLISIS FUNDAMENTAL:
Valuación: {str(fundamental.get('info', {}).get('valuacion', {}).get('pe_ratio', 'N/A'))}
ROE: {str(fundamental.get('info', {}).get('rentabilidad', {}).get('roe', 'N/A'))}

📈 PROYECCIÓN (30 días):
Tendencia: {str(prediccion.get('corto_plazo_30d', {}).get('tendencia', 'N/A'))}

⚠️ CONTEXTO MACRO:
Tasas 10Y: {str(analisis_360.get('analisis', {}).get('macroeconomico', {}).get('tasas_interes', {}).get('10y', 'N/A'))}%
Desempleo: {str(analisis_360.get('analisis', {}).get('macroeconomico', {}).get('desempleo', 'N/A'))}%
            """
            return resumen
            
        except Exception as e:
            return f"Error generando resumen: {e}"
    
    def _generar_recomendacion(self, analisis_360: Dict[str, Any]) -> str:
        """Genera una recomendación basada en el análisis"""
        try:
            tecnico = analisis_360.get('analisis', {}).get('tecnico', {})
            recomendaciones_tecnicas = tecnico.get('recomendaciones', [])
            
            if any('alcista' in str(r).lower() for r in recomendaciones_tecnicas):
                return "🟢 BUY - Señales alcistas detectadas"
            elif any('bajista' in str(r).lower() for r in recomendaciones_tecnicas):
                return "🔴 SELL - Señales bajistas detectadas"
            else:
                return "🟡 HOLD - Mercado neutral, mantener posición"
                
        except Exception:
            return "⚪ Análisis - Insuficientes datos"
    
    def _generar_resumen_cartera(self, analisis_cartera: Dict[str, Any]) -> str:
        """Genera un resumen de la cartera"""
        diversificacion = analisis_cartera.get('diversificacion', {})
        puntaje = diversificacion.get('puntaje_diversificacion', 0)
        
        return f"""
📊 RESUMEN CARTERA
- Diversificación: {puntaje}/100
- Recomendación: {diversificacion.get('recomendacion', 'N/A')}
- Correlación promedio: {diversificacion.get('correlacion_promedio', 'N/A')}
        """
    
    def _determinar_ganador(self, analisis_1: Dict[str, Any], analisis_2: Dict[str, Any]) -> str:
        """Determina cuál activo es mejor"""
        try:
            score_1 = 0
            score_2 = 0
            
            # Scores técnicos
            tecnico_1 = len(analisis_1.get('analisis', {}).get('tecnico', {}).get('hallazgos', []))
            tecnico_2 = len(analisis_2.get('analisis', {}).get('tecnico', {}).get('hallazgos', []))
            score_1 += tecnico_1
            score_2 += tecnico_2
            
            # Scores fundamentales
            pe_1 = analisis_1.get('analisis', {}).get('fundamental', {}).get('info', {}).get('valuacion', {}).get('pe_ratio')
            pe_2 = analisis_2.get('analisis', {}).get('fundamental', {}).get('info', {}).get('valuacion', {}).get('pe_ratio')
            
            if pe_1 and pe_2 and isinstance(pe_1, (int, float)) and isinstance(pe_2, (int, float)):
                if pe_1 < pe_2:
                    score_1 += 1
                else:
                    score_2 += 1
            
            ticker_1 = analisis_1.get('ticker', 'Activo 1')
            ticker_2 = analisis_2.get('ticker', 'Activo 2')
            
            if score_1 > score_2:
                return f"✅ {ticker_1} es más atractivo"
            elif score_2 > score_1:
                return f"✅ {ticker_2} es más atractivo"
            else:
                return "🔀 Ambos activos son similares"
                
        except Exception:
            return "⚪ Análisis comparativo limitado"
    
    def analizar_convergencia(self, ticker: str, dias: int = 20) -> Dict[str, Any]:
        """
        Analiza la convergencia de precios y volumen
        Detecta si el activo está convergiendo o divergiendo
        
        Args:
            ticker: Ticker del activo
            dias: Periodo de análisis en días (default: 20)
            
        Returns:
            Diccionario con análisis de convergencia
        """
        try:
            import yfinance as yf
            import pandas as pd
            
            self.logger.info(f"Analizando convergencia para {ticker}...")
            
            # Obtener datos históricos
            datos = yf.download(ticker, period='3mo', progress=False)
            
            if datos.empty:
                return {
                    "ticker": ticker,
                    "error": "No hay datos disponibles",
                    "tipo": "convergencia"
                }
            
            # Calcular medias móviles del precio
            datos['SMA_precio'] = datos['Close'].rolling(window=dias).mean()
            
            # Calcular desviación estándar del precio
            datos['Volatilidad'] = datos['Close'].rolling(window=dias).std()
            
            # Calcular medias móviles del volumen
            datos['SMA_volumen'] = datos['Volume'].rolling(window=dias).mean()
            datos['Volatilidad_vol'] = datos['Volume'].rolling(window=dias).std()
            
            # Detectar convergencia
            # Un precio converge si su volatilidad es baja respecto al promedio
            volatilidad_promedio = datos['Volatilidad'].mean()
            volatilidad_actual = datos['Volatilidad'].iloc[-1]
            
            if pd.isna(volatilidad_promedio) or pd.isna(volatilidad_actual):
                volatilidad_promedio = 0
                volatilidad_actual = 0
            
            precio_converge = (volatilidad_actual < volatilidad_promedio * 0.7)
            
            # Volumen también converge
            vol_promedio = datos['Volatilidad_vol'].mean()
            vol_actual = datos['Volatilidad_vol'].iloc[-1]
            
            if pd.isna(vol_promedio) or pd.isna(vol_actual):
                vol_promedio = 0
                vol_actual = 0
            
            volumen_converge = (vol_actual < vol_promedio * 0.7)
            
            # Calcular ratio de convergencia
            ratio_convergencia = (
                (volatilidad_promedio - volatilidad_actual) / volatilidad_promedio * 100
            ) if volatilidad_promedio > 0 else 0
            
            # Generar análisis
            analisis = {
                "ticker": ticker,
                "tipo": "convergencia",
                "timestamp": datetime.now().isoformat(),
                "precio_convergencia": bool(precio_converge),
                "volumen_convergencia": bool(volumen_converge),
                "ambos_convergen": bool(precio_converge and volumen_converge),
                "dias_analizados": dias,
                "volatilidad_actual": float(volatilidad_actual) if not pd.isna(volatilidad_actual) else 0,
                "volatilidad_promedio": float(volatilidad_promedio) if not pd.isna(volatilidad_promedio) else 0,
                "ratio_convergencia_pct": round(float(ratio_convergencia), 2),
            }
            
            # Interpretación
            if precio_converge and volumen_converge:
                analisis["interpretacion"] = "✅ Fuerte convergencia: Precio y volumen estables"
                analisis["implicacion"] = "Punto de ruptura potencial próximo"
            elif precio_converge:
                analisis["interpretacion"] = "⚠️  Convergencia de precio: Volumen aún irregular"
                analisis["implicacion"] = "Posible consolidación"
            elif volumen_converge:
                analisis["interpretacion"] = "⚠️  Convergencia de volumen: Precio aún volátil"
                analisis["implicacion"] = "Esperar estabilidad de precio"
            else:
                analisis["interpretacion"] = "❌ Sin convergencia: Volatilidad normal"
                analisis["implicacion"] = "Movimiento de mercado esperado"
            
            self.logger.info(f"✅ Análisis de convergencia completado para {ticker}")
            return analisis
            
        except Exception as e:
            self.logger.error(f"Error en análisis de convergencia: {e}")
            return {
                "ticker": ticker,
                "error": str(e),
                "tipo": "convergencia"
            }
    
    def limpiar_caches(self):
        """Limpia todos los cachés"""
        self.analyzer.limpiar_cache()
        self.correlation_analyzer.limpiar_cache()
        self.ml_predictor.limpiar_cache()
        self.fundamental_analyzer.limpiar_cache()
        self.macro_data.limpiar_cache()
        self.logger.info("✅ Todos los cachés limpiados")
