"""
Funciones para inicializar la base de datos y registrar resultados de pruebas
realizadas en el sistema de Álgebra Lineal. Maneja conexión MySQL y escritura
de registros en la tabla Datos.
"""
import json
import pymysql
import os
from typing import Dict, Any
from dotenv import load_dotenv 

load_dotenv() 

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD",),
    "port": int(os.getenv("DB_PORT")),
    "cursorclass": pymysql.cursors.DictCursor
}

SQL_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'db.sql')

"""
Ejecuta el archivo SQL que crea la estructura de la base de datos.
Si la BD ya existe, simplemente asegura que las tablas estén creadas.
"""
def inicializar_bd():
    try:
        # Conectamos al servidor MySQL usando la configuración base (sin especificar DB aún).
        with pymysql.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                # Leemos el archivo SQL completo que contiene las sentencias CREATE TABLE.
                with open(SQL_FILE_PATH, 'r', encoding='utf8') as f:
                    sql_script = f.read()

                # Ejecutamos cada sentencia SQL por separado.
                for statement in sql_script.split(';'):
                    statement = statement.strip()
                    if statement:
                        cursor.execute(statement)

                # Guardamos los cambios realizados en la base de datos.
                conn.commit()

    except FileNotFoundError:
        print(SQL_FILE_PATH)
    except Exception as e:
        print(e)

"""
Inserta en la tabla Datos un registro completo con:
  - información de operación,
  - validaciones intuitivas, matemáticas y de diseño,
  - datos de Google Drive,
  - matriz inicial y resultado.
Devuelve True si el registro se almacena correctamente.
"""
def registrar_resultado_prueba(data: Dict[str, Any], validacionesAD: list, validacionesM: list, validacionesD: list, validacionesBP: list, registrosDrive: list ) -> bool:
    try:
        # Aseguramos que la BD y sus tablas estén listas antes de insertar.
        inicializar_bd() 
        # Creamos una copia de la configuración para agregar el nombre de la base de datos.
        db_config_con_bd = DB_CONFIG.copy()
        db_config_con_bd["db"] = "railway"

        # Conectamos directamente a la base de datos 'railway'.
        with pymysql.connect(**db_config_con_bd) as conn:
            with conn.cursor() as cursor:
                # Obtenemos el tipo de operación realizada (Determinante, Inversa, SEL, etc.).
                operacion = str(data.get("operacion", "DESCONOCIDA"))
                # Convertimos el comentario/resultado en string o JSON serializado.
                comentario_obj = data.get("comentario", None)

                comentario_str = (
                    json.dumps(comentario_obj, ensure_ascii=False)
                    if isinstance(comentario_obj, (dict, list))
                    else str(comentario_obj)
                )

                # Guardamos la matriz inicial como JSON para tener un registro exacto.
                matriz_inicial_json = json.dumps(data.get("matriz_inicial", []), ensure_ascii=False)

                # Sentencia INSERT con todos los campos definidos en la tabla Datos.
                sql = """
                    INSERT INTO Datos (
                        version,
                        id_operacion,
                        matriz_inicial_json, 
                        operacion, 
                        resultado,
                        jerarquia_visual,
                        menu_visible_simple,
                        adaptabilidad_accesibilidad,
                        consistencia,
                        simplicidad_claridad,
                        prevencion_errores,
                        matriz_cuadrada,
                        matriz_aumentada,
                        numero_filas,
                        numero_columnas,
                        factor,
                        pivote,
                        posicion_subindices_distintos,
                        terminos_independientes_matriz_aumentada,
                        dropbox_archivo,
                        operacion_realizar,
                        formato_archivo_txt,
                        unico_archivo,
                        filas_tamaño_iguales,
                        elementos_reales,
                        formato_correcto,
                        link_imagen,
                        segundo_link_imagen,
                        es_correcto
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                # Ejecutamos la inserción pasando todos los valores en el mismo orden que la tabla.
                cursor.execute(
                    sql,
                    (
                        os.getenv("VERSION"),
                        registrosDrive[0],
                        matriz_inicial_json,
                        operacion,
                        comentario_str,
                        validacionesAD[0],
                        validacionesAD[1],
                        validacionesAD[2],
                        validacionesAD[3],
                        validacionesAD[4],
                        validacionesAD[5],
                        validacionesM[0],
                        validacionesM[1],
                        validacionesM[2],
                        validacionesM[3],
                        validacionesM[4],
                        validacionesM[5],
                        validacionesM[6],
                        validacionesM[7],
                        validacionesD[0],
                        validacionesD[1],
                        validacionesBP[0],
                        validacionesBP[1],
                        validacionesBP[2],
                        validacionesBP[3],
                        validacionesBP[4],
                        registrosDrive[2],
                        registrosDrive[3],
                        registrosDrive[1],
                    ),
                )
                # Confirmamos la escritura en la base de datos.
                conn.commit()

        # Si todo sale bien, regresamos True indicando que el registro fue exitoso.
        return True

    # En caso de error, lo imprimimos y devolvemos False.
    except Exception as e:
        print(e)
        return False