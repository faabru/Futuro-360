# Importación de librerías necesarias para el funcionamiento del servidor web
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
import json
import os
import traceback
import random
from functools import wraps
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import resend
from database_handler import obtener_db, inicializar_app

# Cargar las variables de entorno desde el archivo .env (configuración de BD y llaves secretas)
load_dotenv()

# Inicialización de la aplicación Flask
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# --- CONFIGURACIÓN DE RESEND (envío de emails) --- 
resend.api_key = os.getenv('RESEND_API_KEY') 
MAIL_FROM = "Futuro 360 <onboarding@resend.dev>" 

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

# --- RECUPERACIÓN DE CONTRASEÑA --- 
 
@app.route('/recuperar-password', methods=['GET', 'POST']) 
def recuperar_password(): 
    """PASO 1: El usuario ingresa su email y recibe el código PIN por Resend""" 
    if request.method == 'POST': 
        email = request.form.get('email', '').strip() 
 
        db = obtener_db() 
        cursor = db.cursor(dictionary=True) 
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,)) 
        usuario = cursor.fetchone() 
 
        if usuario: 
            # Generar código PIN de 6 dígitos 
            codigo = str(random.randint(100000, 999999)) 
 
            # Eliminar códigos anteriores y guardar el nuevo con expiración de 15 min 
            cursor2 = db.cursor() 
            cursor2.execute("DELETE FROM password_resets WHERE email = %s", (email,)) 
            cursor2.execute(""" 
                INSERT INTO password_resets (email, codigo, expira_en) 
                VALUES (%s, %s, DATE_ADD(NOW(), INTERVAL 15 MINUTE)) 
            """, (email, codigo)) 
            db.commit() 
 
            # Enviar email con Resend 
            try: 
                resend.Emails.send({ 
                    "from": MAIL_FROM, 
                    "to": [email], 
                    "subject": "🔐 Tu código de verificación - Futuro 360", 
                    "html": f""" 
                    <div style=\"font-family: sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #eee; border-radius: 10px; overflow: hidden;\">
                        <div style=\"background-color: #0d6efd; padding: 20px; text-align: center; color: white;\">
                            <h1 style=\"margin: 0;\">🎓 Futuro 360</h1>
                        </div>
                        <div style=\"padding: 30px; line-height: 1.6; color: #333;\">
                            <h2 style=\"color: #0d6efd; text-align: center;\">Recuperación de contraseña</h2>
                            <p style=\"text-align: center;\">Ingresá este código en la plataforma para continuar:</p>
                            <div style=\"background-color: #f8f9fa; padding: 20px; text-align: center; border-radius: 5px; margin: 20px 0;\">
                                <span style=\"font-size: 32px; font-weight: bold; letter-spacing: 5px; color: #0d6efd;\">{codigo}</span>
                            </div>
                            <p style=\"text-align: center; font-size: 0.9em; color: #666;\">⏱️ Este código expira en 15 minutos.</p>
                            <hr style=\"border: 0; border-top: 1px solid #eee; margin: 20px 0;\">
                            <p style=\"text-align: center; font-size: 0.8em; color: #999;\">Si no solicitaste este cambio, ignorá este mensaje.</p>
                        </div>
                        <div style=\"background-color: #f8f9fa; padding: 15px; text-align: center; font-size: 0.75em; color: #999;\">
                            Futuro 360 · Orientación Vocacional · Tucumán, Argentina
                        </div>
                    </div>
                    """ 
                }) 
                flash('✅ Te enviamos un código de 6 dígitos a tu correo. Revisá también spam.', 'success') 
            except Exception as e: 
                flash(f'Error al enviar el email: {str(e)}', 'danger') 
                return render_template('recuperar_password.html') 
        else: 
            # Siempre el mismo mensaje por seguridad 
            flash('✅ Si el correo está registrado, recibirás el código en breve.', 'info') 
 
        session['reset_email'] = email 
        return redirect(url_for('verificar_codigo')) 
 
    return render_template('recuperar_password.html') 
 
 
