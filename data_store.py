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
        """Inicializa datos de muestra para testing"""
        from werkzeug.security import generate_password_hash
        import uuid
        from datetime import datetime, timedelta
        
        # Crear usuarios de muestra - 1 docente + 8 estudiantes
        docente = User("doc1", "profesor", "profesor@meduca.edu", "docente", generate_password_hash("123456"))
        self.add_user(docente)
        
        # 8 estudiantes como pidió el usuario
        estudiantes_data = [
            ("est1", "juan", "juan@estudiante.edu"),
            ("est2", "maria", "maria@estudiante.edu"),
            ("est3", "carlos", "carlos@estudiante.edu"),
            ("est4", "ana", "ana@estudiante.edu"),
            ("est5", "luis", "luis@estudiante.edu"),
            ("est6", "sofia", "sofia@estudiante.edu"),
            ("est7", "diego", "diego@estudiante.edu"),
            ("est8", "valentina", "valentina@estudiante.edu")
        ]
        
        estudiantes = []
        for user_id, username, email in estudiantes_data:
            estudiante = User(user_id, username, email, "estudiante", generate_password_hash("123456"))
            self.add_user(estudiante)
            estudiantes.append(estudiante)
        
        # Crear un curso de muestra
        curso = Curso("curso1", "Matemáticas 5to Grado", "5", "2024", docente.id)
        self.add_curso(curso)
        
        # Inscribir todos los estudiantes al curso
        for estudiante in estudiantes:
            inscripcion = Inscripcion(estudiante.id, curso.id)
            self.add_inscripcion(inscripcion)
        
        # Crear 4 clases como pidió el usuario
        clases_data = [
            ("clase1", "Fracciones y Números Decimales", "comp_1_5"),
            ("clase2", "Operaciones con Números Naturales", "comp_1_5"), 
            ("clase3", "Patrones y Secuencias", "comp_2_5"),
            ("clase4", "Geometría Básica", "comp_4_5")
        ]
        
        clases = []
        for clase_id, nombre, competencia_id in clases_data:
            clase = Clase(clase_id, nombre, curso.id, competencia_id)
            self.add_clase(clase)
            clases.append(clase)
        
        # Crear exámenes (pretest y postest) para cada clase
        for i, clase in enumerate(clases):
            # Pretest
            pretest_id = f"pretest_{i+1}"
            pretest = Examen(
                pretest_id, 
                clase.id, 
                "pretest", 
                ["Evaluar conocimientos previos", "Identificar fortalezas", "Detectar áreas de mejora"],
                [
                    {"numero": 1, "enunciado": f"Resuelve el siguiente problema de {clase.nombre.lower()}", "respuesta_correcta": "Respuesta modelo"},
                    {"numero": 2, "enunciado": f"Explica tu procedimiento para resolver {clase.nombre.lower()}", "respuesta_correcta": "Explicación modelo"}
                ]
            )
            self.add_examen(pretest)
            
            # Postest
            postest_id = f"postest_{i+1}"
            postest = Examen(
                postest_id,
                clase.id,
                "postest",
                ["Evaluar aprendizaje adquirido", "Medir progreso", "Validar competencias"],
                [
                    {"numero": 1, "enunciado": f"Aplica lo aprendido en {clase.nombre.lower()}", "respuesta_correcta": "Aplicación correcta"},
                    {"numero": 2, "enunciado": f"Demuestra tu dominio de {clase.nombre.lower()}", "respuesta_correcta": "Demostración completa"}
                ]
            )
            self.add_examen(postest)
            
            # Crear exámenes resueltos para algunos estudiantes
            for j, estudiante in enumerate(estudiantes[:6]):  # Solo 6 de 8 estudiantes tienen exámenes
                # Pretest resuelto
                pretest_resuelto_id = f"pretest_resuelto_{i+1}_{j+1}"
                pretest_resuelto = ExamenResuelto(
                    pretest_resuelto_id,
                    pretest_id,
                    estudiante.id,
                    f"static/uploads/pretest_{clase.id}_{estudiante.id}.jpg",
                    {"respuestas": "Pendiente de análisis OCR"},
                    15.0 + (j * 1.5)  # Calificaciones variadas
                )
                pretest_resuelto.estado = "completado"
                self.add_examen_resuelto(pretest_resuelto)
                
                # Postest resuelto (solo para algunos)
                if j < 4:  # Solo 4 estudiantes tienen postest
                    postest_resuelto_id = f"postest_resuelto_{i+1}_{j+1}"
                    postest_resuelto = ExamenResuelto(
                        postest_resuelto_id,
                        postest_id,
                        estudiante.id,
                        f"static/uploads/postest_{clase.id}_{estudiante.id}.jpg",
                        {"respuestas": "Pendiente de análisis OCR"},
                        17.0 + (j * 1.0)  # Mejores calificaciones en postest
                    )
                    postest_resuelto.estado = "completado"
                    self.add_examen_resuelto(postest_resuelto)
    
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
