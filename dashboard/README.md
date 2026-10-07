README - Dashboard: Mapa Interactivo (Proyecto Integrador de Extracción de Datos Geográficos)
Descripción del Proyecto
Este componente forma parte del módulo Dashboard del Proyecto Integrador de Extracción de Datos Geográficos de Ensenada. Específicamente, es la parte del mapa interactivo, que muestra sobre un mapa los registros geográficos recolectados por el sistema (calle, colonia, nivel de confianza, fuente del dato), con capas de cartografía y satélite, filtro por colonia, y la posibilidad de agregar notas haciendo clic en el mapa. Elegí trabajar en esta parte porque me interesa la visualización de datos geográficos y es la tarea que me fue asignada dentro del equipo.
Objetivos
* Objetivo general: Construir el componente de mapa interactivo del Dashboard, que consuma los datos geográficos del sistema y los muestre de forma clara y navegable para el usuario.
* Objetivos específicos:
   * Representar cada registro geográfico como un marcador en un mapa interactivo, con información emergente (calle, colonia, confianza, fuente).
   * Permitir filtrar los registros mostrados en el mapa por colonia.
   * Permitir alternar entre vista de cartografía (calles) y vista satelital.
   * Permitir agregar notas sobre un punto del mapa con un clic.
   * Dejar el componente listo para conectarse a los datos reales del sistema (actualmente usa datos simulados).
Tecnologías Utilizadas
* HTML5
* CSS3
* JavaScript
* React
* Node.js
* Python
* Java
* MySQL
* MongoDB
* Git / GitHub
* Otra: Streamlit, Folium, streamlit-folium, pandas (ver detalle abajo)


Librería
	Uso en este componente
	folium
	Construcción del mapa interactivo (marcadores, capas de cartografía/satélite) sobre OpenStreetMap
	streamlit-folium
	Puente para renderizar el mapa de folium dentro de Streamlit y capturar interacción del usuario (clics, etc.)
	pandas
	Estructura intermedia entre los datos (en formato JSON) y lo que se dibuja en el mapa
	OpenStreetMap
	Proveedor de mosaicos (tiles) del mapa base, gratuito y sin necesidad de API key
	Funcionalidades Principales
1. Visualización de registros en el mapa: cada registro geográfico se muestra como un marcador, con color distinto según su nivel de confianza (rojo si es menor a 0.7, verde si es mayor o igual).
2. Información emergente (popup): al hacer clic en un marcador se muestra la calle, colonia, confianza y fuente del dato.
3. Filtro por colonia: un selector en la barra lateral permite mostrar solo los registros de una colonia específica, o todos.
4. Cambio de vista cartografía/satélite: un control en el mapa permite alternar entre el fondo de calles (OpenStreetMap) y el fondo satelital (Esri).
5. Notas con un clic: al hacer clic en cualquier punto del mapa, se puede escribir una calle y una nota, y se guarda como un nuevo marcador (por ahora solo en memoria, mientras la app está abierta).
6. Centrado automático del mapa: el mapa se centra según el promedio de coordenadas de los registros que se estén mostrando en ese momento.
Instalación y cómo ejecutarlo
Necesitas:


* Python 3.11 o superior


Instalar las dependencias:


pip install streamlit pandas folium streamlit-folium

Ejecutar:


streamlit run ejemplo_dashboard.py

Esto abre automáticamente la app en tu navegador (normalmente en http://localhost:8501), donde puedes ver el mapa, filtrar por colonia, cambiar entre cartografía/satélite, y agregar notas con un clic.
Estructura del Proyecto
proyectoTraficoEsenada/
└── dashboard/                 ← este componente
    ├── README.md               ← este archivo
    ├── Avance.md                ← bitácora de avance semanal
    ├── DESIGN_DOC.md            ← documento de diseño técnico (Goals/Non-Goals/Background)
    └── ejemplo_dashboard.py     ← script de ejemplo funcional del mapa (prototipo)

Nota: esta es la estructura de mi componente individual. El resto de las carpetas del repositorio corresponden a los módulos de mis compañeros de equipo.
Estado actual
En investigación / prototipo inicial. Aún no está conectado a los datos reales del sistema (se está trabajando con datos simulados que respetan el contrato JSON acordado).