"""Procesa noticias para extraer fechas, días, calles y colonias."""
import re
import json
#############################
#       DETECTAR FECHAS
#############################
    # Detecta fechas dentro del texto
def detectar_fechas(texto):
# Funcion para buscar fechas fomato AAAA-MM-DD

# Creamos un diccionario que relaciona cada mes con su mumero
    meses={
        "enero": "01","febrero": "02", "marzo": "03",
        "abril": "04","mayo": "05","junio": "06",
        "julio": "07","agosto": "08","septiembre": "09",
        "octubre": "10","noviembre": "11","diciembre": "12"}

# Define el patron que debe tener la fecha
    patron = r"(\d{1,2}) de (\w+) de (\d{4})"

    # Busca en el texto una fecha que coincida con el patron
    resultado = re.search(patron, texto.lower())

# Verifica si se encontro una fecha
    if resultado:
        dia = resultado.group(1) # Obtiene el dia que se encontro
        mes = resultado.group(2) # Obtiene el mes que se encontro
        año = resultado.group(3) # Obtiene el año que se encontro

        if mes in meses:
            return f"{año}-{meses[mes]}-{int(dia):02d}"
    return None

#############################
# DETECTAR DIAS DE LA SEMANA
#############################

def detectar_dias(texto):
    # Funcion para Buscar un dia de la semana

    # Creamos una lista con todos los dias de la semana que
    dias = ["domingo","lunes","martes",
    "miércoles","jueves","viernes","sábado"]
 # Se utilizaran para comprobar si una palabra es un dia de la semana

 # Lower() convierte todo el texto a minusculas y Split() divide el texto en palabras
    palabras = texto.lower().split()

 # Recorre todas las palabras una por una
    for i, palabra in enumerate(palabras):

        # Quita de la palabra los caracteres y verifica si es un dia de la semana
        if palabra.strip(",.:") in dias:
            if i + 1 < len(palabras):
                 # selecciona  la palabra que esta despues del dia
                numero = palabras[i + 1].strip(",.:")
                 # Une el dia y el numero
                return palabra + " " + numero
    return None
# Si no encuentra ningun dia regresa None

############################
#    DETECTAR CALLES
############################

def detectar_calles(texto):
# Funcion para Buscar calles o avenidas

# Creamos una lista con diferentes formas de referirse a una calle
    tipos_calle = ["calle","avenida","av.",
    "boulevard","blvd.","calzada","carretera"]

 # Dividimos el texto en palabras separadas
    palabras=texto.split()

    # Recorre cada palabra del texto
    for i, palabra in enumerate(palabras):

        palabra_limpia=palabra.lower().strip(",.:")
        # Convertimos la palabra en minusculas y eliminamos caracteres

# Comprobamos si la palabra es uno de los tipos de calle de la lista
        if palabra_limpia in tipos_calle:
            # Verificamos que haya una palabra despues
            if i + 1 < len(palabras):
                # Obtenemos la palabra que esta exactamente despues
                nombre = palabras[i + 1].strip(",.:")
                # Une el tipo de calle y el nombre
                return palabra + " " + nombre
    return None
# Si no encuentra ningun tipo de calle regresa None

############################
#    DETECTAR COLONIAS
############################

def detectar_colonias(texto):
# Funcion para Buscar colonias

    palabras=texto.split()
    # Dividimos el texto en palabras separadas

# Recorre todas las palabras
    for i, palabra in enumerate(palabras):
        palabra_limpia = palabra.lower().strip(",.:")
        # Convertimos a minusculas y eliminamos caracteres para que solo quede la palabra "colonia"

# Comprobamos si la palabra actual es exactamente "colonia"
        if palabra_limpia == "colonia":
            # Comprueba que exista una palabra después de "colonia"
            if i + 1 < len(palabras):
                # Obtenemos la palabra que esta exactamente despues de "colonia"
                nombre = palabras[i + 1].strip(",.:")
                return nombre # Devuelve el nombre de la colonia encontrado
    return None
# Si no se encuentra la palabra "colonia" devuelve None

###########################
#  PORCENTAJE DE CONFIANZA
###########################

def porcentaje_confianza(fecha, dia, calle, colonia):
# Funcion que recibe 4 datos: fecha, dia, calle y colonia

    datos_encontrados = 0
# contador que nos ayuda a contar cuantos datos encontramos

# Verifica si se encontro una fecha y si se encontro le suma 1 al contador
    if fecha:
        datos_encontrados += 1
 # Verifica si se encontro un dia y si se encontro le suma 1 al contaor
    if dia:
        datos_encontrados += 1

 # Vericfica si se encuentro una calle y si se encontro le suma 1 al contador
    if calle:
        datos_encontrados += 1

 # Verifica si se encuentra una colonia y si se encontro le  suma 1 al contado
    if colonia:
        datos_encontrados += 1

# Divide los datos que se encontraron / 4 para obtener el porcentaje de confianza
    return datos_encontrados / 4

###########################
#  Procesar Noticias
###########################

def procesador_noticias(texto):
    # Funcion que va a procesar todas las demas funciones en conjunto

    # Busca la fecha en el texto y guarda el resultado en la variable fecha
    fecha = detectar_fechas(texto)
    # Busca el dia en el texto y lo guarda en la variable dia
    dia = detectar_dias(texto)
     # Busca la calle en el texto y lo guarda en la variable calle
    calle = detectar_calles(texto)
    # Busca la colonia en el texto y lo guarda en la variable colonia
    colonia = detectar_colonias(texto)

# Calcula que tan completa es la información encontrada o el nivel de confianza
    confianza = porcentaje_confianza(
    fecha,
    dia,
    calle,
    colonia)

# Crea un diccionario que guarda el resultado toda la informacion
    resultado={
    "Fecha": fecha,
    "Dia": dia,
    "Calle": calle,
    "Colonia": colonia,
    "Nivel de Confianza": confianza}

    return resultado
 # Devuelve todos los resultados que encontro la funcion

############################
# LEER NOTICIAS DEL JSON
############################

# Abre el archivo JSON para leerlo y lo llama archivo
with open("noticias_pruebas.json", "r", encoding="utf-8") as archivo:
    noticias = json.load(archivo)
    # Lee el JSON y guarda las noticias en noticias

############################
# PROCESAR NOTICIAS
############################

# Recorre una por una todas las noticias
for noticia in noticias:
    # Obtiene el texto de la noticia
    texto_noticia= noticia["texto"]
    # Envia el texto a la funcion para extraer la informacion
    resultado = procesador_noticias(texto_noticia)
    print("URL:", noticia["url"])

  # Recorre los datos encontrados y separa su nombre (clave) y contenido (valor)
    for clave, valor in resultado.items():
        print(clave + ":", valor)
    print("-----------------------------")
