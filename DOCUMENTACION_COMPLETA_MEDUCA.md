# MEDUCA - Sistema de Evaluación Matemática Inteligente
## Documentación Completa del Sistema

### RESUMEN EJECUTIVO

MEDUCA (Sistema de Evaluación Matemática Inteligente) es una plataforma web educativa desarrollada en Flask que permite a docentes de matemáticas de primaria (grados 1-6) y secundaria (grados 1-5) crear exámenes inteligentes basados en competencias matemáticas, gestionar estudiantes, y proporcionar retroalimentación automatizada usando IA. El sistema utiliza un enfoque de **examen unificado** donde el mismo examen sirve tanto para pretest como postest, diferenciándose únicamente en el momento de aplicación y análisis.

### ARQUITECTURA DEL SISTEMA

#### Stack Tecnológico
- **Backend**: Flask (Python 3.11)
- **IA**: Google Gemini API (gemini-2.5-flash, gemini-2.5-pro)
- **Frontend**: Bootstrap 5.3 + Vanilla JavaScript + Feather Icons
- **PDF**: ReportLab para generación de exámenes imprimibles
- **Almacenamiento**: In-memory con modelos Python (MVP)
- **Archivos**: Sistema local para imágenes de exámenes
- **Servidor**: Gunicorn con binding a 0.0.0.0:5000

#### Estructura de Archivos Principales

```
/
├── app.py                          # Configuración principal Flask
├── routes.py                       # Todas las rutas y controladores
├── models.py                       # Modelos de datos
├── data_store.py                   # Almacenamiento in-memory + datos de prueba
├── gemini_service.py               # Integración con Google Gemini IA
├── pdf_generator.py                # Generación de PDFs de exámenes
├── competencias_matematicas.py     # Competencias por grado
├── static/
│   ├── css/custom.css              # Estilos personalizados
│   └── uploads/                    # Imágenes de exámenes subidos
└── templates/
    ├── base.html                   # Template base
    ├── login.html                  # Autenticación
    ├── dashboard_docente.html      # Dashboard para profesores
    ├── dashboard_estudiante.html   # Dashboard para estudiantes
    ├── generar_examen.html         # Creación de exámenes con IA
    ├── seleccionar_tipo_descarga.html # Selector de pretest/postest para PDF
    ├── subir_examenes.html         # Subida de exámenes resueltos
    ├── ver_examenes_subidos.html   # Visualización de exámenes subidos
    ├── feedback_estudiante.html    # Retroalimentación detallada
    └── [otros templates]
```

### FLUJO PRINCIPAL DEL SISTEMA

#### 1. GESTIÓN DE USUARIOS Y CURSOS
- **Registro/Login**: Sistema de autenticación con roles (docente/estudiante)
- **Creación de Cursos**: Docentes crean cursos especificando grado y materia
- **Gestión de Clases**: Cada clase se asocia a UNA competencia matemática específica
- **Inscripción de Estudiantes**: Docentes inscriben estudiantes por email

#### 2. CREACIÓN DE EXÁMENES UNIFICADOS (NUEVA IMPLEMENTACIÓN)
**Característica Clave**: Un solo examen por clase que sirve para pretest Y postest

1. **Generación de Criterios con IA**:
   ```python
   # En gemini_service.py
   def generar_criterios_evaluacion(self, competencia_info: Dict, grado: str) -> List[str]:
       # Genera exactamente 4 criterios específicos para la competencia
   ```

2. **Generación de Preguntas con IA**:
   ```python
   def generar_preguntas_examen(self, criterios: List[str], competencia_info: Dict, grado: str) -> List[Dict]:
       # Genera 5 preguntas alineadas con los criterios
   ```

3. **Creación del Examen**:
   - Tipo: `"unificado"` (ya no se distingue en creación)
   - Criterios: Exactamente 4 criterios generados por IA
   - Preguntas: 5 preguntas con respuestas esperadas
   - PDF: Máximo 2 páginas, espacios en blanco sin líneas

#### 3. DESCARGA DE EXÁMENES CON SELECCIÓN DE TIPO
**Flujo Mejorado**:
1. Docente hace clic en "Descargar PDF"
2. Sistema muestra `seleccionar_tipo_descarga.html`
3. Docente elige "Pretest" o "Postest"
4. PDF se genera con el tipo seleccionado en el encabezado
5. Archivo descarga: `examen_[tipo]_[nombre_clase].pdf`

