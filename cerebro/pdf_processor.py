"""
cerebro/pdf_processor.py
Procesador de documentos PDF
Extrae y estructura información de PDFs locales
"""

import pdfplumber
import os
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class PDFProcessor:
    """Procesa y extrae información de archivos PDF"""
    
    def __init__(self, pdfs_dir: str = "pdfs"):
        """
        Inicializa el procesador de PDF
        
        Args:
            pdfs_dir: Directorio donde están almacenados los PDFs
        """
        self.pdfs_dir = pdfs_dir
        self.processed_documents = {}
        
    def procesar_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Procesa un archivo PDF y extrae su contenido
        
        Args:
            pdf_path: Ruta del archivo PDF
            
        Returns:
            Diccionario con información procesada del PDF
        """
        try:
            documento = {
                "nombre": os.path.basename(pdf_path),
                "ruta": pdf_path,
                "fecha_procesamiento": datetime.now().isoformat(),
                "paginas": [],
                "metadatos": {},
                "texto_completo": ""
            }
            
            with pdfplumber.open(pdf_path) as pdf:
                documento["metadatos"] = pdf.metadata or {}
                documento["total_paginas"] = len(pdf.pages)
                
                for num_pagina, pagina in enumerate(pdf.pages, 1):
                    info_pagina = {
                        "numero": num_pagina,
                        "texto": pagina.extract_text() or "",
                        "tablas": pagina.extract_tables() or [],
                    }
                    documento["paginas"].append(info_pagina)
                    documento["texto_completo"] += info_pagina["texto"] + "\n"
            
            self.processed_documents[os.path.basename(pdf_path)] = documento
            return documento
            
        except Exception as e:
            print(f"Error procesando PDF {pdf_path}: {str(e)}")
            return None
    
    def procesar_todos_pdfs(self) -> List[Dict[str, Any]]:
        """
        Procesa todos los PDFs en el directorio
        
        Returns:
            Lista de documentos procesados
        """
        documentos = []
        
        if not os.path.exists(self.pdfs_dir):
            os.makedirs(self.pdfs_dir)
            print(f"Directorio {self.pdfs_dir} creado. Coloca tus PDFs aquí.")
            return documentos
        
        for archivo in os.listdir(self.pdfs_dir):
            if archivo.lower().endswith('.pdf'):
                ruta_completa = os.path.join(self.pdfs_dir, archivo)
                doc = self.procesar_pdf(ruta_completa)
                if doc:
                    documentos.append(doc)
        
        return documentos
    
    def extraer_texto_completo(self) -> str:
        """
        Extrae todo el texto procesado de los PDFs
        
        Returns:
            Texto concatenado de todos los PDFs
        """
        texto_completo = ""
        for doc in self.processed_documents.values():
            texto_completo += doc["texto_completo"] + "\n---\n"
        return texto_completo
    
    def buscar_en_documentos(self, termino: str) -> List[Dict]:
        """
        Busca un término en los documentos procesados
        
        Args:
            termino: Término a buscar
            
        Returns:
            Lista de resultados encontrados
        """
        resultados = []
        
        for nombre_doc, doc in self.processed_documents.items():
            for num_pag, pagina in enumerate(doc["paginas"], 1):
                if termino.lower() in pagina["texto"].lower():
                    resultados.append({
                        "documento": nombre_doc,
                        "pagina": num_pag,
                        "fragmento": pagina["texto"]
                    })
        
        return resultados
    
    def guardar_procesamiento(self, archivo_salida: str = "processed_docs.json"):
        """
        Guarda los documentos procesados en formato JSON
        
        Args:
            archivo_salida: Nombre del archivo de salida
        """
        try:
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                json.dump(self.processed_documents, f, ensure_ascii=False, indent=2)
            print(f"Documentos guardados en {archivo_salida}")
        except Exception as e:
            print(f"Error guardando documentos: {str(e)}")
