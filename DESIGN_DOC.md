# Mapa Interactivo – Dashboard

**Link:** (link a este archivo una vez subido al repo)
**Author(s):** Edgar Eduardo Lopez Orozco
**Status:** Draft
**Última actualización:** 2026-10-07

## Contenido
- Goals
- Non-Goals
- Background
- Diseño propuesto
- Alternativas consideradas

---

## Goals

- Mostrar en un mapa interactivo los registros geográficos recolectados por el sistema (calle, colonia, nivel de confianza, fuente del dato).
- Permitir filtrar los registros visibles en el mapa por colonia.
- Permitir alternar entre vista de cartografía (calles) y vista satelital.
- Permitir agregar notas sobre un punto del mapa con un clic.
- Que el mapa funcione sin depender de una API de pago (ej. Google Maps), usando OpenStreetMap/Esri como proveedores de mosaicos gratuitos.
- Dejar el componente listo para conectarse a datos reales, aunque por ahora funcione con datos simulados.

## Non-Goals

- Este componente **no** se encarga de extraer, limpiar ni validar los datos geográficos (eso corresponde a otros módulos del sistema).
- Este componente **no** administra ni modifica directamente la base de datos.
- No incluye, por ahora, trazado de rutas (`PolyLine`) ni agrupación de puntos (`MarkerCluster`) — queda como posible mejora futura si el volumen de datos lo requiere.
- No incluye autenticación ni manejo de roles — eso lo cubre otro componente del equipo (Jesus).
- Las notas que se agregan con clic **no** se guardan de forma permanente todavía (solo viven en memoria mientras la app está abierta); guardarlas de forma persistente queda como trabajo futuro.

## Background

Dentro del Plan de Trabajo del módulo Dashboard, el reparto de tareas me asignó específicamente el **mapa** (Semana 2 del cronograma). El Dashboard en general actúa solo como capa de presentación: consume los datos del sistema, nunca accede directo a la base de datos ni a los módulos de extracción.

El mapa necesita coordenadas (latitud/longitud) para ubicar cada registro, pero esas coordenadas no vienen en el contrato JSON base del Dashboard — se obtienen normalizadas desde otro módulo del sistema. Por eso, mientras esa integración no esté lista, el prototipo usa coordenadas simuladas que respetan la misma estructura que se espera recibir en producción.

## Diseño propuesto

- **Obtención de datos:** el componente recibirá una lista de registros (JSON) con la información geográfica, ya enriquecidos con sus coordenadas (latitud/longitud).
- **Transformación:** los datos se cargan en un DataFrame de `pandas` para poder filtrarlos fácilmente (por colonia).
- **Renderizado del mapa:** se usa `folium` para construir el mapa (con OpenStreetMap como base), agregando un marcador por cada registro, con un popup mostrando calle, colonia, confianza y fuente. El color del marcador indica el nivel de confianza (rojo si es bajo, verde si es alto).
- **Integración con Streamlit:** como Streamlit no puede renderizar objetos de Folium de forma nativa, se usa `streamlit-folium` (función `st_folium`) para mostrarlo dentro de la app.
- **Filtro:** un `selectbox` en la barra lateral de Streamlit permite elegir una colonia específica o ver todos los registros.
- **Capas de cartografía/satélite:** se agregan dos `folium.TileLayer` (OpenStreetMap y el servicio de imágenes satelitales de Esri) junto con `folium.LayerControl`, para que el usuario elija el fondo del mapa.
- **Notas con clic:** `streamlit-folium` devuelve el último punto donde el usuario hizo clic (`last_clicked`). Con ese dato se muestran campos para escribir una calle y una nota, que se guardan en `st.session_state` y se dibujan como un nuevo marcador en el mapa.

## Alternativas consideradas

- **Google Maps / Mapbox:** se descartaron porque requieren una API key y, en el caso de Google Maps, tienen costo asociado a partir de cierto volumen de uso. OpenStreetMap es gratuito y no requiere llave.
- **Plotly (mapbox/scattermapbox) en vez de Folium:** se descartó porque el equipo ya había definido Folium + streamlit-folium en el Plan de Trabajo, y Folium ofrece más flexibilidad nativa para marcadores, popups y agrupación de puntos sin depender de una cuenta de Mapbox.
