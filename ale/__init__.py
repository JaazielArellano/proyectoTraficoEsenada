"""
cleaner_lib - Libreria del modulo Cleaner - Proyecto Extratron
Responsable: Alejandra Buelna

Este paquete agrupa toda la logica de limpieza de HTML del proyecto
Extratron. Se puede importar directamente sin necesidad de la API:

    from cleaner_lib import limpiar_html, limpiar_noticia, limpiar_lote

Contenido:
    - modelos.py  -> Contratos de datos (Pydantic): NoticiaCruda, LoteCrudo,
                      NoticiaLimpia, ResultadoLimpieza.
    - limpieza.py -> Funciones puras de limpieza (sin FastAPI, sin red).
    - api_cleaner.py -> API que expone la libreria por HTTP, para que el
                         Collector/Extractor nos manden sus JSON y reciban
                         de vuelta el texto limpio.
"""

from .limpieza import limpiar_html, limpiar_lote, limpiar_noticia
from .modelos import LoteCrudo, NoticiaCruda, NoticiaLimpia, ResultadoLimpieza

__all__ = [
    "limpiar_html",
    "limpiar_noticia",
    "limpiar_lote",
    "NoticiaCruda",
    "LoteCrudo",
    "NoticiaLimpia",
    "ResultadoLimpieza",
]