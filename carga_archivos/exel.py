# ==================================================
#  CARGA DE ARCHIVOS (mi parte del Dashboard)
#
#  ¿Qué hace?
#   1. Recibe un archivo (CSV, JSON o Excel)
#   2. Revisa que esté bien
#   3. Saca cada fila del archivo
#   4. Manda cada fila a una tabla de la base de datos
#
#  ¿Cómo se usa?
#   Solo dale al botón ▶ de VS Code.
#   Se prenden 2 cosas al mismo tiempo:
#   - La pantalla: se abre sola en el navegador
#   - La API:      http://TU-IP:5050/api/archivos
#                  (tu IP sale escribiendo ipconfig en la terminal)
#   Para apagar todo: Ctrl + C en la terminal
# ==================================================

import io
import csv
import json
import sys
import subprocess

# --------------------------------------------------
# 0. INSTALAR LO QUE FALTE (solo pasa la primera vez)
# --------------------------------------------------
for paquete in ["requests", "openpyxl", "flask", "streamlit"]:
    try:
        __import__(paquete)
    except ImportError:
        print("Instalando " + paquete + "... (espera)")
        subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])

import requests
from openpyxl import load_workbook


# --------------------------------------------------
# 1. DATOS QUE PUEDES CAMBIAR
# --------------------------------------------------

# Dirección de la base de datos (al final se le pega el nombre de la tabla)
BASE_DE_DATOS = "http://148.231.239.96:4002/api/datos/"

# Tabla que se usa si no escriben otra
TABLA = "archivos"

# Clave para poder usar nuestra API (cámbiala)
CLAVE = "miclave"

# Puertos (si alguno está ocupado, cambia el número)
PUERTO_PANTALLA = 8600
PUERTO_API = 5050

# Tamaño máximo permitido: 10 MB
TAMANO_MAXIMO = 10 * 1024 * 1024

# Tipos de archivo que sí aceptamos
TIPOS_PERMITIDOS = [".csv", ".json", ".xlsx"]


# --------------------------------------------------
# 2. SACAR EL TIPO DEL ARCHIVO
#    Ejemplo: "ventas.CSV"  ->  ".csv"
# --------------------------------------------------
def sacar_tipo(nombre):
    if "." not in nombre:
        return ""
    return "." + nombre.split(".")[-1].lower()


# --------------------------------------------------
# 3. SACAR LAS FILAS DEL ARCHIVO
#    Regresa una lista así:
#    [ {"nombre": "Ana", "edad": 20},
#      {"nombre": "Luis", "edad": 22} ]
# --------------------------------------------------
def sacar_filas(nombre, contenido):
    tipo = sacar_tipo(nombre)
    filas = []

    if tipo == ".csv":
        texto = contenido.decode("utf-8-sig")
        for fila in csv.DictReader(io.StringIO(texto)):
            filas.append(dict(fila))

    if tipo == ".json":
        datos = json.loads(contenido)
        if isinstance(datos, dict):   # un solo registro
            datos = [datos]
        for fila in datos:
            if isinstance(fila, dict):
                filas.append(fila)

    if tipo == ".xlsx":
        libro = load_workbook(io.BytesIO(contenido), read_only=True, data_only=True)
        hoja = libro.active
        todas = list(hoja.values)
        libro.close()
        if todas:
            encabezados = todas[0]            # la primera fila son los títulos
            for valores in todas[1:]:
                if any(v is not None for v in valores):   # saltar filas vacías
                    fila = {}
                    for titulo, valor in zip(encabezados, valores):
                        if titulo is not None:
                            fila[str(titulo)] = valor
                    filas.append(fila)

    # Las fechas y cosas raras se convierten a texto
    for fila in filas:
        for llave in fila:
            if not isinstance(fila[llave], (str, int, float, bool, type(None))):
                fila[llave] = str(fila[llave])

    return filas


# --------------------------------------------------
# 4. REVISAR QUE EL ARCHIVO ESTÉ BIEN
#    Regresa: (True o False, mensaje, filas)
# --------------------------------------------------
def revisar_archivo(nombre, contenido):
    tipo = sacar_tipo(nombre)

    if tipo not in TIPOS_PERMITIDOS:
        return False, "Solo se aceptan archivos CSV, JSON o Excel", []

    if len(contenido) == 0:
        return False, "El archivo está vacío", []

    if len(contenido) > TAMANO_MAXIMO:
        return False, "El archivo pesa más de 10 MB", []

    try:
        filas = sacar_filas(nombre, contenido)
    except Exception:
        return False, "El archivo está dañado o no se puede leer", []

    if len(filas) == 0:
        return False, "El archivo no tiene filas con datos", []

    return True, "El archivo está bien", filas


