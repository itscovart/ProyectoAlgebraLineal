import os
import pymysql

# Lee conexión de variables de entorno
MYSQL_HOST = os.getenv("DB_HOST", "127.0.0.1")
MYSQL_PORT = int(os.getenv("DB_PORT", "3306"))
MYSQL_USER = os.getenv("DB_USER", "root")
MYSQL_PASSWORD = os.getenv("DB_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "railway")
MYSQL_TABLE = os.getenv("MYSQL_TABLE", "Datos")

# La columna queda fija como pediste:
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

def insert_imagen_link(url: str):
    """
    Inserta SOLO el link en la columna 'imagen_matriz' de tu tabla.
    Ajusta MYSQL_TABLE desde env var (MYSQL_TABLE).
    """
    sql = f"INSERT INTO `{MYSQL_TABLE}` (`{COLUMN_NAME}`) VALUES (%s)"
    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (url,))
    finally:
        conn.close()