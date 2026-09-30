import json
import os
import time
from datetime import datetime
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

# PARCHE: Silenciar advertencias al cerrar Chrome en Windows
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
                if isinstance(datos, dict) and "urls" in datos:
                    return {url: {"url": url} for url in datos["urls"]}
                elif isinstance(datos, list):
                    return {item["url"]: item for item in datos}
        except Exception:
            return {}
    return {}


def guardar_enlaces(archivo_json, lista_enlaces):
    """Guarda la lista de enlaces en formato JSON."""
    with open(archivo_json, "w", encoding="utf-8") as f:
        json.dump(lista_enlaces, f, ensure_ascii=False, indent=4)


def obtener_enlaces_actuales(url_objetivo):
    """Abre Chrome en segundo plano (headless) y extrae todos los enlaces href de CFE."""
    enlaces_extraidos = []
    driver = None

    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    try:
        try:
            driver = uc.Chrome(options=options, version_main=153, headless=True)
        except Exception:
            driver = uc.Chrome(options=options, headless=True)

        driver.get(url_objetivo)
        time.sleep(6)  # Espera para carga dinámica de JavaScript

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")

        # Buscar todas las etiquetas <a> con atributo href
        etiquetas_a = soup.find_all("a", href=True)

        for a in etiquetas_a:
            href_relativo = a.get("href", "").strip()

            if (
                not href_relativo
                or href_relativo.startswith("#")
                or href_relativo.lower().startswith("javascript:")
            ):
                continue

            link_absoluto = urljoin(url_objetivo, href_relativo)

            if not link_absoluto.startswith(("http://", "https://")):
                continue

            if not any(item["url"] == link_absoluto for item in enlaces_extraidos):
                texto_titulo = a.get_text(strip=True) or "[Sin texto]"
                enlaces_extraidos.append(
                    {
                        "source": "cfe",
                        "titulo": texto_titulo,
                        "url": link_absoluto,
                        "url_relativa": href_relativo,
                        "es_boletin": (
                            "boletin" in link_absoluto.lower()
                            or "prensa" in link_absoluto.lower()
                            or "i=" in link_absoluto
                        ),
                        "retrieved_at": datetime.now().isoformat()
                    }
                )

        return enlaces_extraidos

    except Exception as error:
        print(f"❌ Error al conectar con CFE: {error}")
        return []

    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass


def monitorear_cfe(
    url_objetivo="https://www.cfe.mx",
    archivo_json="links_cfe.json",
    minutos_espera=10,
):
    print("=== INICIANDO SERVICIO DE MONITOREO CONTINUO CFE (SEGUNDO PLANO) ===\n")

    try:
        while True:
            existentes_dict = cargar_enlaces_existentes(archivo_json)

            print(f"🔍 Consultando portal CFE ({url_objetivo})...")
            enlaces_actuales = obtener_enlaces_actuales(url_objetivo)
            print(f"📥 Enlaces href encontrados en la página: {len(enlaces_actuales)}")

            nuevos_enlaces = []
            for item in enlaces_actuales:
                if item["url"] not in existentes_dict:
                    nuevos_enlaces.append(item)

            if nuevos_enlaces:
                print(f"🎉 ¡Se encontraron {len(nuevos_enlaces)} enlaces nuevos!")
                for nuevo in nuevos_enlaces[:5]:
                    print(f"    • [{nuevo['titulo'][:40]}] -> {nuevo['url']}")

                todos_los_enlaces = list(existentes_dict.values()) + nuevos_enlaces
                guardar_enlaces(archivo_json, todos_los_enlaces)
                print(f"✅ Archivo '{archivo_json}' actualizado con éxito. Total acumulado: {len(todos_los_enlaces)}")
            else:
                print("ℹ️ No se encontraron enlaces nuevos respecto a 'links_cfe.json'.")

            print(f"⏳ Esperando {minutos_espera} minutos para la siguiente búsqueda...\n")
            time.sleep(minutos_espera * 60)

    except KeyboardInterrupt:
        print("\n Monitoreo detenido manualmente por el usuario de forma limpia.")


if __name__ == "__main__":
    monitorear_cfe()


