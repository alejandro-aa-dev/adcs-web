# Mejoras de Accesibilidad — ADCS Web

## Evaluación Inicial WAVE
**Puntuación:** 5.4/10
**Problema Principal:** "This page has no heading structure!"

### Problemas Identificados:
1. Falta de estructura jerárquica de encabezados (h1, h2, h3)
2. Salto de niveles: h1 → h5 (sin h2 intermedio)
3. Necesidad de envoltura semántica `<main>`

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

