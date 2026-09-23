# Dashboard Componente: Gráficas, Indicadores y Mapa Interactivo

**Proyecto:** Proyecto Integrador de Extracción de Datos Geográficos (Ensenada)
**Módulo general:** Dashboard (Aplicación Web, Visualización y Administración)
**Responsable de este componente:** Edgar Eduardo Lopez Orozco
**Materia:** Patrones De Comportamiento De Datos Grupo 371
**Equipo del módulo Dashboard:** Jesus Luna García, Jorge Emilio García Raygoza, Edgar Eduardo Lopez Orozco

## ¿Qué es este componente?

Este es uno de los sub componentes del módulo **Dashboard** del proyecto integrador. Mientras que otros compañeros del equipo trabajan en autenticación los roles, CRUD de registros, y carga También exportación de Excel, a mí **Edgar** me corresponde la parte de:

* **Panel de indicadores y gráficas dinámicas** (con Plotly / Plotly Express)
* **Mapa interactivo** con la información geográfica del sistema (con Folium + streamlit-folium)
* Búsqueda y filtrado de puntos geográficos sobre el mapa

en el Plan de Trabajo, este componente corresponde a la **Semana 2** del cronograma general del módulo.

## Alcance de este componente

* Consumir datos ya entregados por la API de PostgreSQL el Dashboard **no** accede directamente a la base de datos).
* Consumir la API de Catastro para obtener coordenadas normalizadas de los registros.
* Transformar esos datos (vía pandas) en:

  * Las Gráficas interactivas en el  conteo de registros por colonia, evolución por fecha, nivel de confianza promedio,
  * Un mapa interactivo con marcadores, y en el futuro rutas y la agrupación de puntos.

## Tecnologías utilizadas en este componente

|Librería|Uso en este componente|
|-|-|
|plotly,plotly.express|Gráficas interactivas **zoom, paneo, hover** a partir de DataFrames de pandas|
|folium|Construcción del mapa interactivo **marcadores, rutas, mapas de coropletas** sobre OpenStreetMap|
|streamlit-folium|Puente para renderizar el mapa de **folium** dentro de **Streamlit** y capturar interacción del usuario|
|pandas|Estructura intermedia entre el **JSON** que devuelven las **APIs** y las funciones de graficado|
|OpenStreetMap|Proveedor de mosaicos **tiles** del mapa base, gratuito y sin necesidad de **API key**|



