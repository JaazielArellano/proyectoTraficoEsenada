import requests
import json
import os

API_URL = "https://relax-albatross-pessimism.ngrok-free.dev/urls"

def enviar_a_api():
    #Obtener la ruta de la carpeta donde se encuentra este archivo
    directorio_actual = os.path.dirname(__file__)
    ruta_json = os.path.join(directorio_actual, "cespe_links.json")

    # Cargar todos los enlaces guardados en un solo JSON 
    with open(ruta_json, "r", encoding="utf-8") as f:
        enlaces = json.load(f)

    if not enlaces:
        print("No hay enlaces para enviar.")
        return

    # Enviar TODOS los enlaces juntos en un solo JSON
    payload = {"urls": enlaces}  # clave 'urls' con la lista completa
    respuesta = requests.post(API_URL, json=payload)

    if respuesta.status_code == 200:
        print("✅ Todos los enlaces enviados correctamente en un solo JSON")
    else:
        print(f"❌ Error al enviar -> Código {respuesta.status_code}")

# Ejecutar la verificación
if __name__ == "__main__":
    enviar_a_api()
