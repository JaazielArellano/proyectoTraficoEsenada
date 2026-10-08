"""
ejemplo_dashboard_emilio_edgar.py

Prototipo del componente "Mapa interactivo" del módulo Dashboard.

Autor: Edgar Eduardo Lopez Orozco
Proyecto: Proyecto Integrador de Extracción de Datos Geográficos (Ensenada)

Cómo correrlo:
    pip install streamlit pandas folium streamlit-folium
    streamlit run ejemplo_dashboard_v3.py
"""

import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium


# 1. Datos simulados (mock) mismos campos que el contrato JSON del proyecto

"""
MOCK_DATA = [
    {"id": 1, "date": "2026-09-10", "day": "jueves", "street": "Avenida Reforma",
     "neighborhood": "Centro", "confidence": 0.92, "source": "fuente_web",
     "created_by": "usuario_admin", "lat": 31.8667, "lon": -116.5964},
    {"id": 2, "date": "2026-09-11", "day": "viernes", "street": "Calle Ryerson",
     "neighborhood": "Centro", "confidence": 0.81, "source": "carga_excel",
     "created_by": "edgar", "lat": 31.8611, "lon": -116.6017},
    {"id": 3, "date": "2026-09-12", "day": "sábado", "street": "Boulevard Costero",
     "neighborhood": "Playitas", "confidence": 0.75, "source": "fuente_web",
     "created_by": "usuario_admin", "lat": 31.8506, "lon": -116.6142},
    {"id": 4, "date": "2026-09-12", "day": "sábado", "street": "Calle Novena",
     "neighborhood": "Playitas", "confidence": 0.60, "source": "carga_excel",
     "created_by": "edgar", "lat": 31.8489, "lon": -116.6098},
    {"id": 5, "date": "2026-09-14", "day": "lunes", "street": "Avenida Reforma",
     "neighborhood": "Centro", "confidence": 0.95, "source": "fuente_web",
     "created_by": "usuario_admin", "lat": 31.8670, "lon": -116.5970},
    {"id": 6, "date": "2026-09-15", "day": "martes", "street": "Calle Diamante",
     "neighborhood": "Valle Dorado", "confidence": 0.68, "source": "fuente_web",
     "created_by": "usuario_admin", "lat": 31.8724, "lon": -116.6205},
]
"""

# AGREGADO PARA CONECTAR CON LA CARGA DE EXCEL 
# Los datos simulados de arriba quedaron entre comillas (desactivados): para
# volver a usarlos basta quitar las comillas triples y borrar este bloque.
# Ahora el mapa se alimenta de los registros que se suben por Excel y se guardan
# en la API simulada (sección 5). Se conserva el nombre MOCK_DATA para que la
# línea df = pd.DataFrame(MOCK_DATA) funcione sin cambios. Solo se dibujan los
# registros que traen lat y lon. (Con una API real habría que llenar
# st.session_state.api_registros con lo que devuelva el GET.)
COLUMNAS_MAPA = ["id", "date", "day", "street", "neighborhood",
                 "confidence", "source", "created_by", "lat", "lon"]
MOCK_DATA = pd.DataFrame(
    [r for r in st.session_state.get("api_registros", [])
     if r.get("lat") is not None and r.get("lon") is not None],
    columns=COLUMNAS_MAPA,
)

df = pd.DataFrame(MOCK_DATA)

# NUEVO: lista para guardar las notas que escribas.
# Se crea una sola vez; así no se borra cada vez que haces clic en algo.
if "notas" not in st.session_state:
    st.session_state.notas = []


# 2. Configuración de página + filtro simple por colonia

st.set_page_config(page_title="Dashboard - Mapa", layout="wide")
st.title("Prototipo: Mapa Interactivo")
st.caption("Datos simulados (mock)")

colonias = ["Todas"] + sorted(df["neighborhood"].unique().tolist())
colonia_seleccionada = st.sidebar.selectbox("Filtrar por colonia", colonias)

# Filtrar el DataFrame según la colonia elegida por el usuario.
if colonia_seleccionada == "Todas":
    df_filtrado = df
