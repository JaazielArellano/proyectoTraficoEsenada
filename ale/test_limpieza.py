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


# ---------- Pruebas agregadas tras detectar texto vacio en paginas reales ----------

def test_pagina_envuelta_en_form_no_queda_vacia():
    # Muchas paginas (ASP.NET) meten TODO el contenido dentro de un <form>
    html = "<html><body><form runat='server'><h1>Titulo</h1><p>Texto de la nota.</p></form></body></html>"
    assert limpiar_html(html) == "Titulo Texto de la nota."


def test_conserva_titulo_que_esta_en_header():
    html = "<body><header><h1>Titulo</h1></header><article><p>Texto</p></article></body>"
    resultado = limpiar_html(html)
    assert "Titulo" in resultado and "Texto" in resultado


def test_article_largo_ignora_menu_lateral():
    html = "<body><aside>Noticias relacionadas</aside><article>" + "Texto de la nota. " * 20 + "</article></body>"
    resultado = limpiar_html(html)
    assert "Noticias relacionadas" not in resultado
    assert "Texto de la nota." in resultado


def test_pagina_con_javascript_usa_metadatos():
    html = ("<html><head><meta property='og:title' content='Choque en Reforma'>"
            "<meta property='og:description' content='Dos heridos.'></head>"
            "<body><div id='app'></div><script src='a.js'></script></body></html>")
    assert limpiar_html(html) == "Choque en Reforma Dos heridos."


def test_pagina_sin_nada_regresa_vacio():
    assert limpiar_html("<body><div id='app'></div><script src='a.js'></script></body>") == ""
