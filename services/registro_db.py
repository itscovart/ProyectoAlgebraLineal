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

def registrar_resultado_prueba(data: Dict[str, Any]) -> bool:
    try:
        inicializar_bd() 
        db_config_con_bd = DB_CONFIG.copy()
        db_config_con_bd["db"] = "railway"

        with pymysql.connect(**db_config_con_bd) as conn:
            with conn.cursor() as cursor:
                operacion = str(data.get("operacion", "DESCONOCIDA"))
                comentario_obj = data.get("comentario", None)

                matrices_pasos = data.get("matrices_pasos", [])
                if isinstance(matrices_pasos, (list, dict)):
                    num_pasos = len(matrices_pasos)
                else:
                    num_pasos = 1 if matrices_pasos else 0

                resultado_es_valido = comentario_obj is not None and "Error" not in str(comentario_obj)

                comentario_str = (
                    json.dumps(comentario_obj, ensure_ascii=False)
                    if isinstance(comentario_obj, (dict, list))
                    else str(comentario_obj)
                )

                matriz_inicial_json = json.dumps(data.get("matriz_inicial", []), ensure_ascii=False)

                sql = """
                    INSERT INTO Prueba (
                        operacion, 
                        resultado_es_valido, 
                        num_pasos, 
                        matriz_inicial_json, 
                        comentario_resultado
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """

                cursor.execute(
                    sql,
                    (
                        operacion,
                        resultado_es_valido,
                        num_pasos,
                        matriz_inicial_json,
                        comentario_str,
                    ),
                )
                conn.commit()

        return True

    except Exception as e:
        print(e)
        return False