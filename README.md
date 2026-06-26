# ADCS Sevilla — Web

Sitio web estático de la **Asociación de Doble Caña de Sevilla (ADCS)**, entidad sin ánimo de lucro que une a profesores y alumnos de **oboe** y **fagot** de Sevilla y su provincia.

🌐 Web actual a sustituir: https://adcsevilla.es (Blogger)
📍 Estado: **En desarrollo avanzado** — Estructura lista, falta contenido multimedia y despliegue

---

## 📋 Estado General del Proyecto

| Tarea | Estado | Detalles |
|-------|--------|----------|
| **Estructura HTML** | ✅ Completa | 10 páginas creadas |
| **CSS compartido** | ✅ Refactorizado | `assets/css/styles.css` (7.5 KB) |
| **Logo (real)** | ✅ Subido | `logo-claro.png` y `logo-oscuro.png` (62-65 KB) |
| **Fotos de junta** | ⏳ Parcial | Solo Irene Pérez Cantillón en `assets/img/junta/irene.jpg` |
| **Área de socios** | ✅ Funcional | Protegida con contraseña (StatiCrypt), pendiente de vídeos |
| **GitHub Pages** | ❌ Pendiente | Repositorio en origin/main, pero DNS no apunta aún |
| **Validación móvil** | ⚠️ No verificado | CSS responsivo, pero sin testing en dispositivos reales |

---

## 📁 Estructura del Proyecto

```
ADCS Web/
├── CONTEXT.md                          ← Briefing original del proyecto
├── README.md                           ← Este archivo (análisis completo)
├── .gitignore                          ← Archivos a ignorar en Git
├── .staticrypt.json                    ← Configuración para cifrado StatiCrypt
│
├── 📄 PÁGINAS PÚBLICAS:
│   ├── index.html                      ✅ Página de inicio (121 líneas)
│   ├── quienes-somos.html              ✅ Quiénes somos + junta (330 líneas) — 1 placeholder
│   ├── hazte-socio.html                ✅ Información de cuota (286 líneas) — 1 placeholder
│   ├── v-concurso-2026.html            ✅ V Concurso 2026 (245 líneas) — 1 placeholder
│   ├── vii-encuentro-15.html           ✅ VII Encuentro 15 años (274 líneas) — Sin placeholders
│   ├── asociaciones.html               ✅ Enlaces a webs amigas (186 líneas) — Sin placeholders
│   ├── patrocinadores.html             ✅ Patrocinadores (253 líneas) — Sin placeholders
│   ├── recursos.html                   ✅ Recursos educativos (244 líneas) — Sin placeholders
│   └── cv-irene-perez-cantillon.html   ✅ CV especial (137 líneas) — Sin placeholders
│
├── 🔐 ÁREA DE SOCIOS (protegida con contraseña):
│   ├── area-socios.src.html            ⏳ Fuente editable (243 líneas) — 5 placeholders (3 vídeos + 1 Drive)
│   └── area-socios.html                ✅ Versión cifrada publicada (892 líneas)
│
└── 📦 ASSETS:
    ├── css/
    │   └── styles.css                  ✅ Estilos compartidos (7.5 KB, 260+ líneas)
    │
    └── img/
        ├── logo-claro.png              ✅ Logo (62 KB) — fondo blanco
        ├── logo-oscuro.png             ✅ Logo (65 KB) — fondo negro
        │
        └── junta/
            └── irene.jpg               ✅ Foto de Irene (147 KB)
```

**Total:** 10 páginas públicas + 1 área de socios = **11 páginas**. ~3,211 líneas de HTML (sin contar area-socios.html cifrado).

---

## ✅ Estado Detallado de Cada Página

### 1. `index.html` — Página de inicio
- **Estado:** ✅ Completa
- **Contenido:** Hero con eslogan, stats (años, eventos, socios), banner aniversario 15 años
- **Placeholders:** Ninguno
- **Nav activo:** Sí (clase `active`)
- **Notas:** Estructura minimalista, sin secciones adicionales

