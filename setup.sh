#!/bin/bash

# Bot Analista A&C - Setup Script para Google IDX

echo "=================================================="
echo "  Configurando Bot Analista A&C en Google IDX"
echo "=================================================="

# Crear entorno virtual
echo ""
echo "Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo ""
echo "Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Crear directorios necesarios
echo ""
echo "Creando directorios..."
mkdir -p logs
mkdir -p data
mkdir -p pdfs

# Configurar variables de entorno
echo ""
echo "=================================================="
echo "  CONFIGURACIÓN COMPLETADA"
echo "=================================================="
echo ""
echo "PRÓXIMOS PASOS:"
echo "1. Configura tu .env con:"
echo "   TELEGRAM_TOKEN=tu_token"
echo "   GOOGLE_API_KEY=tu_api_key"
echo ""
echo "2. Ejecuta el bot:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "3. O usa el comando de ejecución: 'Ejecutar Bot'"
echo ""
