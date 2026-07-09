-- PARTE 2: Tabla game_carreras y sincronización con carreras existentes

CREATE TABLE IF NOT EXISTS game_carreras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    carrera_id INT NOT NULL,
    texto_boton VARCHAR(100) DEFAULT 'Ver carrera',
    titulo_card VARCHAR(150),
    descripcion_card TEXT,
    activo TINYINT(1) DEFAULT 1,
    orden INT DEFAULT 0,
    FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE
);

INSERT INTO game_carreras (carrera_id, titulo_card, descripcion_card, activo)
SELECT c.id, c.nombre, c.descripcion, 0
FROM carreras c
WHERE c.id NOT IN (SELECT carrera_id FROM game_carreras);
