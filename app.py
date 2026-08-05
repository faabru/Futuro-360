# Importación de librerías necesarias para el funcionamiento del servidor web
from flask import Flask, render_template, request, redirect, url_for, session, flash, g, jsonify, get_flashed_messages
import json
import os
import time
import traceback
import random
import re
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
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

# --- CREDENCIALES DEL LOGIN DE ADMINISTRACIÓN ---
# Acceso exclusivo desde la navbar al panel de administración.
# El email/contraseña por defecto se cargan en la tabla admin_config
# la primera vez. La contraseña puede cambiarse desde la recuperación.
ADMIN_USUARIO = "usuario123"
ADMIN_PASSWORD = "123456789"
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'fabriciovillagra05@gmail.com')


def asegurar_tabla_admin_config():
    """Crea la tabla de configuración del admin si no existe y la
    inicializa con las credenciales por defecto."""
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_config (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL,
            password_hash VARCHAR(255) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cursor.execute("SELECT * FROM admin_config WHERE usuario = %s", (ADMIN_USUARIO,))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO admin_config (usuario, email, password_hash)
            VALUES (%s, %s, %s)
        """, (ADMIN_USUARIO, ADMIN_EMAIL,
              generate_password_hash(ADMIN_PASSWORD)))
        db.commit()

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

def es_ajax():
    """True si la petición fue hecha con fetch/AJAX (X-Requested-With)."""
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


def ajax_o_redirect(f):
    """Si la petición es AJAX responde JSON con ok=True; si no, ejecuta la ruta normal."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        resultado = f(*args, **kwargs)
        if es_ajax():
            # Limpiar mensajes flash acumulados para no arrastrarlos al recargar
            list(get_flashed_messages())
            return jsonify(ok=True)
        return resultado
    return decorated_function

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
        # Acceso concedido desde el login exclusivo de administración (navbar)
        if session.get('admin_autenticado'):
            return f(*args, **kwargs)
        if g.user is None:
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
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
               r.detalle
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
            texto = detalle_data.get('texto', item['detalle'])
        except:
            texto = item['detalle']
        item['detalle_texto'] = texto if len(texto) <= 160 else texto[:160].rsplit(' ', 1)[0] + '…'
        historial.append(item)

    # Total de tests realizados por el usuario
    cursor.execute("""
        SELECT COUNT(*) AS total, MAX(t.fecha_realizacion) AS ultima_fecha
        FROM tests t
        WHERE t.usuario_id = %s
    """, (g.user['id'],))
    stats_tests = cursor.fetchone()
    total_tests = stats_tests['total'] if stats_tests else 0
    ultima_fecha_test = stats_tests['ultima_fecha'] if stats_tests else None

    # Total de carreras y de noticias recientes para la sección de novedades
    cursor.execute("SELECT COUNT(*) AS total FROM carreras")
    total_carreras = cursor.fetchone()['total']

    cursor.execute("""
        SELECT id, titulo, fuente, fecha
        FROM noticias
        WHERE fecha IS NOT NULL
        ORDER BY fecha DESC
        LIMIT 3
    """)
    noticias_recientes = cursor.fetchall()

    return render_template('dashboard.html',
        historial=historial,
        total_tests=total_tests,
        ultima_fecha_test=ultima_fecha_test,
        total_carreras=total_carreras,
        noticias_recientes=noticias_recientes)

@app.route('/carreras')
@requiere_login
def carreras():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    filtro = request.args.get('filtro', 'populares')  # ahora puede ser: populares | todas | [área profesional]
    busqueda = request.args.get('q', '').strip()

    # Determinar si el filtro es un área profesional, populares o todas.
    # Las áreas disponibles vienen de la tabla de orientaciones (gestionada desde
    # el panel admin) + las áreas ya asignadas a carreras en la base.
    asegurar_tabla_orientaciones()
    cursor.execute("SELECT nombre FROM orientaciones ORDER BY nombre")
    areas_registradas = [r['nombre'] for r in cursor.fetchall()]
    cursor.execute("SELECT DISTINCT area_profesional FROM carreras ORDER BY area_profesional")
    areas_carreras = [r['area_profesional'] for r in cursor.fetchall()]
    areas_disponibles = list(dict.fromkeys(areas_registradas + areas_carreras))
    
    area_actual = 'todas'
    filtro_actual = filtro
    es_populares = filtro == 'populares'

    # Traemos todas las carreras: el filtrado por área y la búsqueda se realizan
    # en el cliente (JS) para no recargar la página al buscar o filtrar.
    query = "SELECT * FROM carreras ORDER BY popular DESC, nombre ASC"
    cursor.execute(query)
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

        # Guardar respuestas individuales para mostrarlas después
        respuestas_detalle = []
        for key, val in request.form.items():
            if key.startswith('opcion_'):
                pregunta_id = key.replace('opcion_', '')
                pregunta_texto = request.form.get('pregunta_' + pregunta_id, '')
                area_sel = request.form.get(pregunta_id, '')
                if area_sel == 'Neutral':
                    area_sel = None
                respuestas_detalle.append({
                    "pregunta": pregunta_texto,
                    "opcion": val,
                    "area": area_sel
                })

        # Construir detalle descriptivo como JSON válido (requerido por la BD)
        resumen = [
            {"area": a, "puntos": p}
            for a, p in sorted(puntuacion.items(), key=lambda x: x[1], reverse=True)
        ]
        resumen_texto = ', '.join([f"{r['area']}: {r['puntos']} pts" for r in resumen])
        detalle_resultado_texto = (
            f"Tu área de mayor afinidad es {area_ganadora} con {puntaje_ganador} respuestas. "
            f"Desglose: {resumen_texto}."
        )
        # El campo detalle tiene CHECK(json_valid) en la BD — siempre guardamos JSON
        detalle_resultado_json = json.dumps({
            "texto": detalle_resultado_texto,
            "resumen": resumen,
            "respuestas": respuestas_detalle
        }, ensure_ascii=False)

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
    resumen_puntuacion = []
    respuestas_usuario = []
    try:
        detalle_data = json.loads(resultado['detalle'])
        resultado['detalle_texto'] = detalle_data.get('texto', resultado['detalle'])
        resumen_puntuacion = detalle_data.get('resumen', [])
        respuestas_usuario = detalle_data.get('respuestas', [])
    except:
        resultado['detalle_texto'] = resultado['detalle']

    # Si no hay respuestas guardadas (tests viejos), intentar reconstruir desde el texto
    if not respuestas_usuario and not resumen_puntuacion:
        texto = resultado['detalle_texto']
        partes = re.findall(r'([\w\s]+?):\s*(\d+)\s*pts', texto)
        resumen_puntuacion = [{"area": a.strip(), "puntos": int(p)} for a, p in partes]

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

    return render_template('resultado_detalle.html',
        resultado=resultado,
        carreras=carreras_sugeridas,
        resumen_puntuacion=resumen_puntuacion,
        respuestas_usuario=respuestas_usuario)

# Listado histórico de todos los tests realizados por el usuario
@app.route('/mis-resultados')
@requiere_login
def mis_resultados():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.id, r.area_profesional_sugerida, t.fecha_realizacion,
               r.detalle
        FROM resultados r
        JOIN tests t ON r.test_id = t.id
        WHERE t.usuario_id = %s
        ORDER BY t.fecha_realizacion DESC
    """, (g.user['id'],))
    resultados = cursor.fetchall()
    for item in resultados:
        try:
            detalle_data = json.loads(item['detalle'])
            texto = detalle_data.get('texto', item['detalle'])
        except:
            texto = item['detalle']
        item['detalle_texto'] = texto if len(texto) <= 160 else texto[:160].rsplit(' ', 1)[0] + '…'
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

    # Asegura las columnas de los botones en game_carreras
    asegurar_columnas_botones_game(db, cursor)

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
          'texto_boton': r['texto_boton'] or 'Ver carrera',
          'boton_no': r.get('boton_no') or 'No es lo mío',
          'boton_info': r.get('boton_info') or 'Info',
          'boton_yes': r.get('boton_yes') or 'Me interesa'} for r in carreras_juego],
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

    asegurar_tabla_filtros_fecha()

    # Construir query dinámica con filtros 
    query = "SELECT * FROM noticias WHERE 1=1" 
    params = [] 

    # Filtro por fecha: usa la condición guardada en la tabla filtros_fecha
    if filtro_fecha != 'todas': 
        cursor.execute("SELECT condicion FROM filtros_fecha WHERE valor = %s", (filtro_fecha,)) 
        fila_fecha = cursor.fetchone() 
        if fila_fecha and fila_fecha['condicion']: 
            query += " AND " + fila_fecha['condicion'] 

 
    if filtro_fuente != 'todas': 
        query += " AND fuente = %s" 
        params.append(filtro_fuente) 
 
    # La búsqueda por texto y la categoría se filtran en el cliente (JS) para
    # no recargar la página. La fecha y la fuente se mantienen del lado servidor.
    query += " ORDER BY fecha DESC, id DESC" 
 
    cursor.execute(query, params) 
    items_noticias = cursor.fetchall() 
 
    # Obtener fuentes y categorías únicas para los filtros.
    # Las fuentes visibles son las registradas (activas) en la tabla fuentes,
    # más las fuentes de noticias que todavía no están registradas en la tabla.
    # Las categorías incluyen las orientaciones registradas en el panel admin.
    asegurar_tabla_fuentes()
    cursor.execute("SELECT nombre FROM fuentes WHERE activo = 1 ORDER BY nombre")
    fuentes_activas = [row['nombre'] for row in cursor.fetchall()]
    cursor.execute("SELECT nombre FROM fuentes")
    todas_registradas = [row['nombre'] for row in cursor.fetchall()]
    cursor.execute("SELECT nombre FROM fuentes_eliminadas")
    fuentes_eliminadas = [row['nombre'] for row in cursor.fetchall()]
    cursor.execute("SELECT DISTINCT fuente FROM noticias ORDER BY fuente")
    fuentes_noticias = [row['fuente'] for row in cursor.fetchall()]
    fuentes = list(dict.fromkeys(
        fuentes_activas + [f for f in fuentes_noticias if f not in todas_registradas and f not in fuentes_eliminadas]
    ))

    asegurar_tabla_orientaciones()
    cursor.execute("SELECT nombre FROM orientaciones ORDER BY nombre")
    areas_registradas = [row['nombre'] for row in cursor.fetchall()]
    cursor.execute("SELECT DISTINCT categoria FROM noticias ORDER BY categoria")
    categorias_noticias = [row['categoria'] for row in cursor.fetchall()]
    categorias = list(dict.fromkeys(areas_registradas + categorias_noticias))

    asegurar_tabla_filtros_fecha()
    cursor.execute("SELECT valor, etiqueta FROM filtros_fecha WHERE activo = 1 ORDER BY orden, id")
    filtros_fecha = cursor.fetchall()

    return render_template('noticias.html',
        noticias=items_noticias,
        fuentes=fuentes,
        categorias=categorias,
        filtros_fecha=filtros_fecha,
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

# Login exclusivo del administrador (acceso rápido desde la navbar)
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Login independiente para el panel de administración"""
    if session.get('admin_autenticado'):
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        password = request.form.get('password', '')

        asegurar_tabla_admin_config()
        db = obtener_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM admin_config WHERE usuario = %s",
            (usuario,)
        )
        admin = cursor.fetchone()

        if admin and check_password_hash(admin['password_hash'], password):
            session['admin_autenticado'] = True
            flash('¡Bienvenido al panel de administración!', 'success')
            return redirect(url_for('admin_dashboard'))

        flash('Usuario o contraseña incorrectos.', 'danger')

    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    """Cierra la sesión exclusiva de administración"""
    session.pop('admin_autenticado', None)
    flash('Sesión de administrador cerrada.', 'info')
    return redirect(url_for('admin_login'))


