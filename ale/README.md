# Módulo Cleaner — Extratron

**Responsable:** Alejandra Buelna
**Equipo:** Request / Collector / Cleaner (Ximena Lozada — Request/Collector, Alejandra Buelna — Cleaner)
**Proyecto:** Extratron — Plataforma de Extracción, Validación y Gestión de Información Geográfica

---

## 1. ¿Qué hace este módulo?

El Cleaner es el paso que convierte el **HTML crudo** que descarga el Collector en **texto limpio y legible**, listo para que el equipo de Extractor detecte fechas, calles, colonias y demás datos.

```
Fuentes web → Request/Collector (Ximena) → Cleaner (Alejandra) → Extractor
```

Para esto construí una **librería de Python** (`cleaner_lib`) que Ximena importa directamente en su código, justo después de descargar cada página. No depende de ningún framework web ni necesita levantar un servidor.

## 2. Contrato de salida

La librería entrega cada noticia en el formato oficial definido en el documento del proyecto:

```json
{
  "source": "vigia",
  "url": "https://vigia.net/nota1",
  "retrieved_at": "2026-10-08T10:00:00+00:00",
  "text": "Texto limpio y legible de la noticia."
}
```

| Campo | Descripción |
|---|---|
| `source` | Fuente de origen (ej. `vigia`, `ensenada_net`, `facebook`) |
| `url` | Link de donde se sacó la noticia |
| `retrieved_at` | Fecha y hora de procesamiento (ISO 8601, UTC) |
| `text` | Texto limpio, sin HTML, scripts ni elementos de navegación |

## 3. Estructura de la librería

```
cleaner_lib/
  __init__.py          # Expone las funciones principales
  __main__.py          # Uso desde la terminal
  modelos.py           # Contratos de datos (Pydantic)
  limpieza.py          # Funciones de limpieza
  test_limpieza.py     # Pruebas con pytest
  requirements.txt     # Dependencias
```

| Archivo | Contenido |
|---|---|
| `modelos.py` | `NoticiaCruda`, `LoteCrudo` (entrada) y `NoticiaLimpia`, `ResultadoLimpieza` (salida) |
| `limpieza.py` | `limpiar_html()`, `limpiar_registro()`, `limpiar_registros()`, `limpiar_archivo()`, `limpiar_noticia()` y `limpiar_lote()` |
| `test_limpieza.py` | 49 pruebas unitarias |

## 4. Cómo funciona la limpieza

La función principal es `limpiar_html()` y sigue estos pasos:

1. **Detecta JSON**: si la respuesta (o el campo `html`) trae JSON, se extrae solo el texto legible y se descartan llaves, ids, tokens y URLs.
2. **Corrige la codificación** con `ftfy` (ej. `registrÃ³` → `registró`) y normaliza Unicode (NFC).
3. **Parsea el HTML** con `BeautifulSoup` + `lxml`, que tolera HTML mal formado.
4. **Elimina el ruido**: `script`, `style`, `nav`, `footer`, `iframe`, etc., y también bloques de menú, pie, cookies, breadcrumbs y barras laterales identificados por su `class`, `id` o `role`, con protecciones para no borrar el contenido real.
5. **Conserva la estructura**: párrafos separados por línea en blanco, listas con `- ` y tablas de datos como filas `a | b`.
6. **Elige el contenido principal** (`<article>` o `<main>`; si es muy corto usa el `<body>`).
7. **Respaldo con metadatos** (`og:title`, `og:description`, `description`) cuando la página casi no trae texto, por ejemplo sitios que cargan con JavaScript.

Funciones de más alto nivel:

- `limpiar_registro(registro)` — limpia un registro del Collector y lo regresa en el formato del contrato, conservando su `source` y `retrieved_at`.
- `limpiar_registros(registros)` — regresa `(limpios, errores)`; un registro malo o con texto vacío no detiene a los demás.
- `limpiar_archivo(entrada, salida, ruta_errores)` — lee un JSON, lo limpia y escribe el resultado consolidado.
- `limpiar_noticia()` y `limpiar_lote()` — versiones por noticia y por fuente.

