#!/usr/bin/env python3
"""
test_imports.py
Verifica que todos los imports principales funcionan
"""

import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    """Prueba todos los imports críticos"""
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Data sources
    try:
        from data_sources.macroeconomic_data import MacroeconomicDataManager
        logger.info("✅ MacroeconomicDataManager")
        tests_passed += 1
    except Exception as e:
        logger.error(f"❌ MacroeconomicDataManager: {e}")
        tests_failed += 1
    
    # Test 2: Analysis modules
    try:
        from analisis.analyzer import Analyzer
        logger.info("✅ Analyzer")
        tests_passed += 1
    except Exception as e:
        logger.error(f"❌ Analyzer: {e}")
        tests_failed += 1
    
    # Test 3: Enhanced Analyzer
    try:
        from analisis.enhanced_analyzer import EnhancedAnalyzer
        logger.info("✅ EnhancedAnalyzer")
        tests_passed += 1
    except Exception as e:
        logger.error(f"❌ EnhancedAnalyzer: {e}")
        tests_failed += 1
    
    # Test 4: ML Predictor
    try:
        from analisis.ml_predictor import MLPredictor
        logger.info("✅ MLPredictor")
        tests_passed += 1
    except Exception as e:
        logger.error(f"❌ MLPredictor: {e}")
        tests_failed += 1
    
    # Test 5: Correlation Analyzer
    try:
        from analisis.correlation_analyzer import CorrelationAnalyzer
        logger.info("✅ CorrelationAnalyzer")
        tests_passed += 1
    except Exception as e:
        logger.error(f"❌ CorrelationAnalyzer: {e}")
        tests_failed += 1
    
    # Test 6: AI Engine
    try:
        from ia.ai_engine import AIEngine
        logger.info("✅ AIEngine")
        tests_passed += 1
    except Exception as e:
        logger.error(f"❌ AIEngine: {e}")
        tests_failed += 1
    
    # Test 7: Telegram Bot
    try:
        from telegram_bot.bot import TelegramAnalystBot
        logger.info("✅ TelegramAnalystBot")
        tests_passed += 1
    except Exception as e:
        logger.error(f"❌ TelegramAnalystBot: {e}")
        tests_failed += 1
    
    # Test 8: Knowledge Manager
    try:
        from cerebro.knowledge_manager import KnowledgeManager
        logger.info("✅ KnowledgeManager")
        tests_passed += 1
    except Exception as e:
        logger.error(f"❌ KnowledgeManager: {e}")
        tests_failed += 1
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info(f"✅ PASSED: {tests_passed}")
    logger.info(f"❌ FAILED: {tests_failed}")
    logger.info("="*50)
    
    return tests_failed == 0

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
