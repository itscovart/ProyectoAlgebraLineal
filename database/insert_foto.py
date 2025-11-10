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
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )

def insert_imagen_link(url: str, matriz: str):
    sql = f"UPDATE `{MYSQL_TABLE}` SET `{COLUMN_NAME}` = %s WHERE matriz_inicial_json = CAST(%s AS JSON)"
    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (url, matriz))
    finally:
        conn.close()