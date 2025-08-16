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
    
    def generar_examen_pdf(self, examen: Examen, clase: Clase, curso: Curso, competencia) -> str:
        """Genera un PDF imprimible del examen"""
        # Crear archivo temporal
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_path = temp_file.name
        temp_file.close()
        
        # Crear el documento PDF
        doc = SimpleDocTemplate(temp_path, pagesize=A4, 
                               rightMargin=0.75*inch, leftMargin=0.75*inch,
                               topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        story = []
        
        # Título del examen
        title_style = self.styles['Title']
        title = Paragraph(f"EXAMEN DE MATEMÁTICAS - {examen.tipo.upper()}", title_style)
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
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
            story.append(Spacer(1, 0.1*inch))
        
        story.append(Spacer(1, 0.3*inch))
        
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
        story.append(Spacer(1, 0.4*inch))
        
        # Preguntas
        question_style = self.styles['Normal']
        for i, pregunta in enumerate(examen.preguntas, 1):
            # Número y enunciado de la pregunta
            q_title = f"<b>Pregunta {i}:</b> {pregunta['enunciado']}"
            p = Paragraph(q_title, question_style)
            story.append(p)
            story.append(Spacer(1, 0.2*inch))
            
            # Espacio para desarrollo
            desarrollo = """
            <b>Desarrollo:</b><br/>
            <br/>
            ___________________________________________________________________<br/>
            <br/>
            ___________________________________________________________________<br/>
            <br/>
            ___________________________________________________________________<br/>
            <br/>
            ___________________________________________________________________<br/>
            <br/>
            ___________________________________________________________________<br/>
            """
            p = Paragraph(desarrollo, info_style)
            story.append(p)
            story.append(Spacer(1, 0.2*inch))
            
            # Recuadro para respuesta final
            respuesta_final = """
            <b>Respuesta final:</b>
            <br/>
            <br/>
            ┌─────────────────────────────────────┐<br/>
            │                                                                     │<br/>
            │                  RESPUESTA FINAL                    │<br/>
            │                                                                     │<br/>
            └─────────────────────────────────────┘
            """
            p = Paragraph(respuesta_final, info_style)
            story.append(p)
            story.append(Spacer(1, 0.4*inch))
        
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
