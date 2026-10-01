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

# Etiquetas que nunca deben aparecer en el texto final: no son contenido
# real de la noticia, son navegacion, anuncios o codigo.
ETIQUETAS_A_QUITAR = ["script", "style", "nav", "footer", "header", "aside", "iframe", "form"]


# ---------- 2. Funcion principal: HTML crudo -> texto limpio ----------

def limpiar_html(html_crudo: str) -> str:
    """
    Convierte un fragmento de HTML crudo en texto legible y normalizado.

    Pasos:
      1. Corrige errores de codificacion (tildes/ñ mal codificadas) con ftfy.
      2. Parsea el HTML con lxml (tolera HTML mal formado).
      3. Elimina nodos que no son contenido real (script, nav, footer, etc.).
      4. Extrae el texto y colapsa espacios/saltos de linea sobrantes.
    """
    if not html_crudo or not html_crudo.strip():
        return ""

    html_arreglado = ftfy.fix_text(html_crudo)
    soup = BeautifulSoup(html_arreglado, "lxml")

    for etiqueta in soup(ETIQUETAS_A_QUITAR):
        etiqueta.decompose()

    texto = soup.get_text(separator=" ", strip=True)
    texto = re.sub(r"\s+", " ", texto).strip()
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