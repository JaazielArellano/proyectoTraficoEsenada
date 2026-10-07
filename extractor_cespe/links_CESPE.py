
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json


def extractor_links():

    url_base = "https://www.cespe.gob.mx/public/Noticias?page=1"

    respuesta = requests.get(
        url_base,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    ) 

    print("Código de respuesta:", respuesta.status_code)
    print("Caracteres recibidos:", len(respuesta.text))

    soup = BeautifulSoup(respuesta.text, "html.parser")

    lista_links = []

    for a in soup.find_all("a", href=True):

        href = a["href"]
        texto = a.get_text(" ", strip=True)

        print("TEXTO:", texto)
        print("LINK:", href)
        print("------------------------")

        if (
            "aviso" in texto.lower()
            or "corte" in texto.lower()
            or "suspensión" in texto.lower()
            or "suspension" in texto.lower()
        ):

            full_url = urljoin(url_base, href)

            lista_links.append(full_url)

    return lista_links


urls = extractor_links()

print("\nLISTA FINAL:")
print(urls)

import json

with open("cespe_links.json", "w", encoding="utf-8") as f:
    json.dump(urls, f, ensure_ascii=False, indent=4)

print(f"\n✅ Se guardaron {len(urls)} enlaces en cespe_links.json")
 