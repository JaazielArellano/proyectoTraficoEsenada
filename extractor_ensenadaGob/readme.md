Oliver Geovanni Gallegos Lobo
Modulo: Extractor

 Extractor y Procesador de Noticias de Ensenada


 Descripción del Proyecto:
Este proyecto tiene como objetivo obtener y procesar noticias del sitio web del Gobierno de Ensenada automaticamente. El sistema obtiene los enlaces de las noticias mediante el RSS, identifica cuales  son nuevas y las guarda en archivos JSON. Depues, los enlaces se  envian a una API y una vez recibido el texto de la noticia, se procesa para obtener informacion como la fecha, día, calle, colonia y nivel de confianza.



 Objetivos
- Objetivo general: Automatizar la extraccion y procesamiento de noticias del Gobierno de Ensenada para obtener infformacion de cada noticia.

- Objetivos especificos:
  - Extraer los enlaces de las noticias mediante el RSS del Gobierno de Ensenada.
  - Identificar y guardar uicamente las noticias nuevas.
  - Enviar los enlaces de las noticias nuevas a una API.
  - Procesar el texto de las noticias recibidas.
  - Obtener datos como fecha, dia, calle y colonia.
  - Calcular un nivel de confianza de la informacion encontrada.



-[x] Python

-[x] Requests

-[x] BeautifulSoup

-[x] JSON

-[x] Expresiones regulares (`re`)

-[x] Git / GitHub

-[ ] HTML5

-[ ] CSS3

-[ ] JavaScript

-[ ] React

-[ ] Node.js

-[ ] MySQL

-[ ] MongoDB

-[ ] Otra



 Funciones Principales:
 
1.Extraer noticias: Obtiene los enlaces de las noticias desde el RSS del Gobierno de Ensenada.

2.Detectar noticias nuevas: Compara los enlaces obtenidos con un historial para identificar cuales son nuevos.

3.Guardar noticias: Guarda el historial y las noticias nuevas en archivos JSON.

4.Enviar enlaces: Envia los enlaces nuevos a una API mediante una peticion POST.

5.Procesar texto:Analiza el texto de una noticia una vez que es recibido.

6.Detectar información: Busca la fecha, día, calle y colonia dentro del texto.

7.Calcular confianza:Calcula un nivel de confianza dependiendo de los datos encontrados.


 Estructura del Proyecto

proyecto/
│

├── main.py

├── enviar_links.py

├── procesador_texto.py

├── noticias_historial_ensenada.json

└── noticias_nuevas_ensenada.json