else:
    # 1. Reviso fila por fila: ¿la colonia es la que eligió el usuario? (Sí/No)
    es_la_colonia_elegida = df["neighborhood"] == colonia_seleccionada

    # 2. Me quedo solo con las filas que dijeron "Sí"
    df_filtrado = df[es_la_colonia_elegida]

st.write("Mostrando registros en el mapa.")


# 3. Mapa interactivo con Folium + streamlit-folium

if len(df_filtrado) > 0:
    centro_lat = df_filtrado["lat"].mean()
    centro_lon = df_filtrado["lon"].mean()
else:
    centro_lat, centro_lon = 31.8667, -116.5964

# CAMBIO 1 (satélite y cartografía):
# tiles=None crea el mapa sin fondo, y abajo le agregamos dos fondos.
mapa = folium.Map(location=[centro_lat, centro_lon], zoom_start=13, tiles=None)

# Fondo 1: cartografía (calles)
folium.TileLayer("OpenStreetMap", name="Cartografía (calles)").add_to(mapa)

# Fondo 2: satélite
folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",
    name="Satélite",
).add_to(mapa)

# Botón en el mapa para cambiar entre cartografía y satélite
folium.LayerControl().add_to(mapa)

# Marcadores de los registros
for _, fila in df_filtrado.iterrows():
    popup_html = (
         f"<b>{fila['street']}</b><br>"
         f"Colonia: {fila['neighborhood']}<br>"
         f"Confianza: {fila['confidence']}<br>"
         f"Fuente: {fila['source']}"
    )
    folium.Marker(
        location=[fila["lat"], fila["lon"]],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=fila["street"],
        icon=folium.Icon(color="red" if fila["confidence"] < 0.7 else "green"),
    ).add_to(mapa)

# NUEVO: marcadores azules para las notas que ya guardaste
for nota in st.session_state.notas:
    folium.Marker(
        location=[nota["lat"], nota["lon"]],
        popup=f"<b>{nota['calle']}</b><br>{nota['texto']}",
        tooltip=nota["calle"],
        icon=folium.Icon(color="blue"),
    ).add_to(mapa)

# Dibuja el mapa. La variable "resultado" guarda lo que hizo el usuario en él (por ejemplo, le das un clic).
resultado = st_folium(mapa, width=None, height=550)


# 4. CAMBIO 2 agregar una nota con un clic en el mapa

# Si el usuario hizo clic en el mapa, aquí viene la latitud y longitud del clic.
clic = resultado.get("last_clicked")

if clic:
    st.write(f"Punto seleccionado: {clic['lat']:.5f}, {clic['lng']:.5f}")

    calle = st.text_input("Nombre de la calle")
    texto = st.text_area("Noticia o dato")

    if st.button("Guardar nota"):
        # Guardamos la nota junto con el punto donde se hizo clic
        st.session_state.notas.append({
            "calle": calle,
            "texto": texto,
            "lat": clic["lat"],
            "lon": clic["lng"],
        })
        # Vuelve a correr el script para que el marcador azul aparezca en el mapa
        st.rerun()
else:
    st.info("Haz clic en un punto del mapa para agregar una noticia o dato.")



# 5. CARGA DE EXCEL CON VALIDACIÓN 
#    5.1 Validación del ARCHIVO: funciones de validar_archivos.py tal cual
#        (único cambio: print()  st.success / st.error).
#    5.2 Validación del CONTENIDO: lo que pide el plan (columnas, campos
#        requeridos, formato de fecha, reporte de errores por fila).
#    5.3 API SIMULADA (para probar el envío de registros sin servidor real).
#    5.4 Pantalla de carga de Excel (lo que se guarda alimenta el mapa).

import os
import io
import csv
import json
import time
import zipfile
import tempfile
from datetime import datetime


# 5.1 Validación del archivo (de validar_archivos.py)

# Límite temporal del archivo
LIMITE_MB = 10


def validar_json(ruta):

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        # Revisar que tenga información
        if datos is None or datos == {} or datos == []:
            return False

        return True

    except:
        return False


