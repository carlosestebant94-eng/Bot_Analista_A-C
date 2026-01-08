#!/usr/bin/env python3
"""Test para verificar que el análisis narrativo se genera correctamente"""

import sys
from pathlib import Path

# Agregar rutas
sys.path.insert(0, str(Path(__file__).parent))

from telegram_bot.bot import TelegramAnalystBot
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Crear instancia del bot
bot = TelegramAnalystBot()

# Datos de prueba
datos_actuales = {
    'ticker': 'AAPL',
    'precio_actual': 150.25,
    'cambio_pct': 2.5
}

indicadores = {
    'RSI': {
        'valor': 65,
        'nivel': 'Sobrecomprado',
        'señal': 'Débil al alza'
    },
    'MACD': {
        'linea_macd': 2.34,
        'linea_senal': 1.85,
        'señal': 'Alcista'
    },
    'STOCHASTIC': {
        'linea_k': 78,
        'linea_d': 72,
        'señal': 'Sobrecomprado'
    },
    'MEDIAS_MOVILES': {
        'SMA_20': 148.50,
        'SMA_50': 146.20,
        'SMA_200': 144.00
    },
    'VOLUMEN': {
        'volumen_actual': '52.3M',
        'relacion': '1.2',
        'señal': 'Normal'
    }
}

alexander = {
    'marea': {
        'marea_general': 'Alcista',
        'vix': 15.2,
        'volatilidad_mercado': 'Baja',
        'riesgo': 'Bajo'
    },
    'movimiento': {
        'movimiento': 'Alcista',
        'fuerza': 'Fuerte',
        'consenso': 78,
        'señales_alcistas': 3,
        'señales_bajistas': 0
    },
    'factor_social': {
        'sentimiento': 'Positivo',
        'menciones': 'Aumentadas'
    }
}

resultado_analisis = {
    'tecnico': {'indicadores': indicadores},
    'alexander': alexander
}

print("=" * 50)
print("Generando análisis narrativo...")
print("=" * 50)

narrativa = bot._generar_analisis_narrativo(
    resultado_analisis,
    datos_actuales,
    indicadores,
    alexander
)

print("\nANALISIS NARRATIVO GENERADO:\n")
print(narrativa)
print("\n" + "=" * 50)
print(f"Longitud: {len(narrativa)} caracteres")
print("=" * 50)
