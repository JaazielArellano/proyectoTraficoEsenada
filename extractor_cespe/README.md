
# README - Módulo Extractor CESPE

## 📝 Descripción del Proyecto
Este módulo forma parte del sistema de monitoreo de tráfico e incidencias para la ciudad de Ensenada. Se encarga de automatizar la extracción de avisos sobre suspensiones de servicio de agua e intervenciones en la vía pública publicados en el sitio oficial de CESPE. Identifica automáticamente fechas, calles, avenidas y colonias dentro del texto de los comunicados para alimentar la base de datos centralizada del proyecto.

## 🎯 Objetivos
* **Objetivo general:** Desarrollar un módulo extractor modular y autónomo de ejecución por demanda que procese comunicados de CESPE y extraiga datos geográficos y temporales de afectaciones viales.
* **Objetivos específicos:**
  * Recolectar de forma automatizada las URLs de comunicados oficiales evitando duplicados mediante control de caché local.
  * Extraer entidades clave del texto (días, avenidas, colonias) mediante patrones de expresiones regulares y procesamiento de texto.
  * Transmitir los enlaces recolectados a la API receptora del sistema principal mediante un cliente HTTP.

## 🛠️ Tecnologías Utilizadas
- [x] Python
- [ ] HTML5
- [ ] CSS3
- [ ] JavaScript
- [ ] React
- [ ] Node.js
- [ ] Java
- [ ] MySQL
- [ ] MongoDB
- [x] Git / GitHub
- [x] Librerías Python (`requests`, `json`, `re`, `os`)

## ⭐ Funcionalidades Principales
1. **Scraping y monitoreo de enlaces:** Obtiene de manera dinámica los enlaces a comunicados publicados en la plataforma web de CESPE.
2. **Gestión de caché persistente:** Mantiene un registro histórico (`cache.json`) para identificar únicamente noticias nuevas y evitar reprocesamientos.
3. **Extracción de entidades temporales y geográficas:** Identifica automáticamente patrones de calles, avenidas, colonias y fechas dentro del cuerpo de la noticia.
4. **Ejecución por demanda (One-Pass Execution):** Diseñado para ser orquestado por un servidor externo mediante un punto de entrada centralizado (`main.py`).

## 📁 Estructura del Proyecto
```text
extractor_cespe/
├── main.py              # Script principal que coordina la ejecución en una sola pasada
├── extractor_cespe.py   # Función para extraer fechas, calles y colonias del texto
├── links_nuevoCESPE.py  # Scraper de URLs y administrador de cache.json
├── integracionApi.py    # Módulo para enviar los datos procesados a la API
├── cache.json           # Registro histórico de enlaces procesados
├── cespe_links.json     # Base de datos local de enlaces guardados
├── nuevos.json          # Enlaces detectados en la última ejecución
└── README.md            # Documentación técnica del módulo