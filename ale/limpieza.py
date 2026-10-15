"""
limpieza.py - Libreria Cleaner - Proyecto Extratron
Responsable: Alejandra Buelna

Esta libreria tiene UNA sola tarea: convertir HTML crudo (tal como lo
descarga el Collector) en texto limpio y legible, siguiendo el contrato
de salida oficial del proyecto: source, url, retrieved_at, text.

A proposito, estas funciones NO dependen de FastAPI ni de ningun
framework: son funciones puras de Python. Esto es lo que el profe pidio
como "libreria" -- se pueden importar y probar por separado (con pytest,
por ejemplo), sin necesidad de levantar ningun servidor. La API
(api_cleaner.py) solo es una capa delgada que usa estas funciones.

Requisitos (instalar una vez en la terminal):
    pip install beautifulsoup4 lxml ftfy

Como usarla directamente (sin API), desde otro script:
    from cleaner_lib.limpieza import limpiar_html, limpiar_lote
    texto = limpiar_html("<p>Hola <b>mundo</b></p>")
"""

import re
from datetime import datetime, timezone
from typing import List

import ftfy
from bs4 import BeautifulSoup

from .modelos import LoteCrudo, NoticiaCruda, NoticiaLimpia

# ---------- 1. Configuracion de la limpieza ----------

# Etiquetas que nunca son contenido de la noticia (codigo, navegacion, adornos).
# OJO: "form", "header" y "aside" NO estan aqui a proposito. Muchas paginas
# (sobre todo ASP.NET) envuelven TODO su contenido dentro de un <form>, y
# muchos sitios ponen el titulo de la nota dentro de un <header>. Quitarlos
# dejaba el texto vacio.
ETIQUETAS_A_QUITAR = [
    "script", "style", "noscript", "template", "nav", "footer",
    "iframe", "svg", "button", "select", "option",
]

# Si el contenedor principal (<article>/<main>) trae menos caracteres que
# esto, se considera que no es la nota completa y se usa todo el <body>.
MIN_CARACTERES_ARTICULO = 200


# ---------- 2. Funcion principal: HTML crudo -> texto limpio ----------

def _texto(nodo) -> str:
    texto = nodo.get_text(separator=" ", strip=True)
    return re.sub(r"\s+", " ", texto).strip()


def _texto_de_metadatos(soup) -> str:
    """
    Plan B para paginas cuyo contenido carga con JavaScript (o redes como
    Facebook): el HTML estatico casi siempre trae titulo y descripcion en
    <title> y en las etiquetas <meta> (og:title, og:description).
    """
    partes = []
    for clave in ("og:title", "og:description", "description"):
        meta = soup.find("meta", attrs={"property": clave}) or soup.find(
            "meta", attrs={"name": clave}
        )
        if meta and meta.get("content"):
            partes.append(meta["content"].strip())
    if not partes and soup.title and soup.title.string:
        partes.append(soup.title.string.strip())
    # quitar repetidos conservando el orden
    unicos = list(dict.fromkeys(partes))
    return re.sub(r"\s+", " ", " ".join(unicos)).strip()


def limpiar_html(html_crudo: str) -> str:
    """
    Convierte HTML crudo en texto legible y normalizado.

    Pasos:
      1. Corrige errores de codificacion (tildes/ñ mal codificadas) con ftfy.
      2. Parsea el HTML con lxml (tolera HTML mal formado).
      3. Quita codigo y elementos que no son contenido (script, nav, footer...).
      4. Si hay <article> o <main>, toma el texto de ahi (evita menus laterales);
         si es muy corto, usa todo el <body>.
      5. Si no hay texto en el cuerpo (pagina hecha con JavaScript), usa como
         plan B el titulo y la descripcion de las etiquetas <meta>.
      6. Colapsa espacios y saltos de linea sobrantes.

    Regresa "" solo si la pagina de verdad no trae texto.
    """
    if not html_crudo or not html_crudo.strip():
        return ""

    html_arreglado = ftfy.fix_text(html_crudo)
    soup = BeautifulSoup(html_arreglado, "lxml")

    # Los metadatos se leen ANTES de borrar nada
    metadatos = _texto_de_metadatos(soup)

    for etiqueta in soup(ETIQUETAS_A_QUITAR):
        etiqueta.decompose()

    cuerpo = soup.body or soup
    principal = soup.find("article") or soup.find("main")

    texto = _texto(principal) if principal else ""
    if len(texto) < MIN_CARACTERES_ARTICULO:
        texto_cuerpo = _texto(cuerpo)
        if len(texto_cuerpo) > len(texto):
            texto = texto_cuerpo

    if not texto:
        texto = metadatos

    return texto


# ---------- 3. Funciones que arman el contrato oficial de salida ----------

def _ahora_iso() -> str:
    """Fecha/hora actual en formato ISO 8601 con zona horaria (UTC)."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def limpiar_noticia(noticia: NoticiaCruda, fuente: str) -> NoticiaLimpia:
    """Limpia UNA noticia y la entrega ya en el formato de contrato oficial."""
    texto = limpiar_html(noticia.html)
    return NoticiaLimpia(
        source=fuente,
        url=noticia.url,
        retrieved_at=_ahora_iso(),
        text=texto,
    )


def limpiar_lote(lote: LoteCrudo) -> List[NoticiaLimpia]:
    """Limpia todas las noticias de un lote (una sola fuente, ej. 'vigia')."""
    return [limpiar_noticia(noticia, lote.fuente) for noticia in lote.noticias]
