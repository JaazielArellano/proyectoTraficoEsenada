import json
import os
import requests

ARCHIVO_CACHE = "noticias_facebook.json"

def cargar_cache(nombre_archivo):
    """Carga los enlaces guardados previamente si el archivo existe."""
    if os.path.exists(nombre_archivo):
        try:
            with open(nombre_archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
                return set(datos.get("links", []))
        except (json.JSONDecodeError, IOError):
            print("No se pudo leer el cache existente. Se iniciará un cache nuevo.")
            return set()
    return set()

def guardar_cache(nombre_archivo, set_links):
    """Guarda la lista acumulada de enlaces únicos en el archivo JSON."""
    lista_ordenada = list(set_links)
    datos_json = {
        "total": len(lista_ordenada),
        "fuente": "Facebook - Gobierno de Ensenada",
        "links": lista_ordenada
    }
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        json.dump(datos_json, f, ensure_ascii=False, indent=4)

def extractor_facebook_apify(token_apify, limite=20):
    endpoint = f"https://api.apify.com/v2/acts/apify~facebook-posts-scraper/run-sync-get-dataset-items?token={token_apify}"
    payload = {
        "startUrls": [{"url": "https://www.facebook.com/GobiernoDeEnsenada"}],
        "resultsLimit": limite
    }
    
    print("Enviando petición a la nube (extrayendo publicaciones)...")
    respuesta = requests.post(endpoint, json=payload)
    
    if respuesta.status_code in [200, 201]:
        items = respuesta.json()
        nuevos_links = []
        
        for item in items:
            url = item.get("url") or item.get("postUrl") or item.get("canonicalUrl")
            if url:
                url_limpia = url.split("?")[0].split("&")[0]
                nuevos_links.append(url_limpia)
                
        return nuevos_links
    else:
        print(f"Error {respuesta.status_code}: {respuesta.text}")
        return []

# --- EJECUCIÓN PRINCIPAL CON CACHE ---

MI_APIFY_TOKEN = "apify_api_Cm5bfgiXp5vR7iB2bE5H3hTCVrwhyG2POehT"

# 1. Cargar cache existente
cache_links = cargar_cache(ARCHIVO_CACHE)
print(f"Enlaces en cache previo: {len(cache_links)}")

# 2. Extraer nuevas publicaciones desde Apify
links_obtenidos = extractor_facebook_apify(MI_APIFY_TOKEN, limite=20)

# 3. Identificar cuáles enlaces son realmente nuevos
links_nuevos = [link for link in links_obtenidos if link not in cache_links]

# 4. Actualizar el cache si hay elementos nuevos
if links_obtenidos:
    # Agregar todos los enlaces al conjunto acumulado (elimina duplicados automáticamente)
    cache_links.update(links_obtenidos)
    guardar_cache(ARCHIVO_CACHE, cache_links)
    
    print(f"\n¡Éxito! Proceso finalizado.")
    print(f"- Nuevos enlaces encontrados hoy: {len(links_nuevos)}")
    print(f"- Total de enlaces acumulados en '{ARCHIVO_CACHE}': {len(cache_links)}")
    
    if links_nuevos:
        print("\n--- NUEVOS ENLACES AGREGADOS AL CACHE ---")
        for i, link in enumerate(links_nuevos, 1):
            print(f"{i}. {link}")
    else:
        print("\n No se encontraron enlaces nuevos (todos ya estaban en el cache).")
else:
    print("\nNo se pudieron obtener enlaces desde la API.")