
# Mi parte del Dashboard: carga de archivos
import os
import io
import csv
import json
import zipfile
import hashlib
import logging
import sys
from openpyxl import load_workbook

LIMITE = 10 * 1024 * 1024  # 10 MB
CARPETA = os.path.join(os.path.dirname(__file__), "archivos_subidos")
log = logging.getLogger("carga_archivos")


def validar_archivo(nombre, contenido):
    # Revisar el nombre y el tamaño
    if not nombre or "/" in nombre or "\\" in nombre:
        return False, "Nombre no permitido"
    tipo = os.path.splitext(nombre.lower())[1]
    if tipo not in (".csv", ".json", ".xlsx"):
        return False, "Formato no permitido"
    if not contenido:
        return False, "Archivo vacío"
    if len(contenido) > LIMITE:
        return False, "Supera los 10 MB"

    try:
        if tipo == ".json":
            datos = json.loads(contenido.decode("utf-8-sig"))
            if not isinstance(datos, (dict, list)) or not datos:
                return False, "JSON sin datos"

        elif tipo == ".csv":
            if b"\x00" in contenido:
                return False, "CSV inválido"
            filas = list(csv.reader(io.StringIO(contenido.decode("utf-8-sig")), strict=True))
            if len(filas) < 2 or len(filas[0]) < 2:
                return False, "CSV sin datos"
            for fila in filas:
                if len(fila) != len(filas[0]):
                    return False, "CSV con columnas diferentes"
            if not all(c.strip() for c in filas[0]):
                return False, "CSV sin encabezados"
            if not any(c.strip() for fila in filas[1:] for c in fila):
                return False, "CSV sin datos"

        else:  # Excel
            with zipfile.ZipFile(io.BytesIO(contenido)) as comprimido:
                tamaño = sum(f.file_size for f in comprimido.infolist())
                if tamaño > 50 * 1024 * 1024:
                    return False, "Excel demasiado grande por dentro"
            libro = load_workbook(io.BytesIO(contenido), read_only=True, data_only=True)
            try:
                for hoja in libro:
                    for fila in hoja.values:
                        if any(celda is not None for celda in fila):
                            return True, "Archivo válido"
                return False, "Excel sin datos"
            finally:
                libro.close()

        return True, "Archivo válido"
    except Exception as error:
        log.warning("Error al validar: %s", error)
        return False, "Contenido inválido"


def cargar_archivo(nombre, contenido):
    correcto, mensaje = validar_archivo(nombre, contenido)
    if not correcto:
        log.warning("Rechazado: %s", mensaje)
        return False, mensaje

    # Mismo contenido = mismo código, aunque cambie el nombre
    codigo = hashlib.sha256(contenido).hexdigest()
    tipo = os.path.splitext(nombre.lower())[1]
    try:
        os.makedirs(CARPETA, exist_ok=True)
        for guardado in os.listdir(CARPETA):
            if guardado.startswith(codigo + "."):
                return False, "Archivo repetido"

        ruta = os.path.join(CARPETA, codigo + tipo)
        with open(ruta, "xb") as archivo:  # No sobrescribir
            archivo.write(contenido)
        log.info("Archivo guardado")
        return True, "Archivo guardado correctamente"
    except FileExistsError:
        return False, "Archivo repetido"
    except OSError as error:
        log.error("Error al guardar: %s", error)
        return False, "Error al guardar"


def probar():
    # Comprobaciones con archivos de ejemplo
    import tempfile
    from openpyxl import Workbook

    global CARPETA
    original = CARPETA
    try:
        with tempfile.TemporaryDirectory() as carpeta:
            CARPETA = carpeta
            assert validar_archivo("ok.csv", b"a,b\n1,2\n")[0]
            assert validar_archivo("ok.json", b'{"a": 1}')[0]
            assert not validar_archivo("mal.json", b"{")[0]
            assert not validar_archivo("vacio.json", b"")[0]
            assert not validar_archivo("mal.csv", b"a,b\n1\n")[0]
            assert not validar_archivo("grande.csv", b"x" * (LIMITE + 1))[0]
            assert not validar_archivo("falso.xlsx", b"texto")[0]
            libro = Workbook()
            libro.active["A1"] = "Dato"
            memoria = io.BytesIO()
            libro.save(memoria)
            libro.close()
            assert validar_archivo("ok.xlsx", memoria.getvalue())[0]
            assert cargar_archivo("original.csv", b"a,b\n1,2\n")[0]
            assert not cargar_archivo("copia.csv", b"a,b\n1,2\n")[0]
        print("10 comprobaciones correctas")
    finally:
        CARPETA = original


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if "--probar" in sys.argv:
        probar()

    elif "--api" in sys.argv:
        # API HTTP: recibe archivos de otros programas
        from flask import Flask, request, jsonify
        app = Flask(__name__)
        app.config["MAX_CONTENT_LENGTH"] = LIMITE + 1024 * 1024

        @app.route("/api/archivos", methods=["POST"])
        def subir():
            clave = os.getenv("API_KEY")
            if not clave or request.headers.get("X-API-Key") != clave:
                return jsonify(mensaje="Clave incorrecta"), 401
            archivo = request.files.get("archivo")
            if archivo is None:
                return jsonify(mensaje="Falta un archivo"), 400
            correcto, mensaje = cargar_archivo(archivo.filename, archivo.read(LIMITE + 1))
            codigo = 201 if correcto else 400
            if mensaje == "Archivo repetido":
                codigo = 409
            if mensaje == "Supera los 10 MB":
                codigo = 413
            return jsonify(correcto=correcto, mensaje=mensaje), codigo

        app.run(port=5002)

    else:
        # Pantalla para probar sin abrir el Dashboard completo
        import streamlit as st
        st.title("Carga de archivos")
        archivo = st.file_uploader("Selecciona CSV, JSON o Excel", type=["csv", "json", "xlsx"])
        if archivo is not None and st.button("Subir archivo"):
            correcto, mensaje = cargar_archivo(archivo.name, archivo.getvalue())
            if correcto:
                st.success(mensaje)
            else:
                st.error(mensaje)
