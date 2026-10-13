Extractor de noticias de X (Twitter)
Link: https://github.com/JaazielArellano/proyectoTraficoEsenada/tree/extractor/X_extractor
Autor: Arturo Muñiz Tavarez 
Status:Readme corregido para proxima revision 
Ultima actualizacion: 12/10/26

Archivos utilizados en el proyecto: 

- extractorx.py: detecta nombres de calles, avenidas, colonias, fraccionamientos, dias, meses y los genera en formato JSON.

- extractorx_tcapi: extrae los enlaces de las noticias de X los almacena y los envia al API, dejando los 
enlaces antiguos en un historial. 

- main.py: codigo principal que ejecuta todos los codigos. 

Contenido
- Goals
- Non-Goals
- Background
- Overview
- Tecnologias utilizadas
- Librerias requeridas
- Detailed Design
  - Solucion 1
    - Extracción (Scraper)
    - Persistencia (Historial JSON)
    - Envio (API POST)
- Consideraciones
- Métricas

Links
- Fuente de noticias: https://x.com/EnsenadaNews
- API destino: https://relax-albatross-pessimism.ngrok-free.dev/urls

Objetivo
Desarrollar un codigo en Python que extraiga de forma automatizada enlaces de publicaciones recientes desde la cuenta de X @EnsenadaNews, filtre duplicados mediante un historial local y envíe solo los enlaces nuevos a un API.

Goals
- Extraer automáticamente enlaces de tweets desde la fuente web sin dependencias dificiles.
- Filtrar los enlaces mediante un archivo local (`links_extraidos.json`) para no reenviar duplicados a la API.
- Enviar solo los links nuevos mediante solicitudes HTTP POST en formato JSON.

Non-Goals
- Sincronización en tiempo real.
- Procesar o analizar el texto/contenido de los tweets.
- Crear una interfaz gráfica (UI); el programa opera 100% por consola.

Background
Se requiere un sistema capaz de monitorear y recolectar las noticias publicadas por @EnsenadaNews para alimentar la API de un colaborador. Para lograrlo de manera mas facil y sin pagar servicios, se implementó un scraper liviano mediante peticiones HTTP.

Overview
El script realiza un ciclo de trabajo secuencial dividido en tres etapas:
1. Consulta el HTML público de la cuenta objetivo en X.
2. Compara los identificadores encontrados contra el registro local `links_extraidos.json`.
3. Notifica a la API externa enviando solo los enlaces que no han sido registrados antes.


Tecnologías Utilizadas

- [x] Python 3.13.7
- [x] JSON
- [x] Git / GitHub
- [x] Requests
- [x] Re 
- [x] Servidor Linux (UABC)

 
*Dependencias y Librerías Requeridas
El codigo está hecho en Python 3.13.7 y utiliza las librerías:

* Librerías externas:
  - `requests`: Para realizar las peticiones HTTP GET a X (Twitter) y POST a la API.
* Librerías de Python
  - `json`: Manejo de lectura/escritura del archivo de historial `links_extraidos.json`.
  - `datetime`: Manejo de fechas dinámicas y validación del año/día.
  - `os`: Navegación de rutas de archivos y gestión del sistema.

-Comando de instalación:
Ejecuta el siguiente comando en tu terminal para instalar las dependencias necesarias:
```bash
pip install requests

Detailed Design 

Solucion 1

En esta sección se detalla el funcionamiento de cada una de las funciones que se realizaron en el código Python:

1. Obtener y extraer links (`extractor_links_twitter`)
A través de la función `extractor_links_twitter(url_fuente, limite)` se realiza una petición HTTP GET a la página de X utilizando encabezados (`User-Agent`) que simulan un navegador real. Se analiza el código HTML con la expresión regular `r"/(?:[a-zA-Z0-9_]+)/status/(\d+)"` para capturar los IDs de los tweets y construir los enlaces oficiales.

```python
def extractor_links_twitter(url_fuente: str, limite: int = 15) -> list:
    #Envía petición GET con headers de navegador
    #Extrae IDs y arma las URLs: [https://x.com/i/web/status/](https://x.com/i/web/status/){tweet_id}
    #Retorna la lista de URLs encontradas


-Consumo de la API del Extractor-

El codigo consume directo la API de extracción que realizaron las compañeras Alejandra y Ximena. 

Propósito: Transmitir la lista de URLs recién extraídas de X que no han sido procesadas.
URL objetivo: `https://relax-albatross-pessimism.ngrok-free.dev/urls`
-Método HTTP: `POST`
-Headers:
  - `Content-Type: application/json`
  - `ngrok-skip-browser-warning: 69420`

*Formato de datos enviados (Payload):
  ```json
  {
    "urls": [
      "[https://x.com/i/web/status/184123456789](https://x.com/i/web/status/184123456789)"
    ]
  }

#Integración con la API de Catastro

El codigo forma parte de la arquitectura del sistema de tráfico e incidencias urbanas de Ensenada. El rol de este extractor dentro del Catastro se define de la siguiente manera:

1. Extracción y Filtrado:
   - Extrae publicaciones de "@EnsenadaNews" con noticias sobre vialidades o reportes urbanos.
   - Analiza el texto para identificar nombres de calles, avenidas y colonias de Ensenada.

2. API de Alejandra y Ximena:
   - Este script envía los enlaces limpios y validados mediante un `POST` a la API.
   - El servidor de Alejandra y Ximena descarga todo el contenido de la noticia y procesa las entidades extraídas.

3. Vínculo en Catastro:
   - La API de Catastro recibe la ubicación procesada (calle/colonia) y la cruza con la base de datos de claves catastrales y predios del municipio.
   - Permite consultar y mapear geográficamente qué incidencias viales reportadas en X afectan a zonas o predios específicos en el mapa de Catastro Ensenada.

#Estructura del JSON

```json
{
  "date": "2026-09-24",
  "day": "martes",
  "street": "Avenida Reforma",
  "neighborhood": "Centro",
  "confidence": 0.85
}

-Explicación del JSON:

-"date" / "day": Fecha formateada (`AAAA-MM-DD`) y día de la semana calculados con "datetime" a partir del texto de la publicación.
-"street" / "neighborhood": Nombre de la vialidad y colonia/barrio.
-"confidence" : Puntuación decimal (de 0.0 a 1.0) que mide el nivel de certeza de la extracción. Suma valor por cada campo clave encontrado para indicar qué tan confiable es la información antes de vincularla con el mapa de Catastro.

#Estructura de Proyecto

```text
X_extractor/
│
├── Avance.md                   # Documentación de avances previos del proyecto
├── extractorx.py               # Script base de extracción de X (Twitter)
├── extractorx_tcapi.py         # Script principal de extracción y envío a la API
└── readme.md                   # Documentación técnica general del proyecto