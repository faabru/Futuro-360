-- Futuro 360 - dump completo de contenido
-- Generado con scripts/exportar_base.py (no editar a mano).
-- Importar UNA VEZ desde MySQL Workbench (Open SQL Script).

CREATE DATABASE IF NOT EXISTS `futuro360` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `futuro360`;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) DEFAULT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `rol` enum('usuario','admin') DEFAULT 'usuario',
  `activo` tinyint(1) DEFAULT 1,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `es_dueño` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `email`, `password`, `rol`, `activo`, `created_at`, `updated_at`, `es_dueño`) VALUES (1, 'fabricio villagra', NULL, 'fabriciovillagra05@gmail.com', 'scrypt:32768:8:1$fbKF0AGu5nKUiKlM$6c31fae9b2dad27e986b4bb2a9e084be74caefbf5b17959af0afc4c098b26938d8cffc07326ce077ffc508cb8b57f4bba559475c32f8f8a9b49169cdd3963306', 'admin', 1, '2026-05-06 23:35:10', '2026-08-06 06:16:39', 1);
INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `email`, `password`, `rol`, `activo`, `created_at`, `updated_at`, `es_dueño`) VALUES (2, 'perez', '', 'juancarlos@gmail.com', 'scrypt:32768:8:1$2rfLoMFMCIwLSMXq$e6417033e14addf80d85f05dcb982ffc8972d5df36afe1d2674a07d70e2b5a991e986cf1ba56fe6687e326afa4add32d0dc4999b8ab89ba1ef50284c921bd749', 'usuario', 1, '2026-04-14 14:47:42', '2026-08-06 06:16:39', 0);
INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `email`, `password`, `rol`, `activo`, `created_at`, `updated_at`, `es_dueño`) VALUES (3, 'fabri', '', 'fafa@gmail.com', 'scrypt:32768:8:1$lvHVrAduO65FleD5$5b2419357c41702057ca59a1334842c8d166e8a20a7eb97ec4cb68f70778d2f120583a84221ebe518f6acb0e98c3438bb9efecb910a8594e8d8cb2818793a3b6', 'usuario', 1, '2026-04-14 15:23:09', '2026-04-14 15:23:09', 0);
INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `email`, `password`, `rol`, `activo`, `created_at`, `updated_at`, `es_dueño`) VALUES (4, 'fabri', '', 'fafa@gmil.com', 'scrypt:32768:8:1$bBKYRLPbNz4cBII6$fd531a83e1d5cda5b9b9a2b2ef0174d5e2054a7216ea8a75090e08754b0b760fcde500b72b37757a560b92aaadefbea14d0b3375b1c3d985fced95a9133d91a0', 'usuario', 1, '2026-04-14 16:03:53', '2026-04-14 16:03:53', 0);
INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `email`, `password`, `rol`, `activo`, `created_at`, `updated_at`, `es_dueño`) VALUES (5, 'carlos', '', 'manzano05@gamil.com', 'scrypt:32768:8:1$8YiBgRBK72QV3viO$b5db1e57c5b4392ba2c3f004d57b01a953f9cdad3ee4c24ca2a5b06b5537e59b8b3d927a04c6e81f4a887d1332c33e8a338226730f0af9788a3a42132621ecbc', 'usuario', 1, '2026-04-14 16:07:29', '2026-04-14 16:07:29', 0);
INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `email`, `password`, `rol`, `activo`, `created_at`, `updated_at`, `es_dueño`) VALUES (6, 'peru', '', 'peru@gmail.com', 'scrypt:32768:8:1$9SDSm0Oketq7Uxkj$062d49c58b745cd42eb8af62d8ed506ba2c57b10c97e6073496f7b2a2eda0d0a4ce2245696e406f0006d35acfa4ed05f190b0ade43551279656af7de491addd9', 'usuario', 1, '2026-04-14 16:13:34', '2026-04-14 16:13:34', 0);
INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `email`, `password`, `rol`, `activo`, `created_at`, `updated_at`, `es_dueño`) VALUES (8, 'Test User', NULL, 'test@example.com', 'scrypt:32768:8:1$ZO485zszm2D5HR5e$b58565e52e4e2868d756250f88bfd8eca4eb004c47dc295c5e146f8f99c25e4f6e9088abb4c1cc47e18c85c3649222848b725259e55a524dd1f201431c062ec5', 'usuario', 1, '2026-05-09 03:46:38', '2026-08-06 18:58:22', 0);
INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `email`, `password`, `rol`, `activo`, `created_at`, `updated_at`, `es_dueño`) VALUES (9, 'fabricio cortes', NULL, 'elcolofabri2020@gmail.com', 'scrypt:32768:8:1$Z6qnKeNr7kTbIX9s$e63b9406c3b7ec2cc14250b18e9e0f138d97b529d5594bad543402b5f4af6c0a90075ddace0fa01b93150108903f257f7c3fd57a1edd0eb036b72a121c095564', 'usuario', 1, '2026-06-04 19:37:27', '2026-06-04 19:37:27', 0);
INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `email`, `password`, `rol`, `activo`, `created_at`, `updated_at`, `es_dueño`) VALUES (15, 'peter', 'parker', 'spiderman@gmail.com', 'scrypt:32768:8:1$tmAPCJhKObASFLYh$24b93358e3c65a9d33b691d8f94adcabac3582ba8c31313234f790dbfd9cea63ac9384e2db24c4d6ad7ba4f9a27f8039447ca039e4c8e806a93fb11c5c906b35', 'admin', 1, '2026-08-06 18:59:40', '2026-08-11 01:54:42', 0);

