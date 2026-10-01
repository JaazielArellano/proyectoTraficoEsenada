import json
import requests

# URL de la API
url_api = "https://relax-albatross-pessimism.ngrok-free.dev/urls"

# Archivo JSON original
archivo_json = "links_cfe.json"

try:
    # 1. Cargar el JSON que ya contiene {"urls": ["https://...", "https://..."]}
    with open(archivo_json, "r", encoding="utf-8") as archivo:
        payload = json.load(archivo)
    
    total_urls = len(payload.get('urls', []))
    print(f"Archivo '{archivo_json}' cargado correctamente. Total de URLs: {total_urls}")

    headers = {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "69420"
    }

    # 2. Enviar el objeto JSON directamente en un solo envío POST
    print("Enviando todas las URLs juntas a la API...")
    respuesta = requests.post(url_api, json=payload, headers=headers, timeout=15)

    # 3. Verificar respuesta
    print(f"Estado HTTP: {respuesta.status_code}")
    print(f"Respuesta del servidor: {respuesta.text}")

    if respuesta.status_code in (200, 201):
        print("¡Enlaces enviados con éxito!")
    else:
        print("La API devolvió un estado inesperado.")

except FileNotFoundError:
    print(f"Error: El archivo '{archivo_json}' no fue encontrado.")
except json.JSONDecodeError:
    print(f"Error: El archivo '{archivo_json}' no tiene un formato JSON válido.")
except requests.RequestException as error:
    print(f"Error en la petición HTTP: {error}")