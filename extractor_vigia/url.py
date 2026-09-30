import json
import os
import re
import time
import uuid
from datetime import datetime
import urllib3
import requests
from bs4 import BeautifulSoup

# Desactiva la advertencia InsecureRequestWarning en la terminal
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def limpiar_texto(texto):
    """Elimina etiquetas CDATA, caracteres nbsps y espacios extra del texto."""
    if not texto:
        return "Sin título"
    # Eliminar bloques <![CDATA[ ... ]]>
    texto_limpio = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", texto, flags=re.DOTALL)
    # Reemplazar espacios de no-separación (\xa0) por espacios normales
    texto_limpio = texto_limpio.replace("\xa0", " ")
    return texto_limpio.strip()


def extractor_links():
    """Extrae las noticias del feed RSS de El Vigía en formato de objetos."""
    rss_url = "https://www.elvigia.net/rss/feed.html?r=77"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    }

    try:
        respuesta = requests.get(
            rss_url, headers=headers, verify=False, timeout=10
        )
        print(f"Estado de la respuesta HTTP: {respuesta.status_code}")

        if respuesta.status_code == 200:
            soup = BeautifulSoup(respuesta.content, "html.parser")
            noticias = soup.find_all("item") or soup.find_all("entry")

            lista_links = []
            for noticia in noticias:
                link_tag = noticia.find("link")
                title_tag = noticia.find("title")

                # Extraer URL
                href = ""
                if link_tag:
                    href = link_tag.text.strip() or link_tag.get("href", "")

                # Extraer Título y aplicar limpieza regex de CDATA
                texto_raw = title_tag.string or title_tag.text if title_tag else ""
                titulo_limpio = limpiar_texto(str(texto_raw))

                if href:
                    lista_links.append({
                        "id": str(uuid.uuid4()),
                        "titulo": titulo_limpio,
                        "url": href,
                        "retrieved_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                    })

            return lista_links

    except requests.RequestException as error:
        print(f"Error de conexión: {error}")

    return []


def cargar_json(nombre):
    """Carga un archivo JSON existente de forma segura."""
    if os.path.exists(nombre):
        try:
            with open(nombre, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def guardar_json(nombre, datos):
    """Guarda los datos en un archivo JSON."""
    with open(nombre, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)


# --- AUTOMATIZACIÓN CADA 10 MINUTOS ---
INTERVALO_SEGUNDOS = 600  # 10 minutos (10 * 60)

print("Iniciando servicio de extracción automatizada cada 10 minutos...")
print("Presiona Ctrl + C para detenerlo.\n")

while True:
    cache = cargar_json("cache.json")
    nuevos = []

    links_actuales = extractor_links()
    urls_cache = {item["url"] for item in cache if isinstance(item, dict) and "url" in item}

    for item in links_actuales:
        if item["url"] not in urls_cache:
            nuevos.append(item)
            cache.append(item)

    print(f"\n--- Resumen de extracción ---")
    print(f"Links viejos (historial en cache): {len(cache) - len(nuevos)}")
    print(f"Links totalmente nuevos: {len(nuevos)}")

    # 1. Guardar objetos completos en urls.json y cache.json
    guardar_json("urls.json", nuevos)
    guardar_json("cache.json", cache)

    # 2. Guardar solo la lista de cadenas de texto de las URLs nuevas en el formato requerido
    lista_solo_urls = [item["url"] for item in nuevos]
    formato_simple_urls = {
        "urls": lista_solo_urls
    }
    guardar_json("nuevas_urls.json", formato_simple_urls)

    print("Archivos 'urls.json', 'cache.json' y 'nuevas_urls.json' actualizados exitosamente.")
    print("Esperando 10 minutos para la siguiente ejecución...\n")
    time.sleep(INTERVALO_SEGUNDOS)