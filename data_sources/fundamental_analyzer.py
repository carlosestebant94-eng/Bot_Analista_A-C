"""
data_sources/fundamental_analyzer.py
Analizador de datos fundamentales de acciones
Obtiene ratios P/E, earnings, balance sheets, etc.
"""

import logging
import yfinance as yf
import pandas as pd
from typing import Dict, Optional, Any, List
from datetime import datetime, timedelta


class FundamentalAnalyzer:
    """Analizador de datos fundamentales de empresas"""
    
    def __init__(self):
        """Inicializa el analizador fundamental"""
        self.logger = logging.getLogger("FundamentalAnalyzer")
        self.cache = {}
        self.cache_ttl = 86400  # 24 horas
        self.cache_expiry = {}
        self.logger.info("✅ Analizador fundamental inicializado")
    
    def obtener_info_fundamental(self, ticker: str) -> Dict[str, Any]:
        """
        Obtiene información fundamental completa de una acción
        
        Args:
            ticker: Símbolo del ticker (ej: AAPL)
            
        Returns:
            Diccionario con datos fundamentales
        """
        try:
            cache_key = f"fundamental_{ticker}"
            if self._es_cache_valido(cache_key):
                return self.cache[cache_key]
            
            stock = yf.Ticker(ticker)
            info = stock.info
            
            resultado = {
                'ticker': ticker,
                'timestamp': datetime.now().isoformat(),
                'empresa': {
                    'nombre': info.get('longName', 'N/A'),
                    'sector': info.get('sector', 'N/A'),
                    'industria': info.get('industry', 'N/A'),
                    'pais': info.get('country', 'N/A'),
                    'sitio_web': info.get('website', 'N/A'),
                    'descripcion': info.get('longBusinessSummary', 'N/A')[:500]
                },
                'valuacion': self._extraer_valuacion(info),
                'rentabilidad': self._extraer_rentabilidad(info),
                'endeudamiento': self._extraer_endeudamiento(info),
                'salud_financiera': self._extraer_salud_financiera(info),
                'crecimiento': self._extraer_crecimiento(info),
                'eficiencia': self._extraer_eficiencia(info)
            }
            
            # Guardar en cache
            self.cache[cache_key] = resultado
            self.cache_expiry[cache_key] = datetime.now()
            
            return resultado
            
        except Exception as e:
            self.logger.warning(f"Error obteniendo datos fundamentales de {ticker}: {e}")
            return {
                'ticker': ticker,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def obtener_reporte_earnings(self, ticker: str) -> Dict[str, Any]:
        """
        Obtiene datos de earnings y proyecciones
        
        Args:
            ticker: Símbolo del ticker
            
        Returns:
            Diccionario con datos de earnings
        """
        try:
            cache_key = f"earnings_{ticker}"
            if self._es_cache_valido(cache_key):
                return self.cache[cache_key]
            
            stock = yf.Ticker(ticker)
            info = stock.info
            
            resultado = {
                'ticker': ticker,
                'timestamp': datetime.now().isoformat(),
                'earnings': {
                    'eps_actual': info.get('trailingEps', 'N/A'),
                    'eps_proximo': info.get('forwardEps', 'N/A'),
                    'eps_anual': info.get('epsTrailingTwelveMonths', 'N/A'),
                    'crecimiento_eps': self._calcular_crecimiento_eps(info),
                    'fecha_proximo_earnings': info.get('nextFiscalYearEnd', 'N/A'),
                    'fecha_reporte_earnings': info.get('earningsDate', 'N/A')
                },
                'ingresos': {
                    'ingresos_anuales': info.get('totalRevenue', 'N/A'),
                    'ingresos_por_accion': info.get('revenuePerShare', 'N/A'),
                    'margen_operativo': info.get('operatingMargins', 'N/A'),
                    'margen_neto': info.get('profitMargins', 'N/A')
                },
                'proyecciones': {
                    'crecimiento_ingresos_estimado': info.get('revenueGrowth', 'N/A'),
                    'crecimiento_eps_estimado': info.get('epsGrowth', 'N/A')
                }
            }
            
            self.cache[cache_key] = resultado
            self.cache_expiry[cache_key] = datetime.now()
            
            return resultado
            
        except Exception as e:
            self.logger.warning(f"Error obteniendo earnings de {ticker}: {e}")
            return {'ticker': ticker, 'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def obtener_balance_sheet(self, ticker: str) -> Dict[str, Any]:
        """
        Obtiene datos del balance sheet
        
        Args:
            ticker: Símbolo del ticker
            
        Returns:
            Diccionario con datos del balance
        """
        try:
            cache_key = f"balance_{ticker}"
            if self._es_cache_valido(cache_key):
                return self.cache[cache_key]
            
            stock = yf.Ticker(ticker)
            info = stock.info
            
            resultado = {
                'ticker': ticker,
                'timestamp': datetime.now().isoformat(),
                'activos': {
                    'activos_totales': info.get('totalAssets', 'N/A'),
                    'activos_circulantes': info.get('currentAssets', 'N/A')
                },
                'pasivos': {
                    'pasivos_totales': info.get('totalLiabilities', 'N/A'),
                    'deuda_corto_plazo': info.get('currentLiabilities', 'N/A'),
                    'deuda_largo_plazo': info.get('longTermDebt', 'N/A')
                },
                'patrimonio': {
                    'patrimonio_total': info.get('totalStockholderEquity', 'N/A'),
                    'libro_valor': info.get('bookValue', 'N/A')
                }
            }
            
            self.cache[cache_key] = resultado
            self.cache_expiry[cache_key] = datetime.now()
            
            return resultado
            
        except Exception as e:
            self.logger.warning(f"Error obteniendo balance de {ticker}: {e}")
            return {'ticker': ticker, 'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def comparar_pares(self, ticker1: str, ticker2: str) -> Dict[str, Any]:
        """
        Compara dos empresas fundamentalmente
        
        Args:
            ticker1: Primer ticker
            ticker2: Segundo ticker
            
        Returns:
            Comparativa
        """
        info1 = self.obtener_info_fundamental(ticker1)
        info2 = self.obtener_info_fundamental(ticker2)
        
        comparativa = {
            'empresa1': {
                'ticker': ticker1,
                'pe_ratio': info1.get('valuacion', {}).get('pe_ratio'),
                'pb_ratio': info1.get('valuacion', {}).get('pb_ratio'),
                'roe': info1.get('rentabilidad', {}).get('roe'),
                'roa': info1.get('rentabilidad', {}).get('roa')
            },
            'empresa2': {
                'ticker': ticker2,
                'pe_ratio': info2.get('valuacion', {}).get('pe_ratio'),
                'pb_ratio': info2.get('valuacion', {}).get('pb_ratio'),
                'roe': info2.get('rentabilidad', {}).get('roe'),
                'roa': info2.get('rentabilidad', {}).get('roa')
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return comparativa
    
    def _extraer_valuacion(self, info: Dict) -> Dict[str, Any]:
        """Extrae métricas de valuación"""
        return {
            'pe_ratio': info.get('trailingPE', 'N/A'),
            'pe_forward': info.get('forwardPE', 'N/A'),
            'pb_ratio': info.get('priceToBook', 'N/A'),
            'precio_venta': info.get('priceToSalesTrailing12Months', 'N/A'),
            'peg_ratio': info.get('pegRatio', 'N/A'),
            'valor_empresa': info.get('enterpriseValue', 'N/A'),
            'capitalizacion': info.get('marketCap', 'N/A')
        }
    
    def _extraer_rentabilidad(self, info: Dict) -> Dict[str, Any]:
        """Extrae métricas de rentabilidad"""
        return {
            'roe': info.get('returnOnEquity', 'N/A'),
            'roa': info.get('returnOnAssets', 'N/A'),
            'margen_neto': info.get('profitMargins', 'N/A'),
            'margen_operativo': info.get('operatingMargins', 'N/A'),
            'margen_bruto': info.get('grossMargins', 'N/A'),
            'dividendo_yield': info.get('dividendYield', 'N/A')
        }
    
    def _extraer_endeudamiento(self, info: Dict) -> Dict[str, Any]:
        """Extrae métricas de endeudamiento"""
        return {
            'deuda_total': info.get('totalDebt', 'N/A'),
            'ratio_deuda_capital': info.get('debtToEquity', 'N/A'),
            'ratio_deuda_ebitda': info.get('debtToEquity', 'N/A'),
            'interes_coverage': info.get('interestCoverage', 'N/A'),
            'liquides_ratio': info.get('currentRatio', 'N/A')
        }
    
    def _extraer_salud_financiera(self, info: Dict) -> Dict[str, Any]:
        """Extrae métricas de salud financiera"""
        return {
            'ratio_circulante': info.get('currentRatio', 'N/A'),
            'ratio_rapido': info.get('quickRatio', 'N/A'),
            'efectivo': info.get('totalCash', 'N/A'),
            'flujo_efectivo': info.get('operatingCashflow', 'N/A'),
            'flujo_libre': info.get('freeCashflow', 'N/A')
        }
    
    def _extraer_crecimiento(self, info: Dict) -> Dict[str, Any]:
        """Extrae métricas de crecimiento"""
        return {
            'crecimiento_ingresos': info.get('revenueGrowth', 'N/A'),
            'crecimiento_earnings': info.get('earningsGrowth', 'N/A'),
            'crecimiento_5y': info.get('fiveYearAverageReturn', 'N/A')
        }
    
    def _extraer_eficiencia(self, info: Dict) -> Dict[str, Any]:
        """Extrae métricas de eficiencia operativa"""
        return {
            'rotacion_activos': info.get('assetTurnover', 'N/A'),
            'dias_ventas_pendientes': info.get('daysOfSalesOutstanding', 'N/A'),
            'dias_inventario': info.get('daysOfInventoryOutstanding', 'N/A'),
            'ciclo_efectivo': info.get('cashConversionCycle', 'N/A')
        }
    
    def _calcular_crecimiento_eps(self, info: Dict) -> Optional[float]:
        """Calcula el crecimiento de EPS"""
        try:
            eps_actual = info.get('trailingEps')
            eps_historico = info.get('epsTrailingTwelveMonths')
            
            if eps_actual and eps_historico and eps_historico != 0:
                return (eps_actual - eps_historico) / eps_historico * 100
        except:
            pass
        
        return None
    
    def _es_cache_valido(self, key: str) -> bool:
        """Verifica si un cache es válido"""
        if key not in self.cache or key not in self.cache_expiry:
            return False
        
        tiempo_desde_cache = (datetime.now() - self.cache_expiry[key]).total_seconds()
        return tiempo_desde_cache < self.cache_ttl
    
    def limpiar_cache(self):
        """Limpia el cache"""
        self.cache.clear()
        self.cache_expiry.clear()
        self.logger.info("Cache de fundamentales limpiado")
