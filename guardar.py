

"""
Scraper de CFE que genera y actualiza un archivo JSON ('links_cfe.json')
guardando la lista acumulada de links con la estructura de campos requerida.
"""

from datetime import datetime
import json
import os
import time
from urllib.parse import urljoin
import uuid
from bs4 import BeautifulSoup
import setuptools  # Mantiene compatibilidad con distutils en Python 3.12/3.13
import undetected_chromedriver as uc


# PARCHE: Silenciar la advertencia OSError: [WinError 6] en Windows
def _del_silencioso(self):
    try:
        self.quit()
    except Exception:
        pass


uc.Chrome.__del__ = _del_silencioso


def cargar_json_existente(ruta_archivo):
    """Lee el archivo JSON local si existe; si no, retorna una lista vacía."""
    if os.path.exists(ruta_archivo):
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def guardar_json(ruta_archivo, datos):
    """Escribe la lista completa de objetos en el archivo JSON."""
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)


def extraer_y_guardar_links(
    url_objetivo="https://www.cfe.gob.mx/Pages/default.aspx",
    archivo_json="links_cfe.json",
):
    print(f"Abriendo navegador evadido para consultar {url_objetivo}...")

    driver = None
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    # 1. Cargar la lista existente de noticias/links guardados previamente
    registro_existente = cargar_json_existente(archivo_json)
    urls_guardadas = {item["url"] for item in registro_existente}

    try:
        try:
            driver = uc.Chrome(options=options, version_main=153)
        except Exception:
            driver = uc.Chrome(options=options)

        driver.get(url_objetivo)
        driver.implicitly_wait(8)
        time.sleep(2)

        html_content = driver.page_source
        driver.quit()
        driver = None

        soup = BeautifulSoup(html_content, "html.parser")

        # Priorizar enlaces de noticias (div.entry-title a) o tomar todas las etiquetas <a>
        etiquetas_a = soup.select("div.entry-title a")
        if not etiquetas_a:
            etiquetas_a = soup.find_all("a", href=True)

        fecha_captura = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        nuevos_registros = []

        for a in etiquetas_a:
            href_relativo = a.get("href", "").strip()

            if (
                not href_relativo
                or href_relativo.startswith("#")
                or "javascript" in href_relativo.lower()
            ):
                continue

            link_absoluto = urljoin(url_objetivo, href_relativo)

            # Validar que no exista en el archivo JSON ni se duplique en la misma iteración
            if link_absoluto not in urls_guardadas and not any(
                r["url"] == link_absoluto for r in nuevos_registros
            ):
                objeto_noticia = {
                    "id": str(uuid.uuid4()),
                    "titulo": a.text.strip() or "[Sin título]",
                    "url": link_absoluto,
                    "retrieved_at": fecha_captura,
                }
                nuevos_registros.append(objeto_noticia)

        if nuevos_registros:
            # Unir los nuevos elementos a la lista previa y guardar en el JSON
            lista_actualizada = registro_existente + nuevos_registros
            guardar_json(archivo_json, lista_actualizada)
            print(
                f"✨ ¡Se agregaron {len(nuevos_registros)} nuevos links a '{archivo_json}'!"
            )
        else:
            print(
                f"ℹ️ No se encontraron links nuevos. El archivo '{archivo_json}' está actualizado."
            )

    except Exception as error:
        print(f"⚠️ Error durante la extracción: {error}")

    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass


if __name__ == "__main__":
    extraer_y_guardar_links()