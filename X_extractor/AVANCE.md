Avance Módulo: Extractor de Datos de X (Twitter)

**Semana 1 y 2**

Lo que me tocó hacer

Dentro de lo general del trabajo, mi parte consiste en desarrollar el módulo Extractor X. Mi función principal es recibir el texto extraído de las publicaciones de X (Twitter), analizar los textos usando Expresiones Regulares para detectar entidades (calles, colonias, fechas y días) y generar la salida final en formato JSON calculando un índice de confianza.

Qué hice estas semanas y lo que entendí después de 847 leidas y juntas clandestinas.

Al inicio se aclararon los límites de mi parte del trabajo. El módulo Extractor solo recibe la información procesada por el equipo de para transformar el texto libre en datos estructurados.

Revisé la estructura de datos acordada para asegurar que las variables ("date", "day", "street", "neighborhood" y "confidence") coincidan con el formato esperado por el resto de los módulos del grupo. Seguimos un formato que recibimos tiempo antes.

No utilicé librerías externas de web scraping. Me enfoqué en las librerías nativas de Python:

"re": Para crear patrones de búsqueda de texto que reconozcan prefijos como "calle", "avenida", "colonia", "fracc.", etc.
"datetime": Para convertir las fechas encontradas en formato ISO (YYYY-MM-DD) y calcular el día de la semana correspondiente (lunes, martes, etc.)
"json": Para estructurar y formatear el diccionario resultante con sintaxis de llaves {} requerida por el sistema.
Acuerdos con el equipo

Yo entrego un JSON inicial con los datos de la fuente (source, url de X y retrieved\_at). El otro equipo toma esa URL, extrae el contenido de la publicación y me regresa el objeto con el campo "text" lleno.

**Semana 3**

Aunque los codigos cumplian con su funcion, seguian incumpliendo parte de los requisitos del plan de trabajo. Tuve que quitar algunas funciones que eran antiguas o que simplemente ya no se utilizaban. Tambien tuve que quitar algunas funciones de REGEX y ajustar algunos cambios en el archivo Readme que es donde se esta documentando todas las funciones de nuestro modulo. 

**Semana 4**
Por los cambios tuve complicaciones para que el codigo cumpliera su funcion. Una de las lineas regex que tenia el codigo tuve que solicitar a la IA que la hiciera codigo y termino siendo un poco mas extenso y con funciones fuera de nuestra experiencia, asi que opte por usar un API de twitter para facilitar la extraccion y agregarla al codigo.
Otro de los avances que hice fue hablar con el compañero Angel que es el encargado de la base de datos para que me creara un usuario y contraseña dentro de DBeaver para crear mi tabla donde se metera toda la informacion que almacena el JSON de mi codigo. Tuve fallas al intentar crear la tabla porque salian errores o se desorganizaba todo, pero en dia habil lo intentare de nuevo para tener la ip y conexion. 

**Semana 5**
En la ultima clase volvi a darle mi trabajo a la compañera de testing para saber si funcionaba bien el codigo, a lo que entendi no tuvo problemas con nada. 
Como ya esta por cerrar este proyecto los ultimos avances que he hecho son actualizar mis archivos de extractor en Github y actualizar el plan de trabajo con los nuevos avances que realice en las ultimas semanas, ademas de intentar entender mas sobre las funciones que estan dentro de mi codigo. 
Como ultimo utilice Pylint para calificar el codigo y saber si superaba la calificacion minima de 8.5 que nos pidieron. El codigo actualizado la supero por la minima, aun asi tenia errores de espacios en blanco y los tuve que cambiar, tambien hacia falta explicar que hacia cada modulo y cambiar nombres de variables para que estuvieran en letras minusculas. Tambien le pedi ayuda a la IA para que organizara el código que estaba suelto en funciones específicas (petición HTTP, análisis de texto, formato de fechas y guardado de JSON).  

Al final la calificacion fue un total de 9. 

**Cambios antes y despues de utilizar pylint:**

* Reemplazo de bloques except: genéricos por excepciones específicas (except requests.RequestException:, except (FileNotFoundError, json.JSONDecodeError):) para captura de los errores esperados.

* Definicion de variables globales que no cambian (como la URL de la API o la ruta de noticias_x.json) en mayúsculas sostenidas (APIFY_URL, ARCHIVO_JSON).

* Agregue comentarios de documentación al inicio del archivo y dentro de cada función para describir qué hacen, qué parámetros reciben y qué devuelven.

* Acorte las líneas de código y comentarios que superaban los 100 caracteres dividiéndolas en varios renglones.

Un poco de lo que mas o menos aprendi: 

Entendi la importancia de dejar explicaciones al inicio del archivo y dentro de cada función, indicando qué hace cada bloque, qué datos necesita para funcionar y qué resultado entrega. 

Las funciones específicas para cada tarea: una que consulta la API, otra que busca las calles y colonias en el texto, otra que ajusta el formato de las fechas y otra que guarda los datos en el archivo.

