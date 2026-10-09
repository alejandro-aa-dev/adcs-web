"""Auditoría estática de las páginas HTML: estructura, accesibilidad básica y enlaces.
Uso: python tools/auditar.py   (desde la raíz del proyecto)"""
import re, glob, os, json, sys
sys.stdout.reconfigure(encoding="utf-8")
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.ids=[]; s.heads=[]; s.imgs=[]; s.links=[]; s.inputs=[]; s.labels_for=set()
        s.jsonld=[]; s._j=False; s.title=""; s._t=False; s.h1=0; s.lang=None; s.main=0; s.meta={}
        s._a=None; s.anchors=[]; s._buf=""
    def handle_starttag(s,t,a):
        a=dict(a)
        if "id" in a: s.ids.append(a["id"])
        if t=="html": s.lang=a.get("lang")
        if t=="main": s.main+=1
        if t=="title": s._t=True
        if t=="meta" and a.get("name"): s.meta[a["name"]]=a.get("content","")
        if t in "h1 h2 h3 h4 h5 h6".split(): s.heads.append(int(t[1])); s.h1+= t=="h1"
        if t=="img": s.imgs.append(a)
        if t=="a": s._a=a; s._buf=""
        if t in("input","select","textarea") and a.get("type") not in("hidden","submit","button"): s.inputs.append(a)
        if t=="label" and "for" in a: s.labels_for.add(a["for"])
        if t=="script" and a.get("type")=="application/ld+json": s._j=True; s.jsonld.append("")
    def handle_endtag(s,t):
        if t=="title": s._t=False
        if t=="script": s._j=False
        if t=="a" and s._a is not None: s.anchors.append((s._a,s._buf.strip())); s._a=None
    def handle_data(s,d):
        if s._t: s.title+=d
        if s._j: s.jsonld[-1]+=d
        if s._a is not None: s._buf+=d

problemas=0
def avisa(f,m):
    global problemas; problemas+=1; print(f"  [{f}] {m}")

files=sorted(glob.glob("*.html")+glob.glob("socios/*.html"))
for f in files:
    s=open(f,encoding="utf-8").read(); p=P(); p.feed(s)
    if p.lang!="es": avisa(f,"falta lang=es")
    if not p.title.strip(): avisa(f,"sin <title>")
    if not p.meta.get("description"): avisa(f,"sin meta description")
    if p.h1!=1: avisa(f,f"debe tener 1 <h1>, tiene {p.h1}")
    if p.main!=1: avisa(f,f"debe tener 1 <main>, tiene {p.main}")
    for a,b in zip(p.heads,p.heads[1:]):
        if b>a+1: avisa(f,f"salto de encabezado h{a} → h{b}"); break
    dup={i for i in p.ids if p.ids.count(i)>1}
    if dup: avisa(f,f"IDs duplicados: {sorted(dup)}")
    for i in p.imgs:
        if "alt" not in i: avisa(f,f"<img> sin alt: {i.get('src','')[:60]}")
        if not (i.get("width") and i.get("height")) and "assets/img/patrocinadores" not in i.get("src","") : pass
    for i in p.inputs:
        if i.get("id") not in p.labels_for and not i.get("aria-label"): avisa(f,"campo de formulario sin etiqueta")
    for a,txt in p.anchors:
        h=a.get("href","")
        if h=="#": avisa(f,f"enlace '#' sin destino: «{txt[:40]}»")
        if a.get("target")=="_blank" and "noopener" not in a.get("rel",""): avisa(f,f"target=_blank sin noopener: {h[:50]}")
        if not txt and not a.get("aria-label") and "img" not in s[s.find(h):s.find(h)+300]: avisa(f,f"enlace sin texto: {h[:50]}")
        m=re.match(r"^(#.+)$",h)
        if m and m.group(1)[1:] not in p.ids: avisa(f,f"ancla interna inexistente {h}")
    for j in p.jsonld:
        try: json.loads(j)
        except Exception as e: avisa(f,f"JSON-LD inválido: {e}")
    # enlaces locales
    for u in re.findall(r'(?:src|href)="([^"#?:]+?)"',re.sub(r"<!--.*?-->","",s,flags=re.S)):
        if u.startswith(("http","mailto","//")): continue
        path=u.lstrip("/") if u.startswith("/") else os.path.normpath(os.path.join(os.path.dirname(f),u))
        if path and not os.path.exists(path): avisa(f,f"recurso local inexistente: {u}")
print(f"\n{len(files)} páginas auditadas, {problemas} avisos")
sys.exit(1 if problemas else 0)
