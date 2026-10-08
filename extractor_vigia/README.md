# Módulo Extractor – El Vigía

**Enlace:** [Repositorio del proyecto](https://github.com/JaazielArellano/proyectoTraficoEsenada.git)  
**Autor(es):** Angela Guadalupe Martínez Rivera  
**Estado:** Listo para revisión 
**Última actualización:** 2026-10-07  

---

## Archivos principales del proyecto

- **`main.py`**: Script principal que ejecuta el código completo.
- **`url.py`**: Extracción y almacenamiento de enlaces de noticias desde el RSS.
- **`enviar_post.py`**: Envío de URLs hacia la API del validador de peticiones.
- **`extractor_vigia.py`**: Análisis de texto, detección de fechas, días de la semana, calles, avenidas y colonias y generación del contrato JSON.

## Contenido

- [Archivos principales del proyecto](#archivos-principales-del-proyecto)
- [Objetivo](#objetivo)
- [Objetivos y No-goles](#objetivos-y-no-goles)
  - [Objetivos](#objetivos)
  - [No-goles](#no-goles)
- [Fondo](#fondo)
- [Descripción general](#descripción-general)
- [Diseño detallado](#diseño-detallado)
  - [Solución 1: Ejecución mediante la función `ejecutar()` desde `main.py` y archivos JSON](#solución-1-ejecución-modular-mediante-la-función-ejecutar-desde-mainpy-y-archivos-json)
    - [Interfaz](#interfaz)
    - [Backend](#backend)
- [Consideraciones](#consideraciones)
- [Métricas](#métricas)

---

## Objetivo

¿Qué y por qué estamos haciendo esto?

En la materia **Patrones de Comportamiento de Datos**, se está desarrollando un sistema para la detección e identificación de incidentes de tráfico en Ensenada, B.C. 

El propósito del módulo **Extractor** es procesar el texto limpio de las noticias de la página web de **El Vigía** (proporcionado por un proceso externo) para identificar, extraer y estructurar datos importantes como fechas, días de la semana, calles, avenidas y colonias para guardarlos y enviarlos en un archivo JSON que servirá de entrada para el siguiente proceso externo.

---

## Objetivos y No-goles

### Objetivos
* Identificar y extraer fechas, días de la semana, calles, avenidas y colonias mencionadas en el texto limpio proporcionado por un proceso externo en un archivo JSON.
* Generar un archivo JSON (`contrato_salida.json`) para enviarse al siguiente proceso externo.

### No-goles
* **No realiza Scraping:** Es responsabilidad de un proceso externo el cual nos brinda el texto limpio en formato JSON. El módulo Extractor es responsable de extraer y enviar los enlaces desde el RSS, en mi caso mediante los scripts `url.py` y `enviar_post.py`.
* **No realiza validación geográfica/coordenadas:** El módulo no mapea latitud/longitud ni verifica si las calles existen en mapas reales.

---

## Fondo

¿Cuál es el contexto de este proyecto?

Las noticias publicadas en **El Vigía** contienen reportes como cierre de calles, accidentes, entre muchas cosas. Para poder alimentar un mapa o sistema de alertas de tráfico, es necesario transformar este texto en un formato estructurado.

---

## Descripción general

El módulo **Extractor** recibe un listado de noticias en formato JSON. Para cada elemento, toma el campo `text` y aplica patrones de análisis para reconocer ciertos datos necesarios como fechas y vialidades.

Posteriormente, construye un diccionario con la información extraída y calcula un índice de confianza. Finalmente, genera un archivo `contrato_salida.json` que sirve para los siguientes módulos del sistema.

---

## Diseño detallado

### Solución 1: Ejecución mediante la función `ejecutar()` desde `main.py` y archivos JSON

#### Interfaz

Los scripts tienen una función principal `ejecutar()` para ser importada desde `main.py` para facilitar la ejecución del código y la revisión de posibles errores.

* **Entrada (`noticias_entrada.json`):**
  ```json
  [
      {
          "source": "el_vigia",
          "url": "https://www.elvigia.net/ejemplo",
          "retrieved_at": "2026-08-29T19:00:00",
          "text": "El martes 15 de septiembre de 2026 se registró un accidente sobre Avenida Reforma y calle Primera, colonia Centro."
      }
  ]
  ```

* **Salida (`contrato_salida.json`):**
  ```json
  [
      {
          "date": "2026-09-15",
          "day": "martes",
          "street": "Primera",
          "avenue": "Reforma",
          "neighborhood": "Centro",
          "confidence": 1.0
      }
  ]
  ```

#### Backend

* **Tecnologías y herramientas:**
  * Python 3.14.3
  * Visual Studio Code
  * Terminal (CMD) / Git
  * Módulo `json`

* **Reutilización y componentes:**
  * `main.py`: Script principal que llama como librerías los scripts principales: `url.py()`, `enviar_post.py()` y `extractor_vigia.py` usando la función `ejecutar()`.
  * `url.py` / `enviar_post.py`: Scripts complementarios para la recolección y comunicación de enlaces a la API.

---

## Consideraciones

* **Manejo de nulos:** En noticias donde no se mencione alguna calle, avenida o colonia, el valor correspondiente se asigna `null` en lugar de omitirlo.
* **Ajuste de confianza (`confidence`):** El puntaje varía de `0.0` a `1.0` en base a los datos extraídos.

---

## Métricas

Para validar el correcto funcionamiento:
* **Pylint:** Mantener una calificación de **10.00/10** en estándares de código PEP 8.
* **Prueba de integración:** Verificar que el 100% de los elementos de `noticias_entrada.json` sean procesados correctamente a `contrato_salida.json`.
* **Precisión de extracción:** Validar mediante casos de prueba que la fecha, día y vialidades concuerden exactamente con el texto de la noticia recibida.
