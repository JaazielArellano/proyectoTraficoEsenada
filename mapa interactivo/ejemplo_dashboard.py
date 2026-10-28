"""
ejemplo_dashboard.py

Prototipo del componente "Mapa interactivo" del módulo Dashboard.

Autor: Edgar Eduardo Lopez Orozco
Proyecto: Proyecto Integrador de Extracción de Datos Geográficos (Ensenada)

Cómo correrlo:
    pip install streamlit pandas folium streamlit-folium requests
    streamlit run ejemplo_dashboard.py
"""
import unicodedata
import pandas as pd
import folium
import streamlit as st
import requests
from streamlit_folium import st_folium


st.set_page_config(page_title="Dashboard - Mapa", layout="wide")
st.title("Prototipo: Mapa Interactivo")

# Lista para guardar las notas que ubiques en el mapa.
# Se crea una sola vez; así no se borra cada vez que haces clic en algo.
if "notas" not in st.session_state:
    st.session_state.notas = []


# API: CRUD Dinámica PostgreSQL (puerto 4003)
# Elige la tabla desde la barra lateral

BASE_URL = "http://148.231.239.96:4003/api/datos"

TABLAS = {
    "Noticias (alexis_datos)": "alexis_datos",
    "CESPE": "cespe",
    "Otra tabla (escribir nombre)": None,
}

opcion_tabla = st.sidebar.selectbox("Tabla de la API", list(TABLAS))
if TABLAS[opcion_tabla] is None:
    TABLA_API = st.sidebar.text_input("Nombre de la tabla").strip()
    if not TABLA_API:
        st.info("Escribe el nombre de la tabla en la barra lateral.")
        st.stop()
else:
    TABLA_API = TABLAS[opcion_tabla]

# Nombres posibles de cada columna (el código usa el primero que exista en la tabla).
ALIAS = {
    "titulo": [
        "titulo", "title", "nombre", "descripcion", "asunto",
        "motivo", "evento", "aviso", "tipo",
    ],
    "fecha": [
        "fecha_extraccion", "fecha", "fecha_inicio", "fecha_aviso",
        "fecha_publicacion", "date", "created_at",
    ],
    "url": ["url", "link", "enlace"],
    "lat": ["latitud", "lat", "latitude"],
    "lon": ["longitud", "lon", "lng", "longitude"],
    "lugar_texto": [
        "colonia", "nomb_asent", "zona", "sector", "ubicacion",
        "lugar", "direccion", "calle", "nom_vial",
    ],
}


def arreglar_texto(valor):
    """Corrige acentos mal codificados (ej. 'JuÃ¡rez' -> 'Juárez') y quita espacios."""
    if not isinstance(valor, str):
        return valor
    try:
        valor = valor.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    return valor.strip()


# Lugares de la zona con coordenadas APROXIMADAS (centro de cada lugar).
# Agrega o corrige los que necesites: "nombre en minúsculas y sin acentos": (lat, lon)
LUGARES = {
    "playas de chapultepec": (31.8500, -116.6300),
    "chapultepec": (31.8500, -116.6300),
    "valle de guadalupe": (32.0800, -116.5800),
    "maneadero": (31.7300, -116.5600),
    "punta banda": (31.7000, -116.6700),
    "el sauzal": (31.8900, -116.6800),
    "sauzal": (31.8900, -116.6800),
    "ojos negros": (31.9200, -116.2800),
    "san quintin": (30.5600, -115.9400),
    "playitas": (31.8506, -116.6142),
    "valle dorado": (31.8724, -116.6205),
    "ensenada": (31.8667, -116.5964),
    "rosarito": (32.3600, -117.0600),
    "tecate": (32.5700, -116.6250),
    "tijuana": (32.5149, -117.0382),
    "mexicali": (32.6245, -115.4523),
}


