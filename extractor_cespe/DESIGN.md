
# Documento de Diseño Técnico (Design Doc)
## Módulo Extractor — CESPE (`extractor_cespe`)

--

## 1. Visión General y Contexto
El módulo `extractor_cespe` es un componente desacoplado del sistema central de monitoreo de tráfico para la ciudad de Ensenada. Su responsabilidad principal es interceptar comunicados oficiales de la Comisión Estatal de Servicios Públicos de Ensenada (CESPE), extraer enlaces a noticias de suspensiones de agua u obras viales, analizar el contenido textual para estructurar la información geográfica/temporal y transmitirla a la API central del proyecto.

---

## 2. Objetivos y Alcance

### Objetivos (In-Scope)
* **Monitoreo de Fuentes:** Escanear de manera dinámica la sección de noticias del portal de CESPE.
* **Manejo de Caché y Deduplicación:** Filtrar URLs ya procesadas mediante `cache.json` para garantizar que solo se procesen eventos nuevos.
* **Procesamiento de Texto (NLP / RegEx):** Extraer atributos clave (días, avenidas, colonias) a partir del texto no estructurado del comunicado.
* **Integración API:** Transmitir payloads estructurados a los endpoints del servidor principal.


### Fuera de Alcance (Lo que no hace este módulo)
* **Guardado final en base de datos:** Este módulo no guarda la información directamente en la base de datos del proyecto; únicamente le pasa los datos estructurados a la API para que el backend se encargue de almacenarlos.
* **Temporizador o ciclo continuo:** No utiliza bucles infinitos (`while True`) ni pausas de tiempo (`time.sleep`). El programa realiza su trabajo una sola vez y deja que el servidor decida cuándo volver a ejecutarlo.

---

## 3. Arquitectura y Flujo de Datos

El módulo utiliza `main.py` como punto de entrada centralizado para coordinar las tres etapas clave sin generar dependencias circulares:


       ┌────────────────────────┐
       │   Servidor / Cron      │
       └───────────┬────────────┘
                   │  (Ejecuta python main.py)
                   ▼
       ┌────────────────────────┐
       │        main.py         │ (Coordinador Principal)
       └─────┬────────────┬─────┘
             │            │
    (1. Escaneo)    (2. Transmisión)   (3. Extracción)
             │            │                   │
             ▼            ▼                   ▼
     links_nuevoCESPE  integracionApi   extractor_cespe
     ┌──────────────┐  ┌────────────┐   ┌───────────────┐
     │  cache.json  │  │ HTTP POST  │   │ extract_fields│
     │  nuevos.json │  │    API     │   │   (RegEx/NLP) │
     └──────────────┘  └────────────┘   └───────────────┘