@app.route('/admin/recuperar-password', methods=['GET', 'POST'])
def admin_recuperar_password():
    """PASO 1: El admin ingresa su correo y recibe el código PIN por Resend"""
    if session.get('admin_autenticado'):
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()

        # El código solo se envía si el email coincide con el configurado
        if email == ADMIN_EMAIL:
            codigo = str(random.randint(100000, 999999))

            db = obtener_db()
            cursor2 = db.cursor()
            cursor2.execute("DELETE FROM password_resets WHERE email = %s", (email,))
            cursor2.execute("""
                INSERT INTO password_resets (email, codigo, expira_en)
                VALUES (%s, %s, DATE_ADD(NOW(), INTERVAL 15 MINUTE))
            """, (email, codigo))
            db.commit()

            try:
                resend.Emails.send({
                    "from": MAIL_FROM,
                    "to": [email],
                    "subject": "🔐 Tu código de verificación - Panel Admin Futuro 360",
                    "html": f"""
                    <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #eee; border-radius: 10px; overflow: hidden;">
                        <div style="background-color: #dc3545; padding: 20px; text-align: center; color: white;">
                            <h1 style="margin: 0;">🛡️ Panel Admin - Futuro 360</h1>
                        </div>
                        <div style="padding: 30px; line-height: 1.6; color: #333;">
                            <h2 style="color: #dc3545; text-align: center;">Recuperación de contraseña</h2>
                            <p style="text-align: center;">Ingresá este código en el panel para continuar:</p>
                            <div style="background-color: #f8f9fa; padding: 20px; text-align: center; border-radius: 5px; margin: 20px 0;">
                                <span style="font-size: 32px; font-weight: bold; letter-spacing: 5px; color: #dc3545;">{codigo}</span>
                            </div>
                            <p style="text-align: center; font-size: 0.9em; color: #666;">⏱️ Este código expira en 15 minutos.</p>
                            <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                            <p style="text-align: center; font-size: 0.8em; color: #999;">Si no solicitaste este cambio, ignorá este mensaje.</p>
                        </div>
                        <div style="background-color: #f8f9fa; padding: 15px; text-align: center; font-size: 0.75em; color: #999;">
                            Futuro 360 · Orientación Vocacional · Tucumán, Argentina
                        </div>
                    </div>
                    """
                })
                flash('✅ Te enviamos un código de 6 dígitos a tu correo. Revisá también spam.', 'success')
            except Exception as e:
                flash(f'Error al enviar el email: {str(e)}', 'danger')
                return render_template('admin/recuperar_password.html')
        else:
            # Siempre el mismo mensaje por seguridad
            flash('✅ Si el correo está registrado, recibirás el código en breve.', 'info')

        session['admin_reset_email'] = email
        return redirect(url_for('admin_verificar_codigo'))

    return render_template('admin/recuperar_password.html')


