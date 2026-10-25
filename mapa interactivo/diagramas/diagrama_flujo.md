# Diagrama de flujo del proyecto Extracción de Datos Geográficos (Ensenada)

Este diagrama muestra el flujo general de datos del proyecto, desde la extracción hasta el componente del mapa interactivo.

```mermaid
flowchart TD
    A[Fuentes de datos<br/>CFE, Catastro, DENUE, Vigía, etc.] --> B[Módulos extractores<br/>scripts de scraping / APIs externas]
    B --> C[(Base de datos<br/>PostgreSQL)]
    C --> D[API CRUD<br/>puerto 4003 /api/datos/tabla]
    D --> E[Dashboard - Mapa Interactivo<br/>ejemplo_dashboard.py]

    E --> F{¿La tabla trae<br/>coordenadas?}
    F -->|Sí| G[Usa lat/lon de la API]
    F -->|No| H[Busca un lugar conocido<br/>en el texto del registro]

    G --> I[Dibuja marcador naranja<br/>en el mapa]
    H --> I

    I --> J[Usuario interactúa:<br/>filtra, busca, hace clic]
    J --> K[Agrega nota manual<br/>marcador azul]
    K --> L[(Guardado en memoria<br/>st.session_state - temporal)]

    style A fill:#2d2d2d,color:#fff
    style C fill:#1f4e79,color:#fff
    style D fill:#1f4e79,color:#fff
    style E fill:#2e7d32,color:#fff
    style L fill:#6a1b1a,color:#fff
```

**Nota:** el recuadro rojo (`st.session_state`) indica que, por ahora, las notas agregadas con clic solo viven en memoria mientras la app está abierta guardarlas de forma permanente en la base de datos queda como trabajo futuro (ver `DESIGN_DOC.md`, sección *Non-Goals*).
