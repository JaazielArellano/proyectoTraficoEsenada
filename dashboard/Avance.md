# Avance Gráficas, Indicadores y Mapa Interactivo

**Alumno:** Edgar Eduardo Lopez Orozco
**Periodo:** Semana 1 – Semana 2
**Lo que me tocó:** Dentro del módulo Dashboard, la parte de gráficas, indicadores y el mapa interactivo (según el Plan de Trabajo, esto cae en la Semana 2 del cronograma).

\---

## Qué hice: estudié esta semana y media

Primero me puse a leer bien para ubicar exactamente qué me tocaba a mí dentro del Dashboard. Mis compañeros (Jesus y Emilio) están viendo login roles y el CRUD, y a mí me quedó la parte visual: gráficas, indicadores y el mapa.

También repasé el contrato JSON que pusimos de ejemplos con el resto del equipo los campos que va a mandar la API de PostgreSQL: date, day, street, neighborhood, confidence, source, created\_at, created\_by , porque necesitaba saber con qué estructura de datos voy a trabajar antes de ponerme a programar cualquier cosa.

Ya con eso claro, me metí a investigar las librerías que ya estaban puestas en el plan para mi parte:

* **Plotly y Plotly Express:** para las gráficas. Lo que me convenció es que se conecta directo con Streamlit ,st.plotly\_chart, y recibe DataFrames de pandas tal cual, sin tener que estar transformando datos.
* **Folium:** para el mapa. Usa OpenStreetMap como base, que es gratis y no pide API key (a diferencia de Google Maps), y deja poner marcadores, rutas y agrupar puntos.
* **streamlit-folium:** esta la tuve que investigar más porque no sabía para qué era exactamente. Resulta que Streamlit no puede mostrar un mapa de Folium por sí solo — necesita este "puente" para renderizarlo y además para poder capturar si el usuario le da clic a algo del mapa.
* **pandas:** para acomodar los datos que lleguen en JSON antes de mandárselos a Plotly o Folium.

## Acuerdos con el equipo

Quedamos en no cambiar las librerías que ya estaban en el plan (aunque existen otras opciones como Matplotlib o Google Maps), porque Plotly se acopla mejor a Streamlit también en pandas y Folium+OpenStreetMap no necesita pagar nada. También quedó claro que yo no toco la base de datos directo todo lo que muestre en el Dashboard viene de la API, nunca conecto a PostgreSQL por mi cuenta.

Otra cosa que se aclaró: el mapa necesita coordenadas (lat y lon), y esas **no** vienen en el contrato base del Dashboard  hay que pedirlas a la API de Catastro. Mientras esa parte no esté lista, voy a trabajar con coordenadas simuladas.

## Pruebas de código

Esta primera etapa la usé sobre todo para investigar y armar la justificación , así que no traía código todavía. Para este reporte sí armé un primer py de prueba (ejemplo\_dashboard.py, está en esta misma carpeta) nada más para comprobar que las librerías realmente funcionan juntas como esperaba.

Lo que hice en el script:

* Inventé unos datos de ejemplo con la misma estructura del contrato JSON (le agregué lat y lon a mano porque en el futuro esos datos van a venir de Catastro).
* Con Plotly hice una gráfica de barras (registros por colonia) y una de línea (registros por fecha).
* Con Folium mas streamlit-folium hice el mapa, con un marcador por cada registro y un popup que muestra la calle, la colonia y el nivel de confianza.
* Agregué un filtro por colonia en la barra lateral, para ver que sí se actualizan la gráfica y el mapa al cambiarlo.

Para correrlo:
pip install streamlit plotly pandas folium streamlit-folium
streamlit run ejemplo\_dashboard.py


## Qué aprendí

Lo que más me costó entender al principio fue por qué el plan pedía streamlit-folium si ya tenía folium pensé que era redundante. Ya investigando, entendí que Streamlit no sabe renderizar un objeto de Folium por sí solo, entonces sin ese paquete el mapa simplemente no aparece.

También aprendí que con `plotly.express` uno arma una gráfica casi completa en una sola línea (tipo px.bar(df, x="neighborhood")), a diferencia de Plotly "normal" que pide mucho más código.

Y algo que tengo que tener en cuenta para más adelante: Folium arma el mapa como un objeto completo y luego se "inyecta" en la página, no es algo que Streamlit actualice solo en partes  o sea que hay que tener cuidado de que no se esté recargando todo el mapa de más cada vez que alguien interactúa con algo.

## Errores

Al ir probando el script por partes, quise confirmar qué tan cierto era eso de que "Folium solo no funciona en Streamlit" que había leído en la investigación. Así que desinstalé streamlit-folium a propósito y dejé solo streamlit, plotly, pandas y folium.

Error que me marcó:
<img width="1466" height="802" alt="ERROR " src="https://github.com/user-attachments/assets/88a03317-7da6-4822-9d5e-acc7d504cc20" />



**Causa:** streamlit-folium no es parte de Streamlit ni de Folium, es un paquete aparte que hay que instalar explícitamente (`pip install streamlit-folium`). Si no está instalado, ni siquiera truena al momento de dibujar el mapa truena desde el import, antes de correr cualquier otra línea del script.

**Solución:** reinstalar el paquete:
paso 1: en la terminal escribes pip install streamlit plotly pandas folium stramlit-foliun 
ya despues que se descarge todo como en la imagen haces el siguiente paso 
<img width="1470" height="756" alt="paso 1" src="https://github.com/user-attachments/assets/364b79db-7b47-43f0-b5b7-7023c057adfb" />
paso 2: ya que este descargado completamente abajo escribes 
streamlit run ejemplo_dashboard.py 
<img width="1470" height="92" alt="paso 2" src="https://github.com/user-attachments/assets/9243a850-0a97-4eea-9d55-c9815df82b3b" />
asi te saldra el Dashboard. en una ventana emergente 
<img width="1392" height="710" alt="PROTOTIPO 3" src="https://github.com/user-attachments/assets/3bfd98de-51fc-4744-a555-3fdc97f3e904" />
<img width="1482" height="667" alt="PROTOTIPO 2" src="https://github.com/user-attachments/assets/43ec966d-f109-4451-a341-b35cb70c19a7" />
<img width="1442" height="787" alt="PROTOTIPO 1" src="https://github.com/user-attachments/assets/dbceea44-f69e-4a60-bafe-addcfb0ffa8a" />

Esto confirma algo que había anotado en la sección de "Qué aprendí": Folium y streamlit-folium son dos librerías independientes, y ambas son obligatorias para que el mapa aparezca dentro de Streamlit  no es opcional ni redundante tenerlas por separado en el requirements.txt.

Los demás errores (de datos, de conexión a las APIs reales) los voy a ir documentando aquí conforme pasen en la siguiente etapa, cuando conecte con PostgreSQL y Catastro.

## Lo que sigue

* Conectar el script a la API real de PostgreSQL (cambiar los datos inventados por una petición con requests).
* Conectar la API de Catastro para traer coordenadas reales en vez de las que puse a mano.
* Meter más indicadores (confianza promedio, fuente de los datos) y agrupar puntos en el mapa si crecen mucho los datos.

