-- Lucas --> yo podria hacer esto

-- Caetano: dejo esto solo para probar el endpoint /partidos.
CREATE DATABASE IF NOT EXISTS prode;
USE prode;
CREATE TABLE partidos(
	ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	equipo_local VARCHAR(255) NOT NULL,
    equipo_visitante VARCHAR(255) NOT NULL,
    fecha TIMESTAMP NOT NULL,
    fase VARCHAR(100) NOT NULL
)
