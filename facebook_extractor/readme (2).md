README del Módulo: Extractor de Datos de Facebook

Proyecto: Proyecto Integrador de Extracción de Datos  (Ensenada)

Módulo general: Extracción de Noticias de Facebook

Responsable de este módulo: Martin Gonzalez

Materia: Patrones De Comportamiento De Datos

Grupo: 371

¿Qué es este módulo?

Este módulo se encarga de leer automáticamente publicaciones de noticias o reportes en Facebook para convertir el texto en información ordenada y fácil de usar. En lugar de que una persona lea la publicación a mano, la computadora realiza el trabajo por sí sola:

* Entra al enlace de Facebook en segundo plano (sin abrir una ventana en la pantalla).  
* Busca el mensaje o la noticia principal dentro de la publicación.  
* Lee el texto para encontrar automáticamente dónde y cuándo ocurrió el suceso.  
* Organiza toda la información en un formato limpio (JSON) para enviarla a los demás módulos del proyecto.

¿Qué hace este módulo paso a paso?

1. Abrir la noticia: Toma la dirección de internet (URL) de Facebook y la abre usando un navegador invisible para extraer el texto principal.  
2. Manejar problemas: Si la página de Facebook no carga o no permite ver la noticia, el código usa un texto de prueba para que el programa no se detenga ni marque error.  
3. Buscar datos clave en el texto: Lee la noticia palabra por palabra buscando:  
   * La fecha exacta (por ejemplo: "15 de septiembre") y el día de la semana que le corresponde (por ejemplo: "martes").  
   * La calle, avenida o bulevar donde ocurrió el hecho.  
   * La colonia o fraccionamiento mencionado.  
4. Evaluar la calidad: Revisa cuántos datos logró encontrar. Entre más información encuentre (calle, colonia, fecha y día), más alta será la calificación de confianza del resultado.  
5. Entregar el resultado: Genera una lista ordenada con los campos: fecha, día, calle, colonia y nivel de confianza.

Herramientas utilizadas

| Herramienta | Para qué sirve en este módulo |
| :---- | :---- |
| Selenium | Hace que la computadora abra y navegue en Facebook de forma automática e invisible. |
| WebDriver Manager | Se encarga de descargar y preparar el navegador Chrome para que funcione con el código. |
| Expresiones Regulares (Regex) | Son "filtros de búsqueda" que ayudan a encontrar palabras clave dentro del texto como "Avenida", "Colonia" o fechas. |
| Datetime | Ayuda a calcular qué día de la semana cayó la fecha encontrada (lunes, martes, etc.) y le pone el año correcto. |
| JSON | Es el formato final en el que se guardan y entregan los datos ordenados para que los demás módulos del sistema puedan entenderlos. |

