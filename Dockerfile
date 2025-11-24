FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (para OCR y OpenCV)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorios si no existen
RUN mkdir -p logs data pdfs

# Exponer puerto (si es necesario para webhooks)
EXPOSE 8000

# Ejecutar el bot
CMD ["python", "main.py"]
