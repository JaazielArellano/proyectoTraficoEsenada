import json
import os
import requests

RUTA_FUENTE = "https://x.com/EnsenadaNews"
RUTA_ARCHIVO = "links_extraidos.json"
URL_API = "https://relax-albatross-pessimism.ngrok-free.dev/urls"


def extraer_ids_tweets(texto_html):
    """
    Recibe el contenido HTML de la página y extrae los identificadores 
    numéricos de los tuits buscando coincidencias tras '/status/'.
    """
    ids_encontrados = []

    # Divide el HTML en partes cada vez que encuentra '/status/'
    partes = texto_html.split("/status/")

    # Recorre cada fragmento descartando el encabezado previo
    for parte in partes[1:]:
        tweet_id = ""

        # Lee cada caracter hasta que deja de encontrar números
        for caracter in parte:
            if caracter.isdigit():
                tweet_id += caracter
            else:
                break

        # Si se extrajo un ID válido y no está repetido en la lista actual, se agrega
        if tweet_id and tweet_id not in ids_encontrados:
            ids_encontrados.append(tweet_id)

    return ids_encontrados


def extractor_links_twitter(url_fuente: str, limite: int = 15):
    """
    Realiza la petición HTTP GET a la página pública de X, 
    obtiene los IDs de los tuits y genera una lista de enlaces completos.
    """
    headers = {
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    }

    lista_links = []

    try:
        # Hace la solicitud GET a la URL pública de la cuenta
        respuesta = requests.get(
            url_fuente,
            headers=headers,
            timeout=10
        )

        print(
            f"Estado de la respuesta HTTP (X): "
            f"{respuesta.status_code}"
        )

        # Si la respuesta es exitosa procesa el HTML
        if respuesta.status_code == 200:
            texto_html = respuesta.text
            coincidencias = extraer_ids_tweets(texto_html)

            # Reconstruye los enlaces oficiales a partir de los IDs
            for tweet_id in coincidencias:
                link_oficial = f"https://x.com/i/web/status/{tweet_id}"

                if link_oficial not in lista_links:
                    lista_links.append(link_oficial)

                # Detiene la recolección si se alcanza el límite solicitado
                if len(lista_links) >= limite:
                    break

    except requests.RequestException as error:
        print(f"Error de conexión con X: {error}")

    return lista_links


def cargar_historial_existente(ruta_archivo=RUTA_ARCHIVO) -> set:
    """
    Lee el archivo JSON local si existe y retorna un conjunto (set) 
    con las URLs registradas previamente para búsquedas rápidas.
    """
    if os.path.exists(ruta_archivo):
        try:
            with open(
                ruta_archivo,
                "r",
                encoding="utf-8"
            ) as archivo:
                datos = json.load(archivo)

                # Si el JSON guardado tiene estructura de diccionario
                if isinstance(datos, dict):
                    return set(datos.get("urls_historial", []))

                # Si el JSON guarda directamente una lista
                elif isinstance(datos, list):
                    return set(datos)

        except (json.JSONDecodeError, IOError):
            # Si el archivo está dañado o vacío, retorna un conjunto vacío
            return set()

    return set()


def enviar_urls_a_api(urls: list):
    """
    Envía las URLs nuevas detectadas a un webhook/API externo 
    en formato JSON.
    """
    if not urls:
        print("No hay URLs para enviar a la API.")
        return

    payload = {
        "urls": urls
    }


    headers = {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "69420",
    }

    try:
        print(f"Enviando {len(urls)} URL(s) a la API...")
        print(f"Payload enviado: {json.dumps(payload, ensure_ascii=False)}")

        # Envío del arreglo de enlaces por POST a la API
        respuesta = requests.post(
            URL_API,
            json=payload,
            headers=headers,
            timeout=10
        )

        print(f"Estado HTTP de la API: {respuesta.status_code}")
        print(f"Respuesta del servidor: {respuesta.text}")

    except requests.RequestException as error:
        print(f"Error al conectar con la API: {error}")


def main():

    print("Iniciando extracción para X...")
    print(f"Fuente objetivo: {RUTA_FUENTE}\n")

    # Cargar el registro previo acumulado en el JSON local
    historial_previo = cargar_historial_existente()

    # Extraer los enlaces visibles actualmente en la cuenta de X
    urls_obtenidas = extractor_links_twitter(
        RUTA_FUENTE,
        limite=15
    )

    # Filtrar solo las URLs que no estén registradas en el historial
    urls_nuevas = [
        url
        for url in urls_obtenidas
        if url not in historial_previo
    ]

    # Imprimir métricas de la ejecución en consola
    print("\nResumen de extracción")
    print(f"Links en historial previo: {len(historial_previo)}")
    print(f"Links encontrados actualmente: {len(urls_obtenidas)}")
    print(f"Links totalmente nuevos: {len(urls_nuevas)}")

    # Si hay enlaces nuevos, enviarlos al servidor
    if urls_nuevas:
        enviar_urls_a_api(urls_nuevas)
    else:
        print("No hay enlaces nuevos para enviar.")

    # Unir el historial viejo con los nuevos enlaces capturados
    historial_actualizado = list(
        historial_previo.union(
            set(urls_nuevas)
        )
    )

    # Estructurar la información completa que se guardará localmente
    resultado_json = {
        "source": RUTA_FUENTE,
        "query": "Noticias Ensenada",
        "total_extracted": len(urls_obtenidas),
        "urls_nuevas": urls_nuevas,
        "urls_historial": historial_actualizado,
    }

    # Sobrescribir el archivo JSON con los datos y el historial actualizado
    with open(
        RUTA_ARCHIVO,
        "w",
        encoding="utf-8"
    ) as archivo:
        json.dump(
            resultado_json,
            archivo,
            ensure_ascii=False,
            indent=4
        )

    print(f"Archivo '{RUTA_ARCHIVO}' actualizado.")


if __name__ == "__main__":
    main()