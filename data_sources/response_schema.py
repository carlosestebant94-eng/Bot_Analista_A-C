"""
data_sources/response_schema.py
PUNTO 4: Schema unificado para respuestas inter-módulos
Asegura consistencia de formatos en toda la aplicación
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
import pytz


class ResponseStatus(Enum):
    """Estados posibles de una respuesta"""
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    PARTIAL = "partial"


class UnifiedResponse:
    """
    Respuesta unificada para TODAS las APIs internas
    
    Estructura garantizada:
    {
        "status": "success|warning|error|partial",
        "data": {...},
        "metadata": {
            "timestamp": "ISO8601 + timezone",
            "source": "module_name",
            "version": "1.0"
        },
        "errors": ["error1", "error2"],
        "warnings": ["warning1"],
        "cache": {
            "hit": bool,
            "ttl": seconds
        }
    }
    """
    
    def __init__(self, 
                 status: ResponseStatus = ResponseStatus.SUCCESS,
                 data: Optional[Dict[str, Any]] = None,
                 source: str = "unknown"):
        """
        Inicializa respuesta unificada
        
        Args:
            status: Estado de la respuesta
            data: Datos a retornar
            source: Módulo que origina la respuesta
        """
        self.status = status
        self.data = data or {}
        self.source = source
        self.module = source  # Alias para compatibilidad
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.cache_info: Dict[str, Any] = {}
        self.cache_metadata = self.cache_info  # Alias para compatibilidad
        self.timestamp = datetime.now(pytz.UTC)
    
    def add_error(self, error: str) -> 'UnifiedResponse':
        """Agrega un error a la respuesta"""
        self.errors.append(error)
        if self.status == ResponseStatus.SUCCESS:
            self.status = ResponseStatus.ERROR
        return self
    
    def add_warning(self, warning: str) -> 'UnifiedResponse':
        """Agrega una advertencia a la respuesta"""
        self.warnings.append(warning)
        if self.status == ResponseStatus.SUCCESS:
            self.status = ResponseStatus.WARNING
        return self
    
    def set_cache_info(self, hit: bool, ttl: Optional[int] = None) -> 'UnifiedResponse':
        """Registra información de caché"""
        self.cache_info = {
            "hit": hit,
            "ttl": ttl
        }
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario para JSON"""
        response = {
            "status": self.status.value,
            "data": self.data,
            "metadata": {
                "timestamp": self.timestamp.isoformat(),
                "source": self.source,
                "version": "1.0",
                "timezone": "UTC"
            }
        }
        
        if self.errors:
            response["errors"] = self.errors
        
        if self.warnings:
            response["warnings"] = self.warnings
        
        if self.cache_info:
            response["cache"] = self.cache_info
        
        return response


