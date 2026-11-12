#!/usr/bin/env python3
"""Anonimiza el texto extraído de los documentos del Drive (los de la web son públicos y no se tocan).

Seguro por defecto: todo nombre de persona que NO esté en la lista de nombres públicos se sustituye por
«[persona]». La lista de nombres públicos se siembra con los nombres que ya figuran en la web y se amplía
a mano en  <corpus>/nombres_publicos.txt  (uno por línea) tras revisar  nombres_candidatos.csv.

Uso:
    python tools/chatbot/anonimizar.py --corpus "C:/ruta/fuera/del/repo"

Salida: anonimizado/*.txt, anonimizacion.csv (recuentos por tipo, sin valores) y nombres_candidatos.csv.
La detección automática NO es infalible: la revisión humana (revisar.py) es obligatoria.
"""
import argparse
import csv
import os
import re
import sys
from collections import Counter, defaultdict

CORREO_PUBLICO = "oboeyfagotsevilla@gmail.com"

PATRONES = [
    ("dni_nie", re.compile(r"\b(?:\d{8}|[XYZxyz]\d{7})[- ]?[A-Za-z]\b"), "[documento]"),
    ("iban", re.compile(r"\b[A-Z]{2}\d{2}(?:[ -]?[A-Z0-9]{4}){3,7}(?:[ -]?[A-Z0-9]{1,4})?\b"), "[cuenta]"),
    ("cuenta", re.compile(r"\b\d{4}[\s-]+\d{4}[\s-]+\d{2}[\s-]+\d{10}\b"), "[cuenta]"),
    ("nif_entidad", re.compile(r"\(?\b[A-HJNP-SUVW]\d{7}[0-9A-J]\b\)?"), "[NIF]"),
    ("tarjeta", re.compile(r"\b(?:\d{4}[ -]){3}\d{4}\b"), "[tarjeta]"),
    ("telefono", re.compile(r"(?<!\d)(?:\+34[ .-]?)?(?:[6789]\d{2}[ .-]?\d{3}[ .-]?\d{3}|[6789]\d{2}[ .-]?\d{2}[ .-]?\d{2}[ .-]?\d{2})(?!\d)"), "[teléfono]"),
    ("direccion", re.compile(r"\b(?:C/|Calle|Avda\.?|Avenida|Plaza|Pza\.?|Paseo|Camino|Urbanizaci[oó]n)\s+[^,\n]{2,50}?,?\s*(?:n[ºo°.]*\s*)?\d{1,3}(?:[ ,]*(?:\d?[º°ªA-Za-z]{1,2}))?", re.I), "[dirección]"),
    ("codigo_postal", re.compile(r"\b(?:41|11|14|18|21|23|29)\d{3}\b(?=\s+[A-ZÁÉÍÓÚ])"), "[CP]"),
    ("nacimiento", re.compile(r"(?:nacid[oa]|fecha de nacimiento|f\.\s*nac\.?)[^\n]{0,40}", re.I), "[fecha de nacimiento]"),
    ("enlace_privado", re.compile(r"https?://(?:docs|drive|forms)\.google\.com/\S+|https?://forms\.gle/\S+|https?://(?:www\.)?dropbox\.com/\S+|https?://wetransfer\.com/\S+", re.I), "[enlace privado]"),
]
CORREO = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")

