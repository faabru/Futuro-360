-- ═══════════════════════════════════════════════════════════
-- SQL: Cargar imagen_portada e imagen_principal en carreras
-- Rutas relativas desde static/ para usar con url_for('static', filename=...)
-- Nombres de archivo EXACTOS según el filesystem (static/imagenes/)
-- ═══════════════════════════════════════════════════════════

-- AGRONOMÍA
UPDATE carreras SET
  imagen_portada    = 'imagenes/agronomia-ingenieria agronomica -portada.jpg',
  imagen_principal  = 'imagenes/agronomia-ingenieria agronomica -principal.jpg'
WHERE nombre = 'Ingeniería Agronómica';

UPDATE carreras SET
  imagen_portada    = 'imagenes/agronomia-ingenieria forestal -portada.jpg',
  imagen_principal  = 'imagenes/agronomia-ingenieria forestal -principal.jpg'
WHERE nombre = 'Ingeniería Forestal';

UPDATE carreras SET
  imagen_portada    = 'imagenes/agronomia-medicina veterinaria-portada.jpg',
  imagen_principal  = 'imagenes/agronomia-medicina veterinaria-principal.jpg'
WHERE nombre = 'Medicina Veterinaria';

UPDATE carreras SET
  imagen_portada    = 'imagenes/agronomia-Tecnicatura en Producción Agropecuaria-portada.jpg',
  imagen_principal  = 'imagenes/agronomia-Tecnicatura en Producción Agropecuaria-principal.jpg'
WHERE nombre = 'Tecnicatura en Producción Agropecuaria';

-- ARTE Y DISEÑO
UPDATE carreras SET
  imagen_portada    = 'imagenes/arte y diseño-arquitectura-portada.jpg',
  imagen_principal  = 'imagenes/arte y diseño-arquitectura-principal.jpg'
WHERE nombre = 'Arquitectura';

UPDATE carreras SET
  imagen_portada    = 'imagenes/arte y diseño-diseño grafico-portada.jpg',
  imagen_principal  = 'imagenes/arte y diseño-diseño grafico-principal.jpg'
WHERE nombre = 'Diseño Gráfico';

UPDATE carreras SET
  imagen_portada    = 'imagenes/arte y diseño-Licenciatura en Artes Visuales-portada.jpg',
  imagen_principal  = 'imagenes/arte y diseño-Licenciatura en Artes Visuales-principal.jpg'
WHERE nombre = 'Licenciatura en Artes Visuales';

UPDATE carreras SET
  imagen_portada    = 'imagenes/arte y diseño-musica-portada.jpg',
  imagen_principal  = 'imagenes/arte y diseño-musica-principal.jpg'
WHERE nombre = 'Música';

-- CIENCIAS NATURALES
UPDATE carreras SET
  imagen_portada    = 'imagenes/ciencias naturales-biologia-portada.jpg',
  imagen_principal  = 'imagenes/ciencias naturales-biologia-principal.jpg'
WHERE nombre = 'Biología';

UPDATE carreras SET
  imagen_portada    = 'imagenes/ciencias naturales-geologia-portada.jpg',
  imagen_principal  = 'imagenes/ciencias naturales-geologia-principal.jpg'
WHERE nombre = 'Geología';

UPDATE carreras SET
  imagen_portada    = 'imagenes/ciencias naturales-quimica-portada.jpg',
  imagen_principal  = 'imagenes/ciencias naturales-quimica-principal.jpg'
WHERE nombre = 'Química';

-- COMUNICACIÓN
UPDATE carreras SET
  imagen_portada    = 'imagenes/comunicación-Licenciatura en Comunicación Social-portada.jpg',
  imagen_principal  = 'imagenes/comunicación-Licenciatura en Comunicación Social-principal.jpg'
WHERE nombre = 'Licenciatura en Comunicación Social';

UPDATE carreras SET
  imagen_portada    = 'imagenes/comunicación-periodismo-portada.jpg',
  imagen_principal  = 'imagenes/comunicación-periodismo-principal.jpg'
WHERE nombre = 'Periodismo';

UPDATE carreras SET
  imagen_portada    = 'imagenes/comunicación-publicidad-portada.jpg',
  imagen_principal  = 'imagenes/comunicación-publicidad-principal.jpg'
WHERE nombre = 'Publicidad';

-- DERECHO
UPDATE carreras SET
  imagen_portada    = 'imagenes/derecho-abogacia-portada.jpg',
  imagen_principal  = 'imagenes/derecho-abogacia-principal.jpg'
WHERE nombre = 'Abogacía';

UPDATE carreras SET
  imagen_portada    = 'imagenes/derecho-ciencias politicas-portada.jpg',
  imagen_principal  = 'imagenes/derecho-ciencias politicas-principal.jpg'
WHERE nombre = 'Ciencias Políticas';

UPDATE carreras SET
  imagen_portada    = 'imagenes/derecho-notariado-portada.jpg',
  imagen_principal  = 'imagenes/derecho-notariado-principal.jpg'
WHERE nombre = 'Notariado';

-- HUMANIDADES
UPDATE carreras SET
  imagen_portada    = 'imagenes/humanidades-licenciatura en filosofia-portada.jpg',
  imagen_principal  = 'imagenes/humanidades-licenciatura en filosofia-principal.jpg'
WHERE nombre = 'Licenciatura en Filosofía';

-- INGENIERÍA
UPDATE carreras SET
  imagen_portada    = 'imagenes/ingenieria-ingenieria civil-portada.jpg',
  imagen_principal  = 'imagenes/ingenieria-ingenieria civil-principal.jpg'
