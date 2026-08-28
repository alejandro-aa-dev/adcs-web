# Mejoras de Accesibilidad — ADCS Web

## Evaluación Inicial WAVE
**Puntuación:** 5.4/10
**Problema Principal:** "This page has no heading structure!"

### Problemas Identificados:
1. Falta de estructura jerárquica de encabezados (h1, h2, h3)
2. Salto de niveles: h1 → h5 (sin h2 intermedio)
3. Necesidad de envoltura semántica `<main>`

---

## Segunda Evaluación WAVE (tras arreglar encabezados)
**Puntuación:** 5.5/10
**Estructura:** ✅ Resuelta (WAVE detecta 1×h1, 2×h2, main, nav, footer)

### Desglose:
| Categoría | Cantidad |
|-----------|----------|
| Errors | 0 |
| Contrast Errors | 13 |
| Alerts | 2 |
| Structure | 8 |

### Decisión de diseño importante
Los **13 errores de contraste** provienen de los colores de marca de la ADCS
(naranja `#FFAB60`, azul `#3bbfcc`, verde `#4a9e6b`) usados como texto sobre
fondo blanco. Estos colores son **parte de la identidad visual de la ADCS y NO
se modifican**. Es un compromiso conocido: se prioriza la identidad de marca
sobre la puntuación máxima de contraste WCAG.

Por tanto, solo se corrigen los problemas de contraste y accesibilidad que **NO
afectan a los colores de marca**.

### Ratios de contraste de los colores de marca (sobre blanco)
| Color | Uso | Ratio | WCAG AA (4.5:1) |
|-------|-----|-------|-----------------|
| Naranja `#FFAB60` | "Doble Caña", estadísticas, botones | 1.87:1 | ❌ (se mantiene) |
| Azul `#3bbfcc` | "Sevilla", "fagot" | 2.21:1 | ❌ (se mantiene) |
| Verde `#4a9e6b` | "oboe" | 3.28:1 | ❌ (se mantiene) |

---

## Cambios Realizados

### Commit 1: Mejorar estructura de encabezados HTML (7fe8eeb)
**Archivos Modificados:**
- `index.html` — Agregado `<main>` alrededor del contenido principal
- `hazte-socio.html` — Cambio de h3 a h2 para "Cuota anual"
- `cv-alejandro-alvarez-asencio.html` — Agregados h2 para secciones:
  - Formación académica
  - Carrera como intérprete
  - Trayectoria docente
- `cv-irene-perez-cantillon.html` — Estructura similar a Alejandro

### Commit 2: Corregir estructura de encabezados en footer (c8cc176)
**Cambios Principales:**

#### HTML
- Cambio global: `<h5>Navegación</h5>` → `<h2>Navegación</h2>`
- Cambio global: `<h5>Más</h5>` → `<h2>Más</h2>`
- Aplicado en todos los 12 archivos HTML

**Archivos Afectados:**
```
area-socios.src.html
asociaciones.html
cv-alejandro-alvarez-asencio.html
cv-irene-perez-cantillon.html
hazte-socio.html
index.html
patrocinadores.html
quienes-somos.html
recursos.html
v-concurso-2026.html
vii-encuentro-15.html
```

#### CSS (assets/css/styles.css)
- Actualización: `.footer-col h5` → `.footer-col h2`
- Los estilos visuales se mantienen idénticos (tamaño, color, espaciado)

---

## Jerarquía de Encabezados Antes y Después

### ANTES (Problema)
```
h1 — Título principal
(sin h2)
(sin h3)
(sin h4)
h5 — Navegación / Más (en footer)
```

### DESPUÉS (Solucionado)
```
h1 — Título principal / Página header
  h2 — Secciones principales
    h3 — Subsecciones (cuando aplique)
  h2 — Navegación (footer)
  h2 — Más (footer)
```

---

## Resultados Esperados

