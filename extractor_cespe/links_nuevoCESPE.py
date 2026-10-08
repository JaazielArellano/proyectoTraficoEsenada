import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import time

API_URL = "https://relax-albatross-pessimism.ngrok-free.dev/collector"
URL_BASE = "https://www.cespe.gob.mx/public/Noticias?page=1"

def extractor_links():
    respuesta = requests.get(URL_BASE, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(respuesta.text, "html.parser")

    lista_links = []
    for a in soup.find_all("a", href=True):
        texto = a.get_text(" ", strip=True)
        href = a["href"]

        if (
            "aviso" in texto.lower()
            or "corte" in texto.lower()
            or "suspensión" in texto.lower()
            or "suspension" in texto.lower()
        ):
            full_url = urljoin(URL_BASE, href)
            lista_links.append(full_url)

    return lista_links

def guardar_json(nombre, datos):
    with open(nombre, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def enviar_a_api(nuevos):
    if not nuevos:
        print(" No hay enlaces nuevos para enviar.")
        return

    enviados_ok = 0
    enviados_error = 0

    for url in nuevos:
        respuesta = requests.post(API_URL, json={"url": url})
        if respuesta.status_code == 200:
            print(f"Aviso enviado correctamente: {url}")
            enviados_ok += 1
        else:
            print(f"Error al enviar {url} -> Código {respuesta.status_code}")
            enviados_error += 1

    print("\n--- Resumen ---")
    print(f"Enlaces enviados correctamente: {enviados_ok}")
    print(f"Enlaces con error: {enviados_error}")

def ciclo_scraper():
    try:
        with open("cache.json", "r", encoding="utf-8") as f:
            cache = json.load(f)
    except FileNotFoundError:
        cache = []

    urls = extractor_links()
    nuevos = [u for u in urls if u not in cache]

    guardar_json("cespe_links.json", urls)
    guardar_json("nuevos.json", nuevos)
    guardar_json("cache.json", cache + nuevos)

    print(f"Se guardaron {len(urls)} enlaces en cespe_links.json")
    print(f"Nuevos detectados: {len(nuevos)} (guardados en nuevos.json)")

    enviar_a_api(nuevos)

if __name__ == "__main__":
    ciclo_scraper()
    
