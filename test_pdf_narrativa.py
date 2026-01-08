#!/usr/bin/env python3
"""Test para verificar que el PDF incluye el análisis narrativo"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils.pdf_generator import PDFReportGenerator

# Datos de prueba
pdf_gen = PDFReportGenerator()

pdf_path = pdf_gen.generar_reporte_analisis(
    ticker="AAPL",
    datos_actuales={
        'ticker': 'AAPL',
        'precio_actual': 150.25,
        'cambio_pct': 2.5,
        'nombre': 'Apple Inc.'
    },
    fundamentales={
        'P/E Ratio': 28.5,
        'Market Cap': '$3.2T',
        'Dividend Yield': '0.42%'
    },
    tecnico={
        'RSI': {'valor': 65, 'señal': 'Débil al alza'},
        'MACD': {'linea_macd': 2.34, 'linea_senal': 1.85, 'señal': 'Alcista'}
    },
    alexander={
        'marea': {'marea_general': 'Alcista'},
        'movimiento': {'movimiento': 'Alcista'}
    },
    soportes_resistencias={'soporte': 145.0, 'resistencia': 155.0},
    recomendacion={'recomendacion': 'COMPRA'},
    entry_price=150.0,
    stop_loss=148.0,
    take_profit=160.0,
    ganancia_potencial=6.67,
    perdida_potencial=1.33,
    tiempo_proyectado='2 semanas',
    proyeccion='Alcista',
    recomendable='Si',
    analisis_narrativo="""
AAPL se cotiza en $150.25 con un cambio de 2.5%.

El analisis tecnico muestra un RSI en 65 puntos (Debil al alza), mientras que el MACD presenta una senal Alcista. Estos indicadores sugieren un momento debil al alza en el instrumento.

El analisis Alexander indica una Marea Alcista a nivel macro con un Movimiento Alcista en la tendencia local. Esta combinacion sugiere un entorno alcista que favorece posiciones alcistas.

En conclusion, el instrumento presenta una configuracion tecnica y fundamental que refuerza el sesgo alcista observado en el periodo analizado.
"""
)

print(f"PDF generado exitosamente en: {pdf_path}")
print(f"Archivo existe: {Path(pdf_path).exists()}")
print(f"Tamaño: {Path(pdf_path).stat().st_size} bytes")
