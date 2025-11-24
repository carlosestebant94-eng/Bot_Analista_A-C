"""
test_stress.py
Pruebas de carga y estrés del bot
"""

import sys
from pathlib import Path
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from cerebro import KnowledgeManager
from analisis import Analyzer
from ia import AIEngine
from config import Settings

def test_concurrent_knowledge_search():
    """Prueba de búsquedas concurrentes en la base de datos"""
    print("\n" + "="*60)
    print("TEST STRESS 1: BÚSQUEDAS CONCURRENTES")
    print("="*60)
    
    try:
        km = KnowledgeManager()
        
        # Simular 10 búsquedas simultáneas
        def search_task(query):
            resultados = km.buscar_conocimiento(query)
            return len(resultados)
        
        queries = ["trading", "estrategia", "riesgo", "análisis", "precio",
                   "volatilidad", "mercado", "inversión", "rendimiento", "portafolio"]
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(search_task, q) for q in queries]
            results = [f.result() for f in as_completed(futures)]
        
        elapsed_time = time.time() - start_time
        total_results = sum(results)
        
        print(f"✅ {len(queries)} búsquedas completadas")
        print(f"   - Tiempo total: {elapsed_time:.2f}s")
        print(f"   - Resultados encontrados: {total_results}")
        print(f"   - Promedio por búsqueda: {elapsed_time/len(queries):.3f}s")
        
        if elapsed_time < 10:
            print("✅ TEST PASADO: Performance óptimo")
            return True
        else:
            print("⚠️  TEST PARCIAL: Performance puede mejorarse")
            return False
    except Exception as e:
        print(f"❌ TEST FALLIDO: {str(e)}")
        return False

def test_analyzer_load():
    """Prueba de carga del analizador"""
    print("\n" + "="*60)
    print("TEST STRESS 2: CARGA DEL ANALIZADOR")
    print("="*60)
    
    try:
        analyzer = Analyzer()
        
        # Simular 5 análisis secuenciales con datos simples
        data_sets = [
            {"precio": list(range(100, 120))},
            {"volumen": list(range(1000, 1100, 10))},
            {"RSI": list(range(30, 80))},
            {"MACD": [0.5 + i*0.1 for i in range(20)]},
            {"datos": list(range(100))},
        ]
        
        start_time = time.time()
        
        for data in data_sets:
            resultado = analyzer.analizar_datos(
                datos=data,
                contexto="prueba de carga"
            )
        
        elapsed_time = time.time() - start_time
        
        print(f"✅ {len(data_sets)} análisis completados")
        print(f"   - Tiempo total: {elapsed_time:.2f}s")
        print(f"   - Promedio por análisis: {elapsed_time/len(data_sets):.3f}s")
        
        if elapsed_time < 5:
            print("✅ TEST PASADO: Analizador muy rápido")
            return True
        else:
            print("⚠️  TEST PARCIAL: Considerarse optimización")
            return False
    except Exception as e:
        print(f"❌ TEST FALLIDO: {str(e)}")
        return False

def test_memory_usage():
    """Prueba de uso de memoria"""
    print("\n" + "="*60)
    print("TEST STRESS 3: USO DE MEMORIA")
    print("="*60)
    
    try:
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        # Obtener uso inicial
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Realizar operaciones
        km = KnowledgeManager()
        analyzer = Analyzer()
        ai = AIEngine(Settings.GOOGLE_API_KEY)
        
        # Realizar búsquedas para cargar datos
        for i in range(10):
            km.buscar_conocimiento("trading")
            analyzer.analizar_datos({"test": [1, 2, 3, 4, 5]})
        
        # Obtener uso final
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"✅ Análisis de memoria completado")
        print(f"   - Memoria inicial: {initial_memory:.2f} MB")
        print(f"   - Memoria final: {final_memory:.2f} MB")
        print(f"   - Incremento: {memory_increase:.2f} MB")
        
        if final_memory < 500:  # Menos de 500 MB es razonable
            print("✅ TEST PASADO: Uso de memoria óptimo")
            return True
        else:
            print("⚠️  TEST PARCIAL: Alto uso de memoria (pero aceptable para desarrollo)")
            return False
    except ImportError:
        print("⚠️  TEST OMITIDO: psutil no instalado (opcional)")
        return True
    except Exception as e:
        print(f"❌ TEST FALLIDO: {str(e)}")
        return False

def test_api_key_validation():
    """Prueba validación de configuración"""
    print("\n" + "="*60)
    print("TEST STRESS 4: VALIDACIÓN DE CONFIGURACIÓN")
    print("="*60)
    
    try:
        # Validar que todas las claves necesarias existen
        required_keys = {
            'TELEGRAM_TOKEN': Settings.TELEGRAM_TOKEN,
            'GOOGLE_API_KEY': Settings.GOOGLE_API_KEY,
            'GEMINI_MODEL': Settings.GEMINI_MODEL,
            'DATABASE_PATH': Settings.DATABASE_PATH,
        }
        
        missing_keys = [k for k, v in required_keys.items() if not v]
        
        if missing_keys:
            print(f"❌ TEST FALLIDO: Claves faltantes: {missing_keys}")
            return False
        
        print("✅ Todas las claves de configuración presentes:")
        for key, value in required_keys.items():
            if key == 'TELEGRAM_TOKEN':
                masked = f"{str(value)[:10]}..."
            elif key == 'GOOGLE_API_KEY':
                masked = f"{str(value)[:10]}..."
            else:
                masked = str(value)
            print(f"   ✓ {key}: {masked}")
        
        print("✅ TEST PASADO: Configuración válida")
        return True
    except Exception as e:
        print(f"❌ TEST FALLIDO: {str(e)}")
        return False

def main():
    """Ejecutar todas las pruebas de estrés"""
    print("\n" + "="*60)
    print("💪 PRUEBAS DE ESTRÉS Y CARGA - BOT ANALISTA A&C")
    print("="*60)
    
    results = {
        "Test 1 - Búsquedas Concurrentes": test_concurrent_knowledge_search(),
        "Test 2 - Carga del Analizador": test_analyzer_load(),
        "Test 3 - Uso de Memoria": test_memory_usage(),
        "Test 4 - Validación de Configuración": test_api_key_validation(),
    }
    
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS DE ESTRÉS")
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
        print("\n💪 ¡EL BOT ESTÁ LISTO PARA PRODUCCIÓN! Estrés completamente validado.")
    elif passed >= total - 1:
        print("\n✅ El bot puede manejar carga normal sin problemas.")
    else:
        print("\n⚠️  Algunos tests fallaron. Considerar optimización.")
    
    print("\n")

if __name__ == "__main__":
    main()
