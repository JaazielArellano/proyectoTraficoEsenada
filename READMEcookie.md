# Base-de-datos
Proyecto del grupo 371 

El equipo esta formado por 3 personas. Nos repartimos diferentes partes del proyecto para poder trabajar de forma mas ordenada.

Yo llegue al acuerdo de encargarme de la parte de seguridad de la base de datos, principalmente usuarios, permisos, roles y algunas pruebas relacionadas con el acceso a la base de datos.


Primero descargue e instale Docker Desktop y DBeaver 26.0.0.
En Docker cree un servidor de PostgreSQL usando el puerto `5432` y estas variables:

POSTGRES_USER=postgres
POSTGRES_PASSWORD=contrasena
POSTGRES_DB=mi_base

<img width="1550" height="407" alt="dockerfoto" src="https://github.com/user-attachments/assets/76a7ab8f-92a2-44a1-bd72-c0d6343468c2" />

Despues de iniciar el servidor de PostgreSQL, abri DBeaver y cree una conexion nueva.

Use el puerto 5432 y los datos del usuario que configure en Docker para poder entrar a la base de datos.
Una vez conectado pude ver la base de datos mi_base y empezar a hacer pruebas con comandos de PostgreSQL.

<img width="571" height="82" alt="posgresserver" src="https://github.com/user-attachments/assets/d96ac109-8577-4eb0-9e5c-2675609e3f1e" />


Durante las pruebas tuve algunos problemas con la conexion a la base de datos.
Uno de los problemas fue al intentar conectarme con la maquina de un compañero. Mi computadora bloqueaba la IP de su maquina y por eso no se podia realizar la conexion correctamente.
Tuvimos que revisar la configuracion de la conexion y los permisos para poder identificar el problema.


### Crear un usuario

```sql
CREATE USER hola WITH PASSWORD 'contrasena';
```

### Dar todos los permisos sobre una base de datos

```sql
GRANT ALL PRIVILEGES ON DATABASE mi_base TO hola;
```

### Dar permisos para crear tablas

```sql
GRANT ALL ON SCHEMA public TO hola;
```

### Quitar permisos

```sql
REVOKE ALL PRIVILEGES ON DATABASE mi_base FROM hola;
```

### Eliminar un usuario

```sql
DROP ROLE hola;
```

### Dar permisos de administrador

```sql
ALTER ROLE hola WITH SUPERUSER;
```

### Quitar permisos de administrador

```sql
ALTER ROLE hola WITH NOSUPERUSER;
```

<img width="1335" height="495" alt="comandos" src="https://github.com/user-attachments/assets/268c50cc-26ca-47cd-87cf-4d81623ba343" />

Parte 2
Ahora hicimos lo mismo practicamente pero ahora fue desde supabase
La idea principal era que una persona tuviera el control de la base de datos y pudiera crear usuarios para los demás alumnos, decidiendo qué podía hacer cada uno.

Primero se decidió utilizar Supabase porque utiliza PostgreSQL y permite administrar una base de datos desde Internet.

Al principio se investigó cómo podían trabajar los demás alumnos dentro del proyecto. Se encontró que Supabase permite invitar personas desde:

`Organization Settings → Members`

Se probó invitando a un alumno y asignándole el rol `Developer`.

Esta opción funcionó, pero se descartó porque el rol de miembro del proyecto no permite controlar fácilmente permisos específicos como:

```text
Juan → solamente puede trabajar con APIs
Pedro → solamente puede trabajar con Datos
```

Por lo tanto, se buscó otra forma de controlar los permisos.

## Segunda opción: crear una página web

Después se probó utilizar Supabase Auth junto con una página HTML.

La idea era que cada alumno tuviera un inicio de sesión y desde la página pudiera subir información a la base de datos.

Se creó una tabla llamada `datos` y se configuró Row Level Security (RLS). También se creó una página donde el usuario podía iniciar sesión, escribir su nombre y agregar información.

Esta opción funcionó correctamente y se pudo comprobar que la información llegaba a Supabase.

Sin embargo, se decidió descartarla porque la intención del proyecto era que los alumnos trabajaran directamente con la base de datos y no mediante una página intermedia.

## Opción final

Finalmente se decidió utilizar los usuarios y permisos propios de PostgreSQL.

La idea quedó de esta manera:

```text
Administrador
      │
      ↓
Supabase / PostgreSQL
      │
 ┌────┼────┐
 ↓    ↓    ↓
Juan Pedro Otros
 │     │
APIs  Datos
```

Cada alumno tendría su propio usuario, contraseña y permisos.

Para conectarse directamente a la base de datos se utilizaría DBeaver.

## Creación del usuario

Desde:

`Supabase → SQL Editor → New Query`

se creó el primer usuario:

