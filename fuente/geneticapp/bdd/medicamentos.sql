USE `geneticapp_desarrollo`;
CREATE TABLE IF NOT EXISTS `Medicamento` (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT
    , fecha_carga TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    , fecha_modificacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    --
    , nombre VARCHAR(255) NOT NULL
    , principio_activo VARCHAR(255)
    , dosis VARCHAR(100)
    , enfermedad_id INT NOT NULL
    , FOREIGN KEY (enfermedad_id) REFERENCES Enfermedad(id) ON DELETE CASCADE
);