# Palabras que no forman parte de un nombre de persona (instituciones, lugares, términos del dominio…).
STOP = set("""
Asociación Asociacion Doble Caña Cana Sevilla Concurso Encuentro Conservatorio Oboe Oboes Fagot Fagotes Música Musica Cámara Camara
Ciclo Junta Directiva Andalucía Andalucia Escuela Superior Profesional Profesionales Elemental Real Orquesta Sinfónica Sinfonica Teatro
Aula Curso Cursos Taller Talleres Clases Clase Magistral Magistrales Premio Premios Nivel Bases Base Artículo Articulo Capítulo
Universidad Facultad Ayuntamiento Consejería Consejeria Fundación Fundacion Federación Federacion Auditorio Sala Salón Salon Actos
Congreso Jornada Jornadas Sociedad Banda Cuarteto Quinteto Trío Trio Dúo Duo Gala Final Primer Segunda Segundo Primera Tercer Tercera
Cuarto Quinta Quinto Sexto Sexta Edición Edicion Fecha Lugar Hora Horario Inscripción Inscripcion Plazo Cuota Socio Socia Socios Socias
Presidente Presidenta Secretario Secretaria Tesorero Tesorera Vocal Vocales Jurado Participantes Participante Alumnos Alumnas Profesor
Profesora Profesores Profesoras Solista Director Directora Dirección Direccion España Espana Madrid Barcelona Valencia Murcia Granada
Málaga Malaga Córdoba Cordoba Cádiz Cadiz Huelva Jaén Jaen Almería Almeria Triana Nervión Nervion Setas Isla Mágica Magica Giralda
Fototeca Videoteca Instagram Facebook YouTube WhatsApp Google Drive Gmail Word Excel PDF Mozart Bach Beethoven Brahms Haydn Vivaldi
Telemann Händel Handel Albinoni Marcello Saint Saëns Strauss Mahler Weber Danzi Fossati Loree Lorée Reeds Stuff Afoes AFOES Afogal
Ekbe Zasmusic Navidad Reyes Santa Semana Feria Sevillanas Madrigal Pérez Perez Antonio José Jose Pedro Lobo Pink Panther Jingle
Bells Libertango Piazzolla Piazzola Gershwin Prokofiev Verdi Rossini Berlioz Tchaikowsky Tchaikovsky Corelli Joplin Mancini
Estimados Estimadas Querido Queridos Queridas Querida Hola Gracias Saludos Atentamente Buenos Buenas Días Dias Tardes Noches
Lunes Martes Miércoles Miercoles Jueves Viernes Sábado Sabado Domingo Enero Febrero Marzo Abril Mayo Junio Julio Agosto
Septiembre Octubre Noviembre Diciembre Nuestro Nuestra Este Esta Estos Estas Para Por Con Sin Sobre Entre Desde Hasta
La El Los Las Un Una Unos Unas Del Al De En Y O Que Como Si No Se Su Sus Más Mas Muy Todo Todos Todas Cada Cuando Donde
Obra Obras Repertorio Prueba Pruebas Acceso Grado Enseñanzas Enseñanzas EEPP Cañas Canas Mantenimiento Reparación Reparacion
Mayor Menor Sib Fa Do Re Mi Sol Si Lab Mib Reb Op Opus Concerto Concertino Sonata Sonatas Suite Romanza Romanzas Prelude Preludio Courante Sketches Four Motivi Sopra Favorita Pianista Acompañante Acompanante Utilidad Pública Publica Estados Unidos Asamblea General Ordinaria Extraordinaria Distribuirá Partituras Partitura Obligatoria Libre Pieza Piezas Movimiento Allegro Adagio Andante Largo Rondó Rondo Variaciones Fantasía Fantasia Danza Danzas Marcha Vals Tango Habanera Ópera Opera Sinfonía Sinfonia Cuarteto Quinteto Septeto Ramón Cajal Victoria Eugenia Cristóbal Morales Luisa Pons Josep Oro Plata Bronce Primer Segundo Tercer Cuarto Ministerio Educación Educacion Cultura Junta Gobierno Diputación Diputacion Provincial Universidad Hispalense Federación Palacio Parque Plaza Centro Cívico Civico Patrocinador Patrocinadores Colaborador Colaboradores Organiza Organizan Colabora Colaboran Becas Beca Matrícula Matricula Ingreso Ingresos Gastos Total Importe Euros Descuento Descuentos Incluye Incluido Requisitos Requisito Condiciones
Concierto Conciertos Programa Información Informacion Contacto Correo Teléfono Telefono Web Página Pagina Ficha Resultados
""".split())
PARTICULAS = {"de", "del", "de la", "la", "y", "van", "von", "da", "di", "dos", "das", "san"}

CAP = r"[A-ZÁÉÍÓÚÑ][a-záéíóúñü]+(?:-[A-ZÁÉÍÓÚÑ][a-záéíóúñü]+)?"
NOMBRE = re.compile(rf"\b{CAP}(?:\s+(?:(?:de la|del|de|y|van|von|da|di|dos)\s+)?{CAP}){{1,3}}\b")
TRATAMIENTO = re.compile(rf"\b(?:D\.|Dña\.|Dª|Sr\.|Sra\.|Don|Doña|Prof\.|Profa\.|Dr\.|Dra\.)\s+{CAP}(?:\s+{CAP}){{0,3}}")
MAYUS = re.compile(r"\b[A-ZÁÉÍÓÚÑ]{3,}(?:\s+[A-ZÁÉÍÓÚÑ]{3,}){1,3}\b")


def es_nombre(candidato):
    palabras = [p for p in re.split(r"\s+", candidato) if p.lower() not in PARTICULAS]
    if len(palabras) < 2:
        return False
    return not any(p in STOP or p.capitalize() in STOP for p in palabras)


