
import json
import requests

# URL de la API de Ximena y Ale
url_api = "https://relax-albatross-pessimism.ngrok-free.dev/urls"

# Nombre de tu archivo JSON donde guardaste las URLs de CFE
archivo_json = "links_cfe.json"

# 1. Cargar el archivo JSON guardado
try:
    with open(archivo_json, "r", encoding="utf-8") as archivo:
        contenido_json = json.load(archivo)
    
    print(f" Archivo '{archivo_json}' cargado correctamente. Total de URLs a enviar: {len(contenido_json.get('urls', []))}")

    # 2. Definir los encabezados requeridos (incluye la exención de ngrok)
    headers = {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "69420"
    }

    # 3. Enviar la petición POST
    print("Enviando enlaces a la API...")
    respuesta = requests.post(url_api, json=contenido_json, headers=headers, timeout=15)

    # 4. Mostrar resultados
    print(f" Estado HTTP: {respuesta.status_code}")
    print(f"Respuesta del servidor: {respuesta.text}")

    if respuesta.status_code == 200:
        print(" Enlaces enviados con éxito a Ximena y Ale.")
    else:
        print(" La API respondió pero con un estado distinto a 200.")

except FileNotFoundError:
    print(f" Error: El archivo '{archivo_json}' no existe todavía. Ejecuta primero tu script extractor.")
except json.JSONDecodeError:
    print(f" Error: El archivo '{archivo_json}' está vacío o mal formateado.")
except requests.RequestException as error:
    print(f" Error al conectar con la API: {error}")