@app.route('/verificar-codigo', methods=['GET', 'POST']) 
def verificar_codigo(): 
    """PASO 2: El usuario ingresa el código de 6 dígitos""" 
    email = session.get('reset_email') 
    if not email: 
        flash('Sesión expirada. Por favor comenzá de nuevo.', 'warning') 
        return redirect(url_for('recuperar_password')) 
 
    if request.method == 'POST': 
        digitos = [request.form.get(f'd{i}', '') for i in range(1, 7)] 
        codigo_ingresado = ''.join(digitos).strip() 
 
        db = obtener_db() 
        cursor = db.cursor(dictionary=True) 
        cursor.execute(""" 
            SELECT * FROM password_resets 
            WHERE email = %s AND codigo = %s AND usado = 0 AND expira_en > NOW() 
        """, (email, codigo_ingresado)) 
        reset = cursor.fetchone() 
 
        if reset: 
            cursor2 = db.cursor() 
            cursor2.execute( 
                "UPDATE password_resets SET usado = 1 WHERE id = %s", 
                (reset['id'],) 
            ) 
            db.commit() 
            session['reset_verificado'] = True 
            flash('✅ Código verificado. Ahora podés crear tu nueva contraseña.', 'success') 
            return redirect(url_for('nueva_password')) 
        else: 
            flash('❌ Código incorrecto o expirado. Intentá de nuevo o solicitá uno nuevo.', 'danger') 
 
    return render_template('verificar_codigo.html', email=email) 
 
 
@app.route('/nueva-password', methods=['GET', 'POST']) 
def nueva_password(): 
    """PASO 3: El usuario ingresa su nueva contraseña""" 
    email = session.get('reset_email') 
    verificado = session.get('reset_verificado') 
 
    if not email or not verificado: 
        flash('Acceso no autorizado. Por favor comenzá de nuevo.', 'warning') 
        return redirect(url_for('recuperar_password')) 
 
    if request.method == 'POST': 
        password_nueva = request.form.get('password_nueva', '') 
        password_confirmar = request.form.get('password_confirmar', '') 
 
        if len(password_nueva) < 8: 
            flash('La contraseña debe tener al menos 8 caracteres.', 'danger') 
            return render_template('nueva_password.html') 
 
        if password_nueva != password_confirmar: 
            flash('Las contraseñas no coinciden. Intentá de nuevo.', 'danger') 
            return render_template('nueva_password.html') 
 
        db = obtener_db() 
        cursor = db.cursor() 
        cursor.execute( 
            "UPDATE usuarios SET password = %s WHERE email = %s", 
            (generate_password_hash(password_nueva), email) 
        ) 
        db.commit() 
 
        session.pop('reset_email', None) 
        session.pop('reset_verificado', None) 
 
        flash('🎉 ¡Contraseña actualizada! Ya podés iniciar sesión.', 'success') 
        return redirect(url_for('login')) 
 
    return render_template('nueva_password.html') 

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

    filtro = request.args.get('filtro', 'populares')  # ahora puede ser: populares | todas | [área profesional]
    busqueda = request.args.get('q', '').strip()

    # Determinar si el filtro es un área profesional, populares o todas
    cursor.execute("SELECT DISTINCT area_profesional FROM carreras ORDER BY area_profesional")
    areas_disponibles = [r['area_profesional'] for r in cursor.fetchall()]
    
    area_actual = 'todas'
    filtro_actual = filtro
    es_populares = filtro == 'populares'

    # Construir la consulta base
    query_where = " WHERE 1=1"
    params = []

    if es_populares:
        # Primero intentamos filtrar por populares (popular=1)
        # Pero si no hay resultados, mostraremos todas las carreras ordenadas por popularidad
        pass  # No filtramos por popular=1, solo ordenamos por popularidad descendente
    elif filtro in areas_disponibles:
        area_actual = filtro
        filtro_actual = 'todas'
        query_where += " AND area_profesional = %s"
        params.append(area_actual)

    if busqueda:
        query_where += " AND nombre LIKE %s"
        params.append(f"%{busqueda}%")

    # Construir la consulta final
    query = "SELECT * FROM carreras" + query_where + " ORDER BY popular DESC, nombre ASC"
    
    # Añadir LIMIT solo si es 'populares' y no hay búsqueda
    if es_populares and not busqueda:
        query += " LIMIT 6"

    cursor.execute(query, params)
    lista_carreras = cursor.fetchall()

    return render_template('carreras.html',
        carreras=lista_carreras,
        filtro_actual=filtro,
        area_actual=area_actual,
        busqueda=busqueda,
        areas_disponibles=areas_disponibles
    )

