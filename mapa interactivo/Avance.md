# Avance Mapa Interactivo
 
**Alumno:** Edgar Eduardo Lopez Orozco
**Periodo:** Semana 1 – Semana 2 (+ actualización de despliegue + cambio a la API del profe)
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
pip install streamlit pandas folium streamlit-folium requests
streamlit run ejemplo_dashboard.py
```
 
### Tercer script: API del profe (puerto 4003), noticias y selector de tablas
 
El profe me pidió usar otra API (`http://148.231.239.96:4003/docs`, llamada "API CRUD Dinámica PostgreSQL") en lugar de la del DENUE, así que **quité la API anterior del script** y dejé solo esta.
 
**Cómo funciona la API.** Es una API genérica: la tabla que se consulta se elige en la misma URL. En `/docs` (Swagger) tiene solo 4 endpoints:
 
| Método | Ruta | Para qué sirve |
|---|---|---|
| GET | `/api/datos/{nombre_tabla}` | Consultar una tabla (con paginación: `page` y `limit`) |
| POST | `/api/datos/{nombre_tabla}` | Insertar un registro |
| PUT | `/api/datos/{nombre_tabla}/{id_registro}` | Actualizar un registro |
| DELETE | `/api/datos/{nombre_tabla}/{id_registro}` | Eliminar un registro |
 
Yo solo uso el **GET**, porque el mapa únicamente necesita leer datos. Ningún endpoint lista las tablas que existen, así que hay que saber el nombre de antemano.
 
**Tablas que probé:**
 
| Tabla | Qué trae | Resultado |
|---|---|---|
| `prueba` | — | No existe (error 404) |
| `alexis_datos` | Noticias con las columnas `id`, `titulo`, `url`, `fecha_extraccion` (18 registros cuando la probé) | Funciona, pero **no trae coordenadas** |
| `cespe` | Enlaces a avisos de `cespe.gob.mx` (por ejemplo `.../avisos/corte-1001`) | Responde; al probarla, el título y la fecha salían vacíos porque el script todavía no conocía sus columnas (ver Error 11) |
 
**Qué le cambié al script para esta versión:**
 
1. **Lectura de la API sin atrapar errores dentro del caché.** La descarga vive en una función aparte (`descargar_datos(tabla)`), y el `try/except` está en otra función que la llama. Así, si la API falla, el fallo no se guarda en el caché (ver Error 10):
 
```python
BASE_URL = "http://148.231.239.96:4003/api/datos"
 
@st.cache_data(ttl=600)
def descargar_datos(tabla):
    resp = requests.get(f"{BASE_URL}/{tabla}", params={"page": 1, "limit": 100}, timeout=30)
    resp.raise_for_status()
    resp.encoding = "utf-8"    # evita caracteres raros (acentos, ñ)
    data = resp.json()
    registros = data.get("datos") if isinstance(data, dict) else data
    return pd.DataFrame(registros)
```
 
2. **Selector de tabla en la barra lateral.** Se puede cambiar entre `alexis_datos`, `cespe` o escribir el nombre de cualquier otra tabla, sin tocar el código. Cada tabla tiene su propio caché:
 
```python
TABLAS = {
    "Noticias (alexis_datos)": "alexis_datos",
    "CESPE": "cespe",
    "Otra tabla (escribir nombre)": None,
}
opcion_tabla = st.sidebar.selectbox("Tabla de la API", list(TABLAS))
```
 
3. **Detección flexible de columnas.** Un diccionario `ALIAS` lista varios nombres posibles para cada dato (título, fecha, enlace, latitud, longitud, colonia o lugar) y el script usa el primero que exista en la tabla. Si la tabla no tiene título pero sí enlace, usa el final del enlace como título (por ejemplo `corte-1001`).
 
4. **Ubicación de los registros en el mapa.** Como estas tablas no traen coordenadas (ver Error 9), el script hace dos cosas:
   * Si la tabla sí trae latitud y longitud, usa esas coordenadas directo.
   * Si no, busca en el título un lugar conocido (por ejemplo "Valle de Guadalupe" o "Maneadero") en un diccionario `LUGARES` con coordenadas **aproximadas** y pone un marcador **naranja**. Si varias noticias caen en el mismo lugar, se desplazan un poco para que no se encimen.
   * Los marcadores **azules** siguen siendo los que ubico yo con un clic.
 
```python
LUGARES = {
    "valle de guadalupe": (32.0800, -116.5800),
    "maneadero": (31.7300, -116.5600),
    "ensenada": (31.8667, -116.5964),
    # ...
}
```
 
