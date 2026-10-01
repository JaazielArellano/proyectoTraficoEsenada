"""
ejemplo_integracion.py - Como usar la libreria del Cleaner (Alejandra)
dentro del codigo del Collector (Ximena)

Este archivo es solo un EJEMPLO de integracion, para que Ximena sepa donde
y como llamar la libreria cleaner_lib/. No reemplaza su api_collector.py,
solo muestra el paso que falta: una vez que el Collector descarga el HTML
de cada URL (con requests), pasarlo por limpiar_html() antes de guardarlo
o mandarlo al Extractor.

Requisitos:
    pip install requests
    (cleaner_lib/ ya trae sus propios requisitos: beautifulsoup4, lxml, ftfy)

Como correrlo (ejemplo con las URLs que ya tiene encoladas el Collector):
    python ejemplo_integracion.py
"""

import json
from datetime import datetime, timezone

import requests

# Aqui esta la unica linea que Ximena necesita agregar a su codigo:
# importar la funcion de limpieza desde la libreria del Cleaner.
from cleaner_lib import limpiar_html


def descargar_y_limpiar(fuente: str, url: str) -> dict:
    """
    Descarga el HTML de una URL (esto es la parte de Ximena, Request/Collector)
    y lo limpia con la libreria del Cleaner (esto es la parte de Alejandra).

    Regresa el resultado ya en el formato de contrato oficial del proyecto:
    source, url, retrieved_at, text.
    """
    respuesta = requests.get(url, timeout=10)
    respuesta.raise_for_status()
    html_crudo = respuesta.text

    texto_limpio = limpiar_html(html_crudo)  # <-- aqui se usa la libreria

    return {
        "source": fuente,
        "url": url,
        "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "text": texto_limpio,
    }


if __name__ == "__main__":
    # Ejemplo: toma las URLs que ya recibio el Collector (cola_urls.json)
    # y las descarga + limpia una por una.
    with open("cola_urls.json", "r", encoding="utf-8") as f:
        cola = json.load(f)

    resultados = []
    for lote in cola:
        for url in lote["urls"]:
            print(f"Descargando y limpiando: {url}")
            resultados.append(descargar_y_limpiar(fuente="general", url=url))

    with open("noticias_limpias.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    print(f"\nListo. Se procesaron {len(resultados)} URL(s).")
    print("Resultado guardado en noticias_limpias.json")