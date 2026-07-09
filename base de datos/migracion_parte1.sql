-- PARTE 1: Migraciones solicitadas por la tutora
-- Ejecutar con: mysql -u root -p futuro360 < "base de datos/migracion_parte1.sql"

-- CAMBIO 2: Agregar "Ninguna de las anteriores" a cada pregunta
INSERT INTO opciones_pregunta (pregunta_id, texto_opcion, area_profesional)
SELECT id, 'Ninguna de las anteriores', 'Neutral'
FROM preguntas
WHERE id NOT IN (
    SELECT DISTINCT pregunta_id FROM opciones_pregunta WHERE texto_opcion = 'Ninguna de las anteriores'
);

-- CAMBIO 3: Campo popular en carreras
ALTER TABLE carreras ADD COLUMN popular TINYINT(1) DEFAULT 0;

UPDATE carreras SET popular = 1 WHERE nombre IN (
    'Ingeniería en Sistemas de Información',
    'Medicina',
    'Psicología',
    'Abogacía',
    'Contador Público Nacional',
    'Ingeniería Civil',
    'Licenciatura en Administración',
    'Diseño Gráfico'
);
