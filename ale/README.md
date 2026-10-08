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
  modelos.py           # Contratos de datos (Pydantic)
  limpieza.py          # Funciones de limpieza
  test_limpieza.py     # Pruebas con pytest
  requirements.txt     # Dependencias
```

| Archivo | Contenido |
|---|---|
| `modelos.py` | `NoticiaCruda`, `LoteCrudo` (entrada) y `NoticiaLimpia`, `ResultadoLimpieza` (salida) |
| `limpieza.py` | `limpiar_html()`, `limpiar_noticia()` y `limpiar_lote()` |
| `test_limpieza.py` | 5 pruebas unitarias |

## 4. Cómo funciona la limpieza

La función principal es `limpiar_html()` y sigue cuatro pasos:

1. **Corrige la codificación** con `ftfy` (ej. `registrÃ³` → `registró`).
2. **Parsea el HTML** con `BeautifulSoup` + `lxml`, que tolera HTML mal formado.
3. **Elimina lo que no es contenido**: `script`, `style`, `nav`, `footer`, `header`, `aside`, `iframe` y `form`.
4. **Extrae el texto** y colapsa espacios y saltos de línea repetidos.

Funciones de más alto nivel:

- `limpiar_noticia(noticia, fuente)` — limpia una noticia y arma el registro en el formato de contrato.
- `limpiar_lote(lote)` — limpia todas las noticias de una fuente de una sola vez.

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

Resultado: **5 pruebas, 5 aprobadas.**

| Prueba | Qué valida |
|---|---|
| `test_quita_etiquetas_script_y_footer` | Que no quede contenido de `<script>` ni `<footer>` |
| `test_corrige_codificacion_mal_hecha` | Que los errores de codificación se corrijan |
| `test_colapsa_espacios_y_saltos_de_linea` | Que los espacios múltiples se normalicen |
| `test_html_vacio_regresa_texto_vacio` | Que HTML vacío no genere errores |
| `test_limpiar_lote_arma_contrato_oficial` | Que la salida cumpla el contrato (`source`, `url`, `retrieved_at`, `text`) |

También se probó el flujo completo: descargar una página real con `requests.get()` y limpiarla con `limpiar_html()`, confirmando que el resultado llega limpio y en el formato correcto.

## 8. Lo que se hizo

- Definí junto con Ximena el contrato de datos entre Collector y Cleaner.
- Investigué y probé BeautifulSoup, lxml y ftfy para la limpieza de HTML y la corrección de codificación.
- Construí la librería `cleaner_lib` como paquete independiente y reutilizable.
- Escribí y ejecuté las pruebas unitarias con pytest.
- Armé un ejemplo de integración para que Ximena lo conecte a su Collector.
- Empaqueté y compartí la librería con Ximena.

## 9. Pendientes

- Probar la librería con HTML real de las fuentes (Facebook, Ensenada.net, El Vigía, entre otras).
- Ajustar la lista de etiquetas a eliminar según los casos reales que aparezcan (tablas, imágenes con texto alternativo, etc.).
- Definir con Ximena dónde se guardará el resultado consolidado antes de pasarlo al Extractor.
- Agregar evidencia visual (capturas de las pruebas pasando) a la documentación del repositorio.
