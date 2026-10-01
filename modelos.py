"""
Modelos - Libreria Cleaner - Proyecto Extratron
Responsable: Alejandra Buelna

Aqui definimos la "forma" que deben tener los datos que entran y salen
del Cleaner, igual que hizo Ximena con UrlsRecibidas en el Collector.
FastAPI (y nosotros mismos) usamos estas clases para validar
automaticamente que el JSON que llega tiene los campos correctos.

Contrato de ENTRADA (lo que nos manda el Collector/Extractor, por fuente):
{
  "fuente": "vigia",
  "noticias": [
    {"url": "https://vigia.net/nota1", "html": "<div>...</div>"}
  ]
}

Contrato de SALIDA (lo que nosotros entregamos, siguiendo el formato
oficial definido en el documento del proyecto: source, url, retrieved_at, text):
{
  "source": "vigia",
  "url": "https://vigia.net/nota1",
  "retrieved_at": "2026-09-22T10:00:00+00:00",
  "text": "Texto limpio de la pagina..."
}
"""

from typing import List

from pydantic import BaseModel, HttpUrl


class NoticiaCruda(BaseModel):
    """Una noticia tal como llega, con su HTML sin procesar."""
    url: HttpUrl
    html: str


class LoteCrudo(BaseModel):
    """Un lote de noticias de UNA sola fuente (ej. 'vigia', 'facebook')."""
    fuente: str
    noticias: List[NoticiaCruda]


class NoticiaLimpia(BaseModel):
    """
    Una noticia ya limpia, en el formato de contrato oficial del proyecto
    (Cleaner -> Extractor): source, url, retrieved_at, text.
    """
    source: str
    url: HttpUrl
    retrieved_at: str
    text: str


class ResultadoLimpieza(BaseModel):
    """Resultado de limpiar un lote completo de una fuente."""
    fuente: str
    total_noticias: int
    noticias: List[NoticiaLimpia]