Desde la terminal: `python -m cleaner_lib ENTRADA SALIDA [ERRORES]`.

## 5. Librerías utilizadas

| Librería | Uso |
|---|---|
| `beautifulsoup4` | Recorrer el HTML y extraer el texto |
| `lxml` | Parser tolerante a HTML mal formado |
| `ftfy` | Corregir errores de codificación de caracteres |
| `pydantic` | Definir y validar los contratos de datos |
| `re` (estándar) | Normalizar espacios y saltos de línea |
| `pytest` | Pruebas unitarias |

## 6. Instalación y uso

```bash
pip install -r cleaner_lib/requirements.txt
```

Uso básico:

```python
from cleaner_lib import limpiar_html

texto = limpiar_html("<div><p>Hola <b>mundo</b></p><script>x()</script></div>")
print(texto)  # Hola mundo
```

Integración con el Collector (después de descargar el HTML con `requests`):

```python
from cleaner_lib import limpiar_html

respuesta = requests.get(url, timeout=10)
texto_limpio = limpiar_html(respuesta.text)
```

> La carpeta `cleaner_lib/` debe quedar **como carpeta** junto al código del Collector, porque se usa como paquete de Python.

## 7. Pruebas

```bash
pytest cleaner_lib/test_limpieza.py -v
```

Resultado: **49 pruebas, 49 aprobadas.**

| Grupo | Qué valida |
|---|---|
| Limpieza básica | Se quitan scripts, estilos, comentarios y pies de página; se normalizan espacios |
| Codificación | Mojibake, entidades HTML, caracteres invisibles y Unicode NFC |
| Estructura | Párrafos, listas, sublistas y tablas (de datos y de maquetación) conservan su forma |
| HTML difícil | Etiquetas sin cerrar, mayúsculas, fragmentos sin `<body>`, anidado profundo y basura que no es HTML |
| Menús y pies | Ruido detectado por `class`, `id` o `role` sin borrar contenedores con contenido real |
| Metadatos | Respaldo con `og:title`/`description` cuando el cuerpo es solo navegación o JavaScript |
| JSON | Respuesta JSON pura, escapada en `<pre>`, en una línea suelta o envuelta dos veces |
| Contrato | Salida exacta `source`, `url`, `retrieved_at`, `text`; conserva los datos del Collector |
| Lotes y archivos | Un registro malo no detiene a los demás; consolidación de un archivo completo |

## 8. Resultados

- Las **49 pruebas unitarias pasan**.
- Ximena integró `cleaner_lib` en su Collector y procesó los **152 registros** de las fuentes del proyecto.
- **149 de 152 registros (98%)** quedaron con texto limpio y legible en el campo `text`, sin HTML, menús, URLs sueltas ni JSON. Esto incluye fuentes que antes daban problemas, como Facebook, Play Store y ensenada.gob.mx.
- Los 2 registros de YouTube Shorts que siguen mostrando texto de menú fueron revisados por el profesor y aceptados tal como están.
- El resultado final cumple el contrato `source`, `url`, `retrieved_at`, `text` y quedó cargado en la tabla `recolectoras` de PostgreSQL, disponible para el equipo de Extractores.

Las cuatro métricas del módulo quedaron cubiertas: texto legible sin ruido, preservación de la estructura (párrafos, listas y tablas), invarianza de interfaz (entra el JSON del Collector y sale el contrato) y tolerancia a HTML mal formado.

## 9. Lo que se hizo

- Definí junto con Ximena el contrato de datos entre Collector y Cleaner.
- Investigué y probé BeautifulSoup, lxml y ftfy para la limpieza de HTML y la corrección de codificación.
- Construí la librería `cleaner_lib` como paquete independiente y reutilizable.
- Corregí los bugs que Ximena reportó con casos reproducibles: texto de menú y pie de página, contenido JSON en `text`, páginas con el contenido dentro de `<form>` y estructura aplastada en una sola línea.
- Escribí y ejecuté las 49 pruebas unitarias con pytest.
- Armé un ejemplo de integración y un script de procesamiento para el Collector.
- Empaqueté y compartí la librería con Ximena.
