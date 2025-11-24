"""
utils/validators.py
Validadores de archivos y datos
"""

import os
from pathlib import Path
from typing import Tuple, List


def validate_pdf(ruta: str) -> Tuple[bool, str]:
    """
    Valida si un archivo es un PDF válido
    
    Args:
        ruta: Ruta del archivo a validar
        
    Returns:
        Tupla (es_válido, mensaje)
    """
    try:
        # Verificar que existe
        if not os.path.exists(ruta):
            return False, f"Archivo no encontrado: {ruta}"
        
        # Verificar extensión
        if not ruta.lower().endswith('.pdf'):
            return False, f"Archivo no es PDF: {ruta}"
        
        # Verificar que no esté vacío
        tamaño = os.path.getsize(ruta)
        if tamaño == 0:
            return False, "Archivo PDF está vacío"
        
        if tamaño > 100 * 1024 * 1024:  # 100 MB
            return False, "Archivo PDF es demasiado grande (>100 MB)"
        
        return True, "PDF válido"
        
    except Exception as e:
        return False, f"Error validando PDF: {str(e)}"


def validate_image(ruta: str) -> Tuple[bool, str]:
    """
    Valida si un archivo es una imagen válida
    
    Args:
        ruta: Ruta del archivo a validar
        
    Returns:
        Tupla (es_válido, mensaje)
    """
    try:
        # Extensiones permitidas
        extensiones_validas = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
        
        # Verificar que existe
        if not os.path.exists(ruta):
            return False, f"Archivo no encontrado: {ruta}"
        
        # Verificar extensión
        extension = Path(ruta).suffix.lower()
        if extension not in extensiones_validas:
            return False, f"Formato de imagen no soportado: {extension}"
        
        # Verificar que no esté vacío
        tamaño = os.path.getsize(ruta)
        if tamaño == 0:
            return False, "Archivo de imagen está vacío"
        
        if tamaño > 50 * 1024 * 1024:  # 50 MB
            return False, "Archivo de imagen es demasiado grande (>50 MB)"
        
        return True, "Imagen válida"
        
    except Exception as e:
        return False, f"Error validando imagen: {str(e)}"


def listar_archivos_validos(directorio: str, tipo: str = "pdf") -> List[str]:
    """
    Lista archivos válidos en un directorio
    
    Args:
        directorio: Directorio a escanear
        tipo: Tipo de archivos ("pdf" o "imagen")
        
    Returns:
        Lista de rutas válidas
    """
    archivos_validos = []
    
    if not os.path.exists(directorio):
        return archivos_validos
    
    if tipo.lower() == "pdf":
        extensiones = {'.pdf'}
        validador = validate_pdf
    else:
        extensiones = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
        validador = validate_image
    
    try:
        for archivo in os.listdir(directorio):
            ruta_completa = os.path.join(directorio, archivo)
            
            if os.path.isfile(ruta_completa):
                extension = Path(archivo).suffix.lower()
                
                if extension in extensiones:
                    es_valido, _ = validador(ruta_completa)
                    if es_valido:
                        archivos_validos.append(ruta_completa)
        
    except Exception as e:
        print(f"Error escaneando directorio: {str(e)}")
    
    return archivos_validos
