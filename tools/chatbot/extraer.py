#!/usr/bin/env python3
"""Extrae texto de la web (HTML del repo) y de los documentos del Drive aprobados en el inventario.

Uso:
    python tools/chatbot/extraer.py --repo . --drive "G:/Mi unidad" --corpus "C:/ruta/fuera/del/repo"

Salida (en --corpus, NUNCA dentro del repo):
    bruto/web/*.txt          texto de cada página pública
    bruto/drive/*.txt        texto de cada documento del Drive (sin anonimizar todavía)
    extraccion.csv           resultado por documento (caracteres, avisos, metadatos inferidos)
"""
import argparse
import csv
import hashlib
import os
import re
import sys
import zipfile
from html.parser import HTMLParser

SALTAR_WEB_DIRS = {"socios", "docs", "tools", "assets", "dist", "supabase"}


# ---------------------------------------------------------------- web
class _Texto(HTMLParser):
    BLOQUES = {"p", "div", "li", "h1", "h2", "h3", "h4", "tr", "section", "article", "br", "dt", "dd"}
    IGNORAR = {"script", "style", "nav", "footer", "header", "svg", "noscript", "iframe", "form", "button"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip, self.titulo, self._en_title = [], 0, "", False
        self.en_main, self.hay_main = False, False
        self._href = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._en_title = True
        if tag == "main":
            self.en_main = self.hay_main = True
        if tag in self.IGNORAR:
            self.skip += 1
        if tag == "a" and a.get("href", "").startswith(("http", "mailto:")):
            self._href = a["href"]
        if tag in self.BLOQUES:
            self.out.append("\n")
        if tag == "img" and a.get("alt"):
            self.out.append(f" [imagen: {a['alt']}] ")

    def handle_endtag(self, tag):
        if tag == "title":
            self._en_title = False
        if tag in self.IGNORAR and self.skip:
            self.skip -= 1
        if tag == "a" and self._href:
            if not self._href.startswith("mailto:") or "oboeyfagotsevilla@gmail.com" in self._href:
                self.out.append(f" ({self._href.replace('mailto:', '')})")
            self._href = None
        if tag in self.BLOQUES:
            self.out.append("\n")

    def handle_data(self, data):
        if self._en_title:
            self.titulo += data
        elif not self.skip:
            self.out.append(data)


def extraer_html(ruta):
    p = _Texto()
    p.feed(open(ruta, encoding="utf-8").read())
    texto = re.sub(r"[ \t]+", " ", "".join(p.out))
    texto = re.sub(r"\n\s*\n+", "\n\n", texto).strip()
    return p.titulo.strip(), texto


# ---------------------------------------------------------------- documentos
def leer_pdf(ruta):
    import pymupdf
    doc = pymupdf.open(ruta)
    paginas = [pg.get_text() for pg in doc]
    return "\n\n".join(paginas), len(paginas)


def leer_docx(ruta):
    import docx
    d = docx.Document(ruta)
    partes = [p.text for p in d.paragraphs]
    for t in d.tables:
        for fila in t.rows:
            partes.append(" | ".join(c.text.strip() for c in fila.cells))
    return "\n".join(partes), 1


def leer_odt(ruta):
    with zipfile.ZipFile(ruta) as z:
        xml = z.read("content.xml").decode("utf-8", "ignore")
    xml = re.sub(r"</text:(p|h)>", "\n", xml)
    return re.sub(r"<[^>]+>", "", xml), 1


def leer_txt(ruta):
    return open(ruta, encoding="utf-8", errors="ignore").read(), 1


def leer_xlsx(ruta):
    import openpyxl
    wb = openpyxl.load_workbook(ruta, read_only=True, data_only=True)
    filas = []
    for ws in wb.worksheets:
        filas.append(f"## Hoja {ws.title}")
        for r in ws.iter_rows(values_only=True):
            if any(c is not None for c in r):
                filas.append(" | ".join("" if c is None else str(c) for c in r))
    return "\n".join(filas), 1


LECTORES = {".pdf": leer_pdf, ".docx": leer_docx, ".odt": leer_odt, ".txt": leer_txt,
            ".md": leer_txt, ".xlsx": leer_xlsx, ".csv": leer_txt}

ROMANOS = r"(?:I{1,3}|IV|V|VI{0,3}|IX|X{1,3})"


def metadatos(rel):
    """Infiere tipo, edición y año a partir de la ruta (se confirma en la revisión)."""
    t = rel.lower()
    tipo = "otro"
    for clave, nombre in (("concurso", "concurso"), ("encuentro", "encuentro"), ("ciclo de m", "ciclo"),
                          ("clases y talleres", "taller"), ("historia", "historia"),
                          ("estatuto", "estatutos"), ("comunicaciones", "comunicacion"),
                          ("asamblea", "asamblea"), ("proyecto", "proyecto")):
        if clave in t:
            tipo = nombre
            break
    m = re.search(r"\((?:[A-Za-zñÑ\.]+ )?(20\d\d)", rel)
    anio = m.group(1) if m else ""
    m2 = re.search(rf"/({ROMANOS}) (?:Concurso|Encuentro|Concierto)", rel)
    edicion = m2.group(1) if m2 else ""
    return tipo, edicion, anio


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--drive", required=True)
    ap.add_argument("--corpus", required=True)
    a = ap.parse_args()
    repo, drive, corpus = (os.path.abspath(x) for x in (a.repo, a.drive, a.corpus))
    if corpus.startswith(repo):
        sys.exit("ERROR: el corpus no puede estar dentro del repositorio (es público).")
    os.makedirs(f"{corpus}/bruto/web", exist_ok=True)
    os.makedirs(f"{corpus}/bruto/drive", exist_ok=True)

    filas = []
    # --- web
    for f in sorted(os.listdir(repo)):
        if not f.endswith(".html") or re.search(r" \(\d+\)\.html$", f) or f == "404.html":
            continue
        titulo, texto = extraer_html(os.path.join(repo, f))
        nombre = f[:-5]
        open(f"{corpus}/bruto/web/{nombre}.txt", "w", encoding="utf-8").write(f"# {titulo}\n\n{texto}\n")
        filas.append(("web", f, nombre, "web", "", "", len(texto), "", f"https://adcsevilla.es/{f}"))

    # --- drive
    inv = list(csv.DictReader(open(f"{corpus}/inventario.csv", encoding="utf-8-sig"), delimiter=";"))
    for x in inv:
        if x["decision"] != "incluir":
            continue
        rel, ext = x["ruta"], x["extension"]
        lector = LECTORES.get(ext)
        if not lector:
            filas.append(("drive", rel, "", "", "", "", 0, "sin lector para " + ext, ""))
            continue
        try:
            texto, pags = lector(os.path.join(drive, rel))
        except Exception as e:  # archivo dañado, protegido, etc.
            filas.append(("drive", rel, "", "", "", "", 0, f"error: {type(e).__name__}", ""))
            continue
        texto = re.sub(r"[ \t]+", " ", texto)
        texto = re.sub(r"\n\s*\n+", "\n\n", texto).strip()
        aviso = ""
        if len(texto) < 40 * max(pags, 1):
            aviso = "posible escaneo/imagen: texto insuficiente (requiere OCR)"
        tipo, ed, anio = metadatos(rel)
        id_ = hashlib.sha1(rel.encode("utf-8")).hexdigest()[:10]
        open(f"{corpus}/bruto/drive/{id_}.txt", "w", encoding="utf-8").write(texto + "\n")
        filas.append(("drive", rel, id_, tipo, ed, anio, len(texto), aviso, ""))

    with open(f"{corpus}/extraccion.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["origen", "ruta", "id", "tipo", "edicion", "anio", "caracteres", "aviso", "url"])
        w.writerows(filas)
    web = [r for r in filas if r[0] == "web"]
    dr = [r for r in filas if r[0] == "drive"]
    print(f"web: {len(web)} páginas, {sum(r[6] for r in web):,} caracteres")
    print(f"drive: {len(dr)} documentos, {sum(r[6] for r in dr):,} caracteres, "
          f"{sum(1 for r in dr if r[7])} con avisos")


if __name__ == "__main__":
    main()
