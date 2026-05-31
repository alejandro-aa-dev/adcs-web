# ADCS Sevilla — Web

Sitio web estático de la **Asociación de Doble Caña de Sevilla (ADCS)**, entidad sin ánimo de lucro que une a profesores y alumnos de **oboe** y **fagot** de Sevilla y su provincia.

🌐 Web actual a sustituir: https://adcsevilla.es

---

## 📁 Estructura del proyecto

```
ADCS Web/
├── CONTEXT.md              ← Briefing completo del proyecto (LEE PRIMERO)
├── README.md               ← Este archivo
├── .gitignore
├── index.html              ← Página de inicio
├── quienes-somos.html      ← Quiénes somos
├── hazte-socio.html        ← Hazte socio/a 2025/26
│
└── (pendientes de crear)
    ├── v-concurso-2026.html
    ├── vii-encuentro-15.html
    ├── videos-orquestal.html
    ├── webs-amigas.html
    └── patrocinadores.html

└── assets/                 ← (Pendiente de crear)
    ├── css/
    │   └── styles.css      ← CSS compartido (refactor pendiente)
    └── img/
        ├── logo-claro.png  ← Logo para fondos claros
        ├── logo-oscuro.png ← Logo para fondos oscuros
        ├── junta/          ← Fotos de la junta directiva
        └── eventos/        ← Fotos de eventos
```

---

## 🚀 Cómo empezar a trabajar con Claude Code

1. Asegúrate de tener [Claude Code](https://claude.com/claude-code) instalado.
2. Abre una terminal (PowerShell, CMD o Git Bash) en esta carpeta:
   ```
   cd "C:\Users\admin\Documents\Claude\Projects\ADCS Web"
   ```
3. Ejecuta:
   ```
   claude
   ```
4. Lo primero que le dices: **"Lee CONTEXT.md para conocer el proyecto"**.
5. Luego puedes pedirle cualquier tarea, por ejemplo:
   - "Refactoriza el CSS a un archivo compartido en `assets/css/styles.css`"
   - "Crea la página `v-concurso-2026.html` siguiendo el mismo patrón que `quienes-somos.html`"
   - "Inicializa el repositorio Git, créame uno en mi cuenta de GitHub llamado `adcs-web` y sube todo"

---

## 🛠️ Desarrollo local

El proyecto es **HTML estático puro** — no hay build step, ni dependencias.

Para ver una página, basta con abrirla en el navegador (doble clic). O para una experiencia más profesional:

- **Con VS Code:** instala la extensión _Live Server_ y haz clic derecho sobre `index.html` → "Open with Live Server"
- **Con Python:** `python -m http.server 8000` y abre http://localhost:8000

---

## 🌐 Despliegue

**Recomendado:** GitHub Pages (gratis).

Una vez subido el proyecto a GitHub:

1. Ve a **Settings → Pages** del repositorio.
2. En "Source" elige **Deploy from a branch** → `main` → `/ (root)`.
3. Guardar. En un minuto tendrás la web en `https://[usuario].github.io/adcs-web/`.
4. Para usar el dominio `adcsevilla.es`:
   - En GitHub Pages, configura **Custom domain** → `adcsevilla.es`.
   - En tu proveedor de dominio, crea registros DNS tipo A apuntando a las IPs de GitHub Pages (185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153).
   - Espera la propagación DNS (de minutos a 48 h).

Alternativas igualmente buenas: **Netlify** o **Vercel** (drag & drop de la carpeta o conexión con GitHub).

---

## 🎨 Identidad visual

Los detalles completos están en `CONTEXT.md`, pero los colores principales son:

| Variable          | Color    | Uso                          |
|-------------------|----------|------------------------------|
| `--naranja`       | `#FFAB60`| Color principal de la marca  |
| `--oboe`          | `#4a9e6b`| Verde — color del oboe       |
| `--fagot`         | `#3bbfcc`| Azul — color del fagot       |

> ⚠️ El verde `#4a9e6b` es provisional. El usuario pasará el código exacto del logo original.

---

## ✍️ Convenciones de contenido

- La palabra **"oboe"** siempre va en verde con clase `.txt-oboe`.
- La palabra **"fagot"** siempre va en azul con clase `.txt-fagot`.
- **NO** usar emojis decorativos dentro de las tarjetas de contenido (huele a IA).
- Los espacios para fotos van marcados como `<div class="img-placeholder">` con un comentario indicando qué foto poner.

---

## 👤 Créditos

Diseño y desarrollo: **A. Álvarez** (Alejandro Álvarez Asencio, vocal de la ADCS).
