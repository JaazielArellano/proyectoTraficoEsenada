# Módulo de Catastro / Información Geográfica

## Descripción

Mi módulo consiste en obtener y preparar información geográfica de Ensenada,
Baja California, para posteriormente utilizarla en una API de consulta.

Actualmente trabajo con datos de INEGI relacionados con:

- Vialidades
- Asentamientos
- Localidades

## Objetivo

Obtener, organizar y preparar los datos geográficos para facilitar futuras
consultas de calles, avenidas, colonias y localidades.

## Tecnologías utilizadas

- Python
- Pandas
- Requests
- JSON
- CSV
- Servicios de INEGI

## Avance actual

Desarrollé un programa en Python que realiza peticiones a los servicios de
INEGI y genera el archivo `catastro_ensenada.csv`.

Después realicé una primera limpieza de los datos para:

- Eliminar espacios innecesarios.
- Estandarizar textos a mayúsculas.
- Conservar correctamente las claves geográficas.
- Revisar registros duplicados.
- Mantener separado el archivo original del archivo limpio.

Como resultado se obtuvieron 12,731 registros:

- 10,011 vialidades
- 329 asentamientos
- 2,391 localidades

El resultado de la limpieza se guarda en
`catastro_ensenada_limpio.csv`.

El siguiente paso será continuar preparando los datos para posteriormente
desarrollar las consultas y endpoints de la API.