# --- SECCIÓN: TEST VOCACIONAL (CRUD de Resultados) ---

@app.route('/test', methods=['GET', 'POST'])
@requiere_login
def test():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        puntuacion = {}
        for key in request.form.keys():
            if key.startswith('q_') or key.isdigit():
                areas = request.form.getlist(key)
                for area in areas:
                    area_limpia = area.strip() if area else ''
                    # Ignorar valores nulos, vacíos, 'Neutral' o 'Ninguna de las anteriores' — no suman puntos
                    if area_limpia and area_limpia != 'Neutral' and area_limpia.lower() != 'ninguna de las anteriores':
                        puntuacion[area_limpia] = puntuacion.get(area_limpia, 0) + 1

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

# ELIMINADO por requisito de la tutora: los resultados no se pueden borrar,
# deben quedar almacenados permanentemente como historial académico.
# @app.route('/resultado/eliminar/<int:resultado_id>', methods=['POST'])
# @requiere_login
# def eliminar_resultado(resultado_id):
#     db = obtener_db()
#     # IMPORTANTE: dictionary=True para poder acceder por nombre de columna 
#     cursor = db.cursor(dictionary=True)
# 
#     # Buscar el test_id asociado al resultado, verificando que pertenece al usuario 
#     cursor.execute(""" 
#         SELECT t.id as test_id 
#         FROM resultados r 
#         JOIN tests t ON r.test_id = t.id 
#         WHERE r.id = %s AND t.usuario_id = %s 
#     """, (resultado_id, g.user['id'])) 
#     test = cursor.fetchone() 
# 
#     if test: 
#         # Eliminar el test — el resultado se elimina solo por CASCADE en la BD 
#         cursor2 = db.cursor() 
#         cursor2.execute("DELETE FROM tests WHERE id = %s", (test['test_id'],)) 
#         db.commit() 
#         flash('El resultado ha sido eliminado de tu historial.', 'info') 
#     else: 
#         flash('No se encontró el resultado o no tenés permiso para eliminarlo.', 'danger') 
# 
#     return redirect(url_for('mis_resultados'))


# --- SECCIÓN: HERRAMIENTAS ADICIONALES ---

@app.route('/juego')
@requiere_login
def juego():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    # Carreras activas en el juego
    cursor.execute("""
        SELECT gc.*, c.nombre as carrera_nombre, c.id as carrera_id, c.area_profesional
        FROM game_carreras gc
        JOIN carreras c ON gc.carrera_id = c.id
        WHERE gc.activo = 1
        ORDER BY gc.orden
    """)
    carreras_juego = cursor.fetchall()

    # Preguntas activas del mini-juego "Intereses en Juego"
    cursor.execute("""
        SELECT * FROM game_preguntas
        WHERE activo = 1
        ORDER BY orden, id
    """)
    game_preguntas = cursor.fetchall()

    carreras_json = json.dumps(
        [{'id': r['carrera_id'], 'nombre': r['carrera_nombre'],
          'area_profesional': r['area_profesional'],
          'descripcion': r['descripcion_card'] or '',
          'titulo_card': r['titulo_card'] or r['carrera_nombre'],
          'texto_boton': r['texto_boton'] or 'Ver carrera'} for r in carreras_juego],
        ensure_ascii=False
    )

    preguntas_json = json.dumps(
        [{'id': p['id'],
          'texto': p['texto_pregunta'],
          'opciones': [
              {'texto': p['opcion_a_texto'], 'area': p['opcion_a_area']},
              {'texto': p['opcion_b_texto'], 'area': p['opcion_b_area']}
          ]} for p in game_preguntas],
        ensure_ascii=False
    )

    return render_template('juego.html',
        carreras_json=carreras_json,
        carreras_juego=carreras_juego,
        preguntas_json=preguntas_json,
        game_preguntas=game_preguntas
    )

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

    # Verificar si existe un template HTML individual para esta carrera
    # Ejemplo: templates/carreras/carrera_39.html para Arquitectura (id=39)
    template_individual = f'carreras/carrera_{carrera_id}.html'
    template_path = os.path.join(app.template_folder, template_individual)

    if os.path.exists(template_path):
        # Usar el template personalizado de esta carrera específica
        return render_template(template_individual, carrera=carrera)
    else:
        # Fallback al template genérico — ninguna carrera queda sin página
        return render_template('carrera_detalle.html', carrera=carrera)

