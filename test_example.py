"""
test_example.py
Script de prueba y demostración del sistema
Ejecuta pruebas sin necesidad de Telegram
"""

import sys
from pathlib import Path
import json

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from config import Settings
from cerebro import KnowledgeManager, PDFProcessor
from analisis import Analyzer, ImageProcessor
from utils import setup_logger


def test_cerebro():
    """Prueba el módulo del cerebro"""
    print("\n" + "=" * 60)
    print("🧠 PRUEBA DEL MÓDULO CEREBRO")
    print("=" * 60)
    
    # Inicializar
    km = KnowledgeManager()
    logger = setup_logger("TestCerebro")
    
    # Cargar conocimiento
    print("➕ Cargando conocimiento de prueba...")
    km.cargar_documento(
        nombre="doc_prueba.pdf",
        ruta="pdfs/doc_prueba.pdf",
        tipo="pdf",
        contenido="Contenido de prueba sobre análisis financiero"
    )
    
    km.agregar_conocimiento(
        tema="Análisis técnico",
        contenido="El análisis técnico es el estudio de precios históricos y volumen",
        relevancia=0.95
    )
    
    km.agregar_conocimiento(
        tema="Volatilidad",
        contenido="La volatilidad mide la variabilidad de precios",
        relevancia=0.90
    )
    
    print("✅ Documentos y conocimiento cargados")
    
    # Buscar
    print("\n🔍 Buscando conocimiento sobre 'análisis'...")
    resultados = km.buscar_conocimiento("análisis", limite=5)
    for res in resultados:
        print(f"  • {res['tema']}: {res['contenido'][:50]}...")
    
    # Estadísticas
    print("\n📊 Estadísticas:")
    stats = km.obtener_estadisticas()
    for clave, valor in stats.items():
        print(f"  • {clave}: {valor}")
    
    print("✅ Prueba del cerebro completada\n")


def test_analisis():
    """Prueba el módulo de análisis"""
    print("\n" + "=" * 60)
    print("📊 PRUEBA DEL MÓDULO DE ANÁLISIS")
    print("=" * 60)
    
    # Inicializar
    km = KnowledgeManager()
    analyzer = Analyzer(km)
    
    # Datos de prueba
    datos_prueba = {
        "tendencia": "al_alza",
        "volatilidad": 0.15,
        "valores": [100, 105, 110, 108, 115, 120]
    }
    
    print("📈 Analizando datos:")
    print(json.dumps(datos_prueba, indent=2))
    
    # Realizar análisis
    resultado = analyzer.analizar_datos(datos_prueba, contexto="Análisis de tendencia")
    
    print("\n📊 Resultado del análisis:")
    print(f"  Tipo: {resultado['tipo_analisis']}")
    print(f"  Confianza: {resultado['confianza']:.0%}")
    print(f"  Hallazgos:")
    for h in resultado['hallazgos']:
        print(f"    • {h}")
    print(f"  Recomendaciones:")
    for r in resultado['recomendaciones']:
        print(f"    • {r}")
    
    # Análisis comparativo
    print("\n🔄 Realizando análisis comparativo...")
    activo1 = {"valores": [100, 105, 110, 115, 120]}
    activo2 = {"valores": [50, 48, 45, 42, 40]}
    
    comparacion = analyzer.analizar_comparativa(activo1, activo2)
    print(f"  Diferencia: {comparacion['comparacion'].get('diferencia_porcentual', 0):.2f}%")
    print(f"  Recomendación: {comparacion['recomendacion']}")
    
    # Reporte
    print("\n📋 Reporte general:")
    reporte = analyzer.generar_reporte()
    for clave, valor in reporte.items():
        print(f"  • {clave}: {valor}")
    
    print("✅ Prueba de análisis completada\n")


def test_pdf_processor():
    """Prueba el procesador de PDFs"""
    print("\n" + "=" * 60)
    print("📄 PRUEBA DEL PROCESADOR DE PDFs")
    print("=" * 60)
    
    processor = PDFProcessor(str(Settings.PDFS_DIR))
    
    print(f"📁 Buscando PDFs en: {Settings.PDFS_DIR}")
    documentos = processor.procesar_todos_pdfs()
    
    if documentos:
        print(f"✅ Se encontraron {len(documentos)} PDF(s)")
        for doc in documentos:
            print(f"  • {doc['nombre']}: {doc['total_paginas']} páginas")
            texto_preview = doc['texto_completo'][:50].replace('\n', ' ')
            print(f"    Contenido: {texto_preview}...")
    else:
        print("⚠️  No se encontraron PDFs en la carpeta")
        print("   Coloca tus PDFs en la carpeta 'pdfs/' para entrenar el cerebro del bot")
    
    print("✅ Prueba de procesador completada\n")


def test_image_processor():
    """Prueba el procesador de imágenes"""
    print("\n" + "=" * 60)
    print("🖼️  PRUEBA DEL PROCESADOR DE IMÁGENES")
    print("=" * 60)
    
    processor = ImageProcessor()
    
    print("⚠️  No hay imágenes de prueba incluidas")
    print("   Coloca imágenes en el proyecto para probar el análisis visual")
    print("   El procesador puede:")
    print("   • Extraer texto usando OCR")
    print("   • Detectar formas geométricas")
    print("   • Identificar tipos de gráficos")
    print("   • Analizar distribución de colores")
    
    print("✅ Prueba de procesador de imágenes completada\n")


def mostrar_estructura():
    """Muestra la estructura del proyecto"""
    print("\n" + "=" * 60)
    print("📁 ESTRUCTURA DEL PROYECTO")
    print("=" * 60)
    
    directorio_base = Path(__file__).parent
    
    for item in sorted(directorio_base.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            print(f"\n📂 {item.name}/")
            for archivo in sorted(item.iterdir()):
                if archivo.is_file() and not archivo.name.startswith('__'):
                    print(f"   📄 {archivo.name}")
        elif item.is_file() and not item.name.startswith('.'):
            print(f"📄 {item.name}")


def main():
    """Función principal de pruebas"""
    
    print("\n" + "=" * 60)
    print("🤖 BOT ANALISTA A&C - SCRIPT DE PRUEBAS")
    print("=" * 60)
    
    # Mostrar estructura
    mostrar_estructura()
    
    # Crear directorios
    print("\n📁 Creando directorios necesarios...")
    Settings.crear_directorios()
    Settings.mostrar_configuracion()
    
    # Ejecutar pruebas
    try:
        test_cerebro()
        test_analisis()
        test_pdf_processor()
        test_image_processor()
        
        print("\n" + "=" * 60)
        print("✅ TODAS LAS PRUEBAS COMPLETADAS")
        print("=" * 60)
        print("\n🚀 Próximos pasos:")
        print("1. Coloca tus PDFs en la carpeta 'pdfs/'")
        print("2. Configura tu token de Telegram en '.env'")
        print("3. Ejecuta: python main.py")
        print("\n" + "=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {str(e)}")
        raise


if __name__ == "__main__":
    main()
