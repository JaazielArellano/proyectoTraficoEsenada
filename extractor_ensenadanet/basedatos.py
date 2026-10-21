"""Módulo para guardar las noticias extraídas en PostgreSQL."""

import json
import psycopg2 # pylint: disable=import-error

def guardar_en_bd():
    """Lee noticias_nuevas.json e inserta los datos en alexis_datos."""
    with open("noticias_nuevas.json", "r", encoding="utf-8") as archivo:
        noticias = json.load(archivo)

    if not noticias:
        print("No hay noticias nuevas para guardar en la base de datos.")
        return

    try:

        conexion = psycopg2.connect(
            host="10.41.165.254",
            port="5432",
            database="postgres",
            user="alexis",
            password="alexis371"
        )
        cursor = conexion.cursor()

# Base de datos
        sql = """
            INSERT INTO public.alexis_datos (titulo, url, fecha_extraccion)
            VALUES (%s, %s, %s);
        """

        registros_insertados = 0
        for nota in noticias:
            valores = (
                nota["titulo"],
                nota["url"],
                nota["retrieved_at"]
            )
            cursor.execute(sql, valores) # Línea 39 que marcaba error
            registros_insertados += cursor.rowcount

        conexion.commit()
        cursor.close()
        conexion.close()
        print(f"Se guardaron {registros_insertados} noticias en alexis_datos.")

    except psycopg2.Error as error:
        print(f"Error al conectar o guardar en PostgreSQL: {error}")