```sql
CREATE ROLE juan LOGIN PASSWORD 'Juan12345';
```

Después se le permitió conectarse a la base de datos:

```sql
GRANT CONNECT ON DATABASE postgres TO juan;
GRANT USAGE ON SCHEMA public TO juan;
```

También se comprobó que el usuario existiera y pudiera iniciar sesión:

```sql
SELECT rolname, rolcanlogin
FROM pg_roles
WHERE rolname = 'juan';
```

El usuario apareció correctamente y `rolcanlogin` estaba en `true`.

## Conexión desde DBeaver

Para conectar los usuarios desde sus propias computadoras se utilizó DBeaver.

En Supabase se entró a:

`Project Settings → Database → Connect`

Se probó primero la conexión y posteriormente se utilizó `Session Pooler`.

La conexión que funcionó utilizó:

```text
Host: aws-1-us-west-2.pooler.supabase.com
Port: 5432
Database: postgres
```

Para el usuario administrador se utilizó:

```text
postgres.qdalxxddputpogiaeajx
```

## Primer problema de conexión

Cuando se intentó conectar utilizando solamente:

```text
juan
```

apareció el error:

```text
FATAL: (ENOIDENTIFIER) no tenant identifier provided
(external_id or sni_hostname required)
```

Después se descubrió que el Session Pooler necesitaba que el nombre del usuario incluyera el identificador del proyecto.

Por lo tanto, en lugar de:

```text
juan
```

se utilizó:

```text
juan.qdalxxddputpogiaeajx
```

Con este formato la conexión funcionó correctamente.

## Asignación de permisos

Después de conseguir que Juan pudiera conectarse, se crearon tablas para comprobar que los permisos funcionaran.

Por ejemplo, se utilizó la tabla `apis`.

A Juan se le dieron permisos mediante:

```sql
GRANT SELECT, INSERT, UPDATE ON TABLE apis TO juan;
```

Y debido a que la tabla utilizaba un ID automático también se agregó:

```sql
GRANT USAGE, SELECT ON SEQUENCE apis_id_seq TO juan;
```

De esta manera Juan podía consultar, insertar y modificar información de `apis`.

## Segundo problema: RLS

Al intentar insertar información desde DBeaver apareció:

```text
ERROR: new row violates row-level security policy
for table "apis"
```

El problema era que la tabla tenía activado Row Level Security (RLS).

Como el proyecto finalmente utilizaría usuarios y permisos propios de PostgreSQL mediante `GRANT` y `REVOKE`, se decidió desactivar RLS para esta tabla:

```sql
ALTER TABLE apis DISABLE ROW LEVEL SECURITY;
```

Después de hacerlo, Juan pudo insertar información correctamente.

## Comprobación de los permisos

Para comprobar que los usuarios realmente estuvieran separados, se creó otra tabla llamada `datos`.

Juan recibió permisos sobre `apis`, pero no sobre `datos`.

Por lo tanto:

```text
Juan
 ├── apis  → ✅
 └── datos → ❌
```

Al intentar acceder a `datos` desde DBeaver utilizando la cuenta de Juan, PostgreSQL rechazó el acceso.

Esto permitió comprobar que los permisos estaban funcionando correctamente.

En el futuro se puede crear otro usuario, por ejemplo:

```text
Pedro
 ├── datos → ✅
 └── apis  → ❌
```

Mientras que el administrador mantiene acceso completo.

## Resultado final

Después de probar las diferentes opciones, el proyecto terminó utilizando:

* Supabase como servidor de PostgreSQL.
* PostgreSQL Roles para crear usuarios.
* `GRANT` y `REVOKE` para controlar permisos.
* DBeaver para las conexiones.
* Session Pooler para las conexiones externas.

Cada alumno tiene sus propias credenciales y puede conectarse desde su computadora sin necesidad de compartir la cuenta principal.

La estructura final es:

```text
                 Supabase
                    │
                PostgreSQL
                    │
              Administrador
                    │
        ┌───────────┼───────────┐
        ↓           ↓           ↓
      Juan        Pedro       Otros
        │           │
     DBeaver     DBeaver
        │           │
      APIs        Datos
```

## Conclusión

El proyecto comenzó intentando utilizar directamente los miembros de Supabase, pero se descartó porque no permitía manejar de forma suficientemente específica los permisos.

Después se probó una página web utilizando Supabase Auth y RLS. Esta alternativa funcionó, pero tampoco se utilizó porque se buscaba que los alumnos trabajaran directamente con la base de datos.

Finalmente se optó por utilizar los usuarios nativos de PostgreSQL y conectarlos mediante DBeaver.

Con este método, cada alumno tiene su propio usuario, contraseña y permisos, mientras que el administrador mantiene el control de la base de datos y decide qué puede hacer cada usuario.