WHERE nombre = 'Ingeniería Civil';

UPDATE carreras SET
  imagen_portada    = 'imagenes/ingenieria-ingenieria electrica-portada.jpg',
  imagen_principal  = 'imagenes/ingenieria-ingenieria electrica-principal.jpg'
WHERE nombre = 'Ingeniería Eléctrica';

UPDATE carreras SET
  imagen_portada    = 'imagenes/ingenieria-ingenieria industrial-portada.jpg',
  imagen_principal  = 'imagenes/ingenieria-ingenieria industrial-principal.jpg'
WHERE nombre = 'Ingeniería Industrial';

UPDATE carreras SET
  imagen_portada    = 'imagenes/ingenieria-ingenieria mecanica-portada.jpg',
  imagen_principal  = 'imagenes/ingenieria-ingenieria mecanica-principal.jpg'
WHERE nombre = 'Ingeniería Mecánica';

UPDATE carreras SET
  imagen_portada    = 'imagenes/ingenieria-ingenieria quimica-portada.jpg',
  imagen_principal  = 'imagenes/ingenieria-ingenieria quimica-principal.jpg'
WHERE nombre = 'Ingeniería Química';

-- NEGOCIOS
UPDATE carreras SET
  imagen_portada    = 'imagenes/negocios-contador publico nacional-portada.jpg',
  imagen_principal  = 'imagenes/negocios-contador publico nacional-principal.jpg'
WHERE nombre = 'Contador Público Nacional';

UPDATE carreras SET
  imagen_portada    = 'imagenes/negocios-licenciatura en administracion-portada.jpg',
  imagen_principal  = 'imagenes/negocios-licenciatura en administracion-principal.jpg'
WHERE nombre = 'Licenciatura en Administración';

UPDATE carreras SET
  imagen_portada    = 'imagenes/negocios-licenciatura en economia-portada.jpg',
  imagen_principal  = 'imagenes/negocios-licenciatura en economia-principal.jpg'
WHERE nombre = 'Licenciatura en Economía';

UPDATE carreras SET
  imagen_portada    = 'imagenes/negocios-marketing digital-portada.jpg',
  imagen_principal  = 'imagenes/negocios-marketing digital-principal.jpg'
WHERE nombre = 'Marketing Digital';

-- SALUD MENTAL
UPDATE carreras SET
  imagen_portada    = 'imagenes/salud mental-Psicología-portada.jpg',
  imagen_principal  = 'imagenes/salud mental-Psicología-principal.jpg'
WHERE nombre = 'Psicología';

-- SALUD
UPDATE carreras SET
  imagen_portada    = 'imagenes/salud-Kinesiología y Fisioterapia-portada.jpg',
  imagen_principal  = 'imagenes/salud-Kinesiología y Fisioterapia-principal.jpg'
WHERE nombre = 'Kinesiología y Fisioterapia';

UPDATE carreras SET
  imagen_portada    = 'imagenes/salud-bioquimica-portada.jpg',
  imagen_principal  = 'imagenes/salud-bioquimica-principal.jpg'
WHERE nombre = 'Bioquímica';

UPDATE carreras SET
  imagen_portada    = 'imagenes/salud-enfermeria-portada.jpg',
  imagen_principal  = 'imagenes/salud-enfermeria-principal.jpg'
WHERE nombre = 'Enfermería';

UPDATE carreras SET
  imagen_portada    = 'imagenes/salud-farmacia-portada.jpg',
  imagen_principal  = 'imagenes/salud-farmacia-principal.jpg'
WHERE nombre = 'Farmacia';

UPDATE carreras SET
  imagen_portada    = 'imagenes/salud-medicina-portada.jpg',
  imagen_principal  = 'imagenes/salud-medicina-principal.jpg'
WHERE nombre = 'Medicina';

UPDATE carreras SET
  imagen_portada    = 'imagenes/salud-nutrición-portada.jpg',
  imagen_principal  = 'imagenes/salud-nutrición-principal.jpg'
WHERE nombre = 'Nutrición';

UPDATE carreras SET
  imagen_portada    = 'imagenes/salud-odontologia-portada.jpg',
  imagen_principal  = 'imagenes/salud-odontologia-principal.jpg'
WHERE nombre = 'Odontología';

-- TECNOLOGÍA
UPDATE carreras SET
  imagen_portada    = 'imagenes/tecnologia-Ingeniería en Sistemas de Información-portada.jpg',
  imagen_principal  = 'imagenes/tecnologia-Ingeniería en Sistemas de Información-principal.jpg'
WHERE nombre = 'Ingeniería en Sistemas de Información';

UPDATE carreras SET
  imagen_portada    = 'imagenes/tecnologia-Licenciatura en Sistemas de Información-portada.jpg',
  imagen_principal  = 'imagenes/tecnologia-Licenciatura en Sistemas de Información-principal.jpg'
WHERE nombre = 'Licenciatura en Sistemas de Información';

UPDATE carreras SET
  imagen_portada    = 'imagenes/tecnologia-Tecnicatura en Programación-portada.jpg',
  imagen_principal  = 'imagenes/tecnologia-Tecnicatura en Programación-principal.jpg'
WHERE nombre = 'Tecnicatura en Programación';

-- Verificación final
SELECT id, nombre, imagen_portada, imagen_principal
FROM carreras
WHERE imagen_portada IS NOT NULL
ORDER BY nombre;
