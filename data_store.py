from typing import Dict, List, Optional
from models import User, Curso, Clase, Examen, ExamenResuelto, Inscripcion

class DataStore:
    """Simple in-memory data store for the MVP"""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.users_by_username: Dict[str, User] = {}
        self.users_by_email: Dict[str, User] = {}
        self.cursos: Dict[str, Curso] = {}
        self.clases: Dict[str, Clase] = {}
        self.examenes: Dict[str, Examen] = {}
        self.examenes_resueltos: Dict[str, ExamenResuelto] = {}
        self.inscripciones: List[Inscripcion] = []
        
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Inicializa datos hardcodeados para Juan y María - 6to grado"""
        from werkzeug.security import generate_password_hash
        import uuid
        from datetime import datetime, timedelta
        
        # Crear docente
        docente = User("doc1", "profesor", "profesor@meduca.edu", "docente", generate_password_hash("123456"))
        self.add_user(docente)
        
        # Solo Juan y María
        estudiantes_data = [
            ("est1", "juan", "juan@estudiante.edu"),
            ("est2", "maria", "maria@estudiante.edu")
        ]
        
        estudiantes = []
        for user_id, username, email in estudiantes_data:
            estudiante = User(user_id, username, email, "estudiante", generate_password_hash("123456"))
            self.add_user(estudiante)
            estudiantes.append(estudiante)
        
        # Curso de 6to grado
        curso = Curso("curso1", "Matemáticas 6to Grado", "6", "2024", docente.id)
        self.add_curso(curso)
        
        # Inscribir Juan y María al curso
        for estudiante in estudiantes:
            inscripcion = Inscripcion(estudiante.id, curso.id)
            self.add_inscripcion(inscripcion)
        
        # Solo Clase 1 con la primera competencia
        clase = Clase("clase1", "Clase 1", curso.id, "comp_1_6")
        self.add_clase(clase)
        
        # Crear examen unificado con criterios y preguntas hardcodeados
        examen_id = "examen1"
        examen = Examen(
            examen_id, 
            clase.id, 
            "unificado", 
            [
                "Comprende y aplica los conceptos de números naturales correctamente",
                "Utiliza estrategias de resolución apropiadas para 6to grado",
                "Ejecuta los procedimientos matemáticos sin errores",
                "Presenta la respuesta de forma clara y justifica el proceso"
            ],
            [
                {"numero": 1, "enunciado": "Resuelve la siguiente operación: 245 + 378 + 156", "respuesta_correcta": "779"},
                {"numero": 2, "enunciado": "Calcula: 15 × 24", "respuesta_correcta": "360"},
                {"numero": 3, "enunciado": "Divide 648 entre 8", "respuesta_correcta": "81"},
                {"numero": 4, "enunciado": "Resuelve: 3/4 + 1/2", "respuesta_correcta": "5/4 o 1.25"},
                {"numero": 5, "enunciado": "Encuentra el perímetro de un rectángulo de 12 cm de largo y 8 cm de ancho", "respuesta_correcta": "40 cm"}
            ]
        )
        self.add_examen(examen)
        
        # Crear exámenes resueltos hardcodeados para Juan y María
        
        # JUAN - Pretest (nota 15)
        juan_pretest_id = "juan_pretest_1"
        juan_pretest = ExamenResuelto(
            juan_pretest_id,
            examen_id,
            "est1",  # Juan
            "juan_pretest.jpg",
            {"respuestas": "Pendiente de análisis OCR"},
            15.0
        )
        juan_pretest.estado = "completado"
        juan_pretest.tipo_aplicacion = "pretest"
        juan_pretest.analisis_ia = {
            "respuestas_detectadas": [
                {"pregunta": 1, "respuesta_estudiante": "779", "es_correcta": True, "puntos": "10", "justificacion": "Respuesta correcta"},
                {"pregunta": 2, "respuesta_estudiante": "360", "es_correcta": True, "puntos": "10", "justificacion": "Respuesta correcta"},
                {"pregunta": 3, "respuesta_estudiante": "82", "es_correcta": False, "puntos": "5", "justificacion": "Error en el cálculo de división"},
                {"pregunta": 4, "respuesta_estudiante": "1", "es_correcta": False, "puntos": "3", "justificacion": "No simplificó correctamente la fracción"},
                {"pregunta": 5, "respuesta_estudiante": "20 cm", "es_correcta": False, "puntos": "2", "justificacion": "Calculó solo el área, no el perímetro"}
            ],
            "calificacion_total": "15",
            "observaciones_generales": "Juan muestra buena comprensión en operaciones básicas pero tiene dificultades con fracciones y conceptos geométricos."
        }
        self.add_examen_resuelto(juan_pretest)
        
        # JUAN - Postest (nota 15 con feedback de IA y comentarios del docente)
        juan_postest_id = "juan_postest_1"
        juan_postest = ExamenResuelto(
            juan_postest_id,
            examen_id,
            "est1",  # Juan
            "juan_postest.jpg",
            {"respuestas": "Pendiente de análisis OCR"},
            15.0
        )
        juan_postest.estado = "completado"
        juan_postest.tipo_aplicacion = "postest"
        juan_postest.analisis_ia = {
            "respuestas_detectadas": [
                {"pregunta": 1, "respuesta_estudiante": "779", "es_correcta": True, "puntos": "10", "justificacion": "Respuesta correcta"},
                {"pregunta": 2, "respuesta_estudiante": "365", "es_correcta": False, "puntos": "5", "justificacion": "Error en la multiplicación"},
                {"pregunta": 3, "respuesta_estudiante": "81", "es_correcta": True, "puntos": "10", "justificacion": "Respuesta correcta"},
                {"pregunta": 4, "respuesta_estudiante": "1.5", "es_correcta": False, "puntos": "3", "justificacion": "Error en la suma de fracciones"},
                {"pregunta": 5, "respuesta_estudiante": "96 cm²", "es_correcta": False, "puntos": "2", "justificacion": "Calculó el área en lugar del perímetro"}
            ],
            "calificacion_total": "15",
            "observaciones_generales": "Juan ha mejorado en división pero aún tiene dificultades con fracciones y confunde área con perímetro.",
            "feedback_detallado": "Juan, has mostrado progreso en algunas áreas pero necesitas reforzar el trabajo con fracciones y los conceptos geométricos. Te recomiendo practicar más estos temas."
        }
        juan_postest.comentarios_docente = "Juan, has mejorado en operaciones de división, pero necesitas más práctica con fracciones. Confundes frecuentemente área y perímetro. Te sugiero revisar estos conceptos."
        juan_postest.puntos_mejora = "1. Practicar suma y resta de fracciones\n2. Diferenciar claramente área y perímetro\n3. Verificar cálculos de multiplicación"
        self.add_examen_resuelto(juan_postest)
        
        # MARÍA - Pretest (nota 15)
        maria_pretest_id = "maria_pretest_1"
        maria_pretest = ExamenResuelto(
            maria_pretest_id,
            examen_id,
            "est2",  # María
            "maria_pretest.jpg",
            {"respuestas": "Pendiente de análisis OCR"},
            15.0
        )
        maria_pretest.estado = "completado"
        maria_pretest.tipo_aplicacion = "pretest"
        maria_pretest.analisis_ia = {
            "respuestas_detectadas": [
                {"pregunta": 1, "respuesta_estudiante": "780", "es_correcta": False, "puntos": "5", "justificacion": "Error de cálculo en la suma"},
                {"pregunta": 2, "respuesta_estudiante": "360", "es_correcta": True, "puntos": "10", "justificacion": "Respuesta correcta"},
                {"pregunta": 3, "respuesta_estudiante": "81", "es_correcta": True, "puntos": "10", "justificacion": "Respuesta correcta"},
                {"pregunta": 4, "respuesta_estudiante": "5/4", "es_correcta": True, "puntos": "10", "justificacion": "Respuesta correcta"},
                {"pregunta": 5, "respuesta_estudiante": "40 cm", "es_correcta": True, "puntos": "10", "justificacion": "Respuesta correcta"}
            ],
            "calificacion_total": "15",
            "observaciones_generales": "María muestra excelente comprensión en la mayoría de temas pero tiene errores de cálculo en operaciones básicas."
        }
        self.add_examen_resuelto(maria_pretest)
        
        # MARÍA - Postest (nota 15 con feedback de IA y comentarios del docente)
        maria_postest_id = "maria_postest_1"
        maria_postest = ExamenResuelto(
            maria_postest_id,
            examen_id,
            "est2",  # María
            "maria_postest.jpg",
            {"respuestas": "Pendiente de análisis OCR"},
            15.0
        )
        maria_postest.estado = "completado"
        maria_postest.tipo_aplicacion = "postest"
        maria_postest.analisis_ia = {
            "respuestas_detectadas": [
                {"pregunta": 1, "respuesta_estudiante": "779", "es_correcta": True, "puntos": "10", "justificacion": "Respuesta correcta"},
                {"pregunta": 2, "respuesta_estudiante": "360", "es_correcta": True, "puntos": "10", "justificacion": "Respuesta correcta"},
                {"pregunta": 3, "respuesta_estudiante": "82", "es_correcta": False, "puntos": "5", "justificacion": "Error en el cálculo de división"},
                {"pregunta": 4, "respuesta_estudiante": "1.25", "es_correcta": True, "puntos": "10", "justificacion": "Respuesta correcta"},
                {"pregunta": 5, "respuesta_estudiante": "40 cm", "es_correcta": True, "puntos": "10", "justificacion": "Respuesta correcta"}
            ],
            "calificacion_total": "15",
            "observaciones_generales": "María ha mejorado en operaciones básicas pero aún comete errores de cálculo en división.",
            "feedback_detallado": "María, tu comprensión conceptual es excelente, pero necesitas ser más cuidadosa con los cálculos. Revisa siempre tus operaciones."
        }
        maria_postest.comentarios_docente = "María, tu comprensión de los conceptos es muy buena. El problema principal son los errores de cálculo. Te recomiendo verificar siempre tus operaciones paso a paso."
        maria_postest.puntos_mejora = "1. Verificar cálculos de división\n2. Revisar operaciones paso a paso\n3. Practicar más ejercicios de división"
        self.add_examen_resuelto(maria_postest)
    
    # User methods
    def add_user(self, user: User):
        self.users[user.id] = user
        self.users_by_username[user.username] = user
        self.users_by_email[user.email] = user
    
    def get_user(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.users_by_username.get(username)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.users_by_email.get(email)
    
    # Curso methods
    def add_curso(self, curso: Curso):
        self.cursos[curso.id] = curso
    
    def get_curso(self, curso_id: str) -> Optional[Curso]:
        return self.cursos.get(curso_id)
    
    def get_cursos_by_docente(self, docente_id: str) -> List[Curso]:
        return [curso for curso in self.cursos.values() if curso.docente_id == docente_id]
    
    # Clase methods
    def add_clase(self, clase: Clase):
        self.clases[clase.id] = clase
    
    def get_clase(self, clase_id: str) -> Optional[Clase]:
        return self.clases.get(clase_id)
    
    def get_clases_by_curso(self, curso_id: str) -> List[Clase]:
        return [clase for clase in self.clases.values() if clase.curso_id == curso_id]
    
    # Examen methods
    def add_examen(self, examen: Examen):
        self.examenes[examen.id] = examen
    
    def get_examen(self, examen_id: str) -> Optional[Examen]:
        return self.examenes.get(examen_id)
    
    def get_examenes_by_clase(self, clase_id: str) -> List[Examen]:
        return [examen for examen in self.examenes.values() if examen.clase_id == clase_id]
    
    # ExamenResuelto methods
    def add_examen_resuelto(self, examen_resuelto: ExamenResuelto):
        self.examenes_resueltos[examen_resuelto.id] = examen_resuelto
    
    def get_examen_resuelto(self, resuelto_id: str) -> Optional[ExamenResuelto]:
        return self.examenes_resueltos.get(resuelto_id)
    
    def get_examenes_resueltos_by_estudiante(self, estudiante_id: str) -> List[ExamenResuelto]:
        return [er for er in self.examenes_resueltos.values() if er.estudiante_id == estudiante_id]
    
    def get_examenes_resueltos_by_examen(self, examen_id: str) -> List[ExamenResuelto]:
        return [er for er in self.examenes_resueltos.values() if er.examen_id == examen_id]
    
    # Inscripcion methods
    def add_inscripcion(self, inscripcion: Inscripcion):
        # Evitar inscripciones duplicadas
        existing = next((i for i in self.inscripciones 
                        if i.estudiante_id == inscripcion.estudiante_id 
                        and i.curso_id == inscripcion.curso_id), None)
        if not existing:
            self.inscripciones.append(inscripcion)
    
    def get_inscripciones_by_estudiante(self, estudiante_id: str) -> List[Inscripcion]:
        return [i for i in self.inscripciones if i.estudiante_id == estudiante_id]
    
    def get_inscripciones_by_curso(self, curso_id: str) -> List[Inscripcion]:
        return [i for i in self.inscripciones if i.curso_id == curso_id]
    
    def get_examen_resuelto_by_estudiante_examen(self, estudiante_id: str, examen_id: str) -> Optional[ExamenResuelto]:
        """Obtiene el examen resuelto de un estudiante para un examen específico"""
        return next((er for er in self.examenes_resueltos.values() 
                    if er.estudiante_id == estudiante_id and er.examen_id == examen_id), None)
    
    def get_estudiantes_by_estado_examen(self, examen_id: str, estado: str = "completado") -> List[str]:
        """Obtiene lista de IDs de estudiantes que han completado un examen"""
        return [er.estudiante_id for er in self.examenes_resueltos.values() 
                if er.examen_id == examen_id and er.estado == estado]
