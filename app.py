# Importación de librerías necesarias para el funcionamiento del servidor web
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
import os
from functools import wraps
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from database_handler import obtener_db, inicializar_app

# Cargar las variables de entorno desde el archivo .env (configuración de BD y llaves secretas)
load_dotenv()

# Inicialización de la aplicación Flask
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# Inicializar la conexión a la base de datos con la aplicación
inicializar_app(app)

# --- MIDDLEWARE: Función que se ejecuta antes de cada petición ---
# Su objetivo es cargar la información del usuario logueado en la variable global 'g.user'
@app.before_request
def cargar_usuario_logueado():
    id_usuario = session.get('user_id')
    if id_usuario is None:
        g.user = None
    else:
        db = obtener_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id_usuario,))
        g.user = cursor.fetchone()

# --- DECORADORES DE AUTORIZACIÓN ---

def requiere_login(f):
    """Decorador para rutas que requieren que el usuario esté logueado"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def requiere_admin(f):
    """Decorador para rutas que requieren privilegios de administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        if g.user.get('rol') != 'admin':
            flash('No tienes permisos para acceder a esta sección.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# --- SECCIÓN: AUTENTICACIÓN Y REGISTRO ---

# Ruta para el registro de nuevos usuarios (C de CRUD)
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Captura de datos del formulario
        nombre = request.form['nombre']
        email = request.form['email']
        password_raw = request.form['password']

        # Validación: longitud de contraseña (M1)
        if len(password_raw) < 8:
            flash('La contraseña debe tener al menos 8 caracteres.', 'danger')
            return render_template('registro.html')

        db = obtener_db()
        cursor = db.cursor(dictionary=True)
        
        # Validación: email ya registrado (M1)
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            flash('El correo electrónico ya se encuentra registrado.', 'warning')
            return render_template('registro.html')

        # Encriptación de la contraseña por seguridad
        password = generate_password_hash(password_raw)

        try:
            # Inserción del nuevo usuario en la base de datos
            cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                           (nombre, email, password))
            db.commit()
            
            # Iniciar sesión automáticamente después de un registro exitoso
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            usuario = cursor.fetchone()
            session.clear()
            session['user_id'] = usuario['id']
            
            flash('¡Registro exitoso! Bienvenido a Futuro 360.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            # Manejo de errores
            flash(f'Error al registrar el usuario: {e}', 'danger')

    return render_template('registro.html')

# Ruta para iniciar sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = obtener_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()

        # Verificación de que el usuario existe y la contraseña es correcta
        if usuario and check_password_hash(usuario['password'], password):
            session.clear()
            session['user_id'] = usuario['id']
            flash(f'¡Qué bueno verte de nuevo, {usuario["nombre"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Correo o contraseña incorrectos. Por favor, intenta de nuevo.', 'danger')

    return render_template('login.html')

# Ruta para cerrar la sesión
@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('index'))

# Ruta para recuperación de contraseña (simulada)
@app.route('/recuperar-password', methods=['GET', 'POST'])
def recuperar_password():
    if request.method == 'POST':
        email = request.form['email']
        
        db = obtener_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        
        # Siempre mostramos el mismo mensaje por seguridad
        flash('Si el correo está registrado, recibirás las instrucciones en breve.', 'info')
        return redirect(url_for('login'))
        
    return render_template('recuperar_password.html')

# --- SECCIÓN: GESTIÓN DE PERFIL (R, U, D de CRUD) ---

# Ruta para ver y actualizar el perfil del usuario
@app.route('/perfil', methods=['GET', 'POST'])
@requiere_login
def perfil():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']

        db = obtener_db()
        cursor = db.cursor()
        # Actualización de datos del usuario
        cursor.execute("UPDATE usuarios SET nombre = %s, email = %s WHERE id = %s",
                       (nombre, email, g.user['id']))
        db.commit()
        flash('Tu perfil ha sido actualizado correctamente.', 'success')
        return redirect(url_for('perfil'))

    return render_template('perfil.html', user=g.user)

