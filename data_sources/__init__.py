"""
data_sources/
Módulo gestor de fuentes de datos en tiempo real
Conecta con YFinance, Finviz, Polygon.io, Alpha Vantage, FRED
"""

from .market_data import MarketDataManager
from .macroeconomic_data import MacroeconomicDataManager
from .fundamental_analyzer import FundamentalAnalyzer
from .data_validator import DataValidator
from .data_pipeline import DataPipeline, obtener_pipeline

try:
    from .finviz_scraper import FinvizScraper
    __all__ = [
        'MarketDataManager', 
        'FinvizScraper',
        'MacroeconomicDataManager',
        'FundamentalAnalyzer',
        'DataValidator',
        'DataPipeline',
        'obtener_pipeline'
    ]
except ImportError:
    __all__ = [
        'MarketDataManager',
        'MacroeconomicDataManager',
        'FundamentalAnalyzer',
        'DataValidator',
        'DataPipeline',
        'obtener_pipeline'
    ]
