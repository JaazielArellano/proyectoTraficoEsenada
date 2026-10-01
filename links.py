"""
Script para extraer los enlaces (href) y atributos de la CFE evadiendo Imperva.
Guarda los resultados en un archivo JSON y en un CSV.
"""

import csv
import json
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import setuptools  # Mantiene compatibilidad con distutils en Python 3.12/3.13
import undetected_chromedriver as uc


def extraer_hrefs_cfe(
    url_base="https://www.cfe.gob.mx/Pages/default.aspx",
    archivo_json="detalles_etiquetas_cfe.json",
    archivo_csv="enlaces_cfe.csv",
):
    resultados = []

    print(f"Iniciando Chrome evadido para conectar a {url_base}...")

    # Configuración de opciones para el navegador
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    try:
        # Se especifica version_main=153 para alinear con tu navegador instalado
        driver = uc.Chrome(options=options, version_main=153)
    except Exception:
        # Respaldo si Chrome se actualizó automáticamente
        driver = uc.Chrome(options=options)

    try:
        driver.get(url_base)

        # Esperar 8 segundos a que se resuelva la pantalla de validación de Imperva
        print("Esperando la resolución del firewall y renderizado DOM...")
        driver.implicitly_wait(8)

        # Obtener el HTML procesado tras superar la validación
        html_content = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html_content, "html.parser")

        # 1. Selector específico para la sección de boletines/noticias (div.entry-title h4 a)
        etiquetas_seleccionadas = soup.select("div.entry-title a")

        # 2. Si no encuentra esa clase, extrae todas las etiquetas <a> con href
        if not etiquetas_seleccionadas:
            etiquetas_seleccionadas = soup.find_all("a", href=True)

        for a in etiquetas_seleccionadas:
            href_raw = a.get("href", "").strip()

            # Omitir enlaces vacíos, fragmentos locales o scripts
            if (
                not href_raw
                or href_raw.startswith("#")
                or "javascript" in href_raw.lower()
            ):
                continue

            # Convertir URL relativa a URL completa/absoluta
            link_completo = urljoin(url_base, href_raw)

            # Evitar URLs duplicadas
            if not any(
                item["href_absoluto"] == link_completo for item in resultados
            ):
                info_etiqueta = {
                    "texto": a.text.strip() or "[Sin texto]",
                    "href_absoluto": link_completo,
                    "href_original": href_raw,
                    "atributos": a.attrs,
                    "html_completo": str(a),
                }
                resultados.append(info_etiqueta)

        print(
            f"\n¡Conexión exitosa! Se extrajeron {len(resultados)} enlaces (href).\n"
        )

        # Mostrar las primeras 5 entradas en consola
        for i, item in enumerate(resultados[:5], 1):
            print(f"--- ENLACE {i} ---")
            print(f"Texto:    {item['texto']}")
            print(f"URL href: {item['href_absoluto']}")
            print(f"Atributos:{item['atributos']}\n")

        if len(resultados) > 5:
            print(f"... y {len(resultados) - 5} enlaces más.")

        # Exportar a JSON
        with open(archivo_json, "w", encoding="utf-8") as f_json:
            json.dump(resultados, f_json, ensure_ascii=False, indent=4)

        # Exportar a CSV
        with open(
            archivo_csv, "w", newline="", encoding="utf-8-sig"
        ) as f_csv:
            writer = csv.DictWriter(
                f_csv, fieldnames=["texto", "href_absoluto", "href_original"]
            )
            writer.writeheader()
            for r in resultados:
                writer.writerow(
                    {
                        "texto": r["texto"],
                        "href_absoluto": r["href_absoluto"],
                        "href_original": r["href_original"],
                    }
                )

        print(
            f"\nArchivos '{archivo_json}' y '{archivo_csv}' generados correctamente."
        )

    except Exception as error:
        print(f"Error durante el proceso: {error}")
        try:
            driver.quit()
        except Exception:
            pass


if __name__ == "__main__":
    extraer_hrefs_cfe()