# Dashboard: Mapa Interactivo
 
Proyecto Integrador de Extracción de Datos Geográficos (Ensenada) · Módulo Dashboard
Materia: Patrones De Comportamiento De Datos · Grupo 371
 
## Contenido
 
1. [Descripción](#-descripción)
2. [Objetivos](#-objetivos)
3. [Tecnologías](#-tecnologías)
4. [Funcionalidades](#️-funcionalidades)
5. [Instalación y ejecución](#-instalación-y-ejecución)
6. [Variables de entorno](#-variables-de-entorno)
7. [Estructura y responsables](#-estructura-y-responsables)
8. [Documentación del proyecto](#-documentación-del-proyecto)
9. [Equipo](#-equipo)
10. [Estado y pendientes](#-estado-y-pendientes)
## Descripción
 
Componente de **mapa interactivo** del módulo Dashboard. Muestra los registros geográficos del sistema (calle, colonia, nivel de confianza y fuente del dato) sobre un mapa.
 
Permite filtrar por colonia, alternar entre cartografía y satélite, y agregar notas con un clic. Por ahora trabaja con datos simulados.
 
## Objetivos
 
**General:** construir el mapa interactivo del Dashboard, que muestre los datos geográficos del sistema de forma clara y navegable.
 
**Específicos:**
 
- Mostrar cada registro como un marcador con información emergente (calle, colonia, confianza, fuente).
- Filtrar los registros del mapa por colonia.
- Alternar entre vista de cartografía y vista satelital.
- Agregar notas sobre un punto del mapa con un clic.
- Dejar el componente listo para conectarse a datos reales.
## Tecnologías
 
- [ ] HTML5
- [ ] CSS3
- [ ] JavaScript
- [ ] React
- [ ] Node.js
- [x] Python
- [ ] Java
- [ ] MySQL
- [ ] MongoDB
- [x] Git / GitHub
- [x] Otra: Streamlit, Folium, streamlit-folium, pandas
| Librería | Uso en este componente |

`streamlit` Estructura y páginas de la aplicación web 
`folium`  Construcción del mapa interactivo (marcadores y capas) sobre OpenStreetMap 
`streamlit-folium`Muestra el mapa de Folium dentro de Streamlit y captura los clics del usuario 
`pandas`Manejo de los datos en tablas antes de dibujarlos en el mapa 
`openpyxl`Lectura de archivos `.xlsx` (versión conjunta con la carga de Excel) 
`requests`Consumo de una API real (solo si se desactiva la API simulada) 
 
## Funcionalidades
 
1. **Marcadores por registro:** color rojo si la confianza es menor a 0.7, verde si es mayor o igual.
2. **Popup informativo:** al hacer clic en un marcador se ven calle, colonia, confianza y fuente.
3. **Filtro por colonia:** selector en la barra lateral para ver una colonia o todas.
4. **Cartografía y satélite:** control en el mapa para cambiar de fondo (OpenStreetMap o Esri).
5. **Notas con un clic:** se escribe una calle y una nota sobre el punto elegido. Por ahora solo se guardan en memoria.
6. **Centrado automático:** el mapa se centra según los registros que se estén mostrando.
## Instalación y ejecución
 
Se usa un **entorno virtual (venv)** para que las librerías del proyecto no se mezclen con las de otros proyectos.
 
**Requisitos:** Python 3.11 o superior y Git.
 
**1. Clonar el repositorio y cambiar a la rama del Dashboard**
 
```bash
git clone https://github.com/JaazielArellano/proyectoTraficoEsenada.git
cd proyectoTraficoEsenada
git switch dashboard
```
 
**2. Crear el entorno virtual**
 
```bash
python -m venv .venv
```
 
**3. Activarlo**
 
| Sistema | Comando |
|---|---|
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| macOS / Linux | `source .venv/bin/activate` |
 
Si todo salió bien, aparece `(.venv)` al inicio de la línea de la terminal.
 
**4. Instalar las dependencias**
 
```bash
pip install -r requirements.txt
```
 
**5. Ejecutar la aplicación**
 
```bash
streamlit run ejemplo_dashboard.py
```
 
Se abre en el navegador (normalmente en `http://localhos4001t:`). La versión conjunta con la carga de Excel se ejecuta igual, cambiando el nombre del archivo por `ejemplo_dashboard_emilio_edgar.py`.
 
Para salir del entorno virtual: `deactivate`.
 
### Problemas comunes
 
| Mensaje | Causa y solución |
|---|---|
| `streamlit` no se reconoce como comando | El entorno virtual no está activo o faltan las dependencias. Activa el venv y repite el paso 4, o usa `python -m streamlit run ejemplo_dashboard.py`. |
| `ModuleNotFoundError: No module named 'streamlit_folium'` | Falta instalar las dependencias. Repite el paso 4. |
| PowerShell dice que la ejecución de scripts está deshabilitada | En esa misma ventana escribe `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` y vuelve a activar el venv. |
 
La carpeta `.venv` no se sube a GitHub porque está en el `.gitignore`.
 
## Variables de entorno
 
Solo la versión conjunta (`ejemplo_dashboard_emilio_edgar.py`) usa una variable de entorno, y únicamente cuando se conecta a una API real. Con la API simulada (el modo por defecto) no se necesita ninguna.
 
| Variable | Para qué sirve | Ejemplo | Obligatoria |
|---|---|---|---|
| `API_URL` | Dirección base de la API real; el código le agrega `/records` | `http://localhost:8000` | Solo si `USAR_API_SIMULADA = False` |
 
La URL del ejemplo es solo ilustrativa: hay que usar la de la API real.
 
**Cómo definirla** (antes de ejecutar `streamlit run`, en la misma terminal):
 
| Sistema | Comando |
|---|---|
| Windows (PowerShell) | `$env:API_URL = "http://localhost:8000"` |
| Windows (CMD) | `set API_URL=http://localhost:8000` |
| macOS / Linux | `export API_URL="http://localhost:8000"` |
 
La variable solo existe mientras esa ventana de terminal esté abierta, y el código la lee con `os.getenv("API_URL")`.
 
## Estructura y responsables
 
```
proyectoTraficoEsenada/        
README.md
requirements.txt
.gitignore
ejemplo_dashboard.py
ejemplo_dashboard_emilio_edgar.py
Avance.md
Avance_conjunto.md
DESIGN_DOC.md
Readme
Ashetemel
```
 
| Archivo | Qué es | Responsable |
|---|---|---|
| `README.md` | Documento central (este archivo) | Edgar |
| `requirements.txt` | Dependencias con versiones fijas | Edgar |
| `.gitignore` | Evita subir `.venv` y `.env` | Edgar |
| `ejemplo_dashboard.py` | Prototipo del mapa | Edgar |
| `ejemplo_dashboard_emilio_edgar.py` | Mapa + carga de Excel + API de prueba | Edgar y Emilio |
| `Avance.md` | Bitácora individual del mapa | Edgar |
| `Avance_conjunto.md` | Bitácora del trabajo conjunto | Edgar y Emilio |
| `DESIGN_DOC.md` | Diseño técnico del mapa | Edgar |
| `Readme` | Documentación del módulo de gráficas D3.js | Jesús |
| `Ashetemel` | Visualizaciones en HTML | Jesús |
 
Los archivos de Jesús aparecen con su nombre actual. Si los renombra, hay que actualizar esta tabla.
 
## Documentación del proyecto
 
- [Avance.md](Avance.md): investigación, pruebas, errores y aprendizajes del mapa.
- [Avance_conjunto.md](Avance_conjunto.md): integración del mapa con la carga de Excel y la API de prueba.
- [DESIGN_DOC.md](DESIGN_DOC.md): diseño técnico del mapa (objetivos, alcance, alternativas).
- [Readme](Readme): documentación del módulo de gráficas con D3.js.
## Equipo
 
| Integrante | GitHub | Parte |
|---|---|---|
| Edgar Eduardo Lopez Orozco | [@edgarlopez75-blip](https://github.com/edgarlopez75-blip) | Mapa interactivo |
| Jorge Emilio García Raygoza | @usuario-de-emilio | Carga y validación de Excel |
| Jesús Luna García | [@Jesusgg04](https://github.com/Jesusgg04) | Gráficas con D3.js |
 
## Estado y pendientes
 
**Estado:** prototipo funcional con datos simulados.
 
**Pendientes:**
 
- Consumir la API con los datos de prueba del equipo de base de datos.
- Obtener coordenadas y validar calles con la API de Catastro.
- Guardar las notas del mapa de forma permanente.
