"""API para consultar noticias de Ensenada."""

import json

from flask import Flask, jsonify

app = Flask(__name__)



@app.route("/noticias")
def noticias():

    """Obtiene las noticias desde el archivo JSON."""
    with open("noticias_pruebas.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    return jsonify(datos)

if __name__ == "__main__":
    app.run()
