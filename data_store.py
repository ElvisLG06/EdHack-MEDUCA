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
        
        # Crear usuarios de muestra
        docente = User("doc1", "profesor", "profesor@meduca.edu", "docente", generate_password_hash("123456"))
        estudiante1 = User("est1", "juan", "juan@estudiante.edu", "estudiante", generate_password_hash("123456"))
        estudiante2 = User("est2", "maria", "maria@estudiante.edu", "estudiante", generate_password_hash("123456"))
        
        self.add_user(docente)
        self.add_user(estudiante1)
        self.add_user(estudiante2)
    
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
