import json

import pytest

from cleaner_lib.limpieza import (
    limpiar_archivo, limpiar_html, limpiar_lote, limpiar_registro, limpiar_registros,
)
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
    assert noticia.retrieved_at


def test_pagina_envuelta_en_form_no_queda_vacia():
    html = "<html><body><form runat='server'><h1>Titulo</h1><p>Texto de la nota.</p></form></body></html>"
    assert limpiar_html(html) == "Titulo\n\nTexto de la nota."


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


def test_quita_comentarios_html():
    assert "oculto" not in limpiar_html("<p>Hola</p><!-- comentario oculto --><p>mundo</p>")


def test_quita_css_js_y_atributos_de_formato():
    html = ("<html><head><style>p{color:red}</style></head><body>"
            "<p style='color:red' class='x' onclick='robar()'>Texto</p>"
            "<script>alert(1)</script><noscript>Activa JS</noscript></body></html>")
    resultado = limpiar_html(html)
    assert resultado == "Texto"


def test_parrafos_quedan_separados():
    assert limpiar_html("<p>Primero.</p><p>Segundo.</p>") == "Primero.\n\nSegundo."


def test_listas_conservan_elementos_en_lineas():
    assert limpiar_html("<ul><li>Uno</li><li>Dos</li></ul>") == "- Uno\n- Dos"


def test_sublistas_no_dejan_lineas_en_blanco():
    assert limpiar_html("<ul><li>A<ul><li>A1</li></ul></li><li>B</li></ul>") == "- A\n- A1\n- B"


def test_tabla_de_datos_conserva_filas_y_columnas():
    html = ("<table><tr><th>Calle</th><th>Colonia</th></tr>"
            "<tr><td>Reforma</td><td>Centro</td></tr></table>")
    assert limpiar_html(html) == "Calle | Colonia\nReforma | Centro"


def test_tabla_de_maquetacion_no_se_aplasta():
    html = "<table><tr><td><p>Titulo</p><p>Cuerpo de la nota.</p></td><td><div>Anuncio</div></td></tr></table>"
    resultado = limpiar_html(html)
    assert "Titulo\n\nCuerpo de la nota." in resultado
    assert "|" not in resultado


def test_etiqueta_inline_no_parte_palabras():
    assert limpiar_html("<p>El <b>mar</b>tes pasado</p>") == "El martes pasado"


def test_espacio_duro_y_caracteres_invisibles():
    assert limpiar_html("<p>Hola\u00a0\u00a0mundo\u200b feliz</p>") == "Hola mundo feliz"


def test_entidades_html_se_convierten():
    assert limpiar_html("<p>Ni&ntilde;os &amp; ni&ntilde;as &aacute;gil</p>") == "Niños & niñas ágil"


def test_unicode_se_normaliza_a_nfc():
    assert limpiar_html("<p>cafe\u0301</p>") == "caf\u00e9"


def test_mojibake_se_repara():
    assert limpiar_html("<p>informaciÃ³n del dÃ­a</p>") == "información del día"


def test_html_sin_cerrar_etiquetas():
    resultado = limpiar_html("<div><p>Texto sin cerrar <b>negrita<p>otro <i>parrafo</div>")
    assert "Texto sin cerrar negrita" in resultado and "otro parrafo" in resultado


def test_etiquetas_en_mayusculas_y_atributos_raros():
    resultado = limpiar_html("<P CLASS=a>Hola</P><SCRIPT>x()</SCRIPT><BR>Adios")
    assert "x()" not in resultado and "Hola" in resultado and "Adios" in resultado


def test_fragmento_sin_html_ni_body():
    assert limpiar_html("Solo texto <b>plano</b>") == "Solo texto plano"


def test_html_muy_anidado_no_truena():
    html = "<div>" * 300 + "Fondo" + "</div>" * 300
    assert limpiar_html(html) == "Fondo"


def test_basura_no_html_no_truena():
    assert isinstance(limpiar_html("<<<>>> &&& <a href=>>"), str)


