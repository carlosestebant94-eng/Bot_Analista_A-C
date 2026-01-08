"""
utils/pdf_generator.py
Generador de PDFs profesionales para reportes de análisis
"""

import re
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import logging


class PDFReportGenerator:
    """Genera reportes PDF profesionales de análisis de trading"""
    
    def __init__(self, output_dir: str = "data/reportes"):
        """
        Inicializa el generador
        
        Args:
            output_dir: Directorio donde guardar los PDFs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger("PDFReportGenerator")
    
    def generar_reporte_analisis(
        self,
        ticker: str,
        datos_actuales: Dict[str, Any],
        fundamentales: Dict[str, Any],
        tecnico: Dict[str, Any],
        alexander: Dict[str, Any],
        soportes_resistencias: Dict[str, Any],
        recomendacion: Dict[str, Any],
        entry_price: float,
        stop_loss: float,
        take_profit: float,
        ganancia_potencial: float,
        perdida_potencial: float,
        tiempo_proyectado: str,
        proyeccion: str,
        recomendable: str,
        analisis_narrativo: str = ""
    ) -> str:
        """
        Genera un PDF completo del análisis
        
        Args:
            ticker: Símbolo del instrumento
            datos_actuales: Datos actuales del precio
            fundamentales: Análisis fundamental
            tecnico: Análisis técnico
            alexander: Análisis Alexander
            soportes_resistencias: Pivot points
            recomendacion: Recomendación del sistema
            entry_price: Precio de entrada
            stop_loss: Stop loss
            take_profit: Take profit
            ganancia_potencial: Ganancia %
            perdida_potencial: Pérdida %
            tiempo_proyectado: Tiempo estimado
            proyeccion: Proyección visual
            recomendable: Si es recomendable
            analisis_narrativo: Análisis narrativo fundamentado
        
        Returns:
            Ruta del PDF generado
        """
        
        # Nombre del archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{ticker}_ANALISIS_{timestamp}.pdf"
        filepath = self.output_dir / filename
        
        # Crear documento
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch,
            title=f"Análisis {ticker}",
            author="Bot Analista A&C"
        )
        
        # Contenido
        story = []
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2ca02c'),
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        # Título
        precio_actual = datos_actuales.get('precio_actual', 'N/A')
        nombre = datos_actuales.get('nombre', 'Instrumento')
        story.append(Paragraph(f"ANÁLISIS PROFESIONAL 360°", title_style))
        story.append(Paragraph(f"{ticker} - {nombre}", styles['Heading2']))
        story.append(Paragraph(f"Precio Actual: ${precio_actual}", styles['Normal']))
        story.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 
                             ParagraphStyle('date', parent=styles['Normal'], fontSize=9)))
        story.append(Spacer(1, 0.2*inch))
        
        # PLAN DE ACCIÓN TRADING
        story.append(Paragraph("📊 PLAN DE ACCIÓN TRADING", heading_style))
        
        plan_data = [
            ["Parámetro", "Valor"],
            ["Precio de Entrada", f"${entry_price:.2f}"],
            ["Precio Stop Loss", f"${stop_loss:.2f}"],
            ["Precio Take Profit", f"${take_profit:.2f}"],
            ["Ganancia Potencial", f"+{ganancia_potencial:.2f}%"],
            ["Pérdida Máxima", f"-{perdida_potencial:.2f}%"],
            ["Tiempo Proyectado", tiempo_proyectado],
            ["Proyección de Precio", proyeccion],
            ["Recomendación", recomendable],
            ["Veredicto", recomendacion.get('recomendacion', 'N/A')],
            ["Confianza", f"{recomendacion.get('probabilidad_exito', 'N/A')}%"],
        ]
        
        plan_table = Table(plan_data, colWidths=[2.5*inch, 3.5*inch])
        plan_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        story.append(plan_table)
        story.append(Spacer(1, 0.2*inch))
        
        # SOPORTES Y RESISTENCIAS
        story.append(Paragraph("🎯 SOPORTES Y RESISTENCIAS (PIVOT POINTS)", heading_style))
        
        sr_data = [
            ["Nivel", "Precio"],
            ["Resistencia 2 (R2)", f"${soportes_resistencias.get('resistencia_2', 'N/A')}"],
            ["Resistencia 1 (R1)", f"${soportes_resistencias.get('resistencia_1', 'N/A')}"],
            ["Pivot Point", f"${soportes_resistencias.get('pivot', 'N/A')}"],
            ["Soporte 1 (S1)", f"${soportes_resistencias.get('soporte_1', 'N/A')}"],
            ["Soporte 2 (S2)", f"${soportes_resistencias.get('soporte_2', 'N/A')}"],
        ]
        
        sr_table = Table(sr_data, colWidths=[2.5*inch, 3.5*inch])
        sr_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ca02c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        story.append(sr_table)
        story.append(Spacer(1, 0.2*inch))
        
        # ANÁLISIS TÉCNICO
        story.append(Paragraph("📊 INDICADORES TÉCNICOS", heading_style))
        
        indicadores = tecnico.get('indicadores', {})
        tech_data = [["Indicador", "Valor", "Señal"]]
        
        if 'RSI' in indicadores:
            rsi = indicadores['RSI']
            tech_data.append([
                "RSI(14)",
                f"{rsi.get('valor', 'N/A')}",
                f"{rsi.get('señal', 'N/A')}"
            ])
        
        if 'MACD' in indicadores:
            macd = indicadores['MACD']
            tech_data.append([
                "MACD",
                f"MACD: {macd.get('linea_macd', 'N/A')} / Señal: {macd.get('linea_senal', 'N/A')}",
                f"{macd.get('señal', 'N/A')}"
            ])
        
        if 'STOCHASTIC' in indicadores:
            stoch = indicadores['STOCHASTIC']
            tech_data.append([
                "Stochastic",
                f"K: {stoch.get('linea_k', 'N/A')}% / D: {stoch.get('linea_d', 'N/A')}%",
                f"{stoch.get('señal', 'N/A')}"
            ])
        
        if 'MEDIAS_MOVILES' in indicadores:
            sma = indicadores['MEDIAS_MOVILES']
            tech_data.append([
                "Medias Móviles",
                f"SMA20: {sma.get('SMA_20', 'N/A')} / SMA50: {sma.get('SMA_50', 'N/A')} / SMA200: {sma.get('SMA_200', 'N/A')}",
                "Análisis"
            ])
        
        if 'VOLUMEN' in indicadores:
            vol = indicadores['VOLUMEN']
            tech_data.append([
                "Volumen",
                f"{vol.get('volumen_actual', 'N/A')} ({vol.get('relacion', 'N/A')}x promedio)",
                f"{vol.get('señal', 'N/A')}"
            ])
        
        if tech_data:
            tech_table = Table(tech_data, colWidths=[1.8*inch, 2.5*inch, 1.7*inch])
            tech_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff7f0e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            story.append(tech_table)
        
        story.append(Spacer(1, 0.2*inch))
        
        # ANÁLISIS NARRATIVO FUNDAMENTADO (NUEVO PUNTO)
        if analisis_narrativo and analisis_narrativo.strip():
            story.append(Paragraph("📝 ANÁLISIS NARRATIVO FUNDAMENTADO", heading_style))
            
            # Convertir markdown simple a HTML para el PDF de forma segura
            analisis_html = analisis_narrativo
            
            # Primero escapar & (ANTES de otras conversiones)
            analisis_html = analisis_html.replace('&', '&amp;')
            
            # Convertir **texto** a <b>texto</b>
            analisis_html = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', analisis_html)
            
            # Convertir *texto* a <i>texto</i>
            analisis_html = re.sub(r'\*(.+?)\*', r'<i>\1</i>', analisis_html)
            
            # Convertir saltos de línea a <br/>
            analisis_html = analisis_html.replace('\n\n', '<br/><br/>')
            analisis_html = analisis_html.replace('\n', '<br/>')
            
            try:
                story.append(Paragraph(analisis_html, styles['Normal']))
            except Exception as e:
                # Si hay error con HTML, usar texto plano
                self.logger.warning(f"Error rendering narrative HTML: {e}. Using plain text.")
                story.append(Paragraph(analisis_narrativo.replace('\n', '<br/>'), styles['Normal']))
            
            story.append(Spacer(1, 0.2*inch))
        
        # ANÁLISIS FUNDAMENTAL
        story.append(Paragraph("💼 ANÁLISIS FUNDAMENTAL", heading_style))
        
        fund_data = [["Métrica", "Valor"]]
        for clave, valor in fundamentales.items():
            fund_data.append([str(clave), str(valor)])
        
        if len(fund_data) > 1:
            fund_table = Table(fund_data, colWidths=[2.5*inch, 3.5*inch])
            fund_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d62728')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            story.append(fund_table)
        
        story.append(Spacer(1, 0.2*inch))
        
        # ANÁLISIS ALEXANDER (MAREA, MOVIMIENTO, FACTOR SOCIAL)
        story.append(Paragraph("🧭 ANÁLISIS ALEXANDER - METODOLOGÍA UNIFICADA", heading_style))
        
        marea = alexander.get('marea', {})
        movimiento = alexander.get('movimiento', {})
        factor_social = alexander.get('factor_social', {})
        
        # Marea
        story.append(Paragraph("🌊 MAREA (Contexto Macro)", 
                             ParagraphStyle('subheading', parent=styles['Normal'], 
                                          fontSize=11, fontName='Helvetica-Bold')))
        marea_text = f"""
        • General: {marea.get('marea_general', 'N/A')}<br/>
        • VIX: {marea.get('vix', 'N/A')}<br/>
        • Volatilidad: {marea.get('volatilidad_mercado', 'N/A')}<br/>
        • Riesgo: {marea.get('riesgo', 'N/A')}<br/>
        """
        story.append(Paragraph(marea_text, styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        
        # Movimiento
        story.append(Paragraph("📈 MOVIMIENTO (Análisis Técnico Local)", 
                             ParagraphStyle('subheading', parent=styles['Normal'], 
                                          fontSize=11, fontName='Helvetica-Bold')))
        movimiento_text = f"""
        • Tendencia: {movimiento.get('movimiento', 'N/A')} ({movimiento.get('fuerza', 'N/A')})<br/>
        • Consenso: {movimiento.get('consenso', 'N/A')}%<br/>
        • Señales Alcistas: {movimiento.get('señales_alcistas', 0)}/3<br/>
        • Señales Bajistas: {movimiento.get('señales_bajistas', 0)}/3<br/>
        """
        story.append(Paragraph(movimiento_text, styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        
        # Factor Social
        story.append(Paragraph("💼 FACTOR SOCIAL (Fundamentales)", 
                             ParagraphStyle('subheading', parent=styles['Normal'], 
                                          fontSize=11, fontName='Helvetica-Bold')))
        social_text = f"""
        • Valuación: {factor_social.get('valuacion', 'N/A')}<br/>
        • Sentimiento: {factor_social.get('sentimiento_general', 'N/A')}<br/>
        • Tamaño: {factor_social.get('tamaño', 'N/A')}<br/>
        • Solidez: {factor_social.get('solidez', 'N/A')}<br/>
        • Insider Trading: {factor_social.get('insider_sentiment', 'N/A')}<br/>
        • Analyst Rating: {factor_social.get('analyst_sentiment', 'N/A')}<br/>
        """
        story.append(Paragraph(social_text, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Disclaimer
        story.append(Paragraph("⚠️ DISCLAIMER", heading_style))
        disclaimer = """
        Este análisis es solo informativo. No constituye asesoramiento financiero.<br/>
        Todo trading implica riesgo de pérdida total del capital.<br/>
        Consulta con un asesor profesional antes de operar.<br/>
        Los resultados pasados no garantizan resultados futuros.<br/>
        Realiza tu propia investigación antes de tomar decisiones de inversión.
        """
        story.append(Paragraph(disclaimer, styles['Normal']))
        
        # Generar PDF
        try:
            doc.build(story)
            self.logger.info(f"✅ PDF generado: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"❌ Error generando PDF: {str(e)}")
            raise
