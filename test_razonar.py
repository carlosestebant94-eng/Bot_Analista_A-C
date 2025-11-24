#!/usr/bin/env python3
"""
test_razonar.py
Prueba del comando razonar sin necesidad del bot de Telegram
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
    print("=" * 60)
    print("🧠 TEST DEL COMANDO RAZONAR")
    print("=" * 60)
    
    # Inicializar motor de IA
    print("\n1️⃣  Inicializando motor de IA...")
    ai_engine = AIEngine()
    
    if not ai_engine.enabled:
        print("❌ Motor de IA no está habilitado")
        print(f"   API Key configurada: {bool(os.getenv('GOOGLE_API_KEY'))}")
        return
    
    print("✅ Motor de IA inicializado correctamente")
    status = ai_engine.get_status()
    print(f"   Estado: {status['mensaje']}")
    
    # Inicializar base de conocimiento
    print("\n2️⃣  Inicializando base de conocimiento...")
    km = KnowledgeManager(str(Settings.DATABASE_PATH))
    stats = km.obtener_estadisticas()
    print(f"✅ Base de conocimiento cargada")
    print(f"   Documentos: {stats.get('documentos_cargados', 0)}")
    print(f"   Conocimientos: {stats.get('conocimientos_almacenados', 0)}")
    
    # Pruebas de razonamiento
    preguntas = [
        "¿Qué es el análisis técnico?",
        "¿Cuál es la diferencia entre trading y inversión?",
        "¿Cuáles son los indicadores técnicos más importantes?"
    ]
    
    print("\n3️⃣  Probando razonamiento...")
    print("-" * 60)
    
    for i, pregunta in enumerate(preguntas, 1):
        print(f"\n📌 Pregunta {i}: {pregunta}")
        print("-" * 40)
        
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
        try:
            resultado = ai_engine.razonar(pregunta=pregunta, contexto=contexto)
            
            if resultado.get("error"):
                print(f"❌ Error: {resultado['respuesta']}")
            else:
                respuesta = resultado.get("respuesta", "Sin respuesta")
                confianza = resultado.get("confianza", 0.0)
                
                # Mostrar respuesta truncada
                if len(respuesta) > 300:
                    respuesta_preview = respuesta[:297] + "..."
                else:
                    respuesta_preview = respuesta
                
                print(f"✅ Respuesta recibida")
                print(f"\n🤖 {respuesta_preview}")
                print(f"\n📊 Confianza: {confianza:.0%}")
        
        except Exception as e:
            print(f"❌ Excepción: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 60)

if __name__ == "__main__":
    main()