def validar_csv(ruta):

    try:
        with open(ruta, "r", encoding="utf-8", newline="") as archivo:

            lector = csv.reader(archivo)

            filas = list(lector)

        # Revisar que tenga información
        if len(filas) == 0:
            return False

        # Revisar que tenga al menos una fila con columnas
        if len(filas[0]) < 2:
            return False

        return True

    except:
        return False


def validar_excel(ruta):

    try:

        # Los archivos XLSX reales son archivos ZIP internamente
        if not zipfile.is_zipfile(ruta):
            return False

        with zipfile.ZipFile(ruta, "r") as archivo:

            nombres = archivo.namelist()

            # Archivos internos que normalmente debe tener un XLSX
            if "[Content_Types].xml" not in nombres:
                return False

            if "xl/workbook.xml" not in nombres:
                return False

        return True

    except:
        return False


def cargar_archivo(ruta):

    # Quitar espacios y comillas
    ruta = ruta.strip().strip('"')
    ruta_min = ruta.lower()

    # Revisar si existe
    if not os.path.isfile(ruta):
        st.error("El archivo no existe.")
        return False

    # Revisar tamaño
    tamaño_mb = os.path.getsize(ruta) / (1024 * 1024)

    if tamaño_mb > LIMITE_MB:
        st.error(f"El archivo supera el límite de {LIMITE_MB} MB.")
        return False

    # JSON
    if ruta_min.endswith(".json"):

        if validar_json(ruta):
            st.success("Archivo JSON válido.")
            return True

        else:
            st.error("Tiene extensión JSON, pero el contenido no es JSON válido.")
            return False

    # CSV
    elif ruta_min.endswith(".csv"):

        if validar_csv(ruta):
            st.success("Archivo CSV válido.")
            return True

        else:
            st.error("Tiene extensión CSV, pero el contenido no parece un CSV válido.")
            return False

    # Excel
    elif ruta_min.endswith(".xlsx"):

        if validar_excel(ruta):
            st.success("Archivo Excel válido.")
            return True

        else:
            st.error("Tiene extensión XLSX, pero no es un archivo Excel válido.")
            return False

    else:
        st.error("Formato no permitido.")
        return False



# 5.2 Validación del contenido (pandas/openpyxl)

COLUMNAS_REQUERIDAS = ["date", "day", "street", "neighborhood"]
# Columnas opcionales, solo para poder dibujar el registro en el mapa
CONFIANZA_POR_DEFECTO = 1.0  # carga manual por Excel: se considera verificada


def _numero_opcional(fila, columna, minimo, maximo, problemas):
    """Lee una columna numérica opcional. Devuelve el número, o None si no viene."""
    if columna not in fila.index or pd.isna(fila[columna]) or str(fila[columna]).strip() == "":
        return None
    try:
        valor = float(fila[columna])
    except (TypeError, ValueError):
        problemas.append(f"'{columna}' no es un número")
        return None
    if not minimo <= valor <= maximo:
        problemas.append(f"'{columna}' fuera de rango ({minimo} a {maximo})")
        return None
    return valor