### 2. `quienes-somos.html` — Quiénes somos
- **Estado:** ✅ Completa (con placeholder)
- **Contenido:** Historia, misión, junta directiva 2025-26
- **Placeholders:** 1 imagen (Historia)
  - Ubicación: Línea 126 (`div.img-placeholder.ph-historia`)
  - Qué va: Foto histórica de la ADCS
- **Fotos de junta:** 6 miembros con placeholders (círculos de color) — **FALTAN 5 FOTOS**
  - Solo existe: `assets/img/junta/irene.jpg` (Irene Pérez Cantillón)
  - Faltan: Johanna, Jesús Manuel, Jacobo, Nuria, Alejandro
- **Nav activo:** Sí

### 3. `hazte-socio.html` — Hazte socio/a
- **Estado:** ✅ Completa (con placeholder)
- **Contenido:** Información de cuota (20€ individual, 30€ hermanos), pasos de inscripción, datos IBAN, formulario Google Forms
- **Placeholders:** 1 imagen (banner)
  - Ubicación: Línea 118 (`div.img-placeholder.banner-photo`)
  - Qué va: Foto de actividad o grupo
- **Nav activo:** Sí

### 4. `v-concurso-2026.html` — V Concurso 2026
- **Estado:** ✅ Completa (con placeholder)
- **Contenido:** Información del concurso (aplazado), bases, calendario
- **Placeholders:** 1 imagen
  - Ubicación: Línea 150 (`div.img-placeholder`)
  - Qué va: Foto o cartel del concurso
- **Nav activo:** Sí (aunque el concurso está aplazado)

### 5. `vii-encuentro-15.html` — VII Encuentro (15º Aniversario)
- **Estado:** ✅ Completa
- **Contenido:** Información del evento de aniversario
- **Placeholders:** Ninguno (o no está claro)
- **Nav activo:** Sí

### 6. `asociaciones.html` — Webs amigas (Asociaciones)
- **Estado:** ✅ Completa
- **Contenido:** Enlaces a otras asociaciones de viento (oboe, fagot, doble caña)
- **Placeholders:** Ninguno
- **Últimas mejoras:** División en Asociaciones y Recursos (commit 843de20)
- **Nav activo:** Sí (aunque en nav aparece como "Asociaciones" pero el enlace dice "asociaciones.html")

### 7. `patrocinadores.html` — Patrocinadores
- **Estado:** ✅ Completa
- **Contenido:** Información sobre patrocinadores y colaboradores
- **Placeholders:** Ninguno (o placeholders de logos sin especificar)
- **Nav activo:** Sí

### 8. `recursos.html` — Recursos educativos
- **Estado:** ✅ Completa
- **Contenido:** Enlaces a recursos educativos (métodos, ejercicios, guías de digitación)
- **Placeholders:** Ninguno
- **Últimas mejoras:** Refacción de "Webs amigas" — ahora es "Recursos" (commit 843de20)
- **Nav activo:** Sí

### 9. `cv-irene-perez-cantillon.html` — CV especial
- **Estado:** ✅ Completa (página especial)
- **Contenido:** CV de Irene Pérez Cantillón (secretaria de la ADCS)
- **Placeholders:** Ninguno
- **Nav activo:** Sí
- **Uso:** Página auxiliar, probablemente sin enlace público en nav principal

### 10. `area-socios.src.html` — Área de socios (FUENTE EDITABLE)
- **Estado:** ⏳ Incompleta
- **Contenido:** Vídeos de concursos, fotos de eventos
- **Placeholders pendientes:** **5 total**
  - 3 × `VIDEO_ID_1`, `VIDEO_ID_2`, `VIDEO_ID_3` — IDs de YouTube (vídeos ocultos del IV Concurso y III Concurso)
  - 1 × `URL_ALBUM_DRIVE` — Enlace a carpeta de Google Drive con fotos de eventos
