#!/usr/bin/env python3
"""Genera revision.html (local): informe para aprobar documento a documento el corpus anonimizado.

Uso:  python tools/chatbot/revisar.py --corpus "C:/ruta/fuera/del/repo"
Después, abrir <corpus>/revision.html, marcar los documentos aprobados y pulsar «Descargar aprobados.json»;
guardar el archivo en <corpus>/aprobados.json. Nada se sube a Supabase sin ese archivo.
"""
import argparse
import csv
import html
import os
import sys

COLS = ["dni_nie", "iban", "cuenta", "tarjeta", "telefono", "direccion", "cp", "nacimiento",
        "enlace_privado", "correo", "nombres"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    a = ap.parse_args()
    c = os.path.abspath(a.corpus)
    repo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if c.startswith(repo):
        sys.exit("ERROR: el corpus no puede estar dentro del repositorio.")
    filas = list(csv.DictReader(open(f"{c}/anonimizacion.csv", encoding="utf-8-sig"), delimiter=";"))
    avisos = {r["id"]: r["aviso"] for r in csv.DictReader(open(f"{c}/extraccion.csv", encoding="utf-8-sig"), delimiter=";")}
    partes = []
    for r in filas:
        t = open(f"{c}/anonimizado/{r['id']}.txt", encoding="utf-8").read()
        red = ", ".join(f"{k}: {r[k]}" for k in COLS if r[k] not in ("0", ""))
        aviso = avisos.get(r["id"], "")
        partes.append(f"""<article>
<label class="ok"><input type="checkbox" data-id="{r['id']}"> Aprobado</label>
<h3>{html.escape(r['ruta'].split('/')[-1])}</h3>
<p class="m">{html.escape(r['tipo'])} · {html.escape(r['edicion'])} · {html.escape(r['anio'])} · {r['caracteres']} caracteres<br>
<span>{html.escape(r['ruta'])}</span><br>Redacciones → {html.escape(red) or 'ninguna'}{'<br><b>⚠ ' + html.escape(aviso) + '</b>' if aviso else ''}</p>
<details><summary>Ver texto anonimizado</summary><pre>{html.escape(t)}</pre></details></article>""")
    doc = f"""<!doctype html><meta charset="utf-8"><title>Revisión del corpus ADCS (LOCAL, no publicar)</title>
<style>body{{font:15px system-ui;max-width:900px;margin:2rem auto;padding:0 1rem}}article{{border:1px solid #ccc;border-radius:8px;padding:.8rem 1rem;margin:.8rem 0}}
.m{{color:#555;font-size:13px}}.m span{{color:#888}}pre{{white-space:pre-wrap;background:#f6f6f6;padding:.6rem;max-height:420px;overflow:auto}}
.ok{{float:right}}button{{padding:.6rem 1rem;font-size:15px}}</style>
<h1>Revisión del corpus ({len(filas)} documentos)</h1>
<p><b>Documento LOCAL con contenido interno. No lo subas ni lo compartas.</b> Comprueba que no queda ningún dato personal
(nombres no públicos, teléfonos, direcciones, menores) y que el contenido es información que la ADCS aceptaría ver publicada.
Marca solo lo que apruebes.</p>
<p><button id="b">Descargar aprobados.json</button> <span id="n">0</span> aprobados</p>
{''.join(partes)}
<script>
const q=()=>[...document.querySelectorAll('input[data-id]:checked')].map(e=>e.dataset.id);
document.addEventListener('change',()=>document.getElementById('n').textContent=q().length);
document.getElementById('b').onclick=()=>{{const a=document.createElement('a');
a.href=URL.createObjectURL(new Blob([JSON.stringify(q(),null,1)],{{type:'application/json'}}));a.download='aprobados.json';a.click()}};
</script>"""
    open(f"{c}/revision.html", "w", encoding="utf-8").write(doc)
    print(f"{c}/revision.html ({len(filas)} documentos)")


if __name__ == "__main__":
    main()
