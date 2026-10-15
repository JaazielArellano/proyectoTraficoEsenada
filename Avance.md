# Avance Mapa Interactivo
 
**Alumno:** Edgar Eduardo Lopez Orozco
**Periodo:** Semana 1 – Semana 2 (+ actualización de despliegue)
**Lo que me tocó:** Dentro del módulo Dashboard, el mapa interactivo (según el Plan de Trabajo, esto cae en la Semana 2 del cronograma).
 
---
 
## Qué hice, estudié esta semana y media
 
Primero me puse a leer bien para ubicar exactamente qué me tocaba a mí dentro del Dashboard. Mis compañeros (Jesus y Emilio) están viendo login, roles y el CRUD, y a mí me quedó el mapa.
 
También repasé el contrato JSON que pusimos de ejemplo con el resto del equipo (los campos que va a mandar la API de PostgreSQL: `date`, `day`, `street`, `neighborhood`, `confidence`, `source`, `created_at`, `created_by`), porque necesitaba saber con qué estructura de datos voy a trabajar antes de ponerme a programar cualquier cosa.
 
Ya con eso claro, me metí a investigar las librerías que necesito para esta parte:
 
* **Folium:** para el mapa. Usa OpenStreetMap como base, que es gratis y no pide API key (a diferencia de Google Maps), y deja poner marcadores, rutas y agrupar puntos.
* **streamlit-folium:** esta la tuve que investigar más porque no sabía para qué era exactamente. Resulta que Streamlit no puede mostrar un mapa de Folium por sí solo — necesita este "puente" para renderizarlo y además para poder capturar si el usuario le da clic a algo del mapa.
* **pandas:** para acomodar los datos que lleguen en JSON antes de mandárselos a Folium.
Después de tener el mapa básico, investigué cómo agregarle dos cosas más:
 
* **Cambiar entre cartografía y satélite:** Folium permite agregar varios "fondos" de mapa con `folium.TileLayer` y un botón para cambiar entre ellos con `folium.LayerControl`. Para el satélite usé las imágenes de Esri, que se pueden usar sin API key.
* **Agregar una noticia o dato con un clic en el mapa:** `streamlit-folium` devuelve el último punto donde el usuario hizo clic (`last_clicked`, con latitud y longitud), y con eso se puede guardar una nota en ese lugar.
## Acuerdos con el equipo
 
Quedamos en no cambiar las librerías que ya estaban en el plan (aunque existen otras opciones como Google Maps), porque Folium + OpenStreetMap no necesita pagar nada. También quedó claro que yo no toco la base de datos directo — todo lo que muestre en el mapa viene de la API, nunca conecto a PostgreSQL por mi cuenta.
 
Otra cosa que se aclaró: el mapa necesita coordenadas (lat y lon), y esas **no** vienen en el contrato base del Dashboard — hay que pedirlas a la API de Catastro. Mientras esa parte no esté lista, voy a trabajar con coordenadas simuladas.
 
## Pruebas de código
 
Esta primera etapa la usé sobre todo para investigar, así que no traía código todavía. Para este reporte sí armé un primer script de prueba (`ejemplo_dashboard.py`, está en esta misma carpeta) nada más para comprobar que el mapa funciona como esperaba. Después le agregué las mejoras nuevas en una segunda versión del mismo archivo.
 
### Primer script (`ejemplo_dashboard.py`)
 
* Inventé unos datos de ejemplo con la misma estructura del contrato JSON (le agregué lat/lon a mano porque en el futuro esos datos van a venir de Catastro).
* Con Folium + streamlit-folium hice el mapa, con un marcador por cada registro y un popup que muestra la calle, la colonia y el nivel de confianza.
* Agregué un filtro por colonia en la barra lateral, para ver que sí se actualiza el mapa al cambiarlo.
**Cómo funciona el filtro por colonia.** La parte clave se puede leer en dos pasos:
 
```python
# 1. Reviso fila por fila: ¿la colonia es la que eligió el usuario? (Sí/No)
es_la_colonia_elegida = df["neighborhood"] == colonia_seleccionada
 
# 2. Me quedo solo con las filas que dijeron "Sí"
df_filtrado = df[es_la_colonia_elegida]
```
 
