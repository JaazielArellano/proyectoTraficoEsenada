# Modulo Extractor de Noticias de X (Twitter)

* **Link del repositorio:** https://github.com/JaazielArellano/proyectoTraficoEsenada/tree/extractor/X_extractor
* **Autor:** Arturo Muñiz Tavarez 
* **Materia:** Patrones de Comportamiento 
* **Grupo:** 371
* **Modulo:** Extractor de X
* **Status:** Readme listo para calificacion
* **Ultima actualizacion:** 23/10/26

**archivo:** `extractor_X.py`

---
## Contenido
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
---

## Objetivo
Obtener publicaciones de X (Twitter) sobre noticias de tráfico o sucesos de la ciudad, extraer de manera sencilla la ubicación (calle, colonia y su nivel de certeza) y la fecha, y guardar todo ordenado en un archivo JSON.


## Goals
- Extraer automáticamente enlaces de tweets desde la fuente web sin dependencias dificiles.
- Filtrar los enlaces mediante un archivo local (`noticias_x.json`). 
- Enviar solo los links nuevos mediante solicitudes HTTP POST en formato JSON.

## Non-Goals
- Sincronización en tiempo real.
- Procesar o analizar el texto/contenido de los tweets.
- Crear una interfaz gráfica (UI); el programa opera 100% por consola.

## Background

Se requiere un sistema capaz de monitorear y recolectar noticias sobre tráfico e incidentes viales publicadas por la cuenta (@EnsenadaNews). Para lograrlo de forma ligera, clara y fácil de mantener sin usar expresiones regulares, se implementó un extractor mediante peticiones HTTP directas que procesa y estructura la información geográfica en un archivo local JSON.

## Overview

1. **Consulta HTTP:** Realiza una petición `POST` a la API de Apify para obtener las últimas publicaciones de la cuenta objetivo en X.
2. **Filtrado de duplicados:** Compara las URLs de las publicaciones descargadas contra las ya almacenadas en el registro local `noticias_x.json`.
3. **Procesamiento y persistencia:** Extrae la ubicación (calle/colonia), determina la certeza del hallazgo y calcula la fecha normalizada para guardar solo los registros nuevos en el JSON local.

## Tecnologías Utilizadas

- [x] Python 3.13.7
- [x] JSON
- [x] Git / GitHub
- [x] Requests
- [x] Servidor Linux (UABC)

## Dependencias y Librerías Requeridas-
El codigo está hecho en Python 3.13.7 y utiliza las librerías:

**Librerías externas:**
  - `requests`: Para realizar la petición HTTP POST a la API de Apify.
**Librerías de Python:**
  - `json`: Para la lectura del archivo de historial `noticias_x.json`.
  - `datetime`: Manejo de fechas dinámicas y validación del año/día.
  - `os`: Para verificar la existencia del archivo de caché en el sistema.

## Configuración del Entorno

### 1. Requisitos Previos
Tener instalado **Python 3.8 o superior** y **Git** en tu sistema. Puedes verificar tu versión de Python ejecutando:

```bash
python --version
```
## Configuración de Apify (API Key)

El módulo utiliza **Apify** como servicio para realizar el scraping ligero de publicaciones en X (Twitter). Para que el script funcione correctamente, se requiere un Token de API personal:

