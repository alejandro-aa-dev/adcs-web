"""Prepara el sitio para subirlo a Hostalia: copia solo los archivos públicos a dist/adcs-web/
y genera dist/adcs-web.zip. Antes avisa de lo que impediría publicar.
Uso: python tools/empaquetar.py            (desde la raíz del proyecto)
     python tools/empaquetar.py --forzar   (empaqueta aunque haya avisos graves)"""
import os, re, shutil, sys, zipfile, glob
sys.stdout.reconfigure(encoding="utf-8")

EXCLUIR_RAIZ = {".git", ".github", ".claude", ".gitignore", ".gitattributes", "docs", "privado", "tools", "supabase", "dist",
                "CONTEXT.md", "README.md", "ACCESIBILIDAD.md", "MEMORY.md",
                "Memorias", "Fotos y CV"}
EXCLUIR_PATRON = ("logo asoc*",)          # PDF del logo (original de trabajo)
SALIDA = os.path.join("dist", "adcs-web")

def publicos():
    for nombre in sorted(os.listdir(".")):
        if nombre in EXCLUIR_RAIZ or any(glob.fnmatch.fnmatch(nombre, p) for p in EXCLUIR_PATRON):
            continue
        if os.path.isdir(nombre):
            for d, _, fs in os.walk(nombre):
                for f in fs: yield os.path.join(d, f)
        else:
            yield nombre

archivos = list(publicos())
graves, avisos = [], []
html = [f for f in archivos if f.endswith(".html")]
for f in html:
    s = open(f, encoding="utf-8").read()
    visible = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    if "[PENDIENTE" in visible: graves.append(f"{f}: contiene textos [PENDIENTE]")
    if re.search(r'name="robots" content="noindex', visible) and f not in ("404.html",) and not f.startswith("socios"):
        graves.append(f"{f}: sigue marcada noindex (¿borrador?)")
    if 'href="#"' in visible and not f.startswith("socios"): avisos.append(f"{f}: enlaces '#' sin destino")
    for u in re.findall(r'(?:src|href)="([^"#?:]+?)"', visible):
        if u.startswith(("http", "mailto", "//")): continue
        p = u.lstrip("/") if u.startswith("/") else os.path.normpath(os.path.join(os.path.dirname(f), u))
        if p and not os.path.exists(p): graves.append(f"{f}: recurso inexistente {u}")
for f in html:
    if "googleapis" in open(f, encoding="utf-8").read(): avisos.append(f"{f}: referencia a Google Fonts")
if os.path.exists("sitemap.xml"):
    sm = open("sitemap.xml", encoding="utf-8").read()
    for f in html:
        if f in ("404.html",) or f.startswith("socios"): continue
        if f"/{f}<" not in sm and f != "index.html": avisos.append(f"{f}: no está en sitemap.xml")
if "# RewriteEngine" in open(".htaccess", encoding="utf-8").read():
    avisos.append(".htaccess: bloque mod_rewrite (HTTPS) aún comentado — descomentar solo con SSL activo")
for f in glob.glob("socios/*.html"):
    if "Contenido de ejemplo" in open(f, encoding="utf-8").read():
        avisos.append(f"{f}: aún con 'Contenido de ejemplo'")

print("GRAVES (bloquean la publicación):" if graves else "Sin avisos graves.")
for g in graves: print("  ✗", g)
print("AVISOS:" if avisos else "Sin avisos menores.")
for a in avisos: print("  !", a)
if graves and "--forzar" not in sys.argv:
    print("\nNo se ha empaquetado. Corrige lo anterior o usa --forzar."); sys.exit(1)

shutil.rmtree("dist", ignore_errors=True)
for f in archivos:
    dest = os.path.join(SALIDA, f); os.makedirs(os.path.dirname(dest), exist_ok=True); shutil.copy2(f, dest)
zip_path = os.path.join("dist", "adcs-web.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for f in archivos: z.write(f, f.replace("\\", "/"))
mb = os.path.getsize(zip_path) / 1e6
print(f"\n{len(archivos)} archivos → {zip_path} ({mb:.1f} MB)")
