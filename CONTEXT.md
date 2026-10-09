# Proyecto: Web ADCS Sevilla

## Sobre la organización

**Asociación de Doble Caña de Sevilla (ADCS)** — entidad sin ánimo de lucro fundada el 10 de diciembre de 2010, inscrita en el Registro Nacional de Asociaciones el 6 de junio de 2011 con el número **598607**.

Une a profesores y alumnos de **oboe** y **fagot** de Sevilla y su provincia. Organiza ciclos de cámara, masterclasses, talleres, concursos, conciertos y encuentros.

Web actual (a sustituir): https://adcsevilla.es (alojada en Blogger)
Diseñador/desarrollador del nuevo sitio: **A. Álvarez** (el propietario del proyecto, también vocal de la junta).

## Objetivo del proyecto

Sustituir la web de Blogger por un sitio estático (HTML/CSS sin build ni backend) en `adcsevilla.es`.
**Hosting definitivo: Hostalia** (GitHub es solo repositorio de desarrollo). Para el estado real
del proyecto, tareas pendientes y despliegue, ver `README.md`; para accesibilidad, `ACCESIBILIDAD.md`.

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

**REGLA IMPORTANTE:** Siempre que se mencione "oboe" en el texto, va con la clase `.txt-oboe` (verde). Siempre que se mencione "fagot", con `.txt-fagot` (azul). Los colores de marca no se modifican aunque fallen el contraste WCAG.

### Tipografías

- **Playfair Display** (700, 900) — títulos y números grandes
- **Inter** (400–700) — cuerpo de texto y UI

Autoalojadas en `assets/fonts/` y declaradas en `assets/css/fonts.css` (no usar Google Fonts).

### Logo

`assets/img/logo-claro.png` (nav y zonas claras) y `assets/img/logo-oscuro.png` (footer oscuro).

## Reglas de diseño y contenido

1. **NO usar iconos emoji decorativos** dentro de las tarjetas de contenido — "huele a IA". Los únicos emojis permitidos son los del footer (redes sociales) y los `📷/📸` de los placeholders de foto (porque son funcionales).

2. **Placeholders de foto:** cada vez que haya un sitio donde corresponda una foto, dejar un `<div class="img-placeholder">` o similar con instrucciones claras (`<!-- Reemplazar por <img src="..."/> -->`). El usuario meterá fotos reales (de eventos, junta directiva, etc.).

3. **Para los miembros de la junta directiva**, cada uno tendrá su foto personal (estilo "presentación de equipo" de una empresa). Mientras llegan las fotos, hay placeholders circulares.

4. **CTA "Hazte socio/a"** debe aparecer al final de la mayoría de páginas (excepto la propia página de Hazte Socio). El href se ajustará a la ruta real (`hazte-socio.html` o `/p/hazte-socio.html` según donde se aloje).

5. **Copyright:** © 2026 (y "Diseño y desarrollo: A. Álvarez" en el footer).

## Estructura del sitio

12 páginas públicas, 6 páginas del área de socios (`/socios/`), 3 páginas legales en borrador
(`aviso-legal`, `privacidad`, `cookies`) y `404.html`. Listado completo en `README.md`.

## Componentes comunes que se repiten en todas las páginas

1. **Nav superior fijo** con logo y enlaces; versión móvil con hamburguesa.
2. **Breadcrumb** ("Inicio › Nombre de página"), salvo en `index.html`.
3. **Page header** con `section-tag`, título grande y subtítulo.
4. **Footer** común: marca y redes / navegación / más enlaces, y barra inferior con copyright,
   enlaces legales y créditos.
5. **`section-tag`**: `.tag-naranja`, `.tag-oboe` (verde), `.tag-fagot` (azul).

El nav y el footer están duplicados en cada HTML: al cambiarlos hay que cambiarlos en todas las páginas.

## Datos de contacto

- **Email:** oboeyfagotsevilla@gmail.com
- **Facebook:** https://www.facebook.com/adcsevilla/
- **Instagram:** https://www.instagram.com/adcsevilla/
- **WhatsApp (grupo de difusión):** https://www.whatsapp.com/channel/0029Va8ocKGGJP8EXYqmqn34

## Junta directiva 2026/27

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
- **Concepto:** `CUOTA ADCS 2026-27 — [DNI DEL SOCIO/A]`

## Cuotas 2026/27

- 20€ individual
- 30€ dos hermanos/as
- Vigencia: 11 sept 2026 → 10 sept 2027

## Formulario de inscripción (Google Forms)

https://docs.google.com/forms/d/e/1FAIpQLSfpWCU81MLHCoMFYFMkvD-0xaCaBvAaudAu87r45o8hEFq3Rw/viewform

## Estilo de comunicación del usuario

- Habla en español
- Es directo y le gusta iterar rápido
- Prefiere preview HTML estándar para trabajar (no la versión XML de Blogger)
- Va a usar Claude Code para terminar el proyecto
