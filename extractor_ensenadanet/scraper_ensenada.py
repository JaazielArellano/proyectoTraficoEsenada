import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def obtener_notas_ensenadanet():
    # 1. Definir la URL de la página principal de noticias
    url_base = "https://ensenada.net/noticias/"

    # 2. Hacer la petición simulando ser un navegador (para evitar bloqueos)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    print("Conectando con ensenada.net...")
    respuesta = requests.get(url_base, headers=headers)
    respuesta.encoding = 'latin-1' # Formato clásico para sitios web en español

    # 3. Analizar el HTML con BeautifulSoup
    soup = BeautifulSoup(respuesta.text, 'html.parser')

    # 4. Buscar todos los spans que tengan la clase "tituloNota" (lo que viste en tu inspección)
    spans_titulos = soup.find_all('span', class_='tituloNota')

    lista_noticias = []

    # 5. Iterar sobre cada título encontrado para sacar su texto y su link
    for span in spans_titulos:
        titulo_limpio = span.text.strip()

        # El link (href) está en la etiqueta <a> que "envuelve" al span
        etiqueta_a = span.find_parent('a')

        if etiqueta_a and 'href' in etiqueta_a.attrs:
            href_relativo = etiqueta_a['href']

            # Convierte el link relativo (ej. 'nota.php?id=123') en un link completo que funcione
            link_completo = urljoin(url_base, href_relativo)

            lista_noticias.append({
                "titulo": titulo_limpio,
                "link": link_completo
            })

    return lista_noticias

# --- Ejecución del código ---
if __name__ == "__main__":
    noticias_extraidas = obtener_notas_ensenadanet()

    print(f"¡Se encontraron {len(noticias_extraidas)} noticias!\n")

    # Imprimir las primeras 5 para comprobar
    for i, noticia in enumerate(noticias_extraidas[:5], 1):
        print(f"Noticia {i}: {noticia['titulo']}")
        print(f"Enlace: {noticia['link']}\n")