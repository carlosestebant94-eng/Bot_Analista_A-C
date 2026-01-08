#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para reproducir exactamente el error con QQQ
Prueba el flujo completo del bot
"""

import sys
import logging

logging.basicConfig(level=logging.INFO)

# Test 1: Verificar MarketDataManager directamente
print("\n" + "="*70)
print("TEST 1: MarketDataManager.obtener_datos_actuales()")
print("="*70)

from data_sources.market_data import MarketDataManager

manager = MarketDataManager()
datos = manager.obtener_datos_actuales("QQQ")

if "error" in datos:
    print(f"ERROR: {datos['error']}")
else:
    print(f"SUCCESS: QQQ data obtained")
    print(f"   Precio: {datos.get('precio_actual')}")
    print(f"   Volumen: {datos.get('volumen')}")

# Test 2: Verificar AnalysisMethodology.analizar_ticker()
print("\n" + "="*70)
print("TEST 2: AnalysisMethodology.analizar_ticker()")
print("="*70)

from cerebro import AnalysisMethodology

methodology = AnalysisMethodology()
resultado = methodology.analizar_ticker("QQQ")

if resultado.get("status") != "completado":
    print(f"ERROR: {resultado.get('error')}")
    print(f"   Status: {resultado.get('status')}")
else:
    print(f"SUCCESS: Analysis completed")
    print(f"   Ticker: {resultado.get('ticker')}")
    print(f"   Precio: {resultado.get('datos_actuales', {}).get('precio_actual')}")
    print(f"   Recomendacion: {resultado.get('recomendacion', {}).get('recomendacion')}")

print("\n" + "="*70)
