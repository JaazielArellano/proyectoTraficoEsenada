Dashboard: Mapa Interactivo
Proyecto Integrador de Extracción de Datos Geográficos (Ensenada) · Módulo Dashboard
Materia: Patrones De Comportamiento De Datos · Grupo 371
Contenido
Descripción
Objetivos
Tecnologías
Funcionalidades
Instalación y ejecución
Variables de entorno
Estructura y responsables
Documentación del proyecto
Equipo
Estado y pendientes
Descripción
Componente de mapa interactivo del módulo Dashboard. Muestra los registros geográficos del sistema (calle, colonia, nivel de confianza y fuente del dato) sobre un mapa.
Permite filtrar por colonia, alternar entre cartografía y satélite, y agregar notas con un clic. Por ahora trabaja con datos simulados.
Objetivos
General: construir el mapa interactivo del Dashboard, que muestre los datos geográficos del sistema de forma clara y navegable.
Específicos:
Mostrar cada registro como un marcador con información emergente (calle, colonia, confianza, fuente).
Filtrar los registros del mapa por colonia.
Alternar entre vista de cartografía y vista satelital.
Agregar notas sobre un punto del mapa con un clic.
Dejar el componente listo para conectarse a datos reales.
Tecnologías
\[ ] HTML5
\[ ] CSS3
\[ ] JavaScript
\[ ] React
\[ ] Node.js
\[x] Python
\[ ] Java
\[ ] MySQL
\[ ] MongoDB
\[x] Git / GitHub
\[x] Otra: Streamlit, Folium, streamlit-folium, pandas
Librería	Uso en este componente
`streamlit`	Estructura y páginas de la aplicación web
`folium`	Construcción del mapa interactivo (marcadores y capas) sobre OpenStreetMap
`streamlit-folium`	Muestra el mapa de Folium dentro de Streamlit y captura los clics del usuario
`pandas`	Manejo de los datos en tablas antes de dibujarlos en el mapa
`openpyxl`	Lectura de archivos `.xlsx` (versión conjunta con la carga de Excel)
`requests`	Consumo de una API real (solo si se desactiva la API simulada)
Funcionalidades
Marcadores por registro: color rojo si la confianza es menor a 0.7, verde si es mayor o igual.
Popup informativo: al hacer clic en un marcador se ven calle, colonia, confianza y fuente.
Filtro por colonia: selector en la barra lateral para ver una colonia o todas.
Cartografía y satélite: control en el mapa para cambiar de fondo (OpenStreetMap o Esri).
Notas con un clic: se escribe una calle y una nota sobre el punto elegido. Por ahora solo se guardan en memoria.
Centrado automático: el mapa se centra según los registros que se estén mostrando.
Instalación y ejecución
Se usa un entorno virtual (venv) para que las librerías del proyecto no se mezclen con las de otros proyectos.
Requisitos: Python 3.11 o superior y Git.

1. Clonar el repositorio y cambiar a la rama del Dashboard

```bash
git clone https://github.com/JaazielArellano/proyectoTraficoEsenada.git
cd proyectoTraficoEsenada
git switch dashboard
```

2. Crear el entorno virtual

```bash
python -m venv .venv
```

3. Activarlo
Sistema	Comando
Windows (PowerShell)	`.venv\\Scripts\\Activate.ps1`
macOS / Linux	`source .venv/bin/activate`
Si todo salió bien, aparece `(.venv)` al inicio de la línea de la terminal.
4. Instalar las dependencias

```bash
pip install -r requirements.txt
```

5. Ejecutar la aplicación

```bash
streamlit run ejemplo\_dashboard.py
```

Se abre en el navegador (normalmente en `http://localhost:8501`). La versión conjunta con la carga de Excel se ejecuta igual, cambiando el nombre del archivo por `ejemplo\_dashboard\_emilio\_edgar.py`.
Para salir del entorno virtual: `deactivate`.
Problemas comunes
Mensaje	Causa y solución
`streamlit` no se reconoce como comando	El entorno virtual no está activo o faltan las dependencias. Activa el venv y repite el paso 4, o usa `python -m streamlit run ejemplo\_dashboard.py`.
`ModuleNotFoundError: No module named 'streamlit\_folium'`	Falta instalar las dependencias. Repite el paso 4.
PowerShell dice que la ejecución de scripts está deshabilitada	En esa misma ventana escribe `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` y vuelve a activar el venv.
La carpeta `.venv` no se sube a GitHub porque está en el `.gitignore`.
Variables de entorno
Solo la versión conjunta (`ejemplo\_dashboard\_emilio\_edgar.py`) usa una variable de entorno, y únicamente cuando se conecta a una API real. Con la API simulada (el modo por defecto) no se necesita ninguna.
Variable	Para qué sirve	Ejemplo	Obligatoria
`API\_URL`	Dirección base de la API real; el código le agrega `/records`	`http://localhost:8000`	Solo si `USAR\_API\_SIMULADA = False`
La URL del ejemplo es solo ilustrativa: hay que usar la de la API real.
Cómo definirla (antes de ejecutar `streamlit run`, en la misma terminal):
Sistema	Comando
Windows (PowerShell)	`$env:API\_URL = "http://localhost:8000"`
Windows (CMD)	`set API\_URL=http://localhost:8000`
macOS / Linux	`export API\_URL="http://localhost:8000"`
La variable solo existe mientras esa ventana de terminal esté abierta, y el código la lee con `os.getenv("API\_URL")`.


Archivo	Qué es	Responsable
`README.md`	Documento central (este archivo)	Edgar
`requirements.txt`	Dependencias con versiones fijas	Edgar
`.gitignore`	Evita subir `.venv` y `.env`	Edgar
`ejemplo\_dashboard.py`	Prototipo del mapa	Edgar
`ejemplo\_dashboard\_emilio\_edgar.py`	Mapa + carga de Excel + API de prueba	Edgar y Emilio
`Avance.md`	Bitácora individual del mapa	Edgar
`Avance\_conjunto.md`	Bitácora del trabajo conjunto	Edgar y Emilio
`DESIGN\_DOC.md`	Diseño técnico del mapa	Edgar
`Readme`	Documentación del módulo de gráficas D3.js	Jesús
`Ashetemel`	Visualizaciones en HTML	Jesús
Los archivos de Jesús aparecen con su nombre actual. Si los renombra, hay que actualizar esta tabla.
Documentación del proyecto
Avance.md: investigación, pruebas, errores y aprendizajes del mapa.
Avance\_conjunto.md: integración del mapa con la carga de Excel y la API de prueba.
DESIGN\_DOC.md: diseño técnico del mapa (objetivos, alcance, alternativas).
Readme: documentación del módulo de gráficas con D3.js.
Equipo
Integrante	GitHub	Parte
Edgar Eduardo Lopez Orozco	@edgarlopez75-blip	Mapa interactivo
Jorge Emilio García Raygoza	@usuario-de-emilio	Carga y validación de Excel
Jesús Luna García	@Jesusgg04	Gráficas con D3.js
Estado y pendientes
Estado: prototipo funcional con datos simulados.
Pendientes:
Consumir la API con los datos de prueba del equipo de base de datos.
Obtener coordenadas y validar calles con la API de Catastro.
Guardar las notas del mapa de forma permanente.

