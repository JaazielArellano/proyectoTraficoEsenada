# Dashboard Componente: Mapa Interactivo

**Proyecto:** Proyecto Integrador de Extracción de Datos Geográficos (Ensenada)
**Módulo general:** Dashboard (Aplicación Web, Visualización y Administración)
**Responsable de este componente:** Edgar Eduardo Lopez Orozco
**Materia:** Patrones De Comportamiento De Datos – Grupo 371
**Equipo del módulo Dashboard:** Jesus Luna García, Jorge Emilio García Raygoza, Edgar Eduardo Lopez Orozco

## ¿Qué es este componente?

Este es uno de los sub-componentes del módulo **Dashboard** del proyecto integrador. Mientras que mis compañeros trabajan en autenticación/roles, CRUD de registros, y carga/exportación de Excel, a mí (Edgar) me corresponde la parte de:

* **Mapa interactivo** con la información geográfica del sistema (con Folium + streamlit-folium)
* Búsqueda y filtrado de puntos geográficos sobre el mapa

Según el Plan de Trabajo, este componente corresponde a la **Semana 2** del cronograma general del módulo.

## Alcance de este componente

* Consumir la API de Catastro para obtener las coordenadas normalizadas de los registros.
* Consumir datos ya entregados por la API de PostgreSQL (el Dashboard **no** accede directamente a la base de datos).
* Transformar esos datos (vía pandas) y representarlos en un mapa interactivo con marcadores, y en el futuro rutas y agrupación de puntos.

## Tecnologías utilizadas en este componente

|Librería|Uso en este componente|
|-|-|
|`folium`|Construcción del mapa interactivo (marcadores, rutas, mapas de coropletas) sobre OpenStreetMap|
|`streamlit-folium`|Puente para renderizar el mapa de folium dentro de Streamlit y capturar interacción del usuario|
|`pandas`|Estructura intermedia entre el JSON que devuelven las APIs y los datos que se dibujan en el mapa|
|`OpenStreetMap`|Proveedor de mosaicos (tiles) del mapa base, gratuito y sin necesidad de API key|

## Contenido de esta carpeta

* `README.md` – este archivo
* `Avance.md` – bitácora detallada de avance semanal (investigación, decisiones, pruebas, aprendizajes)
* `ejemplo\_dashboard.py` – script de ejemplo funcional (primer prototipo) del mapa, como punto de partida para el desarrollo real del componente

## Estado actual

🔶 En investigación / prototipo inicial. Aún no conectado a las APIs reales de PostgreSQL/Catastro (se está trabajando con datos simulados que respetan el contrato JSON acordado).

