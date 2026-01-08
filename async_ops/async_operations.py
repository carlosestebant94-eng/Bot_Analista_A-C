"""
async_ops/async_operations.py
PUNTO 5: Operaciones asincrónicas para eliminar bloqueos
Convierte operaciones I/O a async/await para parallelizar
"""

import asyncio
import logging
from typing import List, Dict, Any, Callable, Optional, Coroutine
from concurrent.futures import ThreadPoolExecutor
import functools
from datetime import datetime

logger = logging.getLogger("AsyncOperations")


class AsyncDataBatcher:
    """
    Agrupa múltiples requests similares para reducir N+1 queries
    
    Ejemplo:
        batcher = AsyncDataBatcher(batch_size=10, batch_timeout=0.1)
        prices = await batcher.batch_fetch_prices(["AAPL", "MSFT", "GOOGL"])
    """
    
    def __init__(self, batch_size: int = 100, batch_timeout: float = 0.5):
        """
        Inicializa batcher
        
        Args:
            batch_size: Máximo tamaño de batch
            batch_timeout: Tiempo máximo de espera (segundos) antes de ejecutar
        """
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self.logger = logging.getLogger("AsyncDataBatcher")
        
        # Queues por tipo de operación
        self.price_queue: List[tuple] = []
        self.macro_queue: List[tuple] = []
        
        # Timers
        self.price_timer: Optional[asyncio.Task] = None
        self.macro_timer: Optional[asyncio.Task] = None
    
    async def batch_fetch_prices(self, tickers: List[str], 
                                 fetch_fn: Callable) -> Dict[str, Any]:
        """
        Agrupa requests de precios
        
        Args:
            tickers: Lista de tickers a obtener
            fetch_fn: Función async para obtener precios de múltiples tickers
            
        Returns:
            Dict mapping ticker -> price data
        """
        if not tickers:
            return {}
        
        try:
            self.logger.info(f"📦 Batcheando {len(tickers)} tickers")
            
            # Agrupar en lotes de batch_size
            batches = [tickers[i:i + self.batch_size] 
                      for i in range(0, len(tickers), self.batch_size)]
            
            # Ejecutar todos los lotes en paralelo
            tasks = [fetch_fn(batch) for batch in batches]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Combinar resultados
            combined = {}
            for result in results:
                if isinstance(result, dict):
                    combined.update(result)
                elif isinstance(result, Exception):
                    self.logger.error(f"❌ Error en batch: {str(result)}")
            
            self.logger.info(f"✅ Batcheo completado: {len(combined)} precios obtenidos")
            return combined
        
        except Exception as e:
            self.logger.error(f"❌ Error en batch_fetch_prices: {str(e)}")
            return {}
    
    async def batch_fetch_macro(self, indicators: List[str],
                               fetch_fn: Callable) -> Dict[str, Any]:
        """
        Agrupa requests de indicadores macroeconómicos
        
        Args:
            indicators: Lista de indicadores
            fetch_fn: Función async para obtener macros
            
        Returns:
            Dict mapping indicator -> macro data
        """
        if not indicators:
            return {}
        
        try:
            self.logger.info(f"📦 Batcheando {len(indicators)} indicadores macro")
            
            batches = [indicators[i:i + self.batch_size]
                      for i in range(0, len(indicators), self.batch_size)]
            
            tasks = [fetch_fn(batch) for batch in batches]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            combined = {}
            for result in results:
                if isinstance(result, dict):
                    combined.update(result)
                elif isinstance(result, Exception):
                    self.logger.error(f"❌ Error en batch: {str(result)}")
            
            self.logger.info(f"✅ Batcheo macro completado: {len(combined)} indicadores")
            return combined
        
        except Exception as e:
            self.logger.error(f"❌ Error en batch_fetch_macro: {str(e)}")
            return {}


class AsyncExecutor:
    """
    Ejecutor de tareas async seguro con timeouts y limpieza
    """
    
    def __init__(self, max_workers: int = 10, timeout_seconds: float = 30):
        """
        Inicializa executor
        
        Args:
            max_workers: Máximo de workers concurrentes
            timeout_seconds: Timeout global para operaciones
        """
        self.max_workers = max_workers
        self.timeout_seconds = timeout_seconds
        self.logger = logging.getLogger("AsyncExecutor")
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def run_concurrent(self, tasks: List[Coroutine],
                            timeout: Optional[float] = None) -> List[Any]:
        """
        Ejecuta múltiples tareas concurrentemente con timeout
        
        Args:
            tasks: Lista de coroutines
            timeout: Timeout en segundos (usa self.timeout_seconds si no se especifica)
            
        Returns:
            Lista de resultados (Exception si falló)
        """
        timeout = timeout or self.timeout_seconds
        
        try:
            self.logger.info(f"⚡ Ejecutando {len(tasks)} tareas concurrentes (timeout: {timeout}s)")
            results = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=timeout
            )
            
            success = sum(1 for r in results if not isinstance(r, Exception))
            self.logger.info(f"✅ {success}/{len(tasks)} tareas completadas")
            return results
        
        except asyncio.TimeoutError:
            self.logger.error(f"❌ Timeout alcanzado después de {timeout}s")
            return [asyncio.TimeoutError(f"Timeout {timeout}s")] * len(tasks)
        except Exception as e:
            self.logger.error(f"❌ Error en run_concurrent: {str(e)}")
            return [e] * len(tasks)
    
    async def run_with_retry(self, coro: Coroutine, max_retries: int = 3,
                            backoff_factor: float = 2.0) -> Any:
        """
        Ejecuta coroutine con retry exponencial
        
        Args:
            coro: Coroutine a ejecutar
            max_retries: Máximo reintentos
            backoff_factor: Factor de backoff exponencial
            
        Returns:
            Resultado o Exception si falló todos los reintentos
        """
        for attempt in range(max_retries):
            try:
                self.logger.debug(f"🔄 Intento {attempt + 1}/{max_retries}")
                return await asyncio.wait_for(coro, timeout=self.timeout_seconds)
            
            except asyncio.TimeoutError as e:
                if attempt < max_retries - 1:
                    wait_time = (backoff_factor ** attempt)
                    self.logger.warning(f"⏱️  Timeout, esperando {wait_time}s antes de reintentar")
                    await asyncio.sleep(wait_time)
                else:
                    self.logger.error(f"❌ Falló después de {max_retries} reintentos")
                    return e
            
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = (backoff_factor ** attempt)
                    self.logger.warning(f"⚠️  Error: {str(e)}, reintenando en {wait_time}s")
                    await asyncio.sleep(wait_time)
                else:
                    self.logger.error(f"❌ Error permanente después de {max_retries} reintentos")
                    return e
        
        return Exception("Max retries exceeded")
    
    def cleanup(self) -> None:
        """Limpia recursos"""
        self.executor.shutdown(wait=True)
        self.logger.info("🧹 AsyncExecutor limpiado")