CONTRATO = {"source", "url", "retrieved_at", "text"}


def test_registro_sale_con_el_contrato_exacto():
    salida = limpiar_registro({"url": "https://vigia.net/n1", "html": "<p>Hola</p>"})
    assert set(salida) == CONTRATO
    assert salida["text"] == "Hola"


def test_conserva_retrieved_at_y_fuente_del_collector():
    salida = limpiar_registro({
        "source": "vigia", "url": "https://vigia.net/n1",
        "retrieved_at": "2026-10-01T02:24:16+00:00", "html": "<p>Hola</p>",
        "campo_extra_del_collector": 123,
    })
    assert salida["source"] == "vigia"
    assert salida["retrieved_at"] == "2026-10-01T02:24:16+00:00"
    assert "campo_extra_del_collector" not in salida


def test_acepta_otros_nombres_de_llave_para_el_html():
    for llave in ("html", "raw_html", "content", "contenido"):
        assert limpiar_registro({"url": "https://a.com/x", llave: "<p>Hola</p>"})["text"] == "Hola"


def test_deduce_la_fuente_del_dominio():
    assert limpiar_registro({"url": "https://www.ensenada.net/n?id=1", "html": "<p>x</p>"})["source"] == "ensenada_net"


def test_registro_sin_html_da_error_claro():
    with pytest.raises(ValueError, match="no trae HTML"):
        limpiar_registro({"url": "https://a.com/x"})


def test_un_registro_malo_no_detiene_a_los_demas():
    limpios, errores = limpiar_registros([
        {"url": "https://a.com/1", "html": "<p>Bien</p>"},
        {"url": "https://a.com/2"},
        {"url": "https://a.com/3", "html": "<div id='app'></div>"},
    ])
    assert len(limpios) == 1 and len(errores) == 2


def test_limpiar_archivo_consolida_una_carpeta(tmp_path):
    (tmp_path / "a.json").write_text(json.dumps({"url": "https://a.com/1", "html": "<p>Uno</p>"}), encoding="utf-8")
    (tmp_path / "b.json").write_text(json.dumps([{"url": "https://b.com/2", "html": "<p>Dos</p>"}]), encoding="utf-8")
    (tmp_path / "c.json").write_text(json.dumps({"fuente": "vigia", "noticias": [{"url": "https://v.com/3", "html": "<p>Tres</p>"}]}), encoding="utf-8")
    (tmp_path / "roto.json").write_text("{esto no es json", encoding="utf-8")

    salida = tmp_path / "salida.json"
    errores = tmp_path / "errores.json"
    resumen = limpiar_archivo(str(tmp_path), str(salida), str(errores))

    datos = json.loads(salida.read_text(encoding="utf-8"))
    assert resumen["limpios"] == 3 and resumen["errores"] == 1
    assert datos["total"] == 3
    assert all(set(n) == CONTRATO for n in datos["noticias"])
    assert {n["source"] for n in datos["noticias"]} == {"a_com", "b_com", "vigia"}


import html as _html

API = {
    "status": "ok",
    "data": {
        "id": "a1b2c3d4e5f6a7b8c9d0",
        "title": "Choque en Reforma",
        "colonia": "Centro",
        "publicado": "2026-10-01T02:24:16Z",
        "url": "https://ensenada.net/n/1",
        "tags": ["choque", "reforma"],
        "body": "<p>Un choque ocurri&oacute; ayer.</p><ul><li>Dos heridos</li></ul>",
    },
}


def _sin_basura_de_json(texto):
    return not any(x in texto for x in ('{', '}', '":', 'a1b2c3d4', 'https://', '<p>', '&oacute;'))


def test_respuesta_json_pura_se_convierte_en_texto():
    texto = limpiar_html(json.dumps(API))
    assert _sin_basura_de_json(texto)
    assert "Choque en Reforma" in texto and "Un choque ocurrió ayer." in texto and "- Dos heridos" in texto
    assert "colonia: Centro" in texto and "2026-10-01T02:24:16Z" in texto


