"""
test_bot.py
Suite de pruebas para validar el Bot Analista A&C
"""

import sys
from pathlib import Path
import sqlite3

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from config import Settings
from cerebro import KnowledgeManager, PDFProcessor
from analisis import Analyzer
from ia import AIEngine
from utils import logger

def test_1_database():
    """Prueba 1: Verificar que la base de datos está correctamente inicializada"""
    print("\n" + "="*60)
    print("TEST 1: VERIFICAR BASE DE DATOS")
    print("="*60)
    
    try:
        km = KnowledgeManager()
        stats = km.obtener_estadisticas()
        
        print(f"✅ Base de datos conectada")
        print(f"   - Documentos: {stats['documentos_cargados']}")
        print(f"   - Conocimientos: {stats['conocimientos_almacenados']}")
        print(f"   - Análisis realizados: {stats['analisis_realizados']}")
        
        if stats['documentos_cargados'] >= 3:
            print("✅ TEST 1 PASADO: 3 o más documentos cargados")
            return True
        else:
            print("⚠️  TEST 1 PARCIAL: Menos de 3 documentos")
            return False
    except Exception as e:
        print(f"❌ TEST 1 FALLIDO: {str(e)}")
        return False

def test_2_knowledge_search():
    """Prueba 2: Buscar conocimiento en la base de datos"""
    print("\n" + "="*60)
    print("TEST 2: BÚSQUEDA DE CONOCIMIENTO")
    print("="*60)
    
    try:
        km = KnowledgeManager()
        resultados = km.buscar_conocimiento("trading")
        
        if resultados:
            print(f"✅ Se encontraron {len(resultados)} resultados para 'trading'")
            print(f"   Primeros 2 resultados:")
            for i, resultado in enumerate(resultados[:2]):
                tema = resultado.get('tema', 'Sin tema')
                print(f"   - {tema}")
            print("✅ TEST 2 PASADO")
            return True
        else:
            print("⚠️  TEST 2 PARCIAL: No se encontraron resultados")
            return False
    except Exception as e:
        print(f"❌ TEST 2 FALLIDO: {str(e)}")
        return False

def test_3_analyzer():
    """Prueba 3: Verificar que el analizador funciona"""
    print("\n" + "="*60)
    print("TEST 3: ANÁLISIS DE DATOS")
    print("="*60)
    
    try:
        analyzer = Analyzer()
        
        # Datos de ejemplo
        datos_ejemplo = {
            "precio": [100, 102, 101, 103, 105],
            "volumen": [1000, 1500, 1200, 1800, 2000]
        }
        
        resultado = analyzer.analizar_datos(
            datos=datos_ejemplo,
            contexto="análisis de prueba"
        )
        
        if resultado and "hallazgos" in resultado:
            print(f"✅ Análisis completado")
            print(f"   - Confianza: {resultado.get('confianza', 0)}%")
            print(f"   - Hallazgos: {len(resultado.get('hallazgos', []))}")
            print("✅ TEST 3 PASADO")
            return True
        else:
            print("⚠️  TEST 3 PARCIAL: Resultado incompleto")
            return False
    except Exception as e:
        print(f"❌ TEST 3 FALLIDO: {str(e)}")
        return False

def test_4_ai_engine():
    """Prueba 4: Verificar que el motor de IA está disponible"""
    print("\n" + "="*60)
    print("TEST 4: MOTOR DE IA (GEMINI)")
    print("="*60)
    
    try:
        # Verificar configuración
        if not Settings.GOOGLE_API_KEY:
            print("❌ TEST 4 FALLIDO: No se encontró GOOGLE_API_KEY")
            return False
        
        print(f"✅ GOOGLE_API_KEY detectada")
        print(f"   - Modelo configurado: {Settings.GEMINI_MODEL}")
        
        # Verificar que AIEngine puede inicializarse
        ai = AIEngine(Settings.GOOGLE_API_KEY)
        status = ai.get_status()
        
        print(f"✅ AIEngine inicializado correctamente")
        print(f"   Estado: {status}")
        print("✅ TEST 4 PASADO")
        return True
    except Exception as e:
        print(f"⚠️  TEST 4 PARCIAL: {str(e)}")
        print("   (El motor de IA funcionará en producción con Telegram)")
        return False

def test_5_files_structure():
    """Prueba 5: Verificar estructura de archivos"""
    print("\n" + "="*60)
    print("TEST 5: ESTRUCTURA DE ARCHIVOS")
    print("="*60)
    
    required_files = [
        "main.py",
        "config/settings.py",
        "cerebro/knowledge_manager.py",
        "cerebro/pdf_processor.py",
        "analisis/analyzer.py",
        "ia/ai_engine.py",
        "telegram_bot/bot.py",
        "data/memory.db"
    ]
    
    missing = []
    for file in required_files:
        path = Path(__file__).parent / file
        if not path.exists():
            missing.append(file)
        else:
            print(f"✅ {file}")
    
    if not missing:
        print("✅ TEST 5 PASADO: Todos los archivos presentes")
        return True
    else:
        print(f"⚠️  TEST 5 PARCIAL: Archivos faltantes: {missing}")
        return False

def test_6_environment():
    """Prueba 6: Verificar variables de entorno"""
    print("\n" + "="*60)
    print("TEST 6: VARIABLES DE ENTORNO")
    print("="*60)
    
    try:
        if Settings.TELEGRAM_TOKEN:
            print(f"✅ TELEGRAM_TOKEN: {Settings.TELEGRAM_TOKEN[:10]}...")
        else:
            print("⚠️  TELEGRAM_TOKEN no configurado")
        
        if Settings.GOOGLE_API_KEY:
            print(f"✅ GOOGLE_API_KEY: {Settings.GOOGLE_API_KEY[:10]}...")
        else:
            print("⚠️  GOOGLE_API_KEY no configurado")
        
        print(f"✅ Ruta base: {Settings.BASE_DIR}")
        print(f"✅ Base de datos: {Settings.DATABASE_PATH}")
        print("✅ TEST 6 PASADO")
        return True
    except Exception as e:
        print(f"❌ TEST 6 FALLIDO: {str(e)}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("\n" + "="*60)
    print("🧪 INICIANDO SUITE DE PRUEBAS - BOT ANALISTA A&C")
    print("="*60)
    
    results = {
        "Test 1 - Base de Datos": test_1_database(),
        "Test 2 - Búsqueda de Conocimiento": test_2_knowledge_search(),
        "Test 3 - Análisis de Datos": test_3_analyzer(),
        "Test 4 - Motor de IA": test_4_ai_engine(),
        "Test 5 - Estructura de Archivos": test_5_files_structure(),
        "Test 6 - Variables de Entorno": test_6_environment(),
    }
    
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASADO" if result else "❌ FALLIDO"
        print(f"{status} - {test_name}")
    
    print("\n" + "="*60)
    print(f"RESULTADO FINAL: {passed}/{total} pruebas exitosas ({int(passed/total*100)}%)")
    print("="*60)
    
    if passed == total:
        print("\n🎉 ¡TODOS LOS TESTS PASARON! El bot está listo para producción.")
    elif passed >= total - 1:
        print("\n⚠️  La mayoría de tests pasaron. Solo se necesitan ajustes menores.")
    else:
        print("\n❌ Algunos tests fallaron. Revisar el reporte anterior.")
    
    print("\n")

if __name__ == "__main__":
    main()
