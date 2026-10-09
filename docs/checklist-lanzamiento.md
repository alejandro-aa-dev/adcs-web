# Lista de comprobación del día del lanzamiento

Orden recomendado para pasar de la web de Blogger a la nueva en `adcsevilla.es`.
Marca cada paso cuando esté hecho.

## 0. Antes de tocar nada
- [ ] Respondido el `cuestionario-junta.md` y completadas las páginas legales (sin `[PENDIENTE]`).
- [ ] Aprobadas por la Junta `aviso-legal`, `privacidad` y `cookies`. Quitado el aviso de borrador y el `noindex`, y añadidas a `sitemap.xml`.
- [ ] Las tres fotos de junta y las tres imágenes de placeholder, subidas.
- [ ] Decidido lo de Cloudflare (ver `guia-cloudflare-access.md`). **Si no está activo, `/socios/` no debe llevar contenido real.**
- [ ] Copia de seguridad de la web actual de Blogger (Configuración → Gestionar blog → Hacer copia de seguridad).
- [ ] Copia de los registros DNS actuales (sobre todo `MX` y `TXT`).

## 1. Revisión del paquete
```bash
python tools/auditar.py
python tools/empaquetar.py
```
- [ ] `auditar.py` sin avisos graves (los `#` de `/socios/` son contenido de ejemplo hasta tener el real).
- [ ] `empaquetar.py` sin "GRAVES". Genera `dist/adcs-web.zip` y `dist/adcs-web/`.

## 2. Subida a Hostalia
- [ ] Subir el **contenido** de `dist/adcs-web/` (no la carpeta contenedora) a la raíz web del hosting por FTP/SFTP o el administrador de archivos. **Incluye el fichero oculto `.htaccess`.**
- [ ] Comprobar en la dirección provisional de Hostalia que las páginas, imágenes y fuentes cargan.
- [ ] Comprobar `404.html` con una dirección que no exista.

## 3. Dominio y SSL (en este orden)
- [ ] Apuntar `adcsevilla.es` (y `www`) al hosting de Hostalia. Si se usa Cloudflare, hacerlo desde allí.
- [ ] Activar el certificado **SSL** del dominio en Hostalia y comprobar `https://adcsevilla.es`.
- [ ] Comprobar que responden `https://adcsevilla.es/robots.txt` y `https://adcsevilla.es/sitemap.xml`.
- [ ] **Solo con SSL funcionando:** descomentar el bloque `mod_rewrite` de `.htaccess` (fuerza HTTPS y quita el `www`) y volver a subirlo. Hacerlo antes dejaría el sitio inaccesible.
- [ ] Probar `http://adcsevilla.es` y `https://www.adcsevilla.es`: ambas deben acabar en `https://adcsevilla.es/`.

## 4. Comprobaciones finales
- [ ] Navegar por todas las páginas del menú en móvil y escritorio.
- [ ] El pie enlaza bien a aviso legal, privacidad y cookies.
- [ ] El formulario de inscripción y los enlaces a Drive abren.
- [ ] Compartir la portada en WhatsApp o Facebook: debe verse la imagen y el título (caché de previsualización: <https://developers.facebook.com/tools/debug/>).
- [ ] Correo del dominio funcionando (si lo hay).
- [ ] Si hay Cloudflare Access: `/socios/` pide correo y código desde una ventana privada.

## 5. Buscadores
- [ ] Dar de alta `https://adcsevilla.es` en **Google Search Console** (verificación por DNS o por archivo).
- [ ] Enviar `https://adcsevilla.es/sitemap.xml`.
- [ ] Comprobar que `/socios/` **no** aparece indexado.

## 6. Cierre
- [ ] Redirigir o avisar en la web antigua de Blogger si todavía existe en otro dominio (por ejemplo, una entrada con el aviso del cambio).
- [ ] Actualizar `README.md` (estado, despliegue hecho, fecha) y hacer commit.
- [ ] Anotar quién custodia: acceso a Hostalia, registrador del dominio, cuenta de Cloudflare, GitHub.
- [ ] Poner en el calendario: **11 de septiembre** de cada año, revisar la lista de socios con acceso.
