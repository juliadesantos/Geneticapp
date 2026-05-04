USE `geneticapp_desarrollo`;
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

INSERT INTO `Globales` -- data sintética de prueba
SET
    descripcion_larga = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    , descripcion_corta = 'Lorem ipsum dolor sit amet. Hecho con Ch''aska'
    , telefono = '{"cod_pais": "54", "cod_area": "11", "num": "12345678", "tel": "+54 11 12345678"}'
    , correo = 'contacto@geneticapp.ar'
    , domicilio = '{"pais": "AR", "provincia": "AR-C", "ciudad": "Buenos Aires", "direccion": {"calle": "Calle Falsa", "altura": "123", "cp": "A1234ABC"}}';