# --------------------------------------------------
# 5. MANDAR LAS FILAS A LA BASE DE DATOS
#    Cada fila se manda así: {"datos": {"nombre": "Ana", "edad": 20}}
# --------------------------------------------------
def guardar_en_base_de_datos(tabla, filas):
    direccion = BASE_DE_DATOS + tabla
    guardadas = 0

    for numero, fila in enumerate(filas, start=1):
        try:
            respuesta = requests.post(direccion, json={"datos": fila}, timeout=10)
        except requests.RequestException as error:
            return False, (
                "No se pudo conectar con la base de datos.\n\n"
                "Dirección: " + direccion + "\n\n"
                "Error: " + str(error)
            )

        if respuesta.status_code in (200, 201):
            guardadas += 1
        else:
            # Se detiene en la primera fila que falle y dice por qué
            return False, (
                "Se guardaron " + str(guardadas) + " filas, pero la fila "
                + str(numero) + " falló (código " + str(respuesta.status_code)
                + "): " + respuesta.text[:300]
            )

    return True, "Se guardaron " + str(guardadas) + " filas en la tabla " + tabla


# --------------------------------------------------
# 6. SUBIR UN ARCHIVO = REVISAR + GUARDAR
# --------------------------------------------------
def subir_archivo(nombre, contenido, tabla):
    esta_bien, mensaje, filas = revisar_archivo(nombre, contenido)
    if not esta_bien:
        return False, mensaje
    return guardar_en_base_de_datos(tabla, filas)


# --------------------------------------------------
# 7. NUESTRA API (para que otros programas suban archivos)
#    Dirección: http://TU-IP:5050/api/archivos
#    Se manda: el archivo en "archivo" y (opcional) la tabla en "tabla"
# --------------------------------------------------
def iniciar_api():
    from flask import Flask, request

    app = Flask(__name__)

    # No dejar que manden cosas de más de 11 MB
    app.config["MAX_CONTENT_LENGTH"] = TAMANO_MAXIMO + 1024 * 1024

    @app.route("/api/archivos", methods=["POST"])
    def recibir_archivo():
        # ¿Trae la clave correcta?
        if request.headers.get("X-API-Key") != CLAVE:
            return {"mensaje": "Clave incorrecta"}, 401

        # ¿Sí mandó un archivo?
        if "archivo" not in request.files:
            return {"mensaje": "No mandaste ningún archivo"}, 400

        archivo = request.files["archivo"]
        tabla = request.form.get("tabla", TABLA)

        salio_bien, mensaje = subir_archivo(archivo.filename, archivo.read(), tabla)

        if salio_bien:
            return {"mensaje": mensaje}, 201
        return {"mensaje": mensaje}, 400

    # host="0.0.0.0" deja que otras computadoras de la red la usen
    app.run(host="0.0.0.0", port=PUERTO_API)


# --------------------------------------------------
# 8. PANTALLA (para probar con botones)
# --------------------------------------------------
def mostrar_pantalla():
    import streamlit as st

    st.title("Carga de archivos")
    tabla = st.text_input("Nombre de la tabla en la base de datos", TABLA)
    archivo = st.file_uploader("Elige un archivo CSV, JSON o Excel", type=["csv", "json", "xlsx"])

    if archivo is not None and st.button("Subir archivo"):
        with st.spinner("Mandando a la base de datos..."):
            salio_bien, mensaje = subir_archivo(archivo.name, archivo.getvalue(), tabla.strip())
        if salio_bien:
            st.success(mensaje)
        else:
            st.error(mensaje)


# --------------------------------------------------
# 9. PRENDER TODO
# --------------------------------------------------
from streamlit import runtime

if runtime.exists():
    # Streamlit está abriendo este archivo: mostrar la pantalla
    mostrar_pantalla()
else:
    # Lo abriste con el botón ▶:
    import time
    import webbrowser

    # 1) Prender la pantalla sin que Streamlit haga preguntas
    subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", __file__,
        "--server.headless", "true",
        "--server.port", str(PUERTO_PANTALLA),
        "--browser.gatherUsageStats", "false",
    ])

    # 2) Esperar 5 segundos a que cargue y abrirla en el navegador
    time.sleep(5)
    webbrowser.open("http://localhost:" + str(PUERTO_PANTALLA))

    # 3) Prender la API
    iniciar_api()

            
