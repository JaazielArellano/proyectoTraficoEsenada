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

# Tecnologiass utilizadas

El proyecto utiliza principalmente Python y diferentes librerias para realizar solicitudes web, procesar informacion y trabajar con archivos JSON.

-[x] Python

-[x] Requests

-[x] BeautifulSoup

-[x] JSON

-[x] Expresiones regulares (`re`)

-[x] Git / GitHub

# Requisitos
Antes de ejecutar el proyecto es necesario contar con:

- Python 3 instalado.
- Visual Studio Code o un editor de codigo.


 Funciones Principales:
1.Extraer noticias: Obtiene los enlaces de las noticias desde el RSS del Gobierno de Ensenada.
2.Detectar noticias nuevas: Compara los enlaces obtenidos con un historial para identificar cuales son nuevos.
3.Guardar noticias: Guarda el historial y las noticias nuevas en archivos JSON.
4.Enviar enlaces: Envia los enlaces nuevos a una API mediante una peticion POST.
5.Procesar texto:Analiza el texto de una noticia una vez que es recibido.
6.Detectar información: Busca la fecha, día, calle y colonia dentro del texto.
7.Calcular confianza:Calcula un nivel de confianza dependiendo de los datos encontrados.


# Estructura del Proyecto

El proyecto esta organizado en tres archivos principales de Python y dos archivos JSON. 
Cada uno cumple una funcion en especifico dentro del proceso de extraccion, envio y procesamiento de las noticias


proyecto/
│

├── main.py

├── enviar_links.py

├── procesador_texto.py

├── noticias_historial_ensenada.json

└── noticias_nuevas_ensenada.json


# Main.py 
Es el archivo principal del proyecto, Se encarga de consultar el RSS del Ayuntamiento de Ensenada,
obtener los enlaces de las noticias, identificar cuáles son nuevas y actualizar los archivos JSON

# enviar_links.py	
Lee las noticias nuevas almacenadas en el archivo JSON y las envia  a la API mediante una solicitud HTTP POST

# procesador_texto.py	
Se encarga de analizar el texto de las noticias, Busca informacion como la fecha, dia de la semana, calle y colonia, 
y calcula un nivel de confianza basandose en los datos encontrados

# noticias_historial_ensenada.json
Guarda el historial de todos los enlaces de noticias que ya fueron registrados. Se utiliza para evitar volver a procesar
una noticia que ya había sido encontrada.

# noticias_nuevas_ensenada.json	
Guarda solamente  los enlaces que fueron identificados como noticias nuevas, este archivo JSON se  utiliza despues  por
enviar_links.py para enviar la informaciion a la API.
