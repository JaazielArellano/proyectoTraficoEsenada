"""Modulo Request / Collector - CFE (Plataforma Extratron)
------------------------------------------------------
Descripcion:
  Recolecta periodicamente hipervinculos del portal institucional de CFE
  evadiendo el bloqueo WAF/HTTP 403 Forbidden mediante un navegador en segundo
  plano (Headless). Genera contratos JSON estandarizados con UUID para el modulo EXTRACTOR.

Autor: Modulo Request / Recoleccion Web
"""

import json
import os
import time
import uuid
from datetime import datetime
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.common.exceptions import WebDriverException, TimeoutException


# Parche de seguridad para evitar errores al destruir el proceso Chrome en servidores Linux
def _del_silencioso(self):
    try:
        self.quit()
    except Exception:
        pass

uc.Chrome.__del__ = _del_silencioso


def cargar_json(ruta_archivo: str) -> list:
    """
    Carga de forma segura un archivo JSON.
    Retorna una lista vacia si el archivo no existe o contiene un formato invalido,
    registrando la causa exacta para trazabilidad.
    """
    if os.path.exists(ruta_archivo):
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                contenido = json.load(archivo)
                if isinstance(contenido, list):
                    return contenido
        except json.JSONDecodeError as err_json:
            print(f"Error de formato JSON en {ruta_archivo}: {err_json}")
        except IOError as err_io:
            print(f"Error de lectura de archivo E/S en {ruta_archivo}: {err_io}")
    return []


def guardar_json(ruta_archivo: str, datos: list) -> bool:
    """
    Escribe una lista de contratos en un archivo JSON estandarizado.
    """
    try:
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
        return True
    except IOError as err_io:
        print(f"Error al escribir en el archivo {ruta_archivo}: {err_io}")
        return False


def inicializar_driver_headless() -> uc.Chrome:
    """
    Configura e inicializa el navegador Chrome en modo Headless (sin interfaz grafica)
    para ejecutarse en servidores Linux CLI sin entorno de escritorio X11.
    """
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")  # Renderizado en memoria RAM sin ventana
    options.add_argument("--no-sandbox")   # Requerido para entornos de servidor/Docker
    options.add_argument("--disable-dev-shm-usage")  # Previene bloqueos por memoria compartida
    options.add_argument("--disable-gpu")  # Desactiva aceleracion grafica no disponible en CLI
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )

    try:
        driver = uc.Chrome(options=options, headless=True)
        return driver
    except WebDriverException as err_driver:
        print(f"Error critico de inicializacion de Selenium/WebDriver: {err_driver}")
        raise err_driver


def extraer_enlaces_cfe(url_objetivo: str) -> list:
    """
    Navega a la URL objetivo, espera la carga del DOM y procesa la estructura
    HTML mediante BeautifulSoup4 para extraer hipervinculos validos con UUID.
    """
    contratos_lote = []
    driver = None

    try:
        driver = inicializar_driver_headless()
        driver.set_page_load_timeout(30)

        print(f"Conectando a la fuente oficial: {url_objetivo}")
        driver.get(url_objetivo)
        time.sleep(5)  # Espera para renderizado de JavaScript dinamico y bypass de anti-bot

        html_contenido = driver.page_source
        soup = BeautifulSoup(html_contenido, "html.parser")
        etiquetas_a = soup.find_all("a", href=True)

        timestamp_iso = datetime.now().isoformat()

        for etiqueta in etiquetas_a:
            href_relativo = etiqueta.get("href", "").strip()

            # Descartar anclas internas, vacios y scripts ejecutables
            if (
                not href_relativo
                or href_relativo.startswith("#")
                or href_relativo.lower().startswith("javascript:")
                or href_relativo.lower().startswith("mailto:")
            ):
                continue

            url_absoluta = urljoin(url_objetivo, href_relativo)

            if url_absoluta.startswith(("http://", "https://")):
                # Evitar duplicados dentro del mismo lote recolectado
                if not any(item["url"] == url_absoluta for item in contratos_lote):
                    contratos_lote.append({
                        "uuid": str(uuid.uuid4()),
                        "source": "CFE",
                        "url": url_absoluta,
                        "retrieved": timestamp_iso
                    })

        return contratos_lote

    except TimeoutException:
        print(f"Tiempo de espera agotado al conectar a: {url_objetivo}")
        return []
    except WebDriverException as err_web:
        print(f"Error durante la navegacion con WebDriver: {err_web}")
        return []
    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass


def monitorear_cfe(
    url_objetivo: str = "https://cfe.mx",
    archivo_historico: str = "historico_cfe.json",
    archivo_extractor: str = "contrato_cfe.json"
):
    """
    Ejecuta el ciclo de recoleccion para un segmento de tiempo determinado.
    Calcula el delta (novedades) contra el historico acumulado, actualiza
    la persistencia local y genera el contrato JSON listo para el modulo EXTRACTOR.
    """
    print("\n==================================================")
    print(f"CICLO RECOLECTOR CFE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("==================================================")

    # 1. Cargar historico acumulado
    lista_historica = cargar_json(archivo_historico)
    urls_historicas = {item["url"] for item in lista_historica if isinstance(item, dict) and "url" in item}

    # 2. Extraer hipervinculos del lote actual
    lote_actual = extraer_enlaces_cfe(url_objetivo)
    print(f"Hipervinculos detectados en el portal: {len(lote_actual)}")

    # 3. Identificar novedades (delta no procesado previamente)
    nuevos_contratos = []
    for contrato in lote_actual:
        if contrato["url"] not in urls_historicas:
            nuevos_contratos.append(contrato)
            lista_historica.append(contrato)
            urls_historicas.add(contrato["url"])

    # 4. Actualizar historico local
    guardar_json(archivo_historico, lista_historica)

    # 5. Generar contrato entregable para el modulo EXTRACTOR
    guardar_json(archivo_extractor, nuevos_contratos)

    print(f"Novedades identificadas para el EXTRACTOR: {len(nuevos_contratos)}")
    print(f"Registros acumulados en historico: {len(lista_historica)}")
    print(f"Archivo entregable generado: {archivo_extractor}\n")


if __name__ == "__main__":
    # URL oficial de la Comision Federal de Electricidad
    URL_OFICIAL_CFE = "https://cfe.mx"
    monitorear_cfe(url_objetivo=URL_OFICIAL_CFE)
