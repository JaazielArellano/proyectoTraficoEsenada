# Módulo de Extracción Automática y Scraper: Ensenada.net

Link: [https://github.com/JaazielArellano/proyectoTraficoEsenada/tree/extractor/extractor_ensenadanet]

Author(s): Alexis Eduardo Azamar Avalos

Status: Ready for review

Ultima actualización: 2026-10-07

## Contenido
* Goals
* Non-Goals
* Background
* Overview
* Detailed Design
    * Solution 1
        * Frontend
        * Backend
* Consideraciones
* Métricas

---

## Links
* [Repositorio Principal del Proyecto](https://github.com/JaazielArellano/proyectoTraficoEsenada/tree/extractor)
* [Documentación de la API del equipo](https://relax-albatross-pessimism.ngrok-free.dev/urls)

## Objetivo
**¿Qué y por qué estamos haciendo esto?**
El propósito principal es ejecutar un escaneo automatizado y continuo en el portal de noticias Ensenada.net para extraer los enlaces más recientes. Esto resuelve el problema de la falta de tecnologías RSS nativas en el portal, automatizando la recolección inicial de datos, estructurándolos para el módulo de limpieza ("Cleaner"), y asegurando su persistencia histórica en una base de datos centralizada en el servidor, todo sin requerir intervención manual constante.

## Goals
- Extraer enlaces absolutos de forma segura evadiendo bloqueos de red.
- Evadir la recolección de artículos duplicados mediante un historial en caché local (complejidad O(1)).
- Generar contratos de datos estandarizados en formato JSON.
- Persistir el historial de recolección en una base de datos PostgreSQL, garantizando la seguridad de las credenciales del servidor mediante variables de entorno.

## Non-Goals
- No se realiza análisis de Procesamiento de Lenguaje Natural (NLP) ni limpieza del texto de las noticias en este módulo (responsabilidad delegada).
- No se exponen endpoints públicos ni se desarrollan interfaces gráficas (Frontend); es un módulo estrictamente de backend, persistencia y recolección.

## Background
Este módulo forma parte del sistema de recolección de datos del proyecto. Debido a que la fuente de datos carece de un endpoint estructurado, se requiere una arquitectura intermedia que extraiga el HTML (DOM), lo traduzca al formato exacto que el equipo necesita (JSON), y garantice que el registro histórico de extracción se guarde de forma permanente y segura en la base de datos PostgreSQL del equipo de análisis.

## Overview
El script principal funciona como un servicio automatizado preparado para ejecutarse en un servidor Linux (vía cron jobs). Utiliza Python 3.13+, `requests` y `BeautifulSoup4` para recolectar hipervínculos. Posteriormente, el módulo `basedatos.py` toma los hallazgos nuevos y los inserta de forma segura en PostgreSQL utilizando `psycopg2` y `python-dotenv` para ocultar las credenciales.

## Detailed Design

### Solution 1

*   **Frontend**
    *   *N/A - Este es un módulo estrictamente de Backend y recolección de datos.*

*   **Backend**

    -   **Gestión de Datos Independientes:** El sistema utiliza caché local temporal (`noticias_pasadas.json` y `noticias_nuevas.json`) transformando el historial en un `set` de Python para validaciones instantáneas (O(1)).
    -   **Persistencia Segura (PostgreSQL):** Una vez que se identifican noticias inéditas, el sistema se conecta a la base de datos para almacenar el título, URL y fecha de extracción en la tabla `alexis_datos`.
    -   **Ocultamiento de Credenciales:** La conexión a la base de datos es dinámica. No existen contraseñas quemadas en el código (hardcoded); el sistema lee un archivo `.env` externo para inyectar los accesos.
        *   `noticias_pasadas.json`: Base de datos histórica acumulativa. El sistema transforma este historial en un `set` de Python durante la ejecución para validar si un enlace es nuevo con una complejidad algorítmica de O(1).
        *   `noticias_nuevas.json`: Archivo dinámico que contiene únicamente los hallazgos nuevos del último ciclo de extracción.
    *   **Contrato de Salida (JSON):**
        El scraper asigna identificadores únicos generados por la librería nativa `uuid` y marcas de tiempo extraídas con `datetime`, generando el siguiente esquema:
        ```json
        [
          {
            "id": "727621fc-44af-40ce-9657-9213c21ec8bc",
            "titulo": "Título de la noticia extraída",
            "url": "[https://www.ensenada.net/noticias/nota_completa](https://www.ensenada.net/noticias/nota_completa)",
            "retrieved_at": "2026-09-22T18:45:02"
          }
        ]
        ```

## Consideraciones
-   **Seguridad y Archivo `.env`:** Por diseño, el archivo que contiene las contraseñas de la base de datos (`.env`), así como el entorno virtual (`.venv`) y los JSON de caché, están estrictamente excluidos del control de versiones mediante `.gitignore`. Cualquier desarrollador que clone este repositorio deberá crear su propio archivo `.env` localmente.
-   **Evaluación de Calidad en Servidores:** Para evitar falsos positivos al ejecutar evaluaciones de calidad (Pylint) desde cuentas maestras en el servidor Linux sin el entorno virtual activado, el código implementa directivas estratégicas de control (`# pylint: disable=import-error`) en las dependencias externas.
-   **Trade-offs (Complejidad vs Velocidad):** En lugar de usar listas tradicionales, se emplea la conversión a `set` para buscar enlaces pasados, garantizando una complejidad algorítmica O(1).

## Métricas
-   **Calidad de Código:** Evaluación de estándares PEP 8 mediante Pylint (Calificación garantizada de 10/10 en entornos locales y remotos).
-   **Rendimiento:** Validación de respuestas exitosas (Código HTTP 200/201) en el scraping y confirmación de registros insertados (`rowcount`) en PostgreSQL.

##  Estructura de Archivos

```
extractor_ensenadanet/
│
├── main.py                  # Script orquestador. Ejecuta el scraping y llama a la base de datos.
├── scraper_ensenada.py      # Navega el portal, extrae la información y filtra duplicados (crea los JSON).
├── basedatos.py             # Gestiona la conexión e inserción de datos nuevos en PostgreSQL.
├── linkapi.py               # Adaptador API para notificar al servidor del equipo.
├── requirements.txt         # Lista de dependencias (requests, beautifulsoup4, psycopg2-binary, python-dotenv).
├── .gitignore               # Reglas de seguridad para bloquear subir caché, JSONs y el archivo .env.
└── .env (No incluido)       # ARCHIVO OBLIGATORIO. Contiene variables de acceso a PostgreSQL (Debe crearse manualmente).
```

# Guia de Instalación y Ejecución

Sigue estos pasos para clonar, configurar y ejecutar el módulo localmente:

1. Clonar el repositorio

git clone https://github.com/JaazielArellano/proyectoTraficoEsenada.git


2. Crear y activar el entorno virtual (venv)

Para usuarios de Mac / Linux

python3 -m venv .venv
source .venv/bin/activate

Para usuarios de Windows

python -m venv .venv
.venv\Scripts\activate

3. Instalar dependencias

pip install -r requirements.txt

4. IMPORTANTE: Configuración de Variables de Entorno (.env)

Por motivos de seguridad, las contraseñas no vienen incluidas al descargar el código. Si omites este paso, el programa fallará al intentar conectarse a la base de datos.

Crea un archivo llamado exactamente `.env` (con el punto al inicio) en la misma carpeta donde está `main.py`. Ábrelo con tu editor de texto y agrega tus propias credenciales de PostgreSQL utilizando esta estructura exacta (sin comillas ni espacios extras):

DB_HOST=tu_direccion_ip_o_localhost
DB_PORT=5432
DB_NAME=nombre_de_tu_base_de_datos
DB_USER=tu_usuario
DB_PASS=tu_contraseña

(Nota: Este archivo está protegido por el `.gitignore`, por lo que puedes guardar tus datos con confianza de que Git nunca los subirá a internet).

5. Ejecución del proyecto

Una vez guardado tu archivo `.env`, ejecuta el archivo principal (el código se encargará de accionar todos los módulos automáticamente):

python main.py


