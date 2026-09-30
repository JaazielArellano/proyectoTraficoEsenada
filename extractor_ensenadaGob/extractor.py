import requests
from bs4 import BeautifulSoup
import json
import time

#############################
    # WEBSCRAPING / Extractor 
#############################
def extractor_links():
    rss_url = "https://www.ensenada.gob.mx/?feed=rss2"  # URL del RSS de la pagina web
    #respuesta = requests.get(RSS_URL)
    respuesta = requests.get(rss_url, verify=False)     # Obtener el RSS
    soup = BeautifulSoup(respuesta.text, "xml")         # Analizar el XML
    noticias = soup.find_all("item")                    # Buscar todas las noticias del RSS
    lista_links=[]                                      # Lista que guarda los links
    for noticia in noticias:                            # Extraer solamente los links
     link = noticia.find("link")                        # En la noticia busca la etiquta link
     if link:
        lista_links.append(link.text)                   # Guarda los links en la lista
    return lista_links                                  # Regresa la lista de links

################################
#  GUARDAR NOTICIAS EN UN JSON 
################################
def guardar_noticias(noticias):                                     # Funcion para guardar noticias 
    with open("noticias_ensenada.json", "w") as archivo:            # Abir un archivo para escribir información
          json.dump(
            noticias,
            archivo,
            ensure_ascii=False,
            indent=4
        )

################################
#  ACTUALIZAR NOTICIAS  
################################
def actualizar_noticias(noticias):
    nuevos_links=extractor_links()
    noticias_guardadas=noticias
    noticias_nuevas=[]                                                                  # Aqui guardaremos solo los links nuevos

    for link in nuevos_links:
        if link not in noticias_guardadas:
            noticias_guardadas.append(link)                                             # Agregamos al historial de noticias
            noticias_nuevas.append(link)                                                # Agregar las noticias nuevas
    guardar_noticias(noticias_guardadas)

    if noticias_nuevas:
     print("Estas son las nuevas noticias:")
     for link in noticias_nuevas:
        print(link)
        with open("noticias_nuevas.json", "w", encoding="utf-8") as archivo:                     # Guarda por separado unicamente las noticias nuevas
            json.dump(noticias_nuevas, archivo, ensure_ascii=False, indent=4)

    else:
        print("No se encontraron noticias nuevas.")
    print()
    print("Noticias nuevas:", len(noticias_nuevas))                                              # Nos muestra si hay nuevas noticias
    print("Total de noticias guardadas:", len(noticias_guardadas))                               # Total de noticias guardadas 

while True:
    with open("noticias_historial_ensenada.json", "r", encoding="utf-8") as archivo:             # Leer el historial cada vez que se revisan las noticias
        datos = json.load(archivo)
    actualizar_noticias(datos)                                                                   # Revisar el RSS y guardar los links nuevos
    print()
    print("Esperando para volver a revisar...")
    print()
    time.sleep(60)                                                                               # Esperar 1 min antes de repetir el proceso 
