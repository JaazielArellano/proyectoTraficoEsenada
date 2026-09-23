"""
Módulo scraper para extraer los títulos y enlaces de noticias
del portal ensenada.net utilizando BeautifulSoup y requests.
"""

import json
import os
import time
import uuid
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# Configuración principal
URL_BASE = "https://www.ensenada.net/"
# 600 segundos = 10 minutos | pruebas con 10 segundos
# (cambiar a 600 al momento de realizar la ejecución final)
TIEMPO_ESPERA = 10
ARCHIVO_PASADAS = "noticias_pasadas.json"
ARCHIVO_NUEVAS = "noticias_nuevas.json"

def extraer_noticias():
    """Conecta a ensenada.net y extrae los links con la estructura solicitada."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        respuesta = requests.get(URL_BASE, headers=headers, timeout=10)
        # Forzamos latin-1 para evitar problemas de caracteres extraños
        respuesta.encoding = 'latin-1'
        soup = BeautifulSoup(respuesta.text, "html.parser")

        lista_noticias = []

        # Búsqueda de todas las etiquetas <a>
        for etiqueta_a in soup.find_all("a", href=True):
            href = etiqueta_a["href"]
            texto = etiqueta_a.get_text(" ", strip=True)

            # Filtro para ignorar links vacíos.
            if texto:
                full_url = urljoin(URL_BASE, href)

                lista_noticias.append({
                    "id": str(uuid.uuid4()),
                    "titulo": texto,
                    "url": full_url,
                    "retrieved_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                })

        return lista_noticias

    except requests.RequestException as error:
        print(f"❌ Error de conexión: {error}")
        return []

def cargar_historial(ruta_archivo):
    """Carga el JSON de noticias viejas si existe."""
    if os.path.exists(ruta_archivo):
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except json.JSONDecodeError:
            return []
    return []

def guardar_json(ruta_archivo, datos):
    """Sobreescribe un archivo JSON con los datos proporcionados."""
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

def ciclo_scraper():
    """Ejecuta una ronda de extracción, comparación y guardado."""
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Escaneando ensenada.net...")

    # 1. Cargar el historial acumulado
    historial_pasadas = cargar_historial(ARCHIVO_PASADAS)

    # Crear un 'set' de URLs pasadas para hacer la comparación súper rápida
    urls_pasadas_set = {item["url"] for item in historial_pasadas}

    # 2. Extraer las noticias actuales de la página
    noticias_actuales = extraer_noticias()
    noticias_nuevas = []

    # 3. Filtrar cuáles son realmente nuevas
    for noticia in noticias_actuales:
        if noticia["url"] not in urls_pasadas_set:
            noticias_nuevas.append(noticia)
            historial_pasadas.append(noticia) # Añadirla al historial para el futuro

    # 4. Guardar los resultados en sus respectivos archivos
    guardar_json(ARCHIVO_NUEVAS, noticias_nuevas)
    guardar_json(ARCHIVO_PASADAS, historial_pasadas)

    # 5. Reporte en terminal
    print("✅ Extracción completada.")
    print(f"📂 Noticias pasadas (historial total): {len(historial_pasadas)}")
    print(f"🆕 Noticias nuevas encontradas: {len(noticias_nuevas)}")

if __name__ == "__main__":
    print("🚀 Iniciando servicio automatizado de extracción de enlaces...")
    print("⚠️  Presiona Ctrl + C en la terminal para detenerlo.\n")

    while True:
        ciclo_scraper()
        print("⏳ Esperando 10 minutos para la siguiente ejecución...")
        time.sleep(TIEMPO_ESPERA)
