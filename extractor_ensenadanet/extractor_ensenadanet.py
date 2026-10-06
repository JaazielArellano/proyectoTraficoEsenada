"""
Módulo extractor de datos para el portal ensenada.net.
Estructura la información en formato JSON.
"""

import json


# 1. LISTAS Y DICCIONARIOS

dias_semana = ["lunes", "martes", "miércoles", "miercoles", "jueves",
               "viernes", "sábado", "sabado", "domingo"]
meses_numeros = {
    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
}

palabras_calle = ["calle", "av", "av.", "avenida", "bulevar", "blvd", "callejón"]
palabras_colonia = ["colonia", "col", "col.", "fraccionamiento", "fracc", "fracc."]
palabras_omitir = ["esquina", "con", "y", "en", "esq", "esq.",
                   "cerca", "del", "de", "frente", "a"]

# 2. FUNCIÓN DE EXTRACCIÓN

def extraer_datos(texto_limpio, fecha_consulta):
    """Procesa el texto de entrada y extrae entidades clave."""
    texto_limpio = texto_limpio.replace(",", "").replace(".", "")
    texto_minusculas = texto_limpio.lower()

    # Contrato
    datos_encontrados = {
        "date": None,
        "day": None,
        "street": None,
        "neighborhood": None,
        "confidence": 0.0
    }

    palabras = texto_minusculas.split()

    for i, palabra in enumerate(palabras):

        # --- MOTOR TEMPORAL ---
        if palabra in dias_semana and datos_encontrados["day"] is None:
            datos_encontrados["day"] = palabra
            datos_encontrados["confidence"] += 0.2

        if palabra in meses_numeros:
            mes = meses_numeros[palabra]
            if i >= 2 and palabras[i-1] == "de":
                dia_num = palabras[i-2]
                if len(dia_num) == 1:
                    dia_num = "0" + dia_num
                anio = fecha_consulta[0:4]
                # Formato ISO (AAAA-MM-DD)
                datos_encontrados["date"] = f"{anio}-{mes}-{dia_num}"
                datos_encontrados["confidence"] += 0.3


        # Detectar Calles

        if palabra in palabras_calle and datos_encontrados["street"] is None:
            nombre_calle = palabra
            if i + 1 < len(palabras) and palabras[i+1] not in palabras_omitir:
                nombre_calle += f" {palabras[i+1]}"
            if (i + 2 < len(palabras)
                    and palabras[i+2] not in palabras_colonia
                    and palabras[i+2] not in palabras_omitir):

                datos_encontrados["street"] = nombre_calle.title()
                datos_encontrados["confidence"] += 0.25

        # Detectar Colonias

        if palabra in palabras_colonia and datos_encontrados["neighborhood"] is None:
            nombre_colonia = palabra
            if i + 1 < len(palabras) and palabras[i+1] not in palabras_omitir:
                nombre_colonia += f" {palabras[i+1]}"
            if i + 2 < len(palabras) and palabras[i+2] not in palabras_omitir:
                nombre_colonia += f" {palabras[i+2]}"
            datos_encontrados["neighborhood"] = nombre_colonia.title()
            datos_encontrados["confidence"] += 0.25

    datos_encontrados["confidence"] = round(datos_encontrados["confidence"], 2)
    return datos_encontrados

# 3. FLUJO PRINCIPAL (RECEPTOR Y OUTPUT)

if __name__ == "__main__":
    print("--- Iniciando Módulo Extractor ---")

    try:
        with open('entrada.json', 'r', encoding='utf-8') as archivo:
            contrato_entrada = json.load(archivo)

        texto_noticia = contrato_entrada["text"]
        fecha_retrieved = contrato_entrada["retrieved_at"]

        # Ejecutamos la extracción
        resultados = extraer_datos(texto_noticia, fecha_retrieved)

        print("¡Extracción finalizada!\n")
        # Imprimimos SOLO el JSON resultante plano
        print(json.dumps(resultados, indent=4, ensure_ascii=False))

    except FileNotFoundError:
        print("Error: No encuentro el archivo 'entrada.json'.")
