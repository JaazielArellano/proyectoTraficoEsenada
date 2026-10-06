from datetime import datetime
import json
import re


#Extraccion y confianza (REGEX)



def extraer_datos_x(datos_cleaner: dict) -> dict:
  
    # Extraer el texto de la noticia pasándolo por el cleaner
    texto_extraido = datos_cleaner.get("text", "")


    patron_calle = r"(?:calle|c\.|avenida|av\.|bulevar|blvd\.|calzada|privada)\s+([A-Za-z0-9áéíóúÁÉÍÓÚñÑ\s]+?)(?=,|\.|\scolonia|\sfracc|\sbarrio|\sy\b|\sentre\b|$)"
    patron_colonia = r"(?:colonia|col\.|fraccionamiento|fracc\.|barrio|ejido)\s+([A-Za-z0-9áéíóúÁÉÍÓÚñÑ\s]+?)(?=,|\.|\scalle|\sav|\sblvd|$)"
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

    # Limpieza de resultados
    street = calle_match.group(0).strip().title() if calle_match else None
    neighborhood = (
        colonia_match.group(1).strip().title() if colonia_match else None
    )

    date_str = None
    day_str = None


    if fecha_match:
        dia_num = fecha_match.group(1).zfill(2)
        mes_nombre = fecha_match.group(2).lower()
        mes_num = meses.get(mes_nombre, "01")
        anio = "2026"  # Año del proyecto

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

    return {
        "date": date_str,
        "day": day_str,
        "street": street,
        "neighborhood": neighborhood,
        "confidence": round(confidence, 2),
    }



#FLUJO DE EJECUCIÓN 

if __name__ == "__main__":
    print("Iniciando Módulo Extractor y nivel de confianza")

    #lee desde "entrada.json" si el otro modulo lo genera como archivo
    try:
        with open("entrada.json", "r", encoding="utf-8") as archivo:
            noticia_entrada = json.load(archivo)
        print("Archivo 'entrada.json' cargado exitosamente.")

    #Si no existe el archivo físico, ejecuta la prueba integrada por código
    except FileNotFoundError:
        print("No se encontró 'entrada.json'. Ejecutando con prueba de texto directa:\n")
        noticia_entrada = {
            "source": "X (Twitter)",
            "url": "https://x.com/EnsenadaNews/status/123456789",
            "retrieved_at": "2026-09-24T12:00:00",
            "text": "Atención Ensenada: Este martes 15 de septiembre habrá cierre vial por reparaciones en Avenida Reforma, colonia Centro.",
        }

    # Procesar y generar el JSON final con confianza
    resultado = extraer_datos_x(noticia_entrada)

    print("\nExtracción finalizada. JSON entregable:")
    print(json.dumps(resultado, indent=4, ensure_ascii=False))