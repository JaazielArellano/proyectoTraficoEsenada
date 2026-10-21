"""Módulo extractor de enlaces para El Vigía.

Este script obtiene los enlaces de las noticias desde el RSS, 
utilizando un historial en caché y genera archivos JSON.
"""

import json
import os
import re
import uuid
from datetime import datetime
import urllib3
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


# Cargar las variables guardadas en el archivo de configuración .env
load_dotenv()

# Desactivar los mensajes de advertencia de seguridad SSL al hacer peticiones HTTP
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def limpiar_texto(texto):
    """Limpia el texto del título quitando etiquetas raras y espacios extra."""
    if not texto:
        return "Sin título"
    # Quitar etiquetas tipo <![CDATA[ ... ]]> que suelen venir en los RSS
    texto_limpio = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", texto, flags=re.DOTALL)
    # Cambiar espacios invisibles o de formato web (\xa0) por espacios normales
    texto_limpio = texto_limpio.replace("\xa0", " ")
    return texto_limpio.strip()


def extractor_links():
    """Descarga el RSS, extrae noticias y retorna un objeto JSON con los resultados."""
    # Leer la URL del feed RSS configurada en el archivo .env
    rss_url = os.getenv("RSS_URL")

    # Encabezados para simular que la petición la hace un navegador web real
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    }

    try:
        # Hacer la petición para obtener el contenido del feed RSS
        respuesta = requests.get(
            rss_url, headers=headers, verify=False, timeout=10
        )
        print(f"Estado de la respuesta HTTP: {respuesta.status_code}")

        # Si la web respondió correctamente (200)
        if respuesta.status_code == 200:
            # Procesar el contenido usando BeautifulSoup en modo XML
            soup = BeautifulSoup(respuesta.content, "xml")
            # Buscar todos los bloques de noticias ('item' o 'entry')
            noticias = soup.find_all("item") or soup.find_all("entry")

            lista_links = []
            for noticia in noticias:
                link_tag = noticia.find("link")
                title_tag = noticia.find("title")

                # Obtener la dirección URL del enlace
                href = ""
                if link_tag:
                    href = (
                        link_tag.get_text().strip()
                        or link_tag.get("href", "").strip()
                    )

                # Obtener y limpiar el título de la noticia
                texto_raw = title_tag.string or title_tag.text if title_tag else ""
                titulo_limpio = limpiar_texto(str(texto_raw))

                # Guardar la noticia si tiene una URL válida que empiece con http
                if href and href.startswith("http"):
                    lista_links.append({
                        "id": str(uuid.uuid4()),
                        "titulo": titulo_limpio,
                        "url": href,
                        "retrieved_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                    })

            # Devolver objeto JSON y los links extraídos
            return {
                "status": "success",
                "status_code": respuesta.status_code,
                "total_extraidos": len(lista_links),
                "data": lista_links
            }

        # Devolver objeto JSON en caso de error HTTP diferente de 200
        return {
            "status": "fail",
            "status_code": respuesta.status_code,
            "total_extraidos": 0,
            "data": []
        }

    except requests.RequestException as error:
        # Retornar objeto JSON capturando el error de conexión
        print(f"Error de conexión: {error}")
        return {
            "status": "error",
            "status_code": None,
            "message": f"Error de conexión: {error}",
            "data": []
        }


def cargar_json(nombre):
    """Abre y lee un archivo JSON si existe en la carpeta."""
    if os.path.exists(nombre):
        try:
            with open(nombre, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def guardar_json(nombre, datos):
    """Escribe los datos dentro de un archivo JSON."""
    with open(nombre, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)


def ejecutar():
    """Coordinar la extracción, comparar con la caché, guardar archivos y 
    retornar el resumen en un objeto JSON."""
    # Cargar el historial de enlaces guardados anteriormente
    cache = cargar_json("cache.json")
    nuevos = []

    # Extraer las noticias que están públicas en este momento
    resultado_extraccion = extractor_links()
    links_actuales = resultado_extraccion.get("data", [])

    # Crear un conjunto con las URLs conocidas para buscar más rápido
    urls_cache = {item["url"] for item in cache if isinstance(item, dict) and "url" in item}

    # Revisar cuáles noticias son realmente nuevas
    for item in links_actuales:
        if item["url"] not in urls_cache:
            nuevos.append(item)
            cache.append(item)

    # Mostrar en consola cuántas noticias se encontraron
    print("\n--- Resumen de extracción ---")
    print(f"Links viejos (historial en cache): {len(cache) - len(nuevos)}")
    print(f"Links totalmente nuevos: {len(nuevos)}")

    # 1. Guardar las nuevas noticias completas y actualizar la caché
    guardar_json("urls.json", nuevos)
    guardar_json("cache.json", cache)

    # 2. Guardar la lista con las direcciones web nuevas
    lista_solo_urls = [item["url"] for item in nuevos]
    formato_simple_urls = {
        "urls": lista_solo_urls
    }
    guardar_json("nuevas_urls.json", formato_simple_urls)

    print("Archivos 'urls.json', 'cache.json' y 'nuevas_urls.json' actualizados correctamente.")

    # Devolver el resumen del proceso en formato objeto JSON
    return {
        "status": "success",
        "extraccion_status": resultado_extraccion.get("status"),
        "links_viejos": len(cache) - len(nuevos),
        "links_nuevos": len(nuevos),
        "archivos_actualizados": ["urls.json", "cache.json", "nuevas_urls.json"],
        "data": nuevos
    }


if __name__ == "__main__":
    # Ejecución individual para prueba
    resultado = ejecutar()
    print("\nObjeto JSON por ejecutar():")
    print(resultado)
