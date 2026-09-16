import requests
from bs4 import BeautifulSoup
import json

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
urls= extractor_links()                                 # Ejecuta la funcion que extrae los links 
print(urls)                                             # Muestra/Imprime los links guardados en la lista


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

guardar_noticias(urls)

with open("noticias_ensenada.json", "r") as archivo:
    datos = json.load(archivo)



print("Links extraidos RSS")


print(urls)
print("----"*30)

print("Contenido del JSON")
print(datos)



################################
#  ACTUALIZAR NOTICIAS  
################################

def actualizar_noticias(noticias):