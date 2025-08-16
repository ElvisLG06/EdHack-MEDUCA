#!/usr/bin/env python3
"""
Script para crear imágenes de ejemplo de exámenes de Juan y María
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_exam_image(filename, student_name, exam_type, answers):
    """Crea una imagen de examen con las respuestas del estudiante"""
    
    # Crear imagen blanca
    width, height = 800, 1000
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Intentar usar una fuente del sistema, o usar la predeterminada
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
        title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()
    
    # Título
    title = f"Examen de Matemáticas - {student_name.title()} ({exam_type.upper()})"
    draw.text((50, 30), title, fill='black', font=title_font)
    
    # Preguntas y respuestas
    questions = [
        "1. Resuelve: 245 + 378 + 156 =",
        "2. Calcula: 15 × 24 =",
        "3. Divide: 648 ÷ 8 =",
        "4. Resuelve: 3/4 + 1/2 =",
        "5. Perímetro rectángulo 12×8 cm ="
    ]
    
    y_position = 100
    for i, (question, answer) in enumerate(zip(questions, answers)):
        # Pregunta
        draw.text((50, y_position), question, fill='black', font=font)
        
        # Respuesta del estudiante
        answer_text = f"Respuesta: {answer}"
        draw.text((50, y_position + 30), answer_text, fill='blue', font=font)
        
        y_position += 80
    
    # Guardar imagen
    filepath = os.path.join('static', 'uploads', filename)
    image.save(filepath)
    print(f"Imagen creada: {filepath}")

def main():
    """Crea todas las imágenes de ejemplo"""
    
    # Asegurar que el directorio existe
    os.makedirs('static/uploads', exist_ok=True)
    
    # Juan - Pretest
    juan_pretest_answers = ["779", "360", "82", "1", "20 cm"]
    create_exam_image("juan_pretest.jpg", "Juan", "pretest", juan_pretest_answers)
    
    # Juan - Postest
    juan_postest_answers = ["779", "365", "81", "1.5", "96 cm²"]
    create_exam_image("juan_postest.jpg", "Juan", "postest", juan_postest_answers)
    
    # María - Pretest
    maria_pretest_answers = ["780", "360", "81", "5/4", "40 cm"]
    create_exam_image("maria_pretest.jpg", "María", "pretest", maria_pretest_answers)
    
    # María - Postest
    maria_postest_answers = ["779", "360", "82", "1.25", "40 cm"]
    create_exam_image("maria_postest.jpg", "María", "postest", maria_postest_answers)
    
    print("✅ Todas las imágenes de ejemplo han sido creadas")

if __name__ == "__main__":
    main()
