"""
data_sources/data_pipeline.py
CORRECTION #7: Centralized Data Pipeline with Validation
Middleware que centraliza la validación de todos los datos externos
Previene que datos inválidos/incompletos lleguen a los análisis
"""

import logging
from typing import Dict, Optional, Any, List, Tuple
from datetime import datetime
from enum import Enum

from .data_validator import DataValidator
from .market_data import MarketDataManager
from .macroeconomic_data import MacroeconomicDataManager


class DataSource(Enum):
    """Enumeración de fuentes de datos"""
    YFINANCE = "yfinance"
    FRED = "fred"
    FINVIZ = "finviz"
    INTERNAL = "internal"


class DataPipeline:
    """
    Centralized Data Pipeline with automatic validation
    
    Propósito: Canalizar todos los datos a través de validación automática
    Antes de que lleguen a los módulos de análisis.
    
    Beneficios:
    - Una única puerta de entrada para datos
    - Validación consistente en todos lados
    - Logs centralizados de data quality
    - Fácil de auditar y debugging
    """
    
    def __init__(self):
        """Inicializa el pipeline de datos"""
        self.logger = logging.getLogger("DataPipeline")
        self.validator = DataValidator()
        self.market_manager = MarketDataManager()
        self.macro_manager = MacroeconomicDataManager()
        
        # Stats de validación
        self.stats = {
            'total_validations': 0,
            'successful': 0,
            'failed': 0,
            'data_sources': {}
        }
        
        self.logger.info("✅ Data Pipeline inicializado con validación centralizada")
    
    def obtener_datos_mercado(
        self, 
        ticker: str,
        validar: bool = True
    ) -> Dict[str, Any]:
        """
        Obtiene datos de mercado CON VALIDACIÓN AUTOMÁTICA
        
        Args:
            ticker: Símbolo del instrumento
            validar: Si debe validar datos (default: True)
            
        Returns:
            Dict con datos validados o error
        """
        try:
            self._registrar_inicio("market_data", ticker)
            
            # Obtener datos del mercado
            datos = self.market_manager.obtener_datos_actuales(ticker)
            
            # Si hay error, retornar inmediatamente
            if 'error' in datos:
                self._registrar_resultado("market_data", ticker, False, datos['error'])
                return datos
            
            # VALIDAR DATOS SI SE PIDE
            if validar:
                is_valid, errors = self._validar_datos_mercado(datos, ticker)
                if not is_valid:
                    resultado = {
                        'error': f'Datos inválidos: {errors}',
                        'ticker': ticker,
                        'datos_crudos': datos,
                        'timestamp': datetime.now().isoformat()
                    }
                    self._registrar_resultado("market_data", ticker, False, errors)
                    return resultado
            
            self._registrar_resultado("market_data", ticker, True, None)
            return datos
            
        except Exception as e:
            self.logger.error(f"❌ Error en pipeline mercado {ticker}: {str(e)}")
            self._registrar_resultado("market_data", ticker, False, str(e))
            return {'error': str(e), 'ticker': ticker}
    
    def obtener_contexto_macro(
        self,
        validar: bool = True
    ) -> Dict[str, Any]:
        """
        Obtiene contexto macroeconómico CON VALIDACIÓN
        
        Args:
            validar: Si debe validar datos (default: True)
            
        Returns:
            Dict con contexto validado
        """
        try:
            self._registrar_inicio("macro_data", "global")
            
            contexto = self.macro_manager.obtener_contexto_macro_resumido()
            
            if validar:
                is_valid, errors = self._validar_contexto_macro(contexto)
                if not is_valid:
                    self.logger.warning(f"⚠️  Contexto macro parcialmente inválido: {errors}")
            
            self._registrar_resultado("macro_data", "global", True, None)
            return contexto
            
        except Exception as e:
            self.logger.error(f"❌ Error obteniendo contexto macro: {str(e)}")
            self._registrar_resultado("macro_data", "global", False, str(e))
            return {'error': str(e)}
    
    def procesar_lote(
        self,
        tickers: List[str],
        con_validacion: bool = True
    ) -> Dict[str, Dict[str, Any]]:
        """
        Procesa múltiples tickers a través del pipeline
        
        Args:
            tickers: Lista de tickers a procesar
            con_validacion: Si debe validar (default: True)
            
        Returns:
            Dict {ticker: datos_validados}
        """
        resultados = {}
        
        for ticker in tickers:
            resultados[ticker] = self.obtener_datos_mercado(ticker, con_validacion)
        
        # Log resumen
        validos = sum(1 for d in resultados.values() if 'error' not in d)
        self.logger.info(f"✅ Lote procesado: {validos}/{len(tickers)} tickers válidos")
        
        return resultados
    
    # ==================== MÉTODOS PRIVADOS DE VALIDACIÓN ====================
    
    def _validar_datos_mercado(
        self,
        datos: Dict[str, Any],
        ticker: str
    ) -> Tuple[bool, Optional[str]]:
        """Valida datos de mercado según múltiples criterios"""
        
        campos_requeridos = [
            'precio_actual', 'volumen', 'cambio_pct'
        ]
        
        # Verificar campos requeridos
        for campo in campos_requeridos:
            if campo not in datos or datos[campo] is None:
                return False, f"Campo faltante: {campo}"
        
        # Validar precio
        is_valid, err = self.validator.validar_precio(datos['precio_actual'], ticker)
        if not is_valid:
            return False, f"Precio inválido: {err}"
        
        # Validar volumen
        if datos.get('volumen') and datos['volumen'] > 0:
            is_valid, err = self.validator.validar_volumen(datos['volumen'], ticker)
            if not is_valid:
                return False, f"Volumen inválido: {err}"
        
        # Validar cambio %
        cambio = datos.get('cambio_pct')
        if cambio is not None:
            is_valid, err = self.validator.validar_cambio_pct(cambio, ticker)
            if not is_valid:
                return False, f"Cambio % inválido: {err}"
        
        return True, None
    
    def _validar_contexto_macro(
        self,
        contexto: Dict[str, Any]
    ) -> Tuple[bool, Optional[List[str]]]:
        """Valida contexto macroeconómico"""
        
        errores = []
        
        # Validar tasas de interés
        tasas = contexto.get('tasas_interes', {})
        if tasas and '10y' in tasas:
            is_valid, err = self.validator.validar_tasa_interes(tasas['10y'])
            if not is_valid:
                errores.append(f"Tasa 10Y inválida: {err}")
        
        # Validar desempleo
        desempleo = contexto.get('desempleo')
        if desempleo:
            is_valid, err = self.validator.validar_desempleo(desempleo)
            if not is_valid:
                errores.append(f"Desempleo inválido: {err}")
        
        # Validar inflación
        inflacion = contexto.get('inflacion')
        if inflacion:
            is_valid, err = self.validator.validar_inflacion(inflacion)
            if not is_valid:
                errores.append(f"Inflación inválida: {err}")
        
        return len(errores) == 0, errores if errores else None
    
    # ==================== ESTADÍSTICAS Y LOGGING ====================
    
    def _registrar_inicio(self, source: str, ticker: str):
        """Registra el inicio de una validación"""
        self.stats['total_validations'] += 1
        if source not in self.stats['data_sources']:
            self.stats['data_sources'][source] = {'success': 0, 'failed': 0}
    
    def _registrar_resultado(
        self,
        source: str,
        ticker: str,
        exitoso: bool,
        error: Optional[str] = None
    ):
        """Registra resultado de validación"""
        if exitoso:
            self.stats['successful'] += 1
            self.stats['data_sources'][source]['success'] += 1
        else:
            self.stats['failed'] += 1
            self.stats['data_sources'][source]['failed'] += 1
            if error:
                self.logger.warning(f"⚠️  {source}/{ticker}: {error}")
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Retorna estadísticas del pipeline"""
        total = self.stats['total_validations']
        tasa_exito = (self.stats['successful'] / total * 100) if total > 0 else 0
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_validaciones': total,
            'exitosas': self.stats['successful'],
            'fallidas': self.stats['failed'],
            'tasa_exito_pct': round(tasa_exito, 2),
            'por_fuente': self.stats['data_sources']
        }
    
    def generar_reporte_confiabilidad(self) -> str:
        """Genera reporte de confiabilidad del pipeline"""
        stats = self.obtener_estadisticas()
        
        reporte = f"""
