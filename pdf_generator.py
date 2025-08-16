from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame
from reportlab.lib import colors
import tempfile
import os
from models import Examen, Clase, Curso

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
    
    def generar_examen_pdf(self, examen: Examen, clase: Clase, curso: Curso, competencia, tipo_examen: str = None) -> str:
        """Genera un PDF imprimible del examen - Máximo 2 páginas"""
        # Crear archivo temporal
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_path = temp_file.name
        temp_file.close()
        
        # Crear el documento PDF - Máximo 2 páginas
        doc = SimpleDocTemplate(temp_path, pagesize=A4, 
                               rightMargin=0.5*inch, leftMargin=0.5*inch,
                               topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        story = []
        
        # Título del examen
        title_style = self.styles['Title']
        # Usar el tipo especificado o el tipo del examen
        tipo_display = tipo_examen.upper() if tipo_examen else examen.tipo.upper()
        title = Paragraph(f"EXAMEN DE MATEMÁTICAS - {tipo_display}", title_style)
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Información del examen
        info_style = self.styles['Normal']
        info_lines = [
            f"<b>Curso:</b> {curso.nombre} - {curso.grado}° grado",
            f"<b>Clase:</b> {clase.nombre}",
            f"<b>Competencia:</b> {competencia['nombre'] if competencia else 'No definida'}",
            f"<b>Año Académico:</b> {curso.ano_academico}",
            f"<b>Fecha:</b> _________________",
            f"<b>Nombre del Estudiante:</b> _________________________________"
        ]
        
        for line in info_lines:
            p = Paragraph(line, info_style)
            story.append(p)
            story.append(Spacer(1, 0.05*inch))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Instrucciones
        instrucciones = """
        <b>INSTRUCCIONES:</b><br/>
        • Lee cuidadosamente cada pregunta antes de responder<br/>
        • Desarrolla tu procedimiento en el espacio provisto<br/>
        • Escribe tu respuesta final en el recuadro correspondiente<br/>
        • Usa lápiz para poder borrar si es necesario
        """
        p = Paragraph(instrucciones, info_style)
        story.append(p)
        story.append(Spacer(1, 0.3*inch))
        
        # Preguntas - Limitado para que quepa en 2 páginas
        question_style = self.styles['Normal']
        max_preguntas = min(len(examen.preguntas), 2)  # Máximo 2 preguntas para que quepa
        
        for i in range(max_preguntas):
            pregunta = examen.preguntas[i]
            # Número y enunciado de la pregunta
            q_title = f"<b>Pregunta {i+1}:</b> {pregunta['enunciado']}"
            p = Paragraph(q_title, question_style)
            story.append(p)
            story.append(Spacer(1, 0.15*inch))
            
            # Espacio para desarrollo - SIN LÍNEAS, más compacto
            desarrollo = """
            <b>Desarrollo:</b><br/>
            <br/><br/><br/><br/><br/><br/>
            """
            p = Paragraph(desarrollo, info_style)
            story.append(p)
            story.append(Spacer(1, 0.1*inch))
            
            # Recuadro para respuesta final - SIN LÍNEAS
            respuesta_final = """
            <b>Respuesta final:</b><br/>
            <br/><br/><br/>
            """
            p = Paragraph(respuesta_final, info_style)
            story.append(p)
            if i < max_preguntas - 1:  # No agregar espacio después de la última pregunta
                story.append(Spacer(1, 0.2*inch))
        
        # Construir PDF
        doc.build(story)
        return temp_path
    
    def generar_reporte_resultados(self, resultados_clase: dict) -> str:
        """Genera un reporte PDF con los resultados de una clase"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_path = temp_file.name
        temp_file.close()
        
        # Implementar generación de reporte de resultados
        # Por ahora, generar un PDF básico
        c = canvas.Canvas(temp_path, pagesize=letter)
        c.drawString(100, 750, "REPORTE DE RESULTADOS")
        c.drawString(100, 720, f"Clase: {resultados_clase.get('nombre_clase', 'N/A')}")
        c.drawString(100, 700, f"Promedio general: {resultados_clase.get('promedio', 'N/A')}")
        c.save()
        
        return temp_path