Es parecido a un filtro de Excel: primero se marca qué filas cumplen la condición, y luego se descartan las demás. Por ejemplo, si el usuario elige "Playitas", solo se quedan los registros 3 y 4, y esos son los que se dibujan en el mapa.
 
### Segundo script: cartografía/satélite y notas con clic
 
**1. Cambiar entre cartografía y satélite**
 
Antes el mapa usaba un solo fondo (`tiles="OpenStreetMap"`). Ahora el mapa se crea con `tiles=None` (sin fondo) y se le agregan dos fondos:
 
```python
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
```
 
La línea del satélite es la dirección del servidor de Esri que entrega las imágenes. El mapa está cortado en cuadritos (como un mosaico) y Folium solo pide los que se ven en pantalla:
 
* `{z}` es el nivel de zoom.
* `{x}` y `{y}` son la columna y la fila del cuadrito.
Estos tres valores no se cambian a mano, Folium los llena solo cada vez que se mueve o se acerca el mapa. Por eso se necesita internet para ver el satélite: las imágenes se descargan del servidor de Esri.
 
**2. Agregar una noticia o dato con un clic en el mapa**
 
* Se guarda una lista de notas en `st.session_state.notas`. Se usa `session_state` para que las notas no se borren cada vez que se hace clic en algo.
* Con `st_folium` se dibuja el mapa y se guarda lo que hizo el usuario en la variable `resultado`.
* Si el usuario hizo clic, `resultado.get("last_clicked")` trae la latitud y longitud del punto.
* Se muestran dos cajas (nombre de la calle y noticia o dato) y un botón "Guardar nota".
* Al guardar, la nota se agrega a la lista junto con el punto del clic, y `st.rerun()` vuelve a dibujar el mapa para que aparezca un marcador azul en ese lugar.
```python
resultado = st_folium(mapa, width=None, height=550, returned_objects=["last_clicked"])
 
clic = resultado.get("last_clicked")
 
if clic:
    st.write(f"Punto seleccionado: {clic['lat']:.5f}, {clic['lng']:.5f}")
 
    calle = st.text_input("Nombre de la calle")
    texto = st.text_area("Noticia o dato")
 
    if st.button("Guardar nota"):
        st.session_state.notas.append({
            "calle": calle,
            "texto": texto,
            "lat": clic["lat"],
            "lon": clic["lng"],
        })
        st.rerun()
else:
    st.info("Haz clic en un punto del mapa para agregar una noticia o dato.")
```
 
Por ahora las notas solo viven en la memoria de la app, así que se pierden al cerrarla. Eso lo voy a resolver cuando conecte con la API.
 
Para correrlo:
 
```
pip install streamlit pandas folium streamlit-folium
streamlit run ejemplo_dashboard.py
```
 
## Qué aprendí
 
Lo que más me costó entender al principio fue por qué el plan pedía `streamlit-folium` si ya tenía `folium`; pensé que era redundante. Ya investigando, entendí que Streamlit no sabe renderizar un objeto de Folium por sí solo, entonces sin ese paquete el mapa simplemente no aparece.
 
También aprendí que Folium arma el mapa como un objeto completo y luego se "inyecta" en la página, no es algo que Streamlit actualice solo en partes — o sea que hay que tener cuidado de que no se esté recargando todo el mapa de más cada vez que alguien interactúa con algo.
 
Con las mejoras nuevas aprendí que:
 
* Un mapa se arma con **capas de fondo** (tiles), y se pueden combinar varias para cambiar entre cartografía y satélite.
* El satélite se descarga por pedazos desde un servidor, por eso depende del internet.
* Un clic en el mapa solo da **coordenadas** (latitud y longitud), no el nombre de la calle. Por eso, por ahora, el nombre de la calle se escribe a mano.
* Streamlit vuelve a correr todo el script cada vez que el usuario interactúa, así que lo que se quiere conservar (como las notas) hay que guardarlo en `st.session_state`.
## Errores
 
### Error 1: `ModuleNotFoundError` con `streamlit_folium`
 
Al ir probando el script por partes, quise confirmar qué tan cierto era eso de que "Folium solo no funciona en Streamlit" que había leído en la investigación. Así que desinstalé `streamlit-folium` a propósito y dejé solo `streamlit`, `pandas` y `folium`, y traté de importar el módulo:
 