╔════════════════════════════════════════════════════════════════════╗
║           REPORTE DE CONFIABILIDAD - DATA PIPELINE                ║
║              Validación Centralizada de Datos Externos             ║
╚════════════════════════════════════════════════════════════════════╝

📊 ESTADÍSTICAS GLOBALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Validaciones:        {stats['total_validaciones']}
✅ Exitosas:               {stats['exitosas']}
❌ Fallidas:               {stats['fallidas']}
📈 Tasa de Éxito:          {stats['tasa_exito_pct']}%

📦 POR FUENTE DE DATOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for fuente, datos in stats['por_fuente'].items():
            total_fuente = datos['success'] + datos['failed']
            if total_fuente > 0:
                tasa = datos['success'] / total_fuente * 100
                reporte += f"{fuente:20} ✅ {datos['success']:3} | ❌ {datos['failed']:3} | {tasa:6.2f}%\n"
        
        reporte += f"""
🔒 CONFIABILIDAD: {stats['tasa_exito_pct']:.1f}% ({'EXCELENTE ✅' if stats['tasa_exito_pct'] >= 95 else 'BUENA ⚠️' if stats['tasa_exito_pct'] >= 80 else 'CRÍTICA 🔴'})

Timestamp: {stats['timestamp']}
"""
        
        return reporte
    
    def limpiar_estadisticas(self):
        """Limpia las estadísticas acumuladas"""
        self.stats = {
            'total_validations': 0,
            'successful': 0,
            'failed': 0,
            'data_sources': {}
        }
        self.logger.info("Estadísticas limpias")


# ==================== INSTANCIA SINGLETON ====================

_pipeline_instance: Optional[DataPipeline] = None


def obtener_pipeline() -> DataPipeline:
    """Obtiene la instancia singleton del pipeline"""
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = DataPipeline()
    return _pipeline_instance


if __name__ == "__main__":
    # Test del pipeline
    logging.basicConfig(level=logging.INFO)
    
    pipeline = DataPipeline()
    
    # Test 1: Obtener datos de mercado
    print("\n🔍 Test 1: Obtener datos de mercado (con validación)")
    datos = pipeline.obtener_datos_mercado("AAPL")
    print(f"Resultado: {datos}")
    
    # Test 2: Obtener contexto macro
    print("\n🔍 Test 2: Obtener contexto macroeconómico")
    contexto = pipeline.obtener_contexto_macro()
    print(f"Resultado: {contexto}")
    
    # Test 3: Procesar lote
    print("\n🔍 Test 3: Procesar lote de tickers")
    tickers = ["AAPL", "MSFT", "GOOGL"]
    resultados = pipeline.procesar_lote(tickers)
    print(f"Resultados: {len(resultados)} tickers procesados")
    
    # Estadísticas
    print("\n📊 ESTADÍSTICAS DEL PIPELINE")
    print(pipeline.generar_reporte_confiabilidad())
