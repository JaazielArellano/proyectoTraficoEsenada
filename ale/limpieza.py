import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

import ftfy
from bs4 import BeautifulSoup, Comment, NavigableString

from .modelos import LoteCrudo, NoticiaCruda, NoticiaLimpia

ETIQUETAS_A_QUITAR = [
    "script", "style", "noscript", "template", "nav", "footer",
    "iframe", "svg", "button", "select", "option",
]
PALABRAS_RUIDO = {
    "nav", "navbar", "navigation", "menu", "footer", "cookie", "cookies",
    "consent", "breadcrumb", "breadcrumbs", "sidebar",
}
ROLES_RUIDO = {"navigation", "contentinfo", "dialog"}
MIN_CARACTERES_ARTICULO = 200

BLOQUES_PARRAFO = [
    "p", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote",
    "ul", "ol", "dl", "table", "pre", "figure",
]
BLOQUES_LINEA = [
    "div", "section", "article", "main", "header", "aside", "form", "li",
    "dt", "dd", "figcaption", "address", "fieldset", "details", "summary",
    "tr", "td", "th",
]
BLOQUES_EN_CELDA = ["table", "p", "div", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "br"]

ESPACIOS_ESPECIALES = re.compile("[   -   　]")
INVISIBLES = re.compile("[­​-‏‪-‮⁠﻿]")
CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

# marca interna para que dos bloques pegados dejen un solo salto de linea
SALTO = ""
SALTOS_SUAVES = re.compile(r"[ \t]*" + SALTO + r"(?:[ \t]*" + SALTO + r")*[ \t]*")


def _normalizar_texto(texto: str) -> str:
    texto = unicodedata.normalize("NFC", texto)
    texto = ESPACIOS_ESPECIALES.sub(" ", texto)
    texto = INVISIBLES.sub("", texto)
    texto = CONTROL.sub("", texto)
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    lineas = [re.sub(r"[ \t]+", " ", linea).strip() for linea in texto.split("\n")]
    texto = re.sub(r"\n{3,}", "\n\n", "\n".join(lineas))
    return texto.strip()


def _palabras(valor) -> set:
    if isinstance(valor, (list, tuple)):
        valor = " ".join(valor)
    valor = re.sub(r"([a-z])([A-Z])", r"\1 \2", valor or "")
    return set(re.findall(r"[a-z]+", valor.lower()))


def _es_ruido(tag) -> bool:
    if tag.name in ("html", "body", "article", "main"):
        return False
    if tag.find(["article", "main"]) or len(tag.find_all("p")) >= 3:
        return False
    if _palabras(tag.get("class")) & PALABRAS_RUIDO or _palabras(tag.get("id")) & PALABRAS_RUIDO:
        return True
    return tag.get("role") in ROLES_RUIDO


def _quitar_ruido(soup) -> None:
    for etiqueta in soup(ETIQUETAS_A_QUITAR):
        etiqueta.decompose()
    for etiqueta in soup.find_all(True):
        if not etiqueta.decomposed and _es_ruido(etiqueta):
            etiqueta.decompose()


def _marcar_estructura(soup) -> None:
    for comentario in soup.find_all(string=lambda t: isinstance(t, Comment)):
        comentario.extract()

    for s in soup.find_all(string=True):
        if type(s) is NavigableString and s.find_parent("pre") is None:
            s.replace_with(re.sub(r"\s+", " ", str(s)))

    for fila in reversed(soup.find_all("tr")):
        celdas_tag = fila.find_all(["th", "td"], recursive=False)
        if any(c.find(BLOQUES_EN_CELDA) for c in celdas_tag):
            continue
        celdas = [" ".join(c.get_text("").split()) for c in celdas_tag]
        fila.replace_with(NavigableString(" | ".join(c for c in celdas if c) + "\n"))

    for li in soup.find_all("li"):
        li.insert(0, "- ")
    for br in soup.find_all("br"):
        br.replace_with("\n")
    for etiqueta in soup.find_all(BLOQUES_PARRAFO):
        sep = SALTO if etiqueta.name in ("ul", "ol", "dl") and etiqueta.find_parent("li") else "\n\n"
        etiqueta.insert_before(sep)
        etiqueta.insert_after(sep)
    for etiqueta in soup.find_all(BLOQUES_LINEA):
        etiqueta.insert_before(SALTO)
        etiqueta.insert_after(SALTO)


