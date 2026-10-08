# Avance – Trabajo conjunto: Mapa + Carga de Excel con API de prueba

**Alumnos:** Edgar Eduardo Lopez Orozco y Jorge Emilio García Raygoza
**Módulo:** Dashboard
**Materia:** Patrones De Comportamiento De Datos – Grupo 371
**Archivo principal de este avance:** `ejemplo_dashboard_emilio_edgar.py`

---

## Qué hicimos

Juntamos en una sola aplicación de Streamlit el mapa interactivo (la parte de Edgar, `ejemplo_dashboard.py`) y el validador de archivos (`validar_archivos.py`, la carga y validación de Excel que en el Plan de Trabajo le tocó a Emilio). Los dos archivos originales no se modificaron: todo lo que cambió está en `ejemplo_dashboard_emilio_edgar.py`.

Con esto el flujo completo ya funciona dentro de la misma app: subir un Excel, validarlo, enviarlo a una API de prueba y ver los registros guardados como puntos en el mapa.

## Cambios al validador (`validar_archivos.py`)

Las funciones `validar_json`, `validar_csv`, `validar_excel` y `cargar_archivo` conservan la lógica original. Lo único que cambió es dónde se muestran los mensajes, con el mismo texto:

| Antes | Ahora |
|---|---|
| `print(...)` con mensajes de error | `st.error(...)` |
| `print(...)` con mensajes de archivo válido | `st.success(...)` |

Además:

* Se quitó el bloque con `input()`, porque en el Dashboard el archivo se sube con un botón y ya no se escribe una ruta.
* Se agregó la función `validar_contenido_excel`, que revisa las columnas `date`, `day`, `street` y `neighborhood`, que no haya campos vacíos y que la fecha tenga formato AAAA-MM-DD. Los errores se listan con el número de fila del Excel (la fila 1 es el encabezado).

## Cambios al mapa (`ejemplo_dashboard.py`)

* La lógica del mapa se conserva. Solo se simplificó el texto de la línea 55 para dejar un mensaje más general.
* Los datos simulados quedaron entre comillas (desactivados) y se agregó un bloque nuevo que hace que el mapa dibuje los registros guardados en la base de datos de prueba. Para volver a usar los datos simulados basta quitar las comillas triples y borrar ese bloque nuevo.

## Lo nuevo que se agregó

* Carga de archivos Excel (`.xlsx`) con validación del archivo y de su contenido (`st.file_uploader`).
* Una API de prueba, con un botón "Enviar registros válidos a la API".
* Una base de datos de prueba donde la API guarda los registros.
* Columnas opcionales `lat`, `lon` y `confidence`, para que los registros aparezcan en el mapa. `lat` debe estar entre -90 y 90, `lon` entre -180 y 180 y `confidence` entre 0 y 1, y `lat` y `lon` tienen que venir juntas. Si el registro trae coordenadas pero no `confidence`, se usa 1 por defecto.

## La base de datos de prueba

Usamos una base de datos simulada: una lista que vive en la memoria de la aplicación (`st.session_state.api_registros`). Cada registro guarda `id`, `date`, `day`, `street`, `neighborhood`, `source`, `created_by` y `created_at`. Cuando el Excel trae coordenadas, también guarda `lat`, `lon` y `confidence`.

Los campos `source` y `created_by` no vienen en el Excel: la app los llena sola (`carga_excel` y `usuario_demo`).

No es un motor de base de datos real. Sirve para probar el flujo completo de subir, validar, enviar y consultar. Los datos se pierden al recargar la página o cerrar la aplicación, y un botón dentro de la app ("Borrar registros de la API simulada") los borra para repetir las pruebas.

## Qué hace la API

Una API es un intermediario: la aplicación le manda datos, la API los revisa, los guarda o los consulta, y responde con un código y un JSON. Nuestra API de prueba no es un servidor aparte, son funciones de Python dentro del mismo archivo (`_api_simulada_post`, `api_post_records` y `api_get_records`) que se comportan como una API real.

La API no busca lugares ni información en internet. Recibe los registros que se suben en el Excel, donde cada registro es un dato con fecha, día, calle y colonia, y hace lo siguiente con cada uno:

1. Revisa que traiga todos sus campos. Si falta alguno, lo rechaza.
2. Busca duplicados: compara si ya existe un registro con la misma fecha, calle y colonia. Si existe, lo rechaza.
3. Si pasa las revisiones, le asigna un `id` (desde 1001) y la fecha y hora en que se guardó, y lo guarda en la base de datos de prueba.
4. Responde con un código de estado.

| Código | Significado |
|---|---|
| 201 | Se guardaron todos los registros |
| 207 | Se guardaron algunos y otros se rechazaron |
| 400 | No se guardó ningún registro |
| 200 | Consulta correcta de los registros guardados |

También puede devolver los registros guardados cuando se le consultan (`GET /records`). Esos registros son los que el mapa dibuja como puntos.

## Cómo probarlo

```
pip install streamlit pandas folium streamlit-folium openpyxl
streamlit run ejemplo_dashboard_emilio_edgar.py
```

1. Prepara un `.xlsx` con las columnas `date`, `day`, `street` y `neighborhood` y, para verlos en el mapa, `lat` y `lon` (y opcionalmente `confidence`). Por ejemplo:

| date | day | street | neighborhood | lat | lon | confidence |
|---|---|---|---|---|---|---|
| 2026-09-15 | martes | Avenida Reforma | Centro | 31.8667 | -116.5964 | 0.92 |

2. Súbelo con el botón "Archivo Excel". La app lo valida y muestra los registros válidos y los errores por fila.
3. Presiona "Enviar registros válidos a la API". La app muestra la respuesta de la API (201, 207 o 400) y vuelve a dibujar el mapa con los registros nuevos.
4. El mapa empieza vacío porque los datos simulados están desactivados, y se llena con lo que se envíe a la API.
5. Abre "Registros guardados en la API (GET /records)" para ver lo guardado, o bórralos para repetir la prueba.

## Qué aprendimos

* Una API se puede simular con funciones de Python para probar todo el flujo antes de tener la API real.
* Conviene validar en dos niveles: primero el archivo (que sea un Excel válido) y después su contenido (columnas, campos vacíos, formato de fecha y rangos de lat/lon).
* Streamlit vuelve a correr todo el script con cada interacción, por eso lo que se quiere conservar (como los registros de la API de prueba) se guarda en `st.session_state`, y se usa `st.rerun()` para que el mapa se vuelva a dibujar con los datos nuevos.

## Pendientes y limitaciones

* Los registros se pierden al recargar o cerrar la app, porque la base de datos es de prueba y vive en la memoria.
* Para usar una API real hay que poner `USAR_API_SIMULADA = False` y definir la variable de entorno `API_URL`. Las rutas de los endpoints (`/records`) todavía hay que ajustarlas a la API que se use.
* El campo `created_by` está fijo como `usuario_demo`, hasta que se conecte con el usuario del login (parte de Jesús).
