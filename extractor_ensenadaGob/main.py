# Extrae y guarda enlaces de noticias de Ensenada.
import json

import requests
from bs4 import BeautifulSoup

#############################
# WEBSCRAPING / Extractor
#############################

# URL del RSS de la pagina web
def extractor_links():
    #Extrae los enlaces de las noticias del RSS.
    rss_url="https://www.ensenada.gob.mx/?feed=rss2"

    # Obtener el RSS
    respuesta = requests.get(rss_url, verify=False)

    # Analizar el XML
    soup = BeautifulSoup(respuesta.text, "xml")

    # Buscar todas las noticias del RSS
    noticias = soup.find_all("item")

    # Lista que guarda los links
    lista_links=[]

    # Extraer solamente los links
    for noticia in noticias:
        # Buscar la etiqueta link
        link = noticia.find("link")
        
        # Guarda los links en la lista
        if link:
            lista_links.append(link.text)

    return lista_links

################################
# GUARDAR NOTICIAS EN UN JSON
################################

# Guarda las noticias en el archivo de historial
def guardar_noticias(noticias):

    with open(
        "noticias_historial_ensenada.json",
        "w",
        encoding="utf-8"
    ) as archivo_salida:
        json.dump(
            noticias,
            archivo_salida,
            ensure_ascii=False,
            indent=4
        )

################################
# ACTUALIZAR NOTICIAS
################################

def actualizar_noticias(noticias):
    # Actualiza el historial y muestra las noticias nuevas
    nuevos_links=extractor_links()
    noticias_guardadas=noticias

    # Aqui guardaremos solo los links nuevos
    noticias_nuevas=[]

    for link in nuevos_links:
        if link not in noticias_guardadas:

            # Agregamos al historial de noticias
            noticias_guardadas.append(link)

            # Agregar las noticias nuevas
            noticias_nuevas.append(link)

    guardar_noticias(noticias_guardadas)

    if noticias_nuevas:
        print("Estas son las nuevas noticias:")

        for link in noticias_nuevas:
            print(link)

        with open(
            "noticias_nuevas_ensenada.json",
            "w",
            encoding="utf-8"
            ) as archivo:

            # Guarda por separado unicamente las noticias nuevas
            json.dump(
                {"urls": noticias_nuevas},
                archivo,
                ensure_ascii=False,
                indent=4)
    else:
        print("No se encontraron noticias nuevas.")

    print()

     # Nos muestra si hay nuevas noticias
    print("Noticias nuevas:", len(noticias_nuevas))

    # Total de noticias guardadas
    print("Total de noticias guardadas:", len(noticias_guardadas))

while True:
    # Leer el historial cada vez que se revisan las noticias
    with open(
        "noticias_historial_ensenada.json",
        "r",
        encoding="utf-8"
    ) as archivo:
        datos = json.load(archivo)

    # Revisar el RSS y guardar los links nuevos
    actualizar_noticias(datos)

    print()
    print("Esperando para volver a revisar...")
    print()
    # time.sleep(60)  # Esperar 1 min antes de repetir el proceso
