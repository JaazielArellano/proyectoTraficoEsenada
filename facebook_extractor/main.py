#MARTIN ROBERTO GONZALEZ ORTIZ
#COMPORTAMIENTO DE DATOS

"""Módulo para la extracción, procesamiento y almacenamiento de noticias de Facebook.

Extrae datos mediante la API de Apify y los guarda en caché local con
información de ubicación y fechas normalizadas.
"""

import json
import os
import re
from datetime import datetime
import requests

# --- CONFIGURACIÓN ---
ARCHIVO_CACHE = "noticias_facebook_json.json"
MI_APIFY_TOKEN = "apify_api_Vj7kz88fHNwWSNunVBjoZBTzD46RJZ0G7q0h"

# Días de la semana en español
DIAS_SEMANA = {
    0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves",
    4: "Viernes", 5: "Sábado", 6: "Domingo"
}


def cargar_cache(nombre_archivo):
    """Carga los registros previamente guardados."""
    if os.path.exists(nombre_archivo):
        try:
            with open(nombre_archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
                return datos.get("registros", [])
        except (json.JSONDecodeError, IOError):
            print("No se pudo leer el cache existente. Se iniciará uno nuevo.")
            return []
    return []


def guardar_cache(nombre_archivo, registros):
    """Guarda la lista acumulada de noticias procesadas."""
    datos_json = {
        "total": len(registros),
        "fuente": "Facebook - Gobierno de Ensenada",
        "registros": registros,
    }
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        json.dump(datos_json, f, ensure_ascii=False, indent=4)


def extraer_ubicacion_del_texto(texto):
    """Analiza el texto de la publicación para identificar calle y colonia."""
    if not texto:
        return "No detectado", "No detectado", "bajo"

    calle = "No detectado"
    colonia = "No detectado"
    confianza = "bajo"

    # Patrones comunes para detectar calles
    patron_calle = (
        r"(?:calle|av\.|avenida|blvd\.|bulevar|calzada)\s+"
        r"([A-ZÁÉÍÓÚÑa-záéíóúñ0-9\s]+?)(?=\s*(?:,|col\.|colonia|entre|\.|$))"
    )
    # Patrones comunes para detectar colonias/barrios
    patron_colonia = (
        r"(?:col\.|colonia|fracc\.|fraccionamiento|ejido|barrio)\s+"
        r"([A-ZÁÉÍÓÚÑa-záéíóúñ0-9\s]+?)(?=\s*(?:,|entre|\.|$))"
    )

    match_calle = re.search(patron_calle, texto, re.IGNORECASE)
    match_colonia = re.search(patron_colonia, texto, re.IGNORECASE)

    if match_calle:
        calle = match_calle.group(1).strip()
    if match_colonia:
        colonia = match_colonia.group(1).strip()

    # Determinar nivel de confianza
    if match_calle and match_colonia:
        confianza = "alto"
    elif match_calle or match_colonia:
        confianza = "medio"

    return calle, colonia, confianza


def _obtener_fecha_y_dia(raw_time):
    """Auxiliar para parsear y dar formato a la fecha del post."""
    if raw_time:
        try:
            time_clean = str(raw_time).replace("Z", "+00:00")
            dt = datetime.fromisoformat(time_clean)
            return dt.strftime("%Y-%m-%d"), DIAS_SEMANA.get(dt.weekday(), "")
        except ValueError:
            pass

    ahora = datetime.now()
    return ahora.strftime("%Y-%m-%d"), DIAS_SEMANA.get(ahora.weekday(), "")


def extractor_facebook_apify(token_apify, limite=20):
    """Extrae publicaciones de Apify y las convierte al diccionario en español."""
    base_url = "https://api.apify.com/v2/acts/apify~facebook-posts-scraper"
    endpoint = f"{base_url}/run-sync-get-dataset-items?token={token_apify}"
    payload = {
        "startUrls": [{"url": "https://www.facebook.com/GobiernoDeEnsenada"}],
        "resultsLimit": limite,
    }

    print("1. Enviando petición a Apify (extrayendo publicaciones)...")
    try:
        respuesta = requests.post(endpoint, json=payload, timeout=60)
    except requests.RequestException as error:
        print(f"Error de conexión con Apify: {error}")
        return []

    if respuesta.status_code not in [200, 201]:
        print(f"Error Apify {respuesta.status_code}: {respuesta.text}")
        return []

    items = respuesta.json()
    resultados = []

    for item in items:
        # 1. Obtener URL única
        raw_url = (
            item.get("url")
            or item.get("postUrl")
            or item.get("canonicalUrl")
            or ""
        )
        url_limpia = raw_url.split("?")[0].split("&")[0] if raw_url else ""

        # 2. Formatear Fecha y Día
        fecha_str, dia_str = _obtener_fecha_y_dia(
            item.get("time") or item.get("timestamp")
        )

        # 3. Extraer Calle, Colonia y Confianza del texto
        texto_post = item.get("text") or item.get("caption") or ""
        calle, colonia, confianza = extraer_ubicacion_del_texto(texto_post)

        resultados.append({
            "url": url_limpia,
            "fecha": fecha_str,
            "dia": dia_str,
            "calle": calle,
            "colonia": colonia,
            "confianza": confianza,
        })

    return resultados


# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    # 1. Cargar caché previo
    cache_registros = cargar_cache(ARCHIVO_CACHE)
    urls_existentes = {
        item["url"] for item in cache_registros if "url" in item
    }
    print(f"Registros previos en caché: {len(cache_registros)}")

    # 2. Extraer publicaciones de Apify
    noticias_obtenidas = extractor_facebook_apify(MI_APIFY_TOKEN, limite=20)

    if noticias_obtenidas:
        # 3. Filtrar registros no guardados previamente
        nuevos_registros = [
            item for item in noticias_obtenidas
            if item["url"] and item["url"] not in urls_existentes
        ]

        if nuevos_registros:
            cache_registros.extend(nuevos_registros)
            guardar_cache(ARCHIVO_CACHE, cache_registros)

            print("\n¡Extracción exitosa!")
            print(f"- Nuevos registros agregados hoy: {len(nuevos_registros)}")
            print(
                f"- Total acumulado en '{ARCHIVO_CACHE}': "
                f"{len(cache_registros)}\n"
            )

            print("Ejemplo de registro guardado:")
            print(
                json.dumps(
                    nuevos_registros[0], indent=4, ensure_ascii=False
                )
            )
        else:
            print("No hay publicaciones nuevas para agregar.")
    else:
        print("No se pudieron obtener publicaciones desde la API de Apify.")