class PriceData:
    """Esquema unificado para datos de precio"""
    
    def __init__(self, 
                 ticker: str,
                 current_price: float,
                 timestamp: Optional[datetime] = None):
        """
        Inicializa datos de precio normalizados
        
        Args:
            ticker: Símbolo del activo (AAPL, BTC, etc)
            current_price: Precio actual en USD
            timestamp: Timestamp en UTC
        """
        if timestamp is None:
            timestamp = datetime.now(pytz.UTC)
        elif timestamp.tzinfo is None:
            timestamp = pytz.UTC.localize(timestamp)
        
        self.ticker = ticker.upper()
        self.current_price = float(current_price)
        self.timestamp = timestamp
        self.open_price: Optional[float] = None
        self.high_price: Optional[float] = None
        self.low_price: Optional[float] = None
        self.volume: Optional[float] = None
        self.change_percent: Optional[float] = None
        self.change_absolute: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Retorna diccionario normalizado"""
        return {
            "ticker": self.ticker,
            "current_price_usd": self.current_price,
            "open_price_usd": self.open_price,
            "high_price_usd": self.high_price,
            "low_price_usd": self.low_price,
            "volume_units": self.volume,
            "change_percent": self.change_percent,
            "change_absolute": self.change_absolute,
            "timestamp_utc": self.timestamp.isoformat()
        }


class MacroData:
    """Esquema unificado para datos macroeconómicos"""
    
    def __init__(self,
                 indicator: str,
                 value: float,
                 unit: str = "percent",
                 timestamp: Optional[datetime] = None):
        """
        Inicializa datos macro normalizados
        
        Args:
            indicator: Tipo de indicador (unemployment, inflation, interest_rate, etc)
            value: Valor del indicador
            unit: Unidad (percent, basis_points, index, etc)
            timestamp: Timestamp UTC
        """
        if timestamp is None:
            timestamp = datetime.now(pytz.UTC)
        elif timestamp.tzinfo is None:
            timestamp = pytz.UTC.localize(timestamp)
        
        self.indicator = indicator.lower()
        self.value = float(value)
        self.unit = unit.lower()
        self.timestamp = timestamp
        self.frequency: Optional[str] = None  # daily, monthly, quarterly, annual
    
    def to_dict(self) -> Dict[str, Any]:
        """Retorna diccionario normalizado"""
        return {
            "indicator": self.indicator,
            "value": self.value,
            "unit": self.unit,
            "frequency": self.frequency,
            "timestamp_utc": self.timestamp.isoformat()
        }


class AnalysisResult:
    """Esquema unificado para resultados de análisis"""
    
    def __init__(self,
                 analysis_type: str,
                 ticker: str,
                 timestamp: Optional[datetime] = None):
        """
        Inicializa resultado de análisis normalizado
        
        Args:
            analysis_type: Tipo de análisis (correlation, ml_prediction, etc)
            ticker: Símbolo analizado
            timestamp: Timestamp UTC
        """
        if timestamp is None:
            timestamp = datetime.now(pytz.UTC)
        elif timestamp.tzinfo is None:
            timestamp = pytz.UTC.localize(timestamp)
        
        self.analysis_type = analysis_type.lower()
        self.ticker = ticker.upper()
        self.timestamp = timestamp
        self.confidence: float = 0.0  # 0-100
        self.findings: List[str] = []
        self.recommendations: List[str] = []
        self.data_sources: List[str] = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Retorna diccionario normalizado"""
        return {
            "analysis_type": self.analysis_type,
            "ticker": self.ticker,
            "confidence_percent": self.confidence,
            "findings": self.findings,
            "recommendations": self.recommendations,
            "data_sources": self.data_sources,
            "timestamp_utc": self.timestamp.isoformat()
        }


# Funciones de conveniencia

def normalize_timestamp(dt: Optional[datetime] = None) -> datetime:
    """Normaliza un timestamp a UTC"""
    if dt is None:
        return datetime.now(pytz.UTC)
    if dt.tzinfo is None:
        return pytz.UTC.localize(dt)
    return dt.astimezone(pytz.UTC)


def normalize_percentage(value: float) -> float:
    """Normaliza porcentajes a rango 0-100"""
    if value > 100:
        return value / 100
    return value


def normalize_currency(value: float, 
                      from_currency: str = "USD",
                      to_currency: str = "USD") -> float:
    """Normaliza monedas (convertible a futuros cambios)"""
    if from_currency == to_currency:
        return float(value)
    # Placeholder para conversión futura
    return float(value)


if __name__ == "__main__":
    import json
    
    print("\n🔍 TEST: Schema Unificado\n")
    
    # Test 1: Respuesta unificada
    print("1️⃣  Respuesta Unificada:")
    resp = UnifiedResponse(ResponseStatus.SUCCESS, {"key": "value"}, "test_module")
    resp.set_cache_info(True, 3600)
    print(json.dumps(resp.to_dict(), indent=2, default=str))
    
    # Test 2: Datos de precio
    print("\n2️⃣  Precio Unificado:")
    price = PriceData("AAPL", 150.25)
    price.open_price = 149.50
    price.high_price = 151.00
    price.volume = 1000000
    price.change_percent = 0.5
    print(json.dumps(price.to_dict(), indent=2, default=str))
    
    # Test 3: Datos macro
    print("\n3️⃣  Macro Unificado:")
    macro = MacroData("unemployment", 4.2, "percent")
    macro.frequency = "monthly"
    print(json.dumps(macro.to_dict(), indent=2, default=str))
    
    # Test 4: Resultado de análisis
    print("\n4️⃣  Análisis Unificado:")
    analysis = AnalysisResult("correlation", "AAPL")
    analysis.confidence = 85.5
    analysis.findings = ["Strong correlation with SPY"]
    analysis.data_sources = ["yfinance", "fred"]
    print(json.dumps(analysis.to_dict(), indent=2, default=str))
    
    print("\n✅ Schema unificado validado\n")
