#!/usr/bin/env python3
"""Escáner independiente de datos personales sobre el corpus anonimizado (condición previa a subir nada).

Usa patrones más estrictos que anonimizar.py. Termina con código 1 si encuentra algo.

Uso:  python tools/chatbot/escanear_pii.py --corpus "C:/ruta/fuera/del/repo" [--dir anonimizado]
"""
import argparse
import os
import re
import sys

PUBLICO = {"oboeyfagotsevilla@gmail.com"}
REGLAS = [
    ("DNI/NIE", re.compile(r"\b(?:\d{8}|[XYZxyz]\d{7})[- ]?[A-Za-z]\b")),
    ("IBAN", re.compile(r"\b[A-Z]{2}\d{2}[ ]?(?:\d{4}[ ]?){2,6}\d{0,4}\b")),
    ("Teléfono", re.compile(r"(?<![\d/.-])(?:\+34[ .-]?)?[6789]\d{2}[ .-]?\d{2,3}[ .-]?\d{2,3}[ .-]?\d{0,2}(?![\d/.-])")),
    ("Correo", re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")),
    ("Secuencia larga de dígitos", re.compile(r"(?<!\d)\d{9,}(?!\d)")),
    ("Enlace privado", re.compile(r"(?:docs|drive|forms)\.google\.com|forms\.gle|dropbox\.com|wetransfer\.com", re.I)),
    ("Dirección", re.compile(r"\b(?:C/|Calle|Avda\.?|Avenida)\s+[A-ZÁÉÍÓÚ][^\n,]{2,40}\s+\d{1,3}\b")),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--dir", default="anonimizado")
    a = ap.parse_args()
    d = os.path.join(os.path.abspath(a.corpus), a.dir)
    hallazgos = 0
    for f in sorted(os.listdir(d)):
        t = open(os.path.join(d, f), encoding="utf-8").read()
        for nombre, rx in REGLAS:
            for m in rx.finditer(t):
                if nombre == "Correo" and m.group(0).lower() in PUBLICO:
                    continue
                hallazgos += 1
                s = t[max(0, m.start() - 20):m.end() + 20].replace("\n", " ")
                print(f"{f}: {nombre}: …{s}…")
    print(f"\n{hallazgos} hallazgos")
    sys.exit(1 if hallazgos else 0)


if __name__ == "__main__":
    main()
