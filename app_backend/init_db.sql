-- Lucas --> yo podria hacer esto

-- Caetano: dejo esto solo para probar el endpoint /partidos.
CREATE DATABASE IF NOT EXISTS prode;
USE prode;
CREATE TABLE partidos(
	ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	equipo_local VARCHAR(255) NOT NULL,
    equipo_visitante VARCHAR(255) NOT NULL,
    fecha TIMESTAMP NOT NULL,
    fase VARCHAR(100) NOT NULL,
    estadio VARCHAR(50) NOT NULL,
    sede VARCHAR(255) NOT NULL,
    FOREIGN KEY (equipo_local) REFERENCES equipos(ID),
    FOREIGN KEY (equipo_visitante) REFERENCES equipos(ID)
)

CREATE DATABASE IF NOT EXISTS prode;
USE prode;
CREATE TABLE equipos(
    ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    equipos VARCHAR(255) NOT NULL,
)

CREATE DATABASE IF NOT EXISTS prode;
USE prode;
CREATE TABLE predecciones(
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
    partidos_id INT UNIQUE NOT NULL,
    goles_local INT NOT NULL,
    goles_visitante INT NOT NULL,
    foreign key (partido_id) references partidos(ID) 
    
)

CREATE DATABASE IF NOT EXISTS prode;
USE prode;
CREATE TABLE usuarios(
    ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
)

-- santi 2 " falta agregar los INSERTS TO en todas las tablas para probar el funcionamiento del backend. "

-- santi 1 "al final para el ranking no hace falta db se hace con joins con las tablas q ya tenemos"
 --santi 1 -- lastrowid es el id del ultimo registro de la bd
            --santi 1 -- corregi algunas cosas de los ends y d la bd 14/04
