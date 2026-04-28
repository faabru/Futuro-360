CREATE DATABASE IF NOT EXISTS futuro360;
USE futuro360;

-- Tabla de Usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'usuario') NOT NULL DEFAULT 'usuario',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Carreras
CREATE TABLE IF NOT EXISTS carreras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    area_profesional VARCHAR(100) NOT NULL
);

-- Tabla de Tests (Intentos realizados por los usuarios)
CREATE TABLE IF NOT EXISTS tests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    fecha_realizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla de Resultados (Asociados a un Test)
CREATE TABLE IF NOT EXISTS resultados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    test_id INT NOT NULL,
    area_profesional_sugerida VARCHAR(100) NOT NULL,
    detalle TEXT,
    notas_personales TEXT,
    FOREIGN KEY (test_id) REFERENCES tests(id) ON DELETE CASCADE
);

-- Insertar algunas carreras de ejemplo
INSERT INTO carreras (nombre, descripcion, area_profesional) VALUES
('Ingeniería en Sistemas', 'Diseño y desarrollo de software y hardware.', 'Tecnología'),
('Licenciatura en Psicología', 'Estudio de la mente y el comportamiento humano.', 'Salud Mental'),
('Administración de Empresas', 'Gestión y dirección de organizaciones.', 'Negocios'),
('Arquitectura', 'Diseño y construcción de espacios habitables.', 'Diseño'),
('Medicina', 'Estudio y práctica del cuidado de la salud.', 'Salud');

-- Tabla de Preguntas para el Test (opcional pero recomendada para dinamismo)
CREATE TABLE IF NOT EXISTS preguntas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    texto_pregunta VARCHAR(255) NOT NULL,
    area_profesional VARCHAR(100) NOT NULL
);

INSERT INTO preguntas (texto_pregunta, area_profesional) VALUES
('¿Te gusta resolver problemas lógicos y matemáticos?', 'Tecnología'),
('¿Te interesa entender cómo piensan las personas?', 'Salud Mental'),
('¿Te atrae la idea de liderar equipos de trabajo?', 'Negocios'),
('¿Disfrutas diseñando o dibujando planos y estructuras?', 'Diseño'),
('¿Sientes vocación por ayudar a personas enfermas?', 'Salud');

-- Tabla de Comentarios/Consultas
CREATE TABLE IF NOT EXISTS comentarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100),
    mensaje TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
