"""
cerebro/enhanced_analysis.py
SISTEMA MEJORADO DE ANÁLISIS PARA PROYECCIONES MÁS PRECISAS
Combina indicadores técnicos, fundamentales y un scoring ponderado
"""

import logging
from typing import Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class AnalysisScore:
    """Estructura de puntuación del análisis"""
    technical_score: float  # 0-100
    fundamental_score: float  # 0-100
    sentiment_score: float  # 0-100
    combined_score: float  # 0-100
    confidence: float  # 0-100
    divergence: str  # "AGREEMENT", "MINOR_DIVERGENCE", "MAJOR_DIVERGENCE"
    recommendation: str  # "STRONG_BUY", "BUY", "HOLD", "SELL", "STRONG_SELL"
    rationale: str  # Explicación clara


class EnhancedAnalyzer:
    """
    Analizador mejorado que combina técnicos + fundamentales
    para proyecciones más precisas
    """
    
    def __init__(self):
        self.logger = logging.getLogger("EnhancedAnalyzer")
    
    def calcular_technical_score(self, indicadores: Dict) -> float:
        """
        Calcula score técnico (0-100) basado en indicadores
        Componentes:
        - RSI: Momentum (0-30 puntos)
        - MACD: Tendencia (0-25 puntos)
        - Bollinger: Volatilidad (0-20 puntos)
        - Moving Averages: Dirección (0-15 puntos)
        - Volumen: Confirmación (0-10 puntos)
        """
        score = 0
        
        try:
            # 1. RSI (0-30 puntos)
            rsi = indicadores.get("rsi", 50)
            if 30 <= rsi <= 70:
                score += 15  # Zona neutral, sin excesos
            elif rsi > 70:
                score += 5   # Sobrecompra, posible reversa bajista
            elif rsi < 30:
                score += 10  # Sobreventa, posible reversa alcista
            else:
                score += 20  # Momentum fuerte
            
            # 2. MACD (0-25 puntos)
            macd_histogram = indicadores.get("macd_histogram", 0)
            macd_signal = indicadores.get("macd_signal", 0)
            if macd_histogram > 0 and macd_signal > 0:
                score += 25  # Momentum alcista fuerte
            elif macd_histogram > 0:
                score += 15  # Inicio de momentum alcista
            elif macd_histogram < 0 and macd_signal < 0:
                score += 0   # Momentum bajista
            elif macd_histogram < 0:
                score += 5   # Inicio de momentum bajista
            else:
                score += 12  # Neutral
            
            # 3. Bollinger Bands (0-20 puntos)
            bb_position = indicadores.get("bollinger_position", "media")
            if bb_position == "bajo":
                score += 18  # Cerca de soporte, posible rebote
            elif bb_position == "alto":
                score += 8   # Cerca de resistencia
            elif bb_position == "media":
                score += 15  # Zona neutra, espacio para movimiento
            
            # 4. Moving Averages (0-15 puntos)
            sma_200 = indicadores.get("sma_200_direction", "neutral")
            ema_signal = indicadores.get("ema_signal", "neutral")
            if sma_200 == "up" and ema_signal == "up":
                score += 15  # Tendencia alcista confirmada
            elif sma_200 == "down" and ema_signal == "down":
                score += 5   # Tendencia bajista
            elif sma_200 == "up" or ema_signal == "up":
                score += 10  # Una señal alcista
            else:
                score += 8
            
            # 5. Volumen (0-10 puntos)
            volumen_confirmation = indicadores.get("volumen_confirmation", "neutral")
            if volumen_confirmation == "alta":
                score += 10
            elif volumen_confirmation == "baja":
                score += 3
            else:
                score += 5
            
        except Exception as e:
            self.logger.error(f"Error calculando technical_score: {e}")
        
        return min(score, 100)
    
    def calcular_fundamental_score(self, fundamentales: Dict) -> float:
        """
        Calcula score fundamental (0-100)
        Componentes:
        - Valuación P/E (0-25 puntos)
        - ROE/Rentabilidad (0-20 puntos)
        - Debt/Solvencia (0-20 puntos)
        - Crecimiento (0-20 puntos)
        - Posición competitiva (0-15 puntos)
        """
        score = 0
        
        try:
            # 1. P/E Ratio (0-25 puntos)
            pe_ratio = fundamentales.get("pe_ratio")
            if pe_ratio is None:
                score += 12  # Sin datos, neutral
            elif pe_ratio < 10:
                score += 25  # Muy barato
            elif pe_ratio < 15:
                score += 20  # Barato
            elif pe_ratio < 25:
                score += 15  # Justo
            elif pe_ratio < 40:
                score += 8   # Caro
            else:
                score += 2   # Muy caro
            
            # 2. ROE / Rentabilidad (0-20 puntos)
            roe = fundamentales.get("roe", 0)
            if roe > 20:
                score += 20  # Muy rentable
            elif roe > 15:
                score += 18  # Rentable
            elif roe > 10:
                score += 12  # Moderadamente rentable
            elif roe > 5:
                score += 8   # Débilmente rentable
            else:
                score += 2   # No rentable
            
            # 3. Deuda/Solvencia (0-20 puntos)
            debt_to_equity = fundamentales.get("debt_to_equity", 0)
            if debt_to_equity < 0.5:
                score += 20  # Bajo nivel de deuda
            elif debt_to_equity < 1:
                score += 15  # Deuda moderada
            elif debt_to_equity < 1.5:
                score += 10  # Deuda elevada
            elif debt_to_equity < 2:
                score += 5   # Deuda muy elevada
            else:
                score += 1   # Altamente apalancado
            
            # 4. Crecimiento de ingresos (0-20 puntos)
            earnings_growth = fundamentales.get("earnings_growth", 0)
            if earnings_growth > 20:
                score += 20  # Crecimiento explosivo
            elif earnings_growth > 10:
                score += 18  # Crecimiento fuerte
            elif earnings_growth > 5:
                score += 12  # Crecimiento moderado
            elif earnings_growth > 0:
                score += 8   # Crecimiento leve
            else:
                score += 2   # Decrecimiento
            
            # 5. Posición competitiva (0-15 puntos)
            market_cap = fundamentales.get("market_cap", 0)
            if market_cap > 1000000000000:  # > $1T
                score += 15  # Mega cap, muy sólida
            elif market_cap > 100000000000:  # > $100B
                score += 13  # Large cap, sólida
            elif market_cap > 10000000000:  # > $10B
                score += 10  # Mid cap
            elif market_cap > 2000000000:   # > $2B
                score += 7   # Small cap
            else:
                score += 3   # Micro cap
            
        except Exception as e:
            self.logger.error(f"Error calculando fundamental_score: {e}")
        
        return min(score, 100)
    
    def calcular_sentiment_score(self, finviz_data: Dict, insider_data: Dict = None) -> float:
        """
        Calcula score de sentimiento (0-100)
        Componentes:
        - Analyst ratings (0-25 puntos)
        - Insider buying/selling (0-20 puntos)
        - Noticias sentiment (0-20 puntos)
        - Technical sentiment (0-20 puntos)
        - Relative strength vs SPY (0-15 puntos)
        """
        score = 0
        
        try:
            # 1. Analyst Rating (0-25 puntos)
            analyst_rating = finviz_data.get("analyst_rating", "")
            if analyst_rating == "Strong Buy":
                score += 25
            elif analyst_rating == "Buy":
                score += 20
            elif analyst_rating == "Hold":
                score += 12
            elif analyst_rating == "Sell":
                score += 5
            elif analyst_rating == "Strong Sell":
                score += 0
            else:
                score += 12  # Default neutral
            
            # 2. Insider Sentiment (0-20 puntos)
            insider_sentiment = finviz_data.get("insider_sentiment", "neutral")
            if insider_sentiment == "very positive":
                score += 20
            elif insider_sentiment == "positive":
                score += 16
            elif insider_sentiment == "neutral":
                score += 10
            elif insider_sentiment == "negative":
                score += 4
            else:
                score += 10
            
            # 3. Noticias Sentiment (0-20 puntos)
            news_sentiment = finviz_data.get("news_sentiment", "neutral")
            if news_sentiment == "very positive":
                score += 20
            elif news_sentiment == "positive":
                score += 15
            elif news_sentiment == "neutral":
                score += 10
            elif news_sentiment == "negative":
                score += 3
            else:
                score += 10
            
            # 4. Technical Sentiment (0-20 puntos)
            tech_sentiment = finviz_data.get("technical_sentiment", "neutral")
            if tech_sentiment == "strong bullish":
                score += 20
            elif tech_sentiment == "bullish":
                score += 16
            elif tech_sentiment == "neutral":
                score += 10
            elif tech_sentiment == "bearish":
                score += 4
            else:
                score += 10
            
            # 5. Relative Strength (0-15 puntos)
            relative_strength = finviz_data.get("relative_strength", 50)
            if relative_strength > 70:
                score += 15  # Muy fuerte vs mercado
            elif relative_strength > 60:
                score += 12
            elif relative_strength > 40:
                score += 10
            elif relative_strength > 30:
                score += 5
            else:
                score += 2   # Débil vs mercado
            
        except Exception as e:
            self.logger.error(f"Error calculando sentiment_score: {e}")
        
        return min(score, 100)
    
    def detectar_divergencias(self, tech_score: float, fundamental_score: float, 
                              sentiment_score: float) -> Tuple[str, str]:
        """
        Detecta si hay divergencias entre análisis
        Retorna: (tipo_divergencia, descripción)
        """
        scores = [tech_score, fundamental_score, sentiment_score]
        max_score = max(scores)
        min_score = min(scores)
        diferencia = max_score - min_score
        
        if diferencia < 15:
            return "AGREEMENT", "Todos los análisis están de acuerdo"
        elif diferencia < 30:
            return "MINOR_DIVERGENCE", "Hay ligeras discrepancias entre análisis"
        else:
            return "MAJOR_DIVERGENCE", "Hay significativas discrepancias entre análisis"
    
    def generar_recomendacion(self, combined_score: float, divergence_type: str) -> str:
        """
        Genera recomendación basada en score y divergencias
        """
        if divergence_type == "MAJOR_DIVERGENCE":
            # Con divergencias mayores, ser más conservador
            if combined_score >= 75:
                return "BUY"
            elif combined_score >= 60:
                return "HOLD"
            elif combined_score >= 40:
                return "HOLD"
            else:
                return "SELL"
        elif divergence_type == "MINOR_DIVERGENCE":
            if combined_score >= 80:
                return "STRONG_BUY"
            elif combined_score >= 65:
                return "BUY"
            elif combined_score >= 45:
                return "HOLD"
            elif combined_score >= 25:
                return "SELL"
            else:
                return "STRONG_SELL"
        else:  # AGREEMENT
            if combined_score >= 85:
                return "STRONG_BUY"
            elif combined_score >= 70:
                return "BUY"
            elif combined_score >= 55:
                return "HOLD"
            elif combined_score >= 35:
                return "SELL"
            else:
                return "STRONG_SELL"
    
    def analizar_completo(self, indicadores: Dict, fundamentales: Dict, 
                         finviz_data: Dict = None) -> AnalysisScore:
        """
        Análisis completo que combina técnicos, fundamentales y sentimiento
        Retorna AnalysisScore con scoring detallado
        """
        
        # Calcular scores individuales
        tech_score = self.calcular_technical_score(indicadores)
        fund_score = self.calcular_fundamental_score(fundamentales)
        sent_score = self.calcular_sentiment_score(finviz_data or {})
        
        # Calcular score combinado (promedio ponderado)
        # Pesos: Tech=40%, Fundamental=35%, Sentiment=25%
        combined = (tech_score * 0.40) + (fund_score * 0.35) + (sent_score * 0.25)
        
        # Detectar divergencias
        divergence_type, divergence_desc = self.detectar_divergencias(tech_score, fund_score, sent_score)
        
        # Generar recomendación
        recommendation = self.generar_recomendacion(combined, divergence_type)
        
        # Calcular confianza basada en acuerdo
        if divergence_type == "AGREEMENT":
            confidence = 85 + (abs(tech_score - fund_score) * -0.1)
        elif divergence_type == "MINOR_DIVERGENCE":
            confidence = 70 + (abs(tech_score - fund_score) * -0.05)
        else:
            confidence = 55 + (abs(tech_score - fund_score) * -0.05)
        
        confidence = max(min(confidence, 100), 20)  # Entre 20-100
        
        # Generar rationale
        rationale = self._generar_rationale(tech_score, fund_score, sent_score, 
                                           divergence_desc, recommendation)
        
        return AnalysisScore(
            technical_score=round(tech_score, 1),
            fundamental_score=round(fund_score, 1),
            sentiment_score=round(sent_score, 1),
            combined_score=round(combined, 1),
            confidence=round(confidence, 1),
            divergence=divergence_type,
            recommendation=recommendation,
            rationale=rationale
        )
    
    def _generar_rationale(self, tech: float, fund: float, sent: float, 
                          divergence: str, recommendation: str) -> str:
        """Genera explicación textual del análisis"""
        
        parts = []
        
        # Análisis técnico
        if tech >= 75:
            parts.append("Los indicadores técnicos muestran fuerte momentum positivo")
        elif tech >= 55:
            parts.append("Los indicadores técnicos apoyan una tendencia alcista moderada")
        elif tech >= 45:
            parts.append("Los indicadores técnicos muestran consolidación")
        else:
            parts.append("Los indicadores técnicos señalan debilidad")
        
        # Análisis fundamental
        if fund >= 75:
            parts.append("Los fundamentales son sólidos con métricas saludables")
        elif fund >= 55:
            parts.append("Los fundamentales son razonables pero no excepcionales")
        else:
            parts.append("Los fundamentales muestran preocupaciones")
        
        # Sentimiento
        if sent >= 75:
            parts.append("El sentimiento del mercado y analistas es muy positivo")
        elif sent >= 55:
            parts.append("El sentimiento es moderadamente positivo")
        else:
            parts.append("El sentimiento es cauteloso o negativo")
        
        # Divergencias
        if "MAJOR" in divergence:
            parts.append("Existe divergencia significativa - proceder con cautela")
        elif "MINOR" in divergence:
            parts.append("Hay ligeras discrepancias entre análisis")
        else:
            parts.append("Todos los análisis concuerdan")
        
        return ". ".join(parts) + f". Recomendación: {recommendation}"
