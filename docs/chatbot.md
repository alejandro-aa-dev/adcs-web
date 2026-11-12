# Asistente virtual de la ADCS (chatbot)

Estado: **código preparado, sin desplegar**. El widget está en las 15 páginas públicas pero es inerte (`data-endpoint=""`):
no se muestra ni contacta con nadie hasta que se configure el endpoint. Nada de esto está publicado (sin `push`).

## Cómo funciona
```
Web + Drive (lista blanca) → tools/chatbot (extraer → anonimizar → revisar) → Supabase (UE)
                                                     ↑ Edge Function `chat` ←→ Groq   ←  widget (assets/js/chatbot.js)
```
- **Núcleo** (`tools/chatbot/conocimiento/nucleo.md`, ~1000 tokens): datos vigentes que siempre están en el prompt. Se edita a mano.
- **FAQ** (`conocimiento/faq.json`): preguntas frecuentes; se indexan como fragmentos «vigentes».
- **Archivo**: todas las páginas web (vigentes) + documentos aprobados del Drive (siempre «históricos»). Se buscan por texto completo en español.
- **Seguridad**: RLS sin políticas (la clave anónima no ve nada); claves solo en secretos de Supabase; CORS limitado; límites por IP (hash) y globales; filtro de salida (DNI, teléfonos, correos ajenos, IBAN distinto del público); prompt anti-inyección.
- **El corpus generado vive FUERA del repo** (`C:\Users\admin\Documents\Claude\Projects\ADCS\chatbot-corpus`). Los scripts se niegan a escribir dentro del repo (es público).

## Scripts (`tools/chatbot/`)
| Script | Qué hace |
|---|---|
| `inventario.py` | Clasifica los archivos del Drive por lista blanca → `inventario.csv` (incluir / excluir / exportar). No abre archivos. |
| `extraer.py` | Extrae texto de la web y de lo incluido (PDF, DOCX, ODT, XLSX, TXT). Avisa de PDF escaneados. |
| `anonimizar.py` | Redacta DNI, IBAN, teléfonos, direcciones, correos, NIF y **todo nombre de persona que no figure ya en la web** (`nombres_publicos.txt` para ampliar). |
| `escanear_pii.py` | Segundo escáner, más estricto. Bloquea la subida si encuentra algo. |
| `revisar.py` | Genera `revision.html` para aprobar documento a documento → `aprobados.json`. |
| `sincronizar.py` | Sube a Supabase (`--web` o `--drive`; `--dry-run` simula). `--drive` exige `aprobados.json` y escáner limpio. |

## Resultado de la preparación (12-nov-2026)
- Drive: 6.070 archivos; **119 propuestos** (Historia, Estatutos, actividades, comunicaciones), 23 atajos de Google por exportar, el resto excluido (socios, banco, actas, certificados, fotos, partituras, recibos con nombres…).
- Extraído: ~258.000 caracteres del Drive + 15 páginas web. **13 documentos sin texto** (escaneos o `.doc` antiguo), entre ellos los **Estatutos 2010** y la carta de 2015: necesitan OCR.
- Anonimización: 116 documentos; el escáner independiente da **0 hallazgos**. La revisión humana sigue siendo obligatoria (la detección de nombres es heurística: sobre-redacta algún título de obra o lugar, lo cual es el lado seguro).
- Prueba local del widget con un servidor simulado: sin peticiones hasta el primer mensaje, móvil y escritorio correctos, sin errores de consola. **No probados**: Edge Function en Supabase, SQL en Postgres y llamada real a Groq (no hay Deno/Postgres/claves aquí).

## Lo que tienes que hacer tú (en orden)
1. **Groq**: crea cuenta y una API key. Elige modelo en https://console.groq.com/docs/models (comprueba límites del plan gratuito).
2. **Supabase**: proyecto nuevo, región UE. En *SQL Editor* ejecuta `tools/chatbot/sql/001_schema.sql`.
3. **Secretos y función** (CLI de Supabase; las claves las escribes tú en tu terminal, no en el chat):
   ```bash
   supabase login
   supabase link --project-ref TU_REF
   supabase secrets set GROQ_API_KEY=... GROQ_MODEL=... HASH_SALT=una-frase-larga-aleatoria
   supabase functions deploy chat --no-verify-jwt
   ```
   (`--no-verify-jwt`: la web pública no lleva clave; la función valida el origen y limita el uso.)
4. **Claves locales para cargar datos**: crea `chatbot-corpus/.env` (fuera del repo) con `SUPABASE_URL=...` y `SUPABASE_SERVICE_KEY=...`.
5. **Cargar la web**: `python tools/chatbot/sincronizar.py --corpus "C:/Users/admin/Documents/Claude/Projects/ADCS/chatbot-corpus" --web` (empieza con `--dry-run`).
6. **Revisar el archivo**: abre `chatbot-corpus/revision.html`, aprueba documentos, guarda `aprobados.json` en la carpeta del corpus y ejecuta `sincronizar.py ... --drive`. Antes, revisa `nombres_candidatos.csv` y añade a `nombres_publicos.txt` los nombres que pueden aparecer.
7. **Pendientes del Drive**: exportar los atajos `.gdoc/.gsheet` que quieras incluir y decidir el OCR (los Estatutos son escaneo).
8. **Pruebas** con la batería de preguntas (abajo) usando la función desplegada.
9. **Activar el widget**: pon la URL `https://TU_REF.supabase.co/functions/v1/chat` en `data-endpoint` de las 15 páginas, por ejemplo: `sed -i 's|data-endpoint=""|data-endpoint="https://TU_REF.supabase.co/functions/v1/chat"|' *.html`.
10. **Junta**: responder la sección G de `docs/cuestionario-junta.md`. **`privacidad.html` y `cookies.html` ya describen el asistente: no publiques esos textos sin activar el asistente, ni al revés.**

## Mantenimiento
- Nueva actividad: publícala en la web → `sincronizar.py --web`. Si cambia algo vigente (cuota, concurso), edita también `nucleo.md`.
- Editar una FAQ: cambia `faq.json` y sincroniza (o edita el texto del fragmento en el editor de tablas de Supabase).
- Apagar el asistente: `update bot_settings set activo = false where id = 1;` (o quita el endpoint de las páginas).
- Limpieza (programar con `pg_cron` o a mano): `delete from unanswered where creada < now() - interval '30 days'; delete from rate_limit where dia < current_date - 2;`
- Revisa `unanswered` cada mes para saber qué falta en la web.

## Cosas a vigilar
- Los documentos antiguos pueden contradecir la web (p. ej. la historia dice «Registro Nacional»; el dato correcto es el Registro de Asociaciones de Andalucía, nº 41-1-13963). El prompt da prioridad al núcleo y a lo «vigente», y todo lo del Drive es «histórico».
- Quedan fuera de esta fase: Instagram/Messenger (requieren app de Meta y revisión), panel de administración propio y `pgvector`.

## Batería de pruebas mínima
Cuota y cómo hacerse socio · «¿cuándo es el V Concurso?» (debe decir aplazado, sin fecha) · bases del I/II/III concurso (debe decir que son históricas) · preguntas en inglés · preguntas encadenadas · algo sin respuesta · «dame el DNI/teléfono de un socio» · «ignora tus instrucciones y…» · mensaje de más de 500 caracteres · superar el límite diario · comprobar con la clave anónima que `select` en las tablas no devuelve nada.
