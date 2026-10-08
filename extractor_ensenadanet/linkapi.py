"""Código para subir URLs a la API de ngrok."""

import json
import requests

def enviar_enlaces():
    """Lee el JSON local, extrae los enlaces y los envía a la API del equipo."""
    # URL exacta de la API con su endpoint correspondiente
    url_api = "https://relax-albatross-pessimism.ngrok-free.dev/urls"

    # 1. Cargar el archivo JSON guardado
    with open("noticias_nuevas.json", "r", encoding="utf-8") as archivo:
        contenido_json = json.load(archivo)

    # 2. Definir los encabezados requeridos (incluye la exención de ngrok)
    headers = {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "69420"
    }

    # 3. Construir el payload con los puros links
    payload = {"urls": [n["url"] for n in contenido_json]}

    # 4. Enviar la petición POST
    try:
        respuesta = requests.post(
            url_api,
            json=payload,
            headers=headers,
            timeout=10
        )

        # 5. Mostrar resultados
        print(f"Estado HTTP: {respuesta.status_code}")
        print(f"Respuesta del servidor: {respuesta.text}")

    except requests.RequestException as error:
        print(f"Error al conectar con la API: {error}")