def sin_acentos(cadena):
    """Quita acentos y pasa a minúsculas, para comparar texto sin importar tildes."""
    cadena = unicodedata.normalize("NFD", str(cadena))
    return "".join(
        ch for ch in cadena if unicodedata.category(ch) != "Mn"
    ).lower()


def ubicar(cadena):
    """Busca en la cadena un lugar conocido. Regresa (lugar, lat, lon) o (None, None, None)."""
    t = sin_acentos(cadena)
    # Busco primero los nombres más largos (ej. 'playas de chapultepec' antes que 'chapultepec')
    for lugar in sorted(LUGARES, key=len, reverse=True):
        if lugar in t:
            plat, plon = LUGARES[lugar]
            return lugar.title(), plat, plon
    return None, None, None


@st.cache_data(ttl=600)
def descargar_datos(tabla):
    """Descarga los registros de una tabla desde la API y los regresa como DataFrame."""
    # OJO: aquí NO atrapo errores. Si la API falla, Streamlit no guarda nada
    # en memoria y en el siguiente intento vuelve a consultarla.
    resp = requests.get(f"{BASE_URL}/{tabla}", params={"page": 1, "limit": 100}, timeout=30)
    resp.raise_for_status()
    resp.encoding = "utf-8"    # evita caracteres raros (acentos, ñ)
    data = resp.json()

    # La respuesta puede ser una lista o un dict con la lista adentro
    if isinstance(data, dict):
        registros = (data.get("datos") or data.get("data")
                     or data.get("items") or data.get("resultados") or [])
    else:
        registros = data
    return pd.DataFrame(registros)


def preparar(raw):
    """Crea columnas estándar (titulo, fecha, url, lat, lon, lugar_texto)
    a partir de la tabla cruda que llega de la API."""
    d = raw.copy().reset_index(drop=True)

    for destino, candidatos in ALIAS.items():
        d[destino] = None
        for col in candidatos:
            if col in raw.columns:
                d[destino] = raw[col].reset_index(drop=True)
                break

    # Si la tabla no trae título pero sí enlace, uso el final del enlace (ej. 'corte-1001')
    if d["titulo"].isna().all() and d["url"].notna().any():
        d["titulo"] = d["url"].apply(
            lambda u: str(u).rstrip("/").rsplit("/", maxsplit=1)[-1]
            if pd.notna(u) else None
        )

    d["titulo"] = d["titulo"].apply(arreglar_texto)
    d["lugar_texto"] = d["lugar_texto"].apply(arreglar_texto)
    d["fecha"] = d["fecha"].apply(
        lambda x: "" if x is None or (isinstance(x, float) and pd.isna(x)) else str(x)[:10])
    d["lat"] = pd.to_numeric(d["lat"], errors="coerce")
    d["lon"] = pd.to_numeric(d["lon"], errors="coerce")
    d["titulo"] = d["titulo"].fillna("(sin título)")

    if (d["fecha"] != "").any():
        d = d.sort_values("fecha", ascending=False).reset_index(drop=True)
    return d


def cargar_datos(tabla):
    """Regresa (tabla_cruda, mensaje_de_error). Si todo salió bien, el error es None."""
    try:
        return descargar_datos(tabla), None
    except requests.exceptions.RequestException as e:
        print("No se pudo conectar a la API:", e)
        return pd.DataFrame(), str(e)


df_raw, error_api = cargar_datos(TABLA_API)
print("Columnas de la API:", list(df_raw.columns))   # para ver qué trae la tabla
df = preparar(df_raw) if len(df_raw) > 0 else pd.DataFrame(
    columns=["titulo", "fecha", "url", "lat", "lon", "lugar_texto"])


# 2. Configuración de página + buscador

st.caption(f"Tabla: {TABLA_API}. Naranja = ubicación automática, azul = ubicada por ti con clic.")

if error_api:
    st.warning(
        "No se pudo conectar a la API. Intenta de nuevo en un momento. "
        f"Detalle: {error_api}"
    )
