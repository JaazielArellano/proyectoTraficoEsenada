

import json
import requests

url_api = "https://relax-albatross-pessimism.ngrok-free.dev/urls"
archivo_json = "links_cfe.json"

try:
    with open(archivo_json, "r", encoding="utf-8") as archivo:
        contenido_json = json.load(archivo)
    
    lista_urls = contenido_json.get('urls', [])
    print(f"Archivo '{archivo_json}' cargado correctamente. Total de URLs a enviar: {len(lista_urls)}")

    # 1. Unimos todas las URLs en un solo texto separado por saltos de línea
    texto_urls_juntas = "\n".join(lista_urls)

    # 2. Preparamos el payload como un único mensaje o texto
    payload = {
        "mensaje": texto_urls_juntas
    }

    headers = {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "69420"
    }

    print("Enviando todos los enlaces juntos en un solo mensaje...")
    respuesta = requests.post(url_api, json=payload, headers=headers, timeout=15)

    print(f"Estado HTTP: {respuesta.status_code}")
    print(f"Respuesta del servidor: {respuesta.text}")

    if respuesta.status_code == 200:
        print("Enlaces enviados con éxito a Ximena y Ale.")
    else:
        print("La API respondió pero con un estado distinto a 200.")

except FileNotFoundError:
    print(f"Error: El archivo '{archivo_json}' no existe todavía.")
except json.JSONDecodeError:
    print(f"Error: El archivo '{archivo_json}' está vacío o mal formateado.")
except requests.RequestException as error:
    print(f"Error al conectar con la API: {error}")