"""
Script para actualizar en la base de datos el enlace de una imagen asociada
a una matriz inicial. Se conecta a MySQL y actualiza un campo especifico.
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

def insert_imagen_link(url: str, matriz: str):
    """
    Actualiza el campo 'imagen_matriz' para la fila cuya matriz_inicial_json
    coincide con el JSON dado.
    """
    # Construimos la consulta UPDATE usando CAST para comparar JSON.
    sql = f"UPDATE `{MYSQL_TABLE}` SET `{COLUMN_NAME}` = %s WHERE matriz_inicial_json = CAST(%s AS JSON)"
    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            # Ejecutamos la actualizacion pasando los parametros seguros.
            cur.execute(sql, (url, matriz))
    finally:
        conn.close()