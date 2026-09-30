"""Módulo para el envío de URLs hacia la API del validador de peticiones.

Carga las URLs procesadas desde 'nuevas_urls.json' y las envía mediante
petición POST.
"""

import json
import requests

# URL exacta de la API con su endpoint correspondiente (nombre en MAYÚSCULAS)
URL_API = "https://relax-albatross-pessimism.ngrok-free.dev/urls"


def enviar_peticion():
    """Carga el JSON local y realiza el envío POST hacia la API."""
    # 1. Cargar el archivo JSON guardado
    with open("nuevas_urls.json", "r", encoding="utf-8") as archivo:
        contenido_json = json.load(archivo)

    # 2. Definir los encabezados requeridos (incluye la exención de ngrok)
    headers = {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "69420"
    }

    # 3. Enviar la petición POST
    try:
        respuesta = requests.post(
            URL_API, json=contenido_json, headers=headers, timeout=10
        )

        # 4. Mostrar resultados
        print(f"Estado HTTP: {respuesta.status_code}")
        print(f"Respuesta del servidor: {respuesta.text}")

    except requests.RequestException as error:
        print(f"Error al conectar con la API: {error}")


if __name__ == "__main__":
    enviar_peticion()
