from datetime import datetime
from bs4 import BeautifulSoup
import requests


def obtener_limpiar_pagina(url):
    # PASO 1: REQUEST (Descargar la página) 
    # Uso cabeceras sencillas para identificar como un navegador web
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0"
    }

    try:
        # llamar HTTP con un tiempo límite de 10 segundos
        #respuesta = requests.get(url, headers=headers, timeout=10)
        respuesta = requests.get(url, headers=headers, timeout=10, verify=False)
        # Verificar si la respuesta fue exitosa (código 200)
        respuesta.raise_for_status()
    except Exception as error:
        print(f"Error al descargar la página: {error}")
        return None

    # fecha y hora actual en formato estándar
    fecha_consulta = datetime.now().isoformat()

    # Limpiar el HTML
    # Creacion del objeto para analizar el HTML
    soup = BeautifulSoup(respuesta.text, "html.parser")

    # Eliminar las partes irrelevantes (scripts, estilos, navegación y pie de página)
    for elemento in soup(["script", "style", "nav", "footer", "header"]):
        elemento.decompose()

    # Extraccion el texto limpio,   bloques con saltos de línea
    texto_bruto = soup.get_text(separator="\n")

    # Normalizacion texto: quitamos espacios extra e líneas vacías
    lineas = [linea.strip() for linea in texto_bruto.splitlines()]
    lineas_limpias = [linea for linea in lineas if linea]
    texto_final = "\n".join(lineas_limpias)

    #Formato requerido para el Extractor
    resultado = {
        "source": "CFE",
        "url": url,
        "retrieved_at": fecha_consulta,
        "text": texto_final,
    }

    return resultado


# EJEMPLO  
if __name__ == "__main__":
    # URL de prueba (puedes cambiarla por la sección de CFE que estés analizando)
    url_cfe = "https://www.cfe.mx"

    datos_limpios = obtener_limpiar_pagina(url_cfe)

    if datos_limpios:
        print("--- ÉXITO: CONTRATO GENERADO PARA EL EXTRACTOR ---")
        print(f"Fuente: {datos_limpios['source']}")
        print(f"URL: {datos_limpios['url']}")
        print(f"Fecha: {datos_limpios['retrieved_at']}")
        print("\n--- MUESTRA DEL TEXTO LIMPIO ---")
        print(
            datos_limpios["text"][:250]
            )  # Muestra solo los primeros 300 caracteres