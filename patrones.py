"""
Módulo scraper para extraer los títulos y enlaces de noticias/boletines
del portal oficial de la CFE utilizando BeautifulSoup y Playwright.
"""

from urllib.parse import urljoin
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def obtener_notas_cfe():
    """
    Conecta a la sección de boletines de la CFE, extrae los títulos
    y sus enlaces correspondientes, y devuelve una lista de diccionarios.
    """
    url_base = "https://www.cfe.mx/prensa/boletines/pages/default.aspx"
    lista_noticias = []

    print("Conectando con el portal de la CFE...")

    try:
        with sync_playwright() as p:
            # Iniciar navegador Chromium en segundo plano ignorando errores de certificados SSL
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                ignore_https_errors=True,
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            )
            page = context.new_page()

            # Navegar a la página
            page.goto(url_base, timeout=60000, wait_until="domcontentloaded")

            # Hacer un scroll para forzar la carga de elementos de la tabla dinámica
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(3000)

            # Obtener el código HTML final
            html_content = page.content()
            browser.close()

            # Parsear con BeautifulSoup
            soup = BeautifulSoup(html_content, "html.parser")

            # Buscar todos los enlaces que contengan texto (título de la noticia)
            for etiqueta_a in soup.find_all("a", href=True):
                titulo_limpio = etiqueta_a.text.strip()
                href_relativo = etiqueta_a["href"].strip()

                # Ignorar enlaces sin texto, javascripts o anclas internas
                if (
                    not titulo_limpio
                    or not href_relativo
                    or href_relativo.startswith("#")
                    or "javascript" in href_relativo.lower()
                ):
                    continue

                # Filtrar únicamente enlaces pertenecientes a boletines/prensa
                if any(
                    palabra in href_relativo.lower()
                    for palabra in ["boletin", "prensa", "comunicado", "pages"]
                ):
                    link_completo = urljoin("https://www.cfe.mx", href_relativo)

                    # Evitar duplicados
                    if not any(
                        item["link"] == link_completo for item in lista_noticias
                    ):
                        lista_noticias.append({
                            "titulo": titulo_limpio,
                            "link": link_completo,
                        })

    except Exception as e:
        print(f"Error al conectar con CFE: {e}")

    return lista_noticias


if __name__ == "__main__":
    noticias_extraidas = obtener_notas_cfe()

    print(f"¡Se encontraron {len(noticias_extraidas)} noticias de CFE!\n")

    for i, noticia in enumerate(noticias_extraidas[:5], 1):
        print(f"Noticia {i}: {noticia['titulo']}")
        print(f"Enlace: {noticia['link']}\n")