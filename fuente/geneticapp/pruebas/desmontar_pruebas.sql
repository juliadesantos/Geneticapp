-- Script SQL para eliminar la base de datos de pruebas
-- Generado automáticamente por Ch'astack
-- Este script debe ejecutarse con privilegios de root

-- 1. Eliminar base de datos de pruebas
DROP DATABASE IF EXISTS `geneticapp_pruebas`;

-- 2. Eliminar usuarios de pruebas
DROP USER IF EXISTS 'geneticapp_test'@'localhost';
DROP USER IF EXISTS 'geneticapp_test'@'%';

FLUSH PRIVILEGES;
