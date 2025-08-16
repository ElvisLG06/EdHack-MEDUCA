from datetime import datetime
from typing import Dict, List, Optional

class User:
    def __init__(self, user_id: str, username: str, email: str, role: str, password_hash: str):
        self.id = user_id
        self.username = username
        self.email = email
        self.role = role  # 'docente' or 'estudiante'
        self.password_hash = password_hash
        self.created_at = datetime.now()

class Curso:
    def __init__(self, curso_id: str, nombre: str, grado: str, ano_academico: str, docente_id: str):
        self.id = curso_id
        self.nombre = nombre
        self.grado = grado  # '1', '2', '3', etc.
        self.ano_academico = ano_academico
        self.docente_id = docente_id
        self.created_at = datetime.now()

class Clase:
    def __init__(self, clase_id: str, nombre: str, curso_id: str, competencia_id: str):
        self.id = clase_id
        self.nombre = nombre
        self.curso_id = curso_id
        self.competencia_id = competencia_id
        self.created_at = datetime.now()

class Examen:
    def __init__(self, examen_id: str, clase_id: str, tipo: str, criterios: List[str], preguntas: List[Dict]):
        self.id = examen_id
        self.clase_id = clase_id
        self.tipo = tipo  # 'pretest' or 'postest'
        self.criterios = criterios
        self.preguntas = preguntas
        self.created_at = datetime.now()

class ExamenResuelto:
    def __init__(self, resuelto_id: str, examen_id: str, estudiante_id: str, imagen_path: str, respuestas: Dict, calificacion: Optional[float] = None, tipo_aplicacion: str = 'pretest'):
        self.id = resuelto_id
        self.examen_id = examen_id
        self.estudiante_id = estudiante_id
        self.imagen_path = imagen_path
        self.respuestas = respuestas
        self.calificacion = calificacion
        self.tipo_aplicacion = tipo_aplicacion  # 'pretest' o 'postest'
        self.feedback = None
        self.estado = "pendiente"  # "pendiente", "completado", "procesando"
        self.analisis_ia = None  # Resultados del análisis de IA
        self.created_at = datetime.now()

class Inscripcion:
    def __init__(self, estudiante_id: str, curso_id: str):
        self.estudiante_id = estudiante_id
        self.curso_id = curso_id
        self.created_at = datetime.now()
