#  **Extractor de Datos de Facebook \- Proyecto Integrador Ensenada**

* **Enlace:** \[https\://github.com/JaazielArellano/proyectoTraficoEsenada/tree/extractor/facebook\_extractor\]  
* **Autor(es):** Martin Roberto Gonzalez Ortiz  
* **Materia:** Patrones De Comportamiento De Datos | Grupo: 371  
* **Proyecto:** Proyecto Integrador de Extracción de Datos (Ensenada)  
* **Estado:** En revisión  
* **Última actualización:** 2026-10-07

## **Tabla de Contenidos**

1. [Objetivos y No-Objetivos](#bookmark=id.rkuatn8qaa93)  
2. [Fondo y Contexto](#bookmark=id.wqpr6ln7fvlv)  
3. [Descripción General](#bookmark=id.j48fd56l8k0t)  
4. [Diseño Detallado](#bookmark=id.p5hl6g2ivjst)  
   * [Módulo de Extracción (Apify API)](#bookmark=id.fjez4u32p9h5)  
   * [Módulo de Gestión de Caché Local](#bookmark=id.13xfna18hwmk)  
   * [Módulo de Distribución y Webhook (ngrok API)](#bookmark=id.dig1zhfcjle7)  
   * [Extracción de Metadatos y NLP (Pipeline Secundario)](#bookmark=id.wsymavifyva0)  
5. [Consideraciones Técnicas y Seguridad](#bookmark=id.hvv40dxqvcpl)  
6. [Métricas y Evaluación](#bookmark=id.q4btiipo8kme)

## **Objetivos y No-Objetivos**

### **Objetivos**

* **Automatización de Extracción:** Extraer enlaces e información de publicaciones relevantes de Facebook (ej. Página del Gobierno de Ensenada) sin requerir intervención manual.  
* **Control de Duplicados (Deduplicación):** Mantener un historial local (noticias\_facebook.json) para procesar e iterar únicamente sobre publicaciones no registradas previamente.  
* **Procesamiento de Texto y Geolocalización:** Identificar entidades clave en los textos extraídos (fechas, días de la semana, calles, avenidas y colonias).  
* **Calificación de Calidad:** Asignar un nivel de confianza a la información procesada según la densidad de entidades encontradas.  
* **Integración Pipeline:** Despachar automáticamente las URLs recolectadas hacia un servicio web expuesto (a través de ngrok) para la comunicación con otros módulos del proyecto integrador.

### **No-Objetivos**

* **Análisis Multimedia:** No se procesarán imágenes ni archivos de video adjuntos a los posts de Facebook.  
* **Sincronización Bidireccional:** El sistema actúa únicamente como un crawler/extractor unidireccional y no realiza publicaciones ni comentarios en la red social.

## **Fondo y Contexto**

El flujo de información en redes sociales como Facebook sobre eventos o noticias de la ciudad de Ensenada se publica de manera no estructurada. Este módulo resuelve el problema de la ingesta manual de datos convirtiendo publicaciones no estructuradas en estructuras JSON enriquecidas.

Originalmente planteado para su ejecución mediante *Headless Web Scraping* directo (Selenium / WebDriver Manager), la arquitectura de adquisición evolucionó hacia el uso de **Apify (facebook-posts-scraper)** para reducir tiempos de bloqueo, sortear captchas y estandarizar la tasa de peticiones (*rate limits*).

## **Descripción General**

El módulo realiza un flujo en cuatro fases principales:

1. **Lectura de Caché Histórico:** Carga un conjunto de enlaces procesados con anterioridad.  
2. **Ingesta Externa (Scraping/API):** Consulta el servicio de Apify para obtener publicaciones de la fuente objetivo.  
3. **Filtrado y Limpieza de URLs:** Sanitiza parámetros de la URL y determina cuáles son completamente nuevas.  
4. **Almacenamiento y Notificación:** Actualiza la caché persistente local y despacha el payload formateado a la API remota vía ngrok.

## **Diseño Detallado**

### **1\. Módulo de Extracción (Apify API)**

El sistema invoca de forma síncrona el actor apify\~facebook-posts-scraper.

* **Endpoint:** POST https\://api.apify.com/v2/acts/apify\~facebook-posts-scraper/run-sync-get-dataset-items  
* **Parámetros:**  
  * startUrls: https\://www\.facebook.com/GobiernoDeEnsenada  
  * resultsLimit: Configurable (Predeterminado: 20 publicaciones).

#### **Limpieza de URLs**

Para evitar duplicados originados por parámetros de rastreo o analíticas de URL (Query strings), las direcciones web se limpian dividiendo la cadena por los delimitadores ? y &:

url\_limpia \= url.split("?")\[0\].split("&")\[0\]

### **2\. Módulo de Gestión de Caché Local**

Para asegurar el rendimiento y no re-procesar información ya extraída, el módulo utiliza un archivo JSON local (noticias\_facebook.json).

* **Estructura del archivo de Caché:**

{  
    "total": 45,  
    "fuente": "Facebook \- Gobierno de Ensenada",  
    "links": \[  
        "https\://www\.facebook.com/GobiernoDeEnsenada/posts/123456789",  
        "https\://www\.facebook.com/GobiernoDeEnsenada/posts/987654321"  
    \]  
}

* **Lógica de deduplicación:** Mediante conjuntos (sets en Python), la búsqueda de duplicados se realiza en complejidad de tiempo ![][image1].

### **3\. Módulo de Distribución y Webhook (ngrok API)**

Si se detectan URLs que no figuran en la caché local, se arma un payload en formato JSON para ser enviado a la arquitectura central mediante una solicitud HTTP POST.

* **Endpoint de Destino:** https\://relax-albatross-pessimism.ngrok-free.dev/urls  
* **Headers requeridos:**  
  * Content-Type: application/json  
  * ngrok-skip-browser-warning: 69420 *(Bypasses la pantalla de advertencia inicial de ngrok)*

#### **Estructura del Payload**

{  
  "fuente": "Facebook \- Gobierno de Ensenada",  
  "total\_nuevos": 2,  
  "urls": \[  
    "https\://www\.facebook.com/GobiernoDeEnsenada/posts/101010101",  
    "https\://www\.facebook.com/GobiernoDeEnsenada/posts/202020202"  
  \]  
}

### **4\. Extracción de Metadatos y NLP (Pipeline Secundario)**

Para las fases en las que se efectúa la navegación sobre el contenido específico de las publicaciones (mediante Selenium / Regex), el pipeline aplica patrones de reconocimiento para extraer:

* **Fechas y Días:** Cálculo de fecha exacta mediante el módulo datetime e inferencia del día de la semana correspondiente.  
* **Entidades Geográficas:** Identificación mediante expresiones regulares (Regex) con palabras clave como Avenida, Calle, Bulevar, Colonia, Fraccionamiento.  
* **Calificación de Confianza:** Algoritmo ponderado basado en la completitud de campos:  
  ![][image2]

## **Consideraciones Técnicas y Seguridad**

1. **Gestión de Credenciales (CRÍTICO):**  
   * La clave de API (MI\_APIFY\_TOKEN) se encuentra hardcodeada en el archivo. Se debe migrar a variables de entorno utilizando os.getenv("APIFY\_TOKEN") o un archivo .env antes del despliegue en producción.  
2. **Resiliencia HTTP:**  
   * La petición a Apify cuenta con un tiempo de espera (*timeout*) de 60 segundos debido a la naturaleza síncrona del cálculo del dataset.  
   * La petición a ngrok utiliza un timeout ajustado de 10 segundos para no bloquear la ejecución del programa si el tunel ngrok cae.

## **Métricas y Evaluación**

* **Tasa de Ingesta:** Número de publicaciones nuevas encontradas por corrida.  
* **Nivel de Confianza Medio:** Porcentaje de datos con localización válida estructurada (vía Regex).  
* **Efectividad del Caché:** Reducción del tráfico a endpoints externos al descartar URLs repetidas.

**PORQUE USAR REGEX**

### **1\. Desempeño y Velocidad (Cero Latencia)**

* **Regex:** Se ejecuta localmente en **microsegundos**. Puede procesar miles de publicaciones de Facebook en segundos sin depender de conexiones a servidores externos.  
* **Frente a LLMs (ej. GPT-4, Claude):** Una llamada a API para analizar un texto tarda entre 1 y 3 segundos por publicación y requiere conexión constante a internet.  
* **Frente a NLP (ej. Spacy, NLTK):** Cargar un modelo pesado de NLP consume mucha memoria RAM y CPU para tareas que se pueden resolver con reglas sencillas.

### **2\. Formato Predictible en Noticias de Gobierno y Reportes Viales**

Las noticias de fuentes oficiales o páginas de reportes (como el Gobierno de Ensenada) suelen seguir patrones sintácticos muy repetitivos:

* *"Un accidente ocurrió en **Avenida** Reforma y **Calle** Décima..."*  
* *"Obras en **Bulevar** Costero, **Colonia** Centro..."*

Regex aprovecha estos **patrones estructurales prefijados** (*"Calle"*, *"Av."*, *"Blvd."*, *"Col."*) mediante expresiones como `r"(?:Calle|Avenida|Bulevar)\s+[A-Z\u00C0-\u00DCa-z\s]+"` para extraer la información exacta de manera inmediata.

### **3\. Costo Financiero \$0**

* **Regex:** Es una herramienta nativa de Python (`import re`). No cuesta un solo centavo, sin importar si procesas 10 o 1,000,000 de publicaciones.  
* **Frente a LLMs/APIs:** El uso de modelos como OpenAI o Claude cobra por token enviado/recibido. En un scraper que lee noticias constantemente, el costo acumulado se vuelve insostenible.

### **4\. Determinismo vs. Hallazgos Probabilísticos**

* **Regex es determinista:** Si el texto cumple con la regla, extrae el dato; si no cumple, devuelve vacío. No inventa ni altera la información.  
* **Modelos IA / NLP:** Tienen riesgo de "alucinación" o de reinterpretar los nombres de las calles y colonias, lo cual altera los datos reales recopilados para el proyecto.

### **5\. Facilidad de Implementación y Mantenimiento**

Para extraer fechas (*ej. "15 de septiembre"*) y entidades geográficas específicas (*ej. "Colonia Centro"*), definir 3 o 4 reglas de Regex es mucho más directo que:

1. Entrenar o ajustar un modelo de Reconocimiento de Entidades Nombradas (NER) en Spacy.  
2. Armar pipelines complejos de procesamiento de texto.

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAAZCAYAAACo79dmAAACgElEQVR4Xu2Wz6tMYRjHZ0IREpqG5sw5M5OaJFEjUuywY3FZKFbWsrDgD5C9BaWbEiXya8ellFt3QdgruQsWLG4SpdzkXp/vzHtuj8fMnHOvcbOYTz3NvM/3ec/5vu95z3veQmHIkMFSqVSiJEnuRVG01Wu9KJVKq+I4vkzs81om3GgFN/xC5+OtVmuZya8j9xhtqlqt7rB9VEd+lDhHs2g1IUP02Yv+VP+9LoL+ql6vJ17rSqPRWEOHsVqttt1rAsOb0D+gv2AW16d5BrGf/FuibuvL5fJKtFvkJ4k7xHgvs7AU/SbXvlDoMuDfCEafENNeM+iCd4kZ89jaN6F9tdDnJtRszDCr2T3Edd77QXuKFJ2haJa46EULI7+mOurPqs1vg/ZHYsTXWvKYNdc65rU5KNpCwRQxTez2uqGIfsOa1WzQ/sxa2+aLLXnMatkknad7xWtz6MbBwCO9YF5PQV9L3UvVEqdDTn3fyYyvt+QxK8KTG/f5NojLER8EA+e9bsFYi5pvxA/+71EuvXiWibxm5YGY9Pk2PL6yxGC277pLnwDxXC+kcoM2mz4pn29jzVJ40Ospoe41MWMHtahmBeJJmU06O8Ef2w/5w8RPYiyd0ZRFXbPC7LF6q3caaQm5E8R34pLeVqO1IT9CfM3aDcKneKLZbK72WooGIqNJv91AMKINFN2XMWbrCHGK3Bvaz/jdVegy4wJ9M/FJpr0mwkzN+ki3Pkvc2Wf1hTzqta5obcosvwfsJ7UPub5gecj7Bfsr4h5ng/kQDkO3kx6HoYGRderKg05dtc4BKfLawGHZ4DWZCOt7Xmi50fehe7n/LQs9fNPneryQw/eQIf85vwDPgsYcnbNpIwAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,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>