5. **Ubicar una noticia con un clic.** Ahora, además de escribir la nota a mano, el formulario trae una lista para elegir cuál registro de la API se quiere ubicar en el punto donde se hizo clic. Al guardar, el marcador azul lleva el título y un enlace "Ver más".
 
6. **Buscador y tablas.** El buscador de la barra lateral filtra el mapa y la tabla a la vez, sin importar mayúsculas ni acentos (hay que presionar Enter). Debajo del mapa hay una tabla resumen (fecha, título, lugar detectado, enlace) y un expander con la tabla completa tal cual viene de la API, con todas sus columnas. Las celdas vacías se muestran como `—` en lugar de `None`.
 
7. **Botón "Recargar datos"** en la barra lateral, para volver a consultar la API sin reiniciar la app.
 
## Qué aprendí
 
Lo que más me costó entender al principio fue por qué el plan pedía `streamlit-folium` si ya tenía `folium`; pensé que era redundante. Ya investigando, entendí que Streamlit no sabe renderizar un objeto de Folium por sí solo, entonces sin ese paquete el mapa simplemente no aparece.
 
También aprendí que Folium arma el mapa como un objeto completo y luego se "inyecta" en la página, no es algo que Streamlit actualice solo en partes — o sea que hay que tener cuidado de que no se esté recargando todo el mapa de más cada vez que alguien interactúa con algo.
 
Con las mejoras nuevas aprendí que:
 
* Un mapa se arma con **capas de fondo** (tiles), y se pueden combinar varias para cambiar entre cartografía y satélite.
* El satélite se descarga por pedazos desde un servidor, por eso depende del internet.
* Un clic en el mapa solo da **coordenadas** (latitud y longitud), no el nombre de la calle. Por eso, por ahora, el nombre de la calle se escribe a mano.
* Streamlit vuelve a correr todo el script cada vez que el usuario interactúa, así que lo que se quiere conservar (como las notas) hay que guardarlo en `st.session_state`.
 
Con la API del profe y el selector de tablas aprendí que:
 
* Una API "genérica" como esta no sabe de antemano qué hay en cada tabla: el nombre y las columnas dependen de lo que se haya cargado en PostgreSQL, así que el código tiene que tolerar columnas distintas (por eso el diccionario `ALIAS`).
* En Swagger (`/docs`) hay que tener cuidado con qué endpoint se prueba: GET solo consulta, pero POST, PUT y DELETE **modifican la base de datos** del proyecto.
* `@st.cache_data` guarda lo que regresa la función **aunque sea un resultado vacío por un error**. Por eso conviene no atrapar el error dentro de la función cacheada.
* Que los datos no traigan coordenadas no los hace inútiles: se pueden ubicar de forma aproximada con el lugar que mencionan, siempre avisando que la ubicación es aproximada.
* Los acentos mal codificados (como `JU�REZ`) vienen de la codificación de caracteres, no de Streamlit ni de Folium.
 
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
 
### Error 5: caracteres raros en los nombres (`JU�REZ`)
 
En el filtro por colonia aparecían nombres como `BENITO JU�REZ`, con un signo de interrogación en lugar del acento.
 
**Causa:** problema de codificación de caracteres al leer el texto de la API.
 
**Solución:** forcé la lectura en UTF-8 (`resp.encoding = "utf-8"`) y agregué una función `arreglar_texto()` que corrige acentos mal codificados (por ejemplo `JuÃ¡rez` pasa a `Juárez`) y quita espacios sobrantes. También le puse formato de título (`BENITO JUÁREZ` se ve como `Benito Juárez`).
 
**Lección:** si el signo `�` ya viene guardado así en la base de datos, no se puede recuperar desde Python; habría que corregirlo donde se cargaron los datos originales (por ejemplo, abriendo el CSV con la codificación correcta).
 
### Error 6: conexión rechazada con la API del puerto 4003 (`WinError 10061`)
 
Al probar la API nueva desde mi máquina, la terminal mostró:
 
```
No se pudo conectar a la API, usando datos simulados: HTTPConnectionPool(host='148.231.239.96', port=4003):
Max retries exceeded ... [WinError 10061] No se puede establecer una conexión ya que el equipo de destino
denegó expresamente dicha conexión
```
 
**Causa:** no era un error del código: el servidor rechazó la conexión porque la API no estaba corriendo o no era accesible en ese momento.
 