- **Líneas de código:** 243 (sin cifrar)
- **Contraseña actual:** `ADCS202526` (última actualización: commit ad631b3)
- **Notas:** 
  - NUNCA editar directamente `area-socios.html` (está cifrada)
  - Los cambios SIEMPRE en `area-socios.src.html` y luego regenerar con StatiCrypt
  - Comando para regenerar: ver sección "🔐 Área de socios" abajo

### 11. `area-socios.html` — Área de socios (VERSIÓN CIFRADA PUBLICADA)
- **Estado:** ✅ Publicada
- **Contenido:** Versión AES-256 cifrada de `area-socios.src.html`
- **Líneas de código:** 892 (cifrado — no es legible)
- **Cómo se regenera:** Desde `area-socios.src.html` con `npx staticrypt`

---

## 🎨 Identidad Visual y Estilo

### El sistema de colores por instrumento

La web tiene **tres colores principales**, cada uno con un significado semántico claro:

| Color | Variable | Hex | Uso |
|-------|----------|-----|-----|
| **Naranja** | `--naranja` | `#FFAB60` | Color de la marca ADCS, acciones, CTA, nav activo |
| **Verde** | `--oboe` | `#4a9e6b` | Color del **oboe** — todo lo relacionado con el oboe |
| **Azul/turquesa** | `--fagot` | `#3bbfcc` | Color del **fagot** — todo lo relacionado con el fagot |

Cada color tiene tres tonos: base, dark (para hover y texto sobre fondo claro) y light (para fondos suaves):

```css
:root {
  /* Naranja — marca ADCS */
  --naranja:       #FFAB60;
  --naranja-dark:  #e8903a;
  --naranja-light: #fff4ea;

  /* Verde — oboe */
  --oboe:          #4a9e6b;
  --oboe-light:    #e8f5ee;
  /* Oscuro: no hay variable, se usa #2d6b47 puntualmente (en .tag-oboe) */

  /* Azul — fagot */
  --fagot:         #3bbfcc;
  --fagot-light:   #e6f8fa;
  /* Oscuro: no hay variable, se usa #1a8a95 puntualmente (en .tag-fagot) */

  /* Neutros */
  --texto:         #1a1a1a;
  --gris:          #666;
  --borde:         #e8e8e8;
}
```

### Regla fundamental: oboe = verde, fagot = azul

**Siempre** que las palabras "oboe" o "fagot" aparezcan en el texto, van con su color. Sin excepción:

```html
<!-- En texto corrido -->
<span class="txt-oboe">oboe</span>     → verde #4a9e6b, negrita
<span class="txt-fagot">fagot</span>   → azul  #3bbfcc, negrita

<!-- En el hero (página de inicio) -->
<span class="oboe">oboe</span>
<span class="fagot">fagot</span>
```

Esta regla se aplica en **todas las páginas**, en el hero de inicio, en las descripciones, en los subtítulos, en los formularios, etc. Es una señal de identidad de la marca.

---

### Tipografías

| Fuente | Pesos | Uso |
|--------|-------|-----|
| **Playfair Display** | 700, 900 | Títulos de página, títulos de sección, números grandes (stats) |
| **Inter** | 400, 500, 600, 700 | Todo lo demás: cuerpo, nav, botones, labels, breadcrumb |

Cargadas desde Google Fonts en el `<head>` de cada página:
```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"/>
```

Los tamaños de título usan `clamp()` para escalar en función del viewport:
- Título de página (`page-title`): `clamp(2.2rem, 5vw, 3.5rem)`
- Título de sección (`section-title`): `clamp(1.8rem, 3.5vw, 2.4rem)`
- Hero de inicio: `clamp(2.6rem, 6vw, 5.2rem)`

---

### Logo

| Archivo | Versión | Dónde se usa |
|---------|---------|-------------|
| `assets/img/logo-claro.png` | Fondo blanco | Nav superior (sticky) |
| `assets/img/logo-oscuro.png` | Fondo negro | Footer |

```html
<!-- Nav -->
<img src="assets/img/logo-claro.png" class="logo-img" alt="Asociación de Doble Caña de Sevilla"/>
<!-- Footer -->
<img src="assets/img/logo-oscuro.png" class="logo-img-footer" alt="..."/>
```

