

import json
import os
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def cargar_enlaces_existentes(archivo_json):
    """Carga la lista de URLs guardadas previamente en el objeto JSON."""
    if os.path.exists(archivo_json):
        try:
            with open(archivo_json, "r", encoding="utf-8") as f:
                datos = json.load(f)
                if isinstance(datos, dict) and "urls" in datos:
                    return set(datos["urls"])
        except Exception:
            return set()
    return set()


def guardar_enlaces(archivo_json, lista_urls):
    """Guarda la lista de URLs en el formato {"urls": [...]} exactamente como en la imagen."""
    estructura_json = {
        "urls": list(lista_urls)
    }
    with open(archivo_json, "w", encoding="utf-8") as f:
        json.dump(estructura_json, f, ensure_ascii=False, indent=4)


def obtener_enlaces_actuales(url_objetivo):
    """Abre Chrome en segundo plano, espera a que carguen las etiquetas <a> y extrae los href."""
    enlaces_extraidos = []
    driver = None

    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    try:
        try:
            driver = uc.Chrome(options=options, version_main=153, headless=True)
        except Exception:
            driver = uc.Chrome(options=options, headless=True)

        driver.get(url_objetivo)

        # Esperar hasta 15 segundos a que el DOM cargue al menos un elemento <a>
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "a"))
        )

        # Hacer scroll hacia abajo para activar scripts dinámicos
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
        time.sleep(3)

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")

        etiquetas_a = soup.find_all("a", href=True)
        print(f" Título obtenido: {driver.title}")
        print(f" Total de etiquetas <a> encontradas en el DOM: {len(etiquetas_a)}")

        for a in etiquetas_a:
            href_relativo = a.get("href", "").strip()

            if (
                not href_relativo
                or href_relativo.startswith("#")
                or href_relativo.lower().startswith("javascript:")
            ):
                continue

            link_absoluto = urljoin(url_objetivo, href_relativo)

            if link_absoluto.startswith(("http://", "https://")):
                if link_absoluto not in enlaces_extraidos:
                    enlaces_extraidos.append(link_absoluto)

        return enlaces_extraidos

    except Exception as error:
        print(f" Error durante el escaneo: {error}")
        return []

    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass


def monitorear_cfe(
    url_objetivo="https://www.cfe.mx/Pages/default.aspx",
    archivo_json="links_cfe.json",
    minutos_espera=10,
):
    print("=== INICIANDO COLLECTOR CFE EN SEGUNDO PLANO ===\n")

    try:
        while True:
            existentes_set = cargar_enlaces_existentes(archivo_json)

            print(f"Escaneando {url_objetivo}...")
            enlaces_actuales = obtener_enlaces_actuales(url_objetivo)

            nuevos_enlaces = [url for url in enlaces_actuales if url not in existentes_set]

            if nuevos_enlaces:
                print(f"\n🎉 ¡Se encontraron {len(nuevos_enlaces)} enlaces nuevos!")
                for nuevo in nuevos_enlaces[:5]:
                    print(f"    • {nuevo}")

                # Unir los existentes con los nuevos evitando duplicados
                todos_los_enlaces = existentes_set.union(set(nuevos_enlaces))
                guardar_enlaces(archivo_json, todos_los_enlaces)
                print(f"Archivo '{archivo_json}' actualizado con {len(todos_los_enlaces)} enlaces acumulados.\n")
            else:
                print("ℹ No se encontraron enlaces nuevos en esta ronda.\n")

            print(f"⏳ Esperando {minutos_espera} minutos para el siguiente ciclo...\n")
            time.sleep(minutos_espera * 60)

    except KeyboardInterrupt:
        print("\n Monitoreo detenido por el usuario.")


if __name__ == "__main__":
    monitorear_cfe()