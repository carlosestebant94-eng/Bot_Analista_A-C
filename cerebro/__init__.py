"""
cerebro/__init__.py
Módulo del cerebro - Base de conocimiento del bot
"""
from .knowledge_manager import KnowledgeManager
from .pdf_processor import PDFProcessor

__all__ = ['KnowledgeManager', 'PDFProcessor']
