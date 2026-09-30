"""Módulo para extraer datos del portal El Vigía."""

# Importa el módulo json
import json


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


# Función para extraer nombres de calles, avenidas y colonias
def extraer_vias_publicas(texto):
    """Busca palabras clave de vías públicas en el texto y guarda las calles."""
    # Diccionario con listas vacías para cada uno
    diccionario_vias = {
        "calle": [],
        "avenida": [],
        "colonia": []
    }
    # Divide el texto en palabras individuales
    palabras = texto.split()
    # Obtiene la cantidad total de palabras
    total_palabras = len(palabras)

    # Recorre las palabras evaluando cada posición
    for i, palabra in enumerate(palabras):
        # Pasa la palabra a minúsculas y quita la puntuación
        palabra_actual = palabra.lower().strip(",.:;")

        # Comprueba que exista una palabra siguiente para tomar el nombre de la vía
        if i + 1 < total_palabras:
            # Obtiene el nombre de la vía/colonia eliminando puntuación
            siguiente_palabra = palabras[i + 1].strip(",.:;")

            # Si encuentra alguna palabra similar de avenida o bulevar, guarda la siguiente palabra
            if palabra_actual in ["avenida", "av", "bulevar", "blvd"]:
                diccionario_vias["avenida"].append(siguiente_palabra)
            # Si encuentra la palabra calle, guarda el nombre asignado
            elif palabra_actual == "calle":
                diccionario_vias["calle"].append(siguiente_palabra)
            # Si encuentra la palabra colonia o col, la clasifica como tal
            elif palabra_actual in ["colonia", "col"]:
                diccionario_vias["colonia"].append(siguiente_palabra)

    # Devuelve el diccionario con las vías detectadas
    return diccionario_vias


# Función que une la extracción y calcula la confianza
def crear_contrato(texto):
    """Crear el contrato de salida del Extractor."""
    # Ejecuta la extracción de días
    dias = procesar_y_evaluar_dias(texto)
    # Ejecuta la extracción de fecha
    fecha = extraer_fecha(texto)
    # Ejecuta la extracción de vías públicas
    vias = extraer_vias_publicas(texto)

    # Selecciona el primer día encontrado o asigna None si no hubo resultados
    dia = list(dias.keys())[0] if dias else None
    # Selecciona la primera calle encontrada o asigna None
    calle = vias["calle"][0] if vias["calle"] else None
    # Selecciona la primera avenida encontrada o asigna None
    avenida = vias["avenida"][0] if vias["avenida"] else None
    # Selecciona la primera colonia encontrada o asigna None
    colonia = vias["colonia"][0] if vias["colonia"] else None

# Asignación ponderada de confianza
    confidence = 0.50
    if fecha:
        confidence += 0.15
    if dia:
        confidence += 0.10
    if calle or avenida:
        confidence += 0.15
    if colonia:
        confidence += 0.10

    # Retorna el diccionario final estructurado como contrato JSON
    return {
        "date": fecha,
        "day": dia,
        "street": calle,
        "avenue": avenida,
        "neighborhood": colonia,
        "confidence": round(confidence, 2)
    }


# Define la función para probar la ejecución local del script
def main():
    """Función principal de prueba."""
    # Texto de prueba que simula una noticia
    texto_noticia = """
    El martes 15 de septiembre de 2026 se registró un accidente
    sobre Avenida Reforma, en la calle Primera, colonia Centro.
    """
    # Procesa el texto de prueba con la función del contrato
    resultado = crear_contrato(texto_noticia)
    # Imprime el resultado transformado a JSON
    print(json.dumps(resultado, ensure_ascii=False, indent=4))


# Ejecutar main()
if __name__ == "__main__":
    main()
