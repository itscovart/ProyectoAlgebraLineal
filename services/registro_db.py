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

def inicializar_bd():
    try:
        with pymysql.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                with open(SQL_FILE_PATH, 'r', encoding='utf8') as f:
                    sql_script = f.read()

                for statement in sql_script.split(';'):
                    statement = statement.strip()
                    if statement:
                        cursor.execute(statement)

                conn.commit()

    except FileNotFoundError:
        print(SQL_FILE_PATH)
    except Exception as e:
        print(e)

def registrar_resultado_prueba(data: Dict[str, Any], validacionesAD: list, validacionesM: list, validacionesD: list, validacionesBP: list, registrosDrive: list ) -> bool:
    try:
        inicializar_bd() 
        db_config_con_bd = DB_CONFIG.copy()
        db_config_con_bd["db"] = "railway"

        with pymysql.connect(**db_config_con_bd) as conn:
            with conn.cursor() as cursor:
                operacion = str(data.get("operacion", "DESCONOCIDA"))
                comentario_obj = data.get("comentario", None)

                comentario_str = (
                    json.dumps(comentario_obj, ensure_ascii=False)
                    if isinstance(comentario_obj, (dict, list))
                    else str(comentario_obj)
                )

                matriz_inicial_json = json.dumps(data.get("matriz_inicial", []), ensure_ascii=False)

                sql = """
                    INSERT INTO Prueba (
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
                        es_correcto,
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

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
                conn.commit()

        return True

    except Exception as e:
        print(e)
        return False