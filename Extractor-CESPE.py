
"Módulo Extractor para el portal CESPE (Comisión Estatal de Servicios Públicos de Ensenada)."

# Detetectar dias de la semana y numero. 
def procesar_y_evaluar_dias(texto):
    """Analiza el texto de un aviso y detecta los días de la semana mencionados."""
    dias_semana = [
        "domingo", "lunes", "martes", "miercoles", "miércoles",
        "jueves", "viernes", "sabado", "sábado"
    ]
    #se divide el texto en palabras individuales para poder
    #revisar cada palabra y buscar los días de la semana.
    palabras = texto.split() 
    diccionario_dias = {}
    texto_size = len(palabras)

    for i, palabra in enumerate(palabras):
        palabra_actual = palabra.lower().strip(",.:;")

        if palabra_actual in dias_semana and i + 1 < texto_size:
            siguiente_palabra = palabras[i + 1].strip(",.:;")

            if siguiente_palabra.isdigit():
                numero_dia = int(siguiente_palabra)

                if 1 <= numero_dia <= 31:
                    if palabra_actual in ["miercoles", "miércoles"]:
                        dia_limpio = "miércoles"
                    elif palabra_actual in ["sabado", "sábado"]:
                        dia_limpio = "sábado"
                    else:
                        dia_limpio = palabra_actual

                    diccionario_dias[dia_limpio] = numero_dia

    return diccionario_dias

# Aqui obtenemos la fecha, CESPE normalmente no repite el año en el aviso, asi que si no aparece
#usamos la fecha de referencia que es el que nos dará el retrieved_at
def extraer_fecha(texto, anio_referencia=None):
    """Busca una fecha en el texto. Reconoce con año y sin año."""
    meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    palabras = texto.lower().split()
    total_palabras = len(palabras)

    for i, palabra in enumerate(palabras):
        palabra_actual = palabra.strip(",.:;")

        if palabra_actual.isdigit() and 1 <= int(palabra_actual) <= 31:
            numero_dia = int(palabra_actual)

            # patrón CON año: "9 de septiembre de 2026"
            if i + 4 < total_palabras:
                p_de1 = palabras[i + 1].strip(",.:;")
                mes = palabras[i + 2].strip(",.:;")
                p_de2 = palabras[i + 3].strip(",.:;")
                anio = palabras[i + 4].strip(",.:;")

                if p_de1 == "de" and mes in meses and p_de2 == "de" and anio.isdigit() and len(anio) == 4:
                    numero_mes = meses.index(mes) + 1
                    return f"{anio}-{numero_mes:02d}-{numero_dia:02d}"

            # patrón SIN año: "9 de septiembre" (muy común en CESPE)
            if i + 2 < total_palabras:
                p_de1 = palabras[i + 1].strip(",.:;")
                mes = palabras[i + 2].strip(",.:;")

                if p_de1 == "de" and mes in meses and anio_referencia:
                    numero_mes = meses.index(mes) + 1
                    return f"{anio_referencia}-{numero_mes:02d}-{numero_dia:02d}"

    return None

# Extraemos la ubicación, si es calle, avenida y/o boulevard
def extraer_via(texto):
    """Busca menciones de avenida, bulevar o calle y regresa tipo + nombre."""
    palabras_clave = {
        "avenida": "avenida", "av.": "avenida", "av": "avenida",
        "bulevar": "bulevar", "blvd.": "bulevar", "blvd": "bulevar",
        "calle": "calle",
    }
    palabras_de_corte = {"entre", "y", "en", "de"}
    palabras = texto.split()
    total_palabras = len(palabras)

    for i, palabra in enumerate(palabras):
        palabra_actual = palabra.lower().strip(",.:;")

        if palabra_actual in palabras_clave:
            tipo_via = palabras_clave[palabra_actual]
            nombre_partes = []

            # recorre las palabras siguientes mientras empiecen con mayúscula
            j = i + 1
            while j < total_palabras:
                siguiente = palabras[j].strip(",.:;")
                if siguiente and siguiente[0].isupper() and siguiente.lower() not in palabras_de_corte:
                    nombre_partes.append(siguiente)
                    j += 1
                else:
                    break

            if nombre_partes:
                return {"tipo": tipo_via, "nombre": " ".join(nombre_partes)}

    return None

# extrae la colinia
# en ocaciones menciona una sola colonia, en otras un listado de varias... 
def extraer_colonias(texto):
    """Detecta colonias mencionadas. Regresa una lista (1 o varias)."""
    colonias = []

    # caso 1: mención directa "colonia X"
    palabras = texto.split()
    for i, palabra in enumerate(palabras):
        if palabra.lower().strip(",.:;") == "colonia" and i + 1 < len(palabras):
            siguiente = palabras[i + 1].strip(",.:;")
            if siguiente and siguiente[0].isupper():
                colonias.append(siguiente)

    # caso 2: listado enumerado, una colonia por línea
    lineas = texto.split("\n")
    dentro_del_listado = False
    for linea in lineas:
        linea_limpia = linea.strip()

        if "colonias" in linea_limpia.lower() and linea_limpia.lower().rstrip(":").endswith("son"):
            dentro_del_listado = True
            continue

        if dentro_del_listado:
            if linea_limpia and len(linea_limpia.split()) <= 5 and not linea_limpia.endswith("."):
                colonias.append(linea_limpia)
            else:
                dentro_del_listado = False

    return list(dict.fromkeys(colonias))  # sin duplicados, conserva orden

#Contrato de salida
def extract_fields(contrato_cleaner):
    texto = contrato_cleaner["text"]
    anio_referencia = contrato_cleaner.get("retrieved_at", "")[:4] or None

    data = {}

    dias_encontrados = procesar_y_evaluar_dias(texto)
    if dias_encontrados:
        data["dia"] = list(dias_encontrados.keys())[0]
        if len(dias_encontrados) > 1:
            data["dias"] = dias_encontrados

    fecha = extraer_fecha(texto, anio_referencia)
    if fecha:
        data["fecha"] = fecha

    via = extraer_via(texto)
    if via:
        data[via["tipo"]] = via["nombre"]

    colonias = extraer_colonias(texto)
    if colonias:
        data["colonia"] = colonias[0]
        if len(colonias) > 1:
            data["colonias"] = colonias

    confianza = round(min(1.0, 0.25 + 0.15 * len(data)), 2)

    return {
        "source": contrato_cleaner.get("source"),
        "url": contrato_cleaner.get("url"),
        "data": data,
        "confidence": confianza,
    }