@app.route('/admin/verificar-codigo', methods=['GET', 'POST'])
def admin_verificar_codigo():
    """PASO 2: El admin ingresa el código de 6 dígitos"""
    email = session.get('admin_reset_email')
    if not email:
        flash('Sesión expirada. Por favor comenzá de nuevo.', 'warning')
        return redirect(url_for('admin_recuperar_password'))

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
            session['admin_reset_verificado'] = True
            flash('✅ Código verificado. Ahora podés crear tu nueva contraseña.', 'success')
            return redirect(url_for('admin_nueva_password'))
        else:
            flash('❌ Código incorrecto o expirado. Intentá de nuevo o solicitá uno nuevo.', 'danger')

    return render_template('admin/verificar_codigo.html', email=email)


@app.route('/admin/nueva-password', methods=['GET', 'POST'])
def admin_nueva_password():
    """PASO 3: El admin ingresa su nueva contraseña"""
    email = session.get('admin_reset_email')
    verificado = session.get('admin_reset_verificado')

    if not email or not verificado:
        flash('Acceso no autorizado. Por favor comenzá de nuevo.', 'warning')
        return redirect(url_for('admin_recuperar_password'))

    if request.method == 'POST':
        password_nueva = request.form.get('password_nueva', '')
        password_confirmar = request.form.get('password_confirmar', '')

        if len(password_nueva) < 8:
            flash('La contraseña debe tener al menos 8 caracteres.', 'danger')
            return render_template('admin/nueva_password.html')

        if password_nueva != password_confirmar:
            flash('Las contraseñas no coinciden. Intentá de nuevo.', 'danger')
            return render_template('admin/nueva_password.html')

        db = obtener_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE admin_config SET password_hash = %s WHERE usuario = %s",
            (generate_password_hash(password_nueva), ADMIN_USUARIO)
        )
        db.commit()

        session.pop('admin_reset_email', None)
        session.pop('admin_reset_verificado', None)

        flash('🎉 ¡Contraseña del panel actualizada! Ya podés iniciar sesión.', 'success')
        return redirect(url_for('admin_login'))

    return render_template('admin/nueva_password.html')


@app.route('/admin')
@requiere_admin
def admin_dashboard():
    asegurar_tabla_orientaciones()
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT id, nombre, email, rol, created_at FROM usuarios")
    usuarios = cursor.fetchall()

    cursor.execute("SELECT * FROM carreras")
    carreras = cursor.fetchall()

    cursor.execute("SELECT * FROM preguntas")
    preguntas = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) AS total FROM noticias")
    total_noticias = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) AS total FROM noticias WHERE fecha = CURDATE()")
    noticias_hoy = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) AS total FROM game_carreras WHERE activo = 1")
    carreras_juego_activas = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) AS total FROM game_preguntas WHERE activo = 1")
    preguntas_juego_activas = cursor.fetchone()['total']

    cursor.execute("SELECT * FROM orientaciones ORDER BY nombre")
    orientaciones = cursor.fetchall()

    return render_template('admin/dashboard.html',
        usuarios=usuarios, carreras=carreras, preguntas=preguntas,
        total_noticias=total_noticias, noticias_hoy=noticias_hoy,
        carreras_juego_activas=carreras_juego_activas,
        preguntas_juego_activas=preguntas_juego_activas,
        orientaciones=orientaciones)


