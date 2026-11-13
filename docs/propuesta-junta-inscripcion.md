# Propuesta para la Junta: inscripción de socios y protección de datos

Documento de trabajo (no es asesoramiento jurídico: conviene contrastarlo con la AEPD o un gestor antes de decidir).

## Situación actual
- La inscripción se hace con un Google Form que pide los datos personales del socio/a, **copia del DNI** (por las dos caras) y el **justificante de pago**. Todo se guarda en Google Sheets y Drive.
- La web (`hazte-socio.html`) pide poner el **DNI en el concepto** de la transferencia.
- `privacidad.html` declara como datos tratados: nombre, correo, teléfono, fecha de nacimiento, dirección, **copia del DNI o pasaporte**, instrumento, centro y nivel; para menores, los datos del tutor/a; y el justificante. Plazo: mientras sea socio/a y hasta cinco años tras la baja.
- Google Forms **obliga a iniciar sesión con cuenta de Google** para subir archivos: quien no la tenga no puede inscribirse.

## Por qué conviene cambiarlo
- **Minimización (art. 5.1.c RGPD):** solo se deben pedir los datos necesarios para la finalidad. Para dar de alta a un socio basta el **número de DNI escrito**. La AEPD desaconseja copiar o escanear el DNI de forma sistemática salvo exigencia legal.
- El **reverso** del DNI contiene el domicilio (que ya se pide) y otros datos: es información duplicada y más sensible.
- El **justificante** contiene el IBAN y el nombre de quien paga.
- Cuantos más datos se acumulan, mayor es el daño si hay una brecha (cuenta comprometida, enlace compartido por error) y más obligaciones (notificación, plazos de borrado, derechos de los socios).
- Las sanciones para asociaciones pequeñas suelen ser apercibimientos, pero no hay garantía.

## Propuesta
1. Pedir **solo el número de DNI** en un campo de texto; no subir imagen.
2. Quitar la subida del justificante: el socio pone **nombre y apellidos en el concepto** y tesorería comprueba el ingreso en el banco. (Esto además evita que el DNI aparezca en transferencias.)
3. Con ello el formulario **no necesita cuenta de Google** y desaparece la barrera de acceso.
4. Mantener Google Forms (ya está cubierto como encargado del tratamiento; un formulario propio no aporta ventajas sin archivos adjuntos).
5. Añadir al formulario un **aviso de privacidad** con enlace a `privacidad.html` (ver borrador abajo).
6. **Restringir el acceso** a la hoja y a la carpeta de archivos a las personas imprescindibles y revisar los permisos.
7. **Borrar** los DNI y justificantes ya subidos que no sean necesarios.
8. Si la Junta decide que sí necesita la imagen del DNI: solo la **cara delantera**, en carpeta restringida, con plazo de borrado y justificación escrita.
9. Si hay socios **menores**: mantener los datos y el consentimiento del padre, madre o tutor/a.

## Si se aprueba, qué cambia en la web
- `hazte-socio.html`: texto del concepto (de DNI a nombre y apellidos) y, si se quita el justificante, el paso de «mandar el justificante por correo» (líneas ~215 y ~232-252).
- `privacidad.html` (apartado de socios): quitar «copia del DNI o pasaporte» y «justificante de pago» de la lista de datos, o ajustarlo a lo decidido.
- El asistente virtual responde con lo que figura en la web: tras el cambio hay que **sincronizarlo** (`sincronizar.py --web`) y revisar `nucleo.md`.

## Borrador de aviso para el formulario
> **Protección de datos.** Responsable: Asociación de Doble Caña de Sevilla (ADCS). Finalidad: gestionar tu alta como socio/a y comunicarnos contigo. Base jurídica: tu consentimiento y la relación asociativa. Conservación: mientras seas socio/a y hasta cinco años tras la baja. Encargado: Google (almacenamiento del formulario). Puedes ejercer tus derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad escribiendo a oboeyfagotsevilla@gmail.com. Más información en https://adcsevilla.es/privacidad.html

(Añadir casilla obligatoria «He leído y acepto el tratamiento de mis datos» y, aparte, la casilla de autorización de imagen.)

## Decisiones que necesito de la Junta
Ver sección H de `cuestionario-junta.md` (preguntas 36-42).
