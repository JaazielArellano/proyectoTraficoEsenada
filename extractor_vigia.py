"""Módulo para extraer datos del portal El Vigía."""


# Define la función que identifica los días de la semana y sus números
def procesar_y_evaluar_dias(texto):
    """Analizar el texto de una noticia y detectar los días de la semana."""
    # Lista de días a buscar, incluyendo con y sin acento
    dias_semana = [
        "domingo", "lunes", "martes", "miercoles", "miércoles",
        "jueves", "viernes", "sabado", "sábado"
    ]
    # Separa el texto en una lista de palabras individuales
    palabras = texto.split()
    # Diccionario donde se guardará día:número
    diccionario_dias = {}
    # Obtiene la cantidad total de palabras
    texto_size = len(palabras)

    # Recorre cada palabra obteniendo su índice (i) y su valor (palabra)
    for i, palabra in enumerate(palabras):
        # Convierte la palabra a minúsculas y elimina signos de puntuación pegados
        palabra_actual = palabra.lower().strip(",.:;")

        # Comprueba si la palabra es un día válido y si hay una palabra después
        if palabra_actual in dias_semana and i + 1 < texto_size:
            # Obtiene la siguiente palabra y elimina la puntuación
            siguiente_palabra = palabras[i + 1].strip(",.:;")

            # Verifica si la siguiente palabra es un número (ejemplo: "martes 15")
            if siguiente_palabra.isdigit():
                # Convierte el texto del número a un valor entero (int)
                numero_dia = int(siguiente_palabra)

                # Asegura que el número esté en un rango válido de días del mes
                if 1 <= numero_dia <= 31:
                    # Ajusta la ortografía del día si es miércoles
                    if palabra_actual in ["miercoles", "miércoles"]:
                        dia_limpio = "miércoles"
                    # Ajusta la ortografía del día si es sábado
                    elif palabra_actual in ["sabado", "sábado"]:
                        dia_limpio = "sábado"
                    # Mantiene el nombre del día tal cual si no requirió acento
                    else:
                        dia_limpio = palabra_actual

                    # Guarda el resultado en el diccionario
                    diccionario_dias[dia_limpio] = numero_dia

    # Devuelve el diccionario con los días y números
    return diccionario_dias


# Función para extraer una fecha estructurada en formato YYYY-MM-DD
def extraer_fecha(texto):
    """Buscar una fecha utilizando las palabras del texto.

    Ejemplo: martes 15 de septiembre de 2026
    """
    # Lista con los meses del año
    meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    # Convierte el texto completo a minúsculas y lo divide en palabras
    palabras = texto.lower().split()
    # Guarda la cantidad total de palabras procesadas
    total_palabras = len(palabras)

    # Recorre la lista de palabras buscando su posición exacta
    for i, palabra in enumerate(palabras):
        # Limpia signos de puntuación
        palabra_actual = palabra.strip(",.:;")

        # Evalúa si la palabra es un número y representa un día del 1 al 31
        if palabra_actual.isdigit() and 1 <= int(palabra_actual) <= 31:
            # Convierte la palabra detectada a número entero
            numero_dia = int(palabra_actual)

            # Verifica que existan al menos 4 palabras más adelante para el patrón completo
            if i + 4 < total_palabras:
                # Extrae la primera palabra unión (debería ser "de")
                p_de1 = palabras[i + 1].strip(",.:;")
                # Extrae el posible nombre del mes
                mes = palabras[i + 2].strip(",.:;")
                # Extrae la segunda palabra uníon (debería ser "de")
                p_de2 = palabras[i + 3].strip(",.:;")
                # Extrae el año
                año = palabras[i + 4].strip(",.:;")

                # Confirma que la estructura tenga "de (mes) de"
                if p_de1 == "de" and mes in meses and p_de2 == "de":
                    # Valida que el año sea numérico y tenga 4 dígitos
                    if año.isdigit() and len(año) == 4:
                        # Obtiene el número del mes (1 al 12) basado en su índice
                        numero_mes = meses.index(mes) + 1
                        # Retorna la fecha en formato YYYY-MM-DD
                        return f"{año}-{numero_mes:02d}-{numero_dia:02d}"

    # Retorna None si no se encontró ninguna fecha válida en el texto
    return None
