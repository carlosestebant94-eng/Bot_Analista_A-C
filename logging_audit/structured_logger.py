"""
logging_audit/structured_logger.py
PUNTO 6: Sistema de logging estructurado + audit trail
Reemplaza print statements dispersos con JSON estructurado
"""

import logging
import json
import logging.handlers
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
import uuid
import threading

logger = logging.getLogger("StructuredLogger")


class StructuredFormatter(logging.Formatter):
    """
    Formateador que genera JSON estructurado para cada log
    Facilita parsing, búsqueda y análisis de logs
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Convierte log record a JSON estructurado"""
        log_dict = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "thread": record.thread,
            "thread_name": record.threadName,
        }
        
        # Agregar contexto adicional si existe
        if hasattr(record, "user_id"):
            log_dict["user_id"] = record.user_id
        if hasattr(record, "request_id"):
            log_dict["request_id"] = record.request_id
        if hasattr(record, "ticker"):
            log_dict["ticker"] = record.ticker
        if hasattr(record, "duration_ms"):
            log_dict["duration_ms"] = record.duration_ms
        if hasattr(record, "status"):
            log_dict["status"] = record.status
        
        # Agregar exception si existe
        if record.exc_info:
            log_dict["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_dict, ensure_ascii=False)


class AuditLogger:
    """
    Logger especializado para auditoría
    Registra todas las operaciones críticas con contexto completo
    
    Ejemplo:
        audit = AuditLogger("market_data")
        audit.log_data_fetch("AAPL", source="yfinance", status="success", records=150)
    """
    
    def __init__(self, module_name: str, audit_dir: str = "logs/audit"):
        """
        Inicializa audit logger
        
        Args:
            module_name: Nombre del módulo (ej: "market_data", "analyzer")
            audit_dir: Directorio para audit logs
        """
        self.module_name = module_name
        self.audit_dir = Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger(f"Audit.{module_name}")
        self._setup_audit_handler()
        self.session_id = str(uuid.uuid4())[:8]
    
    def _setup_audit_handler(self) -> None:
        """Configura handler de auditoría con rotación"""
        log_file = self.audit_dir / f"{self.module_name}_audit.jsonl"
        
        # Handler con rotación por tamaño (10MB) + backup
        handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=10
        )
        
        handler.setFormatter(StructuredFormatter())
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
    
    def log_data_fetch(self, identifier: str, source: str, 
                      status: str, records: int, 
                      duration_ms: float = 0,
                      error: Optional[str] = None) -> None:
        """
        Registra operación de obtención de datos
        
        Args:
            identifier: Ticker/indicador obtenido
            source: Fuente de datos (yfinance, fred, etc)
            status: 'success', 'partial', 'error'
            records: Número de registros obtenidos
            duration_ms: Tiempo en ms
            error: Error si aplica
        """
        record = self.logger.makeRecord(
            self.logger.name,
            logging.INFO,
            "(audit)",
            0,
            f"Data fetch: {identifier} from {source}",
            (),
            None
        )
        
        record.identifier = identifier
        record.source = source
        record.status = status
        record.records = records
        record.duration_ms = round(duration_ms, 2)
        record.session_id = self.session_id
        record.event_type = "DATA_FETCH"
        
        if error:
            record.error = error
        
        self.logger.handle(record)
    
    def log_analysis_result(self, ticker: str, analysis_type: str,
                           confidence: float, findings: int,
                           duration_ms: float = 0) -> None:
        """
        Registra resultado de análisis
        
        Args:
            ticker: Ticker analizado
            analysis_type: Tipo de análisis
            confidence: Nivel de confianza (0-1)
            findings: Número de hallazgos
            duration_ms: Tiempo de análisis
        """
        record = self.logger.makeRecord(
            self.logger.name,
            logging.INFO,
            "(audit)",
            0,
            f"Analysis: {analysis_type} on {ticker}",
            (),
            None
        )
        
        record.ticker = ticker
        record.analysis_type = analysis_type
        record.confidence = round(confidence, 3)
        record.findings = findings
        record.duration_ms = round(duration_ms, 2)
        record.session_id = self.session_id
        record.event_type = "ANALYSIS_RESULT"
        
        self.logger.handle(record)
    
    def log_error_event(self, error_type: str, error_msg: str,
                       severity: str = "error", context: Dict = None) -> None:
        """
        Registra evento de error crítico
        
        Args:
            error_type: Tipo de error
            error_msg: Mensaje de error
            severity: 'error', 'critical', 'warning'
            context: Contexto adicional
        """
        record = self.logger.makeRecord(
            self.logger.name,
            logging.ERROR if severity == "error" else logging.CRITICAL,
            "(audit)",
            0,
            f"Error: {error_type}",
            (),
            None
        )
        
        record.error_type = error_type
        record.error_message = error_msg
        record.severity = severity
        record.session_id = self.session_id
        record.event_type = "ERROR_EVENT"
        
        if context:
            for key, value in context.items():
                setattr(record, key, value)
        
        self.logger.handle(record)
    
    def log_security_event(self, event_type: str, details: str,
                          severity: str = "warning") -> None:
        """
        Registra evento de seguridad
        
        Args:
            event_type: Tipo de evento (API_KEY_ACCESS, INVALID_INPUT, etc)
            details: Detalles del evento
            severity: Severidad
        """
        record = self.logger.makeRecord(
            self.logger.name,
            logging.WARNING if severity == "warning" else logging.CRITICAL,
            "(audit)",
            0,
            f"Security: {event_type}",
            (),
            None
        )
        
        record.event_type = "SECURITY_EVENT"
        record.security_event = event_type
        record.details = details
        record.severity = severity
        record.session_id = self.session_id
        record.timestamp = datetime.now().isoformat()
        
        self.logger.handle(record)