# Ruta para eliminar la cuenta del usuario (Baja de CRUD)
@app.route('/perfil/eliminar', methods=['POST'])
@requiere_login
def eliminar_usuario():
    db = obtener_db()
    cursor = db.cursor()
    # Eliminación física del registro del usuario
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (g.user['id'],))
    db.commit()
    session.clear()
    flash('Tu cuenta ha sido eliminada. Lamentamos verte partir.', 'info')
    return redirect(url_for('index'))

# --- SECCIÓN: RUTAS DE LA PÁGINA ---

# Página de inicio (Home)
@app.route('/')
def index():
    # Si el usuario ya está logueado, lo enviamos directo al panel de control
    if g.user:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

# Panel de Control (Dashboard) del usuario
@app.route('/dashboard')
@requiere_login
def dashboard():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    # Obtenemos los últimos 3 resultados del test para mostrar en el panel
    cursor.execute("""
        SELECT r.id, r.area_profesional_sugerida, t.fecha_realizacion, r.detalle
        FROM resultados r
        JOIN tests t ON r.test_id = t.id
        WHERE t.usuario_id = %s
        ORDER BY t.fecha_realizacion DESC
        LIMIT 3
    """, (g.user['id'],))
    historial = cursor.fetchall()
    
    return render_template('dashboard.html', historial=historial)

# Listado de todas las carreras disponibles
@app.route('/carreras')
@requiere_login
def carreras():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM carreras")
    lista_carreras = cursor.fetchall()
    return render_template('carreras.html', carreras=lista_carreras)

# --- SECCIÓN: TEST VOCACIONAL (CRUD de Resultados) ---

# Ruta para realizar el test vocacional
@app.route('/test', methods=['GET', 'POST'])
@requiere_login
def test():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        # Captura de respuestas del test
        respuestas = request.form.to_dict()
        puntuacion = {}

        # Contabilizamos las áreas según las respuestas marcadas
        for id_pregunta, area in respuestas.items():
            puntuacion[area] = puntuacion.get(area, 0) + 1

        # Determinamos el área con mayor puntaje (la sugerida)
        area_ganadora = max(puntuacion, key=puntuacion.get) if puntuacion else "Indefinido"

        # Guardamos el registro del intento del test
        cursor.execute("INSERT INTO tests (usuario_id) VALUES (%s)", (g.user['id'],))
        id_test = cursor.lastrowid

        # Guardamos el resultado detallado asociado al test
        detalle_resultado = f"Según tus respuestas, presentas una fuerte afinidad con el área de {area_ganadora}."
        cursor.execute("INSERT INTO resultados (test_id, area_profesional_sugerida, detalle) VALUES (%s, %s, %s)",
                       (id_test, area_ganadora, detalle_resultado))
        db.commit()

        # Redirigimos al usuario a ver su informe recién generado
        return redirect(url_for('ver_resultado', resultado_id=cursor.lastrowid))

    # Cargar las preguntas dinámicas desde la base de datos para mostrar el formulario
    cursor.execute("SELECT * FROM preguntas")
    preguntas = cursor.fetchall()
    return render_template('test.html', preguntas=preguntas)

# Ruta para ver el detalle de un resultado específico
@app.route('/resultado/<int:resultado_id>')
@requiere_login
def ver_resultado(resultado_id):
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    # Consulta que une el resultado con la fecha del test
    cursor.execute("""
        SELECT r.*, t.fecha_realizacion
        FROM resultados r
        JOIN tests t ON r.test_id = t.id
        WHERE r.id = %s AND t.usuario_id = %s
    """, (resultado_id, g.user['id']))
    resultado = cursor.fetchone()

    if not resultado:
        flash('No se pudo encontrar el resultado solicitado.', 'danger')
        return redirect(url_for('mis_resultados'))

    # Obtenemos carreras sugeridas que pertenezcan al mismo área del resultado
    cursor.execute("SELECT * FROM carreras WHERE area_profesional = %s", (resultado['area_profesional_sugerida'],))
    carreras_sugeridas = cursor.fetchall()

    return render_template('resultado_detalle.html', resultado=resultado, carreras=carreras_sugeridas)