```python
# En routes.py
@app.route('/descargar_examen/<examen_id>')
@app.route('/descargar_examen/<examen_id>/<tipo_descarga>')
def descargar_examen(examen_id, tipo_descarga=None):
    if not tipo_descarga:
        return render_template('seleccionar_tipo_descarga.html', ...)
    # Generar PDF con tipo específico
```

#### 4. APLICACIÓN Y SUBIDA DE EXÁMENES
**Proceso de Subida Mejorado**:
1. Docente fotografía exámenes físicos resueltos
2. En `subir_examenes.html`, selecciona tipo de aplicación:
   - **Pretest**: Antes de enseñar la competencia
   - **Postest**: Después de enseñar la competencia
3. Selecciona estudiante y sube imagen
4. Sistema almacena con `tipo_aplicacion` (pretest/postest)

```python
# En routes.py - subir_examen_resuelto()
tipo_aplicacion = request.form.get('tipo_aplicacion', 'pretest')
# El análisis de IA depende del tipo_aplicacion, no del examen.tipo
```

#### 5. ANÁLISIS INTELIGENTE DIFERENCIADO
**Análisis para Pretest**:
- IA analiza respuestas básicamente
- Califica respuestas como correctas/incorrectas
- NO proporciona feedback detallado
- Almacena resultados para comparación futura

**Análisis para Postest**:
- IA hace análisis completo comparando con pretest del mismo estudiante
- Genera feedback detallado sobre progreso
- Identifica mejoras y áreas de atención
- Proporciona sugerencias de aprendizaje

```python
# En gemini_service.py
def analizar_examen_imagen(self, imagen_path: str, preguntas: List[Dict], tipo_examen: str):
    if tipo_examen == 'pretest':
        # Análisis básico sin feedback extenso
    else:
        # Análisis completo con feedback detallado

def procesar_examen_postest(self, imagen_path: str, preguntas: List[Dict], pretest_resultado: Dict):
    # Comparación detallada pretest vs postest
```

### MODELOS DE DATOS

```python
class User:
    id, username, email, role, password_hash, created_at

class Curso:
    id, nombre, grado, ano_academico, docente_id, created_at

class Clase:
    id, nombre, curso_id, competencia_id, created_at

class Examen:
    id, clase_id, tipo, criterios, preguntas, created_at
    # tipo = "unificado" para nuevos exámenes

class ExamenResuelto:
    id, examen_id, estudiante_id, imagen_path, respuestas
    calificacion, tipo_aplicacion, feedback, estado, analisis_ia, created_at
    # NUEVO: tipo_aplicacion = "pretest" | "postest"

class Inscripcion:
    estudiante_id, curso_id, created_at
```

### INTEGRACIÓN CON IA (GOOGLE GEMINI)

#### Configuración
```python
# En gemini_service.py
from google import genai

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
```

#### Funcionalidades de IA

1. **Generación de Criterios**:
   - Modelo: gemini-2.5-flash
   - Input: Competencia matemática + grado
   - Output: 4 criterios específicos y medibles

2. **Generación de Preguntas**:
   - Modelo: gemini-2.5-flash
   - Input: Criterios + competencia + grado
   - Output: 5 preguntas con respuestas esperadas

3. **Análisis de Imágenes**:
   - Modelo: gemini-2.5-pro (multimodal)
   - Input: Imagen del examen + preguntas + tipo
   - Output: OCR + análisis de respuestas + calificación

4. **Feedback Inteligente**:
   - Comparación pretest vs postest
   - Identificación de mejoras
   - Recomendaciones personalizadas

### INTERFAZ DE USUARIO

