import json
import requests

url_api = "https://relax-albatross-pessimism.ngrok-free.dev/urls"                              # URL exacta de la API con su endpoint correspondiente


with open("noticias_nuevas_ensenada.json", "r", encoding="utf-8") as archivo:                  # Cargar el archivo JSON guardado
    contenido_json = json.load(archivo)

headers = {                                                                                    # Definir los encabezados requeridos (incluye la exención de ngrok)
    "Content-Type": "application/json",
    "ngrok-skip-browser-warning": "69420"
}

try:
    respuesta = requests.post(url_api, json=contenido_json, headers=headers, timeout=10)        # Enviar la peticion POST

    print(f"Estado HTTP: {respuesta.status_code}")                                              # Mostrar resultados
    print(f"Respuesta del servidor: {respuesta.text}")
except requests.RequestException as error:
    print(f"Error al conectar con la API: {error}")
