from typing import List

from pydantic import BaseModel, HttpUrl


class NoticiaCruda(BaseModel):
    url: HttpUrl
    html: str


class LoteCrudo(BaseModel):
    fuente: str
    noticias: List[NoticiaCruda]


class NoticiaLimpia(BaseModel):
    source: str
    url: HttpUrl
    retrieved_at: str
    text: str


class ResultadoLimpieza(BaseModel):
    fuente: str
    total_noticias: int
    noticias: List[NoticiaLimpia]
