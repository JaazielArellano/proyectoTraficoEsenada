import json
import time
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests

from cleaner_lib import limpiar_html

ARCHIVO_COLA = "cola_urls.json"
ARCHIVO_SALIDA = "noticias_limpias.json"
ARCHIVO_ERRORES = "errores.json"
PAUSA_SEGUNDOS = 1.0
TIMEOUT_SEGUNDOS = 15
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ExtratronBot/1.0; proyecto escolar UABC)"}


def nombre_fuente(url):
    dominio = urlparse(url).netloc.lower()
    if dominio.startswith("www."):
        dominio = dominio[4:]
    return dominio.replace(".", "_")


def ahora():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def descargar(url):
    respuesta = requests.get(url, headers=HEADERS, timeout=TIMEOUT_SEGUNDOS)
    respuesta.raise_for_status()
    if respuesta.encoding is None or respuesta.encoding.lower() == "iso-8859-1":
        respuesta.encoding = respuesta.apparent_encoding
    return respuesta.text


def main():
    with open(ARCHIVO_COLA, "r", encoding="utf-8") as f:
        cola = json.load(f)

    urls = []
    for envio in cola:
        for url in envio["urls"]:
            if url not in urls:
                urls.append(url)

    print(f"URLs por procesar: {len(urls)}\n")
    noticias, errores = [], []

    for i, url in enumerate(urls, start=1):
        print(f"[{i}/{len(urls)}] {url}")
        try:
            texto = limpiar_html(descargar(url))
            if not texto:
                raise ValueError("el texto limpio quedo vacio")
            noticias.append({"source": nombre_fuente(url), "url": url, "retrieved_at": ahora(), "text": texto})
            print(f"    ok ({len(texto)} caracteres)")
        except Exception as e:
            errores.append({"url": url, "error": str(e), "at": ahora()})
            print(f"    error: {e}")
        time.sleep(PAUSA_SEGUNDOS)

    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        json.dump({"total": len(noticias), "noticias": noticias}, f, ensure_ascii=False, indent=2)
    with open(ARCHIVO_ERRORES, "w", encoding="utf-8") as f:
        json.dump(errores, f, ensure_ascii=False, indent=2)

    print(f"\n{len(noticias)} noticias en {ARCHIVO_SALIDA}, {len(errores)} errores en {ARCHIVO_ERRORES}")


if __name__ == "__main__":
    main()