def validar_contenido_excel(archivo):
    """
    Revisa columnas, campos vacíos y formato de fecha fila por fila.
    Devuelve (registros_validos, errores). Usa el contrato de salida (4.2 del plan).
    """
    try:
        datos = pd.read_excel(io.BytesIO(archivo.getvalue()), engine="openpyxl")
    except Exception as e:
        return [], [f"No se pudo leer el Excel: {e}"]

    datos.columns = [str(c).strip().lower() for c in datos.columns]
    datos = datos.dropna(how="all")  # ignora filas totalmente vacías (conserva el # de fila)

    faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in datos.columns]
    if faltantes:
        return [], [f"Faltan columnas requeridas: {', '.join(faltantes)}"]
    if datos.empty:
        return [], ["El archivo no tiene registros."]

    validos, errores = [], []
    for i, fila in datos.iterrows():
        n = i + 2  # fila real en Excel (1 = encabezado)
        problemas = []

        for col in COLUMNAS_REQUERIDAS:
            if pd.isna(fila[col]) or str(fila[col]).strip() == "":
                problemas.append(f"'{col}' vacío")

        fecha = None
        if not pd.isna(fila["date"]):
            f = pd.to_datetime(str(fila["date"]).strip()[:10], format="%Y-%m-%d", errors="coerce")
            if pd.isna(f):
                problemas.append("'date' no tiene formato AAAA-MM-DD")
            else:
                fecha = f.strftime("%Y-%m-%d")

        # Columnas opcionales para el mapa
        antes = len(problemas)
        lat = _numero_opcional(fila, "lat", -90, 90, problemas)
        lon = _numero_opcional(fila, "lon", -180, 180, problemas)
        confianza = _numero_opcional(fila, "confidence", 0, 1, problemas)
        if len(problemas) == antes and (lat is None) != (lon is None):
            problemas.append("'lat' y 'lon' deben venir juntas")

        if problemas:
            errores.append(f"Fila {n}: " + "; ".join(problemas))
            continue

        registro = {
            "date": fecha,
            "day": str(fila["day"]).strip().lower(),
            "street": str(fila["street"]).strip(),
            "neighborhood": str(fila["neighborhood"]).strip(),
            "source": "carga_excel",
            "created_by": "usuario_demo",  # PENDIENTE: usuario del login (Jesus)
        }
        if confianza is not None:
            registro["confidence"] = confianza
        if lat is not None:
            registro["lat"], registro["lon"] = lat, lon
            registro.setdefault("confidence", CONFIANZA_POR_DEFECTO)
        validos.append(registro)

    return validos, errores



# 5.3 API SIMULADA
#     Imita POST /records y GET /records. Guarda en la memoria de la app
#     (st.session_state), así que los registros se pierden al recargar o cerrar.
#     Para usar una API real: USAR_API_SIMULADA = False y definir la variable de
#     entorno API_URL (las rutas reales dependen de la API que se use).

USAR_API_SIMULADA = True
API_URL = os.getenv("API_URL", "")

CAMPOS_CONTRATO_SALIDA = ["date", "day", "street", "neighborhood", "source", "created_by"]
CAMPOS_OPCIONALES = ["lat", "lon", "confidence"]  # los usa el mapa


