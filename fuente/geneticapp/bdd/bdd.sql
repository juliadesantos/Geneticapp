CREATE DATABASE IF NOT EXISTS `geneticapp_desarrollo`;

CREATE USER IF NOT EXISTS 'servidor_local_geneticapp'@'localhost' IDENTIFIED BY 'S3rv1d0r@.geneticapp!';

GRANT SELECT
    ON geneticapp_desarrollo.*
    TO 'servidor_local_geneticapp'@'localhost';
GRANT UPDATE
    ON geneticapp_desarrollo.*
    TO 'servidor_local_geneticapp'@'localhost';
GRANT DELETE
    ON geneticapp_desarrollo.*
    TO 'servidor_local_geneticapp'@'localhost';
GRANT INSERT
    ON geneticapp_desarrollo.*
    TO 'servidor_local_geneticapp'@'localhost';
GRANT EXECUTE
    ON geneticapp_desarrollo.*
    TO 'servidor_local_geneticapp'@'localhost';

FLUSH PRIVILEGES;