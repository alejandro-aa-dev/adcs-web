# ADCS Web — Memory Index

**INICIO DE SESIÓN:** leer este archivo, esperar instrucciones. Nada más.

---

## Project status
Website for ADCS Sevilla (oboe/fagot association). Static HTML/CSS; final hosting is Hostalia (GitHub = dev repo only).
Up to date status, pending tasks and deployment: see README.md. Pending items depend mostly on the Junta (DNS/Cloudflare, legal data, photos, real content for /socios/).

## Design rules (CRITICAL)
- Oboe mention → `.txt-oboe` (green #4a9e6b) | Fagot mention → `.txt-fagot` (blue #3bbfcc)
- NO emoji decorations in content cards ("huele a IA") | emoji only: footer social + `📷` placeholders
- Photo placeholders: `<div class="img-placeholder"><!-- Reemplazar por <img/> --></div>`
- CTA "Hazte socio" at end of most pages (except hazte-socio.html itself)
- Fonts: Playfair Display (700,900) headers | Inter (400-700) body — self-hosted in assets/fonts/, never Google Fonts
- Logo: two versions needed (logo-claro.png for light bg, logo-oscuro.png for dark)

## User style
Spanish language, direct/fast iteration, prefers HTML preview, using Claude Code.