def _texto(nodo) -> str:
    texto = nodo.get_text("").replace(SALTO + SALTO, SALTO)
    return _normalizar_texto(SALTOS_SUAVES.sub("\n", texto))


def _texto_de_metadatos(soup) -> str:
    partes = []
    for clave in ("og:title", "og:description", "description"):
        meta = soup.find("meta", attrs={"property": clave}) or soup.find("meta", attrs={"name": clave})
        if meta and meta.get("content"):
            partes.append(meta["content"].strip())
    if not partes and soup.title and soup.title.string:
        partes.append(soup.title.string.strip())
    return _normalizar_texto(" ".join(dict.fromkeys(partes)))


CLAVES_TECNICAS = {
    "id", "uuid", "guid", "token", "csrf", "nonce", "class", "style", "type",
    "@type", "@context", "__typename", "hash", "sig", "signature", "version",
    "lang", "locale", "status", "success", "ok", "code",
}
URL = re.compile(r"^(https?://|www\.|//)\S+$", re.I)
ID = re.compile(r"^[A-Za-z0-9_\-=+/.:]{16,}$")
FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}(:\d{2})?(\.\d+)?(Z|[+-]\d{2}:?\d{2})?)?$")
CLAVE_LEGIBLE = re.compile(r"^[A-Za-zÀ-ÿ_ \-]{2,40}$")


def _con_clave(clave: str, valor: str) -> str:
    if clave and CLAVE_LEGIBLE.match(clave):
        return f"{clave.replace('_', ' ')}: {valor}"
    return valor


def _lineas_de_json(valor, clave: str = "", prof: int = 0) -> List[str]:
    if prof > 40:
        return []
    if isinstance(valor, dict):
        lineas: List[str] = []
        for k, v in valor.items():
            lineas += _lineas_de_json(v, str(k), prof + 1)
        return lineas
    if isinstance(valor, list):
        if valor and all(isinstance(v, str) and len(v.split()) == 1 for v in valor):
            palabras = [v.strip() for v in valor if v.strip() and not URL.match(v.strip())]
            return [_con_clave(clave, ", ".join(palabras))] if palabras else []
        lineas = []
        for v in valor:
            lineas += _lineas_de_json(v, clave, prof + 1)
        return lineas
    if not isinstance(valor, str):
        return []

    texto = valor.strip()
    if not texto or clave.lower() in CLAVES_TECNICAS:
        return []
    if "<" in texto and ">" in texto:
        limpio = limpiar_html(texto)
        return [limpio] if limpio else []
    if FECHA.match(texto):
        return [_con_clave(clave, texto)]
    if URL.match(texto) or ID.match(texto) or not re.search(r"[A-Za-zÀ-ÿ]", texto):
        return []
    if len(texto.split()) >= 2:
        return [texto]
    return [_con_clave(clave, texto)]


def _desde_json(objeto) -> str:
    lineas = _lineas_de_json(objeto)
    sin_repetir = [l for i, l in enumerate(lineas) if i == 0 or l != lineas[i - 1]]
    return _normalizar_texto("\n".join(sin_repetir))


def _texto_si_es_json(contenido: str) -> Optional[str]:
    candidato = contenido.strip().lstrip("﻿")
    if candidato[:1] not in ("{", "["):
        return None
    try:
        objeto = json.loads(candidato)
    except ValueError:
        return None
    return _desde_json(objeto)


def _desjsonizar_lineas(texto: str) -> str:
    salida = []
    for linea in texto.split("\n"):
        convertida = _texto_si_es_json(linea) if linea.strip()[:1] in ("{", "[") else None
        if convertida is None:
            salida.append(linea)
        elif convertida:
            salida.append(convertida)
    return _normalizar_texto("\n".join(salida))


def limpiar_html(html_crudo: str) -> str:
    """Convierte HTML (o JSON) crudo en texto legible. Regresa "" si no hay texto."""
    if not html_crudo or not html_crudo.strip():
        return ""

    como_json = _texto_si_es_json(html_crudo)
    if como_json is not None:
        return como_json

    soup = BeautifulSoup(ftfy.fix_text(html_crudo), "lxml")
    metadatos = _texto_de_metadatos(soup)

    _quitar_ruido(soup)
    _marcar_estructura(soup)

    cuerpo = soup.body or soup
    principal = soup.find("article") or soup.find("main")

    texto = _texto(principal) if principal else ""
    if len(texto) < MIN_CARACTERES_ARTICULO:
        texto_cuerpo = _texto(cuerpo)
        if len(texto_cuerpo) > len(texto):
            texto = texto_cuerpo

    como_json = _texto_si_es_json(texto)
    if como_json is not None:
        texto = como_json
    texto = _desjsonizar_lineas(texto)

    if metadatos and len(texto) < MIN_CARACTERES_ARTICULO and len(metadatos) >= len(texto):
        texto = metadatos

    return texto