DROP TABLE IF EXISTS `carreras`;
CREATE TABLE `carreras` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `area_profesional` varchar(100) NOT NULL,
  `instituciones` text DEFAULT NULL,
  `popular` tinyint(1) DEFAULT 0,
  `imagen` varchar(500) DEFAULT '',
  `imagen_portada` varchar(500) DEFAULT NULL,
  `imagen_principal` varchar(500) DEFAULT NULL,
  `a_que_se_dedica` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (1, 'Ingeniería en Sistemas de Información', 'Diseño y desarrollo de software, bases de datos, redes y sistemas informáticos.', 'Tecnología', 'UTN - FR Tucumán, UNT - FACET', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (2, 'Licenciatura en Sistemas de Información', 'Análisis, diseño e implementación de sistemas de información empresariales.', 'Tecnología', 'UNT - FACET, UNSTA', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (3, 'Tecnicatura en Programación', 'Desarrollo de aplicaciones web, móviles y de escritorio. Salida laboral rápida.', 'Tecnología', 'UTN - FR Tucumán, Institutos Superiores de Tucumán', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (4, 'Ingeniería Civil', 'Diseño y construcción de infraestructuras: edificios, puentes, caminos y obras hidráulicas.', 'Ingeniería', 'UNT - FACET, UTN - FR Tucumán', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (5, 'Ingeniería Mecánica', 'Diseño, análisis y mantenimiento de sistemas mecánicos y procesos industriales.', 'Ingeniería', 'UNT - FACET, UTN - FR Tucumán', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (6, 'Ingeniería Eléctrica', 'Generación, transmisión y distribución de energía eléctrica. Automatización industrial.', 'Ingeniería', 'UNT - FACET, UTN - FR Tucumán', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (7, 'Ingeniería Industrial', 'Optimización de procesos productivos, gestión de calidad y logística industrial.', 'Ingeniería', 'UTN - FR Tucumán, UNT - FACET', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (8, 'Ingeniería Química', 'Transformación de materias primas en productos industriales mediante procesos químicos.', 'Ingeniería', 'UNT - FACET', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (9, 'Medicina', 'Diagnóstico, tratamiento y prevención de enfermedades.', 'Salud', 'UNT - Facultad de Medicina', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (10, 'Enfermería', 'Cuidado integral del paciente en hospitales, clínicas y atención domiciliaria.', 'Salud', 'UNT - Facultad de Medicina, Instituto Superior de Enfermería', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (11, 'Odontología', 'Diagnóstico y tratamiento de enfermedades bucodentales.', 'Salud', 'UNT - Facultad de Odontología', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (12, 'Kinesiología y Fisioterapia', 'Rehabilitación física y recuperación del movimiento.', 'Salud', 'UNT - Facultad de Medicina', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (13, 'Nutrición', 'Planificación de dietas y planes alimentarios para individuos y comunidades.', 'Salud', 'UNT - Facultad de Medicina, UNSTA', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (14, 'Bioquímica', 'Análisis clínicos, investigación farmacéutica y control de calidad alimentaria.', 'Salud', 'UNT - FBQyF', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (15, 'Farmacia', 'Dispensación de medicamentos, control de calidad y farmacología clínica.', 'Salud', 'UNT - FBQyF', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (16, 'Psicología', 'Estudio del comportamiento humano, terapia individual y grupal.', 'Salud Mental', 'UNT - Facultad de Psicología, UNSTA', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (17, 'Trabajo Social', 'Intervención en problemáticas sociales y acompañamiento a comunidades vulnerables.', 'Salud Mental', 'UNT - Facultad de Filosofía y Letras', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (18, 'Psicopedagogía', 'Diagnóstico y tratamiento de dificultades de aprendizaje.', 'Salud Mental', 'UNSTA, Institutos Superiores de Tucumán', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (19, 'Biología', 'Estudio de los seres vivos, genética, ecología y biotecnología.', 'Ciencias Naturales', 'UNT - Facultad de Ciencias Naturales', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (20, 'Geología', 'Estudio de la estructura y composición de la Tierra. Minería y recursos naturales.', 'Ciencias Naturales', 'UNT - Facultad de Ciencias Naturales', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (21, 'Química', 'Investigación y aplicación de la composición y transformación de la materia.', 'Ciencias Naturales', 'UNT - FBQyF', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (22, 'Ingeniería Agronómica', 'Producción vegetal, manejo de suelos y gestión de empresas agropecuarias.', 'Agronomía', 'UNT - FAZ', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (23, 'Medicina Veterinaria', 'Salud y producción animal, sanidad de mascotas y animales de granja.', 'Agronomía', 'UNT - FAZ', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (24, 'Ingeniería Forestal', 'Manejo y conservación de bosques, recursos madereros y gestión ambiental.', 'Agronomía', 'UNT - FAZ', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (25, 'Tecnicatura en Producción Agropecuaria', 'Formación técnica en producción animal y vegetal con salida laboral rápida.', 'Agronomía', 'INTA Tucumán, Institutos Superiores Rurales', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (26, 'Contador Público Nacional', 'Auditoría, impuestos, contabilidad y asesoramiento financiero empresarial.', 'Negocios', 'UNT - FCE, UNSTA', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (27, 'Licenciatura en Administración', 'Gestión de empresas, recursos humanos, marketing y estrategia organizacional.', 'Negocios', 'UNT - FCE, UNSTA, UTN', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (28, 'Licenciatura en Economía', 'Análisis de mercados, política económica y desarrollo regional.', 'Negocios', 'UNT - FCE', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (29, 'Marketing Digital', 'Estrategias de comunicación digital, publicidad online y posicionamiento de marcas.', 'Negocios', 'UNSTA, Institutos Superiores de Tucumán', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (30, 'Abogacía', 'Representación legal, litigios y asesoramiento jurídico en todas las ramas del derecho.', 'Derecho', 'UNT - Facultad de Derecho, UNSTA', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (31, 'Notariado', 'Escrituras, contratos y documentos legales con fe pública.', 'Derecho', 'UNT - Facultad de Derecho', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (32, 'Ciencias Políticas', 'Análisis del poder, instituciones del Estado y gestión pública.', 'Derecho', 'UNT - Facultad de Derecho', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (33, 'Licenciatura en Historia', 'Investigación y enseñanza del pasado humano. Archivos, museos y docencia.', 'Humanidades', 'UNT - Facultad de Filosofía y Letras', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (34, 'Licenciatura en Filosofía', 'Pensamiento crítico, ética, lógica y epistemología.', 'Humanidades', 'UNT - Facultad de Filosofía y Letras', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (35, 'Licenciatura en Letras', 'Literatura, lingüística, escritura creativa y docencia de lengua.', 'Humanidades', 'UNT - Facultad de Filosofía y Letras', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (36, 'Diseño Gráfico', 'Creación visual de marcas, publicidad, packaging e interfaces digitales.', 'Arte y Diseño', 'UNT - Facultad de Artes, UNSTA, Institutos Superiores', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (37, 'Licenciatura en Artes Visuales', 'Pintura, escultura, instalación y gestión cultural.', 'Arte y Diseño', 'UNT - Facultad de Artes', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (38, 'Música', 'Interpretación, composición y dirección musical.', 'Arte y Diseño', 'UNT - Facultad de Artes', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (39, 'Arquitectura', 'Diseño y planificación de edificios y espacios. Combina arte, técnica y funcionalidad.', 'Arte y Diseño', 'UNT - FAU', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (40, 'Licenciatura en Comunicación Social', 'Periodismo, relaciones públicas, comunicación institucional y medios digitales.', 'Comunicación', 'UNT - Facultad de Filosofía y Letras', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (41, 'Periodismo', 'Reportaje, redacción, conducción y producción periodística en todos los medios.', 'Comunicación', 'Institutos Superiores de Tucumán, UNT', 0, '', NULL, NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`) VALUES (42, 'Publicidad', 'Creación de campañas publicitarias, estrategia de marca y comunicación persuasiva.', 'Comunicación', 'UNSTA, Institutos Superiores', 0, '', NULL, NULL, NULL);

DROP TABLE IF EXISTS `areas`;
CREATE TABLE `areas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `icono` varchar(50) DEFAULT NULL,
  `color` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `areas` (`id`, `nombre`, `descripcion`, `icono`, `color`) VALUES (1, 'Ciencias Exactas', 'Matem??tica, F??sica, Ingenier??a, Inform??tica', '????', '#4F8EF7');
INSERT INTO `areas` (`id`, `nombre`, `descripcion`, `icono`, `color`) VALUES (2, 'Ciencias de la Salud', 'Medicina, Enfermer??a, Bioqu??mica, Farmacia', '??????', '#2DC87A');
INSERT INTO `areas` (`id`, `nombre`, `descripcion`, `icono`, `color`) VALUES (3, 'Ciencias Sociales', 'Derecho, Psicolog??a, Sociolog??a, Trabajo Social', '????', '#F7A94F');
INSERT INTO `areas` (`id`, `nombre`, `descripcion`, `icono`, `color`) VALUES (4, 'Arte y Dise??o', 'Arquitectura, Bellas Artes, Dise??o, M??sica', '????', '#E05CDB');
INSERT INTO `areas` (`id`, `nombre`, `descripcion`, `icono`, `color`) VALUES (5, 'Humanidades', 'Historia, Filosof??a, Letras, Comunicaci??n', '????', '#F7574F');
INSERT INTO `areas` (`id`, `nombre`, `descripcion`, `icono`, `color`) VALUES (6, 'Ciencias Naturales', 'Biolog??a, Geolog??a, Ecolog??a, Veterinaria', '????', '#4FC9F7');
INSERT INTO `areas` (`id`, `nombre`, `descripcion`, `icono`, `color`) VALUES (7, 'Econom??a y Negocios', 'Administraci??n, Econom??a, Comercio, Marketing', '????', '#F7D94F');

DROP TABLE IF EXISTS `preguntas`;
CREATE TABLE `preguntas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `texto_pregunta` varchar(255) NOT NULL,
  `area_profesional` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (1, '¿Qué tipo de problemas te sentís más motivado/a a resolver hoy?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (2, 'Si pudieras elegir un entorno para trabajar diariamente, ¿cuál sería?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (3, '¿Qué capacidad destacás más en tu personalidad?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (4, '¿Qué área genera mayor curiosidad intelectual en vos?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (5, '¿Cuál sería tu aporte ideal a la sociedad de Tucumán?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (6, 'Ante un objeto tecnológico nuevo, ¿qué despierta tu interés?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (7, '¿Qué área de la salud te parece más gratificante?', 'Salud');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (8, '¿Qué actividad disfrutás realizar de manera independiente?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (9, '¿Cómo preferís abordar la naturaleza?', 'Ciencias Naturales');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (10, '¿Cuál es tu relación con los números?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (11, '¿Qué tipo de lectura preferís en tu tiempo libre?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (12, 'En un equipo de trabajo, ¿qué rol solés ocupar?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (13, '¿Qué te motiva de una carrera profesional?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (14, '¿Qué importancia le das a la investigación?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (15, '¿Qué te gusta construir o dirigir?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (16, '¿Qué desafío científico te parece más urgente?', 'Ciencias');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (17, 'Si tuvieras que enseñar algo, ¿qué elegirías?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (18, '¿Qué área de la comunicación te interesa más?', 'Comunicación');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (19, '¿Cómo te ves en 10 años?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (20, '¿Qué preferís diseñar o crear?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (21, '¿Qué valor considerás fundamental en tu trabajo?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (22, '¿Con qué herramientas te sentís más cómodo/a?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (23, '¿Qué tipo de leyes te interesan más?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (24, '¿Qué te gusta transformar en el mundo del trabajo?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (25, '¿Qué área del campo te atrae más?', 'Agronomía');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (26, '¿Qué preferís analizar?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (27, '¿Qué tipo de asistencia preferís brindar?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (28, '¿Qué importancia le das a la expresión corporal?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (29, '¿Qué temas elegirías para un documental?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (30, '¿Cuál es tu principal motivo para estudiar hoy?', 'General');

DROP TABLE IF EXISTS `opciones_pregunta`;
CREATE TABLE `opciones_pregunta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pregunta_id` int(11) NOT NULL,
  `texto_opcion` varchar(300) NOT NULL,
  `area_profesional` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pregunta_id` (`pregunta_id`),
  CONSTRAINT `opciones_pregunta_ibfk_1` FOREIGN KEY (`pregunta_id`) REFERENCES `preguntas` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7628 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7501, 1, 'Desafíos lógicos, numéricos o estadísticos', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7502, 1, 'Problemas de salud física o bienestar de las personas', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7503, 1, 'Conflictos sociales, legales o de justicia', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7504, 1, 'Fallas técnicas en máquinas o sistemas electrónicos', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7505, 1, 'Necesidades de expresión artística o comunicación visual', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7506, 1, 'Retos de producción de alimentos o cuidado ambiental', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7507, 2, 'Un laboratorio de investigación química o biológica', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7508, 2, 'El aire libre, trabajando con la tierra, rocas o bosques', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7509, 2, 'Una oficina gestionando procesos, finanzas o marketing', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7510, 2, 'Un centro de salud, hospital o clínica dental', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7511, 2, 'Un estudio creativo, set de filmación o teatro', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7512, 2, 'Una obra en construcción o planta industrial', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7513, 3, 'Tu pensamiento crítico y análisis filosófico', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7514, 3, 'Tu habilidad para cuidar y acompañar a otros en crisis', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7515, 3, 'Tu destreza manual y precisión técnica', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7516, 3, 'Tu facilidad para comunicar ideas y persuadir', 'Comunicación');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7517, 3, 'Tu rapidez para entender lenguajes lógicos y de programación', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7518, 4, 'El origen del universo y las leyes de la energía', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7519, 4, 'La historia de las civilizaciones y sus transformaciones', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7520, 4, 'El comportamiento de la mente humana y las emociones', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7521, 4, 'La composición química de los materiales y medicamentos', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7522, 4, 'El funcionamiento de la economía y los mercados', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7523, 5, 'Diseñar infraestructuras seguras (puentes, caminos)', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7524, 5, 'Mejorar la productividad agrícola de forma sustentable', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7525, 5, 'Garantizar el cumplimiento de las leyes y derechos', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7526, 5, 'Crear software y soluciones digitales innovadoras', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7527, 5, 'Educar en el campo de las artes y la cultura', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7528, 6, 'Cómo están diseñados sus circuitos electrónicos internos', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7529, 6, 'El mecanismo físico y motor que lo hace moverse', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7530, 6, 'Cómo se puede vender y posicionar en el mercado', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7531, 6, 'El impacto ambiental que genera su producción', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7532, 7, 'Diagnóstico médico y tratamiento de enfermedades', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7533, 7, 'Rehabilitación física y recuperación del movimiento', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7534, 7, 'Cuidado directo y acompañamiento del paciente', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7535, 7, 'Prevención a través de la nutrición saludable', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7536, 7, 'Salud y estética bucodental', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7537, 8, 'Analizar datos y crear hojas de cálculo precisas', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7538, 8, 'Escribir ensayos, reflexiones o crónicas sociales', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7539, 8, 'Dibujar, diseñar logotipos o editar videos', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7540, 8, 'Realizar experimentos o pequeñas investigaciones', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7541, 9, 'Estudiando la vida de los microorganismos y la genética', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7542, 9, 'Analizando la estructura de la tierra, volcanes y sismos', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7543, 9, 'Gestionando la salud y producción de animales', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7544, 9, 'Conservando los recursos forestales y el clima', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7545, 10, 'Me apasiona la teoría matemática pura y abstracta', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7546, 10, 'Los uso para el cálculo financiero, impuestos y costos', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7547, 10, 'Los aplico para el análisis de estructuras y fuerzas físicas', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7548, 10, 'Los utilizo para analizar estadísticas sociales o demográficas', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7549, 11, 'Noticias sobre tecnología, IA y sistemas', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7550, 11, 'Libros de historia, biografía o política', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7551, 11, 'Revistas sobre salud, bienestar y medicina', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7552, 11, 'Manuales técnicos de mecánica o electrónica', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7553, 12, 'El que organiza los recursos y optimiza los procesos', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7554, 12, 'El que propone la visión creativa y estética', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7555, 12, 'El que analiza las normas y media en los conflictos', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7556, 12, 'El que se enfoca en los detalles técnicos y operativos', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7557, 13, 'La posibilidad de innovar tecnológicamente', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7558, 13, 'El servicio directo a la comunidad y la ayuda humanitaria', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7559, 13, 'La estabilidad que brinda la gestión empresarial y contable', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7560, 13, 'La libertad de creación artística y cultural', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7561, 14, 'Mucha, me gusta descubrir nuevas curas o vacunas', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7562, 14, 'Bastante, me interesa entender el pasado de mi región', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7563, 14, 'Me interesa la investigación aplicada a la industria', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7564, 14, 'Prefiero la investigación sobre el comportamiento humano', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7565, 15, 'Una gran empresa o un emprendimiento propio', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7566, 15, 'Una obra de teatro, una película o una banda musical', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7567, 15, 'Una campaña de concientización ambiental', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7568, 15, 'Un sistema de redes informáticas seguro', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7569, 16, 'El cambio climático y la gestión del agua', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7570, 16, 'La creación de energías limpias y eficientes', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7571, 16, 'El tratamiento de enfermedades mentales en la sociedad', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7572, 16, 'La digitalización y automatización de la vida cotidiana', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7573, 17, 'Ciencias exactas (Física, Química, Matemática)', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7574, 17, 'Artes visuales o música', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7575, 17, 'Filosofía, Historia o Ética', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7576, 17, 'Educación para la salud y prevención', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7577, 18, 'El periodismo y los medios masivos', 'Comunicación');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7578, 18, 'El marketing digital y la publicidad', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7579, 18, 'La comunicación institucional en empresas', 'Comunicación');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7580, 18, 'La divulgación científica o cultural', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7581, 19, 'Supervisando procesos en una fábrica o industria', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7582, 19, 'Atendiendo pacientes en un consultorio o centro médico', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7583, 19, 'Litigando en tribunales o asesorando legalmente', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7584, 19, 'Investigando y publicando hallazgos académicos', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7585, 20, 'Un edificio moderno y funcional', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7586, 20, 'Un sistema de riego eficiente para el campo', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7587, 20, 'Una estrategia de ventas internacional', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7588, 20, 'Una plataforma interactiva o aplicación móvil', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7589, 21, 'La precisión y el rigor lógico', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7590, 21, 'La justicia y la equidad', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7591, 21, 'La empatía y la compasión', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7592, 21, 'La eficiencia y la productividad', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7593, 22, 'Computadoras y software especializado', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7594, 22, 'Instrumental quirúrgico o de diagnóstico', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7595, 22, 'Herramientas de corte, soldadura y maquinaria', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7596, 22, 'Instrumentos musicales, pinceles o cámaras', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7597, 23, 'Las leyes que regulan el comportamiento social y civil', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7598, 23, 'Las leyes de la física que gobiernan el movimiento', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7599, 23, 'Las normas contables y leyes del mercado', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7600, 23, 'Las normas ambientales y de protección de recursos', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7601, 24, 'Hacer las industrias más seguras y eficientes', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7602, 24, 'Incorporar más arte y creatividad en la vida diaria', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7603, 24, 'Mejorar la salud mental de los trabajadores', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7604, 24, 'Facilitar el acceso a la tecnología para todos', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7605, 25, 'El manejo de cultivos extensivos', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7606, 25, 'El cuidado y sanidad de los animales', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7607, 25, 'El estudio de los suelos y las rocas', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7608, 25, 'El manejo de bosques y parques naturales', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7609, 26, 'Un saldo contable y la rentabilidad de una empresa', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7610, 26, 'Una obra de arte o una pieza teatral', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7611, 26, 'Un mapa meteorológico o astronómico', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7612, 26, 'La estructura de una molécula o ADN', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7613, 27, 'Asistencia técnica en reparaciones complejas', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7614, 27, 'Asistencia social en comunidades vulnerables', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7615, 27, 'Asistencia nutricional y planes de salud', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7616, 27, 'Asesoramiento financiero y económico', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7617, 28, 'Mucha, me interesa la danza y el teatro', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7618, 28, 'Intermedia, la veo clave para kinesiología y rehabilitación', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7619, 28, 'Poca, prefiero el trabajo intelectual o administrativo', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7620, 29, 'La vida secreta de los volcanes y terremotos', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7621, 29, 'El impacto de la inteligencia artificial en el empleo', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7622, 29, 'La historia olvidada de los pueblos de Tucumán', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7623, 29, 'Avances en la medicina para alargar la vida', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7624, 30, 'Cumplir un sueño de vocación postergado', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7625, 30, 'Adquirir habilidades técnicas para una salida laboral rápida', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7626, 30, 'Profundizar en el conocimiento científico y académico', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7627, 30, 'Desarrollar mi potencial creativo y expresivo', 'Arte y Diseño');

DROP TABLE IF EXISTS `orientaciones`;
CREATE TABLE `orientaciones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=999 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (6, 'Agronomía');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (10, 'Arte y Diseño');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (391, 'Ciencias');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (5, 'Ciencias Naturales');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (11, 'Comunicación');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (8, 'Derecho');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (409, 'Educacion');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (374, 'fisica');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (9, 'Humanidades');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (2, 'Ingeniería');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (37, 'matematica');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (7, 'Negocios');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (3, 'Salud');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (4, 'Salud Mental');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (1, 'Tecnología');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (405, 'Tecnologia y Computacion');

DROP TABLE IF EXISTS `carrera_areas`;
CREATE TABLE `carrera_areas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `carrera_id` int(11) NOT NULL,
  `area` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_carrera` (`carrera_id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `carrera_areas` (`id`, `carrera_id`, `area`) VALUES (62, 43, 'Agronomía');
INSERT INTO `carrera_areas` (`id`, `carrera_id`, `area`) VALUES (63, 43, 'Arte y Diseño');
INSERT INTO `carrera_areas` (`id`, `carrera_id`, `area`) VALUES (64, 43, 'Ciencias');

DROP TABLE IF EXISTS `noticias`;
CREATE TABLE `noticias` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(300) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `imagen` varchar(500) DEFAULT NULL,
  `fuente` varchar(100) NOT NULL,
  `fecha` date NOT NULL,
  `link` varchar(500) DEFAULT '#',
  `categoria` varchar(100) DEFAULT 'General',
  `es_externa` tinyint(1) DEFAULT 0,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_link` (`link`(255))
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`) VALUES (1, 'Nuevas becas estratégicas para ingeniería', 'La Universidad Nacional de Tucumán abre 50 nuevas becas completas para carreras de ingeniería con énfasis en tecnología e innovación para el ciclo 2026.', 'https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=600&q=80', 'La Gaceta', '2026-05-07', '#1', 'Ingeniería', 0, '2026-05-09 16:55:02');
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`) VALUES (2, 'Tendencias: IA y programación dominan las inscripciones 2026', 'Según datos estadísticos, las carreras tecnológicas crecen un 34% en inscriptos. Python, inteligencia artificial y ciberseguridad lideran las preferencias.', 'https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=600&q=80', 'Universia', '2026-05-06', '#2', 'Tecnología', 0, '2026-05-09 16:55:02');
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`) VALUES (3, 'Apertura de inscripciones en facultades de artes de la UNT', 'La Facultad de Artes de la UNT abre inscripciones para Diseño Gráfico, Música y Artes Visuales. Plazo límite: 30 de mayo de 2026.', 'https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=600&q=80', 'La Gaceta', '2026-05-04', '#3', 'Arte y Diseño', 0, '2026-05-09 16:55:02');
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`) VALUES (4, 'La UTN lanza curso gratuito de ciberseguridad para estudiantes', 'UTN Tucumán ofrece una capacitación gratuita de 40 horas en ciberseguridad, abierta a todos los estudiantes universitarios de la región.', 'https://images.unsplash.com/photo-1510511459019-5dda7724fd87?w=600&q=80', 'UTN', '2026-05-03', '#4', 'Tecnología', 0, '2026-05-09 16:55:02');
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`) VALUES (5, 'Psicología y Trabajo Social: las carreras sociales más elegidas en Tucumán', 'Un informe de la UNT revela que las carreras del área social crecen sostenidamente, con Psicología liderando con más de 1.200 inscriptos anuales.', 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=600&q=80', 'Universia', '2026-05-01', '#5', 'Salud Mental', 0, '2026-05-09 16:55:02');
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`) VALUES (6, 'Agronomía sustentable: nuevas materias en la FAZ para 2026', 'La Facultad de Agronomía y Zootecnia incorpora tres nuevas materias enfocadas en agricultura sustentable, riego inteligente y gestión ambiental.', 'https://images.unsplash.com/photo-1574943320219-553eb213f72d?w=600&q=80', 'La Gaceta', '2026-04-28', '#6', 'Agronomía', 0, '2026-05-09 16:55:02');
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`) VALUES (7, 'Con un dispositivo que convierte la luz en sonido y a través de la piel: así pueden disfrutar los invidentes del eclipse', 'Un aparato desarrollado en el Instituto de Ciencias del Espacio del CSIC permitirá que los invidentes no se pierdan el fenómeno astronómico', 'https://imagenes.elpais.com/resizer/v2/5WQMBNRE7BB47BS2KIGCYT3WIQ.jpg?auth=6d42bbc185f29513894302639505603e1dcea8883253858f25b9173fb9eb4eb7', 'El País Tecnología', '2026-07-29', 'https://elpais.com/sociedad/2026-07-29/con-un-dispositivo-que-convierte-la-luz-en-sonido-y-a-traves-de-la-piel-asi-pueden-disfrutar-los-invidentes-del-eclipse.html', 'Tecnología', 1, '2026-07-30 06:28:01');
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`) VALUES (8, 'De la Thermomix al cortacésped autónomo: así se están llenando las casas de robots', 'Una nueva generación de máquinas autónomas se abre paso en casa y apuntan a un mantenimiento cotidiano del hogar casi invisible', 'https://imagenes.elpais.com/resizer/v2/IK3D4TDKTZCVLJSAR4GBK27GHE.jpg?auth=e2f4c6923992f680f05788789d39b9f658542bf28123146cf32dec8ab87fd8a3', 'El País Tecnología', '2026-07-29', 'https://elpais.com/tecnologia/2026-07-29/de-la-thermomix-al-cortacesped-autonomo-asi-se-estan-llenando-las-casas-de-robots.html', 'Tecnología', 1, '2026-07-30 06:28:02');
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`) VALUES (9, 'Amigos digitales con IA, la nueva amenaza para la salud mental de los adolescentes', 'Los psicólogos alertan de que los jóvenes recurren cada vez más a herramientas como ChatGPT en busca de apoyo emocional, una práctica que consideran altamente peligrosa', 'https://imagenes.elpais.com/resizer/v2/EYH5I2VEQFC7RCXYOLLTP7BBDY.jpg?auth=ffa7376ee53b6aa282c293092329ba18e889974a939098301230e47de7f1b3ca', 'El País Tecnología', '2026-07-28', 'https://elpais.com/tecnologia/2026-07-28/amigos-digitales-con-ia-la-nueva-amenaza-para-la-salud-mental-de-los-adolescentes.html', 'Tecnología', 1, '2026-07-30 06:28:02');
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`) VALUES (10, 'Proteger la libertad de expresión es mucho más que poder decir lo que te dé la gana', 'La concepción europea sobre este asunto nunca se ha basado en la idea de que “quien habla puede decir cualquier cosa y los demás deben callarse”', 'https://imagenes.elpais.com/resizer/v2/BK5YXPGNVBDRPPIJAC77WASZI4.jpg?auth=96998ca0aa5d38e8380d542ab8714513963c5fbc67a8930c4d87c24cba779159', 'El País Tecnología', '2026-07-27', 'https://elpais.com/tecnologia/2026-07-27/proteger-la-libertad-de-expresion-es-mucho-mas-que-poder-decir-lo-que-te-de-la-gana.html', 'Tecnología', 1, '2026-07-30 06:28:02');
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`) VALUES (11, 'Cuando el león de la IA se escapa de la jaula', 'Podríamos decir que la inteligencia artificial decidió que la manera más eficaz de aprobar el examen era… robar y copiar', 'https://imagenes.elpais.com/resizer/v2/VSL7B5G4JJHJ5CKKEKRQGMW5T4.jpg?auth=b6c8ac34ea8de8c4f1eab5c6c18f193413cb01f64d4801943b91c50c0cf1e18c', 'El País Tecnología', '2026-07-26', 'https://elpais.com/tecnologia/2026-07-26/cuando-el-leon-de-la-ia-se-escapa-de-la-jaula.html', 'Tecnología', 1, '2026-07-30 06:28:02');
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`) VALUES (12, 'Cuando la inteligencia artificial pone a prueba el Pacto Verde Europeo', 'Bruselas defiende la reducción de emisiones, pero se muestra dispuesta a impulsar la expansión de infraestructuras con un elevado consumo eléctrico y dependientes de combustibles fósiles', 'https://imagenes.elpais.com/resizer/v2/RYDELIKOVNADNFA33BTMJQAMXI.jpg?auth=64903ddcd362582e01f383fe10c0de592b66d71f5b44e7e94540f23b3a1d3c53', 'El País Tecnología', '2026-07-25', 'https://elpais.com/tecnologia/2026-07-25/cuando-la-inteligencia-artificial-pone-a-prueba-el-pacto-verde-europeo.html', 'Tecnología', 1, '2026-07-30 06:28:02');
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`) VALUES (13, 'Un misterioso relato gay de Alan Turing lo retrata como descarado, amante de la literatura y del sexo', 'La imagen de uno de los mayores científicos del siglo XX está lejos de lo que fueron su vida y gustos reales, según un estudio de la Universidad de Cambridge', 'https://imagenes.elpais.com/resizer/v2/D4H3WRJJLVE6JJSONRJRJ4J3WA.jpg?auth=331b3a7020519d1778ec9d71f911682506a59e7b45ae0ee9dad3cf47c9e279fc', 'El País Tecnología', '2026-07-23', 'https://elpais.com/tecnologia/2026-07-23/un-misterioso-relato-gay-de-alan-turing-lo-retrata-como-descarado-amante-de-la-literatura-y-del-sexo.html', 'Tecnología', 1, '2026-07-30 06:28:02');
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`) VALUES (14, 'Un nuevo modelo de OpenAI provoca un ataque “sin precedentes” contra otra plataforma de inteligencia artificial', 'Los creadores de ChatGPT probaban sus nuevas creaciones en un entorno aislado. Pero la máquina supo salir por su cuenta, en un escenario propio de la ciencia ficción', 'https://imagenes.elpais.com/resizer/v2/VSL7B5G4JJHJ5CKKEKRQGMW5T4.jpg?auth=b6c8ac34ea8de8c4f1eab5c6c18f193413cb01f64d4801943b91c50c0cf1e18c', 'El País Tecnología', '2026-07-22', 'https://elpais.com/tecnologia/2026-07-22/un-nuevo-modelo-de-openai-provoca-un-ataque-sin-precedentes-contra-otra-plataforma-de-inteligencia-artificial.html', 'Tecnología', 1, '2026-07-30 06:28:02');
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`) VALUES (16, 'Capacitación en Electroneumática', 'la utn invita a alumnos y profesionales a participar de los nuevos cursos capacitacion', 'https://frt.utn.edu.ar/wp-content/uploads/2026/05/Captura-de-pantalla-2026-05-14-221610.png', 'UTN', '2026-08-05', 'https://frt.utn.edu.ar/capacitacion-en-electroneumatica/', 'General', 0, '2026-08-05 04:19:40');

DROP TABLE IF EXISTS `fuentes`;
CREATE TABLE `fuentes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `activo` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=494 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `fuentes` (`id`, `nombre`, `activo`) VALUES (8, 'La Gaceta', 1);
INSERT INTO `fuentes` (`id`, `nombre`, `activo`) VALUES (10, 'UTN', 1);
INSERT INTO `fuentes` (`id`, `nombre`, `activo`) VALUES (35, 'siglo 21', 1);
INSERT INTO `fuentes` (`id`, `nombre`, `activo`) VALUES (178, 'UNT', 1);
INSERT INTO `fuentes` (`id`, `nombre`, `activo`) VALUES (255, 'clarín', 1);
INSERT INTO `fuentes` (`id`, `nombre`, `activo`) VALUES (418, 'Prueba', 1);

DROP TABLE IF EXISTS `fuentes_eliminadas`;
CREATE TABLE `fuentes_eliminadas` (
  `nombre` varchar(100) NOT NULL,
  PRIMARY KEY (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `fuentes_eliminadas` (`nombre`) VALUES ('El País Tecnología');
INSERT INTO `fuentes_eliminadas` (`nombre`) VALUES ('Universia');

DROP TABLE IF EXISTS `filtros_fecha`;
CREATE TABLE `filtros_fecha` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `valor` varchar(20) NOT NULL,
  `etiqueta` varchar(50) NOT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `orden` int(11) DEFAULT 0,
  `condicion` varchar(250) NOT NULL DEFAULT '',
  `es_fijo` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `valor` (`valor`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `filtros_fecha` (`id`, `valor`, `etiqueta`, `activo`, `orden`, `condicion`, `es_fijo`) VALUES (1, 'todas', 'Todas', 1, 0, '', 1);
INSERT INTO `filtros_fecha` (`id`, `valor`, `etiqueta`, `activo`, `orden`, `condicion`, `es_fijo`) VALUES (2, 'hoy', 'Hoy', 1, 1, 'fecha = CURDATE()', 1);
INSERT INTO `filtros_fecha` (`id`, `valor`, `etiqueta`, `activo`, `orden`, `condicion`, `es_fijo`) VALUES (4, 'semana', 'Esta semana', 1, 3, 'fecha >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)', 1);
INSERT INTO `filtros_fecha` (`id`, `valor`, `etiqueta`, `activo`, `orden`, `condicion`, `es_fijo`) VALUES (5, 'mes', 'Este mes', 1, 4, 'fecha >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)', 1);
INSERT INTO `filtros_fecha` (`id`, `valor`, `etiqueta`, `activo`, `orden`, `condicion`, `es_fijo`) VALUES (10, '2026', '2026', 1, 5, 'fecha >= ''2026-01-01'' AND fecha <= ''2026-12-31''', 0);
INSERT INTO `filtros_fecha` (`id`, `valor`, `etiqueta`, `activo`, `orden`, `condicion`, `es_fijo`) VALUES (11, 'ayer', 'Ayer', 1, 2, 'fecha = DATE_SUB(CURDATE(), INTERVAL 1 DAY)', 1);
INSERT INTO `filtros_fecha` (`id`, `valor`, `etiqueta`, `activo`, `orden`, `condicion`, `es_fijo`) VALUES (12, 'las_mejores_carreras', 'las mejores carreras 2026', 1, 6, 'fecha >= ''2026-08-05'' AND fecha <= ''2026-08-06''', 0);
INSERT INTO `filtros_fecha` (`id`, `valor`, `etiqueta`, `activo`, `orden`, `condicion`, `es_fijo`) VALUES (13, 'mejores_carreras_202', 'mejores carreras 2027', 1, 7, 'fecha >= ''2026-08-06'' AND fecha <= ''2026-08-07''', 0);

DROP TABLE IF EXISTS `game_carreras`;
CREATE TABLE `game_carreras` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `carrera_id` int(11) NOT NULL,
  `texto_boton` varchar(100) DEFAULT 'Ver carrera',
  `titulo_card` varchar(150) DEFAULT NULL,
  `descripcion_card` text DEFAULT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `orden` int(11) DEFAULT 0,
  `boton_no` varchar(100) NOT NULL DEFAULT 'No es lo mío',
  `boton_info` varchar(100) NOT NULL DEFAULT 'Info',
  `boton_yes` varchar(100) NOT NULL DEFAULT 'Me interesa',
  PRIMARY KEY (`id`),
  KEY `carrera_id` (`carrera_id`),
  CONSTRAINT `game_carreras_ibfk_1` FOREIGN KEY (`carrera_id`) REFERENCES `carreras` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=437 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `game_preguntas`;
CREATE TABLE `game_preguntas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `texto_pregunta` varchar(300) NOT NULL,
  `opcion_a_texto` varchar(200) NOT NULL,
  `opcion_a_area` varchar(100) NOT NULL,
  `opcion_b_texto` varchar(200) NOT NULL,
  `opcion_b_area` varchar(100) NOT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `orden` int(11) DEFAULT 0,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (1, 'Te regalan un kit de herramientas. Que haces primero?', 'Desarmo la radio para ver como funciona por dentro', 'Tecnologia', 'Ayudo a un vecino a arreglar su silla rota', 'Servicio Social', 0, 0, '2026-07-16 17:52:16');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (2, 'Estas en un museo. A que sala vas?', 'Sala de innovaciones cientificas y robots', 'Tecnologia', 'Sala de cuadros clasicos y esculturas', 'Arte y Diseno', 0, 0, '2026-07-16 17:52:16');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (3, 'Hay un problema en el curso. Como actuas?', 'Organizo a todos para encontrar una solucion justa', 'Liderazgo', 'Analizo los datos y busco una explicacion logica', 'Investigacion', 1, 0, '2026-07-16 17:52:16');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (6, 'te gusta leeer', 'si', 'Ciencias', 'no', 'Arte y Diseño', 1, 0, '2026-08-06 19:22:11');

DROP TABLE IF EXISTS `tests`;
CREATE TABLE `tests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) NOT NULL,
  `fecha` datetime DEFAULT current_timestamp(),
  `completado` tinyint(1) DEFAULT 0,
  `fecha_realizacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `tests_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `resultados`;
CREATE TABLE `resultados` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `test_id` int(11) NOT NULL,
  `area_profesional_sugerida` varchar(100) NOT NULL,
  `area_id` int(11) NOT NULL,
  `puntaje` int(11) DEFAULT 0,
  `detalle` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`detalle`)),
  `created_at` datetime DEFAULT current_timestamp(),
  `notas_personales` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `test_id` (`test_id`),
  KEY `area_id` (`area_id`),
  CONSTRAINT `resultados_ibfk_1` FOREIGN KEY (`test_id`) REFERENCES `tests` (`id`) ON DELETE CASCADE,
  CONSTRAINT `resultados_ibfk_2` FOREIGN KEY (`area_id`) REFERENCES `areas` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS=1;

-- Fin del dump
