"""
data_sources/data_validator.py
Validador centralizado para todos los datos externos
Garantiza integridad y confiabilidad de fuentes
"""

import logging
from typing import Dict, Any, Optional, Union, List
from datetime import datetime
import pandas as pd
import numpy as np


class DataValidator:
    """Validador de datos externos de múltiples fuentes"""
    
    def __init__(self):
        self.logger = logging.getLogger("DataValidator")
        self.validation_errors = []
    
    # =====================================================
    # VALIDADORES DE MERCADO (YFinance)
    # =====================================================
    
    @staticmethod
    def validar_precio(precio: Any, ticker: str = "") -> tuple[bool, Optional[str]]:
        """
        Valida que un precio sea válido
        
        Args:
            precio: Valor a validar
            ticker: Símbolo del ticker (para logs)
        
        Returns:
            (es_válido, mensaje_error)
        """
        if precio is None:
            return False, f"{ticker}: Precio es None"
        
        try:
            precio_float = float(precio)
        except (ValueError, TypeError):
            return False, f"{ticker}: Precio no es numérico: {precio}"
        
        # Validaciones de rango
        if precio_float <= 0:
            return False, f"{ticker}: Precio negativo o cero: {precio_float}"
        
        if precio_float > 1_000_000:
            return False, f"{ticker}: Precio anormalmente alto: {precio_float}"
        
        return True, None
    
    @staticmethod
    def validar_volumen(volumen: Any, ticker: str = "") -> tuple[bool, Optional[str]]:
        """
        Valida que un volumen sea válido
        
        Args:
            volumen: Valor a validar
            ticker: Símbolo del ticker (para logs)
        
        Returns:
            (es_válido, mensaje_error)
        """
        if volumen is None:
            return False, f"{ticker}: Volumen es None"
        
        try:
            vol_int = int(volumen)
        except (ValueError, TypeError):
            return False, f"{ticker}: Volumen no es numérico: {volumen}"
        
        if vol_int < 0:
            return False, f"{ticker}: Volumen negativo: {vol_int}"
        
        return True, None
    
    @staticmethod
    def validar_cambio_pct(cambio: Any, ticker: str = "") -> tuple[bool, Optional[str]]:
        """
        Valida que un cambio porcentual sea válido
        
        Args:
            cambio: Valor a validar
            ticker: Símbolo del ticker (para logs)
        
        Returns:
            (es_válido, mensaje_error)
        """
        if cambio is None:
            return False, f"{ticker}: Cambio % es None"
        
        try:
            cambio_float = float(cambio)
        except (ValueError, TypeError):
            return False, f"{ticker}: Cambio % no es numérico: {cambio}"
        
        # Cambios extremos raramente ocurren
        if abs(cambio_float) > 100:
            return False, f"{ticker}: Cambio % anomálico: {cambio_float}%"
        
        return True, None
    
    # =====================================================
    # VALIDADORES DE FUNDAMENTALES (YFinance)
    # =====================================================
    
    @staticmethod
    def validar_pe_ratio(pe: Any, ticker: str = "") -> tuple[bool, Optional[str]]:
        """
        Valida que un P/E ratio sea válido
        
        Args:
            pe: Valor a validar
            ticker: Símbolo del ticker
        
        Returns:
            (es_válido, mensaje_error)
        """
        if pe is None:
            return True, None  # P/E None es aceptable (empresas sin earnings)
        
        try:
            pe_float = float(pe)
        except (ValueError, TypeError):
            return False, f"{ticker}: P/E no es numérico: {pe}"
        
        if pe_float < 0:
            return False, f"{ticker}: P/E negativo: {pe_float}"
        
        # P/E > 500 es sospechoso pero posible (growth stocks)
        if pe_float > 5000:
            return False, f"{ticker}: P/E anormalmente alto: {pe_float}"
        
        return True, None
    
    @staticmethod
    def validar_market_cap(market_cap: Any, ticker: str = "") -> tuple[bool, Optional[str]]:
        """
        Valida que un market cap sea válido
        
        Args:
            market_cap: Valor a validar
            ticker: Símbolo del ticker
        
        Returns:
            (es_válido, mensaje_error)
        """
        if market_cap is None:
            return True, None  # Market cap None es aceptable
        
        try:
            mc = float(market_cap)
        except (ValueError, TypeError):
            return False, f"{ticker}: Market Cap no es numérico: {market_cap}"
        
        if mc < 0:
            return False, f"{ticker}: Market Cap negativo: {mc}"
        
        if mc > 100_000_000_000_000:  # > $100 trillones
            return False, f"{ticker}: Market Cap irrealista: ${mc}"
        
        return True, None
    
    @staticmethod
    def validar_debt_to_equity(d_e: Any, ticker: str = "") -> tuple[bool, Optional[str]]:
        """
        Valida que D/E ratio sea válido
        
        Args:
            d_e: Valor a validar
            ticker: Símbolo del ticker
        
        Returns:
            (es_válido, mensaje_error)
        """
        if d_e is None:
            return True, None
        
        try:
            de = float(d_e)
        except (ValueError, TypeError):
            return False, f"{ticker}: D/E no es numérico: {d_e}"
        
        if de < 0:
            return False, f"{ticker}: D/E negativo (equity negativo): {de}"
        
        if de > 100:
            return False, f"{ticker}: D/E anormalmente alto: {de}"
        
        return True, None
    
    @staticmethod
    def validar_roe(roe: Any, ticker: str = "") -> tuple[bool, Optional[str]]:
        """
        Valida que ROE sea válido
        
        Args:
            roe: Valor a validar
            ticker: Símbolo del ticker
        
        Returns:
            (es_válido, mensaje_error)
        """
        if roe is None:
            return True, None
        
        try:
            roe_float = float(roe)
        except (ValueError, TypeError):
            return False, f"{ticker}: ROE no es numérico: {roe}"
        
        # ROE típicamente entre -100% y +100%
        if abs(roe_float) > 500:
            return False, f"{ticker}: ROE extremo: {roe_float}%"
        
        return True, None
    
    # =====================================================
    # VALIDADORES DE DATOS MACRO (FRED)
    # =====================================================
    
    @staticmethod
    def validar_tasa_interes(tasa: Any, tipo: str = "general") -> tuple[bool, Optional[str]]:
        """
        Valida que una tasa de interés sea válida
        
        Args:
            tasa: Valor a validar
            tipo: Tipo de tasa (10y, 2y, general)
        
        Returns:
            (es_válido, mensaje_error)
        """
        if tasa is None:
            return False, f"Tasa {tipo} es None"
        
        try:
            tasa_float = float(tasa)
        except (ValueError, TypeError):
            return False, f"Tasa {tipo} no es numérica: {tasa}"
        
        # Las tasas típicamente están entre -5% y +20%
        if tasa_float < -10:
            return False, f"Tasa {tipo} negativa extrema: {tasa_float}%"
        
        if tasa_float > 50:
            return False, f"Tasa {tipo} anormalmente alta: {tasa_float}%"
        
        return True, None
    
    @staticmethod
    def validar_inflacion(inflacion: Any) -> tuple[bool, Optional[str]]:
        """
        Valida que tasa de inflación sea válida
        
        Args:
            inflacion: Valor a validar
        
        Returns:
            (es_válido, mensaje_error)
        """
        if inflacion is None:
            return False, "Inflación es None"
        
        try:
            inf = float(inflacion)
        except (ValueError, TypeError):
            return False, f"Inflación no es numérica: {inflacion}"
        
        # Inflación típicamente -10% a +20%
        if inf < -50:
            return False, f"Inflación negativa extrema: {inf}%"
        
        if inf > 100:
            return False, f"Inflación anormalmente alta: {inf}%"
        
        return True, None
    
    @staticmethod
    def validar_desempleo(desempleo: Any) -> tuple[bool, Optional[str]]:
        """
        Valida tasa de desempleo
        
        Args:
            desempleo: Valor a validar
        
        Returns:
            (es_válido, mensaje_error)
        """
        if desempleo is None:
            return False, "Desempleo es None"
        
        try:
            desemp = float(desempleo)
        except (ValueError, TypeError):
            return False, f"Desempleo no es numérico: {desempleo}"
        
        # Desempleo típicamente 0-15%
        if desemp < 0:
            return False, f"Desempleo negativo: {desemp}%"
        
        if desemp > 50:
            return False, f"Desempleo anormalmente alto: {desemp}%"
        
        return True, None
    
    # =====================================================
    # VALIDADORES DE VIX
    # =====================================================
    
    @staticmethod
    def validar_vix(vix: Any) -> tuple[bool, Optional[str]]:
        """
        Valida que VIX sea válido
        
        Args:
            vix: Valor a validar
        
        Returns:
            (es_válido, mensaje_error)
        """
        if vix is None:
            return False, "VIX es None"
        
        try:
            vix_float = float(vix)
        except (ValueError, TypeError):
            return False, f"VIX no es numérico: {vix}"
        
        # VIX típicamente 10-80
        if vix_float < 5:
            return False, f"VIX anormalmente bajo: {vix_float}"
        
        if vix_float > 200:
            return False, f"VIX anormalmente alto: {vix_float}"
        
        return True, None
    
    # =====================================================
    # VALIDADORES DE DATAFRAMES
    # =====================================================
    
    @staticmethod
    def validar_historico(historico: pd.DataFrame, ticker: str = "") -> tuple[bool, Optional[str]]:
        """
        Valida que un DataFrame histórico sea válido
        
        Args:
            historico: DataFrame con datos OHLCV
            ticker: Símbolo del ticker
        
        Returns:
            (es_válido, mensaje_error)
        """
        if historico is None or historico.empty:
            return False, f"{ticker}: Histórico vacío o None"
        
        # Debe tener columnas esperadas
        columnas_esperadas = {'Open', 'High', 'Low', 'Close', 'Volume'}
        columnas_presentes = set(historico.columns)
        
        if not columnas_esperadas.issubset(columnas_presentes):
            faltantes = columnas_esperadas - columnas_presentes
            return False, f"{ticker}: Faltan columnas: {faltantes}"
        
        # Validar High >= Low >= Close >= Open
        for idx, row in historico.iterrows():
            if row['High'] < row['Low']:
                return False, f"{ticker}: High < Low en {idx}"
            if row['High'] < row['Close']:
                return False, f"{ticker}: High < Close en {idx}"
        
        return True, None
    
    # =====================================================
    # VALIDADOR DE RESPUESTAS COMPLETAS
    # =====================================================
    
    def validar_datos_mercado_completos(self, datos: Dict[str, Any], ticker: str) -> tuple[bool, List[str]]:
        """
        Valida respuesta completa de obtener_datos_actuales
        
        Args:
            datos: Dict con datos de mercado
            ticker: Símbolo del ticker
        
        Returns:
            (es_válido, lista_de_errores)
        """
        errores = []
        
        # Validar que no sea error
        if 'error' in datos:
            return False, [f"Error en datos: {datos.get('error')}"]
        
        # Validar campos críticos
        is_valid, err = self.validar_precio(datos.get('precio_actual'), ticker)
        if not is_valid:
            errores.append(err)
        
        is_valid, err = self.validar_volumen(datos.get('volumen'), ticker)
        if not is_valid:
            errores.append(err)
        
        is_valid, err = self.validar_cambio_pct(datos.get('cambio_pct'), ticker)
        if not is_valid:
            errores.append(err)
        
        return len(errores) == 0, errores
    
    def validar_fundamentales_completos(self, fundamentales: Dict[str, Any], ticker: str) -> tuple[bool, List[str]]:
        """
        Valida respuesta completa de obtener_fundamentales
        
        Args:
            fundamentales: Dict con datos fundamentales
            ticker: Símbolo del ticker
        
        Returns:
            (es_válido, lista_de_errores)
        """
        errores = []
        
        if 'error' in fundamentales:
            return False, [f"Error en fundamentales: {fundamentales.get('error')}"]
        
        # Validar campos no críticos (pueden ser None)
        is_valid, err = self.validar_pe_ratio(fundamentales.get('pe_ratio'), ticker)
        if not is_valid:
            errores.append(err)
        
        is_valid, err = self.validar_market_cap(fundamentales.get('market_cap'), ticker)
        if not is_valid:
            errores.append(err)
        
        is_valid, err = self.validar_debt_to_equity(fundamentales.get('debt_to_equity'), ticker)
        if not is_valid:
            errores.append(err)
        
        is_valid, err = self.validar_roe(fundamentales.get('roe'), ticker)
        if not is_valid:
            errores.append(err)
        
        return len(errores) == 0, errores
    
    def generar_reporte_validacion(self) -> Dict[str, Any]:
        """
        Genera reporte de todas las validaciones realizadas
        
        Returns:
            Dict con resumen de validaciones
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'total_validaciones': len(self.validation_errors),
            'errores': self.validation_errors,
            'estado': 'OK' if len(self.validation_errors) == 0 else 'CON ERRORES'
        }
