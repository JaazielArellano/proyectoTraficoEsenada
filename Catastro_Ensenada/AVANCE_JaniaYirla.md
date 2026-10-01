# Avance del módulo de Catastro

## ¿Qué hice?

Esta semana y media estuve trabajando en mi parte del módulo de Catastro.
Primero investigué cómo obtener datos geográficos de Ensenada desde INEGI
usando Python.

Hice pruebas con vialidades, asentamientos y localidades y logré generar
un CSV con 12,731 registros:

- 10,011 vialidades
- 329 asentamientos
- 2,391 localidades

Después hice una primera limpieza y generé otro archivo llamado
`catastro_ensenada_limpio.csv`.

## Acuerdos

Como equipo acordamos utilizar INEGI como fuente de los datos. Mi parte
consiste en la obtención y preparación de los datos y después trabajar
con la API.

Por el momento decidimos trabajar con vialidades, asentamientos y
localidades de Ensenada.

## ¿Qué estudié y aprendí?

Estuve aprendiendo a usar `requests` para hacer peticiones y obtener
información desde INEGI.

También utilicé Pandas para convertir los datos a DataFrames, unirlos,
limpiarlos y guardarlos en CSV.

Algunas funciones que aprendí a utilizar fueron:

`concat()`, `str.strip()`, `str.upper()`, `zfill()` y `drop_duplicates()`.

Todavía no he utilizado un framework porque primero estoy trabajando con
los datos. Esto se verá más adelante cuando empecemos con la API.

## Pruebas de código

Para obtener los datos de Ensenada utilicé sus claves:

```python
CVE_ENT = "02"
CVE_MUN = "001"
```

Una de las pruebas para consultar INEGI fue:

```python
respuesta = requests.get(url, timeout=60)
respuesta.raise_for_status()
datos = respuesta.json()
```

Después convertí los registros a un DataFrame:

```python
df = pd.DataFrame(registros)
```

Para la limpieza hice pruebas como:

```python
df[columna] = df[columna].str.strip()
df[columna] = df[columna].str.upper()
```

También corregí el formato de las claves:

```python
df["cve_ent"] = df["cve_ent"].str.zfill(2)
df["cve_mun"] = df["cve_mun"].str.zfill(3)
df["cve_loc"] = df["cve_loc"].str.zfill(4)
```

## Fallos y resultados

Uno de los problemas fue que al unir los datos aparecían muchos valores
vacíos. Al revisar el CSV me di cuenta de que vialidades, asentamientos
y localidades usan columnas diferentes, así que no eliminé todos los
valores vacíos porque podía borrar información válida.

También tuve que cuidar las claves `02` y `001`, porque podían perder los
ceros si se tomaban como números.

Como prueba también revisé los duplicados y el resultado fue 0. Después
de la limpieza se conservaron los 12,731 registros originales.

## Siguiente paso

Lo siguiente será seguir preparando los datos y comenzar con las pruebas
para las consultas de la API.