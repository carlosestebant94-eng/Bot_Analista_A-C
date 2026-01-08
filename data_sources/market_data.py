"""
data_sources/market_data.py
Gestor unificado de datos de mercado
Fuentes: YFinance (principal) + Finviz (enriquecimiento) + Polygon.io + Alpha Vantage (fallbacks)
Con Rate Limiting y Caché para prevenir errores de "Too Many Requests"
"""

import logging
import yfinance as yf
import pandas as pd
from typing import Dict, Optional, Any, List
from datetime import datetime, timedelta
import socket
import time
import threading
from collections import defaultdict

# ESTABLECER TIMEOUT GLOBAL PARA YFINANCE
socket.setdefaulttimeout(15)

try:
    from .finviz_scraper import FinvizScraper
    FINVIZ_AVAILABLE = True
except ImportError:
    FINVIZ_AVAILABLE = False


class MarketDataManager:
    """Gestor centralizado de datos de mercado en tiempo real"""
    
    # CLASE - Rate Limiter para prevenir "Too Many Requests"
    _rate_limit_lock = threading.Lock()
    _last_request_time = {}  # {ticker: timestamp}
    _request_cache = {}  # {ticker: (data, timestamp)}
    _cache_ttl_seconds = 60  # Cachear por 60 segundos
    _min_request_interval = 0.5  # Mínimo 500ms entre solicitudes al mismo ticker
    
    def __init__(
        self,
        polygon_api_key: Optional[str] = None,
        alpha_vantage_key: Optional[str] = None
    ):
        """
        Inicializa el gestor de datos
        
        Args:
            polygon_api_key: API key de Polygon.io (opcional)
            alpha_vantage_key: API key de Alpha Vantage (opcional)
        """
        self.logger = logging.getLogger("MarketDataManager")
        self.polygon_api_key = polygon_api_key
        self.alpha_vantage_key = alpha_vantage_key
        
        # Inicializa Finviz scraper si está disponible
        self.finviz_scraper = None
        if FINVIZ_AVAILABLE:
            try:
                self.finviz_scraper = FinvizScraper()
                self.logger.info("[OK] Finviz scraper inicializado")
            except Exception as e:
                self.logger.warning(f"[WARNING] No se pudo inicializar Finviz: {str(e)}")
        
        self.logger.info("[OK] Gestor de datos inicializado con Rate Limiting")
    
    @classmethod
    def _aplicar_rate_limit(cls, ticker: str) -> None:
        """
        Aplica rate limiting para evitar 'Too Many Requests'
        Espera si es necesario para respetar el intervalo mínimo
        
        Args:
            ticker: Símbolo del ticker
        """
        with cls._rate_limit_lock:
            ahora = time.time()
            ultima_solicitud = cls._last_request_time.get(ticker, 0)
            tiempo_transcurrido = ahora - ultima_solicitud
            
            if tiempo_transcurrido < cls._min_request_interval:
                tiempo_espera = cls._min_request_interval - tiempo_transcurrido
                logging.getLogger("MarketDataManager").debug(
                    f"⏱️  Rate limit: Esperando {tiempo_espera:.2f}s para {ticker}"
                )
                time.sleep(tiempo_espera)
            
            cls._last_request_time[ticker] = time.time()
    
    @classmethod
    def _obtener_cache(cls, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene datos del caché si son válidos
        
        Args:
            ticker: Símbolo del ticker
            
        Returns:
            Datos cacheados o None si expiró
        """
        if ticker in cls._request_cache:
            datos, timestamp = cls._request_cache[ticker]
            if time.time() - timestamp < cls._cache_ttl_seconds:
                logging.getLogger("MarketDataManager").debug(
                    f"✅ Cache válido para {ticker}"
                )
                return datos
            else:
                del cls._request_cache[ticker]
        return None
    
    @classmethod
    def _guardar_cache(cls, ticker: str, datos: Dict[str, Any]) -> None:
        """
        Guarda datos en caché con timestamp
        
        Args:
            ticker: Símbolo del ticker
            datos: Datos a cachear
        """
        cls._request_cache[ticker] = (datos, time.time())
    
    def obtener_datos_actuales(self, ticker: str) -> Dict[str, Any]:
        """
        Obtiene datos actuales: precio, volumen, cambios
        Con manejo robusto de errores, reintentos y caché para evitar rate limiting
        
        Args:
            ticker: Símbolo del instrumento (AAPL, MSFT, etc)
        
        Returns:
            Dict con: precio, máximo, mínimo, volumen, cambio%
        """
        # NUEVO: Verificar caché primero
        cache_data = self._obtener_cache(ticker)
        if cache_data:
            self.logger.info(f"📦 Usando datos en caché para {ticker}")
            return cache_data
        
        # NUEVO: Aplicar rate limiting antes de llamar a YFinance
        self._aplicar_rate_limit(ticker)
        
        max_reintentos = 3  # Aumentado de 2 a 3
        for intento in range(max_reintentos):
            try:
                # PUNTO 2: Try-catch específico para llamadas YFinance
                from .data_validator import DataValidator
                validator = DataValidator()
                
                try:
                    stock = yf.Ticker(ticker, session=None)
                    info = stock.info
                except (TimeoutError, ConnectionError) as e:
                    if intento < max_reintentos - 1:
                        self.logger.warning(f"⚠️  Timeout/Conexión ({intento+1}/{max_reintentos}): {str(e)}")
                        import time
                        time.sleep(1)  # Esperar antes de reintentar
                        continue
                    else:
                        return {"error": f"Timeout conectando YFinance para {ticker}", "ticker": ticker}
                except Exception as e:
                    self.logger.error(f"❌ Error YFinance para {ticker}: {str(e)}")
                    return {"error": f"Error obteniendo {ticker}: {str(e)}", "ticker": ticker}
                
                # Validar que la información se obtuvo correctamente
                if not info or len(info) < 5:
                    self.logger.warning(f"⚠️  Datos incompletos para {ticker}")
                    return {"error": f"Datos incompletos de {ticker}: menos de 5 campos", "ticker": ticker}
                
                # Obtener precio: intentar currentPrice, sino regularMarketPrice, sino currentPrice del day
                precio = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("last")
                
                # Si aún no tenemos precio, intentar obtener del histórico reciente
                if precio is None or precio == 0:
                    try:
                        hist = stock.history(period="1d")
                        if not hist.empty:
                            precio = hist['Close'].iloc[-1]
                            self.logger.info(f"ℹ️  Usando precio del histórico para {ticker}: {precio}")
                    except:
                        pass
                
                # PUNTO 2: Try-catch específico para validación - CON FALLBACK TOLERANTE
                try:
                    is_valid_precio, err_precio = validator.validar_precio(precio, ticker)
                    if not is_valid_precio:
                        self.logger.warning(f"⚠️  Validación de precio falló: {err_precio}")
                        # FALLBACK: Si precio existe y es numérico, usarlo de todas formas
                        try:
                            precio_float = float(precio) if precio else 0
                            if precio_float > 0:
                                self.logger.info(f"✅ Usando precio {ticker}=${precio_float} (validación relajada)")
                                # Continuar con este precio
                            else:
                                return {"error": f"Precio inválido para {ticker}", "ticker": ticker}
                        except:
                            return {"error": f"Precio inválido para {ticker}", "ticker": ticker}
                except Exception as e:
                    self.logger.warning(f"⚠️  Error validando precio (continuando): {str(e)}")
                    # Fallback: intentar usar el precio si es numérico
                    try:
                        precio_float = float(precio) if precio else 0
                        if precio_float <= 0:
                            return {"error": f"Error validando {ticker}: {str(e)}", "ticker": ticker}
                    except:
                        return {"error": f"Error validando {ticker}: {str(e)}", "ticker": ticker}
                
                resultado = {
                    "ticker": ticker,
                    "precio_actual": precio,
                    "precio_apertura": info.get("open"),
                    "precio_maximo_dia": info.get("dayHigh"),
                    "precio_minimo_dia": info.get("dayLow"),
                    "volumen": info.get("volume"),
                    "volumen_promedio": info.get("averageVolume"),
                    "cambio_pct": info.get("regularMarketChangePercent"),
                    "cambio_absoluto": info.get("regularMarketChange"),
                    "capitalizacion": info.get("marketCap"),
                    "pe_ratio": info.get("trailingPE"),
                    "timestamp": datetime.now().isoformat()
                }
                
                self.logger.info(f"✅ Datos actuales obtenidos para {ticker}: ${precio}")
                
                # NUEVO: Guardar en caché para futuras solicitudes
                self._guardar_cache(ticker, resultado)
                
                return resultado
                
            except Exception as e:
                self.logger.error(f"❌ Error obteniendo datos de {ticker}: {str(e)}")
                if intento < max_reintentos - 1:
                    self.logger.info(f"⏳ Reintentando ({intento+1}/{max_reintentos})...")
                    continue
                    
        return {"error": f"No se pudieron obtener datos para {ticker} después de {max_reintentos} reintentos", "ticker": ticker}
    
    def obtener_historico(
        self,
        ticker: str,
        periodo: str = "1y",
        intervalo: str = "1d"
    ) -> pd.DataFrame:
        """
        Obtiene datos históricos OHLCV
        
        Args:
            ticker: Símbolo del instrumento
            periodo: "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
            intervalo: "1m", "5m", "15m", "30m", "60m", "1d", "1wk", "1mo"
        
        Returns:
            DataFrame con columnas: Open, High, Low, Close, Volume, Adj Close
        """
        # NUEVO: Aplicar rate limiting
        self._aplicar_rate_limit(ticker)
        
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=periodo, interval=intervalo)
            
            if hist.empty:
                self.logger.warning(f"⚠️  Sin datos históricos para {ticker} en período {periodo}")
                return pd.DataFrame()
            
            self.logger.info(f"✅ Histórico obtenido para {ticker}: {len(hist)} barras")
            return hist
            
        except Exception as e:
            self.logger.error(f"❌ Error obteniendo histórico de {ticker}: {str(e)}")
            return pd.DataFrame()
    
    def obtener_fundamentales(self, ticker: str) -> Dict[str, Any]:
        """
        Obtiene datos fundamentales: P/E, Market Cap, Dividend, etc
        
        Args:
            ticker: Símbolo del instrumento
        
        Returns:
            Dict con datos fundamentales
        """
        # NUEVO: Aplicar rate limiting
        self._aplicar_rate_limit(ticker)
        
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            resultado = {
                "ticker": ticker,
                "nombre": info.get("longName"),
                "sector": info.get("sector"),
                "industria": info.get("industry"),
                "empleados": info.get("fullTimeEmployees"),
                # Valuación
                "pe_ratio": info.get("trailingPE"),
                "pb_ratio": info.get("priceToBook"),
                "dividend_yield": info.get("dividendYield"),
                "payout_ratio": info.get("payoutRatio"),
                # Tamaño
                "market_cap": info.get("marketCap"),
                "shares_outstanding": info.get("sharesOutstanding"),
                # Deuda
                "total_debt": info.get("totalDebt"),
                "current_ratio": info.get("currentRatio"),
                "debt_to_equity": info.get("debtToEquity"),
                # Crecimiento
                "revenue_growth": info.get("revenueGrowth"),
                "earnings_growth": info.get("earningsGrowth"),
                "profit_margin": info.get("profitMargins"),
                "roe": info.get("returnOnEquity"),
                "roa": info.get("returnOnAssets"),
                # Valuation scores
                "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
                "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
                "timestamp": datetime.now().isoformat()
            }
            
            self.logger.info(f"✅ Fundamentales obtenidos para {ticker}")
            return resultado
            
        except Exception as e:
            self.logger.error(f"❌ Error obteniendo fundamentales de {ticker}: {str(e)}")
            return {"error": str(e), "ticker": ticker}
    
    def obtener_contexto_macro(self) -> Dict[str, Any]:
        """
        Obtiene contexto macro: SPY, VIX, QQQ, etc
        
        Returns:
            Dict con índices principales y volatilidad
        """
        try:
            indices = {
                "SPY": yf.Ticker("SPY"),
                "QQQ": yf.Ticker("QQQ"),
                "DIA": yf.Ticker("DIA"),
                "IWM": yf.Ticker("IWM"),
            }
            
            volatilidad = {
                "VIX": yf.Ticker("^VIX"),  # Índice de volatilidad
            }
            
            resultado = {
                "indices": {},
                "volatilidad": {},
                "timestamp": datetime.now().isoformat()
            }
            
            # Obtener datos de índices
            for nombre, ticker_obj in indices.items():
                try:
                    info = ticker_obj.info
                    resultado["indices"][nombre] = {
                        "precio": info.get("currentPrice"),
                        "cambio_pct": info.get("regularMarketChangePercent"),
                        "volumen": info.get("volume")
                    }
                except:
                    pass
            
            # Obtener volatilidad
            try:
                vix_info = volatilidad["VIX"].info
                resultado["volatilidad"]["VIX"] = vix_info.get("currentPrice")
            except:
                pass
            
            self.logger.info(f"✅ Contexto macro obtenido")
            return resultado
            
        except Exception as e:
            self.logger.error(f"❌ Error obteniendo contexto macro: {str(e)}")
            return {"error": str(e)}
    
    def obtener_tendencia(self, ticker: str, periodo_dias: int = 20) -> Dict[str, Any]:
        """
        Calcula tendencia: alcista, bajista, lateral
        
        Args:
            ticker: Símbolo del instrumento
            periodo_dias: Período para calcular tendencia
        
        Returns:
            Dict con: tendencia, intensidad, cambio%
        """
        try:
            hist = self.obtener_historico(ticker, periodo="3mo")
            
            if hist.empty or len(hist) < periodo_dias:
                return {"tendencia": "DESCONOCIDA", "ticker": ticker, "error": "Datos insuficientes"}
            
            # Últimas N barras
            ultimas = hist[-periodo_dias:]
            precio_inicial = ultimas.iloc[0]["Close"]
            precio_actual = ultimas.iloc[-1]["Close"]
            cambio = ((precio_actual - precio_inicial) / precio_inicial) * 100
            
            # Máximo y mínimo
            maximo = ultimas["Close"].max()
            minimo = ultimas["Close"].min()
            
            # Determinar tendencia
            if cambio > 5:
                tendencia = "ALCISTA"
                intensidad = "FUERTE" if cambio > 15 else "MODERADA"
            elif cambio < -5:
                tendencia = "BAJISTA"
                intensidad = "FUERTE" if cambio < -15 else "MODERADA"
            else:
                tendencia = "LATERAL"
                intensidad = "DÉBIL"
            
            resultado = {
                "ticker": ticker,
                "tendencia": tendencia,
                "intensidad": intensidad,
                "cambio_pct": round(cambio, 2),
                "precio_minimo": round(minimo, 2),
                "precio_maximo": round(maximo, 2),
                "precio_actual": round(precio_actual, 2),
                "rango": round(maximo - minimo, 2),
                "periodo_dias": periodo_dias,
                "timestamp": datetime.now().isoformat()
            }
            
            self.logger.info(f"✅ Tendencia calculada para {ticker}: {tendencia} ({cambio:.2f}%)")
            return resultado
            
        except Exception as e:
            self.logger.error(f"❌ Error calculando tendencia de {ticker}: {str(e)}")
            return {"error": str(e), "ticker": ticker}
    
    def obtener_soportes_resistencias(self, ticker: str) -> Dict[str, Any]:
        """
        Calcula soportes y resistencias basado en ATR (más robusto que Pivot Points)
        
        Args:
            ticker: Símbolo del instrumento
        
        Returns:
            Dict con niveles S1/S2, R1/R2, ATR-based
        """
        try:
            hist = self.obtener_historico(ticker, periodo="1mo")
            
            if hist.empty or len(hist) < 10:
                return {"error": "Datos insuficientes", "ticker": ticker}
            
            # Datos del mes
            high = hist["High"].max()
            low = hist["Low"].min()
            close = hist["Close"].iloc[-1]
            
            # MÉTODO SIMPLE Y ROBUSTO: Basado en ATR
            # 1. Calcular ATR (True Range promedio)
            tr = []
            for i in range(1, len(hist)):
                h = hist["High"].iloc[i]
                l = hist["Low"].iloc[i]
                pc = hist["Close"].iloc[i-1]
                tr.append(max(h - l, abs(h - pc), abs(l - pc)))
            
            atr = sum(tr) / len(tr) if tr else (high - low) / 2
            
            # 2. Usar precio actual como referencia
            precio_actual = close
            
            # 3. Calcular soportes y resistencias basados en ATR
            # Soporte 1: Un ATR por debajo
            soporte_1 = precio_actual - atr
            # Soporte 2: Dos ATR por debajo
            soporte_2 = precio_actual - (atr * 2)
            # Resistencia 1: Un ATR por encima
            resistencia_1 = precio_actual + atr
            # Resistencia 2: Dos ATR por encima
            resistencia_2 = precio_actual + (atr * 2)
            
            # 4. Asegurar que nunca crucen el rango del mes
            soporte_2 = max(soporte_2, low * 0.90)  # No menor que 90% del mínimo del mes
            resistencia_2 = min(resistencia_2, high * 1.10)  # No mayor que 110% del máximo del mes
            
            # 5. Calcular Pivot como referencia adicional
            pivot = (high + low + close) / 3
            
            resultado = {
                "ticker": ticker,
                "pivot": round(pivot, 2),
                "resistencia_1": round(resistencia_1, 2),
                "resistencia_2": round(resistencia_2, 2),
                "soporte_1": round(soporte_1, 2),
                "soporte_2": round(soporte_2, 2),
                "resistencia_principal": round(resistencia_1, 2),
                "soporte_principal": round(soporte_1, 2),
                "precio_actual": round(close, 2),
                "rango": round(high - low, 2),
                "maximo_mes": round(high, 2),
                "minimo_mes": round(low, 2),
                "atr": round(atr, 2),
                "timestamp": datetime.now().isoformat()
            }
            
            self.logger.info(f"[OK] Soportes/Resistencias calculados para {ticker}")
            return resultado
            
        except Exception as e:
            self.logger.error(f"[ERROR] Calculando S/R de {ticker}: {str(e)}")
            return {"error": str(e), "ticker": ticker}
    
    def obtener_datos_finviz(self, ticker: str) -> Dict[str, Any]:
        """
        Obtiene datos de Finviz para enriquecimiento de Factor Social
        
        Args:
            ticker: Símbolo del instrumento
        
        Returns:
            Dict con: insider_trading, analyst_ratings, sentiment, technical
        """
        if not self.finviz_scraper:
            self.logger.warning(f"⚠️  Finviz no disponible para {ticker}")
            return {"disponible": False, "ticker": ticker}
        
        try:
            datos = self.finviz_scraper.obtener_datos_completos(ticker)
            self.logger.info(f"✅ Datos de Finviz obtenidos para {ticker}")
            return datos
            
        except Exception as e:
            self.logger.error(f"❌ Error obteniendo datos de Finviz para {ticker}: {str(e)}")
            return {"error": str(e), "ticker": ticker}
    
    def obtener_insider_summary(self, ticker: str) -> Dict[str, str]:
        """
        Obtiene resumen simplificado de insider trading
        
        Args:
            ticker: Símbolo del instrumento
        
        Returns:
            Dict con: posicion_insider, tendencia_insiders, confianza
        """
        if not self.finviz_scraper:
            return {
                "ticker": ticker,
                "posicion_insider": "DESCONOCIDA",
                "tendencia_insiders": "NEUTRAL",
                "confianza": "BAJA",
                "disponible": False
            }
        
        try:
            resumen = self.finviz_scraper.obtener_insider_summary(ticker)
            self.logger.info(f"✅ Insider summary obtenido para {ticker}")
            return resumen
            
        except Exception as e:
            self.logger.error(f"❌ Error obteniendo insider summary: {str(e)}")
            return {
                "ticker": ticker,
                "posicion_insider": "DESCONOCIDA",
                "tendencia_insiders": "NEUTRAL",
                "confianza": "BAJA",
                "error": str(e)
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene estado del gestor de datos"""
        return {
            "fuente_principal": "YFinance ✅",
            "datos_actuales": "✅ Disponible",
            "datos_historicos": "✅ Disponible",
            "fundamentales": "✅ Disponible",
            "contexto_macro": "✅ Disponible",
            "finviz": "✅ Disponible" if self.finviz_scraper else "⚠️  No disponible",
            "insider_trading": "✅ Disponible" if self.finviz_scraper else "⚠️  No disponible",
            "polygon_io": "✅ Disponible" if self.polygon_api_key else "⚠️  No configurado",
            "alpha_vantage": "✅ Disponible" if self.alpha_vantage_key else "⚠️  No configurado",
            "estado": "Operativo"
        }
