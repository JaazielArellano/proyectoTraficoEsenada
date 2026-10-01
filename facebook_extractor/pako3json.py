import json
import os
import requests

# --- CONFIGURACIÓN ---
ARCHIVO_CACHE = "noticias_facebook.json"
URL_API_NGROK = "https://relax-albatross-pessimism.ngrok-free.dev/urls"
# IMPORTANTE: Cambia esta API key, la que tenías ya quedó expuesta
MI_APIFY_TOKEN = "apify_api_Cm5bfgiXp5vR7iB2bE5H3hTCVrwhyG2POehT"


def cargar_cache(nombre_archivo):
    """Carga los enlaces guardados previamente si el archivo existe."""
    if os.path.exists(nombre_archivo):
        try:
            with open(nombre_archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
                return set(datos.get("links", []))
        except (json.JSONDecodeError, IOError):
            print("No se pudo leer el cache existente. Se iniciará un cache nuevo.")
            return set()
    return set()


def guardar_cache(nombre_archivo, set_links):
    """Guarda la lista acumulada de enlaces únicos en el archivo JSON."""
    lista_ordenada = list(set_links)
    datos_json = {
        "total": len(lista_ordenada),
        "fuente": "Facebook - Gobierno de Ensenada",
        "links": lista_ordenada,
    }
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        json.dump(datos_json, f, ensure_ascii=False, indent=4)


def extractor_facebook_apify(token_apify, limite=20):
    endpoint = f"https://api.apify.com/v2/acts/apify~facebook-posts-scraper/run-sync-get-dataset-items?token={token_apify}"
    payload = {
        "startUrls": [{"url": "https://www.facebook.com/GobiernoDeEnsenada"}],
        "resultsLimit": limite,
    }

    print("1. Enviando petición a Apify (extrayendo publicaciones)...")
    respuesta = requests.post(endpoint, json=payload, timeout=60)

    if respuesta.status_code in [200, 201]:
        items = respuesta.json()
        nuevos_links = []

        for item in items:
            url = (
                item.get("url") or item.get("postUrl") or item.get("canonicalUrl")
            )
            if url:
                url_limpia = url.split("?")[0].split("&")[0]
                nuevos_links.append(url_limpia)

        return nuevos_links
    else:
        print(f"Error Apify {respuesta.status_code}: {respuesta.text}")
        return []


def enviar_a_ngrok(payload_datos):
    """Envía la payload con URLs a tu API ngrok."""
    headers = {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "69420",
    }
    print("3. Enviando nuevos enlaces a la API en ngrok...")
    try:
        respuesta = requests.post(
            URL_API_NGROK, json=payload_datos, headers=headers, timeout=10
        )
        print(f"   Estado HTTP: {respuesta.status_code}")
        print(f"   Respuesta Servidor: {respuesta.text}")
    except requests.RequestException as error:
        print(f"   Error al conectar con la API ngrok: {error}")


# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    # 1. Cargar cache
    cache_links = cargar_cache(ARCHIVO_CACHE)
    print(f"Enlaces en cache previo: {len(cache_links)}")

    # 2. Extraer de Apify
    links_obtenidos = extractor_facebook_apify(MI_APIFY_TOKEN, limite=20)

    # 3. Filtrar solo los enlaces realmente NUEVOS
    links_nuevos = [
        link for link in links_obtenidos if link not in cache_links
    ]

    if links_obtenidos:
        # Actualizar el archivo de caché histórico
        cache_links.update(links_obtenidos)
        guardar_cache(ARCHIVO_CACHE, cache_links)

        print(f"\n¡Extracción exitosa!")
        print(f"- Nuevos enlaces encontrados hoy: {len(links_nuevos)}")
        print(
            f"- Total acumulado en '{ARCHIVO_CACHE}': {len(cache_links)}\n"
        )

        # 4. Enviar a ngrok SOLO si hay URLs nuevas
        if links_nuevos:
            payload_para_api = {
                "fuente": "Facebook - Gobierno de Ensenada",
                "total_nuevos": len(links_nuevos),
                "urls": links_nuevos,
            }

            enviar_a_ngrok(payload_para_api)
        else:
            print("No hay enlaces nuevos para enviar a la API ngrok.")
    else:
        print("No se pudieron obtener enlaces desde la API de Apify.")