```python
import streamlit as st
from streamlit_folium import st_folium
```
 
Error que me marcó:
 
```
Traceback (most recent call last):
  File "<string>", line 3, in <module>
ModuleNotFoundError: No module named 'streamlit_folium'
```
 
**Causa:** `streamlit-folium` no es parte de Streamlit ni de Folium, es un paquete aparte que hay que instalar explícitamente (`pip install streamlit-folium`). Si no está instalado, ni siquiera truena al momento de dibujar el mapa — truena desde el `import`, antes de correr cualquier otra línea del script.
 
**Solución:** reinstalar el paquete:
 
```
pip install streamlit-folium
```
 
Después de esto el `import` y el resto del script volvieron a correr sin problema.
 
Esto confirma que Folium y streamlit-folium son dos librerías independientes, y ambas son obligatorias para que el mapa aparezca dentro de Streamlit — no es opcional ni redundante tenerlas por separado en el `requirements.txt`.
 
### Error 2: `streamlit` no se reconoce como comando
 
Al intentar correr el script en la terminal de PowerShell (con el entorno virtual `.venv-1` activado), me salió esto:
 
```
streamlit : El término 'streamlit' no se reconoce como nombre de un cmdlet, función, archivo de script o programa ejecutable.
+ CategoryInfo          : ObjectNotFound: (streamlit:String) [], CommandNotFoundException
+ FullyQualifiedErrorId : CommandNotFoundException
```
 
**Causa:** Streamlit no estaba instalado dentro del entorno virtual que tenía activo, por eso PowerShell no encontraba el comando.
 
**Solución:** instalar las librerías dentro del entorno activo y volver a correr el script:
 
```
pip install streamlit pandas folium streamlit-folium
streamlit run ejemplo_dashboard.py
```
 
Si el comando `streamlit` sigue sin reconocerse, también se puede correr como módulo de Python:
 
```
python -m streamlit run ejemplo_dashboard.py
```
 
**Lección:** conviene revisar siempre que las librerías estén instaladas en el mismo entorno virtual donde se va a correr el script.
 
### Error 3: permisos en el servidor del profe (sin `sudo`, sin `venv`)
 
Al pasar el prototipo del servidor del profe (Ubuntu 24.04, conexión por SSH con el usuario `septimo`), me encontré con que el usuario no tiene permisos de administrador:
 
```
sudo apt install python3.12-venv
[sudo] password for septimo:
septimo is not in the sudoers file.
```
 
**Causa:** sin `sudo` no se puede instalar el paquete `python3-venv`, necesario para crear un entorno virtual. Y sin entorno virtual, `pip install` normal tampoco funciona porque Ubuntu 24 protege el Python del sistema:
 
```
error: externally-managed-environment
```
 
**Solución:** instalar las librerías directo con la bandera que evita ese bloqueo (riesgo bajo porque es un servidor de pruebas compartido solo por el equipo):
 
```
pip install --break-system-packages streamlit pandas folium streamlit-folium
```
 
**Lección:** no siempre se tiene control total del servidor donde se despliega; hay que saber adaptarse a las restricciones que ya vienen configuradas (sin sudo, puertos limitados, etc.) en vez de asumir que se puede instalar/configurar todo como en una máquina propia.
 
### Error 4: archivo perdido por cambio de rama de otro integrante
 
Al volver a entrar al servidor unos días después para reiniciar el dashboard, el archivo `ejemplo_dashboard.py` (y `README.md`, `Avance.md`) ya no estaban en la carpeta `dashboard/`. Con `git status` encontré que la rama local tenía commits distintos a los del repositorio remoto, señal de que otro compañero del equipo usó la misma cuenta del servidor y movió/borró archivos sin que yo me diera cuenta (el servidor y el usuario SSH son compartidos por todo el equipo).
 
**Solución:** sin tocar los cambios pendientes de nadie más, usé el historial de Git para recuperar solo el archivo que necesitaba, buscando en qué commit existía todavía:
 
```
git log --all --oneline -- dashboard/ejemplo_dashboard.py
git show 6d5043a:dashboard/ejemplo_dashboard.py > ejemplo_dashboard.py
```
 
