-- Script SQL amalgamado para crear la base de datos de pruebas
-- Generado automáticamente por Ch'astack
-- Este script debe ejecutarse con privilegios de root

-- 1. Crear base de datos de pruebas
CREATE DATABASE IF NOT EXISTS `geneticapp_pruebas`;

-- 2. Crear usuario de pruebas
CREATE USER IF NOT EXISTS 'geneticapp_test'@'localhost' IDENTIFIED BY 'pRU3b4s!geneticapp!1234';
CREATE USER IF NOT EXISTS 'geneticapp_test'@'%' IDENTIFIED BY 'pRU3b4s!geneticapp!1234';

-- 3. Otorgar privilegios
GRANT SELECT, UPDATE, DELETE, INSERT, EXECUTE, CREATE, DROP, ALTER
    ON `geneticapp_pruebas`.*
    TO 'geneticapp_test'@'localhost';
GRANT SELECT, UPDATE, DELETE, INSERT, EXECUTE, CREATE, DROP, ALTER
    ON `geneticapp_pruebas`.*
    TO 'geneticapp_test'@'%';

FLUSH PRIVILEGES;

-- 4. Usar base de datos de pruebas
USE `geneticapp_pruebas`;

-- 5. Deshabilitar foreign key checks para orden arbitrario
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================
-- TABLAS COPIADAS DESDE BDD DE DESARROLLO
-- ============================================

-- Tabla Globales (igual que desarrollo)
CREATE TABLE IF NOT EXISTS `Globales` (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT
    , fecha_carga TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    , fecha_modificacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    --
    , descripcion_larga TEXT
    , descripcion_corta VARCHAR(280)
    , telefono JSON
    , correo VARCHAR(75)
    , domicilio JSON
);

-- NOTA: Agregar aquí otras tablas del proyecto
-- Las tablas adicionales serán leídas desde bdd/*.sql

-- ============================================
-- DATOS SINTÉTICOS DE PRUEBA
-- ============================================
-- NOTA: Los archivos de bdd/.sintetico/*.sql se ejecutarán aquí
-- para poblar con datos de prueba

INSERT INTO `Globales`
SET
    descripcion_larga = 'Datos de prueba - Lorem ipsum dolor sit amet'
    , descripcion_corta = 'Proyecto de pruebas'
    , telefono = '{"cod_pais": "54", "cod_area" : "11", "num": "00000000", "tel": "+54 11 0000-0000"}'
    , correo = 'pruebas@geneticapp.test'
    , domicilio = '{"pais":"AR","provincia":"AR-C","ciudad":"Test City","direccion":{"calle":"Calle Test","altura":"123","cp":"T0000EST"}}';

-- 6. Rehabilitar foreign key checks
SET FOREIGN_KEY_CHECKS = 1;
