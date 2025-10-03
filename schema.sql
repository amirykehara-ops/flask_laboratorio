-- SQL schema for flask_laboratorio
CREATE DATABASE IF NOT EXISTS `flask_laboratorio` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `flask_laboratorio`;
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    rol ENUM('admin','usuario') NOT NULL DEFAULT 'usuario'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
