"""
ejemplo_dashboard.py

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

df = pd.DataFrame(MOCK_DATA)

# NUEVO: lista para guardar las notas que escribas.
# Se crea una sola vez; así no se borra cada vez que haces clic en algo.
if "notas" not in st.session_state:
    st.session_state.notas = []


# 2. Configuración de página + filtro simple por colonia

st.set_page_config(page_title="Dashboard - Mapa", layout="wide")
st.title("Prototipo: Mapa Interactivo")
st.caption("Datos simulados (mock)  pendiente de conectar a la API real de PostgreSQL/Catastro")

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