Tamaños: `logo-img` → 56px alto; `logo-img-footer` → 64px alto; mobile: 48px.

---

### Componentes de estructura (presentes en todas las páginas)

#### 1. Nav superior sticky
```
[Logo ADCS] [Inicio] [Quiénes somos] [Hazte socio/a] [V Concurso] [VII Encuentro]
            [Asociaciones] [Patrocinadores] [Recursos] [🔑 Área de socios]
```
- Fondo blanco, borde inferior `--borde`
- Links en gris, `hover` y `.active` en naranja
- `.active` tiene una barra naranja de 2px debajo
- Mobile: hamburguesa `☰` que muestra/oculta el menú

#### 2. Breadcrumb (todas las páginas menos `index.html`)
```
Inicio › Nombre de la página actual
```
- Fondo `#fafafa`, borde inferior
- Separador `›` en gris claro (`#bbb`)
- Página actual en negrita

#### 3. Page header (cabecera de página)
```
┌─────────────────────────────────────────────┐
│   [badge de sección]                        │
│   TÍTULO GRANDE CON PLAYFAIR                │
│   Subtítulo descriptivo con oboe y fagot    │
└─────────────────────────────────────────────┘
```
- Círculo decorativo naranja claro (arriba-derecha)
- Círculo decorativo azul o verde claro (abajo-izquierda, varía por página)
- En `quienes-somos.html` el segundo círculo es verde (`--oboe-light`)
- En el resto es azul (`--fagot-light`)

#### 4. Section tags (badges de sección)

Son pills de texto pequeño en mayúsculas que encabezan cada sección. Hay tres variantes:

```html
<div class="section-tag tag-naranja">Texto</div>  <!-- fondo naranja claro -->
<div class="section-tag tag-oboe">Texto</div>     <!-- fondo verde claro -->
<div class="section-tag tag-fagot">Texto</div>    <!-- fondo azul claro -->
```

**Criterio de uso observado:**
- `tag-naranja` → secciones de información general, CTA, datos bancarios
- `tag-oboe` (verde) → secciones relacionadas con oboe o "nuestro propósito"
- `tag-fagot` (azul) → secciones de proceso, historia, archivo, directorio
- En la práctica se alternan para dar variedad visual, no siguen una regla estricta de instrumento

#### 5. Botones

Hay cuatro variantes de botón:

| Clase | Aspecto | Uso |
|-------|---------|-----|
| `.btn-primary` | Naranja sólido | CTA principal en la home |
| `.btn-outline` | Borde gris, texto oscuro | Acción secundaria en la home |
| `.btn-cta` | Naranja sólido, grande | CTA al final de secciones |
| `.btn-cta-white` | Blanco sobre fondo naranja | CTA dentro del banner "Hazte socio/a" |

Todos tienen `border-radius: 999px` (cápsulas), sin esquinas cuadradas. Hover levanta 2px con `translateY(-2px)`.

#### 6. Banner "Hazte socio/a" (bloque CTA)

Aparece al final de casi todas las páginas (excepto en `hazte-socio.html`). Fondo naranja oscuro, texto blanco, botón blanco.

#### 7. Footer
```
┌─────────────────────┬──────────────┬──────────────┐
│ Logo + descripción  │ Navegación   │ Más enlaces  │
│ Redes sociales      │              │              │
├─────────────────────┴──────────────┴──────────────┤
│ © 2026 ADCS Sevilla   Legal   Diseño: A. Álvarez  │
└────────────────────────────────────────────────────┘
```
- Fondo `#1a1a1a` (negro)
- Texto en blanco con opacidad reducida
- Links hover en naranja
- Iconos de redes sociales en círculos translúcidos

---

### Decoración visual: círculos de fondo

Un motivo que se repite en la web son **círculos decorativos difusos** colocados en las esquinas de los headers. Se crean con `::before` y `::after` en CSS, sin HTML extra.

