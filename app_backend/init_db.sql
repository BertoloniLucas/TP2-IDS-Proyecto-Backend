-- Lucas --> yo podria hacer esto

-- Caetano: dejo esto solo para probar el endpoint /partidos.
CREATE DATABASE IF NOT EXISTS prode;
USE prode;
CREATE TABLE partidos(
	ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	equipo_local VARCHAR(255) NOT NULL, FOREIGN KEY (equipo_local) REFERENCES equipos(ID),
    equipo_visitante VARCHAR(255) NOT NULL,
    goles_local INT NOT NULL,
    goles_visitante INT NOT NULL,
    fecha TIMESTAMP NOT NULL,
    fase VARCHAR(100) NOT NULL
    estadio VARCHAR(50) NOT NULL
    sede VARCHAR(255) NOT NULL
)

CREATE DATABASE IF NOT EXISTS prode;
USE prode;
CREATE TABLE equipos(
    ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    equipo VARCHAR(255) NOT NULL,
)

CREATE DATABASE IF NOT EXISTS prode;
USE prode;
CREATE TABLE predecciones(
    ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    partido_id INT NOT NULL,
    equipo_local_goles INT NOT NULL,
    equipo_visitante_goles INT NOT NULL,
    usuario_id INT NOT NULL,
    FOREIGN KEY (partido_id) REFERENCES partidos(ID)

)

CREATE DATABASE IF NOT EXISTS prode;
USE prode;
CREATE TABLE ranking(
    ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    puntos INT NOT NULL
    foreign key (usuario_id) references usuarios(ID) 
    foreign key (puntos) references predecciones(equipo_local_goles, equipo_visitante_goles)
)

CREATE DATABASE IF NOT EXISTS prode;
USE prode;
CREATE TABLE usuarios(
    ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    usuario VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    padron VARCHAR(255) NOT NULL
)

-- santi 2 " falta agregar los INSERTS TO en todas las tablas para probar el funcionamiento del backend. "
