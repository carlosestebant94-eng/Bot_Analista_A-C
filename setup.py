"""
setup.py
Script de configuración rápida del proyecto
Ejecutar una sola vez para inicializar todo
"""

import os
import sys
from pathlib import Path


def crear_archivo_env():
    """Crea el archivo .env si no existe"""
    env_path = Path(".env")
    
    if env_path.exists():
        print("✅ Archivo .env ya existe")
        return
    
    print("\n🔑 CONFIGURACIÓN DE TELEGRAM TOKEN")
    print("=" * 50)
    print("Para obtener tu token:")
    print("1. Abre Telegram y busca @BotFather")
    print("2. Envía: /newbot")
    print("3. Sigue las instrucciones")
    print("4. Copia el token recibido\n")
    
    token = input("Ingresa tu TELEGRAM_TOKEN: ").strip()
    
    if not token:
        print("❌ Token no proporcionado. Saltando creación de .env")
        return
    
    contenido = f"""# Bot Analista A&C - Configuración
TELEGRAM_TOKEN={token}
TELEGRAM_CHAT_ID=
OPENAI_API_KEY=
LOG_LEVEL=INFO
"""
    
    with open(env_path, 'w') as f:
        f.write(contenido)
    
    print(f"✅ Archivo .env creado: {env_path}")


def verificar_dependencias():
    """Verifica si las dependencias están instaladas"""
    print("\n📦 VERIFICANDO DEPENDENCIAS")
    print("=" * 50)
    
    paquetes_necesarios = [
        'telegram',
        'pdfplumber',
        'cv2',  # opencv
        'numpy',
        'pandas',
        'PIL',  # Pillow
        'pytesseract',
    ]
    
    faltantes = []
    
    for paquete in paquetes_necesarios:
        try:
            __import__(paquete)
            print(f"✅ {paquete}")
        except ImportError:
            print(f"❌ {paquete}")
            faltantes.append(paquete)
    
    if faltantes:
        print(f"\n⚠️  Faltarían instalar los siguientes paquetes:")
        print(f"   pip install -r requirements.txt")
    else:
        print("\n✅ Todas las dependencias están instaladas")


def mostrar_estructura():
    """Muestra la estructura del proyecto"""
    print("\n📁 ESTRUCTURA DEL PROYECTO")
    print("=" * 50)
    
    estructura = """
Bot_Analist_A&C/
├── cerebro/                    (🧠 Base de conocimiento)
│   ├── __init__.py
│   ├── knowledge_manager.py    (Gestor de BD)
│   └── pdf_processor.py        (Procesador PDFs)
│
├── telegram_bot/               (🤖 Bot principal)
│   ├── __init__.py
│   └── bot.py                  (Lógica del bot)
│
├── analisis/                   (📊 Motor de análisis)
│   ├── __init__.py
│   ├── analyzer.py            (Análisis de datos)
│   └── image_processor.py     (Análisis de imágenes)
│
├── utils/                      (🔧 Utilidades)
│   ├── __init__.py
│   ├── logger.py              (Sistema de logs)
│   └── validators.py          (Validadores)
│
├── config/                     (⚙️  Configuración)
│   ├── __init__.py
│   └── settings.py            (Configuración centralizada)
│
├── pdfs/                       (📚 Carpeta para entrenar el cerebro)
├── data/                       (💾 Base de datos y datos procesados)
├── logs/                       (📝 Archivos de log)
│
├── main.py                     (🚀 Punto de entrada)
├── test_example.py            (🧪 Script de pruebas)
├── setup.py                    (⚙️  Configuración inicial)
├── requirements.txt           (📦 Dependencias)
├── .env.example               (📋 Plantilla de configuración)
├── README.md                  (📖 Documentación básica)
└── GUIA_COMPLETA.md          (📚 Guía completa)
"""
    
    print(estructura)


def mostrar_proximos_pasos():
    """Muestra los próximos pasos"""
    print("\n🚀 PRÓXIMOS PASOS")
    print("=" * 50)
    
    pasos = """
1. ✅ Configuración completada

2. 📚 Agregar PDFs para entrenar el cerebro:
   - Coloca tus PDFs en la carpeta "pdfs/"
   - El bot extraerá automáticamente el conocimiento

3. 🧪 Ejecutar pruebas (opcional):
   python test_example.py

4. 🤖 Iniciar el bot:
   python main.py

5. 💬 En Telegram:
   - Busca tu bot (el nombre que diste en @BotFather)
   - Envía: /start
   - Usa /ayuda para ver comandos disponibles

6. 📊 Comienza a analizar:
   - Envía datos JSON para análisis
   - Envía imágenes para análisis visual
   - Carga PDFs para entrenar el cerebro
"""
    
    print(pasos)


def main():
    """Función principal"""
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("\n" + "=" * 50)
    print("🤖 BOT ANALISTA A&C - SETUP INICIAL")
    print("=" * 50)
    
    # Crear directorios
    print("\n📁 CREANDO DIRECTORIOS")
    print("=" * 50)
    
    directorios = ['pdfs', 'data', 'logs']
    for directorio in directorios:
        Path(directorio).mkdir(exist_ok=True)
        print(f"✅ Directorio '{directorio}' listo")
    
    # Mostrar estructura
    mostrar_estructura()
    
    # Crear .env
    crear_archivo_env()
    
    # Verificar dependencias
    verificar_dependencias()
    
    # Mostrar próximos pasos
    mostrar_proximos_pasos()
    
    print("\n" + "=" * 50)
    print("✅ SETUP COMPLETADO")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