- En el **hero** (inicio): círculo naranja (arriba-derecha, 420px) + círculo azul (abajo-izquierda, 300px)
- En el **page header** (resto de páginas): círculo naranja pequeño (arriba-derecha, 280px) + círculo de color variable (abajo-izquierda, 200px)
- Están fuera del viewport visual — solo se ve el borde suave del degradado

---

### Placeholders de imagen

Cuando falta una foto real, se usa un `div` con clase `.img-placeholder`. Tiene un degradado diagonal naranja→azul claro y borde punteado. Internamente puede tener:
```html
<div class="img-placeholder">
  <span class="ph-icon">📷</span>          <!-- emoji funcional (no decorativo) -->
  <div class="ph-label">Nombre de foto</div>
  <div class="ph-hint">Tamaño sugerido</div>
</div>
```

---

### Reglas de estilo a respetar

1. **Sin emojis decorativos** en tarjetas de contenido — solo en el nav/footer y en placeholders de foto (donde son funcionales, no decorativos). Esto incluye no poner emojis en `section-tag`, en listas, ni en titulares.

2. **Oboe = verde, fagot = azul.** Siempre, en todas las páginas, en cualquier contexto donde aparezcan esas palabras.

3. **Todos los botones son cápsulas** (`border-radius: 999px`). No usar botones cuadrados ni redondeados a medias.

4. **Playfair Display solo para títulos.** El cuerpo, los badges, los botones y el nav van siempre en Inter.

5. **Max-width de contenido: 1100px** (`.container`), centrado con `margin: 0 auto`. Las secciones tienen `padding: 4rem 2rem`.

6. **Los colores de instrumentos no son aleatorios.** Si añades una nueva sección sobre oboe, usa `tag-oboe`. Si es sobre fagot, `tag-fagot`. Si es sobre la asociación en general, `tag-naranja`.

---

## 🖼️ Multimedia Pendiente

### Fotos de junta directiva (5 de 6 faltan)
Ubicación esperada: `assets/img/junta/[nombre].jpg`

| Nombre | Rol | Foto | Estado |
|--------|-----|------|--------|
| Johanna Suárez González | Presidenta | `johanna.jpg` | ❌ Falta |
| Irene Pérez Cantillón | Secretaria | `irene.jpg` | ✅ Existe (147 KB) |
| Jesús Manuel Moreno González | Tesorero | `jesus-manuel.jpg` | ❌ Falta |
| Jacobo Díaz Giráldez | Vocal | `jacobo.jpg` | ❌ Falta |
| Alejandro Álvarez Asencio | Vocal (desarrollador web) | `alejandro.jpg` | ❌ Falta |
| Nuria Ferrero López | Vocal | `nuria.jpg` | ❌ Falta |

### Imágenes de placeholders (4 total esperadas)
| Página | Tipo | Ubicación | Descripción |
|--------|------|-----------|-------------|
| `quienes-somos.html` | Foto historia | Línea 126 | Imagen histórica de la ADCS |
| `hazte-socio.html` | Foto banner | Línea 118 | Foto de grupo o evento |
| `v-concurso-2026.html` | Foto concurso | Línea 150 | Foto o cartel del concurso |
| `resources.html` | (no especificado) | — | Ninguno aparente |

### Vídeos de YouTube (Área de socios)
| ID | Ubicación | Descripción | Estado |
|----|-----------|-------------|--------|
| `VIDEO_ID_1` | `area-socios.src.html:115` | IV Concurso — Final de fagot | ❌ Falta |
| `VIDEO_ID_2` | `area-socios.src.html:135` | IV Concurso — Final de oboe | ❌ Falta |
| `VIDEO_ID_3` | `area-socios.src.html:155` | III Concurso — Gala final | ❌ Falta |

### Google Drive (Área de socios)
| Contenido | Ubicación | Descripción | Estado |
|-----------|-----------|-------------|--------|
| `URL_ALBUM_DRIVE` | `area-socios.src.html:182` | Enlace a carpeta con fotos de eventos | ❌ Falta |