class PerformanceMonitor:
    """
    Monitorea y registra performance de operaciones críticas
    Genera reportes de latencia, throughput, bottlenecks
    """
    
    def __init__(self):
        self.logger = logging.getLogger("PerformanceMonitor")
        self.operations: Dict[str, List[float]] = {}
        self.lock = threading.RLock()
        self._setup_handler()
    
    def _setup_handler(self) -> None:
        """Configura handler de performance"""
        perf_dir = Path("logs/performance")
        perf_dir.mkdir(parents=True, exist_ok=True)
        
        handler = logging.FileHandler(perf_dir / "performance.jsonl")
        handler.setFormatter(StructuredFormatter())
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def record_operation(self, operation_name: str, duration_ms: float,
                        success: bool = True, metadata: Dict = None) -> None:
        """
        Registra duración de operación
        
        Args:
            operation_name: Nombre de operación
            duration_ms: Duración en ms
            success: Si fue exitosa
            metadata: Metadatos adicionales
        """
        with self.lock:
            if operation_name not in self.operations:
                self.operations[operation_name] = []
            
            self.operations[operation_name].append(duration_ms)
        
        record = self.logger.makeRecord(
            self.logger.name,
            logging.INFO,
            "(perf)",
            0,
            f"Operation: {operation_name}",
            (),
            None
        )
        
        record.operation = operation_name
        record.duration_ms = round(duration_ms, 2)
        record.success = success
        record.timestamp = datetime.now().isoformat()
        
        if metadata:
            for key, value in metadata.items():
                setattr(record, key, value)
        
        self.logger.handle(record)
    
    def get_stats(self, operation_name: str) -> Dict[str, float]:
        """
        Obtiene estadísticas de operación
        
        Returns:
            Dict con min, max, avg, median, p95, p99
        """
        with self.lock:
            if operation_name not in self.operations:
                return {}
            
            times = sorted(self.operations[operation_name])
            n = len(times)
            
            return {
                "count": n,
                "min_ms": round(min(times), 2),
                "max_ms": round(max(times), 2),
                "avg_ms": round(sum(times) / n, 2),
                "median_ms": round(times[n // 2], 2),
                "p95_ms": round(times[int(n * 0.95)], 2),
                "p99_ms": round(times[int(n * 0.99)], 2),
            }
    
    def get_all_stats(self) -> Dict[str, Dict[str, float]]:
        """Obtiene estadísticas de todas las operaciones"""
        with self.lock:
            return {
                op: self.get_stats(op)
                for op in self.operations.keys()
            }
    
    def log_performance_report(self) -> None:
        """Genera reporte de performance"""
        stats = self.get_all_stats()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "operations": stats
        }
        
        perf_dir = Path("logs/performance")
        perf_dir.mkdir(parents=True, exist_ok=True)
        
        with open(perf_dir / "performance_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Performance report generated with {len(stats)} operations")


def setup_centralized_logging(app_name: str = "BotAnalyst",
                             log_level: str = "INFO") -> None:
    """
    Configura logging centralizado para toda la aplicación
    
    Args:
        app_name: Nombre de la aplicación
        log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logs_dir = Path("logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Logger raíz
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Handler de consola (solo INFO+)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # Handler de archivo JSON (todo)
    json_handler = logging.handlers.RotatingFileHandler(
        logs_dir / f"{app_name}.jsonl",
        maxBytes=50 * 1024 * 1024,  # 50MB
        backupCount=20
    )
    json_handler.setFormatter(StructuredFormatter())
    root_logger.addHandler(json_handler)
    
    # Handler de errores críticos
    error_handler = logging.FileHandler(logs_dir / f"{app_name}_errors.log")
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    error_handler.setFormatter(error_formatter)
    root_logger.addHandler(error_handler)
    
    logger.info(f"[OK] Centralized logging configured for {app_name}")


# Instancias globales
_performance_monitor: Optional[PerformanceMonitor] = None


def get_performance_monitor() -> PerformanceMonitor:
    """Obtiene instancia global del monitor de performance"""
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor()
    return _performance_monitor


if __name__ == "__main__":
    print("\n🧪 TEST: Structured Logging & Audit Trail\n")
    
    setup_centralized_logging("BotAnalyst", "DEBUG")
    
    # Test 1: AuditLogger
    print("1️⃣  Test AuditLogger:")
    audit = AuditLogger("market_data")
    audit.log_data_fetch("AAPL", "yfinance", "success", records=1000, duration_ms=234.5)
    audit.log_analysis_result("AAPL", "technical", confidence=0.87, findings=5, duration_ms=512.3)
    audit.log_error_event("API_ERROR", "Connection timeout", severity="warning")
    audit.log_security_event("API_KEY_ACCESS", "Credential validated")
    
    # Test 2: PerformanceMonitor
    print("\n2️⃣  Test PerformanceMonitor:")
    perf = get_performance_monitor()
    perf.record_operation("fetch_price", 125.5)
    perf.record_operation("fetch_price", 150.3)
    perf.record_operation("fetch_price", 100.2)
    perf.record_operation("analyze_sentiment", 1250.5)
    
    stats = perf.get_stats("fetch_price")
    print(f"Performance stats (fetch_price): {stats}")
    
    perf.log_performance_report()
    
    print("\n✅ Structured logging funcional\n")
