#  CFE Scraper & Monitoring System

Sistema automatizado en Python para el monitoreo, extracción y notificación masiva de enlaces, boletines y avisos oficiales del portal de la **Comisión Federal de Electricidad (CFE)**. 

El proyecto evade mecanismos de protección DOM (como Imperva) mediante `undetected-chromedriver`, estructura la información capturada en archivos JSON locales y permite el envío masivo de la información a un webhook/API REST.

---

## Características

- **Extracción Evasiva**: Utiliza `undetected-chromedriver` para superar las pantallas de validación iniciales (Imperva) del sitio de CFE.
- **Monitoreo Continuo**: Ciclos de escaneo configurable para detectar enlaces o noticias nuevas en tiempo real.
- **Estructuración de Datos**: Asignación de UUIDs únicos, marcas de tiempo en formato ISO (`retrieved_at`) y títulos procesados.
- **Evita Duplicados**: Compara los registros actuales con el histórico en JSON para no almacenar o notificar elementos repetidos.
- **Envío Masivo (Payload)**: Scripts integrados para empaquetar y enviar todas las URLs acumuladas en un solo request HTTP hacia la API externa.

---

## Tecnologías Utilizadas

- **Python 3.10+**
- **[undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)**: Automatización de Chrome sin detección de Selenium.
- **BeautifulSoup4**: Parseo y extracción HTML del DOM.
- **Requests**: Comunicación HTTP/REST con la API de destino.
- **JSON & UUID**: Formateo y gestión de identificadores únicos.

---

##  Estructura del Proyecto

```text
.
├── Collector CFE.py      # Envía las URLs acumuladas a la API en formato list JSON {"urls": [...]}
├── enviar_junto.py       # Envía las URLs unificadas en un solo string de texto
├── guardar.py            # Scraper con generación de UUID y control de duplicados
├── guardarlinks.py       # Monitoreo continuo guardando únicamente el arreglo de URLs
├── links.py              # Extracción general de etiquetas <a> y exportación a JSON y CSV
├── links_formato.py      # Monitoreo estructurado con esquema estandarizado (id, titulo, url, retrieved_at)
├── links_cfe.json        # Base de datos local/acumulado de enlaces en JSON
└── README.md             # Documentación del proyecto
