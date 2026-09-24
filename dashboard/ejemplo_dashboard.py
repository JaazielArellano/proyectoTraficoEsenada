"""
ejemplo_dashboard.py

Script de ejemplo prototipo para el componente de:
"Mapa interactivo" del módulo Dashboard.

Autor: Edgar Eduardo Lopez Orozco
Proyecto: Proyecto Integrador de Extracción de Datos Geográficos (Ensenada)

Este script usa DATOS SIMULADOS que respetan el contrato JSON acordado con
el equipo, más latitud/
longitud simuladas, solo para poder probar el mapa mientras esa integración no está lista.

Cómo correrlo:
    pip install streamlit pandas folium streamlit-folium
    streamlit run ejemplo_dashboard.py
"""

import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium


# 1. Datos simulados (mock) mismos campos que el contrato JSON del proyecto
#    + latitud/longitud simuladas en el futuro vendrán de la API de Catastro

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

# 2. Configuración de página + filtro simple por colonia

st.set_page_config(page_title="Dashboard - Mapa", layout="wide")
st.title("Prototipo: Mapa Interactivo")
st.caption("Datos simulados (mock)  pendiente de conectar a la API real de PostgreSQL/Catastro")

colonias = ["Todas"] + sorted(df["neighborhood"].unique().tolist())
colonia_seleccionada = st.sidebar.selectbox("Filtrar por colonia", colonias)

# Hace la Filtracion del  DataFrame según la colonia elegida por el usuario.
# Si eligió "Todas", se usan todos los registros; si no, solo los de esa colonia.
if colonia_seleccionada == "Todas":
    df_filtrado = df
else:
    df_filtrado = df[df["neighborhood"] == colonia_seleccionada]

st.write("Mostrando registros en el mapa.")


# 3. Mapa interactivo con Folium + streamlit-folium

if len(df_filtrado) > 0:
    centro_lat = df_filtrado["lat"].mean()
    centro_lon = df_filtrado["lon"].mean()
else:
    centro_lat, centro_lon = 31.8667, -116.5964 

mapa = folium.Map(location=[centro_lat, centro_lon], zoom_start=13, tiles="OpenStreetMap")

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

st_folium(mapa, width=None, height=550)