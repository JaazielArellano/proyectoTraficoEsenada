from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
import pandas as pd

app = FastAPI()

# Cargar los datos
df = pd.read_csv("catastro_ensenada_limpio.csv", dtype=str)
df = df.fillna("")


# Mostrar la interfaz
@app.get("/", include_in_schema=False)
def inicio():
    archivo_html = Path(__file__).with_name("interfaz.html")
    return FileResponse(archivo_html)


# Consultar si existe una calle
@app.get("/calle")
def existe_calle(nombre: str):

    nombre = nombre.strip().upper()

    calles = df[
        (df["TIPO_ELEMENTO"] == "VIALIDAD") &
        (df["tipovial"] == "CALLE")
    ]

    existe = calles["nomvial"].str.upper().eq(nombre).any()

    return {
        "existe": bool(existe)
    }