-- Esquema del asistente virtual de la ADCS (Supabase / PostgreSQL).
-- Ejecutar una sola vez en el editor SQL de Supabase (proyecto exclusivo de la ADCS, región UE).
-- Seguridad: RLS activado en todas las tablas y SIN políticas => la clave anónima no puede leer ni escribir nada.
-- Solo la Edge Function (service role) accede a los datos.

create extension if not exists unaccent with schema extensions;

-- unaccent no es immutable; este envoltorio permite usarlo en columnas generadas e índices.
create or replace function public.f_unaccent(t text) returns text
language sql immutable parallel safe strict as $$ select extensions.unaccent(t) $$;

-- Documentos fuente (una fila por página web o documento aprobado del archivo).
create table if not exists public.kb_documents (
  id          bigint generated always as identity primary key,
  origen      text not null check (origen in ('web','drive','faq','manual')),
  titulo      text not null,
  tipo        text not null default 'otro',   -- web, concurso, encuentro, ciclo, taller, historia, estatutos, comunicacion, faq...
  edicion     text,                           -- p. ej. 'IV'
  anio        text,
  vigencia    text not null default 'historico' check (vigencia in ('vigente','historico')),
  url         text,                           -- enlace público que el bot puede citar (nunca rutas internas del Drive)
  activo      boolean not null default true,
  ref_interna text,                           -- identificador interno (no se muestra al usuario)
  revisado_en timestamptz,
  actualizado timestamptz not null default now()
);

-- Fragmentos indexados para la búsqueda de texto completo en español.
create table if not exists public.kb_chunks (
  id        bigint generated always as identity primary key,
  doc_id    bigint not null references public.kb_documents(id) on delete cascade,
  orden     int not null default 0,
  texto     text not null,
  tsv       tsvector generated always as (to_tsvector('spanish', public.f_unaccent(texto))) stored
);
create index if not exists kb_chunks_tsv_idx on public.kb_chunks using gin (tsv);
create index if not exists kb_chunks_doc_idx on public.kb_chunks (doc_id);

-- Configuración general (una sola fila).
create table if not exists public.bot_settings (
  id             int primary key default 1 check (id = 1),
  activo         boolean not null default true,
  bienvenida     text not null default '¡Hola! Soy el asistente virtual (automático) de la Asociación de Doble Caña de Sevilla. Puedo ayudarte con información sobre la asociación, cómo hacerte socio o socia y nuestras actividades. ¿Qué te gustaría saber?',
  nucleo         text not null default '',
  limite_ip_dia  int not null default 40,
  limite_global_dia int not null default 1500,
  actualizado    timestamptz not null default now()
);
insert into public.bot_settings (id) values (1) on conflict do nothing;

-- Preguntas sin respuesta (anónimas; sin IP ni identificador) para mejorar la base de conocimiento.
create table if not exists public.unanswered (
  id       bigint generated always as identity primary key,
  pregunta text not null,
  creada   timestamptz not null default now()
);

-- Contadores de uso por día (claves hasheadas; sin IP en claro).
create table if not exists public.rate_limit (
  clave text not null,
  dia   date not null default current_date,
  n     int  not null default 0,
  primary key (clave, dia)
);

alter table public.kb_documents enable row level security;
alter table public.kb_chunks    enable row level security;
alter table public.bot_settings enable row level security;
alter table public.unanswered   enable row level security;
alter table public.rate_limit   enable row level security;
-- (Sin políticas: acceso denegado a anon/authenticated. service_role se salta RLS.)

-- Incrementa el contador y dice si aún está dentro del límite.
create or replace function public.bump_rate(p_clave text, p_limite int) returns boolean
language plpgsql security definer set search_path = public as $$
declare v int;
begin
  insert into public.rate_limit (clave, dia, n) values (p_clave, current_date, 1)
  on conflict (clave, dia) do update set n = public.rate_limit.n + 1
  returning n into v;
  return v <= p_limite;
end $$;

-- Búsqueda de fragmentos relevantes. La información vigente puntúa más que la histórica.
create or replace function public.kb_search(p_query text, p_limit int default 4)
returns table (doc_id bigint, titulo text, tipo text, edicion text, anio text, vigencia text, url text, texto text, rank real)
language sql stable security definer set search_path = public as $$
  with q as (select websearch_to_tsquery('spanish', public.f_unaccent(p_query)) as tsq)
  select d.id, d.titulo, d.tipo, d.edicion, d.anio, d.vigencia, d.url, c.texto,
         (ts_rank(c.tsv, q.tsq) * case d.vigencia when 'vigente' then 1.5 else 1.0 end)::real as rank
  from public.kb_chunks c
  join public.kb_documents d on d.id = c.doc_id and d.activo
  cross join q
  where c.tsv @@ q.tsq
  order by rank desc
  limit p_limit
$$;

-- Estas funciones solo las puede llamar el backend.
revoke all on function public.bump_rate(text, int) from public, anon, authenticated;
revoke all on function public.kb_search(text, int) from public, anon, authenticated;
grant execute on function public.bump_rate(text, int) to service_role;
grant execute on function public.kb_search(text, int) to service_role;

-- Permisos explícitos: solo service_role (la Edge Function y sincronizar.py). anon/authenticated no reciben nada.
grant usage on schema public to service_role;
grant all on public.kb_documents, public.kb_chunks, public.bot_settings, public.unanswered, public.rate_limit to service_role;
grant usage, select on all sequences in schema public to service_role;

-- Limpieza de preguntas sin respuesta y contadores (programar con pg_cron o ejecutar a mano):
-- delete from public.unanswered where creada < now() - interval '30 days';
-- delete from public.rate_limit where dia < current_date - 2;