@app.route('/carrera/<int:carrera_id>/buscar-universidades')
def buscar_universidades(carrera_id):
    # Verificar sesión manualmente para poder responder JSON si no está logueado
    if g.user is None:
        return {"error": "Sesión expirada. Por favor iniciá sesión nuevamente.", "resultados": [], "status": "unauthorized"}, 401
    """
    Busca en la web universidades de Tucumán que dicten esta carrera utilizando Google Custom Search API.
    Versión optimizada con manejo de errores robusto y validaciones completas.
    """
    # Importar librerías necesarias (pueden estar en el top del archivo, pero por seguridad lo hacemos aquí también)
    import requests as req_lib
    from urllib.parse import quote_plus

    # Paso 1: Validación inicial de la carrera en la base de datos
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM carreras WHERE id = %s", (carrera_id,))
    carrera = cursor.fetchone()

    if not carrera:
        return {"error": "Carrera no encontrada", "resultados": []}, 404

    # Paso 2: (Omitido) Variables de Google Search ya no son necesarias
    # api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
    # engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')

    # Paso 3: Validación y preparación de la consulta
    # Construir una consulta enfocada en la carrera y la ubicación
    query_base = f"{carrera['nombre']} universidad facultad Tucumán site:edu.ar OR site:gov.ar"
    
    if not query_base:
        return {"error": "Consulta vacía", "resultados": []}, 400

    # Paso 4: Realizar la llamada a DuckDuckGo Search API
    try:
        from ddgs import DDGS
        
        resultados = []
        with DDGS() as ddgs:
            # ddgs.text devuelve diccionarios con: title, href, body
            results = list(ddgs.text(query_base, max_results=5))
            
        # Paso 5: Procesar la respuesta exitosa
        for item in results:
            resultados.append({
                "titulo": item.get("title", ""),
                "url": item.get("href", "#"),
                "descripcion": item.get("body", "")
            })

        return {"resultados": resultados, "total": len(resultados), "status": "success"}, 200

    except Exception as e:
        return {
            "error": f"Error interno del servidor al buscar en DDG: {str(e)}",
            "resultados": [],
            "status": "server_error"
        }, 500


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
        nombre = request.form.get('nombre', '')
        descripcion = request.form.get('descripcion', '')
        area_profesional = request.form.get('area_profesional', '')
        imagen_portada = request.form.get('imagen_portada', '')
        imagen_principal = request.form.get('imagen_principal', '')
        a_que_se_dedica = request.form.get('a_que_se_dedica', '')

        db = obtener_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO carreras (nombre, descripcion, area_profesional, instituciones, imagen_portada, imagen_principal, a_que_se_dedica) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (nombre, descripcion, area_profesional, '', imagen_portada, imagen_principal, a_que_se_dedica)
        )
        carrera_id_nueva = cursor.lastrowid
        # Agregar automáticamente al juego "Descubre tu carrera" (inactiva por defecto,
        # el admin la activa manualmente desde el panel del juego)
        cursor.execute(
            """INSERT INTO game_carreras (carrera_id, titulo_card, descripcion_card, activo)
               VALUES (%s, %s, %s, 0)""",
            (carrera_id_nueva, nombre, descripcion)
        )
        db.commit()
        flash('Carrera creada. Las instituciones se completarán con el buscador web en el detalle de la carrera.', 'success')
        return redirect(url_for('admin_carreras'))

    return render_template('admin/carrera_form.html', carrera=None)

