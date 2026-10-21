"""Módulo para el envío de URLs hacia la API del validador de peticiones.

Carga las URLs procesadas desde 'nuevas_urls.json' y las envía mediante
petición POST.
"""

import json
import os
import requests
from dotenv import load_dotenv

# Cargar las variables guardadas en el archivo de configuración .env
load_dotenv()

# Obtener la dirección web de la API desde las variables de entorno
URL_API_POST = os.getenv("URL_API_POST")


def enviar_peticion():
    """Lee el archivo con las nuevas URLs, se las envía al servidor y 
    retorna un objeto JSON."""
    # 1. Abrir y leer el archivo JSON que contiene las URLs recién extraídas
    try:
        with open("nuevas_urls.json", "r", encoding="utf-8") as archivo:
            contenido_json = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        # Retorna un objeto JSON indicando el fallo de lectura
        return {
            "status": "error",
            "message": f"No se pudo leer el archivo nuevas_urls.json: {error}",
            "data": None
        }

    # 2. Configurar la información de cabecera
    headers = {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "69420"
    }

    # 3. Enviar la información al servidor mediante una petición POST
    try:
        respuesta = requests.post(
            URL_API_POST, json=contenido_json, headers=headers, timeout=10
        )

        # 4. Convertir el texto del servidor a un objeto de python
        try:
            respuesta_servidor = respuesta.json()
        except ValueError:
            respuesta_servidor = respuesta.text

        # Retorna un objeto JSON con el resultado de la petición HTTP
        return {
            "status": "success" if respuesta.status_code == 200 else "fail",
            "status_code": respuesta.status_code,
            "response": respuesta_servidor
        }

    except requests.RequestException as error:
        # Retorna un objeto JSON capturando el error de conexión
        return {
            "status": "error",
            "status_code": None,
            "message": f"Error al conectar con la API: {error}"
        }


def ejecutar():
    """Función de enlace para main.py que retorna el objeto JSON devuelto por enviar_peticion."""
    resultado = enviar_peticion()
    return resultado


if __name__ == "__main__":
    # Al probar el script de forma individual, guardamos y mostramos el objeto devuelto
    resultado_json = ejecutar()
    print("Objeto JSON retornado:")
    print(resultado_json)
