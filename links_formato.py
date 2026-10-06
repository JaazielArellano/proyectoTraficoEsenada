"""
Scraper de monitoreo para CFE con estructura de JSON personalizada.
Genera la salida exacta con campos: id (UUID), titulo, url y retrieved_at.
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


def cargar_enlaces_existentes(archivo_json):
    """Carga los enlaces guardados previamente desde el JSON."""
    if os.path.exists(archivo_json):
        try:
            with open(archivo_json, "r", encoding="utf-8") as f:
                datos = json.load(f)
                return {item["url"]: item for item in datos}
        except Exception:
            return {}
    return {}


def guardar_enlaces(archivo_json, lista_enlaces):
    """Guarda la lista de enlaces actualizada en el JSON."""
    with open(archivo_json, "w", encoding="utf-8") as f:
        json.dump(lista_enlaces, f, ensure_ascii=False, indent=4)


def obtener_enlaces_actuales(url_objetivo):
    """Abre Chrome evadido y extrae las noticias actuales con la estructura solicitada."""
    enlaces_extraidos = []
    driver = None

    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

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

        # Seleccionar las noticias (div.entry-title a) o respaldar con todas las etiquetas <a>
        etiquetas_a = soup.select("div.entry-title a")
        if not etiquetas_a:
            etiquetas_a = soup.find_all("a", href=True)

        # Marca de tiempo en formato ISO exacto
        fecha_registro = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        for a in etiquetas_a:
            href_relativo = a.get("href", "").strip()

            if (
                not href_relativo
                or href_relativo.startswith("#")
                or "javascript" in href_relativo.lower()
            ):
                continue

            link_absoluto = urljoin(url_objetivo, href_relativo)

            # Evitar duplicados en la misma lectura
            if not any(item["url"] == link_absoluto for item in enlaces_extraidos):
                enlaces_extraidos.append(
                    {
                        "id": str(uuid.uuid4()),  # Genera el UUID dinámico
                        "titulo": a.text.strip() or "[Sin título]",
                        "url": link_absoluto,
                        "retrieved_at": fecha_registro,
                    }
                )

        return enlaces_extraidos

    except Exception as error:
        print(f"Error al conectar con CFE: {error}")
        return []

    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass


def monitorear_cfe_estandar(
    url_objetivo="https://www.cfe.gob.mx/Pages/default.aspx",
    archivo_json="links_cfe.json",
    minutos_espera=10,
):
    print(" Iniciando servicio de monitoreo CFE (Formato Estandarizado)...\n")

    while True:
        existentes_dict = cargar_enlaces_existentes(archivo_json)
        enlaces_actuales = obtener_enlaces_actuales(url_objetivo)

        nuevos_enlaces = []
        for item in enlaces_actuales:
            if item["url"] not in existentes_dict:
                nuevos_enlaces.append(item)

        if nuevos_enlaces:
            print(f"¡Se encontraron {len(nuevos_enlaces)} enlaces nuevos!")
            for nuevo in nuevos_enlaces:
                print(f"   [{nuevo['titulo']}] -> {nuevo['url']}")

            todos_los_enlaces = list(existentes_dict.values()) + nuevos_enlaces
            guardar_enlaces(archivo_json, todos_los_enlaces)
            print(f"Archivo '{archivo_json}' actualizado con éxito.")
        else:
            print("ℹ️ No se encontraron enlaces nuevos.")

        print(
            f" Esperando {minutos_espera} minutos para la siguiente búsqueda...\n"
        )
        time.sleep(minutos_espera * 60)


if __name__ == "__main__":
    monitorear_cfe_estandar()