CREATE DATABASE IF NOT EXISTS `railway`;
USE `railway`;

CREATE TABLE IF NOT EXISTS `Prueba` (
  `id_prueba` INT NOT NULL AUTO_INCREMENT,
  `operacion` VARCHAR(20) NOT NULL,
  `resultado_es_valido` BOOLEAN NOT NULL,
  `num_pasos` INT NOT NULL,
  `matriz_inicial_json` JSON NOT NULL,
  `comentario_resultado` TEXT NULL,
  `fecha_registro` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_prueba`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
