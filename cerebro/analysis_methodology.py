"""
cerebro/analysis_methodology.py
PILAR FUNDAMENTAL: Análisis unificado basado en:
- Doc 1: Teoría (Metodología Alexander + 3 tipos análisis)
- Doc 3: Implementación técnica (RSI, MACD, Stochastic)
- Doc 2: Formato output (Tabla PLUG)
"""

import logging
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
import pandas as pd
import ta  # Technical Analysis library con todas las fórmulas

from data_sources.market_data import MarketDataManager


class TechnicalAnalyzer:
    """Calcula indicadores técnicos basado en Doc 3 (fórmulas ProRealTime)"""
    
    def __init__(self):
        self.logger = logging.getLogger("TechnicalAnalyzer")
    
    def calcular_rsi(self, precios: pd.Series, periodo: int = 14) -> pd.Series:
        """
        RSI (Relative Strength Index)
        Doc 3: PeriodoRSI = 14
        Niveles: 30 (sobreventa) / 70 (sobrecompra)
        """
        return ta.momentum.rsi(precios, window=periodo)
    
    def calcular_macd(self, precios: pd.Series) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        MACD (Moving Average Convergence Divergence)
        Doc 3: MACDrapido=12, MACDlento=26, Señal=9
        """
        macd = ta.trend.MACD(precios, window_fast=12, window_slow=26, window_sign=9)
        macd_diff = macd.macd()  # Línea MACD
        macd_signal = macd.macd_signal()  # Línea Señal
        macd_histogram = macd.macd_diff()  # Histograma
        return macd_diff, macd_signal, macd_histogram
    
    def calcular_stochastic(self, high: pd.Series, low: pd.Series, close: pd.Series, 
                           periodo: int = 14, suavizado_k: int = 3, suavizado_d: int = 3) -> Tuple[pd.Series, pd.Series]:
        """
        Stochastic Oscillator
        Doc 3: periodo=14, K=3, D=3
        Niveles: 20 (sobreventa) / 80 (sobrecompra)
        """
        stoch = ta.momentum.StochRSIIndicator(close, window=periodo, smooth1=suavizado_k, smooth2=suavizado_d)
        k_line = stoch.stochrsi()  # %K
        d_line = stoch.stochrsi_d()  # %D
        return k_line, d_line
    
    def calcular_sma(self, precios: pd.Series, periodo: int = 20) -> pd.Series:
        """SMA (Simple Moving Average)"""
        return ta.trend.sma_indicator(precios, window=periodo)
    
    def calcular_ema(self, precios: pd.Series, periodo: int = 9) -> pd.Series:
        """EMA (Exponential Moving Average)"""
        return ta.trend.ema_indicator(precios, window=periodo)
    
    def calcular_bollinger_bands(self, precios: pd.Series, periodo: int = 20) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Bollinger Bands (Banda superior, media, inferior)"""
        bb = ta.volatility.BollingerBands(precios, window=periodo)
        return bb.bollinger_hband(), bb.bollinger_mavg(), bb.bollinger_lband()
    
    def calcular_atr(self, high: pd.Series, low: pd.Series, close: pd.Series, periodo: int = 14) -> pd.Series:
        """ATR (Average True Range) - Volatilidad"""
        return ta.volatility.average_true_range(high, low, close, window=periodo)
    
    def calcular_volumen_sma(self, volumen: pd.Series, periodo: int = 20) -> pd.Series:
        """Volumen promedio"""
        return ta.trend.sma_indicator(volumen, window=periodo)
    
    def analizar_indicadores(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Análisis técnico completo con todos los indicadores
        
        Args:
            df: DataFrame con columnas [Open, High, Low, Close, Volume]
        
        Returns:
            Dict con todos los indicadores calculados y señales
        """
        if df.empty or len(df) < 30:
            return {"error": "Datos insuficientes para análisis técnico"}
        
        # Obtener últimas barras (mínimo 30 para todos los cálculos)
        df = df.iloc[-60:]  # Últimos 60 días
        
        resultado = {
            "timestamp": datetime.now().isoformat(),
            "num_barras": len(df),
            "precio_actual": df["Close"].iloc[-1],
            "indicadores": {},
            "señales": {}
        }
        
        try:
            # RSI (14)
            rsi = self.calcular_rsi(df["Close"], periodo=14)
            rsi_actual = rsi.iloc[-1]
            resultado["indicadores"]["RSI"] = {
                "valor": round(rsi_actual, 2),
                "nivel": "SOBRECOMPRA" if rsi_actual > 70 else "SOBREVENTA" if rsi_actual < 30 else "NEUTRAL",
                "señal": "COMPRA" if rsi_actual < 30 else "VENTA" if rsi_actual > 70 else "ESPERA"
            }
            
            # MACD
            macd_diff, macd_signal, macd_hist = self.calcular_macd(df["Close"])
            macd_diff_actual = macd_diff.iloc[-1]
            macd_signal_actual = macd_signal.iloc[-1]
            macd_hist_actual = macd_hist.iloc[-1]
            resultado["indicadores"]["MACD"] = {
                "linea_macd": round(macd_diff_actual, 4),
                "linea_senal": round(macd_signal_actual, 4),
                "histograma": round(macd_hist_actual, 4),
                "señal": "COMPRA" if macd_hist_actual > 0 and macd_diff_actual > macd_signal_actual else "VENTA" if macd_hist_actual < 0 else "ESPERA"
            }
            
            # Stochastic
            k_line, d_line = self.calcular_stochastic(df["High"], df["Low"], df["Close"])
            k_actual = k_line.iloc[-1]
            d_actual = d_line.iloc[-1]
            resultado["indicadores"]["STOCHASTIC"] = {
                "linea_k": round(k_actual, 2),
                "linea_d": round(d_actual, 2),
                "nivel": "SOBRECOMPRA" if k_actual > 80 else "SOBREVENTA" if k_actual < 20 else "NEUTRAL",
                "señal": "COMPRA" if k_actual < 20 else "VENTA" if k_actual > 80 else "ESPERA"
            }
            
            # SMAs
            sma20 = self.calcular_sma(df["Close"], 20).iloc[-1]
            sma50 = self.calcular_sma(df["Close"], 50).iloc[-1]
            sma200 = self.calcular_sma(df["Close"], 200).iloc[-1]
            resultado["indicadores"]["MEDIAS_MOVILES"] = {
                "SMA_20": round(sma20, 2),
                "SMA_50": round(sma50, 2),
                "SMA_200": round(sma200, 2),
                "tendencia_corto": "ALCISTA" if df["Close"].iloc[-1] > sma20 else "BAJISTA",
                "tendencia_medio": "ALCISTA" if df["Close"].iloc[-1] > sma50 else "BAJISTA",
                "tendencia_largo": "ALCISTA" if df["Close"].iloc[-1] > sma200 else "BAJISTA"
            }
            
            # EMA
            ema9 = self.calcular_ema(df["Close"], 9).iloc[-1]
            ema21 = self.calcular_ema(df["Close"], 21).iloc[-1]
            resultado["indicadores"]["EMA"] = {
                "EMA_9": round(ema9, 2),
                "EMA_21": round(ema21, 2),
                "señal": "COMPRA" if ema9 > ema21 else "VENTA" if ema9 < ema21 else "ESPERA"
            }
            
            # Bollinger Bands
            bb_upper, bb_mid, bb_lower = self.calcular_bollinger_bands(df["Close"], 20)
            bb_upper_actual = bb_upper.iloc[-1]
            bb_mid_actual = bb_mid.iloc[-1]
            bb_lower_actual = bb_lower.iloc[-1]
            resultado["indicadores"]["BOLLINGER_BANDS"] = {
                "banda_superior": round(bb_upper_actual, 2),
                "banda_media": round(bb_mid_actual, 2),
                "banda_inferior": round(bb_lower_actual, 2),
                "posicion": "SOBRECOMPRA" if df["Close"].iloc[-1] > bb_upper_actual else "SOBREVENTA" if df["Close"].iloc[-1] < bb_lower_actual else "NEUTRAL"
            }
            
            # ATR (Volatilidad)
            atr = self.calcular_atr(df["High"], df["Low"], df["Close"], 14).iloc[-1]
            resultado["indicadores"]["ATR"] = {
                "valor": round(atr, 2),
                "volatilidad": "ALTA" if atr > df["Close"].std() else "MEDIA" if atr > df["Close"].std() * 0.5 else "BAJA"
            }
            
            # Volumen
            vol_avg = self.calcular_volumen_sma(df["Volume"], 20).iloc[-1]
            vol_actual = df["Volume"].iloc[-1]
            resultado["indicadores"]["VOLUMEN"] = {
                "volumen_actual": int(vol_actual),
                "volumen_promedio": int(vol_avg),
                "relacion": round(vol_actual / vol_avg, 2),
                "señal": "FUERTE" if vol_actual > vol_avg * 1.2 else "DEBIL" if vol_actual < vol_avg * 0.8 else "NORMAL"
            }
            
            return resultado
            
        except Exception as e:
            self.logger.error(f"Error en análisis técnico: {str(e)}")
            return {"error": str(e)}


class AlexanderAnalyzer:
    """
    Lógica de decisión basada en Metodología Alexander (Doc 1-2)
    Evalúa: Marea + Movimiento + Factor Social → Recomendación
    """
    
    def __init__(self):
        self.logger = logging.getLogger("AlexanderAnalyzer")
        self.data_manager = MarketDataManager()
    
    def analizar_marea(self, ticker: str, contexto_macro: Dict) -> Dict[str, Any]:
        """
        Marea = Contexto general del mercado (SPY, VIX, tendencia)
        Doc 1: Analizar si la "marea general" es alcista o bajista
        """
        try:
            from data_sources import DataValidator
            validator = DataValidator()
            
            vix = contexto_macro.get("volatilidad", {}).get("VIX")
            spy_cambio = contexto_macro.get("indices", {}).get("SPY", {}).get("cambio_pct")
            
            # VALIDAR VIX
            is_valid_vix, err_vix = validator.validar_vix(vix)
            if not is_valid_vix:
                self.logger.warning(f"⚠️  {err_vix}, usando valor por defecto 20")
                vix = 20
                vix_validado = False
            else:
                vix_validado = True
            
            # VALIDAR SPY CAMBIO %
            is_valid_spy, err_spy = validator.validar_cambio_pct(spy_cambio, "SPY")
            if not is_valid_spy:
                self.logger.warning(f"⚠️  {err_spy}, usando valor por defecto 0")
                spy_cambio = 0
                spy_validado = False
            else:
                spy_validado = True
            
            resultado = {
                "vix": vix,
                "spy_cambio_pct": spy_cambio,
                "marea_general": "ALCISTA" if vix < 20 and spy_cambio > 0 else "BAJISTA" if vix > 25 and spy_cambio < 0 else "NEUTRAL",
                "volatilidad_mercado": "ALTA" if vix > 25 else "MODERADA" if vix > 15 else "BAJA",
                "riesgo": "ALTO" if vix > 30 else "MODERADO" if vix > 20 else "BAJO"
            }
            
            return resultado
            
        except Exception as e:
            self.logger.error(f"Error analizando marea: {str(e)}")
            return {"error": str(e)}
    
    def analizar_movimiento(self, ticker: str, indicadores_tecnicos: Dict) -> Dict[str, Any]:
        """
        Movimiento = Análisis técnico local del instrumento
        Doc 1: Patrones, soporte/resistencia, divergencias
        """
        try:
            rsi = indicadores_tecnicos.get("indicadores", {}).get("RSI", {})
            macd = indicadores_tecnicos.get("indicadores", {}).get("MACD", {})
            stoch = indicadores_tecnicos.get("indicadores", {}).get("STOCHASTIC", {})
            
            # Contar señales alcistas
            señales_alcistas = 0
            señales_bajistas = 0
            
            if rsi.get("señal") == "COMPRA":
                señales_alcistas += 1
            elif rsi.get("señal") == "VENTA":
                señales_bajistas += 1
            
            if macd.get("señal") == "COMPRA":
                señales_alcistas += 1
            elif macd.get("señal") == "VENTA":
                señales_bajistas += 1
            
            if stoch.get("señal") == "COMPRA":
                señales_alcistas += 1
            elif stoch.get("señal") == "VENTA":
                señales_bajistas += 1
            
            # Determinación del movimiento
            if señales_alcistas >= 2:
                movimiento = "ALCISTA"
                fuerza = "FUERTE" if señales_alcistas == 3 else "MODERADA"
            elif señales_bajistas >= 2:
                movimiento = "BAJISTA"
                fuerza = "FUERTE" if señales_bajistas == 3 else "MODERADA"
            else:
                movimiento = "LATERAL"
                fuerza = "INDECISO"
            
            resultado = {
                "movimiento": movimiento,
                "fuerza": fuerza,
                "señales_alcistas": señales_alcistas,
                "señales_bajistas": señales_bajistas,
                "consenso": round((señales_alcistas + señales_bajistas) / 3 * 100, 1) if (señales_alcistas + señales_bajistas) > 0 else 0,
                "indicadores_analizados": ["RSI(14)", "MACD(12,26,9)", "Stochastic(14,3,3)"]
            }
            
            return resultado
            
        except Exception as e:
            self.logger.error(f"Error analizando movimiento: {str(e)}")
            return {"error": str(e)}
    
    def analizar_factor_social(self, ticker: str, fundamentales: Dict, tendencia: Dict, datos_finviz: Dict = None) -> Dict[str, Any]:
        """
        Factor Social = Sentimiento, datos fundamentales, contexto, insider trading
        Doc 1: Earnings, Insider buying, Fortaleza relativa vs SPY
        + Finviz: Insider transactions, Analyst ratings, Sentiment scores
        """
        try:
            pe_ratio = fundamentales.get("pe_ratio")
            market_cap = fundamentales.get("market_cap", 0)
            debt_to_equity = fundamentales.get("debt_to_equity", 0)
            roe = fundamentales.get("roe", 0)
            
            # Análisis de valuación
            valuacion = "CARA" if pe_ratio and pe_ratio > 25 else "BARATA" if pe_ratio and pe_ratio < 15 else "JUSTA"
            
            # Análisis de tamaño
            if market_cap:
                if market_cap > 200e9:
                    tamaño = "MEGA CAP"
                    riesgo_liquidez = "MUY BAJO"
                elif market_cap > 10e9:
                    tamaño = "LARGE CAP"
                    riesgo_liquidez = "BAJO"
                elif market_cap > 2e9:
                    tamaño = "MID CAP"
                    riesgo_liquidez = "MODERADO"
                else:
                    tamaño = "SMALL CAP"
                    riesgo_liquidez = "ALTO"
            else:
                tamaño = "DESCONOCIDO"
                riesgo_liquidez = "MEDIO"
            
            # Análisis de solidez
            solidez = "FUERTE" if debt_to_equity and debt_to_equity < 1 else "MODERADA" if debt_to_equity and debt_to_equity < 2 else "DÉBIL"
            
            # Enriquecimiento con datos de Finviz
            insider_sentiment = "NEUTRAL"
            analyst_sentiment = "NEUTRAL"
            finviz_disponible = False
            
            if datos_finviz and not datos_finviz.get("error"):
                finviz_disponible = True
                
                # Evalúa insider trading sentiment
                insider_data = datos_finviz.get("insider_trading", {})
                if insider_data:
                    insider_summary = self._evaluar_insider_trading(insider_data)
                    insider_sentiment = insider_summary
                
                # Evalúa analyst ratings
                analyst_data = datos_finviz.get("analyst_ratings", {})
                if analyst_data:
                    analyst_sentiment = self._evaluar_analyst_ratings(analyst_data)
            
            # Sentimiento combinado
            sentimiento_general = "POSITIVO" if valuacion != "CARA" and solidez != "DÉBIL" and insider_sentiment != "BAJISTA" else "NEGATIVO" if valuacion == "CARA" or insider_sentiment == "BAJISTA" else "NEUTRAL"
            
            resultado = {
                "valuacion": valuacion,
                "pe_ratio": pe_ratio,
                "tamaño": tamaño,
                "market_cap": market_cap,
                "solidez": solidez,
                "debt_to_equity": debt_to_equity,
                "roe": roe,
                "riesgo_liquidez": riesgo_liquidez,
                "sentimiento_general": sentimiento_general,
                # Nuevos campos Finviz
                "insider_sentiment": insider_sentiment,
                "analyst_sentiment": analyst_sentiment,
                "finviz_disponible": finviz_disponible
            }
            
            return resultado
            
        except Exception as e:
            self.logger.error(f"Error analizando factor social: {str(e)}")
            return {"error": str(e)}
    
    def _evaluar_insider_trading(self, insider_data: Dict) -> str:
        """Evalúa sentimiento basado en insider trading data"""
        if not insider_data:
            return "NEUTRAL"
        
        # Lógica simplificada: si hay más compras que ventas -> ALCISTA
        compras = sum(1 for v in insider_data.values() if "buy" in str(v).lower() or "compra" in str(v).lower())
        ventas = sum(1 for v in insider_data.values() if "sell" in str(v).lower() or "venta" in str(v).lower())
        
        if compras > ventas:
            return "ALCISTA"
        elif ventas > compras:
            return "BAJISTA"
        return "NEUTRAL"
    
    def _evaluar_analyst_ratings(self, analyst_data: Dict) -> str:
        """Evalúa sentimiento basado en analyst ratings"""
        if not analyst_data:
            return "NEUTRAL"
        
        # Lógica simplificada: si hay targets al alza -> ALCISTA
        targets = [v for v in analyst_data.values() if "target" in str(v).lower()]
        
        if targets:
            return "ALCISTA"
        return "NEUTRAL"
    
    def generar_recomendacion(self, marea: Dict, movimiento: Dict, factor_social: Dict) -> Dict[str, Any]:
        """
        Genera recomendación final basada en las 3 análisis
        Doc 1-2: COMPRA AGRESIVA, COMPRA, ESPERA, VENTA, VENTA AGRESIVA
        """
        try:
            # Scoring
            score = 0
            
            # Marea (40%)
            if marea.get("marea_general") == "ALCISTA":
                score += 40
            elif marea.get("marea_general") == "NEUTRAL":
                score += 20
            
            # Movimiento (40%)
            if movimiento.get("movimiento") == "ALCISTA":
                score += 40
            elif movimiento.get("movimiento") == "NEUTRAL":
                score += 20
            
            # Factor Social (20%)
            if factor_social.get("sentimiento_general") == "POSITIVO":
                score += 20
            elif factor_social.get("sentimiento_general") == "NEUTRAL":
                score += 10
            
            # Determinar recomendación
            if score >= 90:
                recomendacion = "COMPRA AGRESIVA"
                probabilidad = 85
            elif score >= 70:
                recomendacion = "COMPRA"
                probabilidad = 70
            elif score >= 50:
                recomendacion = "ESPERA"
                probabilidad = 55
            elif score >= 30:
                recomendacion = "VENTA"
                probabilidad = 70
            else:
                recomendacion = "VENTA AGRESIVA"
                probabilidad = 85
            
            return {
                "recomendacion": recomendacion,
                "score": score,
                "probabilidad_exito": probabilidad,
                "confianza": "ALTA" if abs(score - 50) > 30 else "MODERADA" if abs(score - 50) > 15 else "BAJA"
            }
            
        except Exception as e:
            self.logger.error(f"Error generando recomendación: {str(e)}")
            return {"error": str(e)}


class AnalysisMethodology:
    """
    PILAR FUNDAMENTAL: Motor de análisis unificado
    Combina: Técnico (Doc 3) + Alexander (Doc 1-2) + Reporte (Doc 2)
    """
    
    def __init__(self):
        self.logger = logging.getLogger("AnalysisMethodology")
        self.data_manager = MarketDataManager()
        self.technical_analyzer = TechnicalAnalyzer()
        self.alexander_analyzer = AlexanderAnalyzer()
    
    def analizar_ticker(self, ticker: str) -> Dict[str, Any]:
        """
        Análisis completo de un ticker
        
        Args:
            ticker: Símbolo del instrumento (AAPL, MSFT, etc)
        
        Returns:
            Dict con análisis técnico + Alexander + recomendación
        """
        
        self.logger.info(f"🔍 Iniciando análisis completo de {ticker}...")
        
        resultado_final = {
            "ticker": ticker,
            "timestamp": datetime.now().isoformat(),
            "status": "procesando"
        }
        
        try:
            # 1️⃣  Obtener datos actuales
            self.logger.info(f"📊 Obteniendo datos actuales...")
            datos_actuales = self.data_manager.obtener_datos_actuales(ticker)
            if "error" in datos_actuales:
                return {**resultado_final, "error": datos_actuales["error"], "status": "error"}
            
            resultado_final["datos_actuales"] = datos_actuales
            
            # 2️⃣  Obtener datos históricos
            self.logger.info(f"📈 Obteniendo datos históricos...")
            df_historico = self.data_manager.obtener_historico(ticker, periodo="1y")
            if df_historico.empty:
                return {**resultado_final, "error": "No hay datos históricos", "status": "error"}
            
            # 3️⃣  Análisis técnico (Doc 3)
            self.logger.info(f"🔧 Calculando indicadores técnicos...")
            indicadores = self.technical_analyzer.analizar_indicadores(df_historico)
            resultado_final["tecnico"] = indicadores
            
            # 4️⃣  Obtener fundamentales
            self.logger.info(f"📋 Obteniendo datos fundamentales...")
            fundamentales = self.data_manager.obtener_fundamentales(ticker)
            resultado_final["fundamentales"] = fundamentales
            
            # 5️⃣  Contexto macro
            self.logger.info(f"🌍 Obteniendo contexto macro...")
            contexto_macro = self.data_manager.obtener_contexto_macro()
            resultado_final["contexto_macro"] = contexto_macro
            
            # 6️⃣  Tendencia
            self.logger.info(f"📉 Calculando tendencia...")
            tendencia = self.data_manager.obtener_tendencia(ticker)
            resultado_final["tendencia"] = tendencia
            
            # 7️⃣  Soportes/Resistencias
            self.logger.info(f"🎯 Calculando soportes y resistencias...")
            sr = self.data_manager.obtener_soportes_resistencias(ticker)
            resultado_final["soportes_resistencias"] = sr
            
            # 7️⃣.5️⃣  Obtener datos de Finviz
            self.logger.info(f"🦊 Obteniendo datos de Finviz...")
            datos_finviz = self.data_manager.obtener_datos_finviz(ticker)
            resultado_final["finviz"] = datos_finviz
            
            # 8️⃣  Análisis Alexander (Doc 1-2)
            self.logger.info(f"🧭 Aplicando metodología Alexander...")
            marea = self.alexander_analyzer.analizar_marea(ticker, contexto_macro)
            movimiento = self.alexander_analyzer.analizar_movimiento(ticker, indicadores)
            factor_social = self.alexander_analyzer.analizar_factor_social(ticker, fundamentales, tendencia, datos_finviz)
            
            resultado_final["alexander"] = {
                "marea": marea,
                "movimiento": movimiento,
                "factor_social": factor_social
            }
            
            # 9️⃣  Generar recomendación final
            self.logger.info(f"✅ Generando recomendación final...")
            recomendacion = self.alexander_analyzer.generar_recomendacion(marea, movimiento, factor_social)
            resultado_final["recomendacion"] = recomendacion
            
            resultado_final["status"] = "completado"
            self.logger.info(f"✅ Análisis completado para {ticker}")
            
            return resultado_final
            
        except Exception as e:
            self.logger.error(f"❌ Error en análisis de {ticker}: {str(e)}")
            resultado_final["error"] = str(e)
            resultado_final["status"] = "error"
            return resultado_final
    
    def get_status(self) -> Dict[str, Any]:
        """Estado del motor de análisis"""
        return {
            "modulo": "AnalysisMethodology",
            "estado": "✅ Operativo",
            "fuentes_datos": self.data_manager.get_status(),
            "indicadores": ["RSI", "MACD", "Stochastic", "SMA", "EMA", "Bollinger Bands", "ATR", "Volumen"],
            "metodologia": "Alexander (Marea + Movimiento + Factor Social)"
        }