elif len(df) == 0:
    st.warning("La API respondió, pero la tabla no tiene registros.")

if st.sidebar.button("Recargar datos"):
    st.cache_data.clear()
    st.rerun()

busqueda = st.sidebar.text_input("Buscar")
if busqueda:
    # Busca sin importar mayúsculas ni acentos, en título y lugar
    texto_busqueda = sin_acentos(busqueda)
    mascara = (df["titulo"].astype(str) + " " + df["lugar_texto"].astype(str)).apply(
        lambda t: texto_busqueda in sin_acentos(t))
    df_filtrado = df[mascara].copy()
else:
    df_filtrado = df.copy()

# Ubicación: si la tabla trae coordenadas las uso; si no, busco el lugar en el texto
def ubicar_fila(registro):
    """Regresa (lugar, lat, lon, exacta) para un registro del DataFrame.

    exacta=True si la coordenada vino de la API; False si se dedujo
    buscando un lugar conocido dentro del texto del registro.
    """
    if pd.notna(registro["lat"]) and pd.notna(registro["lon"]):
        return (
            registro["lugar_texto"] or "Coordenadas de la API",
            registro["lat"],
            registro["lon"],
            True,
        )
    texto_registro = f"{registro['titulo']} {registro['lugar_texto'] or ''}"
    lugar, plat, plon = ubicar(texto_registro)
    return lugar, plat, plon, False

if len(df_filtrado) > 0:
    ubic = df_filtrado.apply(ubicar_fila, axis=1)
    df_filtrado["lugar"] = ubic.apply(lambda x: x[0])
    df_filtrado["lat"] = ubic.apply(lambda x: x[1])
    df_filtrado["lon"] = ubic.apply(lambda x: x[2])
    df_filtrado["exacta"] = ubic.apply(lambda x: x[3])
else:
    for c in ["lugar", "exacta"]:
        df_filtrado[c] = None
df_en_mapa = df_filtrado.dropna(subset=["lat", "lon"])

st.sidebar.write(f"Registros: {len(df_filtrado)} de {len(df)}")
st.sidebar.write(f"Ubicados en el mapa: {len(df_en_mapa)}")
st.sidebar.caption("Escribe y presiona Enter para buscar.")


# 3. Mapa interactivo con Folium + streamlit-folium

puntos = [(r["lat"], r["lon"]) for _, r in df_en_mapa.iterrows()]
puntos += [(n["lat"], n["lon"]) for n in st.session_state.notas]

if puntos:
    centro_lat = sum(p[0] for p in puntos) / len(puntos)
    centro_lon = sum(p[1] for p in puntos) / len(puntos)
else:
    centro_lat, centro_lon = 31.8667, -116.5964   # Ensenada

# tiles=None crea el mapa sin fondo, y abajo le agregamos dos fondos.
mapa = folium.Map(location=[centro_lat, centro_lon], zoom_start=13, tiles=None)

# Fondo 1: cartografía (calles)
folium.TileLayer("OpenStreetMap", name="Cartografía (calles)").add_to(mapa)

# Fondo 2: satélite
esri_satelite_url = (
    "https://server.arcgisonline.com/ArcGIS/rest/services/"
    "World_Imagery/MapServer/tile/{z}/{y}/{x}"
)
folium.TileLayer(
    tiles=esri_satelite_url,
    attr="Esri",
    name="Satélite",
).add_to(mapa)

# Botón en el mapa para cambiar entre cartografía y satélite
folium.LayerControl().add_to(mapa)

