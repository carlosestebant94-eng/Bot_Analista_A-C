"""
analisis/screener.py
Módulo de Screener Automático - Análisis multidimensional de símbolos financieros
Agrega datos de múltiples fuentes y genera recomendaciones por horizonte temporal
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from dataclasses import dataclass, asdict
from enum import Enum

try:
    from data_sources import MarketDataManager
except ImportError:
    # Fallback si está en contexto diferente
    MarketDataManager = None


class Timeframe(Enum):
    """Horizontes de inversión soportados"""
    SHORT_TERM = "corto_plazo"    # 1-3 días
    MEDIUM_TERM = "mediano_plazo"  # 1-4 semanas
    LONG_TERM = "largo_plazo"      # 3-12 meses


class RecommendationType(Enum):
    """Tipos de recomendación"""
    STRONG_BUY = "FUERTE COMPRA"
    BUY = "COMPRA"
    HOLD = "MANTENER"
    SELL = "VENTA"
    STRONG_SELL = "FUERTE VENTA"


@dataclass
class TechnicalIndicators:
    """Indicadores técnicos de un símbolo"""
    rsi: float  # Relative Strength Index (0-100)
    macd_signal: float  # MACD vs Signal Line
    ma_20: float  # Moving Average 20 días
    ma_50: float  # Moving Average 50 días
    bollinger_upper: float
    bollinger_lower: float
    precio_actual: float
    volumen_sma: float  # Volume SMA
    atr: float  # Average True Range


@dataclass
class ScreenerResult:
    """Resultado de análisis para un símbolo"""
    ticker: str
    timestamp: str
    timeframe: str
    precio_actual: float
    recomendacion: str
    score: float  # 0-100
    señales_compra: int
    señales_venta: int
    indicadores: Dict[str, float]
    razon_principal: str
    confianza: float  # 0-1
    variacion_esperada: float  # % esperado de cambio
    niveles_clave: Dict[str, float]  # resistencia, soporte


class ScreenerAutomatico:
    """
    Motor de screener automático para identificar oportunidades de inversión
    Analiza múltiples indicadores técnicos y genera recomendaciones por timeframe
    """
    
    def __init__(self, market_data_manager: Optional[Any] = None):
        """
        Inicializa el screener
        
        Args:
            market_data_manager: Referencia al gestor de datos de mercado
        """
        self.logger = logging.getLogger("ScreenerAutomatico")
        self.market_data = market_data_manager or MarketDataManager()
        self.cache_datos = {}
        self.logger.info("✅ Screener Automático inicializado")
    
    def analizar_simbolo(
        self,
        ticker: str,
        timeframe: Timeframe = Timeframe.MEDIUM_TERM,
        periodo_dias: int = 90
    ) -> Optional[ScreenerResult]:
        """
        Analiza un símbolo y genera recomendación
        
        Args:
            ticker: Símbolo a analizar (AAPL, MSFT, etc)
            timeframe: Horizonte de inversión
            periodo_dias: Período de análisis histórico
            
        Returns:
            ScreenerResult con análisis completo o None si falla
        """
        try:
            self.logger.info(f"🔍 Analizando {ticker} en {timeframe.value}...")
            
            # 1. Obtener datos históricos
            datos_historicos = self._obtener_datos_historicos(ticker, periodo_dias)
            if datos_historicos is None or datos_historicos.empty:
                self.logger.warning(f"⚠️  No se obtuvieron datos para {ticker}")
                return None
            
            # 2. Calcular indicadores técnicos
            indicadores = self._calcular_indicadores(datos_historicos, ticker)
            
            # 3. Obtener datos fundamentales/actuales
            datos_actuales = self.market_data.obtener_datos_actuales(ticker)
            
            # 4. Generar señales según timeframe
            señales = self._generar_señales(
                indicadores,
                datos_historicos,
                timeframe
            )
            
            # 5. Calcular score y recomendación
            score = self._calcular_score(señales, indicadores, timeframe)
            recomendacion = self._generar_recomendacion(score, señales)
            
            # 6. Calcular niveles clave
            niveles_clave = self._calcular_niveles_clave(datos_historicos)
            
            # 7. Estimar variación esperada
            variacion_esperada = self._estimar_variacion(indicadores, timeframe)
            
            # Construir resultado
            resultado = ScreenerResult(
                ticker=ticker,
                timestamp=datetime.now().isoformat(),
                timeframe=timeframe.value,
                precio_actual=datos_actuales.get("precio_actual", 0),
                recomendacion=recomendacion.value,
                score=score,
                señales_compra=sum(1 for s in señales if s > 0),
                señales_venta=sum(1 for s in señales if s < 0),
                indicadores=asdict(indicadores),
                razon_principal=self._generar_razon(señales, indicadores, timeframe),
                confianza=min(1.0, abs(score) / 100.0),
                variacion_esperada=variacion_esperada,
                niveles_clave=niveles_clave
            )
            
            self.logger.info(
                f"[OK] {ticker}: {resultado.recomendacion} (score: {float(score if score is not None else 50):.1f}, confianza: {float(resultado.confianza if resultado.confianza is not None else 0.5):.1%})"
            )
            
            return resultado
            
        except Exception as e:
            self.logger.error(f"❌ Error analizando {ticker}: {str(e)}")
            return None
    
    def _obtener_datos_historicos(self, ticker: str, dias: int = 90) -> Optional[pd.DataFrame]:
        """Obtiene datos históricos del ticker"""
        try:
            import yfinance as yf
            
            fecha_inicio = datetime.now() - timedelta(days=dias)
            datos = yf.download(
                ticker,
                start=fecha_inicio.date(),
                end=datetime.now().date(),
                progress=False
            )
            
            if datos.empty:
                return None
            
            self.cache_datos[ticker] = datos
            return datos
            
        except Exception as e:
            self.logger.error(f"Error descargando datos para {ticker}: {e}")
            return None
    
    def _calcular_indicadores(
        self,
        datos: pd.DataFrame,
        ticker: str
    ) -> TechnicalIndicators:
        """Calcula todos los indicadores técnicos"""
        
        try:
            close = datos['Close']
            volumen = datos['Volume']
            
            # RSI (14 períodos)
            rsi = self._calcular_rsi(close, 14)
            if pd.isna(rsi):
                rsi = 50.0
            
            # MACD
            macd_signal = self._calcular_macd(close)
            if pd.isna(macd_signal):
                macd_signal = 0.0
            
            # Medias móviles
            ma_20 = float(close.rolling(20).mean().iloc[-1].item())
            ma_50 = float(close.rolling(50).mean().iloc[-1].item())
            
            if pd.isna(ma_20):
                ma_20 = float(close.iloc[-1])
            if pd.isna(ma_50):
                ma_50 = float(close.iloc[-1])
            
            # Bandas de Bollinger
            bb = self._calcular_bollinger_bands(close, 20, 2)
            if pd.isna(bb['upper']):
                bb['upper'] = float(close.iloc[-1])
            if pd.isna(bb['lower']):
                bb['lower'] = float(close.iloc[-1])
            
            # ATR (Average True Range)
            atr = self._calcular_atr(datos, 14)
            if pd.isna(atr):
                atr = 0.0
            
            # Volume SMA
            volumen_sma = float(volumen.rolling(20).mean().iloc[-1].item())
            if pd.isna(volumen_sma):
                volumen_sma = float(volumen.iloc[-1].item())
            
            precio_actual = float(close.iloc[-1].item())
            
            return TechnicalIndicators(
                rsi=float(rsi),
                macd_signal=float(macd_signal),
                ma_20=float(ma_20),
                ma_50=float(ma_50),
                bollinger_upper=float(bb['upper']),
                bollinger_lower=float(bb['lower']),
                precio_actual=float(precio_actual),
                volumen_sma=float(volumen_sma),
                atr=float(atr)
            )
            
        except Exception as e:
            self.logger.error(f"Error calculando indicadores: {e}")
            # Retornar indicadores con valores por defecto
            return TechnicalIndicators(50.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    
    def _calcular_rsi(self, close: pd.Series, periodo: int = 14) -> float:
        """Calcula RSI (Relative Strength Index)"""
        try:
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=periodo).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=periodo).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            result = float(rsi.iloc[-1].item())
            
            if pd.isna(result):
                return 50.0
            return result
        except:
            return 50.0
    
    def _calcular_macd(self, close: pd.Series) -> float:
        """Calcula señal MACD vs Signal Line"""
        try:
            ema_12 = close.ewm(span=12).mean()
            ema_26 = close.ewm(span=26).mean()
            macd = ema_12 - ema_26
            signal = macd.ewm(span=9).mean()
            
            result = float(macd.iloc[-1].item() - signal.iloc[-1].item())
            if pd.isna(result):
                return 0.0
            return result
        except:
            return 0.0
    
    def _calcular_bollinger_bands(
        self,
        close: pd.Series,
        periodo: int = 20,
        desv_std: float = 2
    ) -> Dict[str, float]:
        """Calcula Bandas de Bollinger"""
        try:
            sma = close.rolling(window=periodo).mean()
            std = close.rolling(window=periodo).std()
            
            upper = sma + (std * desv_std)
            lower = sma - (std * desv_std)
            
            upper_val = float(upper.iloc[-1].item())
            lower_val = float(lower.iloc[-1].item())
            
            if pd.isna(upper_val):
                upper_val = float(close.iloc[-1])
            if pd.isna(lower_val):
                lower_val = float(close.iloc[-1])
            
            return {
                'upper': upper_val,
                'lower': lower_val
            }
        except:
            return {'upper': float(close.iloc[-1]), 'lower': float(close.iloc[-1])}
    
    def _calcular_atr(self, datos: pd.DataFrame, periodo: int = 14) -> float:
        """Calcula Average True Range"""
        try:
            high = datos['High']
            low = datos['Low']
            close = datos['Close']
            
            tr1 = high - low
            tr2 = abs(high - close.shift())
            tr3 = abs(low - close.shift())
            
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = tr.rolling(window=periodo).mean()
            
            result = float(atr.iloc[-1])
            if pd.isna(result):
                return 0.0
            return result
        except:
            return 0.0
    
    def _generar_señales(
        self,
        indicadores: TechnicalIndicators,
        datos: pd.DataFrame,
        timeframe: Timeframe
    ) -> List[float]:
        """
        Genera señales de compra/venta basadas en indicadores
        Retorna lista de señales: 1=compra, 0=neutral, -1=venta
        """
        señales = []
        
        # Señal RSI
        if indicadores.rsi < 30:
            señales.append(1.0)  # Sobrevendido = Compra
        elif indicadores.rsi > 70:
            señales.append(-1.0)  # Sobrecomprado = Venta
        else:
            señales.append(0.0)
        
        # Señal MACD
        señales.append(1.0 if indicadores.macd_signal > 0 else -1.0)
        
        # Señal Media Móviles
        if (indicadores.precio_actual > indicadores.ma_20 and 
            indicadores.ma_20 > indicadores.ma_50):
            señales.append(1.0)  # Tendencia alcista
        elif (indicadores.precio_actual < indicadores.ma_20 and 
              indicadores.ma_20 < indicadores.ma_50):
            señales.append(-1.0)  # Tendencia bajista
        else:
            señales.append(0.0)
        
        # Señal Bandas Bollinger
        if indicadores.precio_actual < indicadores.bollinger_lower:
            señales.append(1.0)  # Precio bajo, potencial rebote
        elif indicadores.precio_actual > indicadores.bollinger_upper:
            señales.append(-1.0)  # Precio alto, potencial corrección
        else:
            señales.append(0.0)
        
        # Señal Momentum (últimos 5 días)
        try:
            close = datos['Close']
            if len(close) >= 5:
                cambio_5d = (float(close.iloc[-1].item()) / float(close.iloc[-5].item()) - 1) * 100
                
                if timeframe == Timeframe.SHORT_TERM:
                    if cambio_5d > 5:
                        señales.append(-1.0)  # Muy alcista = tomar ganancias
                    elif cambio_5d < -5:
                        señales.append(1.0)  # Muy bajista = oportunidad
                    else:
                        señales.append(0.0)
                elif timeframe == Timeframe.MEDIUM_TERM:
                    if cambio_5d > 3:
                        señales.append(1.0)
                    elif cambio_5d < -3:
                        señales.append(-1.0)
                    else:
                        señales.append(0.0)
                else:  # LONG_TERM
                    señales.append(0.0)  # Momentum corto plazo menos relevante
            else:
                señales.append(0.0)
                
        except Exception as e:
            self.logger.debug(f"Error en señal de momentum: {e}")
            señales.append(0.0)
        
        return señales
    
    def _calcular_score(
        self,
        señales: List[float],
        indicadores: TechnicalIndicators,
        timeframe: Timeframe
    ) -> float:
        """
        Calcula score final de 0-100
        Basado en acuerdo de señales e indicadores
        """
        try:
            # Promedio ponderado de señales
            score_base = float(np.mean(señales) * 50 + 50)  # Convierte [-1,1] a [0,100]
            
            if pd.isna(score_base) or score_base is None:
                score_base = 50.0
            
            # Ajustes según timeframe
            if timeframe == Timeframe.SHORT_TERM:
                # Más peso a RSI y MACD
                rsi_val = float(indicadores.rsi) if indicadores.rsi is not None else 50.0
                rsi_score = 50 + (rsi_val - 50) * 0.5
                score = (score_base * 0.5) + (rsi_score * 0.5)
            elif timeframe == Timeframe.MEDIUM_TERM:
                # Equilibrio de indicadores
                score = score_base
            else:  # LONG_TERM
                # Más peso a tendencias de largo plazo
                precio = float(indicadores.precio_actual) if indicadores.precio_actual is not None else 0
                ma_50 = float(indicadores.ma_50) if indicadores.ma_50 is not None else precio
                if precio > ma_50:
                    score = score_base + 10
                else:
                    score = score_base - 10
            
            result = float(np.clip(float(score), 0, 100))
            if pd.isna(result) or result is None:
                return 50.0
            return result
        except Exception as e:
            self.logger.debug(f"Error calculando score: {e}")
            return 50.0
    
    def _generar_recomendacion(
        self,
        score: float,
        señales: List[float]
    ) -> RecommendationType:
        """Genera recomendación basada en score"""
        
        acuerdo = sum(1 for s in señales if s > 0) - sum(1 for s in señales if s < 0)
        
        if score >= 75 and acuerdo >= 3:
            return RecommendationType.STRONG_BUY
        elif score >= 60 and acuerdo >= 2:
            return RecommendationType.BUY
        elif score >= 40 and score <= 60:
            return RecommendationType.HOLD
        elif score <= 40 and acuerdo <= -2:
            return RecommendationType.SELL
        elif score <= 25 and acuerdo <= -3:
            return RecommendationType.STRONG_SELL
        else:
            return RecommendationType.HOLD
    
    def _generar_razon(
        self,
        señales: List[float],
        indicadores: TechnicalIndicators,
        timeframe: Timeframe
    ) -> str:
        """Genera explicación textual de la recomendación"""
        
        razones = []
        
        if timeframe == Timeframe.SHORT_TERM:
            if indicadores.rsi < 30:
                razones.append("RSI sobrevendido (oportunidad corto plazo)")
            elif indicadores.rsi > 70:
                razones.append("RSI sobrecomprado (tomar ganancias)")
        
        if indicadores.macd_signal > 0:
            razones.append("MACD alcista")
        else:
            razones.append("MACD bajista")
        
        if indicadores.precio_actual > indicadores.ma_50:
            razones.append("Precio por encima de MA50 (tendencia alcista)")
        else:
            razones.append("Precio por debajo de MA50 (tendencia bajista)")
        
        return " | ".join(razones) if razones else "Análisis en construcción"
    
    def _calcular_niveles_clave(self, datos: pd.DataFrame) -> Dict[str, float]:
        """Calcula niveles de soporte y resistencia"""
        try:
            high = datos['High']
            low = datos['Low']
            close = datos['Close']
            
            # Últimos 20 días
            data_recent = datos.tail(20)
            
            resistencia = float(data_recent['High'].max().item())
            soporte = float(data_recent['Low'].min().item())
            pivot = (resistencia + soporte + close.iloc[-1].item()) / 3
            
            return {
                'resistencia': resistencia,
                'soporte': soporte,
                'pivot': float(pivot),
                'precio_actual': close.iloc[-1].item()
            }
        except:
            return {}
    
    def _estimar_variacion(
        self,
        indicadores: TechnicalIndicators,
        timeframe: Timeframe
    ) -> float:
        """Estima variación esperada en %"""
        
        try:
            # Validar que tenemos valores válidos
            if (indicadores.precio_actual is None or 
                indicadores.atr is None or 
                indicadores.precio_actual == 0):
                return 0.0
            
            if timeframe == Timeframe.SHORT_TERM:
                # Objetivo: 2-5% en 1-3 días
                volatilidad = float(indicadores.atr) / float(indicadores.precio_actual) * 100
                return volatilidad * 0.8
            elif timeframe == Timeframe.MEDIUM_TERM:
                # Objetivo: 5-15% en 1-4 semanas
                volatilidad = float(indicadores.atr) / float(indicadores.precio_actual) * 100
                return volatilidad * 2
            else:  # LONG_TERM
                # Objetivo: 15-50% en 3-12 meses
                volatilidad = float(indicadores.atr) / float(indicadores.precio_actual) * 100
                return volatilidad * 5
        except:
            return 0.0
    
    def screener_por_sector(
        self,
        tickers: List[str],
        timeframe: Timeframe = Timeframe.MEDIUM_TERM,
        limite: int = 10
    ) -> List[ScreenerResult]:
        """
        Ejecuta screener en múltiples símbolos y retorna top N
        
        Args:
            tickers: Lista de símbolos a analizar
            timeframe: Horizonte de inversión
            limite: Cantidad de mejores resultados a retornar
            
        Returns:
            Lista de ScreenerResult ordenada por score descendente
        """
        self.logger.info(f"🔍 Ejecutando screener en {len(tickers)} símbolos...")
        
        resultados = []
        
        for ticker in tickers:
            resultado = self.analizar_simbolo(ticker, timeframe)
            if resultado:
                resultados.append(resultado)
        
        # Ordenar por score descendente
        resultados.sort(key=lambda x: x.score, reverse=True)
        
        return resultados[:limite]
    
    def generar_reporte_texto(self, resultado: ScreenerResult) -> str:
        """Genera reporte textual del análisis"""
        
        lineas = [
            f"📊 ANÁLISIS: {resultado.ticker} | {resultado.timeframe}",
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"💰 Precio: ${resultado.precio_actual:.2f}",
            f"📈 Recomendación: {resultado.recomendacion}",
            f"⭐ Score: {resultado.score:.1f}/100 | Confianza: {resultado.confianza:.1%}",
            f"",
            f"🎯 Señales: {resultado.señales_compra} compra / {resultado.señales_venta} venta",
            f"💡 Razón: {resultado.razon_principal}",
            f"",
            f"📊 Indicadores:",
            f"   • RSI: {resultado.indicadores.get('rsi', 0):.1f}",
            f"   • MACD: {resultado.indicadores.get('macd_signal', 0):.4f}",
            f"   • MA20: ${resultado.indicadores.get('ma_20', 0):.2f}",
            f"   • MA50: ${resultado.indicadores.get('ma_50', 0):.2f}",
            f"   • ATR: ${resultado.indicadores.get('atr', 0):.2f}",
            f"",
            f"🎲 Proyección: {resultado.variacion_esperada:+.2f}% esperado",
            f"",
            f"🔑 Niveles Clave:",
            f"   • Resistencia: ${resultado.niveles_clave.get('resistencia', 0):.2f}",
            f"   • Soporte: ${resultado.niveles_clave.get('soporte', 0):.2f}",
            f"   • Pivot: ${resultado.niveles_clave.get('pivot', 0):.2f}",
        ]
        
        return "\n".join(lineas)
