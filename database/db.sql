-- Base de datos para almacenar pruebas y resultados de operaciones con matrices.
-- Cada registro corresponde a una ejecucion del sistema, con informacion visual, matematica y de validacion.

CREATE DATABASE IF NOT EXISTS `railway`;
USE `railway`;

-- Tabla principal donde se guardan las pruebas y parametros evaluados.
CREATE TABLE IF NOT EXISTS `Datos` (
  -- Informacion Operacion
  `id_prueba` INT NOT NULL AUTO_INCREMENT,
  `version`INT NOT NULL,
  `id_operacion` INT NOT NULL,
  `matriz_inicial_json` JSON NOT NULL,
  `imagen_matriz` TEXT,
  `tamaño_matriz` VARCHAR(11) NOT NULL,
  `operacion` VARCHAR(20) NOT NULL,
  `resultado` TEXT NULL,
  -- Parametros Intuitivo (Anti-Dumbs)
  `jerarquia_visual` BOOLEAN NOT NULL,
  `menu_visible_simple` BOOLEAN NOT NULL,
  `adaptabilidad_accesibilidad` BOOLEAN NOT NULL,
  `consistencia` BOOLEAN NOT NULL,
  `simplicidad_claridad` BOOLEAN NOT NULL,
  `prevencion_errores` BOOLEAN NOT NULL,
  -- Parametros Matematematico
  `matriz_cuadrada` BOOLEAN NOT NULL,
  `matriz_aumentada` BOOLEAN NOT NULL,
  `numero_filas` BOOLEAN NOT NULL,
  `numero_columnas` BOOLEAN NOT NULL,
  `factor` BOOLEAN NOT NULL,
  `pivote` BOOLEAN NOT NULL,
  `posicion_subindices_distintos` BOOLEAN NOT NULL,
  `terminos_independientes_matriz_aumentada` BOOLEAN NOT NULL,
  -- Parametros Diseño
  `dropbox_archivo` BOOLEAN NOT NULL,
  `operacion_realizar` BOOLEAN NOT NULL,
  -- Parametros Boom Proof
  `formato_archivo_txt` BOOLEAN NOT NULL,
  `unico_archivo` BOOLEAN NOT NULL,
  `filas_tamaño_iguales` BOOLEAN NOT NULL,
  `elementos_reales` BOOLEAN NOT NULL,
  `formato_correcto` BOOLEAN NOT NULL,
  -- Registros finales
  `link_imagen` TEXT NOT NULL,
  `segundo_link_imagen` TEXT,
  `es_correcto` BOOLEAN NOT NULL,
  `fecha_registro` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_prueba`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
