# Estado del DNS y del correo de adcsevilla.es (consultado el 31-oct-2026)

Consulta pública con `nslookup` contra 8.8.8.8. No hay acceso al panel de Hostalia: lo que figura aquí no sustituye a revisar el panel.

| Registro | Valor actual | Qué significa |
|---|---|---|
| NS | `ns10/ns11/ns12.servicio-online.net` | El DNS del dominio ya se gestiona en Hostalia (Dominio Absoluto). |
| A (`adcsevilla.es` y `www`) | `217.116.5.231` | La web apunta ya al hosting; hoy responde con una página vacía. |
| MX | `SMTP.GOOGLE.COM` (prioridad 1) | El correo `@adcsevilla.es`, si existe, lo recibe Google. |
| TXT (SPF) | `v=spf1 redirect=spf.dominioabsoluto.net` | Autoriza a enviar correo solo a los servidores de Hostalia, no a Google. |
| TXT (verificación) | `google-site-verification=_Ik06…` | Verificación de propiedad del dominio en Google. No borrar. |
| DKIM (`google._domainkey`) | no existe | Sin firma DKIM. |
| DMARC (`_dmarc`) | no existe | Sin política DMARC. |

## Qué hay que hacer al publicar la web
1. Subir `dist/adcs-web/` al hosting. La web ya apunta a esa IP: **no hace falta tocar el DNS**.
2. No borrar ni modificar el MX ni los TXT.
3. Activar SSL y después el bloque `mod_rewrite` de `.htaccess`.

## Cosas a revisar con la Junta (no urgentes)
- ¿Se usa algún correo `@adcsevilla.es`? Si no, el MX a Google es un resto sin uso. Si se usa, conviene ampliar el SPF para incluir a Google (`include:_spf.google.com`), activar DKIM en Google Workspace y publicar un DMARC; hoy un correo enviado desde Google con la dirección del dominio podría ir a spam.
- La dirección de contacto publicada en la web es `oboeyfagotsevilla@gmail.com`, que no depende del dominio.

## Web antigua
El blog está en `oboeyfagotsevilla.blogspot.com` y **no usa adcsevilla.es como dominio propio**, por lo que la nueva web no pisa sus direcciones y no hace falta mapa 301. El propio blog ya remite a `www.adcsevilla.es`. Recomendado: dejar el blog como archivo y añadirle un enlace destacado a la web nueva.
