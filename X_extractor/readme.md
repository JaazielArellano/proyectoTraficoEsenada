Extractor de Noticias de X (Twitter) 
Link: https://github.com/tu-usuario/tu-repositorio
Autor: Arturo Muñiz Tavarez 
Status: readme listo para revision
Ultima actualización: 2026-10-02

Contenido
- Goals
- Non-Goals
- Background
- Overview
- Detailed Design
  - Solucion 1
    - Extracción (Scraper)
    - Persistencia (Historial JSON)
    - Envio (API POST)
- Consideraciones
- Métricas

Links
- Fuente de noticias: https://x.com/EnsenadaNews
- Endpoint API destino: https://relax-albatross-pessimism.ngrok-free.dev/urls

Objetivo
Desarrollar un codigo en Python que extraiga de forma automatizada enlaces de publicaciones recientes desde la cuenta de X @EnsenadaNews, filtre duplicados mediante un historial local y envíe únicamente los enlaces nuevos a un endpoint API ngrok.

Goals
- Extraer automáticamente enlaces de tweets directamente desde la fuente web sin dependencias complejas.
- Filtrar los enlaces mediante un archivo local (`links_extraidos.json`) para no reenviar duplicados a la API.
- Enviar únicamente los links nuevos mediante solicitudes HTTP POST en formato JSON.

Non-Goals
- Sincronización en tiempo real o mediante WebSockets.
- Procesar o analizar el texto de los tweets. Solo se manejan las URLs.
- Crear una interfaz gráfica (UI); el programa opera 100% por consola.

Background
Se requiere un sistema capaz de monitorear y recolectar las noticias publicadas por @EnsenadaNews para alimentar la API de un colaborador. Para lograrlo de forma mas facil y sin pagar algun servicio, se implementó un scraper liviano mediante peticiones HTTP.

Overview
El script realiza un ciclo de trabajo secuencial dividido en tres etapas:
1. Consulta el HTML público de la cuenta objetivo en X.
2. Compara los identificadores encontrados contra el registro local `links_extraidos.json`.
3. Avisa a la API externa enviando solo los enlaces que no han sido registrados antes.

Detailed Design

Solucion 1

En esta sección se detalla el funcionamiento de cada una de las funciones implementadas en el código Python:

1. Obtener y extraer links (`extractor_links_twitter`)
A través de la función `extractor_links_twitter(url_fuente, limite)` se realiza una petición HTTP GET a la página de X utilizando encabezados (`User-Agent`) que simulan un navegador real. Se analiza el código HTML con la expresión regular `r"/(?:[a-zA-Z0-9_]+)/status/(\d+)"` para capturar los IDs de los tweets y construir los enlaces oficiales.

#Desglose de la Expresión regular (`Regex`)
Para identificar los enlaces de los tweets dentro del código HTML sin depender de librerías pesadas, se utilizó la expresión regular `r"/(?:[a-zA-Z0-9_]+)/status/(\d+)"`. Su funcionamiento se desglosa de la siguiente manera:

- `/(?:[a-zA-Z0-9_]+)`: Busca el nombre de usuario en la URL (letras, números y guiones bajos). El uso de `(?: ... )` crea un grupo de no-captura, lo que significa que el script ignora el nombre de usuario para no saturar los datos recopilados.
- `/status/`: Coincide con el texto de la estructura de URLs estándar que utiliza X para las publicaciones.
- `(\d+)`: Este es el grupo de captura principal. Busca uno o más dígitos numéricos seguidos, los cuales corresponden al ID único del tweet.

#Ejemplo de coincidencia:
En el texto HTML `/EnsenadaNews/status/184123456789`, la expresión regular extrae solo el ID `184123456789`, permitiendo construir el enlace directo: `https://x.com/i/web/status/184123456789`.

```python
def extractor_links_twitter(url_fuente: str, limite: int = 15) -> list:
    # Envía petición GET con headers de navegador
    # Extrae IDs y arma las URLs: [https://x.com/i/web/status/](https://x.com/i/web/status/){tweet_id}
    # Retorna la lista de URLs encontradas