✅ **Estructura semántica correcta:** Jerarquía h1 > h2 > h3 sin saltos
✅ **Acceso para lectores de pantalla:** Navegación clara mediante encabezados
✅ **WCAG Compliance:** Cumplimiento del criterio WCAG 2.1 1.3.1 (Info and Relationships)

---

## Validación

**Commits:**
- `7fe8eeb` — Mejora inicial: main tag + h2 en secciones
- `c8cc176` — Corrección global: footer h5 → h2

**Próximas Acciones:**
- Re-escanear con WAVE para verificar mejora en puntuación
- Verificar en navegadores múltiples
- Prueba con lector de pantalla (NVDA, JAWS, VoiceOver)

---

## Notas Técnicas

### ¿Por qué cambiar h5 a h2?
Los elementos `<h5>` en el footer representaban secciones principales (Navegación, Más), no subsecciones. La jerarquía semántica correcta requiere que sean h2 en relación al h1 de la página.

### CSS No Afectado
El cambio de h5 a h2 en HTML va acompañado de actualización de CSS selector para mantener la estética:
```css
/* Antes */
.footer-col h5 { ... }

/* Después */
.footer-col h2 { ... }
```

### Archivos `<main>`
Agregado en `index.html` y `cv-*.html` para envoltura semántica correcta del contenido principal.

---

## Resumen de Cambios

| Métrica | Antes | Después |
|---------|-------|---------|
| Archivos HTML | 12 | 12 |
| h1 por página | 1 | 1 |
| h2 por página | 0-2 | 2-5 |
| Saltos de nivel | Sí (h1→h5) | No |
| Tags `<main>` | Faltaba | Agregado |
| CSS actualizado | — | Sí (.footer-col) |

---

## Tercera Ronda: Correcciones SIN tocar colores de marca

Tras decidir mantener los colores de marca intactos, se corrigen los problemas
de accesibilidad restantes que NO dependen de dichos colores:

### 1. Contraste del texto atenuado del footer
- **Antes:** `.footer-bottom` usaba `rgba(255,255,255,0.4)` → 3.83:1 ❌
- **Después:** `rgba(255,255,255,0.6)` → ~6.95:1 ✅
- Afecta a: copyright "© 2026…" y créditos "Diseño y desarrollo:"
- Es texto blanco (no color de marca), así que su opacidad sí se ajusta.

### 2. Contraste del separador del breadcrumb
- **Antes:** `.breadcrumb .sep` (el "›") en `#bbb` → ~1.8:1 ❌
- **Después:** `#6f6f6f` → ~4.8:1 ✅
- Mejora el contraste en todas las páginas interiores (no es color de marca).

### 3. Alert "imagen con alt duplicado"
- El logo de la nav ya tiene `aria-label="Inicio ADCS"` en el enlace.
- Su `alt` (idéntico al del logo del footer) se vacía: `alt=""`.
- Patrón correcto: imagen decorativa dentro de un enlace ya etiquetado.
- Elimina la duplicación de texto alternativo.

### 4. Botón de menú hamburguesa sin etiqueta
- **Antes:** `<button class="menu-toggle">☰</button>` (sin nombre accesible útil)
- **Después:** `<button class="menu-toggle" aria-label="Abrir menú de navegación">`
- Aplicado en las 11 páginas con nav estándar.

### Alert que se mantiene (patrón estándar e inofensivo)
- **Enlace redundante:** el logo ("Inicio ADCS") y el enlace "Inicio" de la nav
  apuntan ambos a `index.html`. Es el patrón habitual de cualquier cabecera web
  (logo clicable + enlace de inicio). WAVE lo marca como *alert* (no *error*) y
  apenas afecta a la puntuación. Resolverlo perjudicaría la usabilidad.

---

## Resultado Esperado (3ª ronda)

| Categoría | 2ª eval. | Esperado 3ª eval. |
|-----------|----------|-------------------|
| Errors | 0 | 0 |
| Contrast Errors | 13 | ~11 (footer resuelto; resto = marca, intencional) |
| Alerts | 2 | ~1 (alt duplicado resuelto; redundante se mantiene) |
| AIM Score | 5.5 | ~6.5 |

