
import json
import os
from datetime import datetime
import requests

#Token y URL
TOKEN_APIFY = "apify_api_dxVgg3H5s2OOWgJhjnOqfCgy2CJxmn2ZSGLq"
URL_FUENTE = "https://x.com/EnsenadaNews"
ARCHIVO_CACHE = "noticias_x.json"

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


def cargar_cache(ruta_archivo):

    if os.path.exists(ruta_archivo):
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def guardar_cache(ruta_archivo, lista_registros):

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        json.dump(lista_registros, f, ensure_ascii=False, indent=4)


def buscar_palabra_clave(texto, lista_palabras):
    
    texto_min = texto.lower()
    
    for palabra in lista_palabras:
        posicion = texto_min.find(palabra)
        if posicion != -1:
            
            inicio = posicion + len(palabra)
            subcadena = texto[inicio:].strip()

            
            for separador in [",", ".", "\n"]:
                if separador in subcadena:
                    subcadena = subcadena.split(separador)[0]

            resultado = subcadena.strip()
            if resultado:
                return resultado

    return "No detectado"


def extraer_ubicacion(texto_post):

    if not texto_post:
        return "No detectado", "No detectado", "bajo"

    prefijos_calle = ["calle ", "av. ", "avenida ", "blvd. ", "bulevar ", "calzada "]
    prefijos_colonia = ["col. ", "colonia ", "fracc. ", "fraccionamiento ", "ejido ", "barrio "]

    calle = buscar_palabra_clave(texto_post, prefijos_calle)
    colonia = buscar_palabra_clave(texto_post, prefijos_colonia)

    #Nivel de Confianza
    if calle != "No detectado" and colonia != "No detectado":
        confianza = "alto"
    elif calle != "No detectado" or colonia != "No detectado":
        confianza = "medio"
    else:
        confianza = "bajo"

    return calle, colonia, confianza


def obtener_fecha_y_dia(fecha_bruta):

    if fecha_bruta:
        try:
            limpio = str(fecha_bruta).replace("Z", "+00:00")
            dt = datetime.fromisoformat(limpio)
            return dt.strftime("%Y-%m-%d"), DIAS_SEMANA[dt.weekday()]
        except Exception:
            pass

    hoy = datetime.now()
    return hoy.strftime("%Y-%m-%d"), DIAS_SEMANA[hoy.weekday()]


def solicitar_datos_apify():

    endpoint = (
        f"https://api.apify.com/v2/acts/apidojo~tweet-scraper"
        f"/run-sync-get-dataset-items?token={TOKEN_APIFY}"
    )

    cuerpo_peticion = {
        "startUrls": [URL_FUENTE],
        "maxItems": 15
    }

    print("Obteniendo publicaciones...")
    try:
        respuesta = requests.post(endpoint, json=cuerpo_peticion, timeout=60)
        if respuesta.status_code in [200, 201]:
            return respuesta.json()
        print(f"Error HTTP en la API: {respuesta.status_code}")
        return []
    except Exception as e:
        print(f"Error de red al conectar con Apify: {e}")
        return []


def main():
    registros = cargar_cache(ARCHIVO_CACHE)
    urls_existentes = {item["url"] for item in registros if "url" in item}

    items_brutos = solicitar_datos_apify()
    nuevos_registros = 0

    for item in items_brutos:
        raw_url = item.get("url") or item.get("twitterUrl") or item.get("tweetUrl") or ""
        url_limpia = raw_url.split("?")[0] if raw_url else ""

        #Evitar publicaciones sin URL o duplicadas en el caché
        if not url_limpia or url_limpia in urls_existentes:
            continue

        texto = item.get("full_text") or item.get("text") or ""
        fecha_raw = item.get("createdAt") or item.get("created_at") or item.get("date")

        fecha_str, dia_str = obtener_fecha_y_dia(fecha_raw)
        calle, colonia, confianza = extraer_ubicacion(texto)

        #Salida del JSON con la estructura requerida por el contrato
        registro_estructurado = {
            "url": url_limpia,
            "fecha": fecha_str,
            "dia": dia_str,
            "calle": calle,
            "colonia": colonia,
            "confianza": confianza
        }

        registros.append(registro_estructurado)
        urls_existentes.add(url_limpia)
        nuevos_registros += 1

    guardar_cache(ARCHIVO_CACHE, registros)

    print(f"\nProceso finalizado.")
    print(f"- Nuevas publicaciones agregadas: {nuevos_registros}")
    print(f"- Total acumulado en '{ARCHIVO_CACHE}': {len(registros)}")


if __name__ == "__main__":
    main()