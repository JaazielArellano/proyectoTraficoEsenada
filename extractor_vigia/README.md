# Módulo Extractor – El Vigía

- **Alumna:** Angela Guadalupe Martínez Rivera
- **Materia:** Patrones de Comportamiento de Datos 

## Descripción

El módulo Extractor se encarga de procesar la información limpia de las noticias de **El Vigía**, la cual es entregada por un proceso externo. La función de este módulo es identificar y extraer datos importantes de las noticias, como fechas, días de la semana, calles, avenidas y colonias, para guardarlos y enviarlos en un archivo JSON que servirá de entrada para el siguiente proceso externo.

## Objetivo

Recopilar, procesar y estructurar datos de noticias publicados en la página web de **El Vigía**.

## Tecnologías, recursos y herramientas/plataformas
- **Versión de Python 3.14.3:** Lenguaje utilizado para desarrollar el extractor.
- **Programa Visual Studio Code:** Edición del código.
- **Terminal (CMD):** Para trabajar con Git (control de versiones).
- **Requests:** Librería para realizar solicitudes HTTP.
- **json:** Organizar los datos en formato JSON.

## Archivos del proyecto

- **`main.py`**: Script principal que ejecuta el código completo.
- **`url.py`**: Extracción y almacenamiento de enlaces de noticias desde el RSS.
- **`enviar_post.py`**: Envío de URLs hacia la API del validador de peticiones.
- **`extractor_vigia.py`**: Análisis de texto, detección de fechas, días de la semana, calles, avenidas y colonias y generación del contrato JSON.
