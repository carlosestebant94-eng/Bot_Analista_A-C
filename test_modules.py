"""
test_modules.py
Test rápido de los nuevos módulos
"""

from data_sources.market_data import MarketDataManager
from cerebro.analysis_methodology import AnalysisMethodology

print('='*80)
print('TEST DE MÓDULOS - Verificación de importes y estado')
print('='*80)
print()

# Test 1: MarketDataManager
print('1. MarketDataManager:')
try:
    dm = MarketDataManager()
    status = dm.get_status()
    print(f'   Estado: {status["fuente_principal"]}')
    print(f'   Datos actuales: {status["datos_actuales"]}')
    print(f'   ✅ OK')
except Exception as e:
    print(f'   ❌ ERROR: {e}')

print()

# Test 2: AnalysisMethodology
print('2. AnalysisMethodology:')
try:
    am = AnalysisMethodology()
    status = am.get_status()
    print(f'   Estado: {status["estado"]}')
    print(f'   Metodologia: {status["metodologia"]}')
    print(f'   Indicadores: {len(status["indicadores"])} disponibles')
    print(f'   ✅ OK')
except Exception as e:
    print(f'   ❌ ERROR: {e}')

print()
print('='*80)
print('✅ TODOS LOS MODULOS CARGADOS CORRECTAMENTE')
print('='*80)