@app.route('/admin/carreras/editar/<int:id>', methods=['GET', 'POST'])
@requiere_admin
def editar_carrera(id):
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'POST':
        nombre = request.form.get('nombre', '')
        descripcion = request.form.get('descripcion', '')
        area_profesional = request.form.get('area_profesional', '')
        imagen_portada = request.form.get('imagen_portada', '')
        imagen_principal = request.form.get('imagen_principal', '')
        a_que_se_dedica = request.form.get('a_que_se_dedica', '')
        
        cursor.execute(
            "UPDATE carreras SET nombre = %s, descripcion = %s, area_profesional = %s, imagen_portada = %s, imagen_principal = %s, a_que_se_dedica = %s WHERE id = %s",
            (nombre, descripcion, area_profesional, imagen_portada, imagen_principal, a_que_se_dedica, id)
        )
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
    cursor.execute("SELECT * FROM preguntas ORDER BY id")
    preguntas = cursor.fetchall()
    for p in preguntas:
        cursor.execute("SELECT * FROM opciones_pregunta WHERE pregunta_id = %s", (p['id'],))
        p['opciones'] = cursor.fetchall()
    return render_template('admin/preguntas_lista.html', preguntas=preguntas)


@app.route('/admin/preguntas/nueva', methods=['POST'])
@requiere_admin
def nueva_pregunta():
    texto_pregunta = request.form['texto_pregunta']
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO preguntas (texto_pregunta, area_profesional) VALUES (%s, %s)",
                   (texto_pregunta, 'General'))
    pregunta_id = cursor.lastrowid

    # Procesar las opciones enviadas dinámicamente (texto_opcion_N y area_opcion_N)
    i = 1
    while f'texto_opcion_{i}' in request.form:
        texto_opcion = request.form.get(f'texto_opcion_{i}', '').strip()
        area_opcion = request.form.get(f'area_opcion_{i}', '').strip()
        if texto_opcion and area_opcion:
            cursor.execute(
                "INSERT INTO opciones_pregunta (pregunta_id, texto_opcion, area_profesional) VALUES (%s, %s, %s)",
                (pregunta_id, texto_opcion, area_opcion)
            )
        i += 1

    db.commit()
    flash('Pregunta agregada con sus opciones exitosamente.', 'success')
    return redirect(url_for('admin_preguntas'))


@app.route('/admin/preguntas/eliminar/<int:id>', methods=['POST'])
@requiere_admin
def eliminar_pregunta(id):
    db = obtener_db()
    cursor = db.cursor()
    # Las opciones se eliminan automáticamente por ON DELETE CASCADE
    cursor.execute("DELETE FROM preguntas WHERE id = %s", (id,))
    db.commit()
    flash('Pregunta y sus opciones eliminadas.', 'info')
    return redirect(url_for('admin_preguntas'))


@app.route('/admin/preguntas/opcion/eliminar/<int:id>', methods=['POST'])
@requiere_admin
def eliminar_opcion_pregunta(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM opciones_pregunta WHERE id = %s", (id,))
    db.commit()
    flash('Opción eliminada.', 'info')
    return redirect(url_for('admin_preguntas'))

@app.route('/admin/noticias/actualizar-rss', methods=['POST'])
@requiere_admin
def actualizar_rss():
    """El admin puede actualizar las noticias desde RSS manualmente"""
    try:
        from rss_fetcher import actualizar_noticias_rss
        insertadas = actualizar_noticias_rss(max_por_fuente=8, scraping_imagen=True)
        if insertadas > 0:
            flash(f'✅ RSS actualizado. Se agregaron {insertadas} noticias nuevas.', 'success')
        else:
            flash('ℹ️ RSS actualizado. No hay noticias nuevas por el momento.', 'info')
    except Exception as e:
        flash(f'❌ Error al actualizar RSS: {str(e)}', 'danger')
    return redirect(url_for('admin_noticias')) 

# --- SECCIÓN: ADMIN JUEGO CARRERAS ---

@app.route('/admin/game/carreras')
@requiere_admin
def admin_game_carreras():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT gc.*, c.nombre as carrera_nombre, c.area_profesional
        FROM game_carreras gc
        JOIN carreras c ON gc.carrera_id = c.id
        ORDER BY gc.orden, c.nombre
    """)
    items = cursor.fetchall()
    return render_template('admin/game_carreras.html', items=items)


@app.route('/admin/game/carreras/toggle/<int:id>', methods=['POST'])
@requiere_admin
def toggle_game_carrera(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("UPDATE game_carreras SET activo = NOT activo WHERE id = %s", (id,))
    db.commit()
    flash('Estado actualizado en el juego.', 'success')
    return redirect(url_for('admin_game_carreras'))


@app.route('/admin/game/carreras/editar/<int:id>', methods=['POST'])
@requiere_admin
def editar_game_carrera(id):
    texto_boton = request.form.get('texto_boton', 'Ver carrera')
    titulo_card = request.form.get('titulo_card', '')
    descripcion_card = request.form.get('descripcion_card', '')

    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE game_carreras 
        SET texto_boton = %s, titulo_card = %s, descripcion_card = %s
        WHERE id = %s
    """, (texto_boton, titulo_card, descripcion_card, id))
    db.commit()
    flash('Tarjeta del juego actualizada.', 'success')
    return redirect(url_for('admin_game_carreras'))


