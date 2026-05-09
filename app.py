# Importación de librerías necesarias para el funcionamiento del servidor web
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
import json
import os
import traceback
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
        nombre = request.form['nombre']
        email = request.form['email']
        password_raw = request.form['password']

        if len(password_raw) < 8:
            flash('La contraseña debe tener al menos 8 caracteres.', 'danger')
            return render_template('registro.html')

        db = obtener_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            flash('El correo electrónico ya se encuentra registrado.', 'warning')
            return render_template('registro.html')

        password = generate_password_hash(password_raw)

        try:
            cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                           (nombre, email, password))
            db.commit()
            
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            usuario = cursor.fetchone()
            session.clear()
            session['user_id'] = usuario['id']
            
            flash('¡Registro exitoso! Bienvenido a Futuro 360.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
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
        
        flash('Si el correo está registrado, recibirás las instrucciones en breve.', 'info')
        return redirect(url_for('login'))
        
    return render_template('recuperar_password.html')

# --- SECCIÓN: GESTIÓN DE PERFIL (R, U, D de CRUD) ---

@app.route('/perfil', methods=['GET', 'POST'])
@requiere_login
def perfil():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']

        db = obtener_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("UPDATE usuarios SET nombre = %s, email = %s WHERE id = %s",
                       (nombre, email, g.user['id']))
        db.commit()
        flash('Tu perfil ha sido actualizado correctamente.', 'success')
        return redirect(url_for('perfil'))

    return render_template('perfil.html', user=g.user)

@app.route('/perfil/eliminar', methods=['POST'])
@requiere_login
def eliminar_usuario():
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (g.user['id'],))
    db.commit()
    session.clear()
    flash('Tu cuenta ha sido eliminada. Lamentamos verte partir.', 'info')
    return redirect(url_for('index'))

# --- SECCIÓN: RUTAS DE LA PÁGINA ---

@app.route('/')
def index():
    if g.user:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
