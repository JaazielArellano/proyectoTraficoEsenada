import json
import os
import re
import requests

RUTA_FUENTE = "https://x.com/EnsenadaNews"
RUTA_ARCHIVO = "links_extraidos.json"

#URL de la API
URL_API = "https://relax-albatross-pessimism.ngrok-free.dev/urls"


def extractor_links_twitter(url_fuente: str, limite: int = 15) -> list:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    }

    lista_links = []

    try:
        respuesta = requests.get(url_fuente, headers=headers, timeout=10)
        print(f"Estado de la respuesta HTTP (X): {respuesta.status_code}")

        if respuesta.status_code == 200:
            texto_html = respuesta.text

            coincidencias = re.findall(
                r"/(?:[a-zA-Z0-9_]+)/status/(\d+)", texto_html
            )

            for tweet_id in coincidencias:
                link_oficial = f"https://x.com/i/web/status/{tweet_id}"
                if link_oficial not in lista_links:
                    lista_links.append(link_oficial)
                if len(lista_links) >= limite:
                    break

    except requests.RequestException as error:
        print(f"Error de conexión con X: {error}")

    return lista_links


def cargar_historial_existente(ruta_archivo=RUTA_ARCHIVO) -> set:
    if os.path.exists(ruta_archivo):
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

                if isinstance(datos, dict):
                    return set(datos.get("urls_historial", []))

                elif isinstance(datos, list):
                    return set(datos)
        except (json.JSONDecodeError, IOError):
            return set()
    return set()


def enviar_urls_a_api(urls: list):
    if not urls:
        print("No hay URLs para enviar a la API.")
        return

    payload = {"urls": urls}

    headers = {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "69420",
    }

    try:
        print(f"Enviando {len(urls)} URL(s) a la API...")
        print(f"Payload enviado: {json.dumps(payload, ensure_ascii=False)}")

        respuesta = requests.post(
            URL_API, json=payload, headers=headers, timeout=10
        )

        print(f"Estado HTTP de la API: {respuesta.status_code}")
        print(f"Respuesta del servidor: {respuesta.text}")

    except requests.RequestException as error:
        print(f"Error al conectar con la API: {error}")


if __name__ == "__main__":
    print("Iniciando extracción para X...")
    print(f"Fuente objetivo: {RUTA_FUENTE}\n")

    #Carga historial previo de links_extraidos.json
    historial_previo = cargar_historial_existente()

    #Intenta extraer URLs desde el HTML
    urls_obtenidas = extractor_links_twitter(RUTA_FUENTE, limite=15)

    #Filtra URLs nuevas que no estén en el historial
    urls_nuevas = [
        url for url in urls_obtenidas if url not in historial_previo
    ]

    print("Resumen de extracción")
    print(f"Links en historial previo: {len(historial_previo)}")
    print(f"Links totalmente nuevos: {len(urls_nuevas)}")

    #Envia nuevos links a la API de tu compañera
    if urls_nuevas:
        enviar_urls_a_api(urls_nuevas)
    else:
        print("No hay enlaces nuevos para enviar.")

    #Guarda/Actualiza el archivo JSON
    historial_actualizado = list(historial_previo.union(set(urls_nuevas)))

    resultado_json = {
        "source": RUTA_FUENTE,
        "query": "Noticias Ensenada",
        "total_extracted": len(urls_obtenidas),
        "urls_nuevas": urls_nuevas,
        "urls_historial": historial_actualizado,
    }

    with open(RUTA_ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(resultado_json, archivo, ensure_ascii=False, indent=4)

    print(f"Archivo '{RUTA_ARCHIVO}' actualizado.")