# Marcadores naranjas: registros ubicados automáticamente
repetidos = {}
for _, fila in df_en_mapa.iterrows():
    lat, lon = fila["lat"], fila["lon"]
    if not fila["exacta"]:
        # Pequeño desplazamiento para que no se encimen varios registros del mismo lugar
        k = repetidos.get(fila["lugar"], 0)
        repetidos[fila["lugar"]] = k + 1
        lat += 0.003 * (k // 4)
        lon += 0.003 * (k % 4)
    popup_html = f"<b>{fila['titulo']}</b><br>Lugar: {fila['lugar']}"
    if not fila["exacta"]:
        popup_html += " (aproximado)"
    if fila["fecha"]:
        popup_html += f"<br>Fecha: {fila['fecha']}"
    if pd.notna(fila["url"]) and fila["url"]:
        popup_html += f"<br><a href='{fila['url']}' target='_blank'>Ver más</a>"
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=fila["titulo"],
        icon=folium.Icon(color="orange"),
    ).add_to(mapa)

# Marcadores azules para las notas que ya ubicaste
for nota in st.session_state.notas:
    popup_html = f"<b>{nota['calle'] or 'Sin lugar'}</b><br>{nota['texto']}"
    if nota.get("url"):
        popup_html += f"<br><a href='{nota['url']}' target='_blank'>Ver más</a>"
    folium.Marker(
        location=[nota["lat"], nota["lon"]],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=nota["calle"] or nota["texto"][:40],
        icon=folium.Icon(color="blue"),
    ).add_to(mapa)

# Ajusta la vista para que se vean todos los puntos
if puntos:
    mapa.fit_bounds(
        [[min(p[0] for p in puntos), min(p[1] for p in puntos)],
         [max(p[0] for p in puntos), max(p[1] for p in puntos)]],
        max_zoom=13,
    )

resultado = st_folium(mapa, width=None, height=550, returned_objects=["last_clicked"])


# 4. Ubicar un registro con un clic en el mapa

clic = resultado.get("last_clicked")

if clic:
    st.write(f"Punto seleccionado: {clic['lat']:.5f}, {clic['lng']:.5f}")

    # Opción -1 = escribir una nota manual; las demás son registros de la API
    opciones = [-1] + list(df_filtrado.index)

    def etiqueta(i):
        """Texto que se muestra en el selector para cada opción del combo."""
        if i == -1:
            return "(Escribir nota manualmente)"
        fecha = df_filtrado.loc[i, "fecha"]
        titulo_registro = df_filtrado.loc[i, "titulo"]
        if fecha:
            return f"{fecha} - {titulo_registro}"
        return str(titulo_registro)

    elegida = st.selectbox("Registro a ubicar en este punto", opciones, format_func=etiqueta)
    calle = st.text_input("Calle o lugar")

    if elegida == -1:
        texto = st.text_area("Noticia o dato")
        url = ""
    else:
        texto = df_filtrado.loc[elegida, "titulo"]
        url = df_filtrado.loc[elegida, "url"]
        url = url if pd.notna(url) else ""

    if st.button("Guardar nota"):
        st.session_state.notas.append({
            "calle": calle,
            "texto": texto,
            "url": url,
            "lat": clic["lat"],
            "lon": clic["lng"],
        })
        # Vuelve a correr el script para que el marcador azul aparezca en el mapa
        st.rerun()
else:
    st.info("Haz clic en un punto del mapa para ubicar un registro.")


# 5. Tablas de la API

st.subheader("Registros de la API")
tabla_resumen = df_filtrado[["fecha", "titulo", "lugar", "url"]].copy()
tabla_resumen["lugar"] = tabla_resumen["lugar"].fillna("—")
tabla_resumen["fecha"] = tabla_resumen["fecha"].replace("", "—")
st.dataframe(
    tabla_resumen,
    column_config={
        "fecha": "Fecha",
        "titulo": "Título",
        "lugar": "Lugar detectado",
        "url": st.column_config.LinkColumn("Enlace"),
    },
    hide_index=True,
)

with st.expander("Ver la tabla completa tal cual viene de la API (todas las columnas)"):
    st.write("Columnas:", list(df_raw.columns))
    st.dataframe(df_raw, hide_index=True)