**Lección:** cuando se comparte un mismo usuario de servidor entre varios integrantes, conviene tener más cuidado con las ramas de Git y, si es posible, que cada quien trabaje desde su propia copia o avise antes de cambiar de rama.
 
## Despliegue en el servidor del profe (nuevo)
 
Después del prototipo local, probamos el dashboard en el servidor que el profe preparó para el grupo, para dejarlo accesible por IP y que cualquiera del equipo (o el profe) lo pueda revisar sin tener que correrlo en su propia máquina.
 
**Lo que se hizo:**
 
* Clonación del repo completo (`proyectoTraficoEsenada`) en el servidor vía `git clone` por SSH.
* Instalación de dependencias con `pip install --break-system-packages ...` (ver Error 3).
* El profe indicó que el rango de puertos permitido es **4000 en adelante** (el puerto por defecto de Streamlit, 8501, está bloqueado por el firewall del servidor). Me asignaron el **puerto 4001**.
* Para que el dashboard siga corriendo aunque se cierre la sesión SSH, se usa `nohup` en lugar de `streamlit run` normal:
```
nohup ~/.local/bin/streamlit run ejemplo_dashboard.py --server.address 0.0.0.0 --server.port 4001 > output.log 2>&1 &
```
 
  * `nohup` evita que el proceso se corte al desconectarse.
  * `> output.log 2>&1` guarda toda la salida (y errores) en un archivo, útil para revisar fallas sin tener la terminal abierta.
  * `&` al final corre el proceso en segundo plano.
* El dashboard quedó accesible públicamente en: `http://148.231.239.96:4001`
* Para actualizar el script en el servidor cuando hago cambios en mi máquina, lo subo con `scp` (sin necesidad de hacer `git pull`, ya que la carpeta del servidor tiene commits divergentes por el Error 4):
```
scp ejemplo_dashboard.py septimo@148.231.239.96:/home/septimo/proyectoTraficoEsenada/dashboard/ejemplo_dashboard.py
```
 
**Conexión a la API real (DENUE):** la versión actual del script ya intenta jalar los datos desde una API propia del equipo (`http://148.231.239.96:4002/api/datos`, con los campos del DENUE normalizados a los nombres que usa el mapa: `street`, `neighborhood`, `lat`, `lon`). Si esa API no responde (por ejemplo, porque todavía no está corriendo, o tarda más de 30 segundos), el script cae automáticamente a los datos simulados (`MOCK_DATA`) como respaldo, para que el mapa nunca se quede sin mostrar nada:
 
```python
@st.cache_data(ttl=600)
def cargar_datos():
    try:
        _resp = requests.get(API_URL, params={"page": 1, "limit": 100}, timeout=30)
        _resp.raise_for_status()
        d = pd.DataFrame(_resp.json()["datos"])
        d = d.rename(columns={
            "nom_vial": "street",
            "nomb_asent": "neighborhood",
            "latitud": "lat",
            "longitud": "lon",
        })
        d["confidence"] = 1.0
        d["source"] = "API DENUE"
        return d.dropna(subset=["lat", "lon"])
    except Exception as e:
        print("No se pudo conectar a la API, usando datos simulados:", e)
        return pd.DataFrame(MOCK_DATA)
```
 
`@st.cache_data(ttl=600)` evita pedir los datos a la API cada vez que alguien interactúa con el mapa (como el filtro de colonia o un clic) — los guarda en caché por 10 minutos.
 
## Lo que sigue
 
* Confirmar que la API del DENUE (puerto 4002) quede corriendo de forma estable para dejar de depender de los datos simulados.
* Conectar la API de Catastro para traer coordenadas reales en vez de las que puse a mano.
* Guardar las notas que se agregan con un clic en la base de datos (a través de la API), para que no se pierdan al cerrar la app.
* Obtener el nombre de la calle automáticamente a partir del punto donde se hace clic, en lugar de escribirlo a mano.
* Agrupar puntos en el mapa (`MarkerCluster`) si crecen mucho los datos, y agregar rutas (`PolyLine`) si se llega a necesitar.
* Acordar con el equipo una forma de evitar pisarnos el trabajo en el servidor compartido (por ejemplo, cada quien con su propia rama y avisando antes de hacer cambios grandes).
 
