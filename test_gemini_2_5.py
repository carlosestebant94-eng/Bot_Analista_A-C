#!/usr/bin/env python3
"""
test_gemini_2_5.py
Prueba del modelo Gemini 2.5
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el proyecto al path
sys.path.insert(0, str(Path(__file__).parent))

from ia import AIEngine
from cerebro import KnowledgeManager
from config import Settings

def main():
    print("=" * 70)
    print("🚀 TEST DE GEMINI 2.5-PRO")
    print("=" * 70)
    
    # Inicializar motor de IA
    print("\n1️⃣  Inicializando motor de IA con Gemini 2.5...")
    ai_engine = AIEngine()
    
    if not ai_engine.enabled:
        print("❌ Motor de IA no está habilitado")
        print(f"   API Key configurada: {bool(os.getenv('GOOGLE_API_KEY'))}")
        return
    
    print("✅ Motor de IA inicializado correctamente")
    status = ai_engine.get_status()
    print(f"   Estado: {status['mensaje']}")
    print(f"   Proveedor: {status['proveedor']}")
    
    # Inicializar base de conocimiento
    print("\n2️⃣  Inicializando base de conocimiento...")
    km = KnowledgeManager(str(Settings.DATABASE_PATH))
    stats = km.obtener_estadisticas()
    print(f"✅ Base de conocimiento cargada")
    print(f"   Documentos: {stats.get('documentos_cargados', 0)}")
    print(f"   Conocimientos: {stats.get('conocimientos_almacenados', 0)}")
    
    # Test simple de razonamiento
    print("\n3️⃣  Probando razonamiento con Gemini 2.5...")
    print("-" * 70)
    
    pregunta = "¿Qué es el análisis técnico en el trading?"
    print(f"\n📌 Pregunta: {pregunta}")
    print("-" * 40)
    
    try:
        # Obtener contexto
        documentos_relevantes = km.buscar_conocimiento(pregunta, limite=2)
        contexto = ""
        if documentos_relevantes:
            contexto = "\n".join([
                f"📖 {doc['documento']}: {doc['contenido'][:150]}..."
                for doc in documentos_relevantes
            ])
            print(f"✅ Contexto encontrado ({len(documentos_relevantes)} documentos)")
        else:
            print("⚠️  No se encontró contexto relevante")
        
        # Razonar
        resultado = ai_engine.razonar(
            pregunta=pregunta, 
            contexto=contexto,
            modelo="gemini-2.5-pro"  # Especificar modelo explícitamente
        )
        
        if resultado.get("error"):
            print(f"\n❌ Error: {resultado['respuesta']}")
            return
        
        respuesta = resultado.get("respuesta", "Sin respuesta")
        confianza = resultado.get("confianza", 0.0)
        modelo = resultado.get("modelo", "desconocido")
        
        print(f"\n✅ Respuesta recibida del modelo {modelo}")
        print(f"\n🤖 {respuesta}")
        print(f"\n📊 Confianza: {confianza:.0%}")
        print("\n" + "=" * 70)
        print("✅ TEST EXITOSO - GEMINI 2.5 OPERATIVO")
        print("=" * 70)
    
    except Exception as e:
        print(f"\n❌ Excepción: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