@requiere_login
def dashboard():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.id, r.area_profesional_sugerida, t.fecha_realizacion,
               LEFT(r.detalle, 120) as detalle
        FROM resultados r
        JOIN tests t ON r.test_id = t.id
        WHERE t.usuario_id = %s
        ORDER BY t.fecha_realizacion DESC
        LIMIT 3
    """, (g.user['id'],))
    historial_raw = cursor.fetchall()
    
    historial = []
    for item in historial_raw:
        try:
            detalle_data = json.loads(item['detalle'])
            item['detalle_texto'] = detalle_data.get('texto', item['detalle'])
        except:
            item['detalle_texto'] = item['detalle']
        historial.append(item)
    
    return render_template('dashboard.html', historial=historial)

@app.route('/carreras')
@requiere_login
def carreras():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM carreras")
    lista_carreras = cursor.fetchall()
    return render_template('carreras.html', carreras=lista_carreras)

# --- SECCIÓN: TEST VOCACIONAL (CRUD de Resultados) ---

@app.route('/test', methods=['GET', 'POST'])
@requiere_login
def test():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        # Recolectar respuestas — soporta múltiples selecciones por pregunta
        puntuacion = {}
        for key in request.form.keys():
            if key.startswith('q_') or key.isdigit():
                areas = request.form.getlist(key)
                for area in areas:
                    if area and area.strip():
                        puntuacion[area.strip()] = puntuacion.get(area.strip(), 0) + 1

        # Validar que el usuario respondió algo
        if not puntuacion:
            flash('Por favor, respondé al menos una pregunta antes de finalizar.', 'warning')
            return redirect(url_for('test'))

        # Calcular área ganadora
        area_ganadora = max(puntuacion, key=puntuacion.get)
        puntaje_ganador = puntuacion[area_ganadora]

        # Construir detalle descriptivo como JSON válido (requerido por la BD)
        resumen = ', '.join([
            f"{a}: {p} pts"
            for a, p in sorted(puntuacion.items(), key=lambda x: x[1], reverse=True)
        ])
        detalle_resultado_texto = (
            f"Tu área de mayor afinidad es {area_ganadora} con {puntaje_ganador} respuestas. "
            f"Desglose: {resumen}."
        )
        # El campo detalle tiene CHECK(json_valid) en la BD — siempre guardamos JSON
        detalle_resultado_json = json.dumps({"texto": detalle_resultado_texto}, ensure_ascii=False)

        # Mapeo de área ganadora a area_id (FK requerida por la BD)
        area_ganadora_key = area_ganadora.lower().strip()
        area_id = 1  # Fallback seguro
        if 'tecnolog' in area_ganadora_key or 'ingenier' in area_ganadora_key:
            area_id = 1
        elif 'salud' in area_ganadora_key:
            area_id = 2
        elif 'derecho' in area_ganadora_key or 'social' in area_ganadora_key:
            area_id = 3
        elif 'arte' in area_ganadora_key or 'dise' in area_ganadora_key:
            area_id = 4
        elif 'humanidades' in area_ganadora_key or 'comunicaci' in area_ganadora_key:
            area_id = 5
        elif 'naturales' in area_ganadora_key or 'agronom' in area_ganadora_key:
            area_id = 6
        elif 'negocios' in area_ganadora_key or 'econom' in area_ganadora_key:
            area_id = 7

        try:
            # Insertar el test
            cursor.execute(
                "INSERT INTO tests (usuario_id, completado) VALUES (%s, %s)",
                (g.user['id'], 1)
            )
            id_test = cursor.lastrowid

            # Intento A: con todos los campos
            resultado_id = None
            try:
                cursor.execute(
                    """INSERT INTO resultados
                       (test_id, area_profesional_sugerida, area_id, puntaje, detalle)
                       VALUES (%s, %s, %s, %s, %s)""",
                    (id_test, area_ganadora, area_id, puntaje_ganador, detalle_resultado_json)
                )
                resultado_id = cursor.lastrowid
            except Exception as e1:
                # Intento B: sin puntaje como fallback
                cursor.execute(
                    """INSERT INTO resultados
                       (test_id, area_profesional_sugerida, area_id, detalle)
                       VALUES (%s, %s, %s, %s)""",
                    (id_test, area_ganadora, area_id, detalle_resultado_json)
                )
                resultado_id = cursor.lastrowid

            db.commit()
            flash(f'¡Test completado! Tu área principal es: {area_ganadora}.', 'success')
            return redirect(url_for('ver_resultado', resultado_id=resultado_id))

        except Exception as e:
            traceback.print_exc()
            db.rollback()
            flash(f'Error al guardar: {str(e)}', 'danger')
            return redirect(url_for('test'))

    # GET: cargar preguntas con sus opciones
    # NOTA: json ya está importado al inicio del archivo — NO repetir import aquí
    cursor.execute("SELECT * FROM preguntas ORDER BY id")
    preguntas_raw = cursor.fetchall()

    preguntas_con_opciones = []
    for p in preguntas_raw:
        cursor.execute(
            "SELECT texto_opcion, area_profesional FROM opciones_pregunta WHERE pregunta_id = %s",
            (p['id'],)
        )
        opciones = cursor.fetchall()
        preguntas_con_opciones.append({
            'id': p['id'],
            'texto_pregunta': p['texto_pregunta'],
            'opciones': [{'texto': o['texto_opcion'], 'area': o['area_profesional']} for o in opciones]
        })

    preguntas_json = json.dumps(preguntas_con_opciones, ensure_ascii=False)
    return render_template('test.html', preguntas=preguntas_raw, preguntas_json=preguntas_json)

# Ruta para ver el detalle de un resultado específico
@app.route('/resultado/<int:resultado_id>')
@requiere_login
def ver_resultado(resultado_id):
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
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

    # Procesar el detalle JSON para mostrarlo como texto legible
    try:
        detalle_data = json.loads(resultado['detalle'])
        resultado['detalle_texto'] = detalle_data.get('texto', resultado['detalle'])
    except:
        resultado['detalle_texto'] = resultado['detalle']

    # Buscar carreras sugeridas — búsqueda flexible en 3 niveles
    area = resultado['area_profesional_sugerida']
    
    cursor.execute(
        "SELECT * FROM carreras WHERE area_profesional = %s LIMIT 6",
        (area,)
    )
    carreras_sugeridas = cursor.fetchall()
    
    if not carreras_sugeridas:
        cursor.execute(
            "SELECT * FROM carreras WHERE area_profesional LIKE %s LIMIT 6",
            (f"%{area}%",)
        )
        carreras_sugeridas = cursor.fetchall()
    
    if not carreras_sugeridas:
        cursor.execute("SELECT * FROM carreras LIMIT 6")
        carreras_sugeridas = cursor.fetchall()

    return render_template('resultado_detalle.html', resultado=resultado, carreras=carreras_sugeridas)

# Listado histórico de todos los tests realizados por el usuario
@app.route('/mis-resultados')
@requiere_login
def mis_resultados():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.id, r.area_profesional_sugerida, t.fecha_realizacion,
               LEFT(r.detalle, 80) as detalle
        FROM resultados r
        JOIN tests t ON r.test_id = t.id
        WHERE t.usuario_id = %s
        ORDER BY t.fecha_realizacion DESC
    """, (g.user['id'],))
    resultados = cursor.fetchall()
    return render_template('mis_resultados.html', resultados=resultados)

