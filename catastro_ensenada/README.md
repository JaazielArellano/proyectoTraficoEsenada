# API de Catastro de Ensenada

Proyecto desarrollado en Python para verificar si una calle o avenida existe en Ensenada, Baja California. Utiliza una API con FastAPI y un archivo CSV, sin necesidad de conectarse a una base de datos.

## Tecnologías y archivos

- Python 3.11 o superior.
- FastAPI y Uvicorn: funcionamiento de la API.
- CSV: almacenamiento de las vialidades.
- Pytest y HTTPX: pruebas automatizadas.

Archivos principales:
- `main.py`: contiene la API y la búsqueda.
- `etl.py`: limpia y reduce los datos.
- `test_main.py`: ejecuta las pruebas.
- `catastro_ensenada_limpio.csv`: datos originales.
- `catastro_ensenada.csv`: datos procesados.
- `requirements.txt`: dependencias y versiones.

## Instalación y ejecución

Crear y activar el entorno virtual en Windows:

```bash
py -m venv venv
venv\Scripts\activate
```

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

Procesar el CSV y ejecutar la API:

```bash
python etl.py
python -m uvicorn main:app --host 127.0.0.1 --port 4003
```

Abrir http://127.0.0.1:4003/ para acceder a la documentación interactiva y realizar búsquedas.

## Proceso ETL

El archivo original contiene 12,731 registros. El ETL filtra únicamente las vialidades, conserva su nombre y tipo, elimina acentos, espacios innecesarios, registros vacíos y duplicados.

Como resultado se obtuvieron 3,776 combinaciones únicas de nombre y tipo, almacenadas en `catastro_ensenada.csv`.

## Funcionamiento de la API

El endpoint `GET /buscar` recibe el parámetro `nombre` y verifica si la vialidad está registrada.

Ejemplo:

`http://127.0.0.1:4003/buscar?nombre=Reforma`

La respuesta es un JSON:

```json
{"existe": true}
```

Si no se encuentra, devuelve:

```json
{"existe": false}
```

La búsqueda no distingue mayúsculas, minúsculas ni acentos. Solo verifica nombres, no domicilios específicos.

## Pruebas

Ejecutar:

```bash
python -m pytest -v
```

Se realizaron cuatro pruebas: vialidad existente, inexistente, entrada vacía y entrada mayor a 150 caracteres.

**Resultado obtenido: 4 pruebas aprobadas.**

## Seguridad

La API valida las entradas y limita las búsquedas a 150 caracteres. Funciona localmente con `127.0.0.1`, sin utilizar un dominio DNS público ni almacenar contraseñas.

Para publicarla en internet se recomienda utilizar HTTPS, DNSSEC cuando esté disponible, límites de peticiones y monitoreo. Estas protecciones adicionales todavía no están implementadas.

## Problemas y mejoras

Durante el desarrollo se cambió la conexión a base de datos por un CSV local. También se redujo la información mediante ETL, se instalaron dependencias faltantes y se actualizaron las pruebas al endpoint `/buscar`.

Se configuró el acceso directo a la documentación de FastAPI desde la dirección principal.

## Limitaciones

La API depende de los datos disponibles en el CSV, por lo que no garantiza que todas las vialidades estén registradas o actualizadas. Si se modifica el CSV, es necesario reiniciar el servidor.

## Conclusión

Se logró desarrollar una API que consulta vialidades de Ensenada, devuelve resultados booleanos en JSON y cuenta con un proceso ETL y pruebas automatizadas.