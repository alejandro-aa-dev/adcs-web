# ESTADO DEL PROYECTO — Web ADCS Sevilla

> **Este es el archivo que se lee al empezar cada sesión.** Resumen operativo y corto.
> El detalle técnico completo está en `README.md` (628 líneas). No dupliques información aquí.

**Última actualización:** 2026-09-08

---

## 1. Dónde estamos

Sitio estático puro (HTML + CSS, sin build) para sustituir la web de Blogger de la
Asociación de Doble Caña de Sevilla. **La estructura está terminada; lo que falta es
contenido real, decisiones de la Junta y el despliegue.**

- 10 páginas públicas + `404.html` — hechas
- 6 páginas del área de socios en `/socios/` — hechas, con **contenido de ejemplo**
- CSS compartido en `assets/css/styles.css`
- Logo real, favicon, SEO/Open Graph, `robots.txt`, `sitemap.xml`, `.htaccess` — hechos
- Responsive verificado (17 páginas × 4 anchos, 0 desbordamientos), imágenes optimizadas
- Repo de desarrollo: `github.com/alejandro-aa-dev/adcs-web` (rama `main`)
- **Hosting definitivo: Hostalia**, no GitHub Pages. Dominio `adcsevilla.es` sin apuntar aún.

---

## 2. Bloqueantes (no los toques sin decisión de la Junta)

| # | Bloqueante | De quién depende |
|---|-----------|------------------|
| 1 | Migrar DNS de `adcsevilla.es` a Cloudflare (prerrequisito de Cloudflare Access) | Junta |
| 2 | Configurar Cloudflare Access sobre `/socios/*` (email + OTP) | Junta / infra |
| 3 | Textos de aviso legal, privacidad y cookies (51 enlaces con `href="#"`) | Junta |
| 4 | Contenido real de `/socios/`: vídeos, Drive, actas, partituras, Forms | Junta |
| 5 | Subida a Hostalia y activación del dominio | Alejandro |

⚠️ **`/socios/` NO está protegido técnicamente.** Es HTML público. No subir ahí ningún
dato real de socios, acta, cuenta ni documento privado hasta que la Fase 2 esté activa.

---

## 3. Pendiente que sí se puede hacer ya

- **5 fotos de junta** en `assets/img/junta/`: `johanna.jpg`, `jesus-manuel.jpg`,
  `jacobo.jpg`, `alejandro.jpg`, `nuria.jpg` (solo existe `irene.jpg`)
- **3 imágenes de placeholder**: foto histórica (`quienes-somos.html`),
  foto de grupo (`hazte-socio.html`), cartel del concurso (`v-concurso-2026.html`)
✅ **Cuotas actualizadas al curso 2026/27** (20 € / 30 €, vigencia 11 sept 2026 → 10 sept 2027).

⏰ **Recordatorio anual:** las cuotas caducan cada **10 de septiembre**. Al renovar hay que
cambiar el año en `hazte-socio.html` (etiqueta de curso, periodo, concepto de transferencia
y los 3 metadatos SEO) y en los CTA de `index.html`, `quienes-somos.html`,
`v-concurso-2026.html`, `vii-encuentro-15.html` y `patrocinadores.html` — 13 sitios en total.

---

## 4. Trabajo en curso

**Análisis de la nueva web de AFOES (`https://nueva.afoes.es/`) como referencia de diseño.**
Rama: `claude/afoes-web-analysis-adcs-p52oc9`

- Estado: **bloqueado**. El entorno remoto de Claude Code no puede alcanzar ese dominio
  (403 del proxy de egress) y el subdominio no está indexado, así que no hay caché.
- Para desbloquear: permitir el dominio en la política de red del entorno, **o** que
  Alejandro suba un dump del HTML/CSS y lo adjunte en el chat
  (`curl.exe -sL <url> -o archivo.html` — en PowerShell hace falta el `.exe`,
  porque `curl` es alias de `Invoke-WebRequest`).
- Reserva metodológica ya planteada: AFOES es una asociación **nacional** con revista,
  editorial de partituras, congreso y foros. La ADCS es local y pequeña. Copiar su
  arquitectura de menú traería secciones vacías. Inspirarse sí, calcar no.

---

## 5. Reglas de diseño que no se rompen

- Mención de **oboe** → clase `.txt-oboe` (verde `#4a9e6b`).
  Mención de **fagot** → clase `.txt-fagot` (azul `#3bbfcc`). Naranja de marca: `#FFAB60`.
- **Sin emojis decorativos** en tarjetas de contenido ("huele a IA").
  Permitidos solo: redes en el footer y `📷` de placeholders.
- Tipografías: **Playfair Display** (700/900) títulos, **Inter** (400–700) cuerpo.
- CTA "Hazte socio/a" al final de casi todas las páginas (no en `hazte-socio.html`).
- Marcar el enlace activo del nav con `class="active"`.
- Placeholders: `<div class="img-placeholder"><!-- Reemplazar por <img/> --></div>`

---

## 6. Mapa de la documentación

| Archivo | Para qué sirve | Vigencia |
|---------|----------------|----------|
| `ESTADO_PROYECTO.md` | **Este archivo.** Estado operativo, leer al empezar sesión | ✅ Al día |
| `README.md` | Detalle técnico completo: página por página, componentes, despliegue | ✅ Al día |
| `ACCESIBILIDAD.md` | Registro de mejoras de accesibilidad | ✅ Al día |
| `CONTEXT.md` | Briefing original del proyecto (histórico) | ⚠️ Desactualizado |
| `MEMORY.md` | Antiguo índice de memoria | ❌ Sustituido por este archivo |

**Datos fijos** (contacto, junta directiva, IBAN, redes, Google Forms): en `CONTEXT.md`
§ correspondientes — esa parte sigue siendo válida, lo desactualizado es el estado de avance.

---

## 7. Log de sesiones

| Fecha | Qué se hizo |
|-------|-------------|
| 2026-08-28 | Optimización de imágenes, metadatos SEO/redes, navegación por teclado, favicon, 404, robots, sitemap, `.htaccess`; área de socios poblada con el archivo real de actividades |
| 2026-09-08 | Creado `ESTADO_PROYECTO.md`. Intento de análisis de `nueva.afoes.es` bloqueado por la política de red del entorno. Cuotas actualizadas al curso 2026/27 (13 referencias en 6 páginas) |
