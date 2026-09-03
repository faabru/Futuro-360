-- Futuro 360 - dump completo de contenido
-- Generado con scripts/exportar_base.py (no editar a mano).
-- Importar UNA VEZ desde MySQL Workbench (Open SQL Script).

CREATE DATABASE IF NOT EXISTS `futuro360` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `futuro360`;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS `carreras`;
CREATE TABLE "carreras" (
  "id" int NOT NULL AUTO_INCREMENT,
  "nombre" varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  "descripcion" text COLLATE utf8mb4_unicode_ci,
  "area_profesional" varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  "instituciones" text COLLATE utf8mb4_unicode_ci,
  "popular" tinyint(1) DEFAULT '0',
  "imagen" varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT '',
  "imagen_portada" varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  "imagen_principal" varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  "a_que_se_dedica" text COLLATE utf8mb4_unicode_ci,
  "video" varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY ("id")
);

INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (1, 'Ingeniería en Sistemas de Información', 'Diseño y desarrollo de software, bases de datos, redes y sistemas informáticos.', 'Tecnología', 'UTN - FR Tucumán, UNT - FACET', 1, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648779/tecnologia-Ingenier%C3%ADa%20en%20Sistemas%20de%20Informaci%C3%B3n-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648780/tecnologia-Ingenier%C3%ADa%20en%20Sistemas%20de%20Informaci%C3%B3n-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (2, 'Licenciatura en Sistemas de Información', 'Análisis, diseño e implementación de sistemas de información empresariales.', 'Tecnología', 'UNT - FACET, UNSTA', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648781/tecnologia-Licenciatura%20en%20Sistemas%20de%20Informaci%C3%B3n-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648782/tecnologia-Licenciatura%20en%20Sistemas%20de%20Informaci%C3%B3n-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (3, 'Tecnicatura en Programación', 'Desarrollo de aplicaciones web, móviles y de escritorio. Salida laboral rápida.', 'Tecnología', 'UTN - FR Tucumán, Institutos Superiores de Tucumán', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648782/tecnologia-Tecnicatura%20en%20Programaci%C3%B3n-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648783/tecnologia-Tecnicatura%20en%20Programaci%C3%B3n-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (4, 'Ingeniería Civil', 'Diseño y construcción de infraestructuras: edificios, puentes, caminos y obras hidráulicas.', 'Ingeniería', 'UNT - FACET, UTN - FR Tucumán', 1, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648784/ingenieria-ingenieria%20civil-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648785/ingenieria-ingenieria%20civil-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (5, 'Ingeniería Mecánica', 'Diseño, análisis y mantenimiento de sistemas mecánicos y procesos industriales.', 'Ingeniería', 'UNT - FACET, UTN - FR Tucumán', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648786/ingenieria-ingenieria%20mecanica-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648786/ingenieria-ingenieria%20mecanica-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (6, 'Ingeniería Eléctrica', 'Generación, transmisión y distribución de energía eléctrica. Automatización industrial.', 'Ingeniería', 'UNT - FACET, UTN - FR Tucumán', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648788/ingenieria-ingenieria%20electrica-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648788/ingenieria-ingenieria%20electrica-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (7, 'Ingeniería Industrial', 'Optimización de procesos productivos, gestión de calidad y logística industrial.', 'Ingeniería', 'UTN - FR Tucumán, UNT - FACET', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648789/ingenieria-ingenieria%20industrial-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648790/ingenieria-ingenieria%20industrial-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (8, 'Ingeniería Química', 'Transformación de materias primas en productos industriales mediante procesos químicos.', 'Ingeniería', 'UNT - FACET', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648791/ingenieria-ingenieria%20quimica-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648791/ingenieria-ingenieria%20quimica-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (9, 'Medicina', 'Diagnóstico, tratamiento y prevención de enfermedades.', 'Salud', 'UNT - Facultad de Medicina', 1, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648792/salud-medicina-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648793/salud-medicina-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (10, 'Enfermería', 'Cuidado integral del paciente en hospitales, clínicas y atención domiciliaria.', 'Salud', 'UNT - Facultad de Medicina, Instituto Superior de Enfermería', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648793/salud-enfermeria-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648794/salud-enfermeria-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (11, 'Odontología', 'Diagnóstico y tratamiento de enfermedades bucodentales.', 'Salud', 'UNT - Facultad de Odontología', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648795/salud-odontologia-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648796/salud-odontologia-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (12, 'Kinesiología y Fisioterapia', 'Rehabilitación física y recuperación del movimiento.', 'Salud', 'UNT - Facultad de Medicina', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648796/salud-Kinesiolog%C3%ADa%20y%20Fisioterapia-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648797/salud-Kinesiolog%C3%ADa%20y%20Fisioterapia-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (13, 'Nutrición', 'Planificación de dietas y planes alimentarios para individuos y comunidades.', 'Salud', 'UNT - Facultad de Medicina, UNSTA', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648798/salud-nutrici%C3%B3n-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648798/salud-nutrici%C3%B3n-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (14, 'Bioquímica', 'Análisis clínicos, investigación farmacéutica y control de calidad alimentaria.', 'Salud', 'UNT - FBQyF', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648799/salud-bioquimica-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648800/salud-bioquimica-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (15, 'Farmacia', 'Dispensación de medicamentos, control de calidad y farmacología clínica.', 'Salud', 'UNT - FBQyF', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648800/salud-farmacia-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648801/salud-farmacia-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (16, 'Psicología', 'Estudio del comportamiento humano, terapia individual y grupal.', 'Salud Mental', 'UNT - Facultad de Psicología, UNSTA', 1, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648802/salud%20mental-Psicolog%C3%ADa-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648802/salud%20mental-Psicolog%C3%ADa-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (17, 'Trabajo Social', 'Intervención en problemáticas sociales y acompañamiento a comunidades vulnerables.', 'Salud Mental', 'UNT - Facultad de Filosofía y Letras', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648803/salud%20mental-trabajo%20social-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648804/salud%20mental-trabajo%20social-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (18, 'Psicopedagogía', 'Diagnóstico y tratamiento de dificultades de aprendizaje.', 'Salud Mental', 'UNSTA, Institutos Superiores de Tucumán', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648804/salud%20mental-psicopedagogia-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648805/salud%20mental-psicopedagogia-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (19, 'Biología', 'Estudio de los seres vivos, genética, ecología y biotecnología.', 'Ciencias Naturales', 'UNT - Facultad de Ciencias Naturales', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648806/ciencias%20naturales-biologia-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648806/ciencias%20naturales-biologia-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (20, 'Geología', 'Estudio de la estructura y composición de la Tierra. Minería y recursos naturales.', 'Ciencias Naturales', 'UNT - Facultad de Ciencias Naturales', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648807/ciencias%20naturales-geologia-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648807/ciencias%20naturales-geologia-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (21, 'Química', 'Investigación y aplicación de la composición y transformación de la materia.', 'Ciencias Naturales', 'UNT - FBQyF', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648808/ciencias%20naturales-quimica-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648809/ciencias%20naturales-quimica-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (22, 'Ingeniería Agronómica', 'Producción vegetal, manejo de suelos y gestión de empresas agropecuarias.', 'Agronomía', 'UNT - FAZ', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648809/agronomia-ingenieria%20agronomica%20-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648810/agronomia-ingenieria%20agronomica%20-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (23, 'Medicina Veterinaria', 'Salud y producción animal, sanidad de mascotas y animales de granja.', 'Agronomía', 'UNT - FAZ', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648811/agronomia-medicina%20veterinaria-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648812/agronomia-medicina%20veterinaria-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (24, 'Ingeniería Forestal', 'Manejo y conservación de bosques, recursos madereros y gestión ambiental.', 'Agronomía', 'UNT - FAZ', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648812/agronomia-ingenieria%20forestal%20-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648813/agronomia-ingenieria%20forestal%20-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (25, 'Tecnicatura en Producción Agropecuaria', 'Formación técnica en producción animal y vegetal con salida laboral rápida.', 'Agronomía', 'INTA Tucumán, Institutos Superiores Rurales', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648814/agronomia-Tecnicatura%20en%20Producci%C3%B3n%20Agropecuaria-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648814/agronomia-Tecnicatura%20en%20Producci%C3%B3n%20Agropecuaria-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (26, 'Contador Público Nacional', 'Auditoría, impuestos, contabilidad y asesoramiento financiero empresarial.', 'Negocios', 'UNT - FCE, UNSTA', 1, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648815/negocios-contador%20publico%20nacional-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648816/negocios-contador%20publico%20nacional-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (27, 'Licenciatura en Administración', 'Gestión de empresas, recursos humanos, marketing y estrategia organizacional.', 'Negocios', 'UNT - FCE, UNSTA, UTN', 1, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648816/negocios-licenciatura%20en%20administracion-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648817/negocios-licenciatura%20en%20administracion-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (28, 'Licenciatura en Economía', 'Análisis de mercados, política económica y desarrollo regional.', 'Negocios', 'UNT - FCE', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648818/negocios-licenciatura%20en%20economia-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648819/negocios-licenciatura%20en%20economia-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (29, 'Marketing Digital', 'Estrategias de comunicación digital, publicidad online y posicionamiento de marcas.', 'Negocios', 'UNSTA, Institutos Superiores de Tucumán', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648819/negocios-marketing%20digital-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648820/negocios-marketing%20digital-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (30, 'Abogacía', 'Representación legal, litigios y asesoramiento jurídico en todas las ramas del derecho.', 'Derecho', 'UNT - Facultad de Derecho, UNSTA', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648820/derecho-abogacia-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648821/derecho-abogacia-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (31, 'Notariado', 'Escrituras, contratos y documentos legales con fe pública.', 'Derecho', 'UNT - Facultad de Derecho', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648822/derecho-notariado-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648822/derecho-notariado-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (32, 'Ciencias Políticas', 'Análisis del poder, instituciones del Estado y gestión pública.', 'Derecho', 'UNT - Facultad de Derecho', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648823/derecho-ciencias%20politicas-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648824/derecho-ciencias%20politicas-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (33, 'Licenciatura en Historia', 'Investigación y enseñanza del pasado humano. Archivos, museos y docencia.', 'Humanidades', 'UNT - Facultad de Filosofía y Letras', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648825/humanidades-licenciatura%20en%20historia-portada.png', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648826/humanidades-licenciatura%20en%20historia-principal.png', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (34, 'Licenciatura en Filosofía', 'Pensamiento crítico, ética, lógica y epistemología.', 'Humanidades', 'UNT - Facultad de Filosofía y Letras', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648826/humanidades-licenciatura%20en%20filosofia-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648827/humanidades-licenciatura%20en%20filosofia-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (35, 'Licenciatura en Letras', 'Literatura, lingüística, escritura creativa y docencia de lengua.', 'Humanidades', 'UNT - Facultad de Filosofía y Letras', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648828/humanidades-licenciatura%20en%20letras-portada.png', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648829/humanidades-licenciatura%20en%20letras-principal.png', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (36, 'Diseño Gráfico', 'Creación visual de marcas, publicidad, packaging e interfaces digitales.', 'Arte y Diseño', 'UNT - Facultad de Artes, UNSTA, Institutos Superiores', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648829/arte%20y%20dise%C3%B1o-dise%C3%B1o%20grafico-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648830/arte%20y%20dise%C3%B1o-dise%C3%B1o%20grafico-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (37, 'Licenciatura en Artes Visuales', 'Pintura, escultura, instalación y gestión cultural.', 'Arte y Diseño', 'UNT - Facultad de Artes', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648831/arte%20y%20dise%C3%B1o-Licenciatura%20en%20Artes%20Visuales-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648832/arte%20y%20dise%C3%B1o-Licenciatura%20en%20Artes%20Visuales-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (38, 'Música', 'Interpretación, composición y dirección musical.', 'Arte y Diseño', 'UNT - Facultad de Artes', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648832/arte%20y%20dise%C3%B1o-musica-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648833/arte%20y%20dise%C3%B1o-musica-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (39, 'Arquitectura', 'Diseño y planificación de edificios y espacios. Combina arte, técnica y funcionalidad.', 'Arte y Diseño', 'UNT - FAU', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648834/arte%20y%20dise%C3%B1o-arquitectura-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648835/arte%20y%20dise%C3%B1o-arquitectura-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (40, 'Licenciatura en Comunicación Social', 'Periodismo, relaciones públicas, comunicación institucional y medios digitales.', 'Comunicación', 'UNT - Facultad de Filosofía y Letras', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648836/comunicaci%C3%B3n-Licenciatura%20en%20Comunicaci%C3%B3n%20Social-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648836/comunicaci%C3%B3n-Licenciatura%20en%20Comunicaci%C3%B3n%20Social-principal.jpg', NULL, NULL);
INSERT INTO `carreras` (`id`, `nombre`, `descripcion`, `area_profesional`, `instituciones`, `popular`, `imagen`, `imagen_portada`, `imagen_principal`, `a_que_se_dedica`, `video`) VALUES (42, 'Publicidad', 'Creación de campañas publicitarias, estrategia de marca y comunicación persuasiva.', 'Comunicación', 'UNSTA, Institutos Superiores', 0, '', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648838/comunicaci%C3%B3n-publicidad-portada.jpg', 'https://res.cloudinary.com/eaybmmjr/image/upload/v1786648839/comunicaci%C3%B3n-publicidad-principal.jpg', '', '');

DROP TABLE IF EXISTS `areas`;
CREATE TABLE "areas" (
  "id" int NOT NULL AUTO_INCREMENT,
  "nombre" varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  "descripcion" text COLLATE utf8mb4_unicode_ci,
  "icono" varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  "color" varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY ("id")
);

INSERT INTO `areas` (`id`, `nombre`, `descripcion`, `icono`, `color`) VALUES (1, 'Ciencias Exactas', 'Matem??tica, F??sica, Ingenier??a, Inform??tica', '????', '#4F8EF7');
INSERT INTO `areas` (`id`, `nombre`, `descripcion`, `icono`, `color`) VALUES (2, 'Ciencias de la Salud', 'Medicina, Enfermer??a, Bioqu??mica, Farmacia', '??????', '#2DC87A');
INSERT INTO `areas` (`id`, `nombre`, `descripcion`, `icono`, `color`) VALUES (3, 'Ciencias Sociales', 'Derecho, Psicolog??a, Sociolog??a, Trabajo Social', '????', '#F7A94F');
INSERT INTO `areas` (`id`, `nombre`, `descripcion`, `icono`, `color`) VALUES (4, 'Arte y Dise??o', 'Arquitectura, Bellas Artes, Dise??o, M??sica', '????', '#E05CDB');
INSERT INTO `areas` (`id`, `nombre`, `descripcion`, `icono`, `color`) VALUES (5, 'Humanidades', 'Historia, Filosof??a, Letras, Comunicaci??n', '????', '#F7574F');
INSERT INTO `areas` (`id`, `nombre`, `descripcion`, `icono`, `color`) VALUES (6, 'Ciencias Naturales', 'Biolog??a, Geolog??a, Ecolog??a, Veterinaria', '????', '#4FC9F7');
INSERT INTO `areas` (`id`, `nombre`, `descripcion`, `icono`, `color`) VALUES (7, 'Econom??a y Negocios', 'Administraci??n, Econom??a, Comercio, Marketing', '????', '#F7D94F');

DROP TABLE IF EXISTS `preguntas`;
CREATE TABLE "preguntas" (
  "id" int NOT NULL AUTO_INCREMENT,
  "texto_pregunta" varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  "area_profesional" varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY ("id")
);

INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (1, 'Cuando tenés un día completamente libre, ¿qué te gustaría hacer?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (2, 'Cuando aparece un problema difícil, ¿qué te sale naturalmente hacer?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (3, '¿Qué tema podría hacer que te quedaras investigando durante horas?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (4, 'Te dan un presupuesto para crear un proyecto. ¿Cuál elegirías?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (5, '¿Qué situación te produciría mayor satisfacción?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (6, 'Si pudieras aprender una actividad durante un año, ¿cuál elegirías?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (7, '¿Qué te atraería más de un trabajo que nunca probaste?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (8, '¿Qué te gustaría que alguien dijera de vos dentro de 20 años?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (9, 'Cuando aprendés algo nuevo, ¿qué te genera más curiosidad?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (10, 'Imaginá que mañana tenés que elegir un lugar para pasar todo el día. ¿Cuál preferís?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (11, 'Si supieras que no podés equivocarte, ¿qué te animarías a intentar?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (12, '¿Qué problema del mundo te gustaría poder solucionar?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (13, 'Pensando en tu futuro, ¿qué te gustaría tener más?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (14, '¿Qué sacrificio estarías más dispuesto/a a hacer por una profesión que realmente te apasionara?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (15, '¿Qué te preocupa más cuando pensás en elegir una carrera?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (16, '¿Cuál de estas frases se acerca más a tu manera de pensar?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (17, 'Si tuvieras garantizado un buen sueldo en cualquier profesión, ¿qué elegirías?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (18, '¿Qué te gustaría aprender sobre vos mismo antes de elegir una carrera?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (19, 'Imaginá tu vida laboral ideal. ¿Qué tendría?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (20, 'Imaginá que te proponen armar una muestra o evento para tu comunidad. ¿En qué te gustaría colaborar?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (21, 'Cuando pensás en el trabajo ideal, ¿qué pesa más para vos?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (22, '¿Qué esperás encontrar realmente en una profesión?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (23, 'Cuando tenés que tomar una decisión importante, ¿qué suele pesar más?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (24, '¿Qué clase de desafío te resulta más atractivo?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (25, 'Dentro de diez años, ¿qué te gustaría pensar al mirar hacia atrás?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (26, '¿Qué preferirías hacer durante una jornada de trabajo?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (27, '¿Cuál de estas preguntas te genera más curiosidad?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (28, 'Si pudieras mejorar una sola habilidad tuya, ¿cuál elegirías?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (29, 'Si pudieras cambiar algo de tu comunidad, ¿qué elegirías?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (30, 'Última pregunta: si nadie pudiera juzgarte por tu elección, ¿qué camino sentís que te gustaría explorar?', 'General');

DROP TABLE IF EXISTS `opciones_pregunta`;
CREATE TABLE "opciones_pregunta" (
  "id" int NOT NULL AUTO_INCREMENT,
  "pregunta_id" int NOT NULL,
  "texto_opcion" varchar(300) COLLATE utf8mb4_unicode_ci NOT NULL,
  "area_profesional" varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY ("id"),
  KEY "pregunta_id" ("pregunta_id"),
  CONSTRAINT "opciones_pregunta_ibfk_1" FOREIGN KEY ("pregunta_id") REFERENCES "preguntas" ("id") ON DELETE CASCADE
);

INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (1, 1, 'Pasar tiempo al aire libre, recorrer lugares naturales o estar en contacto con animales o plantas.', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (2, 1, 'Dibujar, diseñar, sacar fotos, hacer música o crear algo propio.', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (3, 1, 'Leer, conocer historias y culturas, y reflexionar sobre distintas ideas.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (4, 1, 'Pasar tiempo con computadoras, tecnología, videojuegos o herramientas digitales.', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (5, 1, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (6, 2, 'Buscar una solución práctica y pensar cómo llevarla a la realidad.', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7, 2, 'Investigar por qué ocurre antes de sacar una conclusión.', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (8, 2, 'Revisar las reglas, derechos o normas que podrían estar involucrados.', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (9, 2, 'Pensar primero en quién puede verse afectado y cómo ayudarlo.', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (10, 2, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (11, 3, 'El universo, los seres vivos o los fenómenos naturales.', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (12, 3, 'Leyes, justicia, derechos y conflictos sociales.', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (13, 3, 'Historia, filosofía, literatura o culturas.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (14, 3, 'Programación, inteligencia artificial, videojuegos o innovación.', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (15, 3, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (16, 4, 'Un proyecto de acompañamiento y bienestar para la comunidad.', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (17, 4, 'Un estudio creativo o proyecto artístico.', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (18, 4, 'Una empresa o emprendimiento.', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (19, 4, 'Diseñar y construir una solución para un problema concreto.', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (20, 4, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (21, 5, 'Saber que ayudaste a una persona a mejorar su salud.', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (22, 5, 'Conseguir que se haga justicia en una situación complicada.', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (23, 5, 'Ver a otras personas disfrutar algo que creaste.', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (24, 5, 'Hacer crecer un proyecto hasta convertirlo en algo exitoso.', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (25, 5, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (26, 6, 'Comunicación, periodismo o producción audiovisual.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (27, 6, 'Historia, literatura, filosofía o idiomas.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (28, 6, 'Psicología, emociones o relaciones humanas.', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (29, 6, 'Programación, robótica o inteligencia artificial.', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (30, 6, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (31, 7, 'Trabajar en contacto con la naturaleza.', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (32, 7, 'Crear o transformar algo de manera original y visual.', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (33, 7, 'Organizar proyectos, negociar y tomar decisiones.', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (34, 7, 'Trabajar cuidando personas.', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (35, 7, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (36, 8, 'Dejó ideas y conocimientos que todavía siguen siendo importantes.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (37, 8, 'Defendió a quienes necesitaban ayuda.', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (38, 8, 'Logró transmitir ideas que llegaron a muchísimas personas.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (39, 8, 'Ayudó a muchas personas a sentirse comprendidas y acompañadas.', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (40, 8, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (41, 9, 'Por qué ocurre determinado fenómeno.', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (42, 9, 'Cómo puede afectar al cuerpo humano.', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (43, 9, 'Cómo llevarlo a la práctica.', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (44, 9, 'Cómo puede influir en las emociones y relaciones.', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (45, 9, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (46, 10, 'Una finca, reserva o espacio natural.', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (47, 10, 'Un estudio de arte o diseño.', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (48, 10, 'Un laboratorio.', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (49, 10, 'Una empresa o espacio de negocios.', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (50, 10, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (51, 11, 'Crear algo que pueda influir en muchas personas.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (52, 11, 'Defender una causa en la que realmente creo.', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (53, 11, 'Construir una solución para un problema importante.', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (54, 11, 'Crear una tecnología que todavía no existe.', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (55, 11, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (56, 12, 'El deterioro ambiental y la producción poco sustentable.', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (57, 12, 'Las enfermedades y problemas de salud.', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (58, 12, 'Los problemas emocionales y la falta de acompañamiento.', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (59, 12, 'La injusticia y la desigualdad ante la ley.', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (60, 12, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (61, 13, 'Contacto con la naturaleza.', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (62, 13, 'Libertad para crear.', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (63, 13, 'Independencia económica.', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (64, 13, 'Tiempo para aprender y reflexionar.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (65, 13, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (66, 14, 'Pasar mucho tiempo estudiando e investigando.', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (67, 14, 'Estar constantemente frente a personas o exponiéndome públicamente.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (68, 14, 'Continuar estudiando y profundizando en ideas que me apasionen.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (69, 14, 'Escuchar y acompañar situaciones emocionales complicadas.', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (70, 14, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (71, 15, 'No tener estabilidad económica.', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (72, 15, 'Quedarme atrás frente a los cambios tecnológicos.', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (73, 15, 'Sentir que mi trabajo no tiene impacto social.', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (74, 15, 'No poder hacer algo creativo.', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (75, 15, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (76, 16, 'Tenemos que aprender a producir sin destruir lo que tenemos.', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (77, 16, 'Antes de opinar, quiero entender qué está pasando.', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (78, 16, 'Entender el pasado ayuda a comprender el presente.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (79, 16, 'Los problemas se solucionan haciendo.', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (80, 16, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (81, 17, 'Trabajar en el cuidado de las personas.', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (82, 17, 'Comunicar e informar.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (83, 17, 'Crear y diseñar.', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (84, 17, 'Programar, innovar o trabajar con tecnología.', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (85, 17, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (86, 18, 'Cómo manejo mis emociones y las de los demás.', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (87, 18, 'Qué tan cómodo/a me siento tomando decisiones y asumiendo riesgos.', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (88, 18, 'Aprender sobre prevención y cuidado de la salud.', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (89, 18, 'Cómo me expreso y cómo logro comunicarme.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (90, 18, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (91, 19, 'Naturaleza, espacios abiertos y proyectos sustentables.', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (92, 19, 'Cultura, conocimiento y aprendizaje continuo.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (93, 19, 'Desafíos técnicos y problemas para resolver.', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (94, 19, 'Tecnología, innovación y herramientas digitales.', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (95, 19, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (96, 20, 'En la investigación: elegir el contenido y los datos.', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (97, 20, 'En lo visual: diseñar la identidad y los carteles.', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (98, 20, 'En la organización: coordinar, presupuestar y comunicar.', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (99, 20, 'En la logística: que todo funcione y esté en su lugar.', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (100, 20, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (101, 21, 'El contacto con el ambiente y la naturaleza.', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (102, 21, 'Sentir que estoy defendiendo algo importante.', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (103, 21, 'Comprender y acompañar a otras personas.', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (104, 21, 'Trabajar con innovación y tecnología.', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (105, 21, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (106, 22, 'Un espacio para pensar, aprender y comprender el mundo.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (107, 22, 'Problemas interesantes que me obliguen a buscar soluciones.', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (108, 22, 'Una oportunidad para construir independencia y crecimiento.', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (109, 22, 'Historias, personas e ideas que pueda comunicar.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (110, 22, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (111, 23, 'Cómo puede afectar al ambiente o a otras formas de vida.', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (112, 23, 'Qué sería lo más justo en esa situación.', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (113, 23, 'Qué opción es más práctica y funciona mejor.', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (114, 23, 'Qué solución puedo encontrar utilizando tecnología.', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (115, 23, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (116, 24, 'Resolver una pregunta difícil mediante investigación.', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (117, 24, 'Lograr que un mensaje llegue y sea comprendido por muchas personas.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (118, 24, 'Convertir una idea en un proyecto exitoso.', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (119, 24, 'Encontrar una forma de mejorar la vida o salud de alguien.', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (120, 24, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (121, 25, 'Hice algo para cuidar nuestro planeta.', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (122, 25, 'Creé cosas que realmente representan quién soy.', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (123, 25, 'Nunca dejé de aprender y cuestionarme.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (124, 25, 'Construí cosas que realmente funcionan.', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (125, 25, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (126, 26, 'Analizar información y hacer experimentos.', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (127, 26, 'Entrevistar, grabar, escribir o comunicar.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (128, 26, 'Conversar y acompañar personas.', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (129, 26, 'Programar, probar herramientas o desarrollar tecnología.', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (130, 26, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (131, 27, '¿Cómo podemos vivir y producir sin destruir el ambiente?', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (132, 27, '¿Por qué ocurre determinado fenómeno?', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (133, 27, '¿Qué hace que una situación sea realmente justa?', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (134, 27, '¿Qué podría llegar a hacer una tecnología que todavía no existe?', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (135, 27, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (136, 28, 'Comunicarme y expresarme mejor.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (137, 28, 'Resolver problemas prácticos.', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (138, 28, 'Liderar y tomar mejores decisiones.', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (139, 28, 'Comprender mejor las emociones.', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (140, 28, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (141, 29, 'Mejorar los espacios verdes y el cuidado ambiental.', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (142, 29, 'Ayudar a que las personas conozcan y defiendan sus derechos.', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (143, 29, 'Mejorar el acceso a la salud.', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (144, 29, 'Mejorar la forma en que la comunidad se informa y comunica.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (145, 29, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (146, 30, 'Arte, diseño, música o creatividad.', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (147, 30, 'Humanidades, cultura, historia, filosofía o literatura.', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (148, 30, 'Ingeniería, construcción o resolución de problemas técnicos.', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (149, 30, 'Programación, informática, inteligencia artificial o tecnología.', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (150, 30, 'Ninguna de las anteriores', 'Neutral');

DROP TABLE IF EXISTS `orientaciones`;
CREATE TABLE "orientaciones" (
  "id" int NOT NULL AUTO_INCREMENT,
  "nombre" varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY ("id"),
  UNIQUE KEY "nombre" ("nombre")
);

INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (6, 'Agronomía');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (10, 'Arte y Diseño');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (391, 'Ciencias');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (5, 'Ciencias Naturales');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (11, 'Comunicación');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (8, 'Derecho');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (9, 'Humanidades');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (2, 'Ingeniería');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (37, 'matematica');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (7, 'Negocios');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (3, 'Salud');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (4, 'Salud Mental');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (1, 'Tecnología');
INSERT INTO `orientaciones` (`id`, `nombre`) VALUES (405, 'Tecnologia y Computacion');

DROP TABLE IF EXISTS `carrera_areas`;
CREATE TABLE "carrera_areas" (
  "id" int NOT NULL AUTO_INCREMENT,
  "carrera_id" int NOT NULL,
  "area" varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY ("id"),
  KEY "idx_carrera" ("carrera_id")
);

INSERT INTO `carrera_areas` (`id`, `carrera_id`, `area`) VALUES (62, 43, 'Agronomía');
INSERT INTO `carrera_areas` (`id`, `carrera_id`, `area`) VALUES (63, 43, 'Arte y Diseño');
INSERT INTO `carrera_areas` (`id`, `carrera_id`, `area`) VALUES (64, 43, 'Ciencias');
INSERT INTO `carrera_areas` (`id`, `carrera_id`, `area`) VALUES (65, 42, 'Comunicación');

DROP TABLE IF EXISTS `noticias`;
CREATE TABLE "noticias" (
  "id" int NOT NULL AUTO_INCREMENT,
  "titulo" varchar(300) COLLATE utf8mb4_unicode_ci NOT NULL,
  "descripcion" text COLLATE utf8mb4_unicode_ci,
  "imagen" varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  "fuente" varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  "fecha" date NOT NULL,
  "link" varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT '#',
  "categoria" varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT 'General',
  "es_externa" tinyint(1) DEFAULT '0',
  "fecha_creacion" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "video" varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY ("id"),
  UNIQUE KEY "unique_link" ("link"(255))
);

INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`, `video`) VALUES (1, 'Nuevas becas estratégicas para ingeniería', 'La Universidad Nacional de Tucumán abre 50 nuevas becas completas para carreras de ingeniería con énfasis en tecnología e innovación para el ciclo 2026.', 'https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=600&q=80', 'La Gaceta', '2026-05-07', '#1', 'Ingeniería', 0, '2026-05-09 16:55:02', NULL);
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`, `video`) VALUES (2, 'Tendencias: IA y programación dominan las inscripciones 2026', 'Según datos estadísticos, las carreras tecnológicas crecen un 34% en inscriptos. Python, inteligencia artificial y ciberseguridad lideran las preferencias.', 'https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=600&q=80', 'Universia', '2026-05-06', '#2', 'Tecnología', 0, '2026-05-09 16:55:02', NULL);
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`, `video`) VALUES (3, 'Apertura de inscripciones en facultades de artes de la UNT', 'La Facultad de Artes de la UNT abre inscripciones para Diseño Gráfico, Música y Artes Visuales. Plazo límite: 30 de mayo de 2026.', 'https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=600&q=80', 'La Gaceta', '2026-05-04', '#3', 'Arte y Diseño', 0, '2026-05-09 16:55:02', NULL);
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`, `video`) VALUES (4, 'La UTN lanza curso gratuito de ciberseguridad para estudiantes', 'UTN Tucumán ofrece una capacitación gratuita de 40 horas en ciberseguridad, abierta a todos los estudiantes universitarios de la región.', 'https://images.unsplash.com/photo-1510511459019-5dda7724fd87?w=600&q=80', 'UTN', '2026-05-03', '#4', 'Tecnología', 0, '2026-05-09 16:55:02', NULL);
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`, `video`) VALUES (5, 'Psicología y Trabajo Social: las carreras sociales más elegidas en Tucumán', 'Un informe de la UNT revela que las carreras del área social crecen sostenidamente, con Psicología liderando con más de 1.200 inscriptos anuales.', 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=600&q=80', 'Universia', '2026-05-01', '#5', 'Salud Mental', 0, '2026-05-09 16:55:02', NULL);
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`, `video`) VALUES (6, 'Agronomía sustentable: nuevas materias en la FAZ para 2026', 'La Facultad de Agronomía y Zootecnia incorpora tres nuevas materias enfocadas en agricultura sustentable, riego inteligente y gestión ambiental.', 'https://images.unsplash.com/photo-1574943320219-553eb213f72d?w=600&q=80', 'La Gaceta', '2026-04-28', '#6', 'Agronomía', 0, '2026-05-09 16:55:02', NULL);
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`, `video`) VALUES (7, 'Con un dispositivo que convierte la luz en sonido y a través de la piel: así pueden disfrutar los invidentes del eclipse', 'Un aparato desarrollado en el Instituto de Ciencias del Espacio del CSIC permitirá que los invidentes no se pierdan el fenómeno astronómico', 'https://imagenes.elpais.com/resizer/v2/5WQMBNRE7BB47BS2KIGCYT3WIQ.jpg?auth=6d42bbc185f29513894302639505603e1dcea8883253858f25b9173fb9eb4eb7', 'El País Tecnología', '2026-07-29', 'https://elpais.com/sociedad/2026-07-29/con-un-dispositivo-que-convierte-la-luz-en-sonido-y-a-traves-de-la-piel-asi-pueden-disfrutar-los-invidentes-del-eclipse.html', 'Tecnología', 1, '2026-07-30 06:28:01', NULL);
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`, `video`) VALUES (8, 'De la Thermomix al cortacésped autónomo: así se están llenando las casas de robots', 'Una nueva generación de máquinas autónomas se abre paso en casa y apuntan a un mantenimiento cotidiano del hogar casi invisible', 'https://imagenes.elpais.com/resizer/v2/IK3D4TDKTZCVLJSAR4GBK27GHE.jpg?auth=e2f4c6923992f680f05788789d39b9f658542bf28123146cf32dec8ab87fd8a3', 'El País Tecnología', '2026-07-29', 'https://elpais.com/tecnologia/2026-07-29/de-la-thermomix-al-cortacesped-autonomo-asi-se-estan-llenando-las-casas-de-robots.html', 'Tecnología', 1, '2026-07-30 06:28:02', NULL);
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`, `video`) VALUES (9, 'Amigos digitales con IA, la nueva amenaza para la salud mental de los adolescentes', 'Los psicólogos alertan de que los jóvenes recurren cada vez más a herramientas como ChatGPT en busca de apoyo emocional, una práctica que consideran altamente peligrosa', 'https://imagenes.elpais.com/resizer/v2/EYH5I2VEQFC7RCXYOLLTP7BBDY.jpg?auth=ffa7376ee53b6aa282c293092329ba18e889974a939098301230e47de7f1b3ca', 'El País Tecnología', '2026-07-28', 'https://elpais.com/tecnologia/2026-07-28/amigos-digitales-con-ia-la-nueva-amenaza-para-la-salud-mental-de-los-adolescentes.html', 'Tecnología', 1, '2026-07-30 06:28:02', NULL);
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`, `video`) VALUES (10, 'Proteger la libertad de expresión es mucho más que poder decir lo que te dé la gana', 'La concepción europea sobre este asunto nunca se ha basado en la idea de que “quien habla puede decir cualquier cosa y los demás deben callarse”', 'https://imagenes.elpais.com/resizer/v2/BK5YXPGNVBDRPPIJAC77WASZI4.jpg?auth=96998ca0aa5d38e8380d542ab8714513963c5fbc67a8930c4d87c24cba779159', 'El País Tecnología', '2026-07-27', 'https://elpais.com/tecnologia/2026-07-27/proteger-la-libertad-de-expresion-es-mucho-mas-que-poder-decir-lo-que-te-de-la-gana.html', 'Tecnología', 1, '2026-07-30 06:28:02', NULL);
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`, `video`) VALUES (11, 'Cuando el león de la IA se escapa de la jaula', 'Podríamos decir que la inteligencia artificial decidió que la manera más eficaz de aprobar el examen era… robar y copiar', 'https://imagenes.elpais.com/resizer/v2/VSL7B5G4JJHJ5CKKEKRQGMW5T4.jpg?auth=b6c8ac34ea8de8c4f1eab5c6c18f193413cb01f64d4801943b91c50c0cf1e18c', 'El País Tecnología', '2026-07-26', 'https://elpais.com/tecnologia/2026-07-26/cuando-el-leon-de-la-ia-se-escapa-de-la-jaula.html', 'Tecnología', 1, '2026-07-30 06:28:02', NULL);
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`, `video`) VALUES (12, 'Cuando la inteligencia artificial pone a prueba el Pacto Verde Europeo', 'Bruselas defiende la reducción de emisiones, pero se muestra dispuesta a impulsar la expansión de infraestructuras con un elevado consumo eléctrico y dependientes de combustibles fósiles', 'https://imagenes.elpais.com/resizer/v2/RYDELIKOVNADNFA33BTMJQAMXI.jpg?auth=64903ddcd362582e01f383fe10c0de592b66d71f5b44e7e94540f23b3a1d3c53', 'El País Tecnología', '2026-07-25', 'https://elpais.com/tecnologia/2026-07-25/cuando-la-inteligencia-artificial-pone-a-prueba-el-pacto-verde-europeo.html', 'Tecnología', 1, '2026-07-30 06:28:02', NULL);
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`, `video`) VALUES (13, 'Un misterioso relato gay de Alan Turing lo retrata como descarado, amante de la literatura y del sexo', 'La imagen de uno de los mayores científicos del siglo XX está lejos de lo que fueron su vida y gustos reales, según un estudio de la Universidad de Cambridge', 'https://imagenes.elpais.com/resizer/v2/D4H3WRJJLVE6JJSONRJRJ4J3WA.jpg?auth=331b3a7020519d1778ec9d71f911682506a59e7b45ae0ee9dad3cf47c9e279fc', 'El País Tecnología', '2026-07-23', 'https://elpais.com/tecnologia/2026-07-23/un-misterioso-relato-gay-de-alan-turing-lo-retrata-como-descarado-amante-de-la-literatura-y-del-sexo.html', 'Tecnología', 1, '2026-07-30 06:28:02', NULL);
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`, `video`) VALUES (14, 'Un nuevo modelo de OpenAI provoca un ataque “sin precedentes” contra otra plataforma de inteligencia artificial', 'Los creadores de ChatGPT probaban sus nuevas creaciones en un entorno aislado. Pero la máquina supo salir por su cuenta, en un escenario propio de la ciencia ficción', 'https://imagenes.elpais.com/resizer/v2/VSL7B5G4JJHJ5CKKEKRQGMW5T4.jpg?auth=b6c8ac34ea8de8c4f1eab5c6c18f193413cb01f64d4801943b91c50c0cf1e18c', 'El País Tecnología', '2026-07-22', 'https://elpais.com/tecnologia/2026-07-22/un-nuevo-modelo-de-openai-provoca-un-ataque-sin-precedentes-contra-otra-plataforma-de-inteligencia-artificial.html', 'Tecnología', 1, '2026-07-30 06:28:02', NULL);
INSERT INTO `noticias` (`id`, `titulo`, `descripcion`, `imagen`, `fuente`, `fecha`, `link`, `categoria`, `es_externa`, `fecha_creacion`, `video`) VALUES (16, 'Capacitación en Electroneumática', 'la utn invita a alumnos y profesionales a participar de los nuevos cursos capacitacion', 'https://frt.utn.edu.ar/wp-content/uploads/2026/05/Captura-de-pantalla-2026-05-14-221610.png', 'UTN', '2026-08-05', 'https://frt.utn.edu.ar/capacitacion-en-electroneumatica/', 'General', 0, '2026-08-05 04:19:40', NULL);

DROP TABLE IF EXISTS `fuentes`;
CREATE TABLE "fuentes" (
  "id" int NOT NULL AUTO_INCREMENT,
  "nombre" varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  "activo" tinyint(1) DEFAULT '1',
  PRIMARY KEY ("id"),
  UNIQUE KEY "nombre" ("nombre")
);

INSERT INTO `fuentes` (`id`, `nombre`, `activo`) VALUES (8, 'La Gaceta', 1);
INSERT INTO `fuentes` (`id`, `nombre`, `activo`) VALUES (10, 'UTN', 1);
INSERT INTO `fuentes` (`id`, `nombre`, `activo`) VALUES (35, 'siglo 21', 1);
INSERT INTO `fuentes` (`id`, `nombre`, `activo`) VALUES (178, 'UNT', 1);
INSERT INTO `fuentes` (`id`, `nombre`, `activo`) VALUES (255, 'clarín', 1);
INSERT INTO `fuentes` (`id`, `nombre`, `activo`) VALUES (418, 'Prueba', 1);

DROP TABLE IF EXISTS `fuentes_eliminadas`;
CREATE TABLE "fuentes_eliminadas" (
  "nombre" varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY ("nombre")
);

INSERT INTO `fuentes_eliminadas` (`nombre`) VALUES ('El País Tecnología');
INSERT INTO `fuentes_eliminadas` (`nombre`) VALUES ('Universia');

DROP TABLE IF EXISTS `filtros_fecha`;
CREATE TABLE "filtros_fecha" (
  "id" int NOT NULL AUTO_INCREMENT,
  "valor" varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  "etiqueta" varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  "activo" tinyint(1) DEFAULT '1',
  "orden" int DEFAULT '0',
  "condicion" varchar(250) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  "es_fijo" tinyint(1) DEFAULT '0',
  PRIMARY KEY ("id"),
  UNIQUE KEY "valor" ("valor")
);

INSERT INTO `filtros_fecha` (`id`, `valor`, `etiqueta`, `activo`, `orden`, `condicion`, `es_fijo`) VALUES (1, 'todas', 'Todas', 1, 0, '', 1);
INSERT INTO `filtros_fecha` (`id`, `valor`, `etiqueta`, `activo`, `orden`, `condicion`, `es_fijo`) VALUES (2, 'hoy', 'Hoy', 1, 1, 'fecha = CURDATE()', 1);
INSERT INTO `filtros_fecha` (`id`, `valor`, `etiqueta`, `activo`, `orden`, `condicion`, `es_fijo`) VALUES (4, 'semana', 'Esta semana', 1, 3, 'fecha >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)', 1);
INSERT INTO `filtros_fecha` (`id`, `valor`, `etiqueta`, `activo`, `orden`, `condicion`, `es_fijo`) VALUES (5, 'mes', 'Este mes', 1, 4, 'fecha >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)', 1);
INSERT INTO `filtros_fecha` (`id`, `valor`, `etiqueta`, `activo`, `orden`, `condicion`, `es_fijo`) VALUES (10, '2026', '2026', 1, 5, 'fecha >= ''2026-01-01'' AND fecha <= ''2026-12-31''', 0);
INSERT INTO `filtros_fecha` (`id`, `valor`, `etiqueta`, `activo`, `orden`, `condicion`, `es_fijo`) VALUES (11, 'ayer', 'Ayer', 1, 2, 'fecha = DATE_SUB(CURDATE(), INTERVAL 1 DAY)', 1);
INSERT INTO `filtros_fecha` (`id`, `valor`, `etiqueta`, `activo`, `orden`, `condicion`, `es_fijo`) VALUES (12, 'las_mejores_carreras', 'las mejores carreras 2026', 1, 6, 'fecha >= ''2026-08-05'' AND fecha <= ''2026-08-06''', 0);
INSERT INTO `filtros_fecha` (`id`, `valor`, `etiqueta`, `activo`, `orden`, `condicion`, `es_fijo`) VALUES (13, 'mejores_carreras_202', 'mejores carreras 2027', 1, 7, 'fecha >= ''2026-08-06'' AND fecha <= ''2026-08-07''', 0);

DROP TABLE IF EXISTS `game_carreras`;
CREATE TABLE "game_carreras" (
  "id" int NOT NULL AUTO_INCREMENT,
  "carrera_id" int NOT NULL,
  "texto_boton" varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT 'Ver carrera',
  "titulo_card" varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  "descripcion_card" text COLLATE utf8mb4_unicode_ci,
  "activo" tinyint(1) DEFAULT '1',
  "orden" int DEFAULT '0',
  "boton_no" varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'No es lo mío',
  "boton_info" varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Info',
  "boton_yes" varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Me interesa',
  PRIMARY KEY ("id"),
  KEY "carrera_id" ("carrera_id"),
  CONSTRAINT "game_carreras_ibfk_1" FOREIGN KEY ("carrera_id") REFERENCES "carreras" ("id") ON DELETE CASCADE
);

INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (437, 1, 'Ver carrera', 'Ingeniería en Sistemas de Información', 'Diseño y desarrollo de software, bases de datos, redes y sistemas informáticos.', 1, 1, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (438, 2, 'Ver carrera', 'Licenciatura en Sistemas de Información', 'Análisis, diseño e implementación de sistemas de información empresariales.', 1, 2, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (439, 3, 'Ver carrera', 'Tecnicatura en Programación', 'Desarrollo de aplicaciones web, móviles y de escritorio. Salida laboral rápida.', 1, 3, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (440, 4, 'Ver carrera', 'Ingeniería Civil', 'Diseño y construcción de infraestructuras: edificios, puentes, caminos y obras hidráulicas.', 1, 4, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (441, 5, 'Ver carrera', 'Ingeniería Mecánica', 'Diseño, análisis y mantenimiento de sistemas mecánicos y procesos industriales.', 1, 5, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (442, 6, 'Ver carrera', 'Ingeniería Eléctrica', 'Generación, transmisión y distribución de energía eléctrica. Automatización industrial.', 1, 6, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (443, 7, 'Ver carrera', 'Ingeniería Industrial', 'Optimización de procesos productivos, gestión de calidad y logística industrial.', 1, 7, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (444, 8, 'Ver carrera', 'Ingeniería Química', 'Transformación de materias primas en productos industriales mediante procesos químicos.', 1, 8, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (445, 9, 'Ver carrera', 'Medicina', 'Diagnóstico, tratamiento y prevención de enfermedades.', 1, 9, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (446, 10, 'Ver carrera', 'Enfermería', 'Cuidado integral del paciente en hospitales, clínicas y atención domiciliaria.', 1, 10, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (447, 11, 'Ver carrera', 'Odontología', 'Diagnóstico y tratamiento de enfermedades bucodentales.', 1, 11, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (448, 12, 'Ver carrera', 'Kinesiología y Fisioterapia', 'Rehabilitación física y recuperación del movimiento.', 1, 12, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (449, 13, 'Ver carrera', 'Nutrición', 'Planificación de dietas y planes alimentarios para individuos y comunidades.', 1, 13, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (450, 14, 'Ver carrera', 'Bioquímica', 'Análisis clínicos, investigación farmacéutica y control de calidad alimentaria.', 1, 14, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (451, 15, 'Ver carrera', 'Farmacia', 'Dispensación de medicamentos, control de calidad y farmacología clínica.', 1, 15, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (452, 16, 'Ver carrera', 'Psicología', 'Estudio del comportamiento humano, terapia individual y grupal.', 0, 16, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (453, 17, 'Ver carrera', 'Trabajo Social', 'Intervención en problemáticas sociales y acompañamiento a comunidades vulnerables.', 0, 17, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (454, 18, 'Ver carrera', 'Psicopedagogía', 'Diagnóstico y tratamiento de dificultades de aprendizaje.', 0, 18, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (455, 19, 'Ver carrera', 'Biología', 'Estudio de los seres vivos, genética, ecología y biotecnología.', 0, 19, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (456, 20, 'Ver carrera', 'Geología', 'Estudio de la estructura y composición de la Tierra. Minería y recursos naturales.', 0, 20, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (457, 21, 'Ver carrera', 'Química', 'Investigación y aplicación de la composición y transformación de la materia.', 0, 21, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (458, 22, 'Ver carrera', 'Ingeniería Agronómica', 'Producción vegetal, manejo de suelos y gestión de empresas agropecuarias.', 0, 22, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (459, 23, 'Ver carrera', 'Medicina Veterinaria', 'Salud y producción animal, sanidad de mascotas y animales de granja.', 0, 23, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (460, 24, 'Ver carrera', 'Ingeniería Forestal', 'Manejo y conservación de bosques, recursos madereros y gestión ambiental.', 0, 24, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (461, 25, 'Ver carrera', 'Tecnicatura en Producción Agropecuaria', 'Formación técnica en producción animal y vegetal con salida laboral rápida.', 0, 25, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (462, 26, 'Ver carrera', 'Contador Público Nacional', 'Auditoría, impuestos, contabilidad y asesoramiento financiero empresarial.', 0, 26, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (463, 27, 'Ver carrera', 'Licenciatura en Administración', 'Gestión de empresas, recursos humanos, marketing y estrategia organizacional.', 0, 27, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (464, 28, 'Ver carrera', 'Licenciatura en Economía', 'Análisis de mercados, política económica y desarrollo regional.', 0, 28, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (465, 29, 'Ver carrera', 'Marketing Digital', 'Estrategias de comunicación digital, publicidad online y posicionamiento de marcas.', 0, 29, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (466, 30, 'Ver carrera', 'Abogacía', 'Representación legal, litigios y asesoramiento jurídico en todas las ramas del derecho.', 0, 30, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (467, 31, 'Ver carrera', 'Notariado', 'Escrituras, contratos y documentos legales con fe pública.', 0, 31, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (468, 32, 'Ver carrera', 'Ciencias Políticas', 'Análisis del poder, instituciones del Estado y gestión pública.', 0, 32, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (469, 33, 'Ver carrera', 'Licenciatura en Historia', 'Investigación y enseñanza del pasado humano. Archivos, museos y docencia.', 0, 33, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (470, 34, 'Ver carrera', 'Licenciatura en Filosofía', 'Pensamiento crítico, ética, lógica y epistemología.', 0, 34, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (471, 35, 'Ver carrera', 'Licenciatura en Letras', 'Literatura, lingüística, escritura creativa y docencia de lengua.', 0, 35, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (472, 36, 'Ver carrera', 'Diseño Gráfico', 'Creación visual de marcas, publicidad, packaging e interfaces digitales.', 0, 36, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (473, 37, 'Ver carrera', 'Licenciatura en Artes Visuales', 'Pintura, escultura, instalación y gestión cultural.', 0, 37, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (474, 38, 'Ver carrera', 'Música', 'Interpretación, composición y dirección musical.', 0, 38, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (475, 39, 'Ver carrera', 'Arquitectura', 'Diseño y planificación de edificios y espacios. Combina arte, técnica y funcionalidad.', 0, 39, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (476, 40, 'Ver carrera', 'Licenciatura en Comunicación Social', 'Periodismo, relaciones públicas, comunicación institucional y medios digitales.', 0, 40, 'No es lo mío', 'Info', 'Me interesa');
INSERT INTO `game_carreras` (`id`, `carrera_id`, `texto_boton`, `titulo_card`, `descripcion_card`, `activo`, `orden`, `boton_no`, `boton_info`, `boton_yes`) VALUES (478, 42, 'Ver carrera', 'Publicidad', 'Creación de campañas publicitarias, estrategia de marca y comunicación persuasiva.', 0, 42, 'No es lo mío', 'Info', 'Me interesa');

DROP TABLE IF EXISTS `game_preguntas`;
CREATE TABLE "game_preguntas" (
  "id" int NOT NULL AUTO_INCREMENT,
  "texto_pregunta" varchar(300) COLLATE utf8mb4_unicode_ci NOT NULL,
  "opcion_a_texto" varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  "opcion_a_area" varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  "opcion_b_texto" varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  "opcion_b_area" varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  "activo" tinyint(1) DEFAULT '1',
  "orden" int DEFAULT '0',
  "fecha_creacion" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY ("id")
);

INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (8, 'Te regalan un día libre. ¿Qué hacés?', 'Salgo a explorar la naturaleza', 'Agronomía', 'Me quedo jugando o viendo series', 'Humanidades', 1, 1, '2026-08-24 10:26:42');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (9, 'En un examen, ¿qué te sale mejor?', 'Las preguntas de números y cálculos', 'Tecnología', 'Los ensayos y textos largos', 'Humanidades', 1, 2, '2026-08-24 10:26:42');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (10, 'Si pudieras, ¿qué harías los fines de semana?', 'Ir al cine o a un recital', 'Arte y Diseño', 'Salir con amigos o familia', 'Salud Mental', 1, 3, '2026-08-24 10:26:42');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (11, '¿Qué te gustaría hacer de grande?', 'Tener mi propio consultorio o clínica', 'Salud', 'Tener mi propia empresa o negocio', 'Negocios', 1, 4, '2026-08-24 10:26:42');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (12, 'Cuando ves una noticia triste, ¿qué sentís?', 'Quiero hacer algo para ayudar', 'Salud Mental', 'Me informo más para entender qué pasó', 'Ciencias Naturales', 1, 5, '2026-08-24 10:26:43');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (13, '¿Qué tipo de lectura preferís?', 'Novelas o poesía que me hacen sentir algo', 'Humanidades', 'Revistas de tecnología o ciencia', 'Tecnología', 1, 6, '2026-08-24 10:26:43');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (14, 'Si tuvieras que elegir entre dos trabajos...', 'Uno que pague bien pero sea aburrido', 'Negocios', 'Uno que me apasione pero pague poco', 'Arte y Diseño', 1, 7, '2026-08-24 10:26:43');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (15, '¿Qué harías si encontrás un animal herido?', 'Lo llevaría a un veterinario o lo cuidaría', 'Salud', 'Buscaría información de qué hacer', 'Ciencias Naturales', 1, 8, '2026-08-24 10:26:43');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (16, 'En una prueba grupal, ¿qué rol tomás?', 'El que organiza y reparte tareas', 'Negocios', 'El que tiene las ideas locas', 'Arte y Diseño', 1, 9, '2026-08-24 10:26:43');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (17, '¿Qué te gusta más de un videojuego?', 'Resolver puzzles y desafíos lógicos', 'Tecnología', 'La historia y los personajes', 'Humanidades', 1, 10, '2026-08-24 10:26:44');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (18, 'Si pudieras vivir en cualquier época...', 'En el futuro, con toda la tecnología', 'Tecnología', 'En la naturaleza, lejos de la ciudad', 'Agronomía', 1, 11, '2026-08-24 10:26:44');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (19, '¿Qué te gustaría saber hacer?', 'Programar una app o un videojuego', 'Tecnología', 'Tocar un instrumento o pintar', 'Arte y Diseño', 1, 12, '2026-08-24 10:26:44');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (20, 'Cuando hay un problema en tu casa...', 'Lo arreglás vos mismo/a con YouTube', 'Ingeniería', 'Llamás a un profesional', 'Salud', 1, 13, '2026-08-24 10:26:44');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (21, '¿Qué te motivaría más para ir a la facu?', 'Que me enseñen cosas que me sirvan para laburar', 'Negocios', 'Que me guste lo que estoy aprendiendo', 'Humanidades', 1, 14, '2026-08-24 10:26:45');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (22, 'Si pudieras cambiar UNA cosa del mundo...', 'La desigualdad y la injusticia', 'Derecho', 'El daño que le hacemos al planeta', 'Agronomía', 1, 15, '2026-08-24 10:26:45');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (23, '¿Qué harías con un laboratorio bien equipado?', 'Haría experimentos de química o biología', 'Ciencias Naturales', 'Inventaría algo nuevo o mejoraría una máquina', 'Tecnología', 1, 16, '2026-08-24 10:26:45');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (24, '¿Qué tipo de proyectos te gustaría liderar?', 'Uno que ayude a la comunidad', 'Salud Mental', 'Uno que sea innovador y rompa esquemas', 'Tecnología', 1, 17, '2026-08-24 10:26:45');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (25, 'Si te ofrecen dos pasantías...', 'En una ONG que trabaja con jóvenes', 'Salud Mental', 'En una startup de tecnología', 'Tecnología', 1, 18, '2026-08-24 10:26:45');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (26, '¿Qué te gustaría que digan de tu trabajo?', 'Que ayudó a mucha gente', 'Salud', 'Que fue creativo y diferente', 'Arte y Diseño', 1, 19, '2026-08-24 10:26:46');
INSERT INTO `game_preguntas` (`id`, `texto_pregunta`, `opcion_a_texto`, `opcion_a_area`, `opcion_b_texto`, `opcion_b_area`, `activo`, `orden`, `fecha_creacion`) VALUES (27, 'Cuando pensás en tu futuro laboral...', 'Quiero estabilidad y buen sueldo', 'Negocios', 'Quiero disfrutar de lo que hago', 'Humanidades', 1, 20, '2026-08-24 10:26:46');

DROP TABLE IF EXISTS `tests`;
CREATE TABLE "tests" (
  "id" int NOT NULL AUTO_INCREMENT,
  "usuario_id" int NOT NULL,
  "fecha" datetime DEFAULT CURRENT_TIMESTAMP,
  "completado" tinyint(1) DEFAULT '0',
  "fecha_realizacion" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY ("id"),
  KEY "usuario_id" ("usuario_id"),
  CONSTRAINT "tests_ibfk_1" FOREIGN KEY ("usuario_id") REFERENCES "usuarios" ("id") ON DELETE CASCADE
);

DROP TABLE IF EXISTS `resultados`;
CREATE TABLE "resultados" (
  "id" int NOT NULL AUTO_INCREMENT,
  "test_id" int NOT NULL,
  "area_profesional_sugerida" varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  "area_id" int NOT NULL,
  "puntaje" int DEFAULT '0',
  "detalle" longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  "created_at" datetime DEFAULT CURRENT_TIMESTAMP,
  "notas_personales" text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY ("id"),
  UNIQUE KEY "test_id" ("test_id"),
  KEY "area_id" ("area_id"),
  CONSTRAINT "resultados_ibfk_1" FOREIGN KEY ("test_id") REFERENCES "tests" ("id") ON DELETE CASCADE,
  CONSTRAINT "resultados_ibfk_2" FOREIGN KEY ("area_id") REFERENCES "areas" ("id") ON DELETE CASCADE,
  CONSTRAINT "resultados_chk_1" CHECK (json_valid(`detalle`))
);

SET FOREIGN_KEY_CHECKS=1;

-- Fin del dump
