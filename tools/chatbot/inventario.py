#!/usr/bin/env python3
"""Inventario y clasificación del Drive de la ADCS para el chatbot (solo lectura).

No abre ningún archivo: clasifica por ruta, nombre y extensión con una LISTA BLANCA.
Todo lo que no esté expresamente permitido queda excluido.

Uso:
    python tools/chatbot/inventario.py --drive "G:/Mi unidad" --salida "C:/ruta/fuera/del/repo"

La salida (inventario.csv) contiene rutas y NO debe guardarse en el repositorio (es público).
"""
import argparse
import csv
import os
import sys
import unicodedata
from collections import Counter

# Carpetas (relativas a la raíz del Drive) cuya inclusión se propone. Prefijos en minúsculas sin tildes.
INCLUIR = {
    "documentacion general/historia de la adcs": "Historia de la asociación",
    "documentacion general/legal y estatutos": "Estatutos y documentos legales públicos",
    "documentacion general/comunicaciones y difusion": "Comunicaciones (revisar contactos)",
    "actividades": "Programas, bases y documentos de actividades",
    "fototeca-videoteca adcs": "Solo carteles en PDF/DOCX",
}

# Carpetas excluidas aunque cuelguen de una incluida.
EXCLUIR_CARPETA = {
    "documentacion general/legal y estatutos/formularios legales": "Plantillas de consentimiento (no son información pública)",
    "documentacion general/socios": "Datos personales de socios",
    "documentacion general/economia": "Datos bancarios y facturas",
    "documentacion general/actas de junta": "Documentos internos de la Junta",
    "documentacion general/certificados emitidos": "Nombres de participantes",
    "documentacion general/partituras": "Partituras (derechos de autor, no informativo)",
    "documentacion general/retransmisiones youtube": "Audios",
    "documentacion general/identidad y logos": "Logos (no texto)",
    "documentacion general/referencias de otras asociaciones": "Material de terceros",
    "copia de seguridad": "Copias duplicadas",
    "para borrar": "Pendiente de borrar",
    "entrada": "Entrada sin clasificar",
    "sin clasificar": "Sin clasificar (decidir a mano)",
}

# Palabras en la ruta que indican datos sensibles: se excluye por defecto.
PALABRAS_SENSIBLES = [
    "inscrip", "participantes", "lista de socios", "socios", "dni", "factura", "banco",
    "acta", "certificado", "presupuesto", "recibo", "domicili", "iban", "nomina",
    "jurado", "calificacion", "puntuacion", "notas", "reunion", "respuestas", "consentimiento",
]

# Subcarpetas internas de organización sin valor informativo para el público.
SUBCARPETAS_EXCLUIR = {
    "/logistica": "Logística interna (señalización de aulas)",
    "/planificacion y tareas": "Planificación interna",
    "/premios y economico": "Economía y reembolsos",
    "/versiones terminadas": "Versiones anteriores duplicadas",
    "/patrocinadores/": "Logotipos de patrocinadores (no texto informativo)",
    "/recibos": "Recibos con nombres",
    "partituras": "Partituras (derechos de autor)",
}

EXT_TEXTO ={".pdf", ".docx", ".doc", ".txt", ".md", ".odt", ".xlsx", ".csv"}
EXT_ATAJO = {".gdoc", ".gsheet", ".gform", ".gslides", ".gshortcut"}


def norm(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.lower().replace("\\", "/")


def clasificar(rel, ext):
    n = norm(rel)
    for pref, motivo in EXCLUIR_CARPETA.items():
        if n.startswith(pref):
            return "excluir", motivo
    base = None
    for pref, motivo in INCLUIR.items():
        if n.startswith(pref):
            base = motivo
            break
    if base is None:
        return "excluir", "Fuera de la lista blanca"
    if ext in EXT_ATAJO:
        return "exportar", "Atajo de Google sin contenido: exportar desde Drive a DOCX/PDF"
    if ext not in EXT_TEXTO:
        return "excluir", "No es documento de texto (foto, audio, vídeo, diseño…)"
    if n.startswith("fototeca-videoteca adcs") and "/carteles/" not in n:
        return "excluir", "Fototeca: solo se admiten carteles"
    for sub, motivo in SUBCARPETAS_EXCLUIR.items():
        if sub in n + "/":
            return "excluir", motivo
    for p in PALABRAS_SENSIBLES:
        if p in n:
            return "excluir", f"Nombre/ruta sensible («{p}»): excluido por defecto"
    if ext in {".xlsx", ".csv"}:
        return "revisar", "Hoja de cálculo: puede contener listados con personas"
    if "acta_fundacional" in n:
        return "revisar", "Acta fundacional: contiene nombres"
    return "incluir", base


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--drive", required=True)
    ap.add_argument("--salida", required=True)
    a = ap.parse_args()
    drive, salida = os.path.abspath(a.drive), os.path.abspath(a.salida)
    repo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if salida.startswith(repo):
        sys.exit("ERROR: la salida no puede estar dentro del repositorio (es público).")
    os.makedirs(salida, exist_ok=True)

    filas, cuenta = [], Counter()
    for raiz, dirs, files in os.walk(drive):
        dirs[:] = [d for d in dirs if d.lower() not in {".git", "$recycle.bin"}]
        for f in files:
            if f.lower() == "desktop.ini":
                continue
            p = os.path.join(raiz, f)
            rel = os.path.relpath(p, drive).replace("\\", "/")
            ext = os.path.splitext(f)[1].lower()
            dec, motivo = clasificar(rel, ext)
            try:
                tam = os.path.getsize(p)
            except OSError:
                tam = -1
            filas.append((rel, ext, tam, dec, motivo))
            cuenta[dec] += 1

    ruta = os.path.join(salida, "inventario.csv")
    with open(ruta, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["ruta", "extension", "bytes", "decision", "motivo"])
        w.writerows(filas)
    print(f"{len(filas)} archivos -> {ruta}")
    for k, v in cuenta.most_common():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
