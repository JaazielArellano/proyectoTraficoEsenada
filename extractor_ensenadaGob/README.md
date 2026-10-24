
# Módulo de Extracción y Procesamiento de Noticias: Gobierno de Ensenada

**Author:** Oliver Geovanni Gallegos Lobo  
**Module:** Extractor  
**Status:** Ready for review  
**Última actualización:** 24 de octubre de 2026

## Contenido

- [Links](#links)
- [Objetivo](#objetivo)
- [Goals](#goals)
- [Non-Goals](#non-goals)
- [Background](#background)
- [Overview](#overview)
- [Detailed Design](#detailed-design)
  - [Solution 1](#solution-1)
  - [Backend](#backend)
  - [Archivos JSON](#archivos-json)
  - [Contrato de datos](#contrato-de-datos)
- [Consideraciones](#consideraciones)
- [Métricas](#métricas)
- [Estructura de archivos](#estructura-de-archivos)
- [Guía de instalación y ejecución](#guía-de-instalación-y-ejecución)

---

## Links

- **Fuente de información:** https://www.ensenada.gob.mx/?feed=rss2
- **Repositorio del proyecto:** [Agregar aquí el enlace del repositorio personal o del equipo]
- **API receptora:** [Configurar la dirección vigente del servicio receptor en `URL_API`]
- **API local:** `http://127.0.0.1:5000/`, si la ruta principal está habilitada en `api.py`.

## Objetivo


El propósito principal de este módulo es automatizar la recolección de enlaces de noticias publicadas en el sitio oficial del Ayuntamiento de Ensenada (Ensenada.gob.mx) y facilitar el procesamiento posterior de su contenido.

El sistema consulta el canal RSS para obtener las URLs de las publicaciones, compara los enlaces encontrados con un historial para identificar cuáles son nuevos y guarda la información en archivos JSON. Posteriormente, un programa envía las URLs nuevas a un servicio externo mediante una solicitud HTTP POST.

Una vez que se dispone del texto de las noticias, otro programa permite identificar información relevante, como fechas, días de la semana, calles, avenidas y colonias. También calcula un porcentaje de confianza según la cantidad de campos detectados.

El proyecto busca reducir las tareas manuales de recolección y organización de información, además de establecer una base para analizar noticias de forma estructurada mediante Python.

## Goals

- Consultar automáticamente el canal RSS del Ayuntamiento de Ensenada.
- Extraer las URLs de las publicaciones disponibles.
- Comparar las URLs obtenidas con un historial para identificar enlaces nuevos.
- Guardar y organizar las direcciones web mediante archivos JSON.
- Enviar las URLs nuevas a un servicio externo mediante solicitudes HTTP POST.
- Procesar textos de noticias para identificar fechas, días, calles y colonias.
- Calcular un porcentaje de confianza basado en los campos identificados.
- Utilizar Flask para proporcionar una API que permita consultar información almacenada en JSON.
- Separar las tareas en archivos Python para facilitar su mantenimiento y modificación.

## Non-Goals

- No se realiza un análisis avanzado de lenguaje natural mediante modelos de inteligencia artificial dentro del procesador descrito.
- El porcentaje de confianza no representa una medida estadística de exactitud.
- La API local no implica que el sistema esté publicado en internet.
- No se considera una integración completamente automática entre todos los componentes mientras el envío, el procesamiento y la consulta de resultados dependan de ejecuciones o archivos independientes.
- No se incluye una base de datos PostgreSQL, ya que el almacenamiento descrito se realiza mediante archivos JSON.

## Background

El módulo forma parte de un proyecto de recolección y procesamiento de información publicada en internet. La fuente seleccionada es el canal RSS del Ayuntamiento de Ensenada, que permite consultar las publicaciones disponibles mediante una estructura XML.

El programa utiliza Python para obtener los enlaces, organizarlos y distinguir las noticias nuevas de las que ya se registraron. Esta separación evita tener que revisar manualmente cada publicación y permite mantener un historial local de las direcciones encontradas.

Después, las URLs nuevas pueden enviarse a un servicio externo para continuar con la obtención del contenido. El texto disponible se analiza mediante funciones de procesamiento que buscan información relevante para su posterior organización.

Finalmente, el proyecto incluye una API desarrollada con Flask para consultar datos almacenados en un archivo JSON. Esta parte permite practicar la comunicación entre programas mediante solicitudes HTTP y respuestas estructuradas.

## Overview

El proyecto se organiza en programas independientes que realizan diferentes etapas del proceso.

El archivo `main.py` consulta el RSS, extrae las URLs y actualiza los archivos JSON que utiliza para registrar las noticias conocidas y las nuevas. Para ello, utiliza `requests`, `BeautifulSoup` y `json`.

El archivo `enviar_links.py` lee las URLs nuevas y las envía a la dirección configurada en `URL_API` mediante una solicitud HTTP POST. La recepción y obtención del texto dependen del servicio externo al que se envían los datos.

El archivo `procesador_texto.py` trabaja con textos de entrada y contiene funciones para identificar fechas, días, calles y colonias. También calcula un porcentaje de confianza y muestra los resultados del análisis.

Como componente complementario, `api.py` utiliza Flask para leer un archivo JSON y devolver su contenido mediante una ruta HTTP.

La solución utiliza archivos JSON como medio de almacenamiento e intercambio de datos. No requiere una base de datos externa en la configuración descrita.

## Detailed Design

### Solution 1

La solución consiste en dividir el proceso en etapas para que cada programa tenga una responsabilidad específica.

#### Frontend

- **N/A.** El proyecto no incluye una interfaz gráfica propia.
- La información puede consultarse mediante archivos JSON, la consola de Python o el navegador cuando se utiliza la API local de Flask.

#### Backend

**1. Recolección de noticias — `main.py`**

El programa consulta el canal RSS:

`https://www.ensenada.gob.mx/?feed=rss2`

Utiliza `requests` para obtener la respuesta del servidor y `BeautifulSoup` para analizar el XML. Después, localiza los elementos correspondientes a las publicaciones y extrae las URLs.

Los enlaces obtenidos se comparan con el historial para identificar las publicaciones nuevas. Finalmente, el programa actualiza los archivos JSON de acuerdo con la lógica implementada.

**2. Envío de enlaces — `enviar_links.py`**

El programa lee el archivo JSON que contiene las URLs nuevas y prepara la información para enviarla al servicio receptor.

La comunicación se realiza mediante una solicitud HTTP POST. La dirección del servicio se configura en la variable `URL_API`.

El programa puede mostrar la respuesta recibida y capturar errores de conexión. Si se utiliza Ngrok, la dirección debe estar vigente y el servicio receptor debe encontrarse activo.

**3. Procesamiento de texto — `procesador_texto.py`**

El procesador recibe o lee textos de noticias y ejecuta funciones para identificar información específica.

- `detectar_fechas()`: busca fechas.
- `detectar_dias()`: identifica días de la semana.
- `detectar_calles()`: busca nombres de calles o avenidas.
- `detectar_colonias()`: busca nombres de colonias.
- `porcentaje_confianza()`: calcula la proporción de campos identificados.
- `procesador_noticias(texto)`: organiza el análisis del texto.

En la versión descrita, el programa utiliza datos de entrada almacenados en un archivo JSON y presenta los resultados en la consola.

**4. API de consulta — `api.py`**

Este componente utiliza Flask para crear una API que lee un archivo JSON y devuelve su contenido como respuesta HTTP.

Si se encuentra configurada la ruta principal `/`, la información puede consultarse desde `http://127.0.0.1:5000/noticias` mientras el servidor está activo.

La API devuelve el contenido del archivo configurado. Para que entregue automáticamente los resultados generados por el procesador, es necesario conectar ambas partes mediante un archivo compartido o una comunicación adicional.

### Archivos JSON

Los archivos JSON permiten almacenar información sin necesidad de utilizar una base de datos externa.


- **`noticias_historial_ensenada.json`:** nombre alternativo mencionado durante el desarrollo para el archivo histórico. Debe utilizarse únicamente si coincide con el código actual.
- **`noticias_nuevas_ensenada.json`:** almacena las URLs identificadas como nuevas y sirve como entrada para `enviar_links.py`.
- **`noticias_pruebas.json`:** contiene datos de prueba utilizados por el procesador o la API, según la configuración de cada archivo.

Los nombres anteriores deben verificarse en el código antes de ejecutar el proyecto, ya que Python necesita que las rutas y los nombres coincidan exactamente.

### Contrato de datos

El formato JSON se utiliza para intercambiar información entre componentes.

Un ejemplo de la estructura enviada por `enviar_links.py` es:

```json
{
  "urls": [
    "https://www.ensenada.gob.mx/ejemplo-1",
    "https://www.ensenada.gob.mx/ejemplo-2"
  ]
}
```

Las URLs son ilustrativas y no corresponden a noticias verificadas.

Un ejemplo de entrada para el procesamiento de texto es:

```json
{
  "url": "https://www.ensenada.gob.mx/ejemplo",
  "texto": "El martes se realizarán trabajos en Avenida Reforma, colonia Centro."
}
```

El procesador puede identificar campos como fecha, día, calle y colonia. El resultado concreto depende de las reglas de detección y del texto de entrada.

Si se encuentran tres de los cuatro campos evaluados, el porcentaje calculado sería:

`(3 / 4) × 100 = 75 %`

Este valor representa la proporción de campos encontrados, no una garantía de que los datos sean correctos.

Los ejemplos anteriores documentan estructuras posibles y no deben confundirse con respuestas reales obtenidas durante una ejecución.

## Consideraciones

- **Dependencias:** se requiere Python y las bibliotecas externas utilizadas por los programas, principalmente `requests`, `beautifulsoup4` y `Flask`.
- **Entorno virtual:** se recomienda utilizar `venv` para mantener separadas las dependencias del proyecto.
- **Archivos JSON:** los nombres, las rutas y las estructuras deben coincidir con lo que espera cada programa.
- **Conexión externa:** el envío de URLs depende de que la API receptora esté disponible y de que la dirección configurada sea válida.
- **Ngrok:** si se utiliza una dirección temporal, es necesario actualizar `URL_API` cuando cambie.
- **Procesamiento:** las reglas de búsqueda pueden no reconocer nombres escritos con abreviaturas, variantes o formatos distintos.
- **Actualización periódica:** una ejecución continua requiere que el ciclo y la pausa estén habilitados en el código. La existencia de `time.sleep(21600)` por sí sola no garantiza que el programa vuelva a consultar el RSS.
- **Seguridad HTTPS:** si una solicitud utiliza `verify=False`, se desactiva la verificación del certificado. Se recomienda mantener la verificación habilitada en la versión definitiva.
- **API local:** la dirección `127.0.0.1` solo permite acceder al servicio desde el equipo local. Para ofrecer acceso externo se requiere una configuración adicional.
- **Control de versiones:** conviene excluir `venv/`, `.venv/` y archivos temporales del repositorio. No deben subirse contraseñas, tokens ni claves privadas.
- **Integración:** el envío de URLs, el procesamiento de texto y la consulta mediante Flask deben verificarse por separado. No se debe asumir que los resultados pasan automáticamente de un componente a otro.

## Métricas

Las siguientes métricas pueden utilizarse para evaluar el funcionamiento del módulo:

- **Cantidad de URLs extraídas:** número de enlaces recuperados del RSS durante una ejecución.
- **Noticias nuevas identificadas:** cantidad de URLs que no estaban registradas en el historial.
- **Detección de duplicados:** revisión de que los enlaces ya registrados no se agreguen nuevamente como nuevos.
- **Comunicación HTTP:** revisión de los códigos de estado y de los mensajes de respuesta del servicio receptor.
- **Campos identificados:** cantidad de fechas, días, calles y colonias reconocidos en los textos de prueba.
- **Porcentaje de confianza:** proporción de los cuatro campos que fueron detectados.
- **Respuesta de la API local:** comprobación de que Flask devuelve el contenido JSON esperado.
- **Manejo de errores:** verificación de la respuesta del programa cuando falla la conexión o un archivo no está disponible.

Las métricas deben obtenerse de ejecuciones reales. No se asignan porcentajes de calidad ni resultados de rendimiento sin contar con evidencias.

## Estructura de archivos

La estructura propuesta para el módulo es:

```text
extractor_ensenada/
│
├── main.py
├── enviar_links.py
├── procesador_texto.py
├── api.py
│
├── noticias_historial_ensenada.json
├── noticias_nuevas_ensenada.json
├── noticias_pruebas.json
│
├── requirements.txt
├── .gitignore
└── README.md
```

Los archivos JSON incluidos en la estructura son ejemplos de los archivos utilizados durante el desarrollo. La estructura definitiva debe reflejar los nombres y las rutas presentes en el código.

### Archivo `requirements.txt`

Para las bibliotecas externas descritas, el archivo puede contener:

```text
requests
beautifulsoup4
Flask
```

Las bibliotecas estándar `json`, `re` y `time` no necesitan incluirse en este archivo.

Si el proyecto requiere versiones específicas, se recomienda registrar y probar las versiones utilizadas en el entorno de desarrollo.

### Archivo `.gitignore`

Se recomienda excluir el entorno virtual y los archivos que no sea necesario compartir:

```gitignore
venv/
.venv/
__pycache__/
*.py[cod]
.env
```

Los archivos JSON de historial y pruebas deben incluirse o excluirse según las necesidades del equipo. No se deben ignorar automáticamente si forman parte de las evidencias o de los datos necesarios para ejecutar el proyecto.

---

# Guía de Instalación y Ejecución

Sigue estos pasos para preparar el proyecto en Windows.

### 1. Obtener los archivos

Si el proyecto está guardado en GitHub, clona el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
```

Reemplaza `URL_DEL_REPOSITORIO` por la dirección real del repositorio.

Después, accede a la carpeta:

```bash
cd nombre_del_proyecto
```

Si ya tienes los archivos en tu computadora, abre CMD en la carpeta donde están guardados.

### 2. Comprobar Python

Ejecuta:

```bash
python --version
```

El proyecto necesita una versión de Python compatible con las bibliotecas utilizadas. No se requiere Python 3.13 específicamente, salvo que el código o el entorno del equipo establezcan ese requisito.

### 3. Crear el entorno virtual

En CMD, ejecuta:

```bash
python -m venv .venv
```

Esto crea un entorno virtual dentro de la carpeta `.venv`.

### 4. Activar el entorno virtual

En Windows con CMD:

```bat
.venv\Scripts\activate
```

En PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Cuando se active correctamente, normalmente aparecerá `(.venv)` al inicio de la línea de comandos.

### 5. Instalar las dependencias

Con el entorno virtual activado, actualiza `pip`:

```bash
python -m pip install --upgrade pip
```

Después instala las bibliotecas:

```bash
python -m pip install -r requirements.txt
```

Si todavía no existe `requirements.txt`, puedes instalar directamente las dependencias:

```bash
python -m pip install requests beautifulsoup4 Flask
```

### 6. Configurar la dirección de la API receptora

Abre `enviar_links.py` y revisa la variable `URL_API`.

Si se utiliza Ngrok, confirma que el servicio receptor esté activo y copia la dirección vigente. No utilices una dirección antigua si la sesión ya terminó.

No se requiere un archivo `.env` para PostgreSQL en la configuración descrita, porque este módulo utiliza archivos JSON y no se ha identificado una conexión a esa base de datos.

### 7. Ejecutar el extractor

Ejecuta:

```bash
python main.py
```

Este programa consulta el RSS, extrae los enlaces y actualiza los archivos JSON configurados.

### 8. Enviar las noticias nuevas

En otra ejecución, después de comprobar que existe el archivo de noticias nuevas, ejecuta:

```bash
python enviar_links.py
```

Revisa la respuesta de la API y los posibles errores de conexión.

### 9. Procesar los textos

Para ejecutar las funciones de procesamiento, utiliza:

```bash
python procesador_texto.py
```

Verifica que el archivo JSON de entrada exista y tenga las claves que espera el código.

### 10. Iniciar la API local

Ejecuta:

```bash
python api.py
```

Si Flask se inicia correctamente, abre en el navegador:

`http://127.0.0.1:5000/`

La respuesta dependerá del archivo JSON configurado en `api.py`.

### 11. Detener los programas

Si un programa permanece ejecutándose en un ciclo continuo o Flask sigue activo, puedes detenerlo con `Ctrl + C` en la terminal correspondiente.

**Nota final:** los cuatro archivos se ejecutan de manera independiente con los comandos anteriores. Para que todo el proceso se ejecute de principio a fin sin intervención manual, se requiere implementar o verificar la coordinación automática entre los componentes.
