#!/usr/bin/env python3
"""
Script para procesar PDFs y cargar en el cerebro
"""

from cerebro.pdf_processor import PDFProcessor
from cerebro.knowledge_manager import KnowledgeManager

def main():
    # Procesar PDFs
    print('📚 Procesando PDFs...')
    processor = PDFProcessor('pdfs')
    documentos = processor.procesar_todos_pdfs()

    print(f'✅ Se han procesado {len(documentos)} documentos PDF')
    for doc in documentos:
        print(f'   - {doc["nombre"]} ({doc["total_paginas"]} páginas)')

    # Guardar procesamiento
    processor.guardar_procesamiento()

    # Cargar en Knowledge Manager
    print('🧠 Cargando documentos en el cerebro...')
    manager = KnowledgeManager()
    manager.cargar_documentos_pdf(documentos)
    print('✅ Documentos cargados exitosamente en el cerebro')

if __name__ == "__main__":
    main()
