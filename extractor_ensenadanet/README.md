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
El propósito principal es ejecutar un escaneo automatizado y continuo en el portal de noticias Ensenada.net para extraer los enlaces más recientes. Esto resuelve el problema de la falta de tecnologías RSS nativas en el portal, automatizando la recolección inicial de datos para alimentar al módulo de limpieza ("Cleaner") sin requerir intervención manual constante.

## Goals
* Extraer enlaces absolutos de forma segura evadiendo bloqueos de red.
* Evadir la recolección de artículos duplicados mediante un historial en caché.
* Generar contratos de datos estandarizados en formato JSON para su posterior análisis de texto.

## Non-Goals
* No se realiza análisis de Procesamiento de Lenguaje Natural (NLP) ni limpieza del texto de las noticias en este módulo (responsabilidad delegada).
* No se mantiene una base de datos pesada tipo SQL; la persistencia es únicamente temporal en JSON para agilizar el proceso O(1).

## Background
Este módulo forma parte del sistema de recolección de datos del proyecto. Debido a que la fuente de datos carece de un endpoint estructurado, se requiere una arquitectura intermedia que extraiga el HTML (DOM), lo limpie, y lo traduzca al formato exacto que el equipo necesita para las siguientes fases de análisis geoespacial y temporal.

## Overview
El script `scraper_ensenada.py` funciona como un servicio automatizado programado para escanear el portal en intervalos regulares (ej. cada 10 minutos). Utiliza Python 3.13+, `requests` y `BeautifulSoup4` para recolectar hipervínculos, compararlos con iteraciones pasadas, y entregar un paquete limpio al adaptador API.

## Detailed Design

### Solution 1

*   **Frontend**
    *   *N/A - Este es un módulo estrictamente de Backend y recolección de datos.*

*   **Backend**
    *   **Gestión de Datos Independientes:** Para optimizar el flujo de datos y evitar la sobrecarga de información, el sistema gestiona dos salidas independientes:
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
*   **Seguridad:** Los archivos generados (`.json`) y el entorno virtual (`.venv`) se excluyen del control de versiones mediante `.gitignore` para mantener el repositorio limpio y evitar filtraciones de estado local.
*   **Trade-offs (Complejidad vs Velocidad):** En lugar de usar listas tradicionales, se emplea la conversión a `set` para buscar enlaces pasados. Esto consume ligeramente más RAM momentánea, pero garantiza una complejidad algorítmica O(1), haciendo que el escaneo sea instantáneo.

## Métricas
*   **Calidad de Código:** Evaluación de estándares de código mediante Pylint (Calificación 10/10).
*   **Rendimiento:** Validación de respuestas exitosas (Código HTTP 200/201) al interactuar con el endpoint de destino mediante `requests`.