# Listado histórico de todos los tests realizados por el usuario
@app.route('/mis-resultados')
@requiere_login
def mis_resultados():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.id, r.area_profesional_sugerida, t.fecha_realizacion
        FROM resultados r
        JOIN tests t ON r.test_id = t.id
        WHERE t.usuario_id = %s
        ORDER BY t.fecha_realizacion DESC
    """, (g.user['id'],))
    resultados = cursor.fetchall()

    return render_template('mis_resultados.html', resultados=resultados)

# Actualizar notas personales en un resultado (U de CRUD)
@app.route('/resultado/actualizar/<int:resultado_id>', methods=['POST'])
@requiere_login
def actualizar_resultado(resultado_id):
    notas_personales = request.form['notas_personales']

    db = obtener_db()
    cursor = db.cursor()
    # Actualizamos el campo de notas personales en la tabla resultados
    cursor.execute("""
        UPDATE resultados r
        JOIN tests t ON r.test_id = t.id
        SET r.notas_personales = %s
        WHERE r.id = %s AND t.usuario_id = %s
    """, (notas_personales, resultado_id, g.user['id']))
    db.commit()
    flash('Tus notas han sido guardadas correctamente.', 'success')
    return redirect(url_for('ver_resultado', resultado_id=resultado_id))

# Eliminar un resultado específico (D de CRUD)
@app.route('/resultado/eliminar/<int:resultado_id>', methods=['POST'])
@requiere_login
def eliminar_resultado(resultado_id):
    db = obtener_db()
    cursor = db.cursor()
    # Al eliminar el test, se elimina el resultado automáticamente por el CASCADE en la BD
    cursor.execute("""
        SELECT test_id FROM resultados r
        JOIN tests t ON r.test_id = t.id
        WHERE r.id = %s AND t.usuario_id = %s
    """, (resultado_id, g.user['id']))
    test = cursor.fetchone()

    if test:
        cursor.execute("DELETE FROM tests WHERE id = %s", (test[0],))
        db.commit()
        flash('El resultado ha sido eliminado de tu historial.', 'info')

    return redirect(url_for('mis_resultados'))

# --- SECCIÓN: HERRAMIENTAS ADICIONALES ---

# Ruta para el mini-juego interactivo
@app.route('/juego')
@requiere_login
def juego():
    return render_template('juego.html')

# Ruta para el centro de noticias y tendencias
@app.route('/noticias')
@requiere_login
def noticias():
    # Datos simulados de noticias académicas
    items_noticias = [
        {"id": 1, "titulo": "Nuevas becas estratégicas para ingeniería", "fuente": "La Gaceta", "fecha": "14/04/2026", "categoria": "hoy"},
        {"id": 2, "titulo": "Tendencias en carreras tecnológicas 2026", "fuente": "Universia", "fecha": "13/04/2026", "categoria": "ayer"},
        {"id": 3, "titulo": "Apertura de inscripciones en facultades de artes", "fuente": "La Gaceta", "fecha": "10/04/2026", "categoria": "esta semana"},
    ]
    return render_template('noticias.html', noticias=items_noticias)

# Ruta para ver el detalle de una carrera universitaria
@app.route('/carrera/<int:carrera_id>')
@requiere_login
def detalle_carrera(carrera_id):
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM carreras WHERE id = %s", (carrera_id,))
    carrera = cursor.fetchone()
    if not carrera:
        flash('No pudimos encontrar información sobre esa carrera.', 'danger')
        return redirect(url_for('carreras'))
    return render_template('carrera_detalle.html', carrera=carrera)

# Ruta para enviar consultas o comentarios desde el footer
@app.route('/comentar', methods=['POST'])
def enviar_comentario():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    mensaje = request.form.get('mensaje')

    if not mensaje:
        flash('Por favor, escribe un mensaje antes de enviar.', 'danger')
        return redirect(request.referrer or url_for('index'))

    db = obtener_db()
    cursor = db.cursor()
    # Guardar la consulta en la tabla de comentarios
    cursor.execute("INSERT INTO comentarios (nombre, email, mensaje) VALUES (%s, %s, %s)",
                   (nombre, email, mensaje))
    db.commit()
    flash('¡Muchas gracias por tu mensaje! Lo hemos recibido correctamente.', 'success')
    return redirect(request.referrer or url_for('index'))

# --- SECCIÓN: PANEL DE ADMINISTRACIÓN ---

@app.route('/admin')
@requiere_admin
def admin_dashboard():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    
    # Obtener todos los usuarios
    cursor.execute("SELECT id, nombre, email, rol, fecha_registro FROM usuarios")
    usuarios = cursor.fetchall()
    
    # Obtener todas las carreras
    cursor.execute("SELECT * FROM carreras")
    carreras = cursor.fetchall()
    
    # Obtener todas las preguntas
    cursor.execute("SELECT * FROM preguntas")
    preguntas = cursor.fetchall()
    
    return render_template('admin/dashboard.html', usuarios=usuarios, carreras=carreras, preguntas=preguntas)

# CRUD de Carreras
@app.route('/admin/carreras')
@requiere_admin
def admin_carreras():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM carreras")
    carreras = cursor.fetchall()
    return render_template('admin/carreras_lista.html', carreras=carreras)

@app.route('/admin/carreras/nueva', methods=['GET', 'POST'])
@requiere_admin
def nueva_carrera():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        area_profesional = request.form['area_profesional']
        
        db = obtener_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO carreras (nombre, descripcion, area_profesional) VALUES (%s, %s, %s)",
                       (nombre, descripcion, area_profesional))
        db.commit()
        flash('Carrera creada exitosamente.', 'success')
        return redirect(url_for('admin_carreras'))
    
    return render_template('admin/carrera_form.html', carrera=None)

@app.route('/admin/carreras/editar/<int:id>', methods=['GET', 'POST'])
@requiere_admin
def editar_carrera(id):
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        area_profesional = request.form['area_profesional']
        
        cursor.execute("UPDATE carreras SET nombre = %s, descripcion = %s, area_profesional = %s WHERE id = %s",
                       (nombre, descripcion, area_profesional, id))
        db.commit()
        flash('Carrera actualizada exitosamente.', 'success')
        return redirect(url_for('admin_carreras'))
    
    cursor.execute("SELECT * FROM carreras WHERE id = %s", (id,))
    carrera = cursor.fetchone()
    return render_template('admin/carrera_form.html', carrera=carrera)

@app.route('/admin/carreras/eliminar/<int:id>', methods=['POST'])
@requiere_admin
def eliminar_carrera(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM carreras WHERE id = %s", (id,))
    db.commit()
    flash('Carrera eliminada exitosamente.', 'info')
    return redirect(url_for('admin_carreras'))

# CRUD de Preguntas
@app.route('/admin/preguntas')
@requiere_admin
def admin_preguntas():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM preguntas")
    preguntas = cursor.fetchall()
    return render_template('admin/preguntas_lista.html', preguntas=preguntas)

@app.route('/admin/preguntas/nueva', methods=['POST'])
@requiere_admin
def nueva_pregunta():
    texto_pregunta = request.form['texto_pregunta']
    area_profesional = request.form['area_profesional']
    
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO preguntas (texto_pregunta, area_profesional) VALUES (%s, %s)",
                   (texto_pregunta, area_profesional))
    db.commit()
    flash('Pregunta agregada exitosamente.', 'success')
    return redirect(url_for('admin_preguntas'))

@app.route('/admin/preguntas/editar/<int:id>', methods=['POST'])
@requiere_admin
def editar_pregunta(id):
    texto_pregunta = request.form['texto_pregunta']
    area_profesional = request.form['area_profesional']
    
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("UPDATE preguntas SET texto_pregunta = %s, area_profesional = %s WHERE id = %s",
                   (texto_pregunta, area_profesional, id))
    db.commit()
    flash('Pregunta actualizada exitosamente.', 'success')
    return redirect(url_for('admin_preguntas'))

@app.route('/admin/preguntas/eliminar/<int:id>', methods=['POST'])
@requiere_admin
def eliminar_pregunta(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM preguntas WHERE id = %s", (id,))
    db.commit()
    flash('Pregunta eliminada exitosamente.', 'info')
    return redirect(url_for('admin_preguntas'))

# Punto de entrada de la aplicación
@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('base.html', content="<div class='container py-5 text-center'><h1>500</h1><p>Algo salió mal en nuestros servidores. Por favor, intenta más tarde.</p></div>"), 500

if __name__ == '__main__':
    # Ejecución en modo desarrollo (debug)
    app.run(debug=True)
