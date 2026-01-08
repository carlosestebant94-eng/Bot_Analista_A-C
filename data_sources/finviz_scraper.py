"""
data_sources/finviz_scraper.py
Scraper de datos desde Finviz para Factor Social enrichment
Extrae: insider trading, analyst ratings, sentiment scores
"""

import logging
from typing import Dict, Optional, Any, List
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time
import random

try:
    from finviz.screener import Screener
    from finviz.quote import Quote
    FINVIZ_AVAILABLE = True
except ImportError:
    FINVIZ_AVAILABLE = False


class FinvizScraper:
    """Extractor de datos de Finviz para análisis fundamental enriquecido"""
    
    # LISTA DE USER-AGENTS PARA ROTACIÓN
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0'
    ]
    
    def __init__(self):
        """Inicializa el scraper de Finviz"""
        self.logger = logging.getLogger("FinvizScraper")
        self.base_url = "https://finviz.com/quote.ashx"
        self.request_delay = 2  # Delay entre requests (segundos)
        self.request_count = 0
        
        if not FINVIZ_AVAILABLE:
            self.logger.info("[OK] Usando web scraping para datos de Finviz")
    
    def obtener_datos_completos(self, ticker: str) -> Dict[str, Any]:
        """
        Obtiene datos completos de Finviz para un ticker
        
        Args:
            ticker: Símbolo del instrumento (AAPL, MSFT, etc)
        
        Returns:
            Dict con: insider_trading, analyst_ratings, sentiment, technical_scores
        """
        try:
            resultado = {
                "ticker": ticker,
                "timestamp": datetime.now().isoformat(),
                "insider_trading": {},
                "analyst_ratings": {},
                "sentiment": {},
                "technical": {},
                "disponibilidad": {}
            }
            
            # Intenta obtener datos de Finviz
            if FINVIZ_AVAILABLE:
                try:
                    resultado.update(self._obtener_datos_finviz_api(ticker))
                    resultado["disponibilidad"]["finviz_api"] = True
                except Exception as e:
                    self.logger.warning(f"⚠️  Error con API Finviz: {str(e)}, intentando web scraping...")
                    resultado["disponibilidad"]["finviz_api"] = False
            
            # Si falla API, intenta web scraping
            if not resultado.get("insider_trading"):
                try:
                    resultado.update(self._scrapear_finviz_web(ticker))
                    resultado["disponibilidad"]["web_scraping"] = True
                except Exception as e:
                    self.logger.error(f"❌ Error scrapeando Finviz: {str(e)}")
                    resultado["disponibilidad"]["web_scraping"] = False
            
            return resultado
            
        except Exception as e:
            self.logger.error(f"❌ Error obteniendo datos de Finviz para {ticker}: {str(e)}")
            return {
                "ticker": ticker,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _obtener_datos_finviz_api(self, ticker: str) -> Dict[str, Any]:
        """
        Obtiene datos usando la API de Finviz (si está disponible)
        
        Args:
            ticker: Símbolo del instrumento
        
        Returns:
            Dict con datos de Finviz
        """
        try:
            quote = Quote(ticker)
            
            # Extrae insider trading
            insider_trading = {
                "transacciones": quote.get_stats().get("Insider Transactions", "N/A"),
                "posesion_insider": quote.get_stats().get("Insider Ownership", "N/A"),
                "transacciones_institucionales": quote.get_stats().get("Institutional Ownership", "N/A"),
                "flotante_corto": quote.get_stats().get("Short Float", "N/A")
            }
            
            # Extrae ratings de analistas
            analyst_ratings = {
                "rating_promedio": quote.get_stats().get("Target Price", "N/A"),
                "numero_analistas": quote.get_stats().get("Recommendation", "N/A"),
                "precio_objetivo": quote.get_stats().get("Target Price", "N/A")
            }
            
            # Extrae scores técnicos
            technical = {
                "rsi": quote.get_stats().get("RSI (14)", "N/A"),
                "movimiento_promedio": quote.get_stats().get("20 Day MA", "N/A"),
                "distancia_a_media": quote.get_stats().get("Distance to 52W H", "N/A")
            }
            
            return {
                "insider_trading": insider_trading,
                "analyst_ratings": analyst_ratings,
                "technical": technical
            }
            
        except Exception as e:
            self.logger.error(f"Error con API Finviz: {str(e)}")
            raise
    
    def _scrapear_finviz_web(self, ticker: str) -> Dict[str, Any]:
        """
        Scraper web de Finviz como fallback
        
        Args:
            ticker: Símbolo del instrumento
        
        Returns:
            Dict con datos scrapeados
        """
        try:
            url = f"{self.base_url}?t={ticker}"
            
            # ROTAR USER-AGENT PARA EVITAR BLOQUEOS
            user_agent = random.choice(self.USER_AGENTS)
            headers = {
                'User-Agent': user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://finviz.com'
            }
            
            # APLICAR DELAY ANTES DE REQUEST
            self.request_count += 1
            if self.request_count > 1:
                delay = self.request_delay + random.uniform(0, 1)  # +random para evitar patrón
                time.sleep(delay)
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extrae datos de las tablas de Finviz
            resultado = {
                "insider_trading": self._extraer_insider_trading(soup),
                "analyst_ratings": self._extraer_analyst_ratings(soup),
                "sentiment": self._extraer_sentiment(soup),
                "technical": self._extraer_technical(soup)
            }
            
            self.logger.info(f"✅ Datos de Finviz scrapeados para {ticker}")
            return resultado
            
        except Exception as e:
            self.logger.error(f"❌ Error scrapeando {ticker}: {str(e)}")
            raise
    
    def _extraer_insider_trading(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extrae datos de insider trading de la página"""
        try:
            insider_data = {}
            
            # Busca la tabla de insider transactions
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        label = cells[0].get_text(strip=True).lower()
                        value = cells[1].get_text(strip=True)
                        
                        if "insider" in label or "float" in label or "institutional" in label:
                            insider_data[label] = value
            
            return insider_data
            
        except Exception as e:
            self.logger.warning(f"⚠️  Error extrayendo insider trading: {str(e)}")
            return {}
    
    def _extraer_analyst_ratings(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extrae ratings de analistas"""
        try:
            analyst_data = {}
            
            # Busca sección de ratings de analistas
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        label = cells[0].get_text(strip=True).lower()
                        value = cells[1].get_text(strip=True)
                        
                        if "target" in label or "rating" in label or "estimate" in label:
                            analyst_data[label] = value
            
            return analyst_data
            
        except Exception as e:
            self.logger.warning(f"⚠️  Error extrayendo analyst ratings: {str(e)}")
            return {}
    
    def _extraer_sentiment(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extrae sentimiento y puntuación técnica"""
        try:
            sentiment_data = {}
            
            # Busca indicadores de sentimiento
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        label = cells[0].get_text(strip=True).lower()
                        value = cells[1].get_text(strip=True)
                        
                        if "sentiment" in label or "news" in label or "score" in label:
                            sentiment_data[label] = value
            
            return sentiment_data
            
        except Exception as e:
            self.logger.warning(f"⚠️  Error extrayendo sentiment: {str(e)}")
            return {}
    
    def _extraer_technical(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extrae scores técnicos"""
        try:
            technical_data = {}
            
            # Busca indicadores técnicos (RSI, promedios móviles, etc)
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        label = cells[0].get_text(strip=True).lower()
                        value = cells[1].get_text(strip=True)
                        
                        if "rsi" in label or "ma" in label or "distance" in label:
                            technical_data[label] = value
            
            return technical_data
            
        except Exception as e:
            self.logger.warning(f"⚠️  Error extrayendo technical: {str(e)}")
            return {}
    
    def obtener_insider_summary(self, ticker: str) -> Dict[str, str]:
        """
        Resumen simplificado de insider trading para análisis
        
        Args:
            ticker: Símbolo del instrumento
        
        Returns:
            Dict con: posicion_insider, tendencia_insiders, confianza
        """
        try:
            datos = self.obtener_datos_completos(ticker)
            insider = datos.get("insider_trading", {})
            
            # Calcula resumen
            resumen = {
                "ticker": ticker,
                "posicion_insider": self._evaluar_posicion(insider),
                "tendencia_insiders": self._evaluar_tendencia(insider),
                "confianza": "MODERADA" if insider else "BAJA",
                "datos_disponibles": bool(insider)
            }
            
            return resumen
            
        except Exception as e:
            self.logger.error(f"❌ Error obteniendo insider summary: {str(e)}")
            return {
                "ticker": ticker,
                "posicion_insider": "DESCONOCIDA",
                "tendencia_insiders": "NEUTRAL",
                "confianza": "BAJA",
                "error": str(e)
            }
    
    def _evaluar_posicion(self, insider_data: Dict) -> str:
        """Evalúa la posición insider basado en datos"""
        if not insider_data:
            return "DESCONOCIDA"
        
        # Lógica simple de evaluación
        return "POSITIVA" if any("buy" in str(v).lower() for v in insider_data.values()) else "NEUTRAL"
    
    def _evaluar_tendencia(self, insider_data: Dict) -> str:
        """Evalúa la tendencia de insiders"""
        if not insider_data:
            return "NEUTRAL"
        
        # Lógica simple de tendencia
        return "ALCISTA" if any("buy" in str(v).lower() for v in insider_data.values()) else "BAJISTA"
    
    def get_status(self) -> Dict[str, str]:
        """Obtiene estado del scraper"""
        return {
            "nombre": "FinvizScraper",
            "finviz_disponible": "✅" if FINVIZ_AVAILABLE else "⚠️ Web Scraping",
            "web_scraping": "✅ Disponible",
            "insider_trading": "✅ Soportado",
            "analyst_ratings": "✅ Soportado",
            "sentiment": "✅ Soportado",
            "estado": "Operativo"
        }
