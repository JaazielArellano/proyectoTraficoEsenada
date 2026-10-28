"""Módulo para la gestión de conexiones a la base de datos PostgreSQL.

Lee las credenciales desde las variables de entorno (.env) y retorna
un objeto de conexión activo.
"""

DB_HOST=10.231.239.96
DB_PORT=5432
DB_NAME=postgres
DB_USER=apis
DB_PASSWORD=apis1


import os
import psycopg2
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()


def get_db_connection():
    """Establece y devuelve una conexión activa a PostgreSQL.

    Raises:
        psycopg2.Error: Si la conexión a la base de datos falla.

    Returns:
        psycopg2.extensions.connection: Objeto de conexión a PostgreSQL.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return conn
    except psycopg2.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        raise
