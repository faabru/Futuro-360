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

INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (31, 'Cuando tenés un problema, ¿qué hacés primero?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (32, '¿En cuál de estos lugares te sentirías más cómodo/a trabajando?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (33, '¿Qué te gustaría que la gente recuerde de vos?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (34, 'Si te regalan un kit de herramientas, ¿qué hacés?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (35, '¿Qué tipo de películas o series te enganchan más?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (36, '¿Qué materia del secundario más te gustó?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (37, 'Si tuvieras que elegir HOY una carrera, ¿a cuál irías?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (38, '¿Qué te gusta más: los números o las personas?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (39, 'Cuando hay un conflicto en tu grupo de amigos, ¿qué hacés?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (40, '¿Qué te genera más satisfacción?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (41, '¿Dónde te ves viviendo en el futuro?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (42, '¿Qué te gusta más de las redes sociales?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (43, 'Si pudieras elegir un superpoder, ¿cuál sería?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (44, '¿Qué tipo de noticias te llaman la atención?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (45, '¿Cómo te describirían tus amigos?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (46, 'Si tuvieras que dar una charla TED, ¿de qué hablarías?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (47, '¿Qué te motiva más para estudiar?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (48, '¿Cuál de estas frases te representa más?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (49, '¿Qué harías con un millón de pesos?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (50, '¿Qué tipo de trabajo te parece más importante?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (51, 'Cuando estás aburrido/a, ¿qué hacés?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (52, '¿Qué te parece más interesante?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (53, '¿Qué tipo de trabajador/a creés que sos?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (54, '¿Qué te haría sentir más orgulloso/a?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (55, 'Si tuvieras que elegir UNA cosa para aprender ahora, ¿cuál sería?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (56, '¿Qué te preocupa más del futuro?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (57, '¿En qué actividad del secundario te sentías más vivo/a?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (58, 'Si pudieras elegir tu estilo de vida a los 30 años, ¿cuál sería?', 'General');
INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) VALUES (59, '¿Qué consejo le darías a alguien que no sabe qué estudiar?', 'General');

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

INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7659, 31, 'Busco una solución lógica y paso a paso', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7660, 31, 'Me pongo a investigar qué lo causó', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7661, 31, 'Hablo con las personas involucradas para entenderlas', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7662, 31, 'Busco soluciones creativas o distintas a las típicas', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7663, 31, 'Analizo si hay alguna ley o regla que aplique', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7664, 31, 'Lo postergo, prefiero dejarlo para después', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7665, 31, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7666, 32, 'En un hospital o clínica atendiendo personas', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7667, 32, 'En un estudio o despacho arreglando asuntos legales', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7668, 32, 'En un taller, fábrica o construyendo algo', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7669, 32, 'En un estudio de arte o diseño trabajando con colores y formas', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7670, 32, 'En un campo o laboratorio cuidando el medio ambiente', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7671, 32, 'Me da igual, siempre y cuando me guste lo que haga', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7672, 32, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7673, 33, 'Que fui justo/a y ayudé a los demás', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7674, 33, 'Que dejé algo lindo, una obra o un diseño', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7675, 33, 'Que descubrí algo importante o inventé algo', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7676, 33, 'Que curé personas o las hice sentir mejor', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7677, 33, 'Que cuidé la tierra y las plantas', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7678, 33, 'Ni idea, apenas estoy empezando a pensarlo', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7679, 33, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7680, 34, 'Lo uso para arreglar algo roto en casa', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7681, 34, 'Lo guardo, no sé para qué sirve', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7682, 34, 'Lo desarmo para ver cómo funciona por dentro', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7683, 34, 'Lo uso para crear algo artístico o decorativo', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7684, 34, 'Lo presto a un vecino que lo necesita', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7685, 34, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7686, 35, 'De misterio o crimen donde hay que resolver algo', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7687, 35, 'De ciencia ficción o tecnología', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7688, 35, 'Documentales sobre la naturaleza o el espacio', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7689, 35, 'Dramas o historias que te hacen sentir algo fuerte', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7690, 35, 'De gente que supera obstáculos o ayuda a otros', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7691, 35, 'No veo mucho, me aburro rápido', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7692, 35, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7693, 36, 'Matemática o física', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7694, 36, 'Biología o química', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7695, 36, 'Historia o literatura', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7696, 36, 'Dibujo técnico o artística', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7697, 36, 'Economía o administración', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7698, 36, 'Ninguna en particular', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7699, 36, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7700, 37, 'Ingeniería en Sistemas o algo de computación', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7701, 37, 'Medicina o enfermería', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7702, 37, 'Abogacía o ciencias políticas', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7703, 37, 'Diseño gráfico o arquitectura', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7704, 37, 'Psicología o trabajo social', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7705, 37, 'Agronomía o biología', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7706, 37, 'Contador o administración de empresas', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7707, 37, 'Todavía no sé, por eso estoy acá', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7708, 37, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7709, 38, 'Los números, me gusta que todo cuente', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7710, 38, 'Las personas, me gusta escucharlas y ayudarlas', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7711, 38, 'Depende del día', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7712, 38, 'Los animales y las plantas', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7713, 38, 'Los colores y las formas', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7714, 38, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7715, 39, 'Intento mediar y que todos queden contentos', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7716, 39, 'Analizo quién tiene razón y se lo digo', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7717, 39, 'Me quedo al margen, no es mi problema', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7718, 39, 'Propongo una solución creativa que no habían pensado', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7719, 39, 'Investigo las causas del conflicto', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7720, 39, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7721, 40, 'Ayudar a alguien que lo necesita', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7722, 40, 'Resolver un problema difícil o un acertijo', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7723, 40, 'Crear algo nuevo: una obra, un diseño, una idea', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7724, 40, 'Ganar dinero o tener estabilidad económica', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7725, 40, 'Aprender algo nuevo cada día', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7726, 40, 'No lo sé, todavía estoy buscando', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7727, 40, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7728, 41, 'En una ciudad grande y con mucha actividad', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7729, 41, 'En un lugar tranquilo, cerca de la naturaleza', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7730, 41, 'En cualquier lado, lo importante es el laburo', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7731, 41, 'En el extranjero, conociendo otras culturas', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7732, 41, 'En Tucumán, aportando a la provincia', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7733, 41, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7734, 42, 'Ver noticias y enterarme de lo que pasa', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7735, 42, 'Crear contenido: fotos, videos, diseños', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7736, 42, 'Aprender cosas nuevas de cuentas educativas', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7737, 42, 'Me gustan pero me sacan mucho tiempo', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7738, 42, 'Conectar con gente y armar comunidades', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7739, 42, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7740, 43, 'Leer la mente de las personas', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7741, 43, 'Curar cualquier enfermedad', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7742, 43, 'Hacer que las máquinas me obedezcan', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7743, 43, 'Volar sobre los campos y ver la naturaleza', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7744, 43, 'Parar el tiempo para pensar con calma', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7745, 43, 'No necesito superpoderes, me gusta la realidad', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7746, 43, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7747, 44, 'De tecnología e innovación', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7748, 44, 'De salud y bienestar', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7749, 44, 'De política y derechos humanos', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7750, 44, 'De arte, cultura y entretenimiento', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7751, 44, 'De medio ambiente y cambio climático', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7752, 44, 'No suelo leer noticias', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7753, 44, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7754, 45, 'El/la que siempre ayuda a los demás', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7755, 45, 'El/la que siempre tiene ideas raras pero buenas', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7756, 45, 'El/la que sabe de todo un poco', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7757, 45, 'El/la tranqui, que va con el ritmo', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7758, 45, 'El/la que siempre pregunta ''¿por qué?''', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7759, 45, 'El/la que organiza todo el grupo', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7760, 45, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7761, 46, 'De cómo la tecnología cambia nuestras vidas', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7762, 46, 'De salud mental y emociones', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7763, 46, 'De un caso injusto que te marcó', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7764, 46, 'De un proyecto artístico o creativo', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7765, 46, 'De conservar el medio ambiente', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7766, 46, 'No daría una charla, me da cosa hablar en público', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7767, 46, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7768, 47, 'Saber que voy a poder ayudar a otros', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7769, 47, 'Ganar bien y tener buena vida', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7770, 47, 'Aprender cosas que me sirvan para crear', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7771, 47, 'Entender cómo funciona el mundo', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7772, 47, 'Porque me lo piden mis viejos', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7773, 47, 'Nada en particular, estudio porque toca', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7774, 47, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7775, 48, 'El que no arriesga, no gana', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7776, 48, 'Nadie entiende lo que siento', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7777, 48, 'Hay que ser justos con todos', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7778, 48, 'La naturaleza nos da todo, hay que cuidarla', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7779, 48, 'Si no funciona, hay que inventar algo nuevo', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7780, 48, 'Ninguna, soy más de acciones que de frases', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7781, 48, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7782, 49, 'Lo invertiría en un negocio propio', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7783, 49, 'Viajaría para conocer otras culturas', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7784, 49, 'Lo donaría a una cause social', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7785, 49, 'Compraría equipamiento para un taller', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7786, 49, 'Ahorrarlo para estar tranquilo/a', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7787, 49, 'Lo usaría para crear una obra o proyecto artístico', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7788, 49, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7789, 50, 'Salvar vidas en un hospital', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7790, 50, 'Defender a alguien que no puede defenderse', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7791, 50, 'Crear tecnología que facilite la vida', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7792, 50, 'Producir alimentos para la gente', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7793, 50, 'Hacer que los espacios se vean lindos', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7794, 50, 'Todos son importantes, no podría elegir', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7795, 50, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7796, 51, 'Busco algo nuevo para aprender', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7797, 51, 'Me pongo a dibujar, escribir o crear algo', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7798, 51, 'Juego a videojuegos o programmes algo', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7799, 51, 'Salgo a caminar o estoy en la naturaleza', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7800, 51, 'Charlo con amigos o veo series', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7801, 51, 'Duermo, la verdad', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7802, 51, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7803, 52, 'La inteligencia artificial y los robots', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7804, 52, 'Las enfermedades y cómo se curan', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7805, 52, 'Las leyes y cómo se hacen las normas', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7806, 52, 'El comportamiento de las personas', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7807, 52, 'Las plantas, los animales y el clima', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7808, 52, 'La economía y los mercados', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7809, 52, 'Me cuesta decidir, todo me parece interesante', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7810, 52, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7811, 53, 'Metódico/a, me gusta tener todo ordenado', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7812, 53, 'Empático/a, me importa cómo se sienten los demás', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7813, 53, 'Creativo/a, me gustan los desafíos distintos', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7814, 53, 'Práctico/a, quiero ver resultados concretos', 'Ingeniería');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7815, 53, 'Perseverante, no me rindo fácil', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7816, 53, 'Todavía no sé, estoy descubriendo', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7817, 53, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7818, 54, 'Curar a alguien o mejorar su calidad de vida', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7819, 54, 'Diseñar un edificio o una obra que todos vean', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7820, 54, 'Crear una app que usen millones de personas', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7821, 54, 'Ganar un caso importante o cambiar una ley', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7822, 54, 'Tener mi propio negocio y que le vaya bien', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7823, 54, 'Cuidar un bosque o una reserva natural', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7824, 54, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7825, 55, 'Programación o robótica', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7826, 55, 'Primeros auxilios o algo de salud', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7827, 55, 'Pintura, fotografía o edición de video', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7828, 55, 'Un idioma nuevo', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7829, 55, 'Contabilidad o marketing', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7830, 55, 'Nada, ya sé demasiado', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7831, 55, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7832, 56, 'No encontrar trabajo estable', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7833, 56, 'Que la tecnología reemplace a las personas', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7834, 56, 'El cambio climático y la contaminación', 'Agronomía');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7835, 56, 'Que no se respeten los derechos humanos', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7836, 56, 'La salud mental de la gente', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7837, 56, 'No me preocupo tanto, ya se verá', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7838, 56, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7839, 57, 'En el laboratorio haciendo experimentos', 'Ciencias Naturales');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7840, 57, 'En la clase de arte o música', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7841, 57, 'En debates o Model ONU', 'Derecho');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7842, 57, 'En el pompis o actividades deportivas', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7843, 57, 'En proyectos sociales o voluntariado', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7844, 57, 'En nada en particular, solo quería que termine', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7845, 57, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7846, 58, 'Tranquilo, con tiempo para mi familia y mis hobbies', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7847, 58, 'Exitoso, con mi propio negocio o empresa', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7848, 58, 'Viajero, conociendo el mundo y otras culturas', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7849, 58, 'De servicio, ayudando a quien más lo necesite', 'Salud');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7850, 58, 'Creativo, viviendo de mi arte o diseño', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7851, 58, 'No lo sé, todavía soy joven', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7852, 58, 'Ninguna de las anteriores', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7853, 59, 'Que piense en qué le gusta hacer, no en qué paga bien', 'Humanidades');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7854, 59, 'Que pruebe varias cosas antes de decidir', 'Neutral');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7855, 59, 'Que piense en cómo quiere ayudar al mundo', 'Salud Mental');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7856, 59, 'Que busque algo con futuro y estabilidad', 'Negocios');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7857, 59, 'Que siga su instinto, el corazón no falla', 'Arte y Diseño');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7858, 59, 'Que estudie algo de tecnología, siempre hay laburo', 'Tecnología');
INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, `texto_opcion`, `area_profesional`) VALUES (7859, 59, 'Ninguna de las anteriores', 'Neutral');

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
