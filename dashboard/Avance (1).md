# Avance Mapa Interactivo

**Alumno:** Edgar Eduardo Lopez Orozco
**Periodo:** Semana 1 – Semana 2
**Lo que me tocó:** Dentro del módulo Dashboard, el mapa interactivo (según el Plan de Trabajo, esto cae en la Semana 2 del cronograma).

\---

## Qué hice, estudié esta semana y media

Primero me puse a leer bien para ubicar exactamente qué me tocaba a mí dentro del Dashboard. Mis compañeros (Jesus y Emilio) están viendo login, roles y el CRUD, y a mí me quedó el mapa.

También repasé el contrato JSON que pusimos de ejemplo con el resto del equipo (los campos que va a mandar la API de PostgreSQL: `date`, `day`, `street`, `neighborhood`, `confidence`, `source`, `created\\\_at`, `created\\\_by`), porque necesitaba saber con qué estructura de datos voy a trabajar antes de ponerme a programar cualquier cosa.

Ya con eso claro, me metí a investigar las librerías que necesito para esta parte:

* **Folium:** para el mapa. Usa OpenStreetMap como base, que es gratis y no pide API key (a diferencia de Google Maps), y deja poner marcadores, rutas y agrupar puntos.
* **streamlit-folium:** esta la tuve que investigar más porque no sabía para qué era exactamente. Resulta que Streamlit no puede mostrar un mapa de Folium por sí solo — necesita este "puente" para renderizarlo y además para poder capturar si el usuario le da clic a algo del mapa.
* **pandas:** para acomodar los datos que lleguen en JSON antes de mandárselos a Folium.

## Acuerdos con el equipo

Quedamos en no cambiar las librerías que ya estaban en el plan (aunque existen otras opciones como Google Maps), porque Folium + OpenStreetMap no necesita pagar nada. También quedó claro que yo no toco la base de datos directo — todo lo que muestre en el mapa viene de la API, nunca conecto a PostgreSQL por mi cuenta.

Otra cosa que se aclaró: el mapa necesita coordenadas (lat y lon), y esas **no** vienen en el contrato base del Dashboard — hay que pedirlas a la API de Catastro. Mientras esa parte no esté lista, voy a trabajar con coordenadas simuladas.

## Pruebas de código

Esta primera etapa la usé sobre todo para investigar, así que no traía código todavía. Para este reporte sí armé un primer script de prueba (`ejemplo\\\_dashboard.py`, está en esta misma carpeta) nada más para comprobar que el mapa funciona como esperaba.

Lo que hice en el script:

* Inventé unos datos de ejemplo con la misma estructura del contrato JSON (le agregué lat/lon a mano porque en el futuro esos datos van a venir de Catastro).
* Con Folium + streamlit-folium hice el mapa, con un marcador por cada registro y un popup que muestra la calle, la colonia y el nivel de confianza.
* Agregué un filtro por colonia en la barra lateral, para ver que sí se actualiza el mapa al cambiarlo.

Para correrlo:

```
pip install streamlit pandas folium streamlit-folium
streamlit run ejemplo\\\_dashboard.py
```

## Qué aprendí

Lo que más me costó entender al principio fue por qué el plan pedía `streamlit-folium` si ya tenía `folium` pensé que era redundante. Ya investigando, entendí que Streamlit no sabe renderizar un objeto de Folium por sí solo, entonces sin ese paquete el mapa simplemente no aparece.

También aprendí que Folium arma el mapa como un objeto completo y luego se "inyecta" en la página, no es algo que Streamlit actualice solo en partes — o sea que hay que tener cuidado de que no se esté recargando todo el mapa de más cada vez que alguien interactúa con algo.

## Errores

Al ir probando el script por partes, quise confirmar qué tan cierto era eso de que "Folium solo no funciona en Streamlit" que había leído en la investigación. Así que desinstalé `streamlit-folium` a propósito y dejé solo `streamlit`, `pandas` y `folium`, y traté de importar el módulo:

```python
import streamlit as st
from streamlit\\\_folium import st\\\_folium
```

Error que me marcó:

```
Traceback (most recent call last):
  File "<string>", line 3, in <module>
ModuleNotFoundError: No module named 'streamlit\\\_folium'
```

**Causa:** `streamlit-folium` no es parte de Streamlit ni de Folium, es un paquete aparte que hay que instalar explícitamente (`pip install streamlit-folium`). Si no está instalado, ni siquiera truena al momento de dibujar el mapa — truena desde el `import`, antes de correr cualquier otra línea del script.

**Solución:** reinstalar el paquete:

```
pip install streamlit-folium
```

Después de esto el `import` y el resto del script volvieron a correr sin problema.

Esto confirma que Folium y streamlit-folium son dos librerías independientes, y ambas son obligatorias para que el mapa aparezca dentro de Streamlit — no es opcional ni redundante tenerlas por separado en el `requirements.txt`.

Los demás errores (de datos, de conexión a las APIs reales) los voy a ir documentando aquí conforme pasen en la siguiente etapa, cuando conecte con PostgreSQL y Catastro.

## Lo que sigue

* Conectar el script a la API real de PostgreSQL (cambiar los datos inventados por una petición con `requests`).
* Conectar la API de Catastro para traer coordenadas reales en vez de las que puse a mano.
* Agrupar puntos en el mapa (`MarkerCluster`) si crecen mucho los datos, y agregar rutas (`PolyLine`) si se llega a necesitar.