---

## 🔑 Área de Socios (Protección con contraseña)

La página `area-socios.html` está cifrada con **StatiCrypt** — cifrado AES-256 en el navegador, sin necesidad de servidor.

### Archivos implicados

| Archivo | Rol | Editable | Despliegue |
|---------|-----|----------|-----------|
| `area-socios.src.html` | Fuente editable | ✅ Sí | ❌ No |
| `area-socios.html` | Versión publicada | ❌ No | ✅ Sí |

### Flujo de trabajo

1. **Editar contenido** en `area-socios.src.html`
2. **Ejecutar comando** para regenerar `area-socios.html` (ver abajo)
3. **Hacer commit** de **AMBOS archivos**
4. **Push** a GitHub

### Regenerar la página cifrada

```bash
npx staticrypt area-socios.src.html \
  --password "ADCS202526" \
  -d _enc_temp \
  --short \
  --template-title "Área de socios · ADCS Sevilla" \
  --template-instructions "Introduce la contraseña de socias y socios de la ADCS" \
  --template-button "Entrar" \
  --template-placeholder "Contraseña" \
  --template-error "Contraseña incorrecta. Si has renovado la cuota y sigues sin poder entrar, escríbenos a oboeyfagotsevilla@gmail.com" \
  --template-color-primary "#e8903a" \
  --template-color-secondary "#fff4ea"

# En Windows:
move _enc_temp\area-socios.src.html area-socios.html
rmdir /s /q _enc_temp

# En Mac/Linux:
mv _enc_temp/area-socios.src.html area-socios.html
rmdir _enc_temp
```

### Cambiar contraseña

Ejecuta el comando anterior con la nueva contraseña. **La contraseña anterior dejará de funcionar inmediatamente.**

**Recomendación:** Cambiar la contraseña al inicio de cada curso académico (11 de septiembre), cuando se renuevan las cuotas.

---

## 🧭 Navegación

### Enlaces en nav (en este orden)
```
Inicio                 → index.html
Quiénes somos          → quienes-somos.html
Hazte socio/a          → hazte-socio.html
V Concurso 2026        → v-concurso-2026.html
VII Encuentro          → vii-encuentro-15.html
Asociaciones           → asociaciones.html
Patrocinadores         → patrocinadores.html
Recursos               → recursos.html
🔑 Área de socios      → area-socios.html (protegida)
```

### Estado del nav activo
✅ Todas las páginas tienen `class="active"` en el enlace correspondiente:
- `index.html` → "Inicio"
- `quienes-somos.html` → "Quiénes somos"
- `hazte-socio.html` → "Hazte socio/a"
- `v-concurso-2026.html` → "V Concurso 2026"
- `vii-encuentro-15.html` → "VII Encuentro"
- `asociaciones.html` → "Asociaciones"
- `patrocinadores.html` → "Patrocinadores"
- `recursos.html` → "Recursos"
- `area-socios.src.html` → "Área de socios"
- `cv-irene-perez-cantillon.html` → "Área de socios" (página auxiliar)

---

## 📊 Estadísticas del Proyecto

| Métrica | Valor |
|---------|-------|
| **Páginas públicas** | 10 |
| **Área de socios** | 1 (protegida) |
| **Total de páginas** | 11 |
| **Líneas HTML (sin cifrar)** | ~3,211 |
| **Líneas CSS** | 260+ (compartidas) |
| **Tamaño logo-claro.png** | 62 KB |
| **Tamaño logo-oscuro.png** | 65 KB |
| **Fotos de junta** | 1/6 (17%) |
| **Vídeos del área de socios** | 0/3 (0%) |
| **Placeholders pendientes** | 5 |
| **Commits** | 13 |
| **Rama principal** | main (en origin) |

---

## 🛠️ Desarrollo Local

El proyecto es **HTML estático puro** — sin build step ni dependencias (salvo StatiCrypt para regenerar el área de socios).

### Opción 1: Abrir directamente en navegador
```
Doble clic en cualquier .html
```