def _ahora_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def limpiar_noticia(noticia: NoticiaCruda, fuente: str) -> NoticiaLimpia:
    return NoticiaLimpia(
        source=fuente,
        url=noticia.url,
        retrieved_at=_ahora_iso(),
        text=limpiar_html(noticia.html),
    )


def limpiar_lote(lote: LoteCrudo) -> List[NoticiaLimpia]:
    return [limpiar_noticia(noticia, lote.fuente) for noticia in lote.noticias]


LLAVES_HTML = ("html", "raw_html", "html_crudo", "content", "contenido", "body")
LLAVES_FUENTE = ("source", "fuente")


def _fuente_desde_url(url: str) -> str:
    dominio = urlparse(url or "").netloc.lower()
    if dominio.startswith("www."):
        dominio = dominio[4:]
    return dominio.replace(".", "_") or "desconocida"


def limpiar_registro(registro: Dict, fuente_por_defecto: Optional[str] = None) -> Dict:
    """Recibe un registro del Collector y regresa {source, url, retrieved_at, text}."""
    html = next((registro[k] for k in LLAVES_HTML if isinstance(registro.get(k), (str, dict, list))), None)
    if html is None:
        raise ValueError(f"El registro no trae HTML (se esperaba alguna de estas llaves: {', '.join(LLAVES_HTML)})")

    url = str(registro.get("url", ""))
    fuente = next((registro[k] for k in LLAVES_FUENTE if registro.get(k)), None) \
        or fuente_por_defecto or _fuente_desde_url(url)

    return {
        "source": fuente,
        "url": url,
        "retrieved_at": str(registro.get("retrieved_at") or _ahora_iso()),
        "text": limpiar_html(html) if isinstance(html, str) else _desde_json(html),
    }


def limpiar_registros(registros: List[Dict], fuente_por_defecto: Optional[str] = None) -> Tuple[List[Dict], List[Dict]]:
    """Regresa (limpios, errores). Un registro malo o con texto vacío no detiene a los demás."""
    limpios, errores = [], []
    for registro in registros:
        try:
            salida = limpiar_registro(registro, fuente_por_defecto)
            if not salida["text"]:
                raise ValueError("El texto limpio quedo vacio (la pagina no trae contenido en el HTML)")
            limpios.append(salida)
        except Exception as e:
            url = str(registro.get("url", "")) if isinstance(registro, dict) else ""
            errores.append({"url": url, "error": str(e)})
    return limpios, errores


def _cargar_registros(ruta: Path) -> List[Dict]:
    with open(ruta, "r", encoding="utf-8") as f:
        datos = json.load(f)
    if isinstance(datos, list):
        return datos
    if isinstance(datos, dict) and isinstance(datos.get("noticias"), list):
        fuente = datos.get("fuente") or datos.get("source")
        return [({"source": fuente, **n} if fuente else n) for n in datos["noticias"]]
    if isinstance(datos, dict):
        return [datos]
    raise ValueError(f"Formato de JSON no reconocido en {ruta}")


def limpiar_archivo(entrada: str, salida: str, ruta_errores: Optional[str] = None) -> Dict:
    """Limpia un .json (o todos los de una carpeta) y escribe un solo JSON consolidado."""
    ruta = Path(entrada)
    archivos = sorted(ruta.glob("*.json")) if ruta.is_dir() else [ruta]

    registros: List[Dict] = []
    errores_lectura: List[Dict] = []
    for archivo in archivos:
        try:
            registros.extend(_cargar_registros(archivo))
        except Exception as e:
            errores_lectura.append({"url": "", "error": f"{archivo.name}: {e}"})

    limpios, errores = limpiar_registros(registros)
    errores = errores_lectura + errores

    with open(salida, "w", encoding="utf-8") as f:
        json.dump({"total": len(limpios), "noticias": limpios}, f, ensure_ascii=False, indent=2)
    if ruta_errores:
        with open(ruta_errores, "w", encoding="utf-8") as f:
            json.dump(errores, f, ensure_ascii=False, indent=2)

    return {"leidos": len(registros), "limpios": len(limpios), "errores": len(errores)}
