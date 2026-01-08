"""
analisis/report_generator.py
Generador de reportes profesionales de análisis
Pilar: Reporte de análisis profesional con tabla de resumen ejecutivo
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class ExecutiveSummary:
    """Resumen ejecutivo estructurado para reportes"""
    
    def __init__(self):
        """Inicializa el resumen ejecutivo"""
        self.recomendacion = None
        self.precio_entrada = None
        self.stop_loss = None
        self.precio_objetivo = None
        self.horizonte = None
        self.probabilidad_exito = None
        self.conviccion = "Media"
    
    def desde_respuesta_ia(self, respuesta: str) -> bool:
        """
        Extrae resumen ejecutivo de respuesta de IA
        
        Args:
            respuesta: Respuesta de Gemini con formato especial
            
        Returns:
            True si se extrajo correctamente
        """
        try:
            # Buscar sección de resumen
            if "=== RESUMEN EJECUTIVO ===" not in respuesta:
                return False
            
            inicio = respuesta.find("=== RESUMEN EJECUTIVO ===")
            fin = respuesta.find("===", inicio + 24)
            seccion = respuesta[inicio:fin] if fin != -1 else respuesta[inicio:]
            
            # Extraer campos con parsing más flexible
            lineas = seccion.split('\n')
            for linea in lineas:
                linea_lower = linea.lower()
                
                if "recomendación:" in linea_lower or "recomendacion:" in linea_lower:
                    valor = linea.split(":")[-1].strip()
                    self.recomendacion = valor.split("-")[0].strip() if valor else None
                    
                elif "precio_entrada:" in linea_lower:
                    valor = linea.split(":")[-1].strip().replace("$", "").replace(",", ".")
                    try:
                        self.precio_entrada = float(valor) if valor else None
                    except:
                        pass
                        
                elif "stop_loss:" in linea_lower:
                    valor = linea.split(":")[-1].strip().replace("$", "").replace(",", ".")
                    try:
                        self.stop_loss = float(valor) if valor else None
                    except:
                        pass
                        
                elif "precio_objetivo:" in linea_lower:
                    valor = linea.split(":")[-1].strip().replace("$", "").replace(",", ".")
                    try:
                        self.precio_objetivo = float(valor) if valor else None
                    except:
                        pass
                        
                elif "horizonte:" in linea_lower:
                    self.horizonte = linea.split(":")[-1].strip()
                    
                elif "probabilidad" in linea_lower:
                    valor = linea.split(":")[-1].strip().replace("%", "").replace(",", ".")
                    try:
                        self.probabilidad_exito = int(float(valor)) if valor else None
                    except:
                        pass
                        
                elif "convicción:" in linea_lower or "conviccion:" in linea_lower:
                    self.conviccion = linea.split(":")[-1].strip()
            
            return True
            
        except Exception as e:
            print(f"Error extrayendo resumen: {str(e)}")
            return False
    
    def validar(self) -> bool:
        """Valida que todos los campos esenciales estén presentes"""
        return all([
            self.recomendacion,
            self.precio_entrada,
            self.stop_loss,
            self.precio_objetivo,
            self.horizonte,
            self.probabilidad_exito is not None
        ])
    
    def a_diccionario(self) -> Dict[str, Any]:
        """Convierte a diccionario"""
        return {
            "recomendacion": self.recomendacion,
            "precio_entrada": self.precio_entrada,
            "stop_loss": self.stop_loss,
            "precio_objetivo": self.precio_objetivo,
            "horizonte": self.horizonte,
            "probabilidad_exito": self.probabilidad_exito,
            "conviccion": self.conviccion
        }


class ProfessionalReport:
    """Generador de reportes profesionales de análisis"""
    
    def __init__(self, titulo: str, instrumento: str, tipo_analisis: str = "técnico"):
        """
        Inicializa generador de reportes
        
        Args:
            titulo: Título del reporte
            instrumento: Instrumento analizado (ej: AAPL, EURUSD)
            tipo_analisis: Tipo de análisis realizado
        """
        self.titulo = titulo
        self.instrumento = instrumento
        self.tipo_analisis = tipo_analisis
        self.fecha_generacion = datetime.now()
        self.secciones = []
        self.resumen_ejecutivo = ExecutiveSummary()
    
    def agregar_seccion(self, titulo: str, contenido: str, 
                       numero_seccion: Optional[int] = None) -> None:
        """
        Agrega una sección al reporte
        
        Args:
            titulo: Título de la sección
            contenido: Contenido de la sección
            numero_seccion: Número de sección (opcional)
        """
        self.secciones.append({
            "titulo": titulo,
            "contenido": contenido,
            "numero": numero_seccion or len(self.secciones) + 1,
            "fecha_agregada": datetime.now().isoformat()
        })
    
    def agregar_datos_fundamentales(self, datos: Dict[str, Any]) -> None:
        """Agrega datos fundamentales del instrumento"""
        contenido = "📊 **Datos Fundamentales del Instrumento**\n\n"
        for clave, valor in datos.items():
            contenido += f"• **{clave}:** {valor}\n"
        
        self.agregar_seccion("Datos Fundamentales", contenido, 1)
    
    def agregar_analisis_tecnico(self, analisis: str) -> None:
        """Agrega análisis técnico"""
        self.agregar_seccion("Análisis Técnico", analisis, 3)
    
    def agregar_indicadores(self, indicadores: Dict[str, Dict[str, Any]]) -> None:
        """
        Agrega indicadores técnicos
        
        Args:
            indicadores: Dict con indicadores {nombre: {valores...}}
        """
        contenido = "📈 **Indicadores Técnicos**\n\n"
        
        for nombre, valores in indicadores.items():
            contenido += f"**{nombre}**\n"
            for clave, valor in valores.items():
                contenido += f"  • {clave}: {valor}\n"
            contenido += "\n"
        
        self.agregar_seccion("Indicadores Técnicos", contenido, 4)
    
    def agregar_osciladores(self, osciladores: Dict[str, Any]) -> None:
        """Agrega osciladores (RSI, MACD, etc)"""
        contenido = "🔄 **Osciladores**\n\n"
        
        for nombre, valor in osciladores.items():
            estado = self._interpretar_oscilador(nombre, valor)
            contenido += f"• **{nombre}:** {valor} - {estado}\n"
        
        self.agregar_seccion("Osciladores", contenido, 5)
    
    def agregar_medias_moviles(self, medias: Dict[str, float]) -> None:
        """Agrega medias móviles"""
        contenido = "📊 **Medias Móviles**\n\n"
        
        for periodo, valor in medias.items():
            contenido += f"• **{periodo}:** {valor}\n"
        
        self.agregar_seccion("Medias Móviles", contenido, 6)
    
    def agregar_puntos_pivote(self, pivotes: Dict[str, float]) -> None:
        """Agrega puntos de pivote"""
        contenido = "🎯 **Puntos de Pivote**\n\n"
        
        for tipo, valor in pivotes.items():
            contenido += f"• **{tipo}:** ${valor:.2f}\n"
        
        self.agregar_seccion("Puntos de Pivote", contenido, 7)
    
    def agregar_analisis_ia(self, analisis: str) -> None:
        """
        Agrega análisis de IA (Gemini)
        
        Args:
            analisis: Texto de análisis de IA
        """
        # Extraer resumen ejecutivo si está presente
        self.resumen_ejecutivo.desde_respuesta_ia(analisis)
        
        # Remover sección de resumen del análisis principal
        if "=== RESUMEN EJECUTIVO ===" in analisis:
            analisis = analisis[:analisis.find("=== RESUMEN EJECUTIVO ===")]
        
        self.agregar_seccion("Análisis Profesional (IA)", analisis, 8)
    
    def agregar_resumen_ejecutivo_manual(self, 
                                        recomendacion: str,
                                        precio_entrada: float,
                                        stop_loss: float,
                                        precio_objetivo: float,
                                        horizonte: str,
                                        probabilidad: int,
                                        conviccion: str = "Media") -> None:
        """
        Agrega resumen ejecutivo manualmente
        
        Args:
            recomendacion: COMPRA/VENTA/ESPERA
            precio_entrada: Precio de entrada
            stop_loss: Stop loss
            precio_objetivo: Precio objetivo
            horizonte: Horizonte temporal
            probabilidad: Probabilidad de éxito (%)
            conviccion: Nivel de convicción
        """
        self.resumen_ejecutivo.recomendacion = recomendacion
        self.resumen_ejecutivo.precio_entrada = precio_entrada
        self.resumen_ejecutivo.stop_loss = stop_loss
        self.resumen_ejecutivo.precio_objetivo = precio_objetivo
        self.resumen_ejecutivo.horizonte = horizonte
        self.resumen_ejecutivo.probabilidad_exito = probabilidad
        self.resumen_ejecutivo.conviccion = conviccion
    
    def generar_tabla_resumen_ejecutivo(self) -> str:
        """
        Genera la tabla de resumen ejecutivo en formato markdown
        
        Returns:
            Tabla formateada en markdown
        """
        if not self.resumen_ejecutivo.validar():
            return "⚠️ Resumen ejecutivo incompleto"
        
        # Determinar color por recomendación
        colores = {
            "COMPRA": "🟢 Verde",
            "VENTA": "🔴 Rojo",
            "ESPERA": "🟠 Naranja"
        }
        
        color = colores.get(self.resumen_ejecutivo.recomendacion, "⚪ Neutral")
        
        tabla = f"""
