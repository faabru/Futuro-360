import mysql.connector
import os
import json
from dotenv import load_dotenv

load_dotenv()

def fix_database_encoding():
    try:
        db = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'futuro360')
        )
        cursor = db.cursor()

        # Disable FK checks to safely drop and recreate
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("DROP TABLE IF EXISTS opciones_pregunta;")
        cursor.execute("DROP TABLE IF EXISTS preguntas;")
        cursor.execute("DROP TABLE IF EXISTS carreras;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        # Recreate tables with correct schemas
        cursor.execute("""
        CREATE TABLE preguntas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            texto_pregunta VARCHAR(255) NOT NULL,
            area_profesional VARCHAR(100) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        cursor.execute("""
        CREATE TABLE opciones_pregunta ( 
           id INT AUTO_INCREMENT PRIMARY KEY, 
           pregunta_id INT NOT NULL, 
           texto_opcion VARCHAR(300) NOT NULL, 
           area_profesional VARCHAR(100) NOT NULL, 
           FOREIGN KEY (pregunta_id) REFERENCES preguntas(id) ON DELETE CASCADE 
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        cursor.execute("""
        CREATE TABLE carreras (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(150) NOT NULL,
            descripcion TEXT,
            area_profesional VARCHAR(100) NOT NULL,
            instituciones TEXT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # Re-insert questions (CLEAN UTF-8)
        questions = [
            ('¿Qué tipo de problemas te sentís más motivado/a a resolver hoy?', 'General'), 
            ('Si pudieras elegir un entorno para trabajar diariamente, ¿cuál sería?', 'General'), 
            ('¿Qué capacidad destacás más en tu personalidad?', 'General'), 
            ('¿Qué área genera mayor curiosidad intelectual en vos?', 'General'), 
            ('¿Cuál sería tu aporte ideal a la sociedad de Tucumán?', 'General'), 
            ('Ante un objeto tecnológico nuevo, ¿qué despierta tu interés?', 'General'), 
            ('¿Qué área de la salud te parece más gratificante?', 'Salud'), 
            ('¿Qué actividad disfrutás realizar de manera independiente?', 'General'), 
            ('¿Cómo preferís abordar la naturaleza?', 'Ciencias Naturales'), 
            ('¿Cuál es tu relación con los números?', 'General'), 
            ('¿Qué tipo de lectura preferís en tu tiempo libre?', 'General'), 
            ('En un equipo de trabajo, ¿qué rol solés ocupar?', 'General'), 
            ('¿Qué te motiva de una carrera profesional?', 'General'), 
            ('¿Qué importancia le das a la investigación?', 'General'), 
            ('¿Qué te gusta construir o dirigir?', 'General'), 
            ('¿Qué desafío científico te parece más urgente?', 'Ciencias'), 
            ('Si tuvieras que enseñar algo, ¿qué elegirías?', 'General'), 
            ('¿Qué área de la comunicación te interesa más?', 'Comunicación'), 
            ('¿Cómo te ves en 10 años?', 'General'), 
            ('¿Qué preferís diseñar o crear?', 'General'), 
            ('¿Qué valor considerás fundamental en tu trabajo?', 'General'), 
            ('¿Con qué herramientas te sentís más cómodo/a?', 'General'), 
            ('¿Qué tipo de leyes te interesan más?', 'General'), 
            ('¿Qué te gusta transformar en el mundo del trabajo?', 'General'), 
            ('¿Qué área del campo te atrae más?', 'Agronomía'), 
            ('¿Qué preferís analizar?', 'General'), 
            ('¿Qué tipo de asistencia preferís brindar?', 'General'), 
            ('¿Qué importancia le das a la expresión corporal?', 'General'), 
            ('¿Qué temas elegirías para un documental?', 'General'), 
            ('¿Cuál es tu principal motivo para estudiar hoy?', 'General')
        ]
        cursor.executemany("INSERT INTO preguntas (texto_pregunta, area_profesional) VALUES (%s, %s)", questions)
        db.commit()

        # Re-insert options (CLEAN UTF-8)
        options = [
            (1,'Desafíos lógicos, numéricos o estadísticos','Tecnología'), 
            (1,'Problemas de salud física o bienestar de las personas','Salud'), 
            (1,'Conflictos sociales, legales o de justicia','Derecho'), 
            (1,'Fallas técnicas en máquinas o sistemas electrónicos','Ingeniería'), 
            (1,'Necesidades de expresión artística o comunicación visual','Arte y Diseño'), 
            (1,'Retos de producción de alimentos o cuidado ambiental','Agronomía'), 
            (2,'Un laboratorio de investigación química o biológica','Ciencias Naturales'), 
            (2,'El aire libre, trabajando con la tierra, rocas o bosques','Agronomía'), 
            (2,'Una oficina gestionando procesos, finanzas o marketing','Negocios'), 
            (2,'Un centro de salud, hospital o clínica dental','Salud'), 
            (2,'Un estudio creativo, set de filmación o teatro','Arte y Diseño'), 
            (2,'Una obra en construcción o planta industrial','Ingeniería'), 
            (3,'Tu pensamiento crítico y análisis filosófico','Humanidades'), 
            (3,'Tu habilidad para cuidar y acompañar a otros en crisis','Salud'), 
            (3,'Tu destreza manual y precisión técnica','Ingeniería'), 
            (3,'Tu facilidad para comunicar ideas y persuadir','Comunicación'), 
            (3,'Tu rapidez para entender lenguajes lógicos y de programación','Tecnología'), 
            (4,'El origen del universo y las leyes de la energía','Ciencias Naturales'), 
            (4,'La historia de las civilizaciones y sus transformaciones','Humanidades'), 
            (4,'El comportamiento de la mente humana y las emociones','Salud Mental'), 
            (4,'La composición química de los materiales y medicamentos','Ciencias Naturales'), 
            (4,'El funcionamiento de la economía y los mercados','Negocios'), 
            (5,'Diseñar infraestructuras seguras (puentes, caminos)','Ingeniería'), 
            (5,'Mejorar la productividad agrícola de forma sustentable','Agronomía'), 
            (5,'Garantizar el cumplimiento de las leyes y derechos','Derecho'), 
            (5,'Crear software y soluciones digitales innovadoras','Tecnología'), 
            (5,'Educar en el campo de las artes y la cultura','Arte y Diseño'), 
            (6,'Cómo están diseñados sus circuitos electrónicos internos','Ingeniería'), 
            (6,'El mecanismo físico y motor que lo hace moverse','Ingeniería'), 
            (6,'Cómo se puede vender y posicionar en el mercado','Negocios'), 
            (6,'El impacto ambiental que genera su producción','Agronomía'), 
            (7,'Diagnóstico médico y tratamiento de enfermedades','Salud'), 
            (7,'Rehabilitación física y recuperación del movimiento','Salud'), 
            (7,'Cuidado directo y acompañamiento del paciente','Salud'), 
            (7,'Prevención a través de la nutrición saludable','Salud'), 
            (7,'Salud y estética bucodental','Salud'), 
            (8,'Analizar datos y crear hojas de cálculo precisas','Negocios'), 
            (8,'Escribir ensayos, reflexiones o crónicas sociales','Humanidades'), 
            (8,'Dibujar, diseñar logotipos o editar videos','Arte y Diseño'), 
            (8,'Realizar experimentos o pequeñas investigaciones','Ciencias Naturales'), 
            (9,'Estudiando la vida de los microorganismos y la genética','Ciencias Naturales'), 
            (9,'Analizando la estructura de la tierra, volcanes y sismos','Ciencias Naturales'), 
            (9,'Gestionando la salud y producción de animales','Agronomía'), 
            (9,'Conservando los recursos forestales y el clima','Agronomía'), 
            (10,'Me apasiona la teoría matemática pura y abstracta','Tecnología'), 
            (10,'Los uso para el cálculo financiero, impuestos y costos','Negocios'), 
            (10,'Los aplico para el análisis de estructuras y fuerzas físicas','Ingeniería'), 
            (10,'Los utilizo para analizar estadísticas sociales o demográficas','Humanidades'), 
            (11,'Noticias sobre tecnología, IA y sistemas','Tecnología'), 
            (11,'Libros de historia, biografía o política','Humanidades'), 
            (11,'Revistas sobre salud, bienestar y medicina','Salud'), 
            (11,'Manuales técnicos de mecánica o electrónica','Ingeniería'), 
            (12,'El que organiza los recursos y optimiza los procesos','Negocios'), 
            (12,'El que propone la visión creativa y estética','Arte y Diseño'), 
            (12,'El que analiza las normas y media en los conflictos','Derecho'), 
            (12,'El que se enfoca en los detalles técnicos y operativos','Ingeniería'), 
            (13,'La posibilidad de innovar tecnológicamente','Tecnología'), 
            (13,'El servicio directo a la comunidad y la ayuda humanitaria','Salud'), 
            (13,'La estabilidad que brinda la gestión empresarial y contable','Negocios'), 
            (13,'La libertad de creación artística y cultural','Arte y Diseño'), 
            (14,'Mucha, me gusta descubrir nuevas curas o vacunas','Ciencias Naturales'), 
            (14,'Bastante, me interesa entender el pasado de mi región','Humanidades'), 
            (14,'Me interesa la investigación aplicada a la industria','Ingeniería'), 
            (14,'Prefiero la investigación sobre el comportamiento humano','Salud Mental'), 
            (15,'Una gran empresa o un emprendimiento propio','Negocios'), 
            (15,'Una obra de teatro, una película o una banda musical','Arte y Diseño'), 
            (15,'Una campaña de concientización ambiental','Agronomía'), 
            (15,'Un sistema de redes informáticas seguro','Tecnología'), 
            (16,'El cambio climático y la gestión del agua','Agronomía'), 
            (16,'La creación de energías limpias y eficientes','Ingeniería'), 
            (16,'El tratamiento de enfermedades mentales en la sociedad','Salud Mental'), 
            (16,'La digitalización y automatización de la vida cotidiana','Tecnología'), 
            (17,'Ciencias exactas (Física, Química, Matemática)','Ciencias Naturales'), 
            (17,'Artes visuales o música','Arte y Diseño'), 
            (17,'Filosofía, Historia o Ética','Humanidades'), 
            (17,'Educación para la salud y prevención','Salud'), 
            (18,'El periodismo y los medios masivos','Comunicación'), 
            (18,'El marketing digital y la publicidad','Negocios'), 
            (18,'La comunicación institucional en empresas','Comunicación'), 
            (18,'La divulgación científica o cultural','Humanidades'), 
            (19,'Supervisando procesos en una fábrica o industria','Ingeniería'), 
            (19,'Atendiendo pacientes en un consultorio o centro médico','Salud'), 
            (19,'Litigando en tribunales o asesorando legalmente','Derecho'), 
            (19,'Investigando y publicando hallazgos académicos','Ciencias Naturales'), 
            (20,'Un edificio moderno y funcional','Ingeniería'), 
            (20,'Un sistema de riego eficiente para el campo','Agronomía'), 
            (20,'Una estrategia de ventas internacional','Negocios'), 
            (20,'Una plataforma interactiva o aplicación móvil','Tecnología'), 
            (21,'La precisión y el rigor lógico','Tecnología'), 
            (21,'La justicia y la equidad','Derecho'), 
            (21,'La empatía y la compasión','Salud'), 
            (21,'La eficiencia y la productividad','Negocios'), 
            (22,'Computadoras y software especializado','Tecnología'), 
            (22,'Instrumental quirúrgico o de diagnóstico','Salud'), 
            (22,'Herramientas de corte, soldadura y maquinaria','Ingeniería'), 
            (22,'Instrumentos musicales, pinceles o cámaras','Arte y Diseño'), 
            (23,'Las leyes que regulan el comportamiento social y civil','Derecho'), 
            (23,'Las leyes de la física que gobiernan el movimiento','Ingeniería'), 
            (23,'Las normas contables y leyes del mercado','Negocios'), 
            (23,'Las normas ambientales y de protección de recursos','Agronomía'), 
            (24,'Hacer las industrias más seguras y eficientes','Ingeniería'), 
            (24,'Incorporar más arte y creatividad en la vida diaria','Arte y Diseño'), 
            (24,'Mejorar la salud mental de los trabajadores','Salud Mental'), 
            (24,'Facilitar el acceso a la tecnología para todos','Tecnología'), 
            (25,'El manejo de cultivos extensivos','Agronomía'), 
            (25,'El cuidado y sanidad de los animales','Agronomía'), 
            (25,'El estudio de los suelos y las rocas','Ciencias Naturales'), 
            (25,'El manejo de bosques y parques naturales','Agronomía'), 
            (26,'Un saldo contable y la rentabilidad de una empresa','Negocios'), 
            (26,'Una obra de arte o una pieza teatral','Arte y Diseño'), 
            (26,'Un mapa meteorológico o astronómico','Ciencias Naturales'), 
            (26,'La estructura de una molécula o ADN','Ciencias Naturales'), 
            (27,'Asistencia técnica en reparaciones complejas','Ingeniería'), 
            (27,'Asistencia social en comunidades vulnerables','Humanidades'), 
            (27,'Asistencia nutricional y planes de salud','Salud'), 
            (27,'Asesoramiento financiero y económico','Negocios'), 
            (28,'Mucha, me interesa la danza y el teatro','Arte y Diseño'), 
            (28,'Intermedia, la veo clave para kinesiología y rehabilitación','Salud'), 
            (28,'Poca, prefiero el trabajo intelectual o administrativo','Negocios'), 
            (29,'La vida secreta de los volcanes y terremotos','Ciencias Naturales'), 
            (29,'El impacto de la inteligencia artificial en el empleo','Tecnología'), 
            (29,'La historia olvidada de los pueblos de Tucumán','Humanidades'), 
            (29,'Avances en la medicina para alargar la vida','Salud'), 
            (30,'Cumplir un sueño de vocación postergado','Humanidades'), 
            (30,'Adquirir habilidades técnicas para una salida laboral rápida','Ingeniería'), 
            (30,'Profundizar en el conocimiento científico y académico','Ciencias Naturales'), 
            (30,'Desarrollar mi potencial creativo y expresivo','Arte y Diseño')
        ]
        cursor.executemany("INSERT INTO opciones_pregunta (pregunta_id, texto_opcion, area_profesional) VALUES (%s, %s, %s)", options)
        db.commit()

        # Re-insert careers (CLEAN UTF-8)
        careers = [
            ('Ingeniería en Sistemas de Información','Tecnología','Diseño y desarrollo de software, bases de datos, redes y sistemas informáticos.','UTN - FR Tucumán, UNT - FACET'), 
            ('Licenciatura en Sistemas de Información','Tecnología','Análisis, diseño e implementación de sistemas de información empresariales.','UNT - FACET, UNSTA'), 
            ('Tecnicatura en Programación','Tecnología','Desarrollo de aplicaciones web, móviles y de escritorio. Salida laboral rápida.','UTN - FR Tucumán, Institutos Superiores de Tucumán'), 
            ('Ingeniería Civil','Ingeniería','Diseño y construcción de infraestructuras: edificios, puentes, caminos y obras hidráulicas.','UNT - FACET, UTN - FR Tucumán'), 
            ('Ingeniería Mecánica','Ingeniería','Diseño, análisis y mantenimiento de sistemas mecánicos y procesos industriales.','UNT - FACET, UTN - FR Tucumán'), 
            ('Ingeniería Eléctrica','Ingeniería','Generación, transmisión y distribución de energía eléctrica. Automatización industrial.','UNT - FACET, UTN - FR Tucumán'), 
            ('Ingeniería Industrial','Ingeniería','Optimización de procesos productivos, gestión de calidad y logística industrial.','UTN - FR Tucumán, UNT - FACET'), 
            ('Ingeniería Química','Ingeniería','Transformación de materias primas en productos industriales mediante procesos químicos.','UNT - FACET'), 
            ('Medicina','Salud','Diagnóstico, tratamiento y prevención de enfermedades.','UNT - Facultad de Medicina'), 
            ('Enfermería','Salud','Cuidado integral del paciente en hospitales, clínicas y atención domiciliaria.','UNT - Facultad de Medicina, Instituto Superior de Enfermería'), 
            ('Odontología','Salud','Diagnóstico y tratamiento de enfermedades bucodentales.','UNT - Facultad de Odontología'), 
            ('Kinesiología y Fisioterapia','Salud','Rehabilitación física y recuperación del movimiento.','UNT - Facultad de Medicina'), 
            ('Nutrición','Salud','Planificación de dietas y planes alimentarios para individuos y comunidades.','UNT - Facultad de Medicina, UNSTA'), 
            ('Bioquímica','Salud','Análisis clínicos, investigación farmacéutica y control de calidad alimentaria.','UNT - FBQyF'), 
            ('Farmacia','Salud','Dispensación de medicamentos, control de calidad y farmacología clínica.','UNT - FBQyF'), 
            ('Psicología','Salud Mental','Estudio del comportamiento humano, terapia individual y grupal.','UNT - Facultad de Psicología, UNSTA'), 
            ('Trabajo Social','Salud Mental','Intervención en problemáticas sociales y acompañamiento a comunidades vulnerables.','UNT - Facultad de Filosofía y Letras'), 
            ('Psicopedagogía','Salud Mental','Diagnóstico y tratamiento de dificultades de aprendizaje.','UNSTA, Institutos Superiores de Tucumán'), 
            ('Biología','Ciencias Naturales','Estudio de los seres vivos, genética, ecología y biotecnología.','UNT - Facultad de Ciencias Naturales'), 
            ('Geología','Ciencias Naturales','Estudio de la estructura y composición de la Tierra. Minería y recursos naturales.','UNT - Facultad de Ciencias Naturales'), 
            ('Química','Ciencias Naturales','Investigación y aplicación de la composición y transformación de la materia.','UNT - FBQyF'), 
            ('Ingeniería Agronómica','Agronomía','Producción vegetal, manejo de suelos y gestión de empresas agropecuarias.','UNT - FAZ'), 
            ('Medicina Veterinaria','Agronomía','Salud y producción animal, sanidad de mascotas y animales de granja.','UNT - FAZ'), 
            ('Ingeniería Forestal','Agronomía','Manejo y conservación de bosques, recursos madereros y gestión ambiental.','UNT - FAZ'), 
            ('Tecnicatura en Producción Agropecuaria','Agronomía','Formación técnica en producción animal y vegetal con salida laboral rápida.','INTA Tucumán, Institutos Superiores Rurales'), 
            ('Contador Público Nacional','Negocios','Auditoría, impuestos, contabilidad y asesoramiento financiero empresarial.','UNT - FCE, UNSTA'), 
            ('Licenciatura en Administración','Negocios','Gestión de empresas, recursos humanos, marketing y estrategia organizacional.','UNT - FCE, UNSTA, UTN'), 
            ('Licenciatura en Economía','Negocios','Análisis de mercados, política económica y desarrollo regional.','UNT - FCE'), 
            ('Marketing Digital','Negocios','Estrategias de comunicación digital, publicidad online y posicionamiento de marcas.','UNSTA, Institutos Superiores de Tucumán'), 
            ('Abogacía','Derecho','Representación legal, litigios y asesoramiento jurídico en todas las ramas del derecho.','UNT - Facultad de Derecho, UNSTA'), 
            ('Notariado','Derecho','Escrituras, contratos y documentos legales con fe pública.','UNT - Facultad de Derecho'), 
            ('Ciencias Políticas','Derecho','Análisis del poder, instituciones del Estado y gestión pública.','UNT - Facultad de Derecho'), 
            ('Licenciatura en Historia','Humanidades','Investigación y enseñanza del pasado humano. Archivos, museos y docencia.','UNT - Facultad de Filosofía y Letras'), 
            ('Licenciatura en Filosofía','Humanidades','Pensamiento crítico, ética, lógica y epistemología.','UNT - Facultad de Filosofía y Letras'), 
            ('Licenciatura en Letras','Humanidades','Literatura, lingüística, escritura creativa y docencia de lengua.','UNT - Facultad de Filosofía y Letras'), 
            ('Diseño Gráfico','Arte y Diseño','Creación visual de marcas, publicidad, packaging e interfaces digitales.','UNT - Facultad de Artes, UNSTA, Institutos Superiores'), 
            ('Licenciatura en Artes Visuales','Arte y Diseño','Pintura, escultura, instalación y gestión cultural.','UNT - Facultad de Artes'), 
            ('Música','Arte y Diseño','Interpretación, composición y dirección musical.','UNT - Facultad de Artes'), 
            ('Arquitectura','Arte y Diseño','Diseño y planificación de edificios y espacios. Combina arte, técnica y funcionalidad.','UNT - FAU'), 
            ('Licenciatura en Comunicación Social','Comunicación','Periodismo, relaciones públicas, comunicación institucional y medios digitales.','UNT - Facultad de Filosofía y Letras'), 
            ('Periodismo','Comunicación','Reportaje, redacción, conducción y producción periodística en todos los medios.','Institutos Superiores de Tucumán, UNT'), 
            ('Publicidad','Comunicación','Creación de campañas publicitarias, estrategia de marca y comunicación persuasiva.','UNSTA, Institutos Superiores')
        ]
        cursor.executemany("INSERT INTO carreras (nombre, area_profesional, descripcion, instituciones) VALUES (%s, %s, %s, %s)", careers)
        db.commit()

        print("Database cleaned and updated successfully!")
        cursor.close()
        db.close()
    except Exception as e:
        print(f"Error fixing database: {e}")

if __name__ == "__main__":
    fix_database_encoding()
