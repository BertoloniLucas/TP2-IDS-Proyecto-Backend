CREATE DATABASE IF NOT EXISTS prode;
USE prode;
CREATE TABLE equipos(
    ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    equipo VARCHAR(255) NOT NULL,
)

CREATE DATABASE IF NOT EXISTS prode;
USE prode;
CREATE TABLE partidos(
	ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	equipo_local INT NOT NULL,
    equipo_visitante INT NOT NULL,
    fecha TIMESTAMP NOT NULL,
    fase VARCHAR(100) NOT NULL,
    estadio VARCHAR(50),
    sede VARCHAR(255),
    FOREIGN KEY (equipo_local) REFERENCES equipos(ID),
    FOREIGN KEY (equipo_visitante) REFERENCES equipos(ID)
)

CREATE DATABASE IF NOT EXISTS prode;
USE prode;
CREATE TABLE usuarios(
    ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
)

CREATE DATABASE IF NOT EXISTS prode;
USE prode;
CREATE TABLE predicciones(
    ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    partido_id INT NOT NULL,
    prediccion_local INT NOT NULL,
    prediccion_visitante INT NOT NULL,
    usuario_id INT NOT NULL,
    FOREIGN KEY (partido_id) REFERENCES partidos(ID)
    FOREIGN KEY (usuarios_id) REFERENCES usuarios(ID)
)

CREATE DATABASE IF NOT EXISTS prode;
USE prode;
CREATE TABLE resultados(
    ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    partido_id INT UNIQUE NOT NULL,
    goles_local INT NOT NULL,
    goles_visitante INT NOT NULL,
    foreign key (partido_id) references partidos(ID) 
)


-- INSERTS EJEMPLO:
use prode;
-- Anfitriones
INSERT INTO equipos (equipo) VALUES ('Canadá'), ('México'), ('Estados Unidos');
-- CONMEBOL (Sudamérica)
INSERT INTO equipos (equipo) VALUES ('Argentina'), ('Brasil'), ('Uruguay'), ('Colombia'), ('Ecuador'), ('Paraguay');
-- UEFA (Europa)
INSERT INTO equipos (equipo) VALUES ('Alemania'), ('Francia'), ('España'), ('Inglaterra'), ('Portugal'), ('Países Bajos'), 
('Bélgica'), ('Croacia'), ('Italia'), ('Austria'), ('Noruega'), ('Suecia'), ('Turquía'), ('República Checa'), ('Escocia'), ('Bosnia y Herzegovina');
-- CAF (África)
INSERT INTO equipos (equipo) VALUES ('Egipto'), ('Argelia'), ('Senegal'), ('Túnez'), ('Nigeria'), ('Marruecos'), ('Costa de Marfil'), ('Sudáfrica'), ('República Democrática del Congo'), ('Cabo Verde');
-- AFC (Asia)
INSERT INTO equipos (equipo) VALUES ('Japón'), ('Corea del Sur'), ('Irán'), ('Australia'), ('Arabia Saudita'), ('Qatar'), ('Irak'), ('Uzbekistán'), ('Jordania');
-- CONCACAF (Norte, Centroamérica y Caribe)
INSERT INTO equipos (equipo) VALUES ('Panamá'), ('Jamaica'), ('Haití'), ('Curazao');
-- OFC (Oceanía)
INSERT INTO equipos (equipo) VALUES ('Nueva Zelanda');
INSERT INTO equipos (equipo) VALUES 
('Argentinos Juniors'),('Atletico Tucumán'),
('Banfield'),('Barracas Central'),('Belgrano'),('Boca Juniors'),('Central Córdoba'),
('Defensa y Justicia'),('Deportivo Riestra'),('Estudiantes'),('Gimnasia'),('Godoy Cruz'),
('Huracan'),('Independiente'),('Independiente Rivadavia'),('Instituto'),('Lanus'),
('Newells Old Boys'),('Platense'),('Racing Club'),('River Plate'),('Rosario Central'),
('San Lorenzo'),('Sarmiento'),('Talleres'),('Tigre'),('Unión'),('Velez Sarsfield');

-- Insertar algunos usuarios de prueba (necesarios para tus predicciones luego)
INSERT INTO usuarios (nombre, email) VALUES 
('Admin', 'admin@prode.com'),
('Juan Perez', 'juan@gmail.com'),
('Lionel', 'leo@inter.com');

