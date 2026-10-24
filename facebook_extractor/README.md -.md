# **Extractor de Datos de Facebook \- Proyecto Integrador Ensenada**

> * **Enlace al Repositorio:** [https\://github.com/JaazielArellano/proyectoTraficoEsenada/tree/extractor/facebook\_extractor](https://github.com/JaazielArellano/proyectoTraficoEsenada/tree/extractor/facebook_extractor)  
> * **Autor:** Martin Roberto Gonzalez Ortiz  
> * **Materia:** Patrones De Comportamiento De Datos \| Grupo: 371  
> * **Proyecto:** Proyecto Integrador de Extracción de Datos y Análisis Vial (Ensenada)  
> * **Script Principal:** Extractor  
> * **Estado:** Refactorizado / Listo para Producción (Calificación Pylint: 9.77/10)  
> * **Última actualización:** Octubre 2026

## **Tabla de Contenidos**

> 1. [Comparativa de Cambios y Nuevas Funcionalidades](#bookmark=id.wuebu670984p)  
> 2. [Bitácora de Avances Semanales (Semana 1 a Semana 5\)](#bookmark=id.pym8qbvn2kgf)  
> 3. [Instalación y Configuración del Entorno](#bookmark=id.b493e4jgkw6t)  
> 4. [Guía de Ejecución y Uso](#bookmark=id.w17kj7305wq0)  
> 5. [Arquitectura y Flujo de Datos](#bookmark=id.b1smfyc1bqv4)  
> 6. [Contrato de Salida y Estructura JSON](#bookmark=id.vajsbmkgl8y)  
> 7. [Control de Calidad, Refactorización y Pylint](#bookmark=id.96gao1alvql7)  
> 8. [Justificación Técnica: Uso de Regex vs. LLMs](#bookmark=id.ok4o27nj9ri0)  
> 9. [Manejo de Errores y Soluciones Frecuentes](#bookmark=id.wq628kivlxf)  
> 10. [Lo Que Sigue](#bookmark=id.lbbmnhhl49av)

## **Comparativa de Cambios y Nuevas Funcionalidades**

A partir del análisis del código original frente a la versión final , se destacan los siguientes cambios principales:

| Componente / Módulo | Versión Inicial (Selenium / Ingesta Inicial) | Versión Actualizada (Extractor.py)   |
| :---- | :---- | :---- |
| **Método de Scraping** | Selenium WebDriver en modo *headless* simulando interacción con el DOM de Facebook. | Peticiones HTTP síncronas directas a la API del actor de **Apify (facebook-posts-scraper)** mediante requests. |
| **Formato y Llaves del JSON** | Campos en inglés: date, day, street, neighborhood, confidence. | Campos estandarizados en español: url, fecha, dia, calle, colonia, confianza. |
| **Estructura de Caché Local** | Ruta con error sintáctico ("noticias\_facebook\_ json.") almacenando solo una lista plana de URLs. | Archivo JSON estandarizado noticias\_facebook\_json.json con metadatos (total, fuente, registros) y objetos completos. |
| **Procesamiento de Fechas** | Extracción con Regex manual sobre cadenas en español e inferencia de días. | Función auxiliar modularizada \_obtener\_fecha\_y\_dia() con lectura de ISO timestamps de Apify y mapa de días de la semana en español. |
| **Puntaje de Confianza** | Proporcional numérico (1.0 a 0.0) según la cantidad de coincidencias clave. | Categorización clara de 3 niveles: "alto" (calle y colonia), "medio" (al menos uno) y "bajo" (ninguno). |
| **Calidad de Código (PEP 8\)** | Calificación de Pylint de 9.0/10 por líneas extensas, falta de docstrings y complejidad anidada. | Calificación de **9.77/10** tras la implementación de *early returns*, tipado documental y división multilínea de Regex. |

## ---

**Bitácora de Avances Semanales**

| Periodo | Actividades Realizadas y Contribuciones | Aprendizajes y Resultados   |
| :---- | :---- | :---- |
| **Semana 1 – Semana 2** | Investigación de técnicas para evitar captchas y bloqueos al ingresar a posts públicos de Facebook. Implementación inicial de Selenium con Chrome Headless y webdriver\_manager. Acuerdo con el equipo del contrato de datos para entregar objetos limpios al módulo de integración. Uso de expresiones regulares preliminares y cálculo de fechas en español con datetime. Creación del mecanismo de respuesta de respaldo (fallback). | Aprendizaje en manipulación del DOM mediante XPATH y combinación de re.search con datetime.strptime(). Comprensión de los beneficios del modo *headless* en servidores sin interfaz gráfica. |
| **Semana 2** | Migración de Web Scraping tradicional con Selenium a arquitectura basada en peticiones HTTP con requests y la API de Apify. Implementación de un sistema de caché local para evitar la duplicación de URLs procesadas. | Reducción significativa en los tiempos de respuesta y eliminación del consumo excesivo de CPU y RAM. |
| **Semana 3** | Revisión general de especificaciones requeridas por el docente. Auditoría preliminar de documentación del proyecto. | Detección de inconsistencias en la guía de instalación y falta de explicaciones de módulos de código. |
| **Semana 4** | Corrección de patrones Regex para evitar falsos positivos en nombres de calles y fechas. Ajustes en la persistencia del archivo de caché y documentación de ejecución. | Mayor precisión en la extracción de direcciones compuestas en la ciudad de Ensenada. |
| **Semana 5** | Coordinación con el equipo de base de datos para la alineación del esquema en PostgreSQL acorde al contrato JSON (url, fecha, dia, calle, colonia, confianza). Auditoría estática de código con **Pylint** (subiendo la puntuación de 9.0/10 a **9.77/10**). Creación de la función auxiliar \_obtener\_fecha\_y\_dia() para desacoplar el procesamiento temporal. Corrección del nombre de la variable constante ARCHIVO\_CACHE a "noticias\_facebook\_json.json". Aplicación del patrón *early return* en la función de extracción y formateo PEP 8 en bloques Regex multilínea. | Dominio de linters en Python para refactorización de código limpio e inteligible. Estructuración de software modular listo para integración en producción. |

## ---

**Instalación y Configuración del Entorno**

Sigue estos pasos para instalar y ejecutar el script en cualquier entorno Python 3.8+.

### **1\. Clonar el repositorio**

`git clone https://github.com/JaazielArellano/proyectoTraficoEsenada.git`  
`cd proyectoTraficoEsenada/facebook_extractor`

### **2\. Crear y activar el entorno virtual**

> * **En Linux / macOS:**  
>   `python3 -m venv venv`  
>   `source venv/bin/activate`  
> * **En Windows (PowerShell):**  
>   `python -m venv venv`  
>   `.\venv\Scripts\Activate.ps1`  
> * **En Windows (CMD):**  
>   `python -m venv venv`  
>   `.\venv\Scripts\activate.bat`

### **3\. Instalar dependencias necesarias**

`pip install requests selenium webdriver-manager`

## ---

**Guía de Ejecución y Uso**

### **1\. Configurar credenciales**

Edita la variable MI\_APIFY\_TOKEN dentro del archivo pako3json.py con tu token activo de Apify:  
`MI_APIFY_TOKEN = "tu_token_de_apify_aqui"`

### **2\. Ejecutar el script principal**

`python Extractor.py`

### **3\. Verificación de salida**

Al finalizar la ejecución exitosa, la consola mostrará un resumen de la cantidad de registros nuevos obtenidos y guardará los datos acumulados en noticias\_facebook\_json.json.

## ---

**Arquitectura y Flujo de Datos**

> 1. **Lectura de Caché (cargar\_cache):** Lee el archivo noticias\_facebook\_json.json y recupera el conjunto de URLs ya registradas para evitar procesamiento duplicado $O(1)$.  
> 2. **Extracción Remota (extractor\_facebook\_apify):** Realiza una petición HTTP POST síncrona a Apify para extraer hasta 20 publicaciones del perfil oficial del Gobierno de Ensenada.  
> 3. **Parsing Geográfico (extraer\_ubicacion\_del\_texto):** Procesa el texto de la publicación aplicando patrones Regex para extraer la calle y la colonia, determinando el nivel de confianza (alto, medio o bajo).  
> 4. **Parsing Temporal (\_obtener\_fecha\_y\_dia):** Normaliza la fecha en formato ISO a la estructura estándar YYYY-MM-DD y la relaciona con el día de la semana en español.  
> 5. **Persistencia (guardar\_cache):** Concatena las publicaciones nuevas al arreglo previo e incrementa el contador total.

## ---

**Contrato de Salida y Estructura JSON**

La salida persistida en noticias\_facebook\_json.json respeta la siguiente estructura:  
`{`  
    `"total": 1,`  
    `"fuente": "Facebook - Gobierno de Ensenada",`  
    `"registros": [`  
        `{`  
            `"url": "https://www.facebook.com/GobiernoDeEnsenada/posts/pfbid02...",`  
            `"fecha": "2026-10-23",`  
            `"dia": "Viernes",`  
            `"calle": "Reforma",`  
            `"colonia": "Centro",`  
            `"confianza": "alto"`  
        `}`  
    `]`  
`}`

## ---

**Control de Calidad, Refactorización y Pylint**

Para cumplir con los estándares requeridos en entornos profesionales y en la materia de Patrones de Comportamiento de Datos, el script pako3json.py fue sometido a evaluación con **Pylint**.

### **Correcciones Implementadas:**

> * **Docstrings y Encabezado:** Se agregó el comentario de identificación de autoría (*MARTIN ROBERTO GONZALEZ ORTIZ*) y docstrings en formato Google/PEP 257 para el módulo y cada función.  
> * **Modularización de Funciones:** La lógica de conversión ISO a datetime fue extraída a la función privada \_obtener\_fecha\_y\_dia().  
> * **Uso de Early Returns:** Reducción de la profundidad de anidamiento en la validación del código de respuesta HTTP.  
> * **Formateo de Cadenas Regex:** Las expresiones regulares fueron divididas en múltiples líneas con paréntesis explícitos para no superar el límite de caracteres por línea.

**Calificación Obtenida:** 9.77 / 10

## ---

**Justificación Técnica: Uso de Regex vs. LLMs**

> 1. **Velocidad y Latencia Cero:** Las expresiones regulares se ejecutan en microsegundos dentro del entorno local, sin requerir procesamiento en GPU ni conexiones adicionales de red.  
> 2. **Costo Cero (\$0 USD):** Funciona utilizando librerías estándar nativas de Python (import re), eliminando cobros por consumo de tokens en APIs de Inteligencia Artificial.  
> 3. **Comportamiento Determinista:** Previene errores de "alucinación" de nombres de calles y colonias que pueden ocurrir al usar modelos del lenguaje.  
> 4. **Patrones Sintácticos Estructurados:** Los comunicados oficiales del Ayuntamiento de Ensenada utilizan conectores estándar como *"Calle"*, *"Av."*, *"Blvd."*, *"Colonia"* o *"Fracc."*, ideales para la extracción mediante reglas Regex.

## 

## **Manejo de Errores y Soluciones Frecuentes**

| Error / Incidencia | Causa Raíz | Solución Aplicada en pako3json.py   |
| :---- | :---- | :---- |
| ModuleNotFoundError: No module named 'requests' | Librería no instalada en el entorno virtual. | Ejecutar pip install requests con el entorno virtual activo. |
| Ruta de Caché Inválida | El nombre anterior de la variable tenía un espacio y extensión corrupta ("noticias\_facebook\_ json."). | Se corrigió a ARCHIVO\_CACHE \= "noticias\_facebook\_json.json". |
| Fallo de Conexión / Timeout en Apify | Caída temporal del servidor de Apify o problemas de red local. | Se añadió un bloque try-except que captura requests.RequestException y retorna una lista vacía sin interrumpir el pipeline. |
| Tabla eliminada en PostgreSQL | Inconsistencia en el servidor central del proyecto integrador. | Se alineó la estructura del objeto devuelto por Python para facilitar la recreación del esquema (url, fecha, dia, calle, colonia, confianza). |

## 

## **Lo Que Sigue**

> * **Reglas Regex Avanzadas:** Refinar las expresiones para detectar intersecciones complejas (ej. *"entre Calle Primera y Calle Segunda"*).  
> * **Integración Directa a PostgreSQL:** Implementar el conector psycopg2 o sqlalchemy para insertar automáticamente los registros con confianza alto o medio en la base de datos central.  
> * **Automatización con Crontab / Task Scheduler:** Programar la ejecución automática del script pako3json.py en el servidor para ejecutar la ingesta periódicamente

**CODIGO FUNCIONANDO**