## 8️⃣ RESUMEN EJECUTIVO - RECOMENDACIONES

| Campo | Valor |
|-------|-------|
| **Recomendación** | {color} **{self.resumen_ejecutivo.recomendacion}** - {self.resumen_ejecutivo.conviccion} Convicción |
| **Precio de Entrada** | ${self.resumen_ejecutivo.precio_entrada:.2f} |
| **Stop Loss (Salida)** | ${self.resumen_ejecutivo.stop_loss:.2f} |
| **Precio Objetivo (T.Profit)** | ${self.resumen_ejecutivo.precio_objetivo:.2f} |
| **Horizonte de Inversión** | {self.resumen_ejecutivo.horizonte} |
| **Probabilidad de Éxito** | {self.resumen_ejecutivo.probabilidad_exito}% |

---

### Cálculo de Riesgo/Recompensa

**Riesgo (R):** ${abs(self.resumen_ejecutivo.precio_entrada - self.resumen_ejecutivo.stop_loss):.2f}
**Recompensa (R):** ${abs(self.resumen_ejecutivo.precio_objetivo - self.resumen_ejecutivo.precio_entrada):.2f}
**Ratio R/R:** {self._calcular_ratio_riesgo():.2f}:1

---
"""
        return tabla
    
    def _calcular_ratio_riesgo(self) -> float:
        """Calcula el ratio riesgo/recompensa"""
        try:
            riesgo = abs(self.resumen_ejecutivo.precio_entrada - 
                        self.resumen_ejecutivo.stop_loss)
            recompensa = abs(self.resumen_ejecutivo.precio_objetivo - 
                            self.resumen_ejecutivo.precio_entrada)
            
            if riesgo == 0:
                return 0
            
            return recompensa / riesgo
        except:
            return 0
    
    def _interpretar_oscilador(self, nombre: str, valor: Any) -> str:
        """Interpreta el estado de un oscilador"""
        interpretaciones = {
            "RSI": lambda v: "Sobrecomprado" if v > 70 else "Sobreventa" if v < 30 else "Neutral",
            "MACD": lambda v: "Señal Alcista" if v > 0 else "Señal Bajista",
            "Estocastico": lambda v: "Sobrecomprado" if v > 80 else "Sobreventa" if v < 20 else "Neutral"
        }
        
        if nombre in interpretaciones:
            try:
                return interpretaciones[nombre](float(str(valor).replace("%", "")))
            except:
                pass
        
        return "Neutral"
    
    def generar_indice(self) -> str:
        """Genera índice del reporte"""
        indice = "## 📋 ÍNDICE DEL REPORTE\n\n"
        
        for seccion in self.secciones:
            indice += f"{seccion['numero']}. {seccion['titulo']}\n"
        
        indice += "\n8. RESUMEN EJECUTIVO - RECOMENDACIONES\n"
        
        return indice
    
    def a_markdown(self) -> str:
        """Genera reporte completo en markdown"""
        reporte = f"""# 📊 {self.titulo}

