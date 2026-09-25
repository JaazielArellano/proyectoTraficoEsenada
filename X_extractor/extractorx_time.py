import json
import os
import re
import time
import requests


RUTA_FUENTE = "https://x.com/znortemedios"

RUTA_ARCHIVO = "links_extraidos.json"

INTERVALO_SEGUNDOS = 600


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
        print(f"Estado de la respuesta HTTP: {respuesta.status_code}")

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
                    previas = datos.get("urls_historial", [])
                    nuevas_previas = datos.get("urls_nuevas", [])
                    return set(previas + nuevas_previas)

                elif isinstance(datos, list):
                    return set(datos)
        except (json.JSONDecodeError, IOError):
            return set()
    return set()


if __name__ == "__main__":
    print("Iniciando monitoreo automatizado para X...")
    print(f"Fuente objetivo: {RUTA_FUENTE}")
    print("Presiona Ctrl + C en la terminal para detener la ejecución.\n")

    while True:
        
        historial_previas = cargar_historial_existente()

        urls_obtenidas = extractor_links_twitter(RUTA_FUENTE, limite=15)

    
        urls_nuevas = [
            url for url in urls_obtenidas if url not in historial_previas
        ]
        lista_historial = list(historial_previas)

        print("Resumen de extracción")
        print(f"Links en historial (previas): {len(lista_historial)}")
        print(f"Links totalmente nuevos: {len(urls_nuevas)}")

        resultado_json = {
            "source": RUTA_FUENTE,
            "query": "Noticias Ensenada",
            "total_extracted": len(urls_obtenidas),
            "urls_nuevas": urls_nuevas,
            "urls_historial": lista_historial,
        }

        with open(RUTA_ARCHIVO, "w", encoding="utf-8") as archivo:
            json.dump(resultado_json, archivo, ensure_ascii=False, indent=4)

        print(f"Archivo '{RUTA_ARCHIVO}' actualizado exitosamente.")
        print(
            f"Esperando {INTERVALO_SEGUNDOS // 60} minutos para la siguiente"
            " búsqueda...\n"
        )

        time.sleep(INTERVALO_SEGUNDOS)