# Guía: proteger el área de socios con Cloudflare Access

Documento para la Junta de la ADCS. Explica **qué se decide, qué se hace y cuánto cuesta** para
que solo los socios y socias puedan entrar en `adcsevilla.es/socios/`.

## 1. Por qué hace falta

Ahora mismo las páginas de `/socios/` son públicas: cualquiera con el enlace puede verlas.
Mientras eso sea así **no se puede subir contenido real** (vídeos de alumnado, actas, cuentas,
partituras con derechos) ni datos de socios.

Cloudflare Access pone una puerta delante de esa carpeta: la persona escribe su correo, recibe un
código de 6 cifras y entra. Cada socio entra con su propio correo, de modo que **se puede dar de
baja a una persona concreta** sin cambiar nada para el resto (con una contraseña compartida, no).

## 2. Qué implica la decisión

| | |
|---|---|
| **Coste** | 0 €. El plan gratuito de Cloudflare (Zero Trust) admite hasta 50 usuarios. |
| **Qué cambia** | Quién resuelve el DNS de `adcsevilla.es`: pasa a ser Cloudflare. La web sigue alojada en Hostalia. |
| **Riesgo** | Si al cambiar el DNS se olvida copiar algún registro (sobre todo los de **correo**, `MX`), el correo del dominio dejaría de funcionar. Se evita revisando la lista antes (paso 3). |
| **Límite** | Más de 50 socios con acceso → hay que pasar a un plan de pago (unos pocos euros por usuario y mes) o dar acceso solo a una parte. |
| **Privacidad** | Cloudflare pasa a ser encargado del tratamiento de los correos de los socios. Ya está previsto en `privacidad.html`. |

Quién debe decidirlo: la Junta. Quién necesita acceso al registrador del dominio: la persona
titular del dominio `adcsevilla.es`.

*(Las condiciones del plan gratuito pueden cambiar: conviene confirmarlas en la web de Cloudflare antes de decidir.)*

## 3. Pasos (los hace una persona con acceso al dominio)

### A. Preparar
1. Averigua **dónde está registrado el dominio** (el "registrador": Hostalia u otro) y quién tiene la cuenta.
2. Haz una **copia de todos los registros DNS actuales** (captura o exportación desde el panel del registrador). Apunta sobre todo: `A`/`CNAME` del sitio, `MX` (correo), `TXT` (SPF, verificación de Google).

### B. Alta en Cloudflare
3. Crea una cuenta en <https://dash.cloudflare.com> con un correo **de la asociación**, no personal (así no depende de una sola persona).
4. "Add a site" → `adcsevilla.es` → plan **Free**.
5. Cloudflare importa los registros que detecta. **Compáralos con la copia del paso 2** y añade los que falten. No continúes hasta que coincidan.
6. En cada registro del sitio web (`adcsevilla.es` y `www`), deja la nube **naranja** (proxy activado). Los registros `MX` van siempre en gris (solo DNS).

### C. Cambiar los nameservers
7. Cloudflare te dará dos nameservers (tipo `xxx.ns.cloudflare.com`). Cámbialos en el panel del registrador.
8. Espera a la propagación (de minutos a 24 h). Cloudflare avisará por correo cuando el dominio esté activo.
9. Comprueba que la web y el correo siguen funcionando.
10. En Cloudflare → SSL/TLS: modo **Full (strict)** (necesita que Hostalia tenga certificado SSL válido en el dominio).

### D. Proteger `/socios/`
11. Entra en <https://one.dash.cloudflare.com> → **Zero Trust** (elige un nombre de equipo, p. ej. `adcs`; plan Free).
12. **Access → Applications → Add an application → Self-hosted.**
    - Nombre: `Área de socios ADCS`
    - Dominio: `adcsevilla.es`, ruta: `socios/*` (añade otra entrada para `www.adcsevilla.es` si se usa).
    - Duración de sesión: 24 h o 1 semana (a gusto de la Junta).
13. **Política (Policy)**: acción *Allow*; regla *Include → Emails* con la lista de correos de socios.
14. **Método de login**: *One-time PIN* (activo por defecto, no hay que configurar nada más).
15. Guarda y prueba en una ventana privada: `https://adcsevilla.es/socios/` debe pedir el correo y mandar un código.

### E. Después
16. Solo entonces: subir el contenido real a `/socios/` (los documentos privados siguen en Google Drive con permisos restringidos; **nunca** en el repositorio de GitHub, que es público).
17. Actualizar `README.md` (Fase 2 hecha) y quitar el aviso "contenido de ejemplo".

## 4. Altas y bajas de socios

- **Alta:** al confirmar el pago de la cuota, añadir el correo a la política (Access → Policies → editar → añadir correo).
- **Baja:** quitar el correo de la lista. Pierde el acceso en cuanto caduca su sesión (se puede forzar en *Access → Users → Revoke*).
- **Cada curso (11 de septiembre):** revisar la lista y dejar solo a quienes han renovado.
- Mantener una **hoja de cálculo** con: nombre, correo, curso de alta, fecha de renovación. Es la fuente de verdad; la lista de Cloudflare es su reflejo. (Más adelante se puede automatizar con Apps Script y la API de Cloudflare, pero no merece la pena hasta que el proceso manual funcione.)

## 5. Limitaciones que conviene conocer

- Solo protege el tráfico que pasa por Cloudflare. Quien conozca la dirección IP directa del servidor de Hostalia podría saltarse la puerta. Para esta asociación es un riesgo bajo; se reduce no publicando esa IP.
- Protege la web, **no** los enlaces de Google Drive o YouTube: esos deben configurarse con sus propios permisos (Drive restringido a personas concretas; vídeos *no listados*, que no son secretos reales, solo no aparecen en búsquedas).
- Si algún socio no tiene o no quiere usar correo electrónico, no puede entrar.

## 6. Alternativa más simple (menos recomendable)

Contraseña única en el hosting (fichero `.htpasswd` de Apache en Hostalia). No requiere cambiar el DNS,
pero **no permite dar de baja a una persona** y la contraseña se acaba compartiendo fuera de la asociación.
Solo sería razonable como medida provisional.

## 7. Si algo sale mal

Para deshacer: en el registrador, vuelve a poner los nameservers originales (los apuntaste en el paso 1). Por eso es importante no borrar la copia del paso 2.
