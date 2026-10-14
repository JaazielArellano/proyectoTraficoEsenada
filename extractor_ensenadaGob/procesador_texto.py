import re

#############################
#       DETECTAR FECHAS 
#############################

def detectar_fechas(texto):                                     # Funcion para buscar fechas fomato AAAA-MM-DD

    meses = {                                                   # Creamos un diccionario que relaciona cada mes con su mumero
        "enero": "01","febrero": "02", "marzo": "03",
        "abril": "04","mayo": "05","junio": "06",
        "julio": "07","agosto": "08","septiembre": "09",
        "octubre": "10","noviembre": "11","diciembre": "12"
    }

    patron = r"(\d{1,2}) de (\w+) de (\d{4})"                   # Define el patron que debe tener la fecha
    resultado = re.search(patron, texto.lower())                # Busca en el texto una fecha que coincida con el patron

    if resultado:                                               # Verifica si se encontro una fecha y si se encontro continua.Si no pasa hasta el return None
        dia = resultado.group(1)                                # Obtiene el dia que se encontro
        mes = resultado.group(2)                                # Obtiene el mes que se encontro
        año = resultado.group(3)                                # Obtiene el año que se encontro

        if mes in meses:
            return f"{año}-{meses[mes]}-{int(dia):02d}"
    return None

#############################
# DETECTAR DIAS DE LA SEMANA 
#############################

def detectar_dias(texto):                                        # Funcion para Buscar un dia de la semana
    dias = ["domingo","lunes","martes",                          # Creamos una lista con todos los dias de la semana que 
    "miércoles","jueves","viernes","sábado"]                     # Se utilizaran para comprobar si una palabra es un dia de la semana

    palabras = texto.lower().split()                             # Lower() convierte todo el texto a minusculas y Split() divide el texto en palabras

    for i, palabra in enumerate(palabras):                       # Recorre todas las palabras una por una
        if palabra.strip(",.:") in dias:                         # Quita de la palabra los caracteres y verifica si es un dia de la semana 
            if i + 1 < len(palabras):
                numero = palabras[i + 1].strip(",.:")            # selecciona  la palabra que esta despues del dia
                return palabra + " " + numero                    # Une el dia y el numero
    return None                                                  # Si no encuentra ningun dia regresa None

############################
#    DETECTAR CALLES 
############################

def detectar_calles(texto):                                      # Funcion para Buscar calles o avenidas 

    tipos_calle = ["calle","avenida","av.",                      # Creamos una lista con diferentes formas de referirse a una calle
    "boulevard", "blvd.", "calzada", "carretera"]

    palabras = texto.split()                                     # Dividimos el texto en palabras separadas
    for i, palabra in enumerate(palabras):                       # Recorre cada palabra del texto
        palabra_limpia = palabra.lower().strip(",.:")            # Convertimos la palabra en minusculas y eliminamos caracteres 

        if palabra_limpia in tipos_calle:                        # Comprobamos si la palabra es uno de los tipos de calle de la lista
            if i + 1 < len(palabras):                            # Verificamos que haya una palabra despues
                nombre = palabras[i + 1].strip(",.:")            # Obtenemos la palabra que esta exactamente despues
                return palabra + " " + nombre                    # Une el tipo de calle y el nombre
    return None                                                  # Si no encuentra ningun tipo de calle regresa None

############################
#    DETECTAR COLONIAS 
############################

def detectar_colonias(texto):                                    # Funcion para Buscar colonias
    palabras = texto.split()                                     # Dividimos el texto en palabras separadas

    for i, palabra in enumerate(palabras):                       # Recorre todas las palabras
        palabra_limpia = palabra.lower().strip(",.:")            # Convertimos a minusculas y eliminamos caracteres para que solo quede la palabra "colonia"

        if palabra_limpia == "colonia":                          # Comprobamos si la palabra actual es exactamente "colonia"
            if i + 1 < len(palabras):                            # Comprueba que exista una palabra después de "colonia"
                nombre = palabras[i + 1].strip(",.:")            # Obtenemos la palabra que esta exactamente despues de "colonia"
                return nombre                                    # Devuelve el nombre de la colonia encontrado
    return None                                                  # Si no se encuentra la palabra "colonia" devuelve None

###########################
#  PORCENTAJE DE CONFIANZA  
###########################

def porcentaje_confianza(fecha, dia, calle, colonia):               # Funcion que recibe 4 datos: fecha, dia, calle y colonia
    datos_encontrados = 0                                           # contador que nos ayuda a contar cuantos datos encontramos

    if fecha:                                                       # Verifica si se encontro una fecha y si se encontro le suma 1 al contador
       datos_encontrados += 1                                       
    if dia:                                                         # Verifica si se encontro un dia y si se encontro le suma 1 al contaor 
        datos_encontrados += 1
    if calle:                                                       # Vericfica si se encuentro una calle y si se encontro le suma 1 al contador            
        datos_encontrados += 1
    if colonia:                                                     # Verifica si se encuentra una colonia y si se encontro le  suma 1 al contador
        datos_encontrados += 1

    return datos_encontrados / 4                                    # Divide los datos que se encontraron / 4 para obtener el porcentaje de confianza

###########################
#  Procesar Noticias   
###########################

def procesador_noticias(texto):                                     # Funcion que va a procesar todas las demas funciones en conjunto

    fecha = detectar_fechas(texto)                                  # Busca la fecha en el texto y guarda el resultado en la variable fecha
    dia = detectar_dias(texto)                                      # Busca el dia en el texto y lo guarda en la variable dia 
    calle = detectar_calles(texto)                                  # Busca la calle en el texto y lo guarda en la variable calle 
    colonia = detectar_colonias(texto)                              # Busca la colonia en el texto y lo guarda en la variable colonia 

    confianza = porcentaje_confianza(                               # Calcula que tan completa es la información encontrada o el nivel de confianza
        fecha,
        dia,
        calle,
        colonia
    )

    resultado = {                                                   # Crea un diccionario que guarda el resultado toda la informacion
        "Fecha": fecha,
        "Dia": dia,
        "Calle": calle,
        "Colonia": colonia,
        "Nivel de Confianza": confianza
    }

    return resultado                                                # Devuelve todos los resultados que encontro la funcion

############################
# LEER NOTICIAS DEL JSON
############################

with open("noticias_pruebas.json", "r", encoding="utf-8") as archivo:               # Abre el archivo JSON para leerlo y lo llama archivo
    noticias = json.load(archivo)                                                   # Lee el JSON y guarda las noticias en noticias

############################
# PROCESAR NOTICIAS
############################

for noticia in noticias:                                                            # Recorre una por una todas las noticias
    texto = noticia["texto"]                                                        # Obtiene el texto de la noticia
    resultado = procesador_noticias(texto)                                          # Envia el texto a la funcion para extraer la informacion 
    print("URL:", noticia["url"])                                                   # Muestra la URL de la noticia

    for clave, valor in resultado.items():                                          # Recorre los datos encontrados y separa su nombre (clave) y contenido (valor)
        print(clave + ":", valor)                                                   # Muestra cada dato
    print("-----------------------------")
