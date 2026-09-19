Avance Módulo: REQUEST (Validación de datos)

Semana 1 y 2

Lo que me tocó hacer

Dentro de lo general del trabajo, mi parte consiste en desarrollar el módulo REQUEST. Mi función principal es recibir el JSON que entregan los extractores (con las entidades ya detectadas: fecha, día, calle, colonia y confianza), revisar que ese JSON cumpla el contrato acordado y validarlo contra un catálogo geográfico de Ensenada, antes de que el módulo de almacenamiento lo guarde en PostgreSQL.

Qué hice estas semanas y lo que entendí

Al inicio revisé la estructura de datos acordada por el equipo, para asegurarme de que las claves ("source", "url", "retrieved_at", "text", "date", "day", "street", "neighborhood", "confidence") sean las mismas que produce el módulo Extractor. Seguimos el mismo formato que usan los demás módulos.

No utilicé librerías externas. Me enfoqué en las librerías nativas de Python:

* "json": para leer el registro de entrada y devolver el resultado de la validación en formato JSON.
* "datetime": para convertir la fecha string a un objeto fecha y calcular el día de la semana real, y así compararlo contra el campo "day".

Acuerdos con el equipo

El módulo Extractor me entrega el JSON con las entidades ya extraídas. Yo reviso que los campos obligatorios estén presentes, que la fecha y el día coincidan entre sí, y que la calle/colonia existan en el catálogo geográfico de la ciudad. Si todo pasa, el registro queda marcado como "valido": true y se puede enviar al módulo de almacenamiento (PostgreSQL); si no, se reporta la lista de errores encontrados.

Se definió que "confidence" debe estar siempre entre 0 y 1, y que si falta calle y colonia al mismo tiempo, el registro no se puede ubicar geográficamente y se descarta.

Pruebas de código

Creé el script `ejemplo_validacion.py` para probar la lógica de validación con tres casos:

1. Un registro correcto (fecha, día y ubicación válidos) → se marca como válido.
2. Un registro donde el día no coincide con la fecha real → detecta el error correctamente.
3. Un registro sin texto y con calle/colonia inventadas (fuera del catálogo) → detecta los tres errores a la vez.

Funcionamiento del script:
1. Recibe el registro (diccionario) con los datos del extractor.
2. Revisa los campos obligatorios y el rango de "confidence".
3. Si hay fecha, la convierte con "datetime" y compara el día de la semana calculado contra el campo "day".
4. Revisa si "street" y "neighborhood" existen en un catálogo de ejemplo de calles/colonias de Ensenada (el catálogo real lo tiene que definir el equipo con datos oficiales, este es solo un ejemplo).
5. Devuelve un JSON con "valido" y la lista de "errores".

Errores y fallos encontrados

* Al principio intenté comparar el día directamente como string sin normalizar mayúsculas/minúsculas, y las pruebas fallaban aunque el dato fuera correcto. Se corrigió comparando todo en minúsculas con ".lower()".
* Me faltaba catálogo real de calles y colonias de Ensenada: por ahora uso una lista de ejemplo chica, pendiente reemplazarla por el catálogo oficial que use el resto del equipo (o una fuente geográfica real, como un archivo con las colonias oficiales del municipio).
* Falta definir con el equipo qué pasa con un registro inválido: si se descarta, se guarda en una tabla aparte para revisión manual, o se reintenta. Por ahora el script solo reporta el error, no decide qué hacer con el registro.

Correr el código

Al utilizar únicamente librerías estándar de Python, no se requiere instalar paquetes externos mediante pip.

Ejecutar en la terminal:

```bash
python ejemplo_validacion.py
```
