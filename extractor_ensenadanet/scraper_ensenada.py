"""
Módulo scraper para extraer los títulos y enlaces de noticias
del portal ensenada.net utilizando BeautifulSoup y requests.
"""

from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def obtener_notas_ensenadanet():
    """
    Conecta a la página principal de ensenada.net, extrae los títulos de las notas
    y sus enlaces correspondientes, y devuelve una lista de diccionarios.
    """
    url_base = "https://ensenada.net/noticias/"

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        )
    }

    print("Conectando con ensenada.net...")
    # Se agrega un timeout de 10 segundos
    respuesta = requests.get(url_base, headers=headers, timeout=10)
    respuesta.encoding = 'latin-1'

    soup = BeautifulSoup(respuesta.text, 'html.parser')

    spans_titulos = soup.find_all('span', class_='tituloNota')

    lista_noticias = []

    for span in spans_titulos:
        titulo_limpio = span.text.strip()

        etiqueta_a = span.find_parent('a')

        if etiqueta_a and 'href' in etiqueta_a.attrs:
            href_relativo = etiqueta_a['href']

            link_completo = urljoin(url_base, href_relativo)

            lista_noticias.append({
                "titulo": titulo_limpio,
                "link": link_completo
            })

    return lista_noticias


if __name__ == "__main__":
    noticias_extraidas = obtener_notas_ensenadanet()

    print(f"¡Se encontraron {len(noticias_extraidas)} noticias!\n")

    for i, noticia in enumerate(noticias_extraidas[:5], 1):
        print(f"Noticia {i}: {noticia['titulo']}")
        print(f"Enlace: {noticia['link']}\n")
