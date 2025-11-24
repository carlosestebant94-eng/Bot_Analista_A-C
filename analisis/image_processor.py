"""
analisis/image_processor.py
Procesador de imágenes y gráficas
Interpreta y analiza imágenes usando visión computacional
"""

try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("⚠️  Advertencia: OpenCV no instalado. Funciones de visión limitadas.")

from PIL import Image
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False


class ImageProcessor:
    """Procesa y analiza imágenes y gráficas"""
    
    def __init__(self):
        """Inicializa el procesador de imágenes"""
        self.ultima_imagen = None
        self.ultima_analisis = None
    
    def cargar_imagen(self, ruta: str) -> Optional[np.ndarray]:
        """
        Carga una imagen desde archivo
        
        Args:
            ruta: Ruta del archivo de imagen
            
        Returns:
            Array numpy de la imagen o None si hay error
        """
        if not CV2_AVAILABLE:
            print("⚠️ OpenCV no disponible para cargar imágenes")
            return None
            
        try:
            imagen = cv2.imread(ruta)
            if imagen is None:
                print(f"No se pudo cargar la imagen: {ruta}")
                return None
            self.ultima_imagen = imagen
            return imagen
        except Exception as e:
            print(f"Error cargando imagen: {str(e)}")
            return None
    
    def extraer_texto_ocr(self, imagen: Optional[np.ndarray] = None) -> str:
        """
        Extrae texto de una imagen usando OCR
        
        Args:
            imagen: Array numpy de la imagen (usa última si no se proporciona)
            
        Returns:
            Texto extraído
        """
        if not TESSERACT_AVAILABLE:
            return "⚠️ Tesseract no instalado"
            
        try:
            if imagen is None:
                imagen = self.ultima_imagen
            
            if imagen is None:
                return ""
            
            # Convertir a PIL para pytesseract
            imagen_pil = Image.fromarray(cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB))
            texto = pytesseract.image_to_string(imagen_pil, lang='spa+eng')
            
            return texto
            
        except Exception as e:
            print(f"Error extrayendo texto OCR: {str(e)}")
            return ""
    
    def detectar_formas(self, imagen: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Detecta formas geométricas en la imagen (para gráficas)
        
        Args:
            imagen: Array numpy de la imagen
            
        Returns:
            Diccionario con información de formas detectadas
        """
        if not CV2_AVAILABLE:
            return {"error": "OpenCV no disponible"}
            
        try:
            if imagen is None:
                imagen = self.ultima_imagen
            
            if imagen is None:
                return {}
            
            # Convertir a escala de grises
            gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            
            # Detección de bordes
            bordes = cv2.Canny(gris, 50, 150)
            
            # Encontrar contornos
            contornos, _ = cv2.findContours(bordes, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            formas_detectadas = {
                "total_contornos": len(contornos),
                "rectangulos": 0,
                "circulos": 0,
                "triangulos": 0,
                "otros": 0,
                "detalles": []
            }
            
            for contorno in contornos:
                area = cv2.contourArea(contorno)
                if area < 100:  # Ignorar formas muy pequeñas
                    continue
                
                epsilon = 0.04 * cv2.arcLength(contorno, True)
                aproximacion = cv2.approxPolyDP(contorno, epsilon, True)
                vertices = len(aproximacion)
                
                forma_info = {
                    "vertices": vertices,
                    "area": float(area),
                    "perimetro": float(cv2.arcLength(contorno, True))
                }
                
                if vertices == 3:
                    formas_detectadas["triangulos"] += 1
                    forma_info["tipo"] = "triangulo"
                elif vertices == 4:
                    formas_detectadas["rectangulos"] += 1
                    forma_info["tipo"] = "rectangulo"
                elif vertices >= 8:
                    formas_detectadas["circulos"] += 1
                    forma_info["tipo"] = "circulo"
                else:
                    formas_detectadas["otros"] += 1
                    forma_info["tipo"] = "otro"
                
                formas_detectadas["detalles"].append(forma_info)
            
            return formas_detectadas
            
        except Exception as e:
            print(f"Error detectando formas: {str(e)}")
            return {}
    
    def analizar_colores(self, imagen: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Analiza la distribución de colores en la imagen
        
        Args:
            imagen: Array numpy de la imagen
            
        Returns:
            Diccionario con análisis de colores
        """
        try:
            if imagen is None:
                imagen = self.ultima_imagen
            
            if imagen is None:
                return {}
            
            # Convertir BGR a HSV para mejor análisis de color
            hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
            
            # Calcular histograma
            histograma = cv2.calcHist([hsv], [0], None, [180], [0, 180])
            
            # Colores dominantes
            alto, ancho = imagen.shape[:2]
            pixeles = imagen.reshape((alto * ancho, 3))
            pixeles = np.float32(pixeles)
            
            # K-means para encontrar colores dominantes
            criterios = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            _, _, centros = cv2.kmeans(pixeles, 3, None, criterios, 10, cv2.KMEANS_RANDOM_CENTERS)
            
            centros = np.uint8(centros)
            
            return {
                "colores_dominantes": len(set(centros.flatten())),
                "paleta_principal": centros.tolist(),
                "saturacion_promedio": float(np.mean(hsv[:, :, 1])),
                "brillo_promedio": float(np.mean(hsv[:, :, 2]))
            }
            
        except Exception as e:
            print(f"Error analizando colores: {str(e)}")
            return {}
    
    def detectar_graficos(self, imagen: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Detecta tipo de gráfico (barras, líneas, pastel, etc)
        
        Args:
            imagen: Array numpy de la imagen
            
        Returns:
            Diccionario con información del gráfico detectado
        """
        try:
            if imagen is None:
                imagen = self.ultima_imagen
            
            if imagen is None:
                return {}
            
            analisis = {
                "tipo_grafico_probable": "",
                "confianza": 0.0,
                "caracteristicas": {}
            }
            
            gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            bordes = cv2.Canny(gris, 50, 150)
            
            # Detectar líneas
            lineas = cv2.HoughLinesP(bordes, 1, np.pi/180, 50, minLineLength=50, maxLineGap=10)
            lineas_horizontales = 0
            lineas_verticales = 0
            
            if lineas is not None:
                for linea in lineas:
                    x1, y1, x2, y2 = linea[0]
                    angulo = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
                    
                    if -10 <= angulo <= 10 or 170 <= angulo <= 180:
                        lineas_horizontales += 1
                    elif 80 <= angulo <= 100:
                        lineas_verticales += 1
            
            analisis["caracteristicas"]["lineas_horizontales"] = lineas_horizontales
            analisis["caracteristicas"]["lineas_verticales"] = lineas_verticales
            
            # Determinar tipo de gráfico basado en características
            if lineas_horizontales > lineas_verticales:
                analisis["tipo_grafico_probable"] = "gráfico_de_barras_horizontal"
                analisis["confianza"] = 0.75
            elif lineas_verticales > lineas_horizontales:
                analisis["tipo_grafico_probable"] = "gráfico_de_barras_vertical"
                analisis["confianza"] = 0.75
            elif lineas_horizontales > 5 and lineas_verticales > 5:
                analisis["tipo_grafico_probable"] = "gráfico_de_dispersión"
                analisis["confianza"] = 0.6
            
            return analisis
            
        except Exception as e:
            print(f"Error detectando gráficos: {str(e)}")
            return {}
    
    def analisis_completo_imagen(self, ruta: str) -> Dict[str, Any]:
        """
        Realiza un análisis completo de una imagen
        
        Args:
            ruta: Ruta del archivo de imagen
            
        Returns:
            Diccionario con análisis completo
        """
        imagen = self.cargar_imagen(ruta)
        if imagen is None:
            return {}
        
        resultado = {
            "archivo": Path(ruta).name,
            "dimensiones": (imagen.shape[1], imagen.shape[0]),
            "texto_extraido": self.extraer_texto_ocr(imagen),
            "formas_detectadas": self.detectar_formas(imagen),
            "analisis_colores": self.analizar_colores(imagen),
            "tipo_grafico": self.detectar_graficos(imagen)
        }
        
        self.ultima_analisis = resultado
        return resultado
