import os
import json
import logging
from typing import List, Dict
from google import genai
from google.genai import types
import base64

class GeminiService:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY", "default_key")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
    
    def generar_criterios_evaluacion(self, competencia: str, grado: str) -> List[str]:
        """Genera exactamente 4 criterios de evaluación para una competencia matemática específica"""
        prompt = f"""
        Eres un experto en educación matemática. Genera exactamente 4 criterios de evaluación específicos y medibles para la siguiente competencia matemática de {grado}° grado:
        
        COMPETENCIA: {competencia}
        
        Los criterios deben:
        - Ser específicos y medibles
        - Estar alineados con el nivel de {grado}° grado
        - Cubrir diferentes aspectos de la competencia
        - Usar lenguaje claro para docentes
        - Enfocarse en habilidades evaluables en un examen escrito
        
        Responde ÚNICAMENTE con una lista de exactamente 4 criterios, uno por línea, sin numeración ni viñetas.
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            if response.text:
                criterios = [c.strip() for c in response.text.strip().split('\n') if c.strip()]
                # Asegurar que tenemos exactamente 4 criterios
                if len(criterios) >= 4:
                    return criterios[:4]
                else:
                    # Si no tenemos suficientes, rellenar con criterios genéricos
                    criterios_genericos = [
                        "Identifica correctamente los conceptos matemáticos del problema",
                        "Aplica procedimientos y estrategias de resolución apropiadas", 
                        "Realiza cálculos y operaciones de manera precisa",
                        "Presenta soluciones claras y justifica el resultado obtenido"
                    ]
                    return (criterios + criterios_genericos)[:4]
            else:
                raise Exception("Respuesta vacía de la IA")
                
        except Exception as e:
            logging.error(f"Error al generar criterios: {e}")
            # Criterios por defecto
            return [
                "Comprende el problema planteado correctamente",
                "Utiliza estrategias de resolución adecuadas al grado",
                "Ejecuta los procedimientos matemáticos sin errores",
                "Presenta la respuesta de forma clara y precisa"
            ]
    
    def generar_preguntas_examen(self, competencia: str, criterios: List[str], grado: str) -> List[Dict]:
        """Genera 5 preguntas de examen basadas en los criterios de evaluación"""
        criterios_texto = '\n'.join([f"- {criterio}" for criterio in criterios])
        
        prompt = f"""
        Eres un experto en creación de evaluaciones matemáticas. Genera exactamente 5 preguntas para un examen de matemáticas de {grado}° grado.
        
        COMPETENCIA: {competencia}
        
        CRITERIOS DE EVALUACIÓN:
        {criterios_texto}
        
        Cada pregunta debe:
        - Estar alineada con la competencia y criterios
        - Ser apropiada para {grado}° grado
        - Tener un enunciado claro
        - Incluir la respuesta correcta
        - Permitir que el estudiante muestre su proceso de resolución
        
        Responde ÚNICAMENTE en formato JSON con esta estructura:
        [
            {{
                "numero": 1,
                "enunciado": "texto de la pregunta",
                "respuesta_correcta": "respuesta esperada"
            }},
            ...
        ]
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            if response.text:
                preguntas = json.loads(response.text)
                # Asegurar que tenemos exactamente 5 preguntas
                if len(preguntas) >= 5:
                    return preguntas[:5]
                else:
                    # Completar con preguntas genéricas si es necesario
                    while len(preguntas) < 5:
                        preguntas.append({
                            "numero": len(preguntas) + 1,
                            "enunciado": f"Resuelve el siguiente problema aplicando la competencia: {competencia}",
                            "respuesta_correcta": "Respuesta variable según el problema"
                        })
                    return preguntas
            else:
                raise Exception("Respuesta vacía de la IA")
                
        except Exception as e:
            logging.error(f"Error al generar preguntas: {e}")
            # Preguntas por defecto
            return [
                {
                    "numero": 1,
                    "enunciado": f"Resuelve un problema relacionado con: {competencia}",
                    "respuesta_correcta": "Variable según el contexto"
                },
                {
                    "numero": 2,
                    "enunciado": f"Aplica estrategias para resolver: {competencia}",
                    "respuesta_correcta": "Variable según el contexto"
                },
                {
                    "numero": 3,
                    "enunciado": f"Demuestra tu comprensión de: {competencia}",
                    "respuesta_correcta": "Variable según el contexto"
                },
                {
                    "numero": 4,
                    "enunciado": f"Explica tu proceso al trabajar con: {competencia}",
                    "respuesta_correcta": "Variable según el contexto"
                },
                {
                    "numero": 5,
                    "enunciado": f"Comunica tu solución para: {competencia}",
                    "respuesta_correcta": "Variable según el contexto"
                }
            ]
    
    def generar_feedback_estudiante(self, pregunta: str, respuesta_incorrecta: str, respuesta_correcta: str, grado: str) -> Dict:
        """Genera feedback personalizado para una respuesta incorrecta"""
        prompt = f"""
        Eres un tutor matemático especializado en {grado}° grado. Un estudiante respondió incorrectamente a una pregunta.
        
        PREGUNTA: {pregunta}
        RESPUESTA DEL ESTUDIANTE: {respuesta_incorrecta}
        RESPUESTA CORRECTA: {respuesta_correcta}
        
        Genera feedback constructivo que incluya:
        1. Una explicación paso a paso de cómo resolver el problema
        2. Sugerencias de recursos educativos (videos de YouTube, sitios web educativos)
        3. Ejercicios similares para practicar
        
        Responde en formato JSON:
        {{
            "explicacion": "explicación paso a paso",
            "recursos": [
                {{"tipo": "video", "titulo": "título del video", "descripcion": "descripción breve"}},
                {{"tipo": "articulo", "titulo": "título del artículo", "descripcion": "descripción breve"}}
            ],
            "ejercicios_similares": ["ejercicio 1", "ejercicio 2", "ejercicio 3"]
        }}
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            if response.text:
                return json.loads(response.text)
            else:
                raise Exception("Respuesta vacía de la IA")
                
        except Exception as e:
            logging.error(f"Error al generar feedback: {e}")
            return {
                "explicacion": "Revisa los pasos del problema y asegúrate de aplicar las estrategias correctas.",
                "recursos": [
                    {"tipo": "video", "titulo": "Recursos matemáticos", "descripcion": "Busca videos educativos relacionados con el tema"}
                ],
                "ejercicios_similares": ["Practica problemas similares", "Repasa los conceptos básicos"]
            }
    
    def analizar_examen_imagen(self, imagen_path: str, preguntas: List[Dict], tipo_examen: str) -> Dict:
        """Analiza una imagen de examen usando IA para extraer respuestas y calificar"""
        try:
            # Leer la imagen
            with open(imagen_path, "rb") as f:
                image_bytes = f.read()
            
            # Crear prompt específico para análisis de exámenes
            preguntas_texto = "\n".join([f"Pregunta {i+1}: {p['enunciado']} (Respuesta esperada: {p['respuesta_correcta']})" 
                                       for i, p in enumerate(preguntas)])
            
            prompt = f"""
            Eres un profesor de matemáticas experto en evaluar exámenes. Analiza esta imagen de un examen de matemáticas.
            
            TIPO DE EXAMEN: {tipo_examen}
            
            PREGUNTAS DEL EXAMEN:
            {preguntas_texto}
            
            INSTRUCCIONES:
            1. Analiza cuidadosamente la imagen del examen
            2. Identifica las respuestas escritas por el estudiante para cada pregunta
            3. Evalúa si las respuestas son correctas, parcialmente correctas o incorrectas
            4. Para el PRETEST: Solo identifica respuestas y da una calificación numérica simple
            5. Para el POSTEST: Además proporciona feedback detallado
            
            Responde en formato JSON:
            {{
                "respuestas_detectadas": [
                    {{
                        "pregunta": 1,
                        "respuesta_estudiante": "respuesta que escribió el estudiante",
                        "es_correcta": true/false,
                        "puntos": "puntos asignados de 10",
                        "justificacion": "breve explicación de la evaluación"
                    }}
                ],
                "calificacion_total": "calificación sobre 20",
                "observaciones_generales": "comentarios sobre la presentación, claridad, etc.",
                "feedback_detallado": "solo para postest - feedback constructivo"
            }}
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.5-pro",  # Usar modelo más potente para análisis de imágenes
                contents=[
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type="image/jpeg",
                    ),
                    prompt
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            if response.text:
                resultado = json.loads(response.text)
                logging.info(f"Análisis de examen completado: {resultado['calificacion_total']} puntos")
                return resultado
            else:
                raise Exception("Respuesta vacía del modelo")
                
        except Exception as e:
            logging.error(f"Error al analizar imagen del examen: {e}")
            # Retornar resultado por defecto en caso de error
            return {
                "respuestas_detectadas": [
                    {
                        "pregunta": i+1,
                        "respuesta_estudiante": "No se pudo detectar la respuesta",
                        "es_correcta": False,
                        "puntos": "5",
                        "justificacion": "Error en el análisis automático"
                    } for i in range(len(preguntas))
                ],
                "calificacion_total": "10",
                "observaciones_generales": "Error en el análisis automático. Revisión manual requerida.",
                "feedback_detallado": "No disponible debido a error técnico"
            }
    
    def procesar_examen_postest(self, imagen_path: str, preguntas: List[Dict], pretest_resultado: Dict = None) -> Dict:
        """Procesa un postest con comparación al pretest para generar feedback de progreso"""
        resultado_base = self.analizar_examen_imagen(imagen_path, preguntas, "postest")
        
        if pretest_resultado:
            # Calcular mejora
            calificacion_pretest = float(pretest_resultado.get('calificacion_total', 0))
            calificacion_postest = float(resultado_base.get('calificacion_total', 0))
            mejora = calificacion_postest - calificacion_pretest
            
            # Agregar análisis de progreso
            resultado_base['analisis_progreso'] = {
                "calificacion_pretest": calificacion_pretest,
                "calificacion_postest": calificacion_postest,
                "mejora_puntos": mejora,
                "porcentaje_mejora": round((mejora / 20) * 100, 1) if mejora > 0 else 0,
                "interpretacion": self._interpretar_progreso(mejora)
            }
        
        return resultado_base
    
    def _interpretar_progreso(self, mejora: float) -> str:
        """Interpreta el progreso del estudiante"""
        if mejora >= 5:
            return "Excelente progreso! Has mejorado significativamente."
        elif mejora >= 2:
            return "Buen progreso. Continúa trabajando en estas áreas."
        elif mejora >= 0:
            return "Progreso moderado. Sigue practicando para mejorar."
        else:
            return "Necesitas más práctica. Revisa los conceptos fundamentales."
