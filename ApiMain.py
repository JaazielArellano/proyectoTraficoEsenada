"""Módulo principal de la API REST para operaciones CRUD dinámicas.

Incluye middleware CORS, paginación en consultas GET y conexión flexible 
a PostgreSQL sin restricciones de autenticación por API Key.
"""

import os
from typing import Any, Dict
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

from database import get_db_connection

load_dotenv()

# Instancia principal de la aplicación FastAPI
app = FastAPI(
    title="API CRUD Dinámica PostgreSQL",
    description="Servicio para gestión dinámica de tablas en PostgreSQL.",
    version="1.0.0"
)

# ---------------------------------------------------------
# CONFIGURACIÓN DE CORS
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DatosRegistro(BaseModel):
    """Modelo Pydantic para recibir diccionarios dinámicos en POST y PUT."""
    datos: Dict[str, Any]


# ---------------------------------------------------------
# 1. READ (GET) - Consulta de datos con paginación
# ---------------------------------------------------------
@app.get("/api/datos/{nombre_tabla}")
def consultar_tabla(
    nombre_tabla: str,
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(10, ge=1, le=100, description="Registros por página")
):
    """Consulta los datos paginados de cualquier tabla existente."""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        # Verificar si la tabla existe en el esquema público
        cur.execute(
            "SELECT EXISTS (SELECT 1 FROM information_schema.tables "
            "WHERE table_schema = 'public' AND table_name = %s);",
            (nombre_tabla,)
        )
        if not cur.fetchone()["exists"]:
            raise HTTPException(
                status_code=404,
                detail=f"La tabla '{nombre_tabla}' no existe en la base de datos."
            )

        # Cálculo de offset para paginación
        offset = (page - 1) * limit
        cur.execute(f'SELECT COUNT(*) as total FROM "{nombre_tabla}";')
        total_registros = cur.fetchone()["total"]

        # Obtener los registros filtrados
        cur.execute(
            f'SELECT * FROM "{nombre_tabla}" LIMIT %s OFFSET %s;',
            (limit, offset)
        )
        datos = cur.fetchall()

        return {
            "estatus": "ok",
            "tabla": nombre_tabla,
            "pagina_actual": page,
            "registros_por_pagina": limit,
            "total_registros": total_registros,
            "total_paginas": (total_registros + limit - 1) // limit,
            "datos": datos
        }
    except HTTPException as http_ex:
        raise http_ex
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err
    finally:
        cur.close()
        conn.close()


# ---------------------------------------------------------
# 2. CREATE (POST) - Inserción de nuevos registros
# ---------------------------------------------------------
@app.post("/api/datos/{nombre_tabla}", status_code=201)
def insertar_registro(nombre_tabla: str, body: DatosRegistro):
    """Inserta un nuevo registro de forma dinámica en la tabla indicada."""
    if not body.datos:
        raise HTTPException(
            status_code=400,
            detail="El cuerpo 'datos' no puede estar vacío."
        )

    columnas = list(body.datos.keys())
    valores = list(body.datos.values())

    cols_str = '", "'.join(columnas)
    placeholders = ', '.join(['%s'] * len(valores))

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = (
            f'INSERT INTO "{nombre_tabla}" ("{cols_str}") '
            f'VALUES ({placeholders}) RETURNING *;'
        )
        cur.execute(query, valores)
        nuevo_registro = cur.fetchone()
        conn.commit()

        return {
            "mensaje": "Registro insertado con éxito",
            "tabla": nombre_tabla,
            "nuevo_registro": nuevo_registro
        }
    except Exception as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(err)) from err
    finally:
        cur.close()
        conn.close()


# ---------------------------------------------------------
# 3. UPDATE (PUT) - Actualización de registros
# ---------------------------------------------------------
@app.put("/api/datos/{nombre_tabla}/{id_registro}")
def actualizar_registro(nombre_tabla: str, id_registro: int, body: DatosRegistro):
    """Actualiza los valores de un registro existente por su ID."""
    if not body.datos:
        raise HTTPException(
            status_code=400,
            detail="El cuerpo 'datos' no puede estar vacío."
        )

    set_clause = ", ".join([f'"{col}" = %s' for col in body.datos.keys()])
    valores = list(body.datos.values())
    valores.append(id_registro)

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = (
            f'UPDATE "{nombre_tabla}" SET {set_clause} '
            f'WHERE id = %s RETURNING *;'
        )
        cur.execute(query, valores)
        actualizado = cur.fetchone()

        if not actualizado:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró el registro con ID {id_registro}."
            )

        conn.commit()
        return {
            "mensaje": "Registro actualizado con éxito",
            "tabla": nombre_tabla,
            "registro_actualizado": actualizado
        }
    except HTTPException as http_ex:
        raise http_ex
    except Exception as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(err)) from err
    finally:
        cur.close()
        conn.close()


# ---------------------------------------------------------
# 4. DELETE (DELETE) - Eliminación de registros
# ---------------------------------------------------------
@app.delete("/api/datos/{nombre_tabla}/{id_registro}")
def eliminar_registro(nombre_tabla: str, id_registro: int):
    """Elimina un registro específico de la tabla por su ID."""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = f'DELETE FROM "{nombre_tabla}" WHERE id = %s RETURNING *;'
        cur.execute(query, (id_registro,))
        eliminado = cur.fetchone()

        if not eliminado:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró el registro con ID {id_registro}."
            )

        conn.commit()
        return {
            "mensaje": f"Registro con ID {id_registro} eliminado con éxito",
            "tabla": nombre_tabla,
            "registro_eliminado": eliminado
        }
    except HTTPException as http_ex:
        raise http_ex
    except Exception as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(err)) from err
    finally:
        cur.close()
        conn.close()
