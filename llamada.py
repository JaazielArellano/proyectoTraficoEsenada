"""
Módulo Request / Collector - Extratron (CFE)
Genera el contrato JSON estandarizado para la integración entre módulos.
Campos obligatorios:
  - source: Nombre de la página ("CFE")
  - url: Enlace recolectado o RSS
  - retrieved: Fecha y hora exacta de recolección
"""

import json
import os
import time
from datetime import datetime
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import urllib3

# Desactivar advertencias de certificados SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def cargar_contratos_existentes(archivo_json):
    """Carga los contratos previamente guardados."""
    if os.path.exists(archivo_json):
        try:
            with open(archivo_json, "r", encoding="utf-8") as f:
                datos = json.load(f)
                if isinstance(datos, list):
                    return {item["url"]: item for item in datos if "url" in item}
        except Exception:
            return {}
    return {}


def guardar_contratos(archivo_json, lista_contratos):
    """Guarda la lista de contratos en formato JSON."""
    with open(archivo_json, "w", encoding="utf-8") as f:
        json.dump(lista_contratos, f, ensure_ascii=False, indent=4)


def obtener_contratos_cfe(url_objetivo):
    """
    Inspecciona la fuente de la CFE y construye el contrato estandarizado.
    """
    contratos_extraidos = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    try:
        response = requests.get(url_objetivo, headers=headers, timeout=15, verify=False)
        print(f"📊 Código de respuesta HTTP: {response.status_code}")
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        etiquetas_a = soup.find_all("a", href=True)

        # Marca temporal exacta para el campo 'retrieved'
        timestamp_recoleccion = datetime.now().isoformat()

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
                if not any(item["url"] == link_absoluto for item in contratos_extraidos):
                    # Estructura del contrato solicitada
                    contratos_extraidos.append({
                        "source": "CFE",
                        "url": link_absoluto,
                        "retrieved": timestamp_recoleccion
                    })

        return contratos_extraidos

    except Exception as error:
        print(f"❌ Error al consultar la fuente: {error}")
        return []


def ejecutar_recoleccion(
    url_objetivo="https://www.cfe.mx",
    archivo_json="contrato_cfe.json"
):
    print("=== GENERANDO CONTRATO JSON PARA EL MÓDULO REQUEST (CFE) ===\n")
    
    # 1. Cargar contratos históricos
    existentes_dict = cargar_contratos_existentes(archivo_json)

    # 2. Consultar portal de CFE
    print(f"🔍 Consultando: {url_objetivo}")
    nuevos_contratos = obtener_contratos_cfe(url_objetivo)
    print(f"📥 Enlaces recolectados de la fuente: {len(nuevos_contratos)}")

    # 3. Evitar duplicados
    agregados = 0
    for contrato in nuevos_contratos:
        if contrato["url"] not in existentes_dict:
            existentes_dict[contrato["url"]] = contrato
            agregados += 1

    # 4. Guardar archivo final
    lista_final = list(existentes_dict.values())
    guardar_contratos(archivo_json, lista_final)
    
    print(f"✅ Archivo '{archivo_json}' guardado con éxito.")
    print(f"🎉 Contratos nuevos agregados: {agregados}. Total acumulado: {len(lista_final)}")


if __name__ == "__main__":
    ejecutar_recoleccion()

