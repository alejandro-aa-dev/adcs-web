#!/usr/bin/env python3
"""Carga la base de conocimiento en Supabase (o la simula con --dry-run).

Modos:
  --web      páginas públicas de la web + núcleo + FAQ (información pública; se puede repetir cada vez que se publique algo)
  --drive    documentos del archivo (Drive) SOLO si están en aprobados.json y pasan el escáner de datos personales

Variables de entorno (o archivo  <corpus>/.env  fuera del repo):
  SUPABASE_URL=https://xxxx.supabase.co
  SUPABASE_SERVICE_KEY=...   (clave service_role; NUNCA en el repo ni en el chat)

Uso:
  python tools/chatbot/sincronizar.py --corpus "C:/ruta/fuera/del/repo" --web --dry-run
  python tools/chatbot/sincronizar.py --corpus "C:/ruta/fuera/del/repo" --web
  python tools/chatbot/sincronizar.py --corpus "C:/ruta/fuera/del/repo" --drive
"""
import argparse
import csv
import datetime
import json
import os
import re
import subprocess
import sys
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(AQUI, "..", ".."))
OBJETIVO, SOLAPE = 900, 120


def trocear(texto):
    """Fragmentos de ~900 caracteres respetando párrafos, con solape."""
    parrafos = [p.strip() for p in re.split(r"\n\s*\n", texto) if p.strip()]
    out, actual = [], ""
    for p in parrafos:
        if actual and len(actual) + len(p) > OBJETIVO:
            out.append(actual)
            actual = actual[-SOLAPE:] + "\n" + p if SOLAPE else p
        else:
            actual = (actual + "\n\n" + p) if actual else p
        while len(actual) > OBJETIVO * 1.6:  # párrafo larguísimo
            out.append(actual[:OBJETIVO])
            actual = actual[OBJETIVO - SOLAPE:]
    if actual.strip():
        out.append(actual)
    return out


class Api:
    def __init__(self, dry):
        self.dry = dry
        self.url = os.environ.get("SUPABASE_URL", "").rstrip("/")
        self.key = os.environ.get("SUPABASE_SERVICE_KEY", "")
        if not dry and not (self.url and self.key):
            sys.exit("Faltan SUPABASE_URL y SUPABASE_SERVICE_KEY (variables de entorno o <corpus>/.env).")

    def llamar(self, metodo, ruta, datos=None, extra=None):
        if self.dry:
            return [{"id": 0}] * (len(datos) if isinstance(datos, list) else 1)
        cab = {"apikey": self.key, "authorization": f"Bearer {self.key}", "content-type": "application/json",
               "Prefer": "return=representation"}
        cab.update(extra or {})
        req = urllib.request.Request(f"{self.url}/rest/v1/{ruta}", method=metodo, headers=cab,
                                     data=json.dumps(datos).encode() if datos is not None else None)
        with urllib.request.urlopen(req) as r:
            cuerpo = r.read()
        return json.loads(cuerpo) if cuerpo else []


def subir_doc(api, doc, texto, stats):
    ids = api.llamar("POST", "kb_documents", doc)
    doc_id = ids[0]["id"]
    trozos = trocear(texto)
    for i in range(0, len(trozos), 100):
        api.llamar("POST", "kb_chunks", [{"doc_id": doc_id, "orden": i + j, "texto": t}
                                         for j, t in enumerate(trozos[i:i + 100])])
    stats["docs"] += 1
    stats["chunks"] += len(trozos)


def cargar_env(corpus):
    p = os.path.join(corpus, ".env")
    if os.path.exists(p):
        for l in open(p, encoding="utf-8"):
            if "=" in l and not l.startswith("#"):
                k, v = l.strip().split("=", 1)
                os.environ.setdefault(k, v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--web", action="store_true")
    ap.add_argument("--drive", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    corpus = os.path.abspath(a.corpus)
    if corpus.startswith(REPO):
        sys.exit("ERROR: el corpus no puede estar dentro del repositorio.")
    if not (a.web or a.drive):
        sys.exit("Indica --web y/o --drive")
    cargar_env(corpus)
    api = Api(a.dry_run)
    stats = {"docs": 0, "chunks": 0}

    if a.web:
        # Reextrae la web actual para que el bot siempre conozca lo último publicado.
        subprocess.run([sys.executable, os.path.join(AQUI, "extraer.py"), "--repo", REPO,
                        "--drive", os.environ.get("DRIVE_RAIZ", "G:/Mi unidad"), "--corpus", corpus],
                       check=True, stdout=subprocess.DEVNULL)
        api.llamar("DELETE", "kb_documents?origen=in.(web,faq)")
        for r in csv.DictReader(open(f"{corpus}/extraccion.csv", encoding="utf-8-sig"), delimiter=";"):
            if r["origen"] != "web":
                continue
            t = open(f"{corpus}/bruto/web/{r['id']}.txt", encoding="utf-8").read()
            titulo = t.splitlines()[0].lstrip("# ").strip() if t else r["id"]
            subir_doc(api, {"origen": "web", "titulo": titulo, "tipo": "web", "vigencia": "vigente",
                            "url": r["url"], "ref_interna": r["ruta"]}, t, stats)
        for f in json.load(open(f"{AQUI}/conocimiento/faq.json", encoding="utf-8")):
            subir_doc(api, {"origen": "faq", "titulo": f["pregunta"], "tipo": "faq", "vigencia": "vigente",
                            "url": f.get("fuente")}, f"{f['pregunta']}\n{f['respuesta']}", stats)
        nucleo = open(f"{AQUI}/conocimiento/nucleo.md", encoding="utf-8").read()
        api.llamar("PATCH", "bot_settings?id=eq.1", {"nucleo": nucleo}, {"Prefer": "return=minimal"})
        print(f"núcleo: {len(nucleo)} caracteres (~{len(nucleo)//4} tokens)")

    if a.drive:
        apro = f"{corpus}/aprobados.json"
        if not os.path.exists(apro):
            sys.exit("No existe aprobados.json: la revisión humana es obligatoria antes de subir el archivo.")
        r = subprocess.run([sys.executable, os.path.join(AQUI, "escanear_pii.py"), "--corpus", corpus])
        if r.returncode != 0:
            sys.exit("El escáner de datos personales ha encontrado coincidencias: no se sube nada.")
        aprobados = set(json.load(open(apro)))
        api.llamar("DELETE", "kb_documents?origen=eq.drive")
        for r in csv.DictReader(open(f"{corpus}/extraccion.csv", encoding="utf-8-sig"), delimiter=";"):
            if r["origen"] != "drive" or r["id"] not in aprobados:
                continue
            t = open(f"{corpus}/anonimizado/{r['id']}.txt", encoding="utf-8").read()
            titulo = os.path.splitext(r["ruta"].split("/")[-1])[0]
            subir_doc(api, {"origen": "drive", "titulo": titulo, "tipo": r["tipo"], "edicion": r["edicion"] or None,
                            "anio": r["anio"] or None, "vigencia": "historico", "url": None,
                            "ref_interna": r["id"], "revisado_en": datetime.datetime.now(datetime.timezone.utc).isoformat()}, t, stats)
    print(("[simulación] " if a.dry_run else "") + f"{stats['docs']} documentos, {stats['chunks']} fragmentos")


if __name__ == "__main__":
    main()
