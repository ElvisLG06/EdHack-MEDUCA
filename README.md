# MEDUCA

## 🎯 Descripción

MEDUCA es una plataforma web inteligente que utiliza IA (Google Gemini) para generar criterios de evaluación y preguntas de examen personalizadas basadas en competencias del currículo panameño.

## ✨ Características Principales

- **Generación Inteligente de Criterios**: La IA genera 4 criterios de evaluación específicos para cada competencia matemática
- **Preguntas Personalizadas**: 5 preguntas de examen alineadas con los criterios generados
- **Dashboard para Docentes**: Gestión de cursos, clases y exámenes
- **Dashboard para Estudiantes**: Visualización de cursos y resultados
- **Análisis de Exámenes**: Evaluación automática de exámenes subidos
- **Feedback Personalizado**: Retroalimentación específica para cada estudiante
- **Generación de PDFs**: Exámenes listos para imprimir

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.11 o superior
- `uv` (gestor de paquetes de Python)

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd EdHack-MEDUCA
```

### 2. Instalar dependencias

```bash
# Instalar uv si no lo tienes
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sincronizar dependencias
source $HOME/.local/bin/env
uv sync
```

### 3. Configurar API Key de Gemini

Edita el archivo `config.py` y reemplaza la API key:

```python
GEMINI_API_KEY = 'TU_API_KEY_DE_GEMINI_AQUI'
```

Para obtener una API key:
1. Ve a [Google AI Studio](https://aistudio.google.com/)
2. Crea una nueva API key
3. Copia la key y pégala en `config.py`

### 4. Ejecutar la aplicación

```bash
source $HOME/.local/bin/env
uv run python main.py
```

La aplicación estará disponible en: **http://localhost:5001**

## 📋 Uso del Sistema

### Para Docentes

1. **Crear un Curso**
   - Accede al dashboard de docente
   - Haz clic en "Crear Curso"
   - Completa la información del curso

2. **Crear Clases**
   - Selecciona una competencia matemática
   - La clase se creará automáticamente

3. **Generar Examen**
   - Ve a la clase creada
   - Haz clic en "Generar Examen"
   - Sigue el proceso de 3 pasos:
     - **Paso 1**: Generar criterios con IA
     - **Paso 2**: Generar preguntas con IA
     - **Paso 3**: Crear y descargar examen

4. **Evaluar Exámenes**
   - Sube las imágenes de los exámenes resueltos
   - La IA analizará automáticamente las respuestas
   - Revisa y ajusta las calificaciones si es necesario

### Para Estudiantes

1. **Acceder al Dashboard**
   - Inicia sesión con tu cuenta de estudiante
   - Visualiza los cursos en los que estás inscrito

2. **Ver Resultados**
   - Revisa tus calificaciones de exámenes
   - Accede al feedback personalizado
   - Observa tu progreso entre pretest y postest

## 🔧 Estructura del Proyecto

```
EdHack-MEDUCA/
├── app.py                 # Configuración principal de Flask
├── main.py               # Punto de entrada de la aplicación
├── routes.py             # Rutas y controladores
├── models.py             # Modelos de datos
├── data_store.py         # Almacenamiento de datos
├── gemini_service.py     # Servicio de IA (Gemini)
├── config.py             # Configuración de la aplicación
├── competencias_matematicas.py  # Definición de competencias
├── pdf_generator.py      # Generación de PDFs
├── static/               # Archivos estáticos (CSS, imágenes)
├── templates/            # Plantillas HTML
└── pyproject.toml        # Dependencias del proyecto
```

## 🧠 Funcionalidades de IA

### Generación de Criterios
- Analiza la competencia matemática específica
- Genera 4 criterios de evaluación medibles
- Adaptados al nivel de grado correspondiente

### Generación de Preguntas
- 5 preguntas alineadas con los criterios
- Enunciados claros y apropiados para el grado
- Incluye respuestas esperadas

### Análisis de Exámenes
- Reconocimiento de escritura a mano
- Evaluación automática de respuestas
- Calificación numérica y feedback

## 🔒 Seguridad

- Autenticación de usuarios
- Validación de permisos por rol
- Sanitización de entradas
- Configuración segura de API keys

## 🐛 Solución de Problemas

### Error de API Key
Si ves errores relacionados con la API key de Gemini:
1. Verifica que la key esté correctamente configurada en `config.py`
2. Asegúrate de que la key sea válida en Google AI Studio
3. Revisa los logs de la aplicación para más detalles

### Puerto Ocupado
Si el puerto 5000 está ocupado (común en macOS):
- La aplicación se ejecutará automáticamente en el puerto 5001
- Accede a http://localhost:5001

### Problemas de Dependencias
```bash
# Reinstalar dependencias
uv sync --reinstall
```

## 📞 Soporte

Para reportar problemas o solicitar nuevas funcionalidades:
1. Revisa los logs de la aplicación
2. Verifica la configuración de la API key

## 📄 Licencia

Este proyecto fue desarrollado para el EdHack 2025.

---

**¡Disfruta usando MEDUCA para crear evaluaciones inteligentes! 🎓✨**
