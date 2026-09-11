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
