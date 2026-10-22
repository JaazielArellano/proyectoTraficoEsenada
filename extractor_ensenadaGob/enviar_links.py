# Envía las noticias nuevas a la API.
import json
import requests

 # URL exacta de la API con su endpoint correspondiente
URL_API="https://relax-albatross-pessimism.ngrok-free.dev/urls"

# Cargar el archivo JSON guardado
with open("noticias_nuevas_ensenada.json","r",encoding="utf-8") as archivo:
    contenido_json =json.load(archivo)

headers = {   # Crea encabezados que se enviaran  con la peticion
    "Content-Type":"application/json",  # Los datos que se estan mandando tienen formato JSON
    "ngrok-skip-browser-warning":"69420"}

try:# Enviar la peticion POST
    respuesta=requests.post(URL_API,json=contenido_json,headers=headers,timeout=10)

# Muestra el codigo de respuesta / la peticion se hizo de forma correcta
    print(f"Estado HTTP:{respuesta.status_code}")
    # Muestra el mensaje de  respuesta del servidor
    print(f"Respuesta del servidor:{respuesta.text}")
     # Si ocurre un error relacionado con la conexion entra aqui

except requests.RequestException as error:
    print(f"Error al conectar con la API:{error}")
