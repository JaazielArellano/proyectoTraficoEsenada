Avance Módulo: Extractor de Datos de X (Twitter)

Semana 1 y 2  





Lo que me tocó hacer

Dentro de lo general del trabajo, mi parte consiste en desarrollar el módulo Extractor X. Mi función principal es recibir el texto extraído de las publicaciones de X (Twitter), analizar los textos usando Expresiones Regulares para detectar entidades (calles, colonias, fechas y días) y generar la salida final en formato JSON calculando un índice de confianza.



Qué hice estas semanas y lo que entendí después de 847 leidas y juntas clandestinas.



Al inicio se aclararon los límites de mi parte del trabajo. El módulo Extractor solo recibe la información procesada por el equipo de para transformar el texto libre en datos estructurados.





Revisé la estructura de datos acordada para asegurar que las variables ("date", "day", "street", "neighborhood" y "confidence") coincidan con el formato esperado por el resto de los módulos del grupo. Seguimos un formato que recibimos tiempo antes.



No utilicé librerías externas de web scraping. Me enfoqué en las librerías nativas de Python:

* "re": Para crear patrones de búsqueda de texto que reconozcan prefijos como "calle", "avenida", "colonia", "fracc.", etc.
* "datetime": Para convertir las fechas encontradas en formato ISO (`YYYY-MM-DD`) y calcular el día de la semana correspondiente (lunes, martes, etc.)
* "json": Para estructurar y formatear el diccionario resultante con sintaxis de llaves `{}` requerida por el sistema.





Acuerdos con el equipo



Yo entrego un JSON inicial con los datos de la fuente (`source`, `url` de X y `retrieved\_at`). El otro equipo toma esa URL, extrae el contenido de la publicación y me regresa el objeto con el campo "text" lleno.



Datos Faltantes: si una noticia no menciona alguna entidad la clave correspondiente debe retornar explícitamente "null" sin romper la ejecución del código.



Cálculo Oficial de Confianza: Se implementó la regla matemática del proyecto: se inicia con una base fija de 0.50 y se suman incrementos (+0.15 por fecha, +0.10 por día, +0.15 por calle y +0.10 por colonia).



Pruebas de código:



Creé el script `extractor\_x.py` para validar el procesamiento del texto y verificar que los datos devueltos cumplan con el contrato acordado.



Funcionamiento del script:

1\. Toma el texto proporcionado dentro de la estructura.

2\. Ejecuta búsquedas con "re.search" ignorando diferencias entre mayúsculas y minúsculas (`re.IGNORECASE`).

3\. Mapea meses y calcula el día exacto de la semana usando "datetime".

4\. Evalúa la presencia de cada campo para incrementar la puntuación de "confidence" sobre la base de 0.50.

5\. Imprime en consola el objeto JSON formateado.



Correr el codigo:

Al utilizar únicamente librerías estándar de Python, no se requiere instalar paquetes externos mediante `pip`.

Ejecutar en la terminal:

&#x20; bash

&#x20; python extractor\_x.py

