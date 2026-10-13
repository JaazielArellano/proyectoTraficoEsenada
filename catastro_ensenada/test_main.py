"""Pruebas de la API de Catastro de Ensenada."""

from fastapi.testclient import TestClient
from main import app, VIALIDADES, normalizar

cliente = TestClient(app)


# Verificar que exista una vialidad del CSV
def test_calle_existente():
    assert len(VIALIDADES) > 0

    calle = next(iter(VIALIDADES))

    respuesta = cliente.get("/buscar", params={"nombre": calle})

    assert respuesta.status_code == 200
    assert respuesta.json() == {"existe": True}


# Verificar una vialidad inexistente
def test_calle_inexistente():
    respuesta = cliente.get(
        "/buscar",
        params={"nombre": "CALLE_INEXISTENTE_XYZ_999"}
    )

    assert respuesta.status_code == 200
    assert respuesta.json() == {"existe": False}


# Verificar que no se acepten búsquedas vacías
def test_entrada_vacia():
    respuesta = cliente.get("/buscar", params={"nombre": ""})

    assert respuesta.status_code == 422


# Verificar el límite de caracteres
def test_entrada_muy_larga():
    respuesta = cliente.get(
        "/buscar",
        params={"nombre": "A" * 151}
    )

    assert respuesta.status_code == 422