def async_wrapper(func: Callable) -> Callable:
    """
    Decorador para convertir funciones síncronas a async
    Útil para I/O-bound operations
    
    Ejemplo:
        @async_wrapper
        def fetch_price(ticker):
            return yf.Ticker(ticker).info['currentPrice']
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))
    return wrapper


class AsyncPoolManager:
    """
    Administrador de pool de conexiones async reutilizables
    Evita crear nuevas conexiones para cada request
    """
    
    def __init__(self, pool_size: int = 5):
        """
        Inicializa pool manager
        
        Args:
            pool_size: Tamaño de pool
        """
        self.pool_size = pool_size
        self.logger = logging.getLogger("AsyncPoolManager")
        self.pools: Dict[str, List[Any]] = {}
    
    async def get_connection(self, pool_name: str,
                            factory: Callable) -> Any:
        """
        Obtiene conexión del pool o crea una nueva
        
        Args:
            pool_name: Nombre del pool
            factory: Función para crear nuevas conexiones
            
        Returns:
            Conexión del pool
        """
        if pool_name not in self.pools:
            self.pools[pool_name] = []
        
        pool = self.pools[pool_name]
        
        if pool:
            conn = pool.pop()
            self.logger.debug(f"♻️  Reutilizando conexión del pool {pool_name}")
            return conn
        
        if len([c for pools in self.pools.values() for c in pools]) < self.pool_size:
            conn = await factory()
            self.logger.debug(f"🆕 Creando nueva conexión para pool {pool_name}")
            return conn
        
        # Esperar a que se libere una conexión
        self.logger.warning(f"⏳ Pool {pool_name} lleno, esperando conexión disponible")
        while not pool:
            await asyncio.sleep(0.1)
        
        return pool.pop()
    
    async def return_connection(self, pool_name: str, connection: Any) -> None:
        """
        Devuelve conexión al pool
        
        Args:
            pool_name: Nombre del pool
            connection: Conexión a devolver
        """
        if pool_name not in self.pools:
            self.pools[pool_name] = []
        
        self.pools[pool_name].append(connection)
        self.logger.debug(f"✅ Conexión devuelta al pool {pool_name}")
    
    async def cleanup(self) -> None:
        """Limpia todos los pools"""
        for pool_name in self.pools:
            self.pools[pool_name].clear()
        self.logger.info("🧹 AsyncPoolManager limpiado")


# Instancia global del executor
_async_executor: Optional[AsyncExecutor] = None


def get_async_executor() -> AsyncExecutor:
    """Obtiene la instancia global del executor async"""
    global _async_executor
    if _async_executor is None:
        _async_executor = AsyncExecutor()
    return _async_executor


if __name__ == "__main__":
    import time
    
    logging.basicConfig(level=logging.INFO)
    
    async def test_async_ops():
        print("\n🧪 TEST: Operaciones Async\n")
        
        # Test 1: AsyncDataBatcher
        print("1️⃣  Test AsyncDataBatcher:")
        batcher = AsyncDataBatcher(batch_size=3)
        
        async def mock_fetch_prices(tickers):
            await asyncio.sleep(0.1)  # Simular I/O
            return {ticker: {"price": 100 + i} for i, ticker in enumerate(tickers)}
        
        prices = await batcher.batch_fetch_prices(
            ["AAPL", "MSFT", "GOOGL", "AMZN"],
            mock_fetch_prices
        )
        print(f"Precios: {prices}")
        
        # Test 2: AsyncExecutor
        print("\n2️⃣  Test AsyncExecutor:")
        executor = get_async_executor()
        
        async def task(i):
            await asyncio.sleep(0.1)
            return f"Resultado {i}"
        
        results = await executor.run_concurrent([task(i) for i in range(5)])
        print(f"Resultados: {results}")
        
        print("\n✅ Operaciones async funcionales\n")
    
    asyncio.run(test_async_ops())
