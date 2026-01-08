#!/usr/bin/env python3
"""
ejemplo_reporte.py
Ejemplo de uso del generador de reportes profesionales
Demuestra cómo crear un reporte completo con tabla de resumen ejecutivo
"""

import sys
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from analisis.report_generator import ProfessionalReport, ExecutiveSummary


def crear_reporte_ejemplo():
    """Crea un reporte de ejemplo completo"""
    
    print("\n" + "="*70)
    print("📊 EJEMPLO: GENERADOR DE REPORTES PROFESIONALES")
    print("="*70)
    
    # 1. Crear reporte
    print("\n✨ Creando reporte de análisis...")
    reporte = ProfessionalReport(
        titulo="Análisis Técnico Profesional - AAPL",
        instrumento="Apple Inc. (AAPL)",
        tipo_analisis="técnico"
    )
    
    # 2. Agregar datos fundamentales
    print("📋 Agregando datos fundamentales...")
    reporte.agregar_datos_fundamentales({
        "Precio Actual": "$185.50",
        "Cambio Diario": "+2.35% (+$4.25)",
        "Volumen": "58.2M",
        "Capitalización": "$2.9T",
        "52 Semanas": "$160.00 - $235.75"
    })
    
    # 3. Agregar análisis técnico
    print("📈 Agregando análisis técnico...")
    reporte.agregar_analisis_tecnico("""
**Análisis de Tendencia:**
- Tendencia principal: Alcista
- Soporte clave: $180.00
- Resistencia: $190.00
- Rompimiento esperado en próximas sesiones

**Patrones Gráficos:**
- Se observa patrón de cuña ascendente
- Potencial rompimiento alcista
- Volumen confirmando movimiento

**Niveles Técnicos:**
- RSI en zona de sobrecompra (75)
- MACD con divergencia alcista
- Bandas de Bollinger expandiéndose
    """)
    
    # 4. Agregar indicadores
    print("📊 Agregando indicadores técnicos...")
    reporte.agregar_indicadores({
        "Media Móvil 50": {"Valor": "$182.30", "Estado": "Alcista"},
        "Media Móvil 200": {"Valor": "$175.80", "Estado": "Alcista"},
        "MACD": {"Valor": "2.45", "Señal": "Compra"},
        "RSI(14)": {"Valor": "75", "Estado": "Sobrecompra"}
    })
    
    # 5. Agregar osciladores
    print("🔄 Agregando osciladores...")
    reporte.agregar_osciladores({
        "RSI": 75,
        "MACD": 2.45,
        "Estocastico": 85
    })
    
    # 6. Agregar medias móviles
    print("📍 Agregando medias móviles...")
    reporte.agregar_medias_moviles({
        "SMA20": 183.20,
        "SMA50": 182.30,
        "SMA200": 175.80,
        "EMA12": 184.50,
        "EMA26": 181.70
    })
    
    # 7. Agregar puntos de pivote
    print("🎯 Agregando puntos de pivote...")
    reporte.agregar_puntos_pivote({
        "R2": 192.50,
        "R1": 188.75,
        "Pivote": 185.00,
        "S1": 181.25,
        "S2": 177.50
    })
    
    # 8. Agregar análisis de IA (simulado)
    print("🤖 Agregando análisis de IA...")
    analisis_ia = """
**Análisis Detallado de Apple Inc. (AAPL)**

La acción de Apple muestra una clara estructura alcista con fortaleza técnica. 
El rompimiento del nivel $183 abre camino hacia resistencias superiores.

La combinación de:
- Tendencia alcista intacta
- Medias móviles alcistas
- Volumen expandiéndose
- RSI elevado pero no crítico

Sugiere continuación del movimiento alcista en el corto plazo.

=== RESUMEN EJECUTIVO ===
RECOMENDACIÓN: COMPRA - Alta Convicción
PRECIO_ENTRADA: $185.50
STOP_LOSS: $180.00
PRECIO_OBJETIVO: $195.00
HORIZONTE: Mediano plazo (3-12 meses)
PROBABILIDAD_ÉXITO: 78%
CONVICCIÓN: Alta
===
"""
    
    reporte.agregar_analisis_ia(analisis_ia)
    
    # 9. El resumen ejecutivo ya fue extraído de la IA, pero podemos verificar
    print("\n✅ Resumen Ejecutivo Extraído:")
    print(f"   Recomendación: {reporte.resumen_ejecutivo.recomendacion}")
    print(f"   Entrada: ${reporte.resumen_ejecutivo.precio_entrada}")
    print(f"   Stop Loss: ${reporte.resumen_ejecutivo.stop_loss}")
    print(f"   Objetivo: ${reporte.resumen_ejecutivo.precio_objetivo}")
    print(f"   Horizonte: {reporte.resumen_ejecutivo.horizonte}")
    print(f"   Probabilidad: {reporte.resumen_ejecutivo.probabilidad_exito}%")
    print(f"   Convicción: {reporte.resumen_ejecutivo.conviccion}")
    
    # 10. Generar reportes
    print("\n📝 Generando reportes...")
    
    # Guardar como markdown
    ruta_md = Path(__file__).parent / "reporte_ejemplo.md"
    if reporte.guardar_markdown(str(ruta_md)):
        print(f"   ✅ Markdown guardado: {ruta_md}")
    else:
        print(f"   ❌ Error guardando markdown")
    
    # Guardar como JSON
    ruta_json = Path(__file__).parent / "reporte_ejemplo.json"
    if reporte.guardar_json(str(ruta_json)):
        print(f"   ✅ JSON guardado: {ruta_json}")
    else:
        print(f"   ❌ Error guardando JSON")
    
    # 11. Mostrar tabla de resumen
    print("\n" + "="*70)
    print("📊 TABLA DE RESUMEN EJECUTIVO")
    print("="*70)
    print(reporte.generar_tabla_resumen_ejecutivo())
    
    # 12. Estadísticas
    print("\n" + "="*70)
    print("📈 ESTADÍSTICAS DEL REPORTE")
    print("="*70)
    print(f"Secciones: {len(reporte.secciones)}")
    print(f"Instrumento: {reporte.instrumento}")
    print(f"Tipo de Análisis: {reporte.tipo_analisis}")
    print(f"Fecha: {reporte.fecha_generacion.strftime('%d/%m/%Y %H:%M:%S')}")
    
    # 13. Muestra parte del markdown
    print("\n" + "="*70)
    print("📄 PREVIEW DEL REPORTE (Primeras 1000 caracteres)")
    print("="*70)
    markdown_completo = reporte.a_markdown()
    print(markdown_completo[:1000] + "...\n")
    
    print("="*70)
    print("✅ EJEMPLO COMPLETADO EXITOSAMENTE")
    print("="*70)
    print("\n💡 Uso del Generador de Reportes:")
    print("""
   1. Crear instancia: report = ProfessionalReport(titulo, instrumento)
   2. Agregar secciones: report.agregar_analisis_tecnico(texto)
   3. Agregar IA: report.agregar_analisis_ia(respuesta_gemini)
   4. Guardar: report.guardar_markdown(ruta) o report.guardar_json(ruta)
   
   La tabla de resumen ejecutivo se genera automáticamente con:
   - Recomendación (COMPRA/VENTA/ESPERA)
   - Precio de entrada
   - Stop loss
   - Precio objetivo
   - Horizonte temporal
   - Probabilidad de éxito
   - Ratio R/R calculado automáticamente
    """)
    print("="*70 + "\n")


if __name__ == "__main__":
    crear_reporte_ejemplo()
