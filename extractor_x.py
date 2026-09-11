from datetime import datetime
import json
import re

def extraer_datos_x(datos_cleaner: dict) -> dict:
    """
    Recibe el diccionario procesado por Cleaner (con la noticia de X)
    y devuelve el JSON estructurado.
    """
    texto_extraido = datos_cleaner.get("text", "")

    patron_calle = (
        r"(?:calle|c\.|avenida|av\.|bulevar|blvd\.)\s+([A-Za-z0-9áéíóúÁÉÍÓÚñÑ\s]+?)(?=,|\.|\scolonia|\sfracc|$)"
    )
    patron_colonia = (
        r"(?:colonia|col\.|fracc\.)\s+([A-Za-z0-9áéíóúÁÉÍÓÚñÑ\s]+?)(?=,|\.|$)"
    )
    patron_fecha = r"(\d{1,2})\s+de\s+(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)"

    dias_semana = {
        0: "lunes",
        1: "martes",
        2: "miércoles",
        3: "jueves",
        4: "viernes",
        5: "sábado",
        6: "domingo",
    }
    meses = {
        "enero": "01",
        "febrero": "02",
        "marzo": "03",
        "abril": "04",
        "mayo": "05",
        "junio": "06",
        "julio": "07",
        "agosto": "08",
        "septiembre": "09",
        "octubre": "10",
        "noviembre": "11",
        "diciembre": "12",
    }


    calle_match = re.search(patron_calle, texto_extraido, re.IGNORECASE)
    colonia_match = re.search(patron_colonia, texto_extraido, re.IGNORECASE)
    fecha_match = re.search(patron_fecha, texto_extraido, re.IGNORECASE)

    street = calle_match.group(0).strip() if calle_match else None
    neighborhood = colonia_match.group(1).strip() if colonia_match else None

    date_str = None
    day_str = None

    if fecha_match:
        dia_num = fecha_match.group(1).zfill(2)
        mes_nombre = fecha_match.group(2).lower()
        mes_num = meses.get(mes_nombre, "01")
        anio = "2026" 

        date_str = f"{anio}-{mes_num}-{dia_num}"

        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            day_str = dias_semana[dt.weekday()]
        except ValueError:
            pass

    confidence = 0.50
    if date_str:
        confidence += 0.15
    if day_str:
        confidence += 0.10
    if street:
        confidence += 0.15
    if neighborhood:
        confidence += 0.10

    resultado = {
        "date": date_str,
        "day": day_str,
        "street": street,
        "neighborhood": neighborhood,
        "confidence": round(confidence, 2),
    }

    return resultado


if __name__ == "__main__":
    noticia_x_desde_cleaner = {
        "source": "X (Twitter)",
        "url": "https://x.com/Argumento_X/status/2095281615396061580",
        "retrieved_at": "2026-09-09T12:00:00",
        "text": "Un hombre identificado como César Alejandro N fue vinculado a proceso por su probable participación en un ataque armado ocurrido en noviembre de 2024 en la colonia 17 de Abril, en Ensenada. " 
    }

    datos = extraer_datos_x(noticia_x_desde_cleaner)

    print(json.dumps(datos, indent=2, ensure_ascii=False))