**Solución:** esperar o avisar a quien la mantiene, y verificar abriendo `http://148.231.239.96:4003/docs` en el navegador. Mientras tanto, el respaldo con datos simulados evitó que el mapa quedara vacío.
 
### Error 7: `404 Not Found` por nombre de tabla incorrecto
 
```
404 Client Error: Not Found for url: http://148.231.239.96:4003/api/datos/datos?page=1&limit=100
```
 
**Causa:** la API sí respondió, pero había usado `datos` como nombre de tabla y esa tabla no existe (la ruta quedó `/api/datos/datos`). También probé `prueba`, que tampoco existe.
 
**Solución:** probar nombres directamente en `/docs`, con el endpoint **GET** y el botón "Try it out". El nombre que sí funcionó fue `alexis_datos`. Como la API no tiene un endpoint que liste las tablas, la forma segura de conocer el nombre es preguntarle al profe o revisar quién cargó los datos.
 
**Otro detalle:** en una de esas pruebas abrí por error el endpoint **POST** en lugar del GET. La API respondió con un error 500 (`can't adapt type 'dict'`) porque le mandé el cuerpo de ejemplo vacío, así que aparentemente no se insertó nada. Aun así, fue un recordatorio de no usar POST, PUT ni DELETE para consultar.
 
### Error 8: `Failed to fetch` en Swagger
 
Al volver a probar `alexis_datos` en `/docs`, Swagger mostró "Failed to fetch" (posibles causas: CORS, falla de red). No era que la tabla no existiera: la petición no llegó al servidor. Al repetirla unos minutos después, la API respondió con los datos.
 
**Lección:** la API del puerto 4003 es intermitente, así que un error de conexión no siempre significa que algo esté mal en el código o en el nombre de la tabla.
 
### Error 9: el mapa salía vacío con la tabla de noticias
 
Con `alexis_datos` la API cargaba bien las 18 noticias, pero el mapa no mostraba ningún marcador.
 
**Causa:** la tabla solo trae `id`, `titulo`, `url` y `fecha_extraccion`: **no tiene latitud ni longitud**. Mi código descartaba (`dropna`) las filas sin coordenadas, así que no quedaba nada que dibujar.
 
**Solución:** agregar la ubicación automática por lugar mencionado en el título (diccionario `LUGARES`, marcadores naranjas) y la opción de ubicar una noticia con un clic (marcadores azules). Las coordenadas del diccionario son aproximadas, y las noticias que no mencionan un lugar conocido solo aparecen en la tabla.
 
### Error 10: el aviso de "no se pudieron cargar" no desaparecía aunque la API ya respondía
 
**Causa:** `@st.cache_data(ttl=600)` guardaba por 10 minutos el resultado vacío que regresaba la función cuando la API fallaba. Aunque la API volviera, el script seguía usando ese resultado guardado.
 
**Solución:** separar la descarga (que no atrapa errores, para que un fallo no se guarde en el caché) de la función que sí maneja el error y muestra el aviso con el detalle. También agregué el botón "Recargar datos", que limpia el caché con `st.cache_data.clear()`.
 
### Error 11: la tabla `cespe` mostraba `None` en fecha, título y lugar
 
Al cambiar a la tabla `cespe`, la columna de enlaces sí traía datos, pero fecha, título y lugar salían como `None`.
 
**Causa:** no era un problema de la API: el script solo conocía las columnas de la tabla de noticias (`titulo`, `fecha_extraccion`) y esta tabla usa otros nombres.
 
**Solución:** la detección flexible de columnas (`ALIAS`), el título tomado del enlace cuando no hay uno, y el expander con la tabla completa para poder ver qué columnas trae cada tabla. Además, el script imprime `Columnas de la API: [...]` en la terminal.
 
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
 
**Conexión a la API real (DENUE) — versión anterior:** *(el profe pidió cambiar a otra API, así que esta función ya no está en el script actual; la versión nueva está en la sección "Tercer script")*. Esa versión del script intentaba jalar los datos desde una API propia del equipo (`http://148.231.239.96:4002/api/datos`, con los campos del DENUE normalizados a los nombres que usa el mapa: `street`, `neighborhood`, `lat`, `lon`). Si esa API no responde (por ejemplo, porque todavía no está corriendo, o tarda más de 30 segundos), el script cae automáticamente a los datos simulados (`MOCK_DATA`) como respaldo, para que el mapa nunca se quede sin mostrar nada:
 
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
 
## Revisión de calidad de código con pylint
 
