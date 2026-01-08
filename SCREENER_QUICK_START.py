#!/usr/bin/env python
"""
SCREENER AUTOMÁTICO - GUÍA RÁPIDA DE USO
Bot Analista A&C - Análisis multidimensional de símbolos financieros
"""

print("""
═══════════════════════════════════════════════════════════════════════════════
                    SCREENER AUTOMÁTICO - GUÍA RÁPIDA
═══════════════════════════════════════════════════════════════════════════════

✅ IMPLEMENTADO: Módulo completo de screener con 3 horizontes de inversión

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 COMANDOS DISPONIBLES EN TELEGRAM:

1. CORTO PLAZO (1-3 días - Momentum):
   /screener corto
   /screener corto AAPL MSFT NVDA
   /screener corto AAPL
   
   ⏰ Tiempo de análisis: ~2-3 segundos por símbolo
   🎯 Focus: RSI, MACD, Momentum reciente

2. MEDIANO PLAZO (1-4 semanas - Tendencia):
   /screener medio
   /screener medio GOOGL AMZN TSLA
   /screener medio SPY QQQ
   
   ⏰ Tiempo de análisis: ~2-3 segundos por símbolo
   🎯 Focus: Medias móviles, Bandas Bollinger, MACD

3. LARGO PLAZO (3-12 meses - Fundamentals):
   /screener largo
   /screener largo BTC EURUSD
   /screener largo SPY BRK.B
   
   ⏰ Tiempo de análisis: ~2-3 segundos por símbolo
   🎯 Focus: Tendencia de largo plazo, MA50

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 ESTRUCTURA DE LA RESPUESTA:

Para cada símbolo analizado recibirás:

  1. 🔴/🟢 TICKER
     💰 Precio actual
     📈 Recomendación (FUERTE COMPRA / COMPRA / MANTENER / VENTA / FUERTE VENTA)
     ⭐ Score: X.X/100 (Confianza: Y%)
     📊 Señales: N↑ compra / M↓ venta
     💡 Razón principal
     🎯 Variación esperada: +/- Z%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 EJEMPLOS DE USO:

Ejemplo 1 - Analizar 3 acciones en mediano plazo:
  /screener medio AAPL MSFT GOOGL
  → Bot analizará AAPL, MSFT, GOOGL
  → Retornará los 3 ordenados por score
  → Tiempo total: ~10-15 segundos

Ejemplo 2 - Corto plazo con símbolos por defecto:
  /screener corto
  → Bot analizará: AAPL, MSFT, NVDA, GOOGL, AMZN
  → Retornará los 5 ordenados por score
  → Ideal para day trading

Ejemplo 3 - Largo plazo con forex y cripto:
  /screener largo EURUSD GBPUSD BTC ETH
  → Bot analizará 4 pares/símbolos
  → Retornará los mejores para inversión a largo
  → Tiempo total: ~10-15 segundos

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 INDICADORES TÉCNICOS CALCULADOS:

Para cada análisis se calcula:

  ✓ RSI (Relative Strength Index)
    • 0-30: Sobrevendido = Oportunidad de compra
    • 30-70: Neutral
    • 70-100: Sobrecomprado = Presión de venta

  ✓ MACD (Moving Average Convergence Divergence)
    • Positivo: Momentum alcista
    • Negativo: Momentum bajista

  ✓ Medias Móviles (MA-20, MA-50)
    • Precio > MA20 > MA50 = Tendencia alcista
    • Precio < MA20 < MA50 = Tendencia bajista

  ✓ Bandas de Bollinger (±2 desviaciones estándar)
    • Precio toca banda inferior = Oportunidad rebote
    • Precio toca banda superior = Presión correctiva

  ✓ ATR (Average True Range)
    • Mide volatilidad
    • Sirve para calcular objetivo de precio

  ✓ Volumen SMA
    • Valida intensidad de los movimientos

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌟 INTERPRETACIÓN DE RECOMENDACIONES:

FUERTE COMPRA (🟢)
  • Score: 75-100
  • Múltiples señales coinciden en compra
  • Alto potencial alcista
  • Confianza: >75%

COMPRA (🟢)
  • Score: 60-75
  • Mayormente señales de compra
  • Potencial alcista moderado
  • Confianza: 60-75%

MANTENER (🟡)
  • Score: 40-60
  • Señales mixtas
  • Sin dirección clara
  • Esperar mejor entrada

VENTA (🔴)
  • Score: 25-40
  • Mayormente señales de venta
  • Presión bajista moderada
  • Confianza: 25-40%

FUERTE VENTA (🔴)
  • Score: 0-25
  • Múltiples señales de venta
  • Alto potencial bajista
  • Confianza: <25%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 ESTRATEGIA RECOMENDADA:

CORTO PLAZO (1-3 días):
  → Buscar FUERTE COMPRA en RSI < 30
  → Take profit en +2% a +5%
  → Stop loss -1%

MEDIANO PLAZO (1-4 semanas):
  → Esperar confirmación de tendencia (2+ señales)
  → Objetivo: +5% a +15%
  → Stop loss: -3% a -5%

LARGO PLAZO (3-12 meses):
  → DCA (Dollar Cost Averaging)
  → Objetivo: +15% a +50%
  → Stop loss: -10% (opcional)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 CONFIGURACIÓN Y PERSONALIZACIÓN:

Símbolos recomendados por defecto:

  CORTO PLAZO: AAPL, MSFT, NVDA, GOOGL, AMZN
  MEDIANO: SPY, QQQ, AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA
  LARGO: SPY, QQQ, BRK.B, AAPL, MSFT, GOOGL, AMZN

Puedes reemplazarlos con:
  • Acciones: TSLA, NVDA, AMD, ZOOM, UBER
  • Índices: SPY, QQQ, IWM, DXY
  • Forex: EURUSD, GBPUSD, USDJPY, NZDUSD
  • Criptos: BTC, ETH, ADA, SOLANA (si yfinance lo soporta)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ LIMITACIONES IMPORTANTES:

  ⏰ Datos retrasados 15+ minutos (limitación yfinance)
  📊 Análisis técnico puro (sin noticias)
  🔍 No analiza eventos corporativos
  💾 90 días de histórico (configurable)
  🌍 Solo símbolos en yfinance (AAPL, MSFT, EUR=X, etc.)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 ARCHIVOS RELACIONADOS:

  Módulo principal:     analisis/screener.py
  Tests:               test_screener.py
  Documentación:       SCREENER_AUTOMATICO_DOCUMENTACION.md
  Bot command:         telegram_bot/bot.py (comando_screener)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 PARA EMPEZAR:

1. Inicia el bot:
   python main.py

2. En Telegram, escribe:
   /screener medio AAPL MSFT GOOGL

3. Espera 10-15 segundos

4. Recibirás análisis completo con recomendaciones

5. Para un símbolo específico:
   /analizar AAPL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ TODO LISTO PARA USAR

El screener está completamente integrado en el bot y listo para análisis
en vivo. Úsalo con responsabilidad y complementa con tu propia investigación.

═══════════════════════════════════════════════════════════════════════════════
""")