# --- ADMIN: INTERESES EN JUEGO (preguntas del mini-juego) ---

@app.route('/admin/game/preguntas')
@requiere_admin
def admin_game_preguntas():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM game_preguntas ORDER BY orden, id")
    preguntas = cursor.fetchall()
    return render_template('admin/game_preguntas.html', preguntas=preguntas)


@app.route('/admin/game/preguntas/nueva', methods=['POST'])
@requiere_admin
def nueva_game_pregunta():
    texto_pregunta = request.form.get('texto_pregunta', '').strip()
    opcion_a_texto = request.form.get('opcion_a_texto', '').strip()
    opcion_a_area  = request.form.get('opcion_a_area', '').strip()
    opcion_b_texto = request.form.get('opcion_b_texto', '').strip()
    opcion_b_area  = request.form.get('opcion_b_area', '').strip()

    if not all([texto_pregunta, opcion_a_texto, opcion_a_area, opcion_b_texto, opcion_b_area]):
        flash('Todos los campos son obligatorios.', 'danger')
        return redirect(url_for('admin_game_preguntas'))

    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO game_preguntas
        (texto_pregunta, opcion_a_texto, opcion_a_area, opcion_b_texto, opcion_b_area)
        VALUES (%s, %s, %s, %s, %s)
    """, (texto_pregunta, opcion_a_texto, opcion_a_area, opcion_b_texto, opcion_b_area))
    db.commit()
    flash('Pregunta agregada al juego exitosamente.', 'success')
    return redirect(url_for('admin_game_preguntas'))


@app.route('/admin/game/preguntas/toggle/<int:id>', methods=['POST'])
@requiere_admin
def toggle_game_pregunta(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("UPDATE game_preguntas SET activo = NOT activo WHERE id = %s", (id,))
    db.commit()
    flash('Estado de la pregunta actualizado.', 'success')
    return redirect(url_for('admin_game_preguntas'))


@app.route('/admin/game/preguntas/eliminar/<int:id>', methods=['POST'])
@requiere_admin
def eliminar_game_pregunta(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM game_preguntas WHERE id = %s", (id,))
    db.commit()
    flash('Pregunta eliminada del juego.', 'info')
    return redirect(url_for('admin_game_preguntas'))


# --- SECCIÓN: ADMIN NOTICIAS ---

@app.route('/admin/noticias')
@requiere_admin
def admin_noticias():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM noticias ORDER BY fecha DESC")
    noticias = cursor.fetchall()
    cursor.execute("SELECT DISTINCT fuente FROM noticias ORDER BY fuente")
    fuentes = [r['fuente'] for r in cursor.fetchall()]
    return render_template('admin/noticias_lista.html', noticias=noticias, fuentes=fuentes)


@app.route('/admin/noticias/nueva', methods=['POST'])
@requiere_admin
def nueva_noticia():
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    imagen = request.form.get('imagen', '')
    fuente = request.form['fuente']
    fecha = request.form['fecha']
    link = request.form.get('link', '#')
    categoria = request.form.get('categoria', 'General')

    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO noticias (titulo, descripcion, imagen, fuente, fecha, link, categoria, es_externa)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 0)
    """, (titulo, descripcion, imagen, fuente, fecha, link, categoria))
    db.commit()
    flash('Noticia agregada exitosamente.', 'success')
    return redirect(url_for('admin_noticias'))


