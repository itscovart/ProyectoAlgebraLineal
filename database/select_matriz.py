"""
Script para consultar una imagen asociada a una matriz.
Si no existe, devuelve el siguiente valor numerico disponible.
"""

import os, json
import pymysql

MYSQL_HOST = os.getenv("DB_HOST", "127.0.0.1")
MYSQL_PORT = int(os.getenv("DB_PORT", "3306"))
MYSQL_USER = os.getenv("DB_USER", "root")
MYSQL_PASSWORD = os.getenv("DB_PASSWORD", "")
MYSQL_DB = os.getenv("DB_DATABASE", "railway")
MYSQL_TABLE = os.getenv("DB_TABLE", "Datos")

COLUMN_NAME = "imagen_matriz"

def _get_conn():
    """
    Crea y devuelve una conexion PyMySQL usando variables de entorno.
    """
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        # autocommit=True permite que cada consulta se confirme automaticamente.
        autocommit=True,
    )

def select_or_next_value(matriz: str):
    """
    Busca en la base de datos si la matriz ya tiene una imagen asociada.
    Si existe, la devuelve; si no, genera un nuevo numero incremental basado en el maximo existente.
    """
    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            # Consulta si ya existe un registro con esa matriz (comparacion JSON).
            sql_select = f"SELECT `{COLUMN_NAME}` FROM `{MYSQL_TABLE}` WHERE matriz_inicial_json = CAST(%s AS JSON)"
            cur.execute(sql_select, (matriz,))
            result = cur.fetchone()

            # Si encontro una imagen y no es NULL, la regresamos tal cual.
            if result and result[COLUMN_NAME] is not None:
                return result[COLUMN_NAME]
            else:
                # Si no hay imagen, buscamos el valor numerico mas alto usado hasta ahora.
                sql_max = f"SELECT MAX(CAST(`{COLUMN_NAME}` AS UNSIGNED)) AS max_val FROM `{MYSQL_TABLE}`"
                cur.execute(sql_max)
                max_result = cur.fetchone()

                # Si no existe ningun valor previo, empezamos desde 0.
                max_val = max_result["max_val"] if max_result and max_result["max_val"] is not None else 0
                # Regresamos el siguiente valor disponible.
                return max_val + 1
    finally:
        conn.close()