**Instrumento:** {self.instrumento}  
**Tipo de Análisis:** {self.tipo_analisis}  
**Fecha de Generación:** {self.fecha_generacion.strftime('%d/%m/%Y %H:%M:%S')}  

---

"""
        
        # Agregar índice
        reporte += self.generar_indice() + "\n---\n\n"
        
        # Agregar secciones
        for seccion in self.secciones:
            reporte += f"## {seccion['numero']}. {seccion['titulo']}\n\n"
            reporte += seccion['contenido'] + "\n\n---\n\n"
        
        # Agregar resumen ejecutivo
        reporte += self.generar_tabla_resumen_ejecutivo()
        
        # Agregar disclaimer
        reporte += """
### ⚠️ DISCLAIMER LEGAL

Este reporte es únicamente para fines informativos y educativos. 
**No constituye asesoramiento financiero, de inversión o recomendación de compra/venta.**

- El análisis se basa en datos históricos y puede no predecir resultados futuros
- Los mercados financieros son volátiles e impredecibles
- Todo trading implica riesgo de pérdida total del capital
- Consulta con un asesor financiero profesional antes de tomar decisiones

**Responsabilidad:** El usuario es 100% responsable de sus decisiones de inversión.

---

*Generado por Bot Analista A&C © 2025*
"""
        
        return reporte
    
    def a_diccionario(self) -> Dict[str, Any]:
        """Convierte el reporte a diccionario"""
        return {
            "titulo": self.titulo,
            "instrumento": self.instrumento,
            "tipo_analisis": self.tipo_analisis,
            "fecha_generacion": self.fecha_generacion.isoformat(),
            "secciones": self.secciones,
            "resumen_ejecutivo": self.resumen_ejecutivo.a_diccionario()
        }
    
    def guardar_json(self, ruta: str) -> bool:
        """
        Guarda el reporte en formato JSON
        
        Args:
            ruta: Ruta donde guardar
            
        Returns:
            True si fue exitoso
        """
        try:
            import json
            with open(ruta, 'w', encoding='utf-8') as f:
                json.dump(self.a_diccionario(), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error guardando reporte: {str(e)}")
            return False
    
    def guardar_markdown(self, ruta: str) -> bool:
        """
        Guarda el reporte en markdown
        
        Args:
            ruta: Ruta donde guardar
            
        Returns:
            True si fue exitoso
        """
        try:
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(self.a_markdown())
            return True
        except Exception as e:
            print(f"Error guardando reporte: {str(e)}")
            return False
