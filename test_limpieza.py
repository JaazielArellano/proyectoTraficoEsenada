"""
test_limpieza.py - Pruebas de la libreria Cleaner
Responsable: Alejandra Buelna

Como correrlas:
    pip install pytest
    pytest test_limpieza.py -v
"""

from cleaner_lib.limpieza import limpiar_html, limpiar_lote
from cleaner_lib.modelos import LoteCrudo, NoticiaCruda


def test_quita_etiquetas_script_y_footer():
    html = "<div><p>Nota real</p><script>trackClick()</script><footer>Compartir</footer></div>"
    resultado = limpiar_html(html)
    assert "trackClick" not in resultado
    assert "Compartir" not in resultado
    assert "Nota real" in resultado


def test_corrige_codificacion_mal_hecha():
    html = "<p>Se registrÃ³ un accidente</p>"
    resultado = limpiar_html(html)
    assert "registró" in resultado


def test_colapsa_espacios_y_saltos_de_linea():
    html = "<p>Hola     \n\n   mundo</p>"
    resultado = limpiar_html(html)
    assert resultado == "Hola mundo"


def test_html_vacio_regresa_texto_vacio():
    assert limpiar_html("") == ""
    assert limpiar_html("   ") == ""


def test_limpiar_lote_arma_contrato_oficial():
    lote = LoteCrudo(
        fuente="vigia",
        noticias=[
            NoticiaCruda(url="https://vigia.net/nota1", html="<p>Texto de prueba</p>"),
        ],
    )
    resultado = limpiar_lote(lote)
    assert len(resultado) == 1
    noticia = resultado[0]
    assert noticia.source == "vigia"
    assert str(noticia.url) == "https://vigia.net/nota1"
    assert noticia.text == "Texto de prueba"
    assert noticia.retrieved_at  # debe traer una fecha/hora, no estar vacio