### Pasos para obtener tu Token:
1. Regístrate o inicia sesión en [Apify](https://www.apify.com/).
2. Ve a la sección de **Settings > Integrations** y copia tu **Personal API Token**.
3. En el archivo `extractor_X.py`, define tu token en la variable correspondiente o asegúrate de tenerla configurada en tus variables de entorno:

```bash
export TOKEN_APIFY="tu_token_aqui"
```
### 1. Clonar el repositorio

`git clone https://github.com/JaazielArellano/proyectoTraficoEsenada.git`  
`cd proyectoTraficoEsenada/X_extractor`

### 2. Crear y activar el entorno virtual

> - **En Linux / macOS:**  
>   `python3 -m venv venv`  
>   `source venv/bin/activate`  
> - **En Windows (PowerShell):**  
>   `python -m venv venv`  
>   `.\venv\Scripts\Activate.ps1`  
> - **En Windows (CMD):**  
>   `python -m venv venv`  
>   `.\venv\Scripts\activate.bat`

### 3. Instalación de bibliotecas

> - **Instalar librerías externas:**  
>   `pip install requests`  
> - **Manejo de módulos nativos:**  
>   `import json`  
>   `import os`  
>   `from datetime import datetime`  
>   *(No requieren instalación vía pip, ya vienen integradas en la instalación estándar de Python).*

### 4. Ejecucion de codigo 

`python extractor_X.py`

### 5. Contrato de salida

Despues de ejecutar el script, se generara un archivo JSON (`noticias_x.json`) en donde vendran los URLS extraidos con los datos que necesitamos. 

## Detailed Design

En esta sección se detalla la arquitectura interna del extractor, describiendo los componentes clave del código y el flujo de datos desde la consulta inicial hasta el almacenamiento.

### 1. Componentes del Sistema

- **Cliente HTTP (`requests`):** Se encarga de enviar la petición `POST` a la API de Apify enviando las credenciales y el token de acceso para extraer el JSON con las publicaciones recientes de la cuenta.
- **Módulo de Parsing y Extracción:** Recorre cada publicación obtenida y aplica la lógica de coincidencia de palabras clave para identificar automáticamente nombres de calles, colonias y asignar un nivel de certeza (*alta*, *media* o *baja*).
- **Normalizador de Fechas (`datetime`):** Convierte las marcas de tiempo nativas de la API al formato estándar de fecha y hora local para garantizar consistencia en los registros.
- **Gestor de Persistencia (`json` y `os`):** Lee el archivo `noticias_x.json`, valida los enlaces para evitar duplicados y guarda únicamente los eventos nuevos.

---

## Consideraciones y Riesgos

En esta sección se describen los factores clave y limitaciones técnicas que se deben tomar en cuenta al operar este módulo.

### 1. Cuota y Límites de la API (Apify)
- **Riesgo:** La API de Apify cuenta con un límite de créditos gratuitos/mensuales. Un número excesivo de peticiones HTTP en poco tiempo podría consumir la cuota disponible.
- **Mitigación:** Configurar la ejecución del script mediante un intervalo adecuado (por ejemplo, ejecuciones programadas cada varias horas o una vez al día) para no agotar los créditos.

### 2. Dependencia de la Estructura de Texto de la Cuenta
- **Riesgo:** El módulo utiliza patrones de texto para extraer automáticamente las calles, colonias y determinar la certeza. Si la cuenta de X cambia abruptamente la manera de redactar sus publicaciones de tráfico, la precisión de la extracción de ubicaciones podría disminuir.
- **Mitigación:** Se mantiene el campo `certeza` (*alta*, *media*, *baja*) para identificar rápidamente registros que requieran revisión o ajuste en las reglas de extracción.

### 3. Concurrencia sobre el Archivo Local
- **Riesgo:** Ya que la persistencia se realiza en un archivo local `noticias_x.json`, ejecuciones simultáneas del script podrían causar conflictos de lectura/escritura en el JSON.
- **Mitigación:** Asegurar que el script se ejecute de forma secuencial y en un solo proceso a la vez.

---

## Métricas

Para evaluar el funcionamiento y rendimiento del extractor, se consideran los siguientes indicadores:

- **Tasa de detección de ubicación:** Porcentaje de publicaciones procesadas en las que se logra identificar exitosamente al menos una calle o colonia con nivel de certeza alto o medio.
- **Evitar duplicados:** Porcentaje de efectividad (100%) al descartar URLs que ya existen en el historial de `noticias_x.json`.
- **Tiempo de ejecución por ciclo:** Tiempo promedio que le toma al script realizar la petición a la API, procesar el texto y actualizar el archivo local.


## Refactorización y Mejoras de Código

Durante el desarrollo del módulo se realizaron optimizaciones clave en `extractor_X.py`

- **Estructura modular:** Se organizó la lógica en funciones específicas con responsabilidades claras (petición HTTP, análisis de ubicación, normalización de fechas y manejo del archivo JSON).
- **Manejo de excepciones:** Se implementaron bloques de control de errores para gestionar fallas en las peticiones de red o en la lectura/escritura del archivo local `noticias_x.json`.
- **Estandarización de fechas:** Se asegura que todas las fechas procesadas sigan el formato estándar ISO (`AAAA-MM-DD HH:MM:SS`), facilitando la integración con los sistemas colaboradores.

---

## Calidad de Código (Pylint)

Para garantizar un código alineado a los estándares oficiales de Python (PEP 8), el script es evaluado utilizando **Pylint**.

### Ejecución de Pylint
Para auditar la calidad del código, ejecuta el siguiente comando en la terminal:

```bash
pylint extractor_X.py