def _api_simulada_post(registros):
    """Simula POST /records: valida campos, rechaza duplicados y asigna id y created_at."""
    if "api_registros" not in st.session_state:
        st.session_state.api_registros = []

    guardados, rechazados = [], []
    for i, reg in enumerate(registros):
        faltan = [c for c in CAMPOS_CONTRATO_SALIDA if reg.get(c) in (None, "")]
        if faltan:
            rechazados.append({"index": i, "error": "Faltan campos: " + ", ".join(faltan)})
            continue

        clave = (reg["date"], reg["street"].lower(), reg["neighborhood"].lower())
        duplicado = any(
            (r["date"], r["street"].lower(), r["neighborhood"].lower()) == clave
            for r in st.session_state.api_registros
        )
        if duplicado:
            rechazados.append({"index": i, "error": "Registro duplicado (misma fecha, calle y colonia)"})
            continue

        nuevo = {
            "id": 1000 + len(st.session_state.api_registros) + 1,
            **{c: reg[c] for c in CAMPOS_CONTRATO_SALIDA},
            **{c: reg[c] for c in CAMPOS_OPCIONALES if reg.get(c) is not None},
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
        st.session_state.api_registros.append(nuevo)
        guardados.append(nuevo)

    if guardados and not rechazados:
        status = 201  # todos guardados
    elif guardados:
        status = 207  # guardados algunos, otros rechazados
    else:
        status = 400  # ninguno guardado

    return {
        "status": status,
        "body": {"inserted": len(guardados), "rejected": rechazados, "records": guardados},
    }


def api_post_records(registros):
    """POST /records. Con la API simulada o con la real devuelve {"status", "body"}."""
    if USAR_API_SIMULADA:
        return _api_simulada_post(registros)

    import requests
    # PENDIENTE: ajustar la ruta al endpoint de la API real que se use
    resp = requests.post(f"{API_URL}/records", json=registros, timeout=10)
    return {"status": resp.status_code, "body": resp.json()}


def api_get_records():
    """GET /records. Con la API simulada devuelve lo guardado en esta sesión."""
    if USAR_API_SIMULADA:
        return {"status": 200, "body": st.session_state.get("api_registros", [])}

    import requests
    # PENDIENTE: ajustar la ruta al endpoint de la API real que se use
    resp = requests.get(f"{API_URL}/records", timeout=10)
    return {"status": resp.status_code, "body": resp.json()}



# 5.4 Pantalla de carga de Excel
#     Lo que guarda la API simulada alimenta el mapa de arriba: al guardar se
#     vuelve a correr la página (st.rerun) y el mapa dibuja los registros nuevos.

def mostrar_respuesta_api(respuesta):
    codigo = respuesta["status"]
    cuerpo = respuesta["body"]
    if codigo == 201:
        st.success(f"API respondió {codigo}: {cuerpo.get('inserted', 0)} registro(s) guardado(s).")
    elif codigo == 207:
        st.warning(
            f"API respondió {codigo}: se guardaron {cuerpo.get('inserted', 0)} y "
            f"se rechazaron {len(cuerpo.get('rejected', []))}."
        )
    else:
        st.error(f"API respondió {codigo}: no se guardó ningún registro.")
    if USAR_API_SIMULADA:
        st.caption("API simulada: los datos solo viven en la memoria de la app.")
    st.json(respuesta)


st.divider()
st.header("Carga de Excel")
st.write(
    "Sube un .xlsx con las columnas: **" + ", ".join(COLUMNAS_REQUERIDAS) + "** "
    "(fecha en formato AAAA-MM-DD)."
)
st.caption(
    "Para verlos en el mapa agrega las columnas opcionales **lat** y **lon** "
    "(y **confidence** de 0 a 1; si no la pones se usa 1)."
)
if not any(
    r.get("lat") is not None and r.get("lon") is not None
    for r in st.session_state.get("api_registros", [])
):
    st.info(
        "El mapa está vacío porque los datos simulados están desactivados. "
        "Sube un Excel con lat y lon y envíalo a la API para verlo en el mapa."
    )
archivo = st.file_uploader("Archivo Excel", type=["xlsx"])

if archivo is not None:
    # cargar_archivo() trabaja con una ruta, así que se guarda un temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(archivo.getvalue())
        ruta_tmp = tmp.name

    archivo_ok = cargar_archivo(ruta_tmp)
    os.remove(ruta_tmp)

    if archivo_ok:
        validos, errores = validar_contenido_excel(archivo)

        if validos:
            st.success(f"{len(validos)} registro(s) válido(s)")
            st.dataframe(pd.DataFrame(validos))
        if errores:
            st.error(f"{len(errores)} problema(s) encontrado(s)")
            for e in errores:
                st.write("• " + e)

        if validos and st.button("Enviar registros válidos a la API"):
            with st.spinner("Enviando a la API..."):
                if USAR_API_SIMULADA:
                    time.sleep(0.6)  # simula el tiempo de respuesta de una API
                respuesta = api_post_records(validos)
            st.session_state.ultima_respuesta = respuesta
            if respuesta["body"].get("inserted", 0) > 0:
                st.rerun()  # vuelve a dibujar el mapa con los registros nuevos

# Respuesta de la última vez que se envió a la API
if "ultima_respuesta" in st.session_state:
    st.markdown("**Última respuesta de la API**")
    mostrar_respuesta_api(st.session_state.ultima_respuesta)


# Registros que ya "guardó" la API (GET /records)
st.divider()
with st.expander("Registros guardados en la API (GET /records)"):
    registros_api = api_get_records()["body"]
    if registros_api:
        st.dataframe(pd.DataFrame(registros_api))
        sin_coord = sum(1 for r in registros_api if r.get("lat") is None or r.get("lon") is None)
        if sin_coord:
            st.caption(f"{sin_coord} registro(s) no tienen lat/lon y no se dibujan en el mapa.")
    else:
        st.write("Todavía no hay registros guardados.")
    if USAR_API_SIMULADA and registros_api and st.button("Borrar registros de la API simulada"):
        st.session_state.api_registros = []
        st.session_state.pop("ultima_respuesta", None)
        st.rerun()
