import os
import uuid
from flask import render_template, request, redirect, url_for, session, flash, send_file, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app import app
from data_store import DataStore
from models import User, Curso, Clase, Examen, ExamenResuelto, Inscripcion
from gemini_service import GeminiService
from pdf_generator import PDFGenerator
from competencias_matematicas import COMPETENCIAS_MATEMATICAS
import logging

# Initialize services
data_store = DataStore()
gemini_service = GeminiService()
pdf_generator = PDFGenerator()

# Helper functions
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def docente_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = data_store.get_user(session['user_id'])
        if not user or user.role != 'docente':
            flash('Acceso denegado. Solo para docentes.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = data_store.get_user_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['user_role'] = user.role
            flash(f'Bienvenido, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales incorrectas', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        if data_store.get_user_by_username(username):
            flash('El nombre de usuario ya existe', 'error')
        elif data_store.get_user_by_email(email):
            flash('El email ya está registrado', 'error')
        else:
            user_id = str(uuid.uuid4())
            password_hash = generate_password_hash(password)
            user = User(user_id, username, email, role, password_hash)
            data_store.add_user(user)
            flash('Registro exitoso. Puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
    
    return render_template('login.html', show_register=True)

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = data_store.get_user(session['user_id'])
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('login'))
    
    if user.role == 'docente':
        cursos = data_store.get_cursos_by_docente(user.id)
        return render_template('dashboard_docente.html', user=user, cursos=cursos)
    else:
        # Estudiante dashboard
        inscripciones = data_store.get_inscripciones_by_estudiante(user.id)
        cursos = [data_store.get_curso(insc.curso_id) for insc in inscripciones if data_store.get_curso(insc.curso_id)]
        
        # Obtener exámenes resueltos del estudiante
        examenes_resueltos = data_store.get_examenes_resueltos_by_estudiante(user.id)
        
        return render_template('dashboard_estudiante.html', user=user, cursos=cursos, examenes_resueltos=examenes_resueltos)

@app.route('/crear_curso', methods=['GET', 'POST'])
@docente_required
def crear_curso():
    if request.method == 'POST':
        nombre = request.form['nombre']
        grado = request.form['grado']
        ano_academico = request.form['ano_academico']
        
        curso_id = str(uuid.uuid4())
        curso = Curso(curso_id, nombre, grado, ano_academico, session['user_id'])
        data_store.add_curso(curso)
        flash('Curso creado exitosamente', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('crear_curso.html')

@app.route('/curso/<curso_id>')
@login_required
def ver_curso(curso_id):
    curso = data_store.get_curso(curso_id)
    if not curso:
        flash('Curso no encontrado', 'error')
        return redirect(url_for('dashboard'))
    
    user = data_store.get_user(session['user_id'])
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('login'))
        
    if user.role == 'docente' and curso.docente_id != user.id:
        flash('No tienes permiso para ver este curso', 'error')
        return redirect(url_for('dashboard'))
    
    clases = data_store.get_clases_by_curso(curso_id)
    competencias = COMPETENCIAS_MATEMATICAS.get(curso.grado, [])
    
    return render_template('crear_clase.html', curso=curso, clases=clases, competencias=competencias)

@app.route('/crear_clase/<curso_id>', methods=['POST'])
@docente_required
def crear_clase(curso_id):
    curso = data_store.get_curso(curso_id)
    if not curso or curso.docente_id != session['user_id']:
        flash('No tienes permiso para crear clases en este curso', 'error')
        return redirect(url_for('dashboard'))
    
    competencia_id = request.form['competencia_id']
    clases_existentes = data_store.get_clases_by_curso(curso_id)
    numero_clase = len(clases_existentes) + 1
    nombre = f"Clase {numero_clase}"
    
    clase_id = str(uuid.uuid4())
    clase = Clase(clase_id, nombre, curso_id, competencia_id)
    data_store.add_clase(clase)
    flash('Clase creada exitosamente', 'success')
    return redirect(url_for('ver_curso', curso_id=curso_id))

@app.route('/generar_examen/<clase_id>')
@docente_required
def generar_examen(clase_id):
    clase = data_store.get_clase(clase_id)
    if not clase:
        flash('Clase no encontrada', 'error')
        return redirect(url_for('dashboard'))
    
    curso = data_store.get_curso(clase.curso_id)
    if not curso or curso.docente_id != session['user_id']:
        flash('No tienes permiso para generar exámenes en esta clase', 'error')
        return redirect(url_for('dashboard'))
    
    competencias = COMPETENCIAS_MATEMATICAS.get(curso.grado, [])
    competencia = next((c for c in competencias if c['id'] == clase.competencia_id), None)
    
    if not competencia:
        flash('Competencia no encontrada', 'error')
        return redirect(url_for('ver_curso', curso_id=clase.curso_id))
    
    return render_template('generar_examen.html', clase=clase, curso=curso, competencia=competencia)

@app.route('/generar_criterios', methods=['POST'])
@docente_required
def generar_criterios():
    clase_id = request.form['clase_id']
    clase = data_store.get_clase(clase_id)
    
    if not clase:
        return jsonify({'error': 'Clase no encontrada'}), 404
    
    curso = data_store.get_curso(clase.curso_id)
    if not curso or curso.docente_id != session['user_id']:
        return jsonify({'error': 'Sin permisos'}), 403
    
    competencias = COMPETENCIAS_MATEMATICAS.get(curso.grado, [])
    competencia = next((c for c in competencias if c['id'] == clase.competencia_id), None)
    
    try:
        criterios = gemini_service.generar_criterios_evaluacion(competencia['nombre'], curso.grado)
        return jsonify({'criterios': criterios})
    except Exception as e:
        logging.error(f"Error generando criterios: {e}")
        return jsonify({'error': 'Error al generar criterios'}), 500

@app.route('/generar_preguntas', methods=['POST'])
@docente_required
def generar_preguntas():
    clase_id = request.form['clase_id']
    criterios = request.form.getlist('criterios')
    
    clase = data_store.get_clase(clase_id)
    if not clase:
        return jsonify({'error': 'Clase no encontrada'}), 404
    
    curso = data_store.get_curso(clase.curso_id)
    if not curso or curso.docente_id != session['user_id']:
        return jsonify({'error': 'Sin permisos'}), 403
    
    competencias = COMPETENCIAS_MATEMATICAS.get(curso.grado, [])
    competencia = next((c for c in competencias if c['id'] == clase.competencia_id), None)
    
    try:
        preguntas = gemini_service.generar_preguntas_examen(competencia['nombre'], criterios, curso.grado)
        return jsonify({'preguntas': preguntas})
    except Exception as e:
        logging.error(f"Error generando preguntas: {e}")
        return jsonify({'error': 'Error al generar preguntas'}), 500

@app.route('/crear_examen', methods=['POST'])
@docente_required
def crear_examen():
    clase_id = request.form['clase_id']
    tipo = 'unificado'  # Examen unificado para pre y post test
    criterios = request.form.getlist('criterios')
    preguntas_json = request.form.getlist('preguntas')
    
    clase = data_store.get_clase(clase_id)
    if not clase:
        flash('Clase no encontrada', 'error')
        return redirect(url_for('dashboard'))
    
    curso = data_store.get_curso(clase.curso_id)
    if curso.docente_id != session['user_id']:
        flash('Sin permisos', 'error')
        return redirect(url_for('dashboard'))
    
    # Parsear preguntas del JSON
    import json
    preguntas = []
    for p_json in preguntas_json:
        try:
            pregunta = json.loads(p_json)
            preguntas.append(pregunta)
        except:
            pass
    
    examen_id = str(uuid.uuid4())
    examen = Examen(examen_id, clase_id, tipo, criterios, preguntas)
    data_store.add_examen(examen)
    
    flash('Examen creado exitosamente', 'success')
    return redirect(url_for('ver_clase', clase_id=clase_id))

@app.route('/clase/<clase_id>')
@login_required
def ver_clase(clase_id):
    clase = data_store.get_clase(clase_id)
    if not clase:
        flash('Clase no encontrada', 'error')
        return redirect(url_for('dashboard'))
    
    curso = data_store.get_curso(clase.curso_id)
    examenes = data_store.get_examenes_by_clase(clase_id)
    
    user = data_store.get_user(session['user_id'])
    if user.role == 'docente' and curso.docente_id != user.id:
        flash('Sin permisos', 'error')
        return redirect(url_for('dashboard'))
    
    competencias = COMPETENCIAS_MATEMATICAS.get(curso.grado, [])
    competencia = next((c for c in competencias if c['id'] == clase.competencia_id), None)
    
    return render_template('ver_resultados.html', 
                         clase=clase, 
                         curso=curso, 
                         competencia=competencia, 
                         examenes=examenes)

@app.route('/descargar_examen/<examen_id>')
@app.route('/descargar_examen/<examen_id>/<tipo_descarga>')
@login_required
def descargar_examen(examen_id, tipo_descarga=None):
    examen = data_store.get_examen(examen_id)
    if not examen:
        flash('Examen no encontrado', 'error')
        return redirect(url_for('dashboard'))
    
    clase = data_store.get_clase(examen.clase_id)
    curso = data_store.get_curso(clase.curso_id)
    
    user = data_store.get_user(session['user_id'])
    if user.role == 'docente' and curso.docente_id != user.id:
        flash('Sin permisos', 'error')
        return redirect(url_for('dashboard'))
    
    competencias = COMPETENCIAS_MATEMATICAS.get(curso.grado, [])
    competencia = next((c for c in competencias if c['id'] == clase.competencia_id), None)
    
    # Si no se especifica tipo_descarga, mostrar selector
    if not tipo_descarga:
        return render_template('seleccionar_tipo_descarga.html', 
                             examen=examen, 
                             clase=clase, 
                             curso=curso, 
                             competencia=competencia)
    
    try:
        # Usar el tipo especificado para la descarga
        pdf_path = pdf_generator.generar_examen_pdf(examen, clase, curso, competencia, tipo_descarga)
        filename = f'examen_{tipo_descarga}_{clase.nombre.replace(" ", "_")}.pdf'
        return send_file(pdf_path, as_attachment=True, download_name=filename)
    except Exception as e:
        logging.error(f"Error generando PDF: {e}")
        flash('Error al generar el PDF del examen', 'error')
        return redirect(url_for('ver_clase', clase_id=examen.clase_id))

@app.route('/subir_examenes/<clase_id>')
@docente_required
def subir_examenes(clase_id):
    clase = data_store.get_clase(clase_id)
    if not clase:
        flash('Clase no encontrada', 'error')
        return redirect(url_for('dashboard'))
    
    curso = data_store.get_curso(clase.curso_id)
    if curso.docente_id != session['user_id']:
        flash('Sin permisos', 'error')
        return redirect(url_for('dashboard'))
    
    examenes = data_store.get_examenes_by_clase(clase_id)
    inscripciones = data_store.get_inscripciones_by_curso(curso.id)
    estudiantes = [data_store.get_user(insc.estudiante_id) for insc in inscripciones]
    
    return render_template('subir_examenes.html', 
                         clase=clase, 
                         curso=curso, 
                         examenes=examenes, 
                         estudiantes=estudiantes)

@app.route('/subir_examen_resuelto', methods=['POST'])
@login_required
def subir_examen_resuelto():
    examen_id = request.form['examen_id']
    estudiante_id = request.form['estudiante_id']
    tipo_aplicacion = request.form.get('tipo_aplicacion', 'pretest')  # pretest o postest
    
    # Verificar permisos - docentes pueden subir para cualquier estudiante, estudiantes solo para sí mismos
    user = data_store.get_user(session['user_id'])
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('login'))
    
    if user.role == 'estudiante' and user.id != estudiante_id:
        flash('Solo puedes subir tus propios exámenes', 'error')
        return redirect(url_for('dashboard'))
    
    if 'imagen' not in request.files:
        flash('No se seleccionó ninguna imagen', 'error')
        return redirect(request.referrer or url_for('dashboard'))
    
    file = request.files['imagen']
    if not file or file.filename == '':
        flash('No se seleccionó ninguna imagen', 'error')
        return redirect(request.referrer or url_for('dashboard'))
    
    if file and allowed_file(file.filename):
        # Verificar si ya existe un examen resuelto para este estudiante y examen
        existing = next((er for er in data_store.examenes_resueltos.values() 
                        if er.examen_id == examen_id and er.estudiante_id == estudiante_id), None)
        
        filename = secure_filename(f"{examen_id}_{estudiante_id}_{uuid.uuid4().hex}.{file.filename.rsplit('.', 1)[1].lower()}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            file.save(filepath)
            
            # Obtener el examen para análisis
            examen = data_store.get_examen(examen_id)
            if not examen:
                flash('Examen no encontrado', 'error')
                return redirect(request.referrer or url_for('dashboard'))
            
            # Analizar la imagen con IA usando el tipo de aplicación
            try:
                if tipo_aplicacion == 'pretest':
                    # Para pretest, solo análisis básico
                    resultado_analisis = gemini_service.analizar_examen_imagen(filepath, examen.preguntas, 'pretest')
                else:
                    # Para postest, análisis completo con comparación
                    # Buscar el pretest del mismo estudiante y examen unificado
                    pretest_resultado = None
                    pretest_resuelto = next((er for er in data_store.examenes_resueltos.values() 
                                           if er.examen_id == examen_id and er.estudiante_id == estudiante_id 
                                           and hasattr(er, 'tipo_aplicacion') and er.tipo_aplicacion == 'pretest'), None)
                    if pretest_resuelto and hasattr(pretest_resuelto, 'analisis_ia'):
                        pretest_resultado = pretest_resuelto.analisis_ia
                    
                    resultado_analisis = gemini_service.procesar_examen_postest(filepath, examen.preguntas, pretest_resultado)
                
                # Extraer calificación
                calificacion = float(resultado_analisis.get('calificacion_total', 10))
                
            except Exception as e:
                logging.error(f"Error en análisis de IA: {e}")
                resultado_analisis = {"error": "Análisis automático no disponible"}
                calificacion = 10.0  # Calificación por defecto
            
            if existing:
                # Actualizar examen existente
                existing.imagen_path = filename
                existing.estado = "completado"
                existing.calificacion = calificacion
                existing.analisis_ia = resultado_analisis
                existing.tipo_aplicacion = tipo_aplicacion
                flash('Imagen del examen actualizada y analizada exitosamente', 'success')
            else:
                # Crear nuevo registro de examen resuelto
                resuelto_id = str(uuid.uuid4())
                examen_resuelto = ExamenResuelto(resuelto_id, examen_id, estudiante_id, filename, {}, None, tipo_aplicacion)
                examen_resuelto.estado = "completado"
                examen_resuelto.calificacion = calificacion
                examen_resuelto.analisis_ia = resultado_analisis
                data_store.add_examen_resuelto(examen_resuelto)
                flash('Imagen del examen subida y analizada exitosamente', 'success')
                
        except Exception as e:
            logging.error(f"Error guardando archivo: {e}")
            flash('Error al guardar la imagen', 'error')
    else:
        flash('Tipo de archivo no permitido. Use JPG, PNG o GIF', 'error')
    
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/inscribir_estudiante', methods=['POST'])
@docente_required
def inscribir_estudiante():
    curso_id = request.form['curso_id']
    email_estudiante = request.form['email_estudiante']
    
    curso = data_store.get_curso(curso_id)
    if not curso or curso.docente_id != session['user_id']:
        flash('Sin permisos', 'error')
        return redirect(url_for('dashboard'))
    
    estudiante = data_store.get_user_by_email(email_estudiante)
    if not estudiante:
        flash('Estudiante no encontrado', 'error')
    elif estudiante.role != 'estudiante':
        flash('El usuario no es un estudiante', 'error')
    else:
        inscripcion = Inscripcion(estudiante.id, curso_id)
        data_store.add_inscripcion(inscripcion)
        flash('Estudiante inscrito exitosamente', 'success')
    
    return redirect(url_for('ver_curso', curso_id=curso_id))

@app.route('/feedback_estudiante/<examen_resuelto_id>')
@login_required
def feedback_estudiante(examen_resuelto_id):
    examen_resuelto = data_store.get_examen_resuelto(examen_resuelto_id)
    if not examen_resuelto:
        flash('Examen no encontrado', 'error')
        return redirect(url_for('dashboard'))
    
    user = data_store.get_user(session['user_id'])
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('login'))
    
    if user.role == 'estudiante' and examen_resuelto.estudiante_id != user.id:
        flash('Sin permisos', 'error')
        return redirect(url_for('dashboard'))
    
    examen = data_store.get_examen(examen_resuelto.examen_id)
    if not examen:
        flash('Examen no encontrado', 'error')
        return redirect(url_for('dashboard'))
        
    clase = data_store.get_clase(examen.clase_id)
    if not clase:
        flash('Clase no encontrada', 'error')
        return redirect(url_for('dashboard'))
        
    curso = data_store.get_curso(clase.curso_id)
    if not curso:
        flash('Curso no encontrado', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('feedback_estudiante.html', 
                         examen_resuelto=examen_resuelto,
                         examen=examen,
                         clase=clase,
                         curso=curso)

@app.route('/ver_examenes_subidos/<clase_id>')
@docente_required
def ver_examenes_subidos(clase_id):
    """Vista para que el docente vea los exámenes subidos por estudiantes"""
    clase = data_store.get_clase(clase_id)
    if not clase:
        flash('Clase no encontrada', 'error')
        return redirect(url_for('dashboard'))
    
    curso = data_store.get_curso(clase.curso_id)
    if not curso or curso.docente_id != session['user_id']:
        flash('Sin permisos', 'error')
        return redirect(url_for('dashboard'))
    
    # Obtener exámenes de esta clase
    examenes = data_store.get_examenes_by_clase(clase_id)
    pretest = next((e for e in examenes if e.tipo == 'pretest'), None)
    postest = next((e for e in examenes if e.tipo == 'postest'), None)
    
    # Obtener estudiantes inscritos
    inscripciones = data_store.get_inscripciones_by_curso(curso.id)
    estudiantes = [data_store.get_user(insc.estudiante_id) for insc in inscripciones 
                  if data_store.get_user(insc.estudiante_id)]
    
    # Obtener exámenes resueltos
    examenes_resueltos = {
        'pretest': [],
        'postest': []
    }
    
    for estudiante in estudiantes:
        if pretest:
            pretest_resuelto = data_store.get_examen_resuelto_by_estudiante_examen(
                estudiante.id, pretest.id)
            if pretest_resuelto:
                examenes_resueltos['pretest'].append({
                    'estudiante': estudiante,
                    'examen_resuelto': pretest_resuelto,
                    'examen': pretest
                })
        
        if postest:
            postest_resuelto = data_store.get_examen_resuelto_by_estudiante_examen(
                estudiante.id, postest.id)
            if postest_resuelto:
                examenes_resueltos['postest'].append({
                    'estudiante': estudiante,
                    'examen_resuelto': postest_resuelto,
                    'examen': postest
                })
    
    return render_template('ver_examenes_subidos.html',
                         clase=clase,
                         curso=curso,
                         examenes_resueltos=examenes_resueltos,
                         pretest=pretest,
                         postest=postest)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('base.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('base.html'), 500