@app.route('/admin/noticias/eliminar/<int:id>', methods=['POST'])
@requiere_admin
def eliminar_noticia(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM noticias WHERE id = %s", (id,))
    db.commit()
    flash('Noticia eliminada.', 'info')
    return redirect(url_for('admin_noticias'))


# --- MANEJO DE ERRORES ---

@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('base.html', content="<div class='container py-5 text-center'><h1>500</h1><p>Algo salió mal. Por favor, intenta más tarde.</p></div>"), 500

# ─────────────────────────────────────────────────────────────────────────────
# AUTO-SINCRONIZACIÓN DE IMÁGENES
# Se ejecuta UNA VEZ al arrancar Flask. Actualiza imagen_portada e
# imagen_principal en la BD para las carreras que las tengan en NULL.
# Si los datos ya están cargados, el costo es prácticamente cero.
# ─────────────────────────────────────────────────────────────────────────────
def sincronizar_imagenes():
    """
    Escanea static/imagenes/ y actualiza los campos imagen_portada / imagen_principal
    de cada carrera que tenga esos campos en NULL.
    No toca registros que ya tienen imagen asignada.
    """
    imagenes_dir = os.path.join(app.static_folder, 'imagenes')
    if not os.path.isdir(imagenes_dir):
        return  # carpeta no existe, nada que hacer

    # Construir índice: nombre_archivo_sin_ext_lower → ruta_relativa_a_static
    index = {}
    for fname in os.listdir(imagenes_dir):
        ruta_relativa = 'imagenes/' + fname
        # Clave: nombre del archivo en minúsculas sin extensión
        clave = os.path.splitext(fname)[0].lower()
        index[clave] = ruta_relativa

    try:
        conn = obtener_db()
        cursor = conn.cursor(dictionary=True)

        # Traer solo carreras sin imágenes (optimización: evita tocar las ya completas)
        cursor.execute("""
            SELECT id, nombre, area_profesional, imagen_portada, imagen_principal
            FROM carreras
            WHERE imagen_portada IS NULL OR imagen_portada = ''
               OR imagen_principal IS NULL OR imagen_principal = ''
        """)
        carreras_sin_imagen = cursor.fetchall()

        if not carreras_sin_imagen:
            cursor.close()
            return  # Todas las carreras ya tienen imagen → nada que hacer

        actualizadas = 0
        for carrera in carreras_sin_imagen:
            area  = (carrera['area_profesional'] or '').lower().strip()
            nombre = (carrera['nombre'] or '').lower().strip()

            # Buscar portada y principal en el índice por coincidencia parcial
            portada   = None
            principal = None
            for clave, ruta in index.items():
                if area in clave and nombre in clave:
                    if 'portada' in clave:
                        portada = ruta
                    elif 'principal' in clave:
                        principal = ruta

            if portada or principal:
                cursor.execute("""
                    UPDATE carreras
                    SET imagen_portada   = COALESCE(NULLIF(imagen_portada, ''), %s),
                        imagen_principal = COALESCE(NULLIF(imagen_principal, ''), %s)
                    WHERE id = %s
                """, (portada, principal, carrera['id']))
                actualizadas += 1

        conn.commit()
        cursor.close()

        if actualizadas:
            app.logger.info(f'[imagenes] Auto-sync: {actualizadas} carreras actualizadas.')
        else:
            app.logger.info('[imagenes] Auto-sync: sin cambios necesarios.')

    except Exception as e:
        app.logger.warning(f'[imagenes] Auto-sync error (no crítico): {e}')


# Punto de entrada de la aplicación
if __name__ == '__main__':
    with app.app_context():
        sincronizar_imagenes()
    app.run(debug=True)