def candidatos(texto):
    vistos = []
    for m in TRATAMIENTO.finditer(texto):
        vistos.append(m.group(0))
    for m in NOMBRE.finditer(texto):
        if es_nombre(m.group(0)):
            vistos.append(m.group(0))
    for m in MAYUS.finditer(texto):
        if es_nombre(m.group(0).title()):
            vistos.append(m.group(0))
    return vistos


def limpiar_trat(n):
    return re.sub(r"^(?:D\.|Dña\.|Dª|Sr\.|Sra\.|Don|Doña|Prof\.|Profa\.|Dr\.|Dra\.)\s+", "", n)


def norm(n):
    return re.sub(r"\s+", " ", limpiar_trat(n)).strip().lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    a = ap.parse_args()
    c = os.path.abspath(a.corpus)
    repo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if c.startswith(repo):
        sys.exit("ERROR: el corpus no puede estar dentro del repositorio.")
    os.makedirs(f"{c}/anonimizado", exist_ok=True)

    # 1) Nombres públicos: los que ya aparecen en la web + los aprobados a mano.
    publicos = set()
    for f in os.listdir(f"{c}/bruto/web"):
        for n in candidatos(open(f"{c}/bruto/web/{f}", encoding="utf-8").read()):
            publicos.add(norm(n))
    extra = f"{c}/nombres_publicos.txt"
    if os.path.exists(extra):
        publicos |= {norm(l) for l in open(extra, encoding="utf-8") if l.strip() and not l.startswith("#")}

    def es_publico(n):
        k = norm(n)
        return k in publicos or any(k in p or p in k for p in publicos if len(p) > 8 and len(k) > 8)

    meta = {r["id"]: r for r in csv.DictReader(open(f"{c}/extraccion.csv", encoding="utf-8-sig"), delimiter=";")
            if r["origen"] == "drive" and r["id"]}
    resumen, cand = [], defaultdict(Counter)
    for id_, r in meta.items():
        ruta_in = f"{c}/bruto/drive/{id_}.txt"
        if not os.path.exists(ruta_in):
            continue
        t = open(ruta_in, encoding="utf-8").read()
        cuenta = Counter()
        for nombre, rx, rep in PATRONES:
            t, n = rx.subn(rep, t)
            cuenta[nombre] += n

        def sust_correo(m):
            if m.group(0).lower() == CORREO_PUBLICO:
                return m.group(0)
            cuenta["correo"] += 1
            return "[correo]"
        t = CORREO.sub(sust_correo, t)

        def sust_nombre(m):
            n = m.group(0)
            if not (es_nombre(limpiar_trat(n)) or TRATAMIENTO.fullmatch(n)):
                return n
            if es_publico(n):
                cand[norm(n)]["publico"] += 1
                return n
            cuenta["nombre"] += 1
            cand[norm(n)]["redactado"] += 1
            return "[persona]"
        t = TRATAMIENTO.sub(sust_nombre, t)
        t = NOMBRE.sub(sust_nombre, t)
        t = MAYUS.sub(lambda m: sust_nombre(m) if es_nombre(m.group(0).title()) else m.group(0), t)
        open(f"{c}/anonimizado/{id_}.txt", "w", encoding="utf-8").write(t)
        resumen.append([id_, r["ruta"], r["tipo"], r["edicion"], r["anio"], len(t)] +
                       [cuenta[k] for k in ("dni_nie", "iban", "cuenta", "tarjeta", "telefono", "direccion",
                                            "codigo_postal", "nacimiento", "enlace_privado", "correo", "nombre")])

    with open(f"{c}/anonimizacion.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["id", "ruta", "tipo", "edicion", "anio", "caracteres", "dni_nie", "iban", "cuenta", "tarjeta",
                    "telefono", "direccion", "cp", "nacimiento", "enlace_privado", "correo", "nombres"])
        w.writerows(resumen)
    with open(f"{c}/nombres_candidatos.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["nombre", "veces_redactado", "veces_publico", "accion_sugerida"])
        for n, k in sorted(cand.items(), key=lambda x: -(x[1]["redactado"] + x[1]["publico"])):
            w.writerow([n, k["redactado"], k["publico"],
                        "mantener (figura en la web)" if k["publico"] and not k["redactado"] else "redactar salvo que lo apruebes"])
    tot = Counter()
    for r in resumen:
        for i, k in enumerate(("dni_nie", "iban", "cuenta", "tarjeta", "telefono", "direccion", "cp", "nacimiento",
                               "enlace_privado", "correo", "nombres")):
            tot[k] += r[6 + i]
    print(f"{len(resumen)} documentos anonimizados. Redacciones:", dict(tot))
    print(f"Nombres públicos sembrados desde la web: {len(publicos)}")


if __name__ == "__main__":
    main()
