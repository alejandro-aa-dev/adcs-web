# Proyecto: Web ADCS Sevilla

## Sobre la organización

**Asociación de Doble Caña de Sevilla (ADCS)** — entidad sin ánimo de lucro fundada el 10 de diciembre de 2010, inscrita en el Registro Nacional de Asociaciones el 6 de junio de 2011 con el número **598607**.

Une a profesores y alumnos de **oboe** y **fagot** de Sevilla y su provincia. Organiza ciclos de cámara, masterclasses, talleres, concursos, conciertos y encuentros.

Web actual (a sustituir): https://adcsevilla.es (alojada en Blogger)
Diseñador/desarrollador del nuevo sitio: **A. Álvarez** (el propietario del proyecto, también vocal de la junta).

## Objetivo del proyecto

Reemplazar la web actual de Blogger por un sitio estático moderno, alojado en GitHub Pages (o similar), apuntando el dominio `adcsevilla.es` al nuevo hosting.

## Identidad visual

### Colores (variables CSS)

```css
:root{
  --naranja:#FFAB60;        /* Color principal de la marca */
  --naranja-dark:#e8903a;
  --naranja-light:#fff4ea;
  --oboe:#4a9e6b;           /* VERDE — color del oboe */
  --oboe-light:#e8f5ee;
  --fagot:#3bbfcc;          /* AZUL/turquesa — color del fagot */
  --fagot-light:#e6f8fa;
  --texto:#1a1a1a;
  --gris:#666;
  --borde:#e8e8e8;
}
```

**REGLA IMPORTANTE:** Siempre que se mencione "oboe" en el texto, va con la clase `.txt-oboe` (verde). Siempre que se mencione "fagot", con `.txt-fagot` (azul). El usuario mencionó que el verde del logo real es distinto al actual `#4a9e6b` — pendiente de que él pase el código exacto.

### Tipografías

- **Playfair Display** (700, 900) — títulos y números grandes
- **Inter** (400, 500, 600, 700) — cuerpo de texto y UI