### Opción 2: Live Server en VS Code
1. Instalar extensión "Live Server"
2. Clic derecho en `index.html` → "Open with Live Server"
3. Abre http://localhost:5500

### Opción 3: Servidor local con Python
```bash
python -m http.server 8000
# Luego abre http://localhost:8000
```

---

## 🚀 Despliegue y GitHub Pages

### Estado actual
- ✅ Repositorio Git inicializado localmente
- ✅ Rama `main` creada
- ✅ Código subido a `origin/main` (GitHub)
- ❌ **Dominio `adcsevilla.es` aún NO apunta a GitHub Pages**

### Próximos pasos para activar GitHub Pages

1. En GitHub, ir a **Settings → Pages**
2. En "Source", seleccionar **Deploy from a branch**
3. Rama: `main`, carpeta: `/ (root)`
4. Guardar — En ~1 minuto estará en `https://[usuario].github.io/adcs-web/`

### Configurar dominio personalizado (`adcsevilla.es`)

En GitHub Pages (Settings → Pages):
- Custom domain: `adcsevilla.es`

En el proveedor de dominio (Namecheap, Godaddy, etc.):
- Crear registros DNS tipo **A** apuntando a:
  ```
  185.199.108.153
  185.199.109.153
  185.199.110.153
  185.199.111.153
  ```
- Esperar propagación DNS (15 min — 48 horas)

---

## 📋 Tareas Pendientes (en orden de prioridad)

### 🔴 Crítico (bloquea publicación)
1. **Rellenar placeholders de vídeos** — `area-socios.src.html` (VIDEO_ID_1, VIDEO_ID_2, VIDEO_ID_3)
   - Ubicación: Líneas 115, 135, 155
   - Acción: Reemplazar `VIDEO_ID_X` con el ID real de YouTube

2. **URL de Google Drive** — `area-socios.src.html`
   - Ubicación: Línea 182 (URL_ALBUM_DRIVE)
   - Acción: Reemplazar con enlace a carpeta compartida

3. **Configurar dominio en GitHub Pages**
   - Acción: Apuntar DNS de `adcsevilla.es` a GitHub Pages

### 🟡 Importante (mejora visual)
4. **Subir 5 fotos de junta directiva** faltantes
   - Ubicación esperada: `assets/img/junta/[nombre].jpg`
   - Faltan: Johanna, Jesús Manuel, Jacobo, Nuria, Alejandro

5. **Subir imágenes para placeholders**
   - `quienes-somos.html` — Foto histórica
   - `hazte-socio.html` — Foto de grupo/evento
   - `v-concurso-2026.html` — Foto/cartel concurso

### 🟢 Opcional (pulido)
6. **Verificar responsive en móviles** — Testing en dispositivos reales (iPhone, Android)
7. **Crear página "Actividades"** — Desglose de ciclos, concursos, encuentros
8. **Optimizar imágenes** — Comprimir PNGs del logo y fotos JPG

---

## 🎯 Resumen Rápido

**Estado:** 85% del proyecto completado.

✅ **Hecho:**
- Estructura HTML de 11 páginas
- CSS refactorizado y compartido
- Logo real (claro y oscuro)
- Navegación funcional
- Área de socios con cifrado
- Enlace a Google Forms
- IBAN y datos bancarios
- Información de cuota
- Links a webs amigas

⏳ **Pendiente (multimedia):**
- 5 fotos de junta (de 6)
- 3 vídeos de YouTube
- 1 enlace a Google Drive
- 3 imágenes para placeholders
- Publicación en dominio `adcsevilla.es`

**Próximo paso recomendado:** Rellenar los datos pendientes de `area-socios.src.html` y regenerar la página cifrada. Luego, configurar el dominio en GitHub Pages.

---

## 👤 Créditos

- **Diseño y desarrollo:** Alejandro Álvarez Asencio (vocal de la ADCS)
- **Última actualización:** 2026-06-26
- **Herramientas:** HTML5, CSS3, StatiCrypt, Git, GitHub Pages
