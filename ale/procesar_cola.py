"""
procesar_cola.py - Une el Collector (Ximena) con el Cleaner (Alejandra)

Que hace:
  1. Lee cola_urls.json (las URLs que mandaron los Extractores a la API de Ximena).
  2. Descarga el HTML de cada URL con requests.
  3. Lo limpia con cleaner_lib.limpiar_html().
  4. Guarda UN solo JSON consolidado (noticias_limpias.json) con el contrato:
        source, url, retrieved_at, text
  5. Las URLs que fallan (404, timeout, bloqueo) NO tumban el proceso:
     se guardan aparte en errores.json para revisarlas.

Requisitos:
    pip install requests beautifulsoup4 lxml ftfy pydantic

Como correrlo (desde la carpeta que contiene cleaner_lib/ y cola_urls.json):
    python procesar_cola.py
"""

import json
import time
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests

from cleaner_lib import limpiar_html

ARCHIVO_COLA = "cola_urls.json"
ARCHIVO_SALIDA = "noticias_limpias.json"
ARCHIVO_ERRORES = "errores.json"

# Pausa entre peticiones para no saturar los sitios (buena practica del proyecto)
PAUSA_SEGUNDOS = 1.0
TIMEOUT_SEGUNDOS = 15

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ExtratronBot/1.0; proyecto escolar UABC)"
}


def nombre_fuente(url: str) -> str:
    """Saca un nombre corto de la fuente a partir del dominio.
    https://www.ensenada.net/nota?id=1 -> ensenada_net
    """
    dominio = urlparse(url).netloc.lower()
    if dominio.startswith("www."):
        dominio = dominio[4:]
    return dominio.replace(".", "_")


def ahora_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def descargar(url: str) -> str:
    respuesta = requests.get(url, headers=HEADERS, timeout=TIMEOUT_SEGUNDOS)
    respuesta.raise_for_status()
    # Si el servidor no declara codificacion, adivinarla (ftfy corrige el resto)
    if respuesta.encoding is None or respuesta.encoding.lower() == "iso-8859-1":
        respuesta.encoding = respuesta.apparent_encoding
    return respuesta.text


def main() -> None:
    with open(ARCHIVO_COLA, "r", encoding="utf-8") as f:
        cola = json.load(f)

    # Juntar todas las URLs de todos los envios, sin repetir
    urls = []
    for envio in cola:
        for url in envio["urls"]:
            if url not in urls:
                urls.append(url)

    print(f"URLs unicas por procesar: {len(urls)}\n")

    noticias, errores = [], []

    for i, url in enumerate(urls, start=1):
        print(f"[{i}/{len(urls)}] {url}")
        try:
            html = descargar(url)
            texto = limpiar_html(html)
            if not texto:
                raise ValueError("La pagina se descargo pero el texto limpio quedo vacio")
            noticias.append({
                "source": nombre_fuente(url),
                "url": url,
                "retrieved_at": ahora_iso(),
                "text": texto,
            })
            print(f"    OK ({len(texto)} caracteres)")
        except Exception as e:
            errores.append({"url": url, "error": str(e), "at": ahora_iso()})
            print(f"    ERROR: {e}")
        time.sleep(PAUSA_SEGUNDOS)

    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        json.dump({"total": len(noticias), "noticias": noticias}, f, ensure_ascii=False, indent=2)

    with open(ARCHIVO_ERRORES, "w", encoding="utf-8") as f:
        json.dump(errores, f, ensure_ascii=False, indent=2)

    print(f"\nListo: {len(noticias)} noticias limpias -> {ARCHIVO_SALIDA}")
    print(f"       {len(errores)} con error      -> {ARCHIVO_ERRORES}")


if __name__ == "__main__":
    main()