def test_json_escapado_dentro_de_pre_se_convierte_en_texto():
    pagina = "<html><body><pre>" + _html.escape(json.dumps(API, indent=2)) + "</pre></body></html>"
    texto = limpiar_html(pagina)
    assert _sin_basura_de_json(texto) and "Choque en Reforma" in texto


def test_json_en_una_linea_suelta_entre_parrafos():
    pagina = "<p>Intro.</p><p>" + _html.escape(json.dumps({"k": "Dato suelto importante"})) + "</p><p>Final.</p>"
    assert limpiar_html(pagina) == "Intro.\n\nDato suelto importante\n\nFinal."


def test_json_envuelto_dos_veces():
    assert "Choque en Reforma" in limpiar_html(json.dumps({"html": json.dumps(API)}))


def test_json_solo_con_ids_y_numeros_queda_vacio():
    assert limpiar_html('{"id":"a1b2c3d4e5f6a7b8c9d0","n":5,"ok":true}') == ""


def test_texto_normal_con_corchetes_no_se_toca():
    assert limpiar_html("<p>[VIDEO] Choque en Reforma</p>") == "[VIDEO] Choque en Reforma"


def test_registro_con_html_ya_como_diccionario():
    salida = limpiar_registro({"url": "https://a.com/1", "html": API})
    assert set(salida) == CONTRATO and _sin_basura_de_json(salida["text"])


def test_menu_y_pie_con_clases_no_ocultan_los_metadatos():
    html = (
        '<html><head><meta property="og:title" content="Patrulla 646 - Accidente en Reforma">'
        '<meta property="og:description" content="Un fuerte accidente con 2 personas lesionadas."></head>'
        '<body><div class="nav-menu">Inicio Explorar Suscripciones</div><div id="app"></div>'
        '<div class="footer-links">Acerca de Prensa Derechos de autor...</div></body></html>'
    )
    assert limpiar_html(html) == "Patrulla 646 - Accidente en Reforma Un fuerte accidente con 2 personas lesionadas."


def test_quita_ruido_por_class_id_role_y_camel_case():
    html = (
        "<body><div class='footerLinks'>Pie</div><div id='cookie-banner'>Cookies</div>"
        "<div role='navigation'>Menu raro</div><p>Nota importante del dia.</p></body>"
    )
    assert limpiar_html(html) == "Nota importante del dia."


def test_menu_sin_clase_reconocible_pierde_contra_metadatos_mas_largos():
    html = (
        '<head><meta property="og:description" content="Choque entre dos autos en Reforma con dos heridos."></head>'
        "<body><div class='x1'>Inicio Explorar</div></body>"
    )
    assert limpiar_html(html) == "Choque entre dos autos en Reforma con dos heridos."


def test_cuerpo_corto_pero_mas_largo_que_los_metadatos_se_conserva():
    html = (
        '<head><meta property="og:title" content="Choque"></head>'
        "<body><p>Un choque ocurrio ayer en Reforma y dejo dos heridos.</p></body>"
    )
    assert limpiar_html(html) == "Un choque ocurrio ayer en Reforma y dejo dos heridos."


def test_clase_de_ruido_en_body_no_borra_la_pagina():
    html = "<body class='menu-open nav-active'><p>Contenido de la nota.</p></body>"
    assert limpiar_html(html) == "Contenido de la nota."


def test_contenedor_con_article_no_se_borra_aunque_se_llame_menu():
    html = "<div class='menu-wrapper'><article><p>Texto de la nota.</p></article></div>"
    assert limpiar_html(html) == "Texto de la nota."


def test_contenedor_con_varios_parrafos_no_se_borra():
    html = "<div class='menu-content'><p>Uno.</p><p>Dos.</p><p>Tres.</p></div>"
    assert limpiar_html(html) == "Uno.\n\nDos.\n\nTres."


def test_titulo_en_header_de_articulo_se_conserva():
    html = "<body><div class='article-header'><h1>Titulo de la nota</h1></div><p>Cuerpo.</p></body>"
    assert "Titulo de la nota" in limpiar_html(html)