-- INSERT DE 30 PARTIDOS (Mundial 2026)
INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase, estadio, sede) VALUES
-- Jornada 1
(2, 4, '2026-06-11 15:00:00', 'Fase de Grupos', 'Estadio Azteca', 'Ciudad de México'),
(3, 5, '2026-06-12 18:00:00', 'Fase de Grupos', 'SoFi Stadium', 'Los Ángeles'),
(1, 6, '2026-06-12 20:00:00', 'Fase de Grupos', 'BMO Field', 'Toronto'),
(7, 8, '2026-06-13 13:00:00', 'Fase de Grupos', 'MetLife Stadium', 'Nueva Jersey'),
(9, 10, '2026-06-13 16:00:00', 'Fase de Grupos', 'Hard Rock Stadium', 'Miami'),
(11, 12, '2026-06-13 19:00:00', 'Fase de Grupos', 'NRG Stadium', 'Houston'),
(13, 14, '2026-06-14 12:00:00', 'Fase de Grupos', 'Gillette Stadium', 'Boston'),
(15, 16, '2026-06-14 15:00:00', 'Fase de Grupos', 'Lincoln Financial Field', 'Filadelfia'),
(17, 18, '2026-06-14 18:00:00', 'Fase de Grupos', 'Lumen Field', 'Seattle'),
(19, 20, '2026-06-15 14:00:00', 'Fase de Grupos', 'Levi\'s Stadium', 'San Francisco'),
-- Jornada 2
(2, 7, '2026-06-16 15:00:00', 'Fase de Grupos', 'Estadio Akron', 'Guadalajara'),
(3, 9, '2026-06-16 18:00:00', 'Fase de Grupos', 'AT&T Stadium', 'Dallas'),
(1, 11, '2026-06-17 20:00:00', 'Fase de Grupos', 'BC Place', 'Vancouver'),
(4, 8, '2026-06-17 13:00:00', 'Fase de Grupos', 'Mercedes-Benz Stadium', 'Atlanta'),
(5, 10, '2026-06-17 16:00:00', 'Fase de Grupos', 'Arrowhead Stadium', 'Kansas City'),
(6, 12, '2026-06-18 19:00:00', 'Fase de Grupos', 'Estadio BBVA', 'Monterrey'),
(13, 15, '2026-06-18 12:00:00', 'Fase de Grupos', 'Gillette Stadium', 'Boston'),
(14, 16, '2026-06-18 15:00:00', 'Fase de Grupos', 'MetLife Stadium', 'Nueva Jersey'),
(17, 19, '2026-06-19 18:00:00', 'Fase de Grupos', 'SoFi Stadium', 'Los Ángeles'),
(18, 20, '2026-06-19 14:00:00', 'Fase de Grupos', 'Lumen Field', 'Seattle'),
-- Jornada 3
(2, 10, '2026-06-20 15:00:00', 'Fase de Grupos', 'Estadio Azteca', 'Ciudad de México'),
(3, 12, '2026-06-20 18:00:00', 'Fase de Grupos', 'NRG Stadium', 'Houston'),
(1, 14, '2026-06-21 20:00:00', 'Fase de Grupos', 'BMO Field', 'Toronto'),
(7, 4, '2026-06-21 13:00:00', 'Fase de Grupos', 'Lincoln Financial Field', 'Filadelfia'),
(9, 5, '2026-06-21 16:00:00', 'Fase de Grupos', 'Hard Rock Stadium', 'Miami'),
(11, 6, '2026-06-22 19:00:00', 'Fase de Grupos', 'Arrowhead Stadium', 'Kansas City'),
(13, 17, '2026-06-22 12:00:00', 'Fase de Grupos', 'Levi\'s Stadium', 'San Francisco'),
(15, 18, '2026-06-22 15:00:00', 'Fase de Grupos', 'AT&T Stadium', 'Dallas'),
(16, 19, '2026-06-23 18:00:00', 'Fase de Grupos', 'Estadio BBVA', 'Monterrey'),
(8, 20, '2026-06-23 14:00:00', 'Fase de Grupos', 'Mercedes-Benz Stadium', 'Atlanta');
-- santi 2 " falta agregar los INSERTS TO en todas las tablas para probar el funcionamiento del backend. "

-- santi 1 "al final para el ranking no hace falta db se hace con joins con las tablas q ya tenemos"
 --santi 1 -- lastrowid es el id del ultimo registro de la bd
            --santi 1 -- corregi algunas cosas de los ends y d la bd 14/04
