# Extractor de Datos de Facebook \- Proyecto Integrador Ensenada

- **Enlace:** [https\://github.com/JaazielArellano/proyectoTraficoEsenada/tree/extractor/facebook\_extractor](https://github.com/JaazielArellano/proyectoTraficoEsenada/tree/extractor/facebook_extractor)  
- **Autor(es):** Martin Roberto Gonzalez Ortiz  
- **Materia:** Patrones De Comportamiento De Datos | Grupo: 371  
- **Proyecto:** Proyecto Integrador de Extracción de Datos (Ensenada)  
- **Estado:** En revisión  
- **Última actualización:** 2026-10-07

---

## **Tabla de Contenidos**

1. [Instalación y Ejecución](#instalación-y-ejecución)  
2. [Objetivos y No-Objetivos](#objetivos-y-no-objetivos)  
3. [Fondo y Contexto](#fondo-y-contexto)  
4. [Descripción General](#descripción-general)  
5. [Diseño Detallado](#diseño-detallado)  
   - [Módulo de Extracción (Apify API)](#1-módulo-de-extracción-apify-api)  
   - [Módulo de Gestión de Caché Local](#2-módulo-de-gestión-de-caché-local)  
   - [Módulo de Distribución y Webhook (ngrok API)](#3-módulo-de-distribución-y-webhook-ngrok-api)  
   - [Extracción de Metadatos y NLP (Pipeline Secundario)](#4-extracción-de-metadatos-y-nlp-pipeline-secundario)  
6. [Consideraciones Técnicas y Seguridad](#consideraciones-técnicas-y-seguridad)  
7. [Métricas y Evaluación](#métricas-y-evaluación)  
8. [Justificación Técnica: ¿Por qué usar Regex?](#justificación-técnica-por-qué-usar-regex)

---

## **Instalación y Ejecución**

Sigue estos pasos para clonar el repositorio, configurar el entorno virtual, instalar las dependencias necesarias y ejecutar el script correctamente.

### **1\. Clonar el repositorio**

Abre tu terminal o consola de comandos y clona el proyecto desde GitHub:

```sh
git clone https://github.com/JaazielArellano/proyectoTraficoEsenada.git
cd proyectoTraficoEsenada/facebook_extractor
```

&nbsp;

### **2\. Crear y activar el entorno virtual (`venv`)**

Crear un entorno virtual permite aislar las librerías requeridas para este proyecto.

* **En Linux / macOS:**

```sh
python3 -m venv venv
source venv/bin/activate
```

* **En Windows (PowerShell):**

  ```powershell

  python -m venv venv

  .\venv\Scripts\Activate.ps1

  ```

* **En Windows (CMD):**

  ```cmd

  python -m venv venv

  .\venv\Scripts\activate.bat

  ```

### **3\. Instalar las librerías necesarias**

El script utiliza la librería de terceros `requests`. Instálala directamente en tu entorno activo ejecutando:

```sh
pip install requests
```

&nbsp;

*(Opcional: Si cuentas con un archivo `requirements.txt` en la raíz de la carpeta, puedes instalar todas las dependencias ejecutando: `pip install -r requirements.txt`)*.

### **4\. Configuración previa a la ejecución**

Antes de correr el proyecto, asegúrate de actualizar las siguientes variables en el código principal:

1. **Token de Apify:** Reemplaza la variable `MI_APIFY_TOKEN` con tu token propio y activo de Apify.  
2. **Servicio ngrok:** Verifica que el endpoint `URL_API_NGROK` coincida con tu túnel activo de ngrok.

### **5\. Ejecución del proyecto**

Una vez configurado el entorno y los tokens, ejecuta el script principal con:

```sh
python extractor_facebook.py
```

&nbsp;

*(Nota: Reemplaza `extractor_facebook.py` con el nombre exacto de tu archivo script si difiere).*

---

## **Objetivos y No-Objetivos**

### **Objetivos**

- **Automatización de Extracción:** Extraer enlaces e información de publicaciones relevantes de Facebook (ej. Página del Gobierno de Ensenada) sin requerir intervención manual.  
- **Control de Duplicados (Deduplicación):** Mantener un historial local (`noticias_facebook.json`) para procesar e iterar únicamente sobre publicaciones no registradas previamente.  
- **Procesamiento de Texto y Geolocalización:** Identificar entidades clave en los textos extraídos (fechas, días de la semana, calles, avenidas y colonias).  
- **Calificación de Calidad:** Asignar un nivel de confianza a la información procesada según la densidad de entidades encontradas.  
- **Integración Pipeline:** Despachar automáticamente las URLs recolectadas hacia un servicio web expuesto (a través de ngrok) para la comunicación con otros módulos del proyecto integrador.

### **No-Objetivos**

- **Análisis Multimedia:** No se procesarán imágenes ni archivos de video adjuntos a los posts de Facebook.  
- **Sincronización Bidireccional:** El sistema actúa únicamente como un crawler/extractor unidireccional y no realiza publicaciones ni comentarios en la red social.

---

## **Fondo y Contexto**

El flujo de información en redes sociales como Facebook sobre eventos o noticias de la ciudad de Ensenada se publica de manera no estructurada. Este módulo resuelve el problema de la ingesta manual de datos convirtiendo publicaciones no estructuradas en estructuras JSON enriquecidas.

Originalmente planteado para su ejecución mediante *Headless Web Scraping* directo (Selenium / WebDriver Manager), la arquitectura de adquisición evolucionó hacia el uso de **Apify (`facebook-posts-scraper`)** para reducir tiempos de bloqueo, sortear captchas y estandarizar la tasa de peticiones (*rate limits*).

---

## **Descripción General**

El módulo realiza un flujo en cuatro fases principales:

1. **Lectura de Caché Histórico:** Carga un conjunto de enlaces procesados con anterioridad.  
2. **Ingesta Externa (Scraping/API):** Consulta el servicio de Apify para obtener publicaciones de la fuente objetivo.  
3. **Filtrado y Limpieza de URLs:** Sanitiza parámetros de la URL y determina cuáles son completamente nuevas.  
4. **Almacenamiento y Notificación:** Actualiza la caché persistente local y despacha el payload formateado a la API remota vía ngrok.

---

## **Diseño Detallado**

### **1\. Módulo de Extracción (Apify API)**

El sistema invoca de forma síncrona el actor `apify~facebook-posts-scraper`.

- **Endpoint:** `POST https://api.apify.com/v2/acts/apify~facebook-posts-scraper/run-sync-get-dataset-items`  
- **Parámetros:**  
  - `startUrls`: `https://www.facebook.com/GobiernoDeEnsenada`  
  - `resultsLimit`: Configurable (Predeterminado: 20 publicaciones).

#### **Limpieza de URLs**

Para evitar duplicados originados por parámetros de rastreo o analíticas de URL (Query strings), las direcciones web se limpian dividiendo la cadena por los delimitadores `?` y `&`:

```py
url_limpia = url.split("?")[0].split("&")[0]
```

&nbsp;

### **2\. Módulo de Gestión de Caché Local**

Para asegurar el rendimiento y no re-procesar información ya extraída, el módulo utiliza un archivo JSON local (`noticias_facebook.json`).

- **Estructura del archivo de Caché:**

```json
{  
    "total": 45,  
    "fuente": "Facebook - Gobierno de Ensenada",  
    "links": [  
        "https://www.facebook.com/GobiernoDeEnsenada/posts/123456789",  
        "https://www.facebook.com/GobiernoDeEnsenada/posts/987654321"  
    ]  
}
```

&nbsp;

- **Lógica de deduplicación:** Mediante conjuntos (`sets` en Python), la búsqueda e identificación de duplicados se realiza de forma eficiente $O(1)$.

### **3\. Módulo de Distribución y Webhook (ngrok API)**

Si se detectan URLs que no figuran en la caché local, se arma un payload en formato JSON para ser enviado a la arquitectura central mediante una solicitud HTTP POST.

- **Endpoint de Destino:** `https://relax-albatross-pessimism.ngrok-free.dev/urls`  
- **Headers requeridos:**  
  - `Content-Type`: `application/json`  
  - `ngrok-skip-browser-warning`: `69420` *(Omite la pantalla de advertencia inicial de ngrok)*

#### **Estructura del Payload**

```json
{  
  "fuente": "Facebook - Gobierno de Ensenada",  
  "total_nuevos": 2,  
  "urls": [  
    "https://www.facebook.com/GobiernoDeEnsenada/posts/101010101",  
    "https://www.facebook.com/GobiernoDeEnsenada/posts/202020202"  
  ]  
}
```

&nbsp;

### **4\. Extracción de Metadatos y NLP (Pipeline Secundario)**

Para las fases en las que se efectúa la navegación sobre el contenido específico de las publicaciones, el pipeline aplica patrones de reconocimiento para extraer:

- **Fechas y Días:** Cálculo de fecha exacta mediante el módulo `datetime` e inferencia del día de la semana correspondiente.  
- **Entidades Geográficas:** Identificación mediante expresiones regulares (Regex) con palabras clave como Avenida, Calle, Bulevar, Colonia, Fraccionamiento.  
- **Calificación de Confianza:** Algoritmo ponderado basado en la completitud de los campos extraídos.

---

## **Consideraciones Técnicas y Seguridad**

1. **Gestión de Credenciales (CRÍTICO):**  
   - Evita dejar claves de API (`MI_APIFY_TOKEN`) hardcodeadas en el código fuente. Se recomienda migrar estas variables a un archivo de entorno `.env` utilizando `os.getenv("APIFY_TOKEN")` antes de despliegues en entornos compartidos.  
2. **Resiliencia HTTP:**  
   - La petición a Apify cuenta con un tiempo de espera (*timeout*) de 60 segundos debido a la naturaleza síncrona del cálculo del dataset.  
   - La petición a ngrok utiliza un timeout ajustado de 10 segundos para no bloquear la ejecución si el túnel se desreconecta.

---

## **Métricas y Evaluación**

- **Tasa de Ingesta:** Número de publicaciones nuevas encontradas por corrida.  
- **Nivel de Confianza Medio:** Porcentaje de datos con localización válida estructurada (vía Regex).  
- **Efectividad del Caché:** Reducción del tráfico a endpoints externos al descartar URLs repetidas.

---

## **Justificación Técnica: ¿Por qué usar Regex?**

### **1\. Desempeño y Velocidad (Cero Latencia)**

- **Regex:** Se ejecuta localmente en **microsegundos**. Puede procesar miles de publicaciones de Facebook en segundos sin depender de conexiones a servidores externos.  
- **Frente a LLMs (ej. GPT-4, Claude):** Una llamada a API para analizar un texto tarda entre 1 y 3 segundos por publicación y requiere conexión constante a internet.  
- **Frente a NLP (ej. Spacy, NLTK):** Cargar un modelo pesado de NLP consume mucha memoria RAM y CPU para tareas que se pueden resolver con reglas sencillas.

### **2\. Formato Predictible en Noticias de Gobierno y Reportes Viales**

Las noticias de fuentes oficiales o páginas de reportes (como el Gobierno de Ensenada) suelen seguir patrones sintácticos muy repetitivos:

- *"Un accidente ocurrió en **Avenida** Reforma y **Calle** Décima..."*  
- *"Obras en **Bulevar** Costero, **Colonia** Centro..."*

Regex aprovecha estos **patrones estructurales prefijados** (*"Calle"*, *"Av."*, *"Blvd."*, *"Col."*) mediante expresiones como `r"(?:Calle|Avenida|Bulevar)\s+[A-Z\u00C0-\u00DCa-z\s]+"` para extraer la información exacta de manera inmediata.

### **3\. Costo Financiero \$0**

- **Regex:** Es una herramienta nativa de Python (`import re`). No cuesta un solo centavo, sin importar si procesas 10 o 1,000,000 de publicaciones.  
- **Frente a LLMs/APIs:** El uso de modelos externos cobra por token enviado/recibido. En un scraper que lee noticias constantemente, el costo acumulado se vuelve insostenible.

### **4\. Determinismo vs. Hallazgos Probabilísticos**

- **Regex es determinista:** Si el texto cumple con la regla, extrae el dato; si no cumple, devuelve vacío. No inventa ni altera la información.  
- **Modelos IA / NLP:** Tienen riesgo de "alucinación" o de reinterpretar los nombres de las calles y colonias, lo cual altera los datos reales recopilados para el proyecto.

### **5\. Facilidad de Implementación y Mantenimiento**

Para extraer fechas (*ej. "15 de septiembre"*) y entidades geográficas específicas (*ej. "Colonia Centro"*), definir 3 o 4 reglas de Regex es mucho más directo que:

1. Entrenar o ajustar un modelo de Reconocimiento de Entidades Nombradas (NER) en Spacy.  
2. Armar pipelines complejos de procesamiento de texto.
