Oliver Geovanni Gallegos Lobo
Modulo: Extractor

¿Que se ha realizado hasta el momento?

1.Conexion con el RSS
Se utilizo la libreria de requests para conectarse al RSS de la pagina web asignada en este caso de Ensenada.gob.mx, asi  
el programa descarga la informacion publicada en la pagina web y la prepara para poder ser procesada.

2.Extraccion de enlaces
Con la libreria de BeautifulSoup se analiza el archivo XML del RSS de la pagina web  para que despues, el programa busque cada noticia 
y extraega unicamente el enlace o link de una noticia en especifico para asi poder guardarlo en una lista que posteriormente se entregara al equipo de REQUEST extraccion de data limpieza (Alejandra y Ximena).

3.Guardado en JSON
Se creo una funcion dedicada a guardar todas las noticias que se encuentran dentro de la pagina web (guardar_noticias()), la cual genera el archivo noticias_ensenada.json,es aqui en donde se almacenan todos los enlaces obtenidos .

Actualizacion de noticias
Tambien se desarrollo una funcion que ayudara a obtner las noticias mas actuales  (actualizar_noticias()), esta funcion lo que hacer es volver a consultar el RSS y comparar todos  los enlaces nuevos con los que ya han sido guardados, asi Si encuentra una noticia nueva la agrega al JSON y muestra el enlace en la consola.

Acuerdo con el equipo
Se llego a un acuerdo con el modulo de  Alejandra y Ximena, quienes son responsables del modulo de  extraccion de data limpieza sobre el formato en el que se les enviaran todos los datos (links)extraidos de las diferentes paginas web.


Estado actual del programa/Modulo
Actualmente el script puede conectarse al RSS de forma correcta y sin errores , extraer los enlaces de las noticias, almacenarlos en un archivo JSON y mantener ese registro o almacenamiento actualizado con las noticias mas recientes si es que las hay. 

-A el programa le falta desarrollar una funcion que le perimita la automatizacion de este proceso
para que el extractor consulte el RSS cada cierto tiempo (por ejemplo, cada 3 horas) y actualice el archivo JSON con los links
-Analisis de los datos una vez regresen del equipo de Alejandra y Ximena.



Conceptos Aprendidos 
RSS: Es un formato XML que agrupa o reune todas las noticias publicadas por una pagina web 
XML:es el formato en el que esta estructurado o organizado el RSS en donde cada  una de las noticia esta en una etiqueta
Item:Cada noticia que se publica en la pagina web se guarda como un item y dentro de el viene la informacion de esa publicacion