#### Tema y Diseño
- **Bootstrap 5.3** con tema claro personalizado
- **Colores principales**: Azul (#2563eb), Verde (#16a34a)
- **Contraste mejorado**: Texto oscuro (#1e293b) sobre fondo blanco
- **Iconografía**: Feather Icons para consistencia visual

#### Dashboards Diferenciados

**Dashboard Docente**:
- Gestión de cursos y clases
- Creación de exámenes con IA
- Subida y análisis de exámenes resueltos
- Visualización de resultados y progreso

**Dashboard Estudiante**:
- Visualización de cursos inscritos
- Acceso a exámenes subidos
- Retroalimentación personalizada
- Seguimiento de progreso personal

### CARACTERÍSTICAS TÉCNICAS ESPECIALES

#### 1. Examen Unificado
- **Problema resuelto**: Eliminación de duplicación pretest/postest
- **Beneficio**: Un solo examen = menor trabajo docente
- **Implementación**: Diferenciación en descarga y análisis, no en creación

#### 2. Generación de PDF Optimizada
- **Límite**: Máximo 2 páginas por diseño pedagógico
- **Formato**: A4 con espacios en blanco sin líneas para escritura natural
- **Contenido**: Encabezado con tipo (Pretest/Postest), información del curso, preguntas numeradas

#### 3. Análisis de IA Contextual
- **OCR avanzado**: Extracción de texto manuscrito en imágenes
- **Análisis semántico**: Comprensión del contenido matemático
- **Feedback diferenciado**: Pretest (básico) vs Postest (comparativo)

#### 4. Gestión de Archivos Segura
- **Validación**: Solo JPG, PNG, GIF hasta 16MB
- **Nomenclatura**: `{examen_id}_{estudiante_id}_{uuid}.{ext}`
- **Almacenamiento**: `/static/uploads/` con `.gitkeep`

### DATOS DE PRUEBA INCLUIDOS

#### Usuarios de Prueba
```python
# Docentes
docente1@meduca.com / password123 (Ana García)
docente2@meduca.com / password123 (Carlos López)

# Estudiantes (8 estudiantes con exámenes pre-cargados)
estudiante1@meduca.com / password123 (María Rodríguez)
estudiante2@meduca.com / password123 (Juan Pérez)
[... hasta estudiante8]
```

#### Cursos y Clases Pre-creados
- **4 cursos** de matemáticas (grados 3°-6°)
- **4 clases** con competencias específicas:
  - Números y Operaciones (3° grado)
  - Fracciones y Decimales (4° grado)
  - Geometría Básica (5° grado)
  - Álgebra Elemental (6° grado)

#### Exámenes de Ejemplo
- **Exámenes unificados** creados para cada clase
- **Imágenes de muestra** de exámenes resueltos
- **Análisis de IA** pre-procesados para demostración

### COMPETENCIAS MATEMÁTICAS POR GRADO

```python
# En competencias_matematicas.py
COMPETENCIAS_MATEMATICAS = {
    "3": [
        {
            "id": "3_cantidad_1",
            "nombre": "Números y Operaciones Básicas",
            "descripcion": "Comprende y opera con números naturales..."
        }
        # ... más competencias
    ]
    # Grados 1-11 con competencias específicas
}
```

### COMANDOS DE EJECUCIÓN

#### Desarrollo
```bash
# Instalar dependencias (ya instaladas en Replit)
# Configurar variable de entorno
export GEMINI_API_KEY="tu_api_key"

# Ejecutar aplicación
python main.py
# O con gunicorn (configurado como workflow)
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

#### Estructura de Workflows
```yaml
# Workflow configurado en Replit
name: "Start application"
command: "gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app"
```

### FLUJO DE TRABAJO PEDAGÓGICO COMPLETO

1. **Preparación**:
   - Docente crea curso y clase
   - Inscribe estudiantes
   - Genera examen unificado con IA (criterios + preguntas)

2. **Aplicación Pretest**:
   - Descarga PDF seleccionando "Pretest"
   - Aplica físicamente a estudiantes
   - Fotografía y sube marcando "Pretest"
   - IA analiza y almacena resultados básicos

3. **Enseñanza**:
   - Docente enseña la competencia usando criterios generados

4. **Aplicación Postest**:
   - Descarga mismo examen seleccionando "Postest"
   - Aplica a estudiantes
   - Fotografía y sube marcando "Postest"
   - IA compara con pretest y genera feedback detallado

5. **Análisis y Seguimiento**:
   - Visualización de progreso individual y grupal
   - Retroalimentación personalizada
   - Identificación de estudiantes que necesitan apoyo

### BENEFICIOS DEL SISTEMA

#### Para Docentes
- **Reducción de carga de trabajo**: IA genera criterios y preguntas
- **Análisis automático**: OCR y calificación automática
- **Feedback inteligente**: Sugerencias personalizadas para cada estudiante
- **Seguimiento de progreso**: Comparación pretest/postest automática

#### Para Estudiantes
- **Retroalimentación inmediata**: Resultados disponibles al subir
- **Progreso visible**: Comparación clara de mejoras
- **Aprendizaje personalizado**: Recomendaciones específicas

#### Para Instituciones
- **Estandarización**: Criterios basados en competencias oficiales
- **Datos objetivos**: Métricas de progreso estudiantil
- **Eficiencia**: Digitalización del proceso de evaluación

### SEGURIDAD Y PRIVACIDAD

- **Autenticación**: Hasheo de contraseñas con Werkzeug
- **Autorización**: Decoradores de rol para protección de rutas
- **Validación de archivos**: Restricción de tipos y tamaños
- **Datos sensibles**: API keys en variables de entorno

### LIMITACIONES ACTUALES Y FUTURAS MEJORAS

#### Limitaciones MVP
- **Almacenamiento**: In-memory (se pierde al reiniciar)
- **Escalabilidad**: Diseñado para demostración
- **Base de datos**: No persistente

#### Mejoras Recomendadas
- **PostgreSQL**: Migración a base de datos persistente
- **Autenticación avanzada**: OAuth, 2FA
- **Analytics**: Dashboard con métricas avanzadas
- **API REST**: Para integraciones externas
- **Notificaciones**: Email/SMS para padres y estudiantes

### PROMPT COMPLETO PARA REPLICACIÓN

**"Crea MEDUCA, un sistema web educativo en Flask para evaluación matemática inteligente con las siguientes especificaciones:**

**ARQUITECTURA**: Flask + Bootstrap 5 + Google Gemini IA + ReportLab PDF + almacenamiento in-memory para MVP.

**FUNCIONALIDAD CORE**: Sistema de examen unificado donde docentes crean UN solo examen por clase usando IA que sirve tanto para pretest como postest. La diferenciación se hace al descargar PDF (selector pretest/postest) y al subir imágenes de exámenes resueltos (selector tipo_aplicacion).

**FLUJO IA**: 1) IA genera 4 criterios específicos por competencia matemática, 2) IA genera 5 preguntas alineadas, 3) IA analiza imágenes de exámenes con OCR, 4) Análisis diferenciado: pretest (básico) vs postest (comparativo con feedback detallado).

**ROLES**: Docente (crea cursos/clases, genera exámenes, sube imágenes, ve resultados) y Estudiante (ve sus exámenes subidos, accede a feedback personalizado).

**COMPETENCIAS**: Sistema basado en competencias matemáticas oficiales por grado (1-11), cada clase tiene exactamente UNA competencia.

**UI/UX**: Tema claro con texto oscuro (#1e293b) sobre fondo blanco, Bootstrap 5.3, Feather Icons, dashboards diferenciados por rol.

**PDF**: Máximo 2 páginas, espacios en blanco sin líneas, encabezado con tipo de examen seleccionado.

**DATOS**: Incluir 8 estudiantes de prueba con exámenes pre-subidos, 4 clases con competencias, usuarios docente/estudiante para testing.

**TÉCNICO**: Estructura modular (routes.py, models.py, gemini_service.py, pdf_generator.py), servidor Gunicorn en puerto 5000, manejo de archivos hasta 16MB, integración Google Gemini con gemini-2.5-flash y gemini-2.5-pro para análisis multimodal.**

Incluye toda la funcionalidad descrita con código completo, templates Bootstrap responsivos, CSS personalizado, JavaScript para interactividad, y documentación técnica completa."

---

**FECHA DE DOCUMENTACIÓN**: Agosto 2025  
**VERSIÓN**: 1.0 - Sistema Unificado  
**ESTADO**: Completamente funcional para MVP educativo

### CONCLUSIÓN

MEDUCA representa una solución completa e innovadora para la evaluación matemática inteligente, combinando pedagogía moderna con tecnología de IA. El sistema de **examen unificado** elimina duplicación de trabajo mientras mantiene la efectividad pedagógica del modelo pretest/postest. La integración con Google Gemini proporciona análisis inteligente que beneficia tanto a docentes como estudiantes, creando un ecosistema educativo más eficiente y personalizado.

La arquitectura modular y el diseño centrado en el usuario aseguran que el sistema sea tanto poderoso como fácil de usar, estableciendo una base sólida para futuras expansiones y mejoras."