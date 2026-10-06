import json
from datetime import datetime

# catalogo de prueba, hay que cambiarlo por el catalogo real de ensenada
COLONIAS_ENSENADA = {
    "zona centro", "chapultepec", "playitas", "obrera",
    "bella vista", "moderna", "reforma",
}
CALLES_ENSENADA = {
    "avenida reforma", "avenida ruiz", "avenida riveroll", "avenida balboa",
    "calle primera", "calle segunda", "boulevard costero",
}

CAMPOS_OBLIGATORIOS = ["source", "url", "retrieved_at", "text", "confidence"]
DIAS = {"lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"}


def validar_campos(registro):
    errores = []
    for campo in CAMPOS_OBLIGATORIOS:
        if campo not in registro or registro[campo] in (None, ""):
            errores.append(f"Falta el campo obligatorio '{campo}'")
    conf = registro.get("confidence")
    if conf is not None and not (isinstance(conf, (int, float)) and 0 <= conf <= 1):
        errores.append(f"'confidence' fuera de rango (0 a 1): {conf}")
    return errores


def validar_fecha(registro):
    errores = []
    fecha = registro.get("date")
    if fecha is None:
        return errores
    try:
        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        return [f"Fecha con formato inválido (se esperaba YYYY-MM-DD): {fecha}"]
    dia = registro.get("day")
    if dia is not None:
        if dia.lower() not in DIAS:
            errores.append(f"Día no reconocido: {dia}")
        else:
            nombres = ["lunes", "martes", "miércoles", "jueves",
                       "viernes", "sábado", "domingo"]
            if nombres[fecha_dt.weekday()] != dia.lower():
                errores.append(f"El día '{dia}' no coincide con la fecha {fecha}")
    return errores


def validar_geografia(registro):
    errores = []
    colonia = registro.get("neighborhood")
    calle = registro.get("street")
    if colonia is not None and colonia.lower() not in COLONIAS_ENSENADA:
        errores.append(f"Colonia no encontrada en el catálogo de Ensenada: {colonia}")
    if calle is not None and calle.lower() not in CALLES_ENSENADA:
        errores.append(f"Calle no encontrada en el catálogo de Ensenada: {calle}")
    if colonia is None and calle is None:
        errores.append("Sin colonia ni calle: no se puede ubicar el evento")
    return errores


def validar_registro(registro):
    errores = validar_campos(registro) + validar_fecha(registro) + validar_geografia(registro)
    return {"valido": len(errores) == 0, "errores": errores}


if __name__ == "__main__":
    pruebas = [
        {
            "source": "X", "url": "https://x.com/ejemplo/1",
            "retrieved_at": "2026-09-18T10:00:00",
            "text": "Accidente en Avenida Reforma, colonia Zona Centro el viernes 18 de septiembre",
            "date": "2026-09-18", "day": "viernes",
            "street": "Avenida Reforma", "neighborhood": "Zona Centro",
            "confidence": 0.90,
        },
        {
            "source": "X", "url": "https://x.com/ejemplo/2",
            "retrieved_at": "2026-09-18T10:05:00",
            "text": "Choque en Playitas el lunes 18 de septiembre",
            "date": "2026-09-18", "day": "lunes",
            "street": None, "neighborhood": "Playitas",
            "confidence": 0.75,
        },
        {
            "source": "X", "url": "https://x.com/ejemplo/3",
            "retrieved_at": "2026-09-18T10:10:00",
            "text": "",
            "date": None, "day": None,
            "street": "Calle Inventada", "neighborhood": "Colonia Fantasma",
            "confidence": 0.50,
        },
    ]

    for i, registro in enumerate(pruebas, start=1):
        resultado = validar_registro(registro)
        print(f"--- Prueba {i} ---")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