# --- SECCIÓN: ORIENTACIONES (áreas profesionales) ---

def asegurar_tabla_orientaciones():
    """Crea la tabla de orientaciones si no existe y la llena con las áreas
    actuales de las carreras (para que el filtro nunca quede vacío)."""
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orientaciones (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL UNIQUE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cursor.execute("""
        INSERT IGNORE INTO orientaciones (nombre)
        SELECT DISTINCT area_profesional FROM carreras
        WHERE area_profesional IS NOT NULL AND area_profesional <> ''
    """)
    db.commit()


@app.route('/admin/orientaciones/nueva', methods=['POST'])
@requiere_admin
def nueva_orientacion():
    nombre = request.form.get('nombre', '').strip()
    if not nombre:
        flash('El nombre de la orientación no puede estar vacío.', 'danger')
        return redirect(url_for('admin_dashboard'))

    asegurar_tabla_orientaciones()
    db = obtener_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO orientaciones (nombre) VALUES (%s)", (nombre,))
        db.commit()
        flash(f'Orientación "{nombre}" agregada. Ya aparece en los filtros de búsqueda.', 'success')
    except Exception:
        db.rollback()
        flash('Esa orientación ya está registrada.', 'warning')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/orientaciones/eliminar/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def eliminar_orientacion(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM orientaciones WHERE id = %s", (id,))
    db.commit()
    flash('Orientación eliminada.', 'info')
    return redirect(url_for('admin_dashboard'))

# CRUD de Carreras

EXTENSIONES_IMAGEN = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def guardar_imagen_carrera(archivo):
    """Guarda una imagen subida desde el formulario en static/imagenes/.
    Devuelve la ruta relativa 'imagenes/<nombre>' o None si no hay archivo válido."""
    if archivo is None or not archivo.filename:
        return None

    nombre_original = secure_filename(archivo.filename)
    if not nombre_original:
        return None

    ext = nombre_original.rsplit('.', 1)[-1].lower() if '.' in nombre_original else ''
    if ext not in EXTENSIONES_IMAGEN:
        return None

    # Nombre único para evitar colisiones (prefijo con timestamp)
    nombre = f"carrera_{int(time.time())}_{nombre_original}"
    ruta = os.path.join(app.static_folder, 'imagenes', nombre)
    archivo.save(ruta)
    return f"imagenes/{nombre}"

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
        a_que_se_dedica = request.form.get('a_que_se_dedica', '')

        # Imágenes: si se sube un archivo, se usa en lugar de la URL
        imagen_portada = request.form.get('imagen_portada', '')
        imagen_principal = request.form.get('imagen_principal', '')
        imagen_portada_subida = guardar_imagen_carrera(request.files.get('imagen_portada_file'))
        imagen_principal_subida = guardar_imagen_carrera(request.files.get('imagen_principal_file'))
        if imagen_portada_subida:
            imagen_portada = imagen_portada_subida
        if imagen_principal_subida:
            imagen_principal = imagen_principal_subida

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
        a_que_se_dedica = request.form.get('a_que_se_dedica', '')

        # Imágenes: si se sube un archivo, se usa en lugar de la URL
        imagen_portada = request.form.get('imagen_portada', '')
        imagen_principal = request.form.get('imagen_principal', '')
        imagen_portada_subida = guardar_imagen_carrera(request.files.get('imagen_portada_file'))
        imagen_principal_subida = guardar_imagen_carrera(request.files.get('imagen_principal_file'))
        if imagen_portada_subida:
            imagen_portada = imagen_portada_subida
        if imagen_principal_subida:
            imagen_principal = imagen_principal_subida
        
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
@ajax_o_redirect
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
    asegurar_tabla_orientaciones()
    cursor.execute("SELECT nombre FROM orientaciones ORDER BY nombre")
    orientaciones = [o['nombre'] for o in cursor.fetchall()]
    return render_template('admin/preguntas_lista.html', preguntas=preguntas, orientaciones=orientaciones)


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
@ajax_o_redirect
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
@ajax_o_redirect
def eliminar_opcion_pregunta(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM opciones_pregunta WHERE id = %s", (id,))
    db.commit()
    flash('Opción eliminada.', 'info')
    return redirect(url_for('admin_preguntas'))

# --- SECCIÓN: ADMIN JUEGO ---

@app.route('/admin/game')
@requiere_admin
def admin_game_index():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS n FROM game_carreras WHERE activo = 1")
    carreras_activas = cursor.fetchone()['n']
    cursor.execute("SELECT COUNT(*) AS n FROM game_carreras")
    carreras_total = cursor.fetchone()['n']

    cursor.execute("SELECT COUNT(*) AS n FROM game_preguntas WHERE activo = 1")
    preguntas_activas = cursor.fetchone()['n']
    cursor.execute("SELECT COUNT(*) AS n FROM game_preguntas")
    preguntas_total = cursor.fetchone()['n']

    return render_template('admin/game_index.html',
        carreras_activas=carreras_activas, carreras_total=carreras_total,
        preguntas_activas=preguntas_activas, preguntas_total=preguntas_total)


# --- SECCIÓN: ADMIN JUEGO CARRERAS ---

@app.route('/admin/game/carreras')
@requiere_admin
def admin_game_carreras():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    asegurar_columnas_botones_game(db, cursor)
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
@ajax_o_redirect
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
    boton_no = request.form.get('boton_no', 'No es lo mío')
    boton_info = request.form.get('boton_info', 'Info')
    boton_yes = request.form.get('boton_yes', 'Me interesa')

    db = obtener_db()
    cursor = db.cursor()
    asegurar_columnas_botones_game(db, cursor)
    cursor.execute("""
        UPDATE game_carreras 
        SET texto_boton = %s, titulo_card = %s, descripcion_card = %s,
            boton_no = %s, boton_info = %s, boton_yes = %s
        WHERE id = %s
    """, (texto_boton, titulo_card, descripcion_card, boton_no, boton_info, boton_yes, id))
    db.commit()
    flash('Tarjeta del juego actualizada.', 'success')
    return redirect(url_for('admin_game_carreras'))


def asegurar_columnas_botones_game(db, cursor):
    """Agrega las columnas de texto de los botones del juego
    'Descubre tu Carrera' a la tabla game_carreras si no existen."""
    columnas = {
        'boton_no': "ADD COLUMN boton_no VARCHAR(100) NOT NULL DEFAULT 'No es lo mío'",
        'boton_info': "ADD COLUMN boton_info VARCHAR(100) NOT NULL DEFAULT 'Info'",
        'boton_yes': "ADD COLUMN boton_yes VARCHAR(100) NOT NULL DEFAULT 'Me interesa'",
    }
    cursor.execute("SHOW COLUMNS FROM game_carreras")
    filas = cursor.fetchall()
    existentes = {r['Field'] if isinstance(r, dict) else r[0] for r in filas}
    for nombre, ddl in columnas.items():
        if nombre not in existentes:
            cursor.execute(f"ALTER TABLE game_carreras {ddl}")
            existentes.add(nombre)
    db.commit()


# --- ADMIN: INTERESES EN JUEGO (preguntas del mini-juego) ---

@app.route('/admin/game/preguntas')
@requiere_admin
def admin_game_preguntas():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM game_preguntas ORDER BY orden, id")
    preguntas = cursor.fetchall()
    asegurar_tabla_orientaciones()
    cursor.execute("SELECT nombre FROM orientaciones ORDER BY nombre")
    orientaciones = [o['nombre'] for o in cursor.fetchall()]
    return render_template('admin/game_preguntas.html', preguntas=preguntas, orientaciones=orientaciones)


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
@ajax_o_redirect
def toggle_game_pregunta(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("UPDATE game_preguntas SET activo = NOT activo WHERE id = %s", (id,))
    db.commit()
    flash('Estado de la pregunta actualizado.', 'success')
    return redirect(url_for('admin_game_preguntas'))


@app.route('/admin/game/preguntas/eliminar/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def eliminar_game_pregunta(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM game_preguntas WHERE id = %s", (id,))
    db.commit()
    flash('Pregunta eliminada del juego.', 'info')
    return redirect(url_for('admin_game_preguntas'))


# --- SECCIÓN: ADMIN NOTICIAS ---

def asegurar_tabla_fuentes():
    """Crea la tabla de fuentes si no existe, le agrega la columna activo
    y registra automáticamente las fuentes que ya están en las noticias,
    excepto las que fueron eliminadas a propósito."""
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fuentes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL UNIQUE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cursor.execute("SHOW COLUMNS FROM fuentes LIKE 'activo'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE fuentes ADD COLUMN activo TINYINT(1) DEFAULT 1")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fuentes_eliminadas (
            nombre VARCHAR(100) NOT NULL PRIMARY KEY
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cursor.execute("SELECT nombre FROM fuentes_eliminadas")
    eliminadas = {r[0] for r in cursor.fetchall()}
    # Registra las fuentes de las noticias que todavía no están eliminadas
    cursor.execute("SELECT DISTINCT fuente FROM noticias WHERE fuente IS NOT NULL AND fuente <> ''")
    for (nombre,) in cursor.fetchall():
        if nombre not in eliminadas:
            cursor.execute("INSERT IGNORE INTO fuentes (nombre) VALUES (%s)", (nombre,))
    db.commit()


def asegurar_tabla_filtros_fecha():
    """Crea la tabla de filtros de fecha del buscador de noticias.
    Cada filtro guarda su etiqueta y la condición SQL que usa para filtrar,
    así el admin puede agregar sus propios rangos de fecha."""
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS filtros_fecha (
            id INT AUTO_INCREMENT PRIMARY KEY,
            valor VARCHAR(30) NOT NULL UNIQUE,
            etiqueta VARCHAR(50) NOT NULL,
            condicion VARCHAR(250) NOT NULL DEFAULT '',
            activo TINYINT(1) DEFAULT 1,
            orden INT DEFAULT 0,
            es_fijo TINYINT(1) DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    for col, ddl in [
        ('condicion', "ADD COLUMN condicion VARCHAR(250) NOT NULL DEFAULT ''"),
        ('es_fijo', 'ADD COLUMN es_fijo TINYINT(1) DEFAULT 0'),
    ]:
        cursor.execute(f"SHOW COLUMNS FROM filtros_fecha LIKE '{col}'")
        if not cursor.fetchone():
            cursor.execute(f"ALTER TABLE filtros_fecha {ddl}")

    cursor.execute("SELECT COUNT(*) AS n FROM filtros_fecha")
    if cursor.fetchone()['n'] == 0:
        presets = [
            ('todas', 'Todas', '', 1, 0, 1),
            ('hoy', 'Hoy', 'fecha = CURDATE()', 1, 1, 1),
            ('ayer', 'Ayer', 'fecha = DATE_SUB(CURDATE(), INTERVAL 1 DAY)', 1, 2, 1),
            ('semana', 'Esta semana', 'fecha >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)', 1, 3, 1),
            ('mes', 'Este mes', 'fecha >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)', 1, 4, 1),
        ]
        cursor.executemany(
            "INSERT INTO filtros_fecha (valor, etiqueta, condicion, activo, orden, es_fijo) VALUES (%s, %s, %s, %s, %s, %s)",
            presets
        )

    # Backfill: asegura que los filtros predefinidos tengan su condición y no sean borrables
    backfill = {
        'todas': '',
        'hoy': 'fecha = CURDATE()',
        'ayer': 'fecha = DATE_SUB(CURDATE(), INTERVAL 1 DAY)',
        'semana': 'fecha >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)',
        'mes': 'fecha >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)',
    }
    for valor, cond in backfill.items():
        cursor.execute("UPDATE filtros_fecha SET condicion = %s, es_fijo = 1 WHERE valor = %s", (cond, valor))
    db.commit()

def guardar_imagen_noticia(archivo):
    """Guarda la imagen de una noticia en static/imagenes/noticias/.
    Devuelve la ruta relativa 'imagenes/noticias/<nombre>' o None."""
    if archivo is None or not archivo.filename:
        return None

    nombre_original = secure_filename(archivo.filename)
    if not nombre_original:
        return None

    ext = nombre_original.rsplit('.', 1)[-1].lower() if '.' in nombre_original else ''
    if ext not in EXTENSIONES_IMAGEN:
        return None

    carpeta = os.path.join(app.static_folder, 'imagenes', 'noticias')
    os.makedirs(carpeta, exist_ok=True)

    nombre = f"noticia_{int(time.time())}_{nombre_original}"
    archivo.save(os.path.join(carpeta, nombre))
    return f"imagenes/noticias/{nombre}"

@app.route('/admin/noticias')
@requiere_admin
def admin_noticias():
    asegurar_tabla_fuentes()
    asegurar_tabla_filtros_fecha()
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    filtro_fecha = request.args.get('fecha', 'todas')
    filtro_fuente = request.args.get('fuente', 'todas')
    filtro_categoria = request.args.get('categoria', 'todas')
    busqueda = request.args.get('q', '').strip()

    # Filtros de búsqueda
    query = "SELECT * FROM noticias WHERE 1=1"
    params = []

    # Filtro por fecha: usa la condición guardada en la tabla filtros_fecha
    if filtro_fecha != 'todas':
        cursor.execute("SELECT condicion FROM filtros_fecha WHERE valor = %s", (filtro_fecha,))
        fila_fecha = cursor.fetchone()
        if fila_fecha and fila_fecha['condicion']:
            query += " AND " + fila_fecha['condicion']

    if filtro_fuente != 'todas':
        query += " AND fuente = %s"
        params.append(filtro_fuente)

    if filtro_categoria != 'todas':
        query += " AND categoria = %s"
        params.append(filtro_categoria)

    if busqueda:
        query += " AND (titulo LIKE %s OR descripcion LIKE %s OR fuente LIKE %s)"
        params.extend([f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%"])

    query += " ORDER BY fecha DESC, id DESC"
    cursor.execute(query, params)
    noticias = cursor.fetchall()

    # Fuentes: registradas en la tabla + las existentes en noticias (sin las eliminadas)
    cursor.execute("SELECT DISTINCT fuente FROM noticias ORDER BY fuente")
    fuentes_noticias = [r['fuente'] for r in cursor.fetchall()]
    cursor.execute("SELECT nombre FROM fuentes ORDER BY nombre")
    fuentes_registradas = [r['nombre'] for r in cursor.fetchall()]
    cursor.execute("SELECT nombre FROM fuentes_eliminadas")
    fuentes_eliminadas = [r['nombre'] for r in cursor.fetchall()]
    fuentes = list(dict.fromkeys(
        fuentes_registradas + [f for f in fuentes_noticias if f not in fuentes_eliminadas]
    ))

    # Categorías: orientaciones registradas + las existentes en noticias
    asegurar_tabla_orientaciones()
    cursor.execute("SELECT nombre FROM orientaciones ORDER BY nombre")
    areas_registradas = [r['nombre'] for r in cursor.fetchall()]
    cursor.execute("SELECT DISTINCT categoria FROM noticias ORDER BY categoria")
    categorias_noticias = [r['categoria'] for r in cursor.fetchall()]
    categorias = list(dict.fromkeys(areas_registradas + categorias_noticias))

    cursor.execute("SELECT * FROM fuentes ORDER BY nombre")
    fuentes_tabla = cursor.fetchall()

    cursor.execute("SELECT * FROM filtros_fecha ORDER BY orden, id")
    filtros_fecha = cursor.fetchall()

    return render_template('admin/noticias_lista.html',
        noticias=noticias, fuentes=fuentes, categorias=categorias,
        fuentes_tabla=fuentes_tabla, filtros_fecha=filtros_fecha,
        filtro_fecha=filtro_fecha, filtro_fuente=filtro_fuente,
        filtro_categoria=filtro_categoria, busqueda=busqueda)


@app.route('/admin/noticias/fuentes/editar/<int:id>', methods=['POST'])
@requiere_admin
def editar_fuente(id):
    nombre = request.form.get('nombre', '').strip()
    if not nombre:
        flash('El nombre de la fuente no puede estar vacío.', 'danger')
        return redirect(url_for('admin_noticias'))
    db = obtener_db()
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE fuentes SET nombre = %s WHERE id = %s", (nombre, id))
        db.commit()
        flash('Fuente actualizada.', 'success')
    except Exception:
        db.rollback()
        flash('Ese nombre ya está en uso por otra fuente.', 'warning')
    return redirect(url_for('admin_noticias'))


@app.route('/admin/noticias/fuentes/toggle/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def toggle_fuente(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("UPDATE fuentes SET activo = NOT activo WHERE id = %s", (id,))
    db.commit()
    flash('Visibilidad de la fuente actualizada.', 'success')
    return redirect(url_for('admin_noticias'))


@app.route('/admin/noticias/filtros-fecha/editar/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def editar_filtro_fecha(id):
    # El formulario de renombrar envía "etiqueta"; el toggle de visibilidad solo envía "activo".
    if 'etiqueta' in request.form:
        etiqueta = request.form.get('etiqueta', '').strip()
        if not etiqueta:
            flash('La etiqueta del filtro no puede estar vacía.', 'danger')
            return redirect(url_for('admin_noticias'))
        db = obtener_db()
        cursor = db.cursor()
        cursor.execute("UPDATE filtros_fecha SET etiqueta = %s WHERE id = %s", (etiqueta, id))
        db.commit()
        flash('Filtro de fecha actualizado.', 'success')
    else:
        activo = 1 if request.form.get('activo') else 0
        db = obtener_db()
        cursor = db.cursor()
        cursor.execute("UPDATE filtros_fecha SET activo = %s WHERE id = %s", (activo, id))
        db.commit()
        flash('Visibilidad del filtro actualizada.', 'success')
    return redirect(url_for('admin_noticias'))


@app.route('/admin/noticias/filtros-fecha/mover/<int:id>/<direccion>', methods=['POST'])
@requiere_admin
def mover_filtro_fecha(id, direccion):
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM filtros_fecha ORDER BY orden, id")
    filas = cursor.fetchall()
    idx = next((i for i, f in enumerate(filas) if f['id'] == id), None)
    if idx is None:
        return redirect(url_for('admin_noticias'))
    if direccion == 'arriba' and idx > 0:
        filas[idx], filas[idx - 1] = filas[idx - 1], filas[idx]
    elif direccion == 'abajo' and idx < len(filas) - 1:
        filas[idx], filas[idx + 1] = filas[idx + 1], filas[idx]
    else:
        flash('El filtro ya está en el límite.', 'info')
        return redirect(url_for('admin_noticias'))
    for orden, f in enumerate(filas):
        cursor.execute("UPDATE filtros_fecha SET orden = %s WHERE id = %s", (orden, f['id']))
    db.commit()
    flash('Orden de los filtros actualizado.', 'success')
    return redirect(url_for('admin_noticias'))


@app.route('/admin/noticias/filtros-fecha/nueva', methods=['POST'])
@requiere_admin
def nueva_filtro_fecha():
    etiqueta = request.form.get('etiqueta', '').strip()
    desde = request.form.get('desde', '').strip()
    hasta = request.form.get('hasta', '').strip()
    activo = 1 if request.form.get('activo') else 0

    if not etiqueta:
        flash('El nombre del filtro no puede estar vacío.', 'danger')
        return redirect(url_for('admin_noticias'))

    def fecha_valida(valor):
        try:
            datetime.strptime(valor, '%Y-%m-%d')
            return True
        except (ValueError, TypeError):
            return False

    if not desde:
        flash('Seleccioná la fecha desde la que se muestran las noticias.', 'danger')
        return redirect(url_for('admin_noticias'))
    if not fecha_valida(desde):
        flash('La fecha "desde" no es válida.', 'danger')
        return redirect(url_for('admin_noticias'))
    if hasta and not fecha_valida(hasta):
        flash('La fecha "hasta" no es válida.', 'danger')
        return redirect(url_for('admin_noticias'))

    if desde and hasta:
        condicion = f"fecha >= '{desde}' AND fecha <= '{hasta}'"
    else:
        condicion = f"fecha >= '{desde}'"

    asegurar_tabla_filtros_fecha()
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    # Generar un "valor" único (clave usada en la URL) a partir de la etiqueta
    base = re.sub(r'[^a-z0-9]+', '_',
                  etiqueta.lower()
                  .replace('á', 'a').replace('é', 'e').replace('í', 'i')
                  .replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')
                  ).strip('_')
    valor = base or 'filtro'
    sufijo = 2
    cursor.execute("SELECT COUNT(*) AS n FROM filtros_fecha WHERE valor = %s", (valor,))
    while cursor.fetchone()['n'] > 0:
        valor = f"{base}_{sufijo}"
        sufijo += 1
        cursor.execute("SELECT COUNT(*) AS n FROM filtros_fecha WHERE valor = %s", (valor,))

    cursor.execute("SELECT COALESCE(MAX(orden), 0) AS m FROM filtros_fecha")
    orden = cursor.fetchone()['m'] + 1

    cur = db.cursor()
    cur.execute(
        "INSERT INTO filtros_fecha (valor, etiqueta, condicion, activo, orden, es_fijo) VALUES (%s, %s, %s, %s, %s, 0)",
        (valor, etiqueta, condicion, activo, orden)
    )
    db.commit()
    if hasta:
        flash(f'Filtro "{etiqueta}" agregado (del {desde} al {hasta}).', 'success')
    else:
        flash(f'Filtro "{etiqueta}" agregado (desde {desde}).', 'success')
    return redirect(url_for('admin_noticias'))


@app.route('/admin/noticias/filtros-fecha/eliminar/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def eliminar_filtro_fecha(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM filtros_fecha WHERE id = %s", (id,))
    db.commit()
    flash('Filtro eliminado.', 'info')
    return redirect(url_for('admin_noticias'))


@app.route('/admin/noticias/fuentes/nueva', methods=['POST'])
@requiere_admin
def nueva_fuente():
    nombre = request.form.get('nombre', '').strip()
    if not nombre:
        flash('El nombre de la fuente no puede estar vacío.', 'danger')
        return redirect(url_for('admin_noticias'))

    asegurar_tabla_fuentes()
    db = obtener_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO fuentes (nombre) VALUES (%s)", (nombre,))
        db.commit()
        flash(f'Fuente "{nombre}" agregada.', 'success')
    except Exception:
        db.rollback()
        flash('Esa fuente ya está registrada.', 'warning')
    return redirect(url_for('admin_noticias'))


@app.route('/admin/noticias/fuentes/eliminar/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def eliminar_fuente(id):
    asegurar_tabla_fuentes()
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT nombre FROM fuentes WHERE id = %s", (id,))
    fila = cursor.fetchone()
    if not fila:
        flash('Fuente no encontrada.', 'warning')
        return redirect(url_for('admin_noticias'))
    cur = db.cursor()
    # Registra la fuente como eliminada para que no se vuelva a auto-registrar
    cur.execute("INSERT IGNORE INTO fuentes_eliminadas (nombre) VALUES (%s)", (fila['nombre'],))
    cur.execute("DELETE FROM fuentes WHERE id = %s", (id,))
    db.commit()
    flash(f'Fuente "{fila["nombre"]}" eliminada.', 'info')
    return redirect(url_for('admin_noticias'))


@app.route('/admin/noticias/nueva', methods=['POST'])
@requiere_admin
def nueva_noticia():
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    fuente = request.form['fuente']
    fecha = request.form['fecha']
    link = request.form.get('link', '#')
    categoria = request.form.get('categoria', 'General')

    # Imagen: si se sube un archivo, se usa en lugar de la URL
    imagen = request.form.get('imagen', '')
    imagen_subida = guardar_imagen_noticia(request.files.get('imagen_file'))
    if imagen_subida:
        imagen = imagen_subida

    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO noticias (titulo, descripcion, imagen, fuente, fecha, link, categoria, es_externa)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 0)
    """, (titulo, descripcion, imagen, fuente, fecha, link, categoria))
    db.commit()
    flash('Noticia agregada exitosamente.', 'success')
    return redirect(url_for('admin_noticias'))


@app.route('/admin/noticias/editar/<int:id>', methods=['POST'])
@requiere_admin
def editar_noticia(id):
    titulo = request.form.get('titulo', '')
    descripcion = request.form.get('descripcion', '')
    fuente = request.form.get('fuente', '')
    fecha = request.form.get('fecha', '')
    link = request.form.get('link', '')
    categoria = request.form.get('categoria', 'General')

    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    # Imagen: si se sube archivo nuevo se usa; si no, se usa la URL del formulario;
    # y si ambas están vacías, se conserva la imagen actual de la noticia.
    imagen_subida = guardar_imagen_noticia(request.files.get('imagen_file'))
    if imagen_subida:
        imagen = imagen_subida
    else:
        imagen_form = request.form.get('imagen', '').strip()
        if imagen_form:
            imagen = imagen_form
        else:
            cursor.execute("SELECT imagen FROM noticias WHERE id = %s", (id,))
            actual = cursor.fetchone()
            imagen = actual['imagen'] if actual else ''

    cursor.execute("""
        UPDATE noticias
        SET titulo = %s, descripcion = %s, imagen = %s, fuente = %s, fecha = %s, link = %s, categoria = %s
        WHERE id = %s
    """, (titulo, descripcion, imagen, fuente, fecha, link, categoria, id))
    db.commit()
    flash('Noticia actualizada exitosamente.', 'success')
    return redirect(url_for('admin_noticias'))


@app.route('/admin/noticias/eliminar/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
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
        print("[imagenes] Directorio de imágenes no encontrado")
        return  # carpeta no existe, nada que hacer

    print(f"[imagenes] Escaneando directorio: {imagenes_dir}")

    # Construir índice: nombre_archivo_sin_ext_lower → ruta_relativa_a_static
    index = {}
    for fname in os.listdir(imagenes_dir):
        ruta_relativa = 'imagenes/' + fname
        # Clave: nombre del archivo en minúsculas sin extensión
        clave = os.path.splitext(fname)[0].lower()
        index[clave] = ruta_relativa

    print(f"[imagenes] Índice construido con {len(index)} archivos")

    def normalizar(texto):
        return (texto
                .replace('á', 'a').replace('é', 'e').replace('í', 'i')
                .replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')
                .strip().lower())

    # Índice por nombre de carrera.
    # Formato de archivo: <área>-<nombre>-<portada|principal>.<ext>
    # Ni el área ni el nombre contienen guiones, así que el nombre es el penúltimo segmento.
    imagenes_por_carrera = {}
    for clave, ruta in index.items():
        partes = [p.strip() for p in clave.split('-')]
        if len(partes) < 3:
            continue  # archivo subido manualmente u otro formato
        nombre_segmento = normalizar(partes[-2])
        if nombre_segmento not in imagenes_por_carrera:
            imagenes_por_carrera[nombre_segmento] = {'portada': None, 'principal': None}
        if partes[-1].startswith('portada'):
            imagenes_por_carrera[nombre_segmento]['portada'] = ruta
        elif partes[-1].startswith('principal'):
            imagenes_por_carrera[nombre_segmento]['principal'] = ruta

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

        print(f"[imagenes] Carreras sin imágenes: {len(carreras_sin_imagen)}")

        if not carreras_sin_imagen:
            cursor.close()
            print("[imagenes] Todas las carreras ya tienen imágenes asignadas")
            return  # Todas las carreras ya tienen imagen → nada que hacer

        actualizadas = 0
        for carrera in carreras_sin_imagen:
            nombre_normalized = normalizar(carrera['nombre'] or '')
            area_normalized = normalizar(carrera['area_profesional'] or '')

            # Buscar portada y principal
            portada   = None
            principal = None

            # Prioridad 1: coincidencia exacta por nombre de la carrera
            coincidencia = imagenes_por_carrera.get(nombre_normalized)
            if coincidencia:
                portada = coincidencia['portada']
                principal = coincidencia['principal']

            # Prioridad 2: si no hubo coincidencia por nombre, buscar por área
            if not (portada and principal):
                for clave, ruta in index.items():
                    clave_normalized = normalizar(clave)
                    if area_normalized and area_normalized in clave_normalized:
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
                print(f"[imagenes] Carrera {carrera['id']} ({carrera['nombre']}) actualizada - Portada: {portada}, Principal: {principal}")

        conn.commit()
        cursor.close()

        if actualizadas:
            print(f'[imagenes] Auto-sync: {actualizadas} carreras actualizadas.')
        else:
            print('[imagenes] Auto-sync: sin cambios necesarios.')

    except Exception as e:
        print(f'[imagenes] Auto-sync error (no crítico): {e}')
        import traceback
        traceback.print_exc()


# Punto de entrada de la aplicación
if __name__ == '__main__':
    print("=== INICIANDO APLICACIÓN FLASK ===")
    with app.app_context():
        print("Ejecutando sincronización de imágenes...")
        sincronizar_imagenes()
        print("Sincronización completada. Iniciando servidor...")
    app.run(debug=True)