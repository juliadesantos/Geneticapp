USE `geneticapp_desarrollo`;
CREATE TABLE IF NOT EXISTS `Enfermedad` (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT
    , fecha_carga TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    , fecha_modificacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    --
    , nombre VARCHAR(255) NOT NULL
    , gen_afectado VARCHAR(100)
    , tipo_herencia VARCHAR(100)
    , sintomas TEXT
);