Para cerrar esta etapa, corrí `pylint` sobre `ejemplo_dashboard.py` en el servidor del profe, para revisar el estilo y la calidad del código más allá de que simplemente "funcione":
 
```
pylint ejemplo_dashboard.py
```
 
**Primera corrida — calificación 7.37/10.** Pylint marcó estos puntos:
 
| Código | Línea(s) | Problema |
|---|---|---|
| C0301 | 115, 147 | Líneas demasiado largas (más de 100 caracteres) |
| C0304 | 179 | Faltaba un salto de línea en blanco al final del archivo |
| C0116 | 56 | La función `cargar_datos()` no tenía docstring |
| W0718 | 70 | `except Exception` demasiado general (atrapa cualquier error, no solo los de red/API) |
| E1137 | 67, 68 | `'d' does not support item assignment` al asignar `d["confidence"]` y `d["source"]` |
 
**Cómo corregí cada uno:**
 
* **Líneas largas (C0301):** corté la URL del satélite de Esri en una constante aparte (`ESRI_SATELITE_URL`) repartida en varias líneas, y partí el `popup_html` en líneas más cortas.
* **Falta de salto de línea final (C0304):** se agregó la línea en blanco al final del archivo.
* **Falta de docstring (C0116):** se agregó una línea descriptiva justo debajo de `def cargar_datos():` explicando qué hace la función.
* **`except` demasiado general (W0718):** se cambió `except Exception as e:` por `except requests.exceptions.RequestException as e:`, para que solo se atrapen errores relacionados con la conexión a la API (y no se oculten errores de programación por accidente).
* **`E1137` en `d["confidence"]` / `d["source"]` (falso positivo):** investigué este error porque el código sí funcionaba bien en el navegador (ya lo había probado). Resulta que es un problema conocido de pylint con pandas: después de un `.rename()`, pylint a veces "pierde de vista" que la variable sigue siendo un `DataFrame` y cree que no admite asignación por índice. Como no es un bug real, lo documenté con un comentario `# pylint: disable=unsupported-assignment-operation` alrededor de esas dos líneas, en vez de cambiar la lógica que ya funcionaba.
**Segunda corrida, después de corregir:** se volvió a ejecutar `pylint ejemplo_dashboard.py` para confirmar que los puntos anteriores ya no aparecieran y que la calificación subiera respecto al 7.37/10 inicial. El archivo corregido ya se subió al servidor (vía `scp`) y quedó corriendo de nuevo con `nohup` en el puerto 4001.
 
**Lección:** pylint no solo encuentra errores que rompen el programa (como el `ModuleNotFoundError` de antes), también señala buenas prácticas (nombres, longitud de línea, documentación, manejo de excepciones) que ayudan a que el código sea más fácil de leer y mantener por el resto del equipo, aunque "ya funcione". También aprendí que no toda alerta de pylint es un error real — hay que entender qué está señalando antes de cambiar código que ya sabes que funciona.
 
**Nota:** esta revisión de pylint se hizo sobre la versión del script con la API del DENUE. Como después se reescribió el script (API del puerto 4003, selector de tablas, ubicación de noticias), falta volver a correr `pylint` sobre la versión nueva.
 
## Lo que sigue
 
* Confirmar con el profe que la API del puerto 4003 quede corriendo de forma estable (se cayó o no respondió varias veces durante las pruebas) y qué tablas voy a usar.
* Revisar las columnas reales de la tabla `cespe` y de las demás tablas que se vayan a mostrar, y agregarlas al diccionario `ALIAS` si hace falta.
* Conseguir una tabla con coordenadas reales (por ejemplo, de la API de Catastro) para dejar de depender de las ubicaciones aproximadas del diccionario `LUGARES`, y completar ese diccionario con los lugares que falten.
* Guardar las notas que se agregan con un clic en la base de datos (usando el POST de la API, en una tabla que el profe designe para eso), para que no se pierdan al cerrar la app.
* Subir la versión nueva del script al servidor con `scp` y reiniciarla con `nohup` en el puerto 4001.
* Volver a correr `pylint` sobre la versión nueva y corregir lo que marque.
* Obtener el nombre de la calle automáticamente a partir del punto donde se hace clic, en lugar de escribirlo a mano.
* Agrupar puntos en el mapa (`MarkerCluster`) si crecen mucho los datos, y agregar rutas (`PolyLine`) si se llega a necesitar.
* Acordar con el equipo una forma de evitar pisarnos el trabajo en el servidor compartido (por ejemplo, cada quien con su propia rama y avisando antes de hacer cambios grandes).