@app.route('/resultado/actualizar/<int:resultado_id>', methods=['POST'])
@requiere_login
def actualizar_resultado(resultado_id):
    notas_personales = request.form['notas_personales']

    db = obtener_db()
    cursor = db.cursor()
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
    # IMPORTANTE: dictionary=True para poder acceder por nombre de columna 
    cursor = db.cursor(dictionary=True)

    # Buscar el test_id asociado al resultado, verificando que pertenece al usuario 
    cursor.execute(""" 
        SELECT t.id as test_id 
        FROM resultados r 
        JOIN tests t ON r.test_id = t.id 
        WHERE r.id = %s AND t.usuario_id = %s 
    """, (resultado_id, g.user['id'])) 
    test = cursor.fetchone() 

    if test: 
        # Eliminar el test — el resultado se elimina solo por CASCADE en la BD 
        cursor2 = db.cursor() 
        cursor2.execute("DELETE FROM tests WHERE id = %s", (test['test_id'],)) 
        db.commit() 
        flash('El resultado ha sido eliminado de tu historial.', 'info') 
    else: 
        flash('No se encontró el resultado o no tenés permiso para eliminarlo.', 'danger') 

    return redirect(url_for('mis_resultados'))

# --- SECCIÓN: HERRAMIENTAS ADICIONALES ---

@app.route('/juego')
@requiere_login
def juego():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM carreras")
    carreras_list = cursor.fetchall()
    carreras_json = json.dumps(carreras_list, ensure_ascii=False)
    return render_template('juego.html', carreras_json=carreras_json)

@app.route('/noticias') 
@requiere_login 
def noticias(): 
    db = obtener_db() 
    cursor = db.cursor(dictionary=True) 
 
    # Filtros recibidos por query string 
    filtro_fecha = request.args.get('fecha', 'todas') 
    filtro_fuente = request.args.get('fuente', 'todas') 
    filtro_categoria = request.args.get('categoria', 'todas') 
    busqueda = request.args.get('q', '').strip() 
 
    # Construir query dinámica con filtros 
    query = "SELECT * FROM noticias WHERE 1=1" 
    params = [] 
 
    if filtro_fecha == 'hoy': 
        query += " AND fecha = CURDATE()" 
    elif filtro_fecha == 'ayer': 
        query += " AND fecha = DATE_SUB(CURDATE(), INTERVAL 1 DAY)" 
    elif filtro_fecha == 'semana': 
        query += " AND fecha >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)" 
    elif filtro_fecha == 'mes': 
        query += " AND fecha >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)" 
 
    if filtro_fuente != 'todas': 
        query += " AND fuente = %s" 
        params.append(filtro_fuente) 
 
    if filtro_categoria != 'todas': 
        query += " AND categoria = %s" 
        params.append(filtro_categoria) 
 
    if busqueda: 
        query += " AND (titulo LIKE %s OR descripcion LIKE %s OR fuente LIKE %s)" 
        params.extend([f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%"]) 
 
    query += " ORDER BY fecha DESC, id DESC LIMIT 20" 
 
    cursor.execute(query, params) 
    items_noticias = cursor.fetchall() 
 
    # Obtener fuentes y categorías únicas para los filtros 
    cursor.execute("SELECT DISTINCT fuente FROM noticias ORDER BY fuente") 
    fuentes = [row['fuente'] for row in cursor.fetchall()] 
 
    cursor.execute("SELECT DISTINCT categoria FROM noticias ORDER BY categoria") 
    categorias = [row['categoria'] for row in cursor.fetchall()] 
 
    return render_template('noticias.html', 
        noticias=items_noticias, 
        fuentes=fuentes, 
        categorias=categorias, 
        filtro_fecha=filtro_fecha, 
        filtro_fuente=filtro_fuente, 
        filtro_categoria=filtro_categoria, 
        busqueda=busqueda 
    ) 

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
    
    cursor.execute("SELECT id, nombre, email, rol, fecha_registro FROM usuarios")
    usuarios = cursor.fetchall()
    
    cursor.execute("SELECT * FROM carreras")
    carreras = cursor.fetchall()
    
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

@app.route('/admin/noticias/actualizar-rss', methods=['POST']) 
@requiere_admin 
def actualizar_rss(): 
    """Ruta para que el admin actualice las noticias desde RSS manualmente""" 
    try: 
        from rss_fetcher import actualizar_noticias_rss 
        insertadas = actualizar_noticias_rss() 
        flash(f'RSS actualizado correctamente. {insertadas} nuevas noticias agregadas.', 'success') 
    except Exception as e: 
        flash(f'Error al actualizar RSS: {str(e)}', 'danger') 
    return redirect(url_for('admin_dashboard')) 

# --- MANEJO DE ERRORES ---

@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('base.html', content="<div class='container py-5 text-center'><h1>500</h1><p>Algo salió mal. Por favor, intenta más tarde.</p></div>"), 500

# Punto de entrada de la aplicación
if __name__ == '__main__':
    app.run(debug=True)