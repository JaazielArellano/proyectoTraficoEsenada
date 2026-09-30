"""
Scraper optimizado para CFE en formato JSON.
Incluye un parche sobre el destructor __del__ de undetected_chromedriver 
para suprimir por completo el aviso OSError: [WinError 6] en Windows.
"""

import json
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import setuptools  # Mantiene compatibilidad con distutils en Python 3.12/3.13
import undetected_chromedriver as uc

# PARCHE: Sobreescribir el destructor __del__ para suprimir el WinError 6 en Windows
def _del_silencioso(self):
    try:
        self.quit()
    except Exception:
        pass

uc.Chrome.__del__ = _del_silencioso


def exportar_links_json(
    url_objetivo="https://www.cfe.gob.mx/Pages/default.aspx",
    archivo_json="links_cfe.json",
):
    lista_enlaces = []
    driver = None

    print(f"Abriendo navegador evadido para extraer enlaces de {url_objetivo}...")

    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    try:
        try:
            driver = uc.Chrome(options=options, version_main=153)
        except Exception:
            driver = uc.Chrome(options=options)

        driver.get(url_objetivo)

        print("Esperando la carga completa del DOM y boletines...")
        driver.implicitly_wait(8)
        time.sleep(2)

        html_content = driver.page_source

        # Cerrar el navegador
        driver.quit()
        driver = None

        soup = BeautifulSoup(html_content, "html.parser")

        # Selector prioritario: div.entry-title h4 a
        etiquetas_a = soup.select("div.entry-title a")

        if not etiquetas_a:
            etiquetas_a = soup.find_all("a", href=True)

        for a in etiquetas_a:
            href_relativo = a.get("href", "").strip()

            if (
                not href_relativo
                or href_relativo.startswith("#")
                or "javascript" in href_relativo.lower()
            ):
                continue

            link_absoluto = urljoin(url_objetivo, href_relativo)

            if not any(item["url"] == link_absoluto for item in lista_enlaces):
                lista_enlaces.append(
                    {
                        "titulo": a.text.strip() or "[Sin texto]",
                        "url": link_absoluto,
                        "url_relativa": href_relativo,
                        "es_boletin": (
                            "boletin" in link_absoluto.lower()
                            or "i=" in link_absoluto
                        ),
                    }
                )

        print(f"\n¡Extracción completada! Se procesaron {len(lista_enlaces)} enlaces.")

        # Guardar en archivo JSON
        with open(archivo_json, "w", encoding="utf-8") as f_json:
            json.dump(lista_enlaces, f_json, ensure_ascii=False, indent=4)

        print(f"Archivo JSON generado exitosamente en: '{archivo_json}'\n")

    except Exception as error:
        print(f"Error durante el scraping: {error}")

    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass


if __name__ == "__main__":
    exportar_links_json()