Cargadas desde Google Fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"/>
```

### Logo

Hay dos versiones:
- **Logo fondo claro** (para nav y zonas claras): usar el archivo con texto blanco sobre fondo naranja
- **Logo fondo oscuro** (para footer negro): usar el archivo con texto negro sobre fondo naranja

En los HTML actuales hay un **SVG provisional aproximado** del logo que el usuario quiere reemplazar por las imágenes reales subidas al repo. Buscar el bloque `<!-- LOGO ADCS - VERSIÓN FONDO CLARO -->` y `<!-- LOGO ADCS - VERSIÓN FONDO OSCURO -->` para localizarlos.

## Reglas de diseño y contenido

1. **NO usar iconos emoji decorativos** dentro de las tarjetas de contenido — "huele a IA". Los únicos emojis permitidos son los del footer (redes sociales) y los `📷/📸` de los placeholders de foto (porque son funcionales).

2. **Placeholders de foto:** cada vez que haya un sitio donde corresponda una foto, dejar un `<div class="img-placeholder">` o similar con instrucciones claras (`<!-- Reemplazar por <img src="..."/> -->`). El usuario meterá fotos reales (de eventos, junta directiva, etc.).

3. **Para los miembros de la junta directiva**, cada uno tendrá su foto personal (estilo "presentación de equipo" de una empresa). Mientras llegan las fotos, hay placeholders circulares.

4. **CTA "Hazte socio/a"** debe aparecer al final de la mayoría de páginas (excepto la propia página de Hazte Socio). El href se ajustará a la ruta real (`hazte-socio.html` o `/p/hazte-socio.html` según donde se aloje).

5. **Copyright:** © 2026 (y "Diseño y desarrollo: A. Álvarez" en el footer).

## Estructura del sitio

Páginas (heredadas de la web actual):

| URL                       | Estado actual                                  |
|---------------------------|------------------------------------------------|
| `index.html`              | ✅ Hecha (versión simplificada, solo hero)     |
| `quienes-somos.html`      | ✅ Hecha (historia, misión, junta, datos)      |
| `hazte-socio.html`        | ✅ Hecha (cuota, pasos, banco, casos)          |
| `v-concurso-2026.html`    | ⏳ Pendiente — V Concurso 2026 (aplazado)      |
| `vii-encuentro-15.html`   | ⏳ Pendiente — VII Encuentro 15º Aniversario   |
| `videos-orquestal.html`   | ⏳ Pendiente — Vídeos de repertorio orquestal  |
| `webs-amigas.html`        | ⏳ Pendiente                                   |
| `patrocinadores.html`     | ⏳ Pendiente                                   |

## Componentes comunes que se repiten en todas las páginas

1. **Nav superior fijo** (sticky) con logo SVG a la izquierda y enlaces a las 8 páginas. Versión mobile: hamburguesa.

2. **Breadcrumb** ("Inicio › Nombre de página"). Excepto en `index.html`.

3. **Page header** con `section-tag` (badge de color), título grande y subtítulo.

4. **Footer** común — 3 columnas (marca + descripción + redes / navegación / más enlaces) + barra inferior con copyright, legales y créditos a A. Álvarez.

5. **Patrón de `section-tag`**:
   - `.tag-naranja` (fondo naranja claro)
   - `.tag-oboe` (verde claro)
   - `.tag-fagot` (azul claro)

## Datos de contacto

- **Email:** oboeyfagotsevilla@gmail.com
- **Facebook:** https://www.facebook.com/adcsevilla/
- **Instagram:** https://www.instagram.com/adcsevilla/
- **WhatsApp (grupo de difusión):** https://www.whatsapp.com/channel/0029Va8ocKGGJP8EXYqmqn34

## Junta directiva 2025/26

- **Presidenta:** Johanna Suárez González
- **Secretaria:** Irene Pérez Cantillón
- **Tesorero:** Jesús Manuel Moreno González
- **Vocal:** Jacobo Díaz Giráldez
- **Vocal:** Alejandro Álvarez Asencio (= A. Álvarez, propietario del proyecto)
- **Vocal:** Nuria Ferrero López

## Datos bancarios (para Hazte Socio)

- **Titular:** Asociación de Doble Caña de Sevilla
- **Caja:** Caja Rural
- **IBAN:** ES09 3187 0101 0851 5831 1919
- **BIC:** BCOEESMM187
- **Concepto:** `CUOTA ADCS 2025-26 — [DNI DEL SOCIO/A]`

## Cuotas 2025/26

- 20€ individual
- 30€ dos hermanos/as
- Vigencia: 11 sept 2025 → 10 sept 2026

## Formulario de inscripción (Google Forms)

https://docs.google.com/forms/d/e/1FAIpQLSfpWCU81MLHCoMFYFMkvD-0xaCaBvAaudAu87r45o8hEFq3Rw/viewform

## Próximos pasos pendientes (en orden sugerido)

### 1. Refactorización inicial (prioridad alta)

El código HTML actual repite los estilos CSS en cada archivo. Extraer todo el CSS a un único `assets/css/styles.css` compartido. Cada HTML solo debería tener un `<link rel="stylesheet" href="assets/css/styles.css"/>`.

Lo mismo con el SVG del logo y el nav/footer si se quiere ir más allá (en sitio estático puro se duplica; con un sistema de plantillas como Eleventy/Astro/Jekyll se podría extraer a un partial).

### 2. Crear las páginas pendientes

Seguir el mismo patrón estructural que `quienes-somos.html` y `hazte-socio.html`:

- Nav + Breadcrumb + Page Header + Secciones + CTA "Hazte socio" + Footer
- Sin iconos emoji decorativos
- Placeholders de foto donde corresponda
- Oboe/fagot siempre en sus colores
- Marcar el enlace activo del nav con `class="active"`

### 3. Subir el logo real

El usuario tiene dos versiones del logo (fondo claro y fondo oscuro). Crear `assets/img/logo-claro.png` (o .svg) y `assets/img/logo-oscuro.png`. Reemplazar los SVG provisionales del nav y footer por `<img>` con clase `logo-img`.

### 4. Configurar GitHub Pages

- `git init` en la carpeta del proyecto
- Crear repo en GitHub (sugerencia: `adcs-web` o `adcsevilla`)
- `git remote add origin ...`
- `git push -u origin main`
- En GitHub: Settings → Pages → Source: `main` branch
- Una vez funcionando, configurar dominio personalizado `adcsevilla.es` (DNS A records apuntando a GitHub Pages)

### 5. Página adicional sugerida

Una página de **Actividades** o **Qué hacemos** (extraída de la sección que había en la versión completa de la home) con detalle del Ciclo "José Antonio Pérez Madrigal", concursos, encuentros, etc.

## Estilo de comunicación del usuario

- Habla en español
- Es directo y le gusta iterar rápido
- Prefiere preview HTML estándar para trabajar (no la versión XML de Blogger)
- Va a usar Claude Code para terminar el proyecto

## Notas finales

El usuario tiene la conversación previa donde fuimos construyendo cada decisión paso a paso. El estado actual de cada página (HTML completo) está en los artefactos:

- `adcs_landing` — index.html (Inicio)
- `adcs_quienes_somos` — quienes-somos.html
- `adcs_hazte_socio` — hazte-socio.html

Estos artefactos se exportarán a archivos en el siguiente paso.
