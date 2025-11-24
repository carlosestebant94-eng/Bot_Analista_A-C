#!/usr/bin/env python
"""
Script para cargar PDFs al cerebro del bot
Ejecutar: python cargar_libros.py
"""

from cerebro import KnowledgeManager, PDFProcessor
from config import Settings

def main():
    """Carga todos los PDFs de la carpeta pdfs/ al cerebro"""
    
    # Crear directorios
    Settings.crear_directorios()
    Settings.mostrar_configuracion()
    
    # Inicializar procesadores
    print("\n" + "="*60)
    print("📚 CARGANDO PDFs AL CEREBRO DEL BOT")
    print("="*60 + "\n")
    
    pdf_processor = PDFProcessor(str(Settings.PDFS_DIR))
    knowledge_manager = KnowledgeManager(str(Settings.DATABASE_PATH))
    
    # Procesar todos los PDFs
    documentos = pdf_processor.procesar_todos_pdfs()
    
    if not documentos:
        print("❌ No se encontraron PDFs en la carpeta pdfs/")
        return
    
    print(f"📖 Se encontraron {len(documentos)} PDF(s)\n")
    
    # Cargar cada documento
    for i, doc in enumerate(documentos, 1):
        print(f"{i}. ✅ Procesando: {doc['nombre']}")
        print(f"   - Páginas: {doc['total_paginas']}")
        print(f"   - Tamaño: {len(doc['texto_completo'])} caracteres")
        
        # Cargar documento en BD
        knowledge_manager.cargar_documento(
            nombre=doc["nombre"],
            ruta=doc["ruta"],
            tipo="pdf",
            contenido=doc["texto_completo"]
        )
        
        # Agregar como conocimiento
        knowledge_manager.agregar_conocimiento(
            tema=f"Contenido: {doc['nombre']}",
            contenido=doc["texto_completo"],
            relevancia=0.95
        )
        print()
    
    # Mostrar estadísticas
    stats = knowledge_manager.obtener_estadisticas()
    
    print("="*60)
    print("✅ CARGA COMPLETADA CON ÉXITO")
    print("="*60)
    print(f"📄 Documentos cargados:      {stats['documentos_cargados']}")
    print(f"🧠 Conocimientos almacenados: {stats['conocimientos_almacenados']}")
    print(f"📊 Confianza promedio:       {stats['confianza_promedio']:.0%}")
    print("="*60)
    print("\n🎉 ¡Tu cerebro está entrenado!")
    print("Ahora puedes:")
    print("  1. Ejecutar: python main.py")
    print("  2. En Telegram: /start")
    print("  3. Usar: /analizar para hacer análisis")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
