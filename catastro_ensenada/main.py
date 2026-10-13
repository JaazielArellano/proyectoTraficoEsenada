"""API de Catastro de Ensenada."""

import csv
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse

from etl import normalizar

app = FastAPI(
    title="API de Catastro de Ensenada",
    description=(
        "API para verificar si una vialidad existe en Ensenada, "
        "Baja California, utilizando un archivo CSV procesado mediante ETL. "
        "Las consultas devuelven una respuesta booleana en formato JSON."
    ),
    version="1.0.0"
)

ARCHIVO = Path(__file__).resolve().parent / "catastro_ensenada.csv"


# Cargar vialidades
def cargar_vialidades(ruta=ARCHIVO):
    with open(ruta, newline="", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo)

        return {
            normalizar(fila["nombre"])
            for fila in lector
            if fila.get("nombre")
        }


VIALIDADES = cargar_vialidades()


# Mostrar la documentación de la API al entrar
@app.get("/", include_in_schema=False)
def inicio():
    return RedirectResponse(url="/docs")


# Endpoint para verificar vialidades
@app.get(
    "/buscar",
    summary="Verificar existencia de una vialidad",
    description=(
        "Recibe el nombre de una calle o avenida de Ensenada "
        "y devuelve true si existe en el CSV o false si no existe."
    ),
    tags=["Consulta de vialidades"]
)
def buscar(
    nombre: str = Query(
        ...,
        min_length=1,
        max_length=150,
        description="Nombre de la calle o avenida que deseas consultar",
        examples=["Reforma"]
    )
):
    existe = normalizar(nombre) in VIALIDADES

    return {
        "existe": existe
    }