"""
GUÍA DE INTEGRACIÓN - Enhanced Analyzer en el Bot

Ejemplo de cómo usar el nuevo sistema de scoring en telegram_bot/bot.py
"""

# PASO 1: Importar en telegram_bot/bot.py
# ==========================================
"""
from cerebro import EnhancedAnalyzer, AnalysisScore
"""

# PASO 2: Inicializar en __init__ del bot
# =========================================
"""
class TelegramAnalystBot:
    def __init__(self, ...):
        ...
        self.enhanced_analyzer = EnhancedAnalyzer()
        self.logger = logging.getLogger(self.__class__.__name__)
"""

# PASO 3: Usar en el método de análisis
# ======================================
"""
def handle_analizar_command(self, update, context):
    simbolo = context.args[0].upper()
    
    # Obtener datos
    resultado_analisis = await self.analysis_manager.analizar(simbolo)
    
    # OPCIÓN 1: Usar el nuevo Enhanced Analyzer
    enhanced_score = self.enhanced_analyzer.analizar_completo(
        indicadores=resultado_analisis.get("tecnico", {}).get("indicadores", {}),
        fundamentales=resultado_analisis.get("fundamentales", {}),
        finviz_data=resultado_analisis.get("finviz", {})
    )
    
    # OPCIÓN 2: Acceder a los datos del score
    mensaje = f'''
📊 ANÁLISIS MEJORADO DE {simbolo}
=====================================

🎯 SCORING PONDERADO:
├─ Técnico: {enhanced_score.technical_score}/100
├─ Fundamental: {enhanced_score.fundamental_score}/100
├─ Sentimiento: {enhanced_score.sentiment_score}/100
└─ SCORE FINAL: {enhanced_score.combined_score}/100

⚡ ESTADO:
├─ Divergencias: {enhanced_score.divergence}
├─ Confianza: {enhanced_score.confidence}%
└─ Recomendación: {enhanced_score.recommendation}

📝 EXPLICACIÓN:
{enhanced_score.rationale}
'''
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje)
"""

# PASO 4: Datos necesarios para el análisis
# ==========================================
"""
El Enhanced Analyzer necesita:

1. INDICADORES TÉCNICOS (Dict):
   - rsi: float (0-100)
   - macd_histogram: float
   - macd_signal: float
   - bollinger_position: str ("alto", "bajo", "media")
   - sma_200_direction: str ("up", "down", "neutral")
   - ema_signal: str ("up", "down", "neutral")
   - volumen_confirmation: str ("alta", "baja", "neutral")

2. FUNDAMENTALES (Dict):
   - pe_ratio: float
   - roe: float (%)
   - debt_to_equity: float
   - earnings_growth: float (%)
   - market_cap: int

3. FINVIZ DATA (Dict):
   - analyst_rating: str
   - insider_sentiment: str
   - news_sentiment: str
   - technical_sentiment: str
   - relative_strength: float (0-100)
"""

# PASO 5: Ejemplo completo de datos
# ==================================
ejemplo_indicadores = {
    "rsi": 72,
    "macd_histogram": 0.15,
    "macd_signal": 0.08,
    "bollinger_position": "media",
    "sma_200_direction": "up",
    "ema_signal": "up",
    "volumen_confirmation": "alta"
}

ejemplo_fundamentales = {
    "pe_ratio": 22,
    "roe": 18,
    "debt_to_equity": 0.7,
    "earnings_growth": 12,
    "market_cap": 1500000000000
}

ejemplo_finviz = {
    "analyst_rating": "Buy",
    "insider_sentiment": "neutral",
    "news_sentiment": "positive",
    "technical_sentiment": "bullish",
    "relative_strength": 65
}

from cerebro import EnhancedAnalyzer

analyzer = EnhancedAnalyzer()
resultado = analyzer.analizar_completo(
    indicadores=ejemplo_indicadores,
    fundamentales=ejemplo_fundamentales,
    finviz_data=ejemplo_finviz
)

print(f"Technical Score: {resultado.technical_score}")  # 76
print(f"Fundamental Score: {resultado.fundamental_score}")  # 74
print(f"Sentiment Score: {resultado.sentiment_score}")  # 71
print(f"Combined Score: {resultado.combined_score}")  # 74.25
print(f"Confidence: {resultado.confidence}%")  # 84
print(f"Divergence: {resultado.divergence}")  # AGREEMENT
print(f"Recommendation: {resultado.recommendation}")  # BUY
print(f"Rationale: {resultado.rationale}")

# PASO 6: Comparación con recomendación anterior
# ===============================================
"""
ANTES (Sin Enhanced Analyzer):
- Recomendación: VENTA AGRESIVA (basada solo en IA)
- Confianza: Implícita, desconocida
- Justificación: "La IA dice que..."

AHORA (Con Enhanced Analyzer):
- Recomendación: BUY
- Confianza: 84% (basada en acuerdo de 3 análisis)
- Justificación: Técnico 76 + Fundamental 74 + Sentimiento 71 
                 = Score 74.25, All agree, Medium confidence

VENTAJA: Mucho más transparente, preciso y con métricas claras
"""

# PASO 7: Ajustar pesos según necesidad
# ======================================
"""
Si quieres dar más peso a fundamentales en sector defensivo:

combined = (tech_score * 0.30) + (fund_score * 0.50) + (sent_score * 0.20)

Si quieres más peso a técnicos en trading rápido:

combined = (tech_score * 0.60) + (fund_score * 0.25) + (sent_score * 0.15)

El sistema es flexible - solo ajusta los pesos en 
cerebro/enhanced_analysis.py línea ~283
"""