> **Nota:** La puntuación queda limitada por la decisión consciente de conservar
> los colores de marca de la ADCS. Los errores de contraste restantes son
> intencionales y forman parte de la identidad visual de la asociación.

### Archivos modificados (3ª ronda)
- `assets/css/styles.css` — opacidad footer + color separador breadcrumb
- 11 archivos HTML — `alt=""` en logo nav + `aria-label` en botón menú


---

## Cuarta Ronda: navegación por teclado y preferencias del sistema

Estas correcciones tampoco tocan los colores de marca.

### 1. Foco visible por teclado (WCAG 2.4.7 / 2.4.11)
La hoja de estilos no definía ningún indicador de foco propio y varios componentes
(botones cápsula, tarjetas enlazadas, píldoras del subnav de socios) dejaban el
contorno por defecto del navegador casi invisible sobre el naranja.

```css
:focus-visible{outline:3px solid var(--texto);outline-offset:3px;border-radius:4px}
footer :focus-visible,.nota-legal :focus-visible{outline-color:#fff}
```

Se usa **negro sobre fondo claro (21:1)** y **blanco sobre el footer oscuro (18:1)**.
Ambos superan con holgura el 3:1 exigido para elementos no textuales, y ninguno de
los dos es un color de marca, así que la identidad visual queda intacta.

### 2. Enlace «Saltar al contenido» (WCAG 2.4.1)
El nav principal tiene 9 enlaces que un usuario de teclado o lector de pantalla
tenía que recorrer en cada página. Se añade como primer elemento del `<body>`
de las 17 páginas:

```html
<a class="skip-link" href="#contenido">Saltar al contenido</a>
```

El `<main>` pasa a ser `<main id="contenido" tabindex="-1">`. El enlace está fuera
de pantalla hasta que recibe el foco (`.skip-link:focus{top:0}`), así que no altera
el diseño visual.

### 3. Estado del menú móvil (WCAG 4.1.2)
El botón hamburguesa cambiaba la clase del menú, pero no comunicaba si estaba
abierto o cerrado. Ahora expone `aria-expanded` y `aria-controls`, y su etiqueta
alterna entre «Abrir» y «Cerrar menú de navegación».

### 4. Respetar «reducir movimiento» (WCAG 2.3.3)
Todas las tarjetas y botones se elevan con `transform:translateY(-2px)` al pasar el
ratón. Bajo `@media(prefers-reduced-motion:reduce)` se anulan transiciones,
animaciones y desplazamientos.

### 5. Enlaces externos
Los 56 enlaces con `target="_blank"` que no llevaban `rel` reciben
`rel="noopener noreferrer"`.

### 6. Estabilidad de la maquetación (CLS)
Los `<img>` del logo y de la foto de junta llevan ya `width`/`height` intrínsecos,
de modo que el navegador reserva el espacio antes de descargarlas y la página no
"salta" al cargar.

### 7. Desbordamiento horizontal en móvil
Auditoría automática de las 17 páginas a 320, 375, 414 y 768 px (68 comprobaciones).
Un único fallo real: en `hazte-socio.html` el IBAN llevaba `white-space:nowrap` y
empujaba la página 12 px fuera de la pantalla a 375 px. Se corrige permitiendo el
salto de línea solo en los espacios entre grupos de dígitos, de forma que ningún
grupo de cuatro cifras se parte:

```css
@media(max-width:520px){
  .bank-value.iban{white-space:normal;letter-spacing:1px;font-size:0.9rem}
}
```

Tras la corrección: **68/68 comprobaciones sin desbordamiento**.

---

## Pendiente

- **Re-escanear con WAVE** tras esta cuarta ronda.
- **Prueba con lector de pantalla** (NVDA o VoiceOver).
- Los errores de contraste que queden seguirán siendo los de los colores de marca,
  que se mantienen intencionadamente (ver la decisión de diseño más arriba).
