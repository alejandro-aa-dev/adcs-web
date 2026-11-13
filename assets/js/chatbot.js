/* Asistente virtual de la ADCS — widget flotante.
 * Instalación: <script src="assets/js/chatbot.js" defer data-endpoint="https://XXXX.supabase.co/functions/v1/chat"></script>
 * Sin data-endpoint (o vacío) el widget NO se muestra, así que es seguro publicarlo antes de tener backend.
 * Privacidad: no contacta con ningún servidor hasta que la persona acepta el aviso y envía su primer mensaje.
 */
(function () {
  'use strict';
  var script = document.currentScript;
  var ENDPOINT = (script && script.getAttribute('data-endpoint') || '').trim();
  if (!ENDPOINT) { return; }

  var MAX = 500, TIMEOUT_MS = 30000, CLAVE = 'adcs-chat-v1';
  var base = script.src.replace(/js\/chatbot\.js(\?.*)?$/, '');
  var css = document.createElement('link');
  css.rel = 'stylesheet'; css.href = base + 'css/chatbot.css';
  document.head.appendChild(css);

  var PREGUNTAS = [
    '¿Cómo me hago socio o socia?',
    '¿Cuánto cuesta la cuota?',
    '¿Cuándo es el próximo concurso?',
    '¿Cómo contacto con la ADCS?'
  ];
  var BIENVENIDA = '¡Hola! Soy el asistente virtual (automático) de la Asociación de Doble Caña de Sevilla. ' +
    'Puedo ayudarte con información sobre la asociación, cómo hacerte socio o socia y nuestras actividades. ¿Qué te gustaría saber?';

  // ---- estado (solo sessionStorage, dentro de try/catch) ----
  var estado = { aceptado: false, mensajes: [] };
  try { var g = JSON.parse(sessionStorage.getItem(CLAVE) || 'null'); if (g && g.mensajes) { estado = g; } } catch (e) {}
  function guardar() { try { sessionStorage.setItem(CLAVE, JSON.stringify(estado)); } catch (e) {} }

  // ---- utilidades de texto ----
  function esc(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function formatear(t) {
    var h = esc(t);
    h = h.replace(/\*\*([^*\n]+)\*\*/g, '<strong>$1</strong>');
    // Enlaces tipo [texto](url): solo https o adcsevilla.es (el modelo a veces omite el https://)
    var guardados = [];
    h = h.replace(/\[([^\]\n]+)\]\(([^)\s]+)\)/g, function (m, txt, u) {
      var url = /^https?:\/\//.test(u) ? u : (/^(www\.)?adcsevilla\.es(\/|$)/.test(u) ? 'https://' + u : (/^[\w-]+\.html(#[\w-]+)?$/.test(u) ? 'https://adcsevilla.es/' + u : null));
      if (!url) { return m; }
      var ext = url.indexOf(location.origin) !== 0;
      guardados.push('<a href="' + url + '"' + (ext ? ' target="_blank" rel="noopener noreferrer"' : '') + '>' + txt + '</a>');
      return '\u0001' + (guardados.length - 1) + '\u0001';
    });
    h = h.replace(/(https?:\/\/[^\s<)]+[^\s<).,;:!?])/g, function (u) {
      var externo = u.indexOf(location.origin) !== 0;
      return '<a href="' + u + '"' + (externo ? ' target="_blank" rel="noopener noreferrer"' : '') + '>' + u.replace(/^https?:\/\//, '') + '</a>';
    });
    h = h.replace(/([\w.+-]+@[\w-]+(?:\.[\w-]+)+)/g, function (m, e, off, all) {
      return all.slice(Math.max(0, off - 1), off) === '>' || all.slice(Math.max(0, off - 7), off).indexOf('mailto:') > -1 ? m : '<a href="mailto:' + e + '">' + e + '</a>';
    });
    h = h.replace(/\u0001(\d+)\u0001/g, function (m, i) { return guardados[+i]; });
    var lineas = h.split('\n'), out = [], lista = false;
    lineas.forEach(function (l) {
      var m = l.match(/^\s*(?:[-*•]|\d+[.)])\s+(.*)$/);
      if (m) { if (!lista) { out.push('<ul>'); lista = true; } out.push('<li>' + m[1] + '</li>'); }
      else { if (lista) { out.push('</ul>'); lista = false; } out.push(l.trim() ? '<p>' + l + '</p>' : ''); }
    });
    if (lista) { out.push('</ul>'); }
    return out.join('');
  }
  function el(tag, cls, attrs) {
    var n = document.createElement(tag);
    if (cls) { n.className = cls; }
    for (var k in (attrs || {})) { n.setAttribute(k, attrs[k]); }
    return n;
  }

  // ---- interfaz ----
  var boton = el('button', 'adcs-chat-btn', { type: 'button', 'aria-expanded': 'false', 'aria-controls': 'adcs-chat-panel' });
  boton.innerHTML = '<span aria-hidden="true">💬</span><span class="adcs-chat-btn-txt">Pregúntanos</span>';
  boton.setAttribute('aria-label', 'Abrir el asistente virtual de la ADCS');

  var panel = el('div', 'adcs-chat-panel', { id: 'adcs-chat-panel', role: 'dialog', 'aria-label': 'Asistente virtual de la ADCS', hidden: '' });
  panel.innerHTML =
    '<header class="adcs-chat-head"><div><strong>Asistente de la ADCS</strong><span class="adcs-chat-badge">IA</span></div>' +
    '<button type="button" class="adcs-chat-x" aria-label="Cerrar el asistente">✕</button></header>' +
    '<div class="adcs-chat-aviso" hidden></div>' +
    '<div class="adcs-chat-log" role="log" aria-live="polite" aria-relevant="additions" tabindex="0"></div>' +
    '<div class="adcs-chat-sug"></div>' +
    '<form class="adcs-chat-form" autocomplete="off"><label class="adcs-chat-sr" for="adcs-chat-in">Escribe tu pregunta</label>' +
    '<textarea id="adcs-chat-in" rows="1" maxlength="' + MAX + '" placeholder="Escribe tu pregunta…"></textarea>' +
    '<button type="submit" class="adcs-chat-send" aria-label="Enviar">➤</button></form>' +
    '<p class="adcs-chat-pie">Asistente automático con IA: puede equivocarse. No escribas datos personales. ' +
    '<a href="privacidad.html#asistente">Privacidad</a></p>';

  var log = panel.querySelector('.adcs-chat-log'), aviso = panel.querySelector('.adcs-chat-aviso'),
      sug = panel.querySelector('.adcs-chat-sug'), form = panel.querySelector('form'),
      entrada = panel.querySelector('textarea'), enviar = panel.querySelector('.adcs-chat-send');
  var ocupado = false;

  function pintar(rol, texto, conCopiar) {
    var b = el('div', 'adcs-chat-msg adcs-chat-' + (rol === 'user' ? 'user' : 'bot'));
    if (rol === 'user') { b.textContent = texto; }
    else {
      b.innerHTML = formatear(texto);
      if (conCopiar) {
        var c = el('button', 'adcs-chat-copy', { type: 'button', 'aria-label': 'Copiar respuesta' });
        c.textContent = 'Copiar';
        c.addEventListener('click', function () {
          var ok = function () { c.textContent = 'Copiado'; setTimeout(function () { c.textContent = 'Copiar'; }, 1500); };
          if (navigator.clipboard) { navigator.clipboard.writeText(texto).then(ok, function () {}); }
        });
        b.appendChild(c);
      }
    }
    log.appendChild(b);
    log.scrollTop = log.scrollHeight;
    return b;
  }

  function mostrarAviso() {
    aviso.hidden = false;
    aviso.innerHTML =
      '<p><strong>Antes de empezar</strong></p>' +
      '<p>Estás hablando con un <strong>asistente automático (inteligencia artificial)</strong>, no con una persona. ' +
      'Tus mensajes se enviarán a nuestros proveedores (Supabase, en la UE, y Groq, en EE. UU.) únicamente para generar la respuesta. ' +
      'No escribas datos personales (DNI, teléfono, datos bancarios…). Más información en la <a href="privacidad.html#asistente">política de privacidad</a>.</p>';
    var ok = el('button', 'adcs-chat-ok', { type: 'button' });
    ok.textContent = 'Entendido, empezar';
    ok.addEventListener('click', function () { estado.aceptado = true; guardar(); iniciar(); entrada.focus(); });
    aviso.appendChild(ok);
    form.hidden = true; sug.hidden = true; log.hidden = true;
    ok.focus();
  }

  function iniciar() {
    aviso.hidden = true; form.hidden = false; sug.hidden = false; log.hidden = false;
    log.innerHTML = '';
    pintar('bot', BIENVENIDA, false);
    estado.mensajes.forEach(function (m) { pintar(m.role, m.content, m.role === 'assistant'); });
    sug.innerHTML = '';
    if (!estado.mensajes.length) {
      PREGUNTAS.forEach(function (q) {
        var s = el('button', 'adcs-chat-chip', { type: 'button' });
        s.textContent = q;
        s.addEventListener('click', function () { preguntar(q); });
        sug.appendChild(s);
      });
    }
  }

  function preguntar(texto) {
    texto = (texto || '').trim().slice(0, MAX);
    if (!texto || ocupado) { return; }
    ocupado = true; enviar.disabled = true; sug.innerHTML = '';
    estado.mensajes.push({ role: 'user', content: texto });
    pintar('user', texto);
    entrada.value = '';
    var esperando = el('div', 'adcs-chat-msg adcs-chat-bot adcs-chat-esperando');
    esperando.innerHTML = '<span class="adcs-chat-sr">El asistente está escribiendo…</span><span class="adcs-chat-puntos" aria-hidden="true"><i></i><i></i><i></i></span>';
    log.appendChild(esperando); log.scrollTop = log.scrollHeight;

    var ctl = window.AbortController ? new AbortController() : null;
    var t = setTimeout(function () { if (ctl) { ctl.abort(); } }, TIMEOUT_MS);
    fetch(ENDPOINT, {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ messages: estado.mensajes.slice(-12) }), signal: ctl ? ctl.signal : undefined,
      referrerPolicy: 'strict-origin-when-cross-origin', credentials: 'omit'
    }).then(function (r) { return r.json().catch(function () { return {}; }); })
      .then(function (d) {
        var r = d && d.reply ? d.reply : 'Ahora mismo no puedo responder. Escríbenos a oboeyfagotsevilla@gmail.com.';
        estado.mensajes.push({ role: 'assistant', content: r }); guardar();
        esperando.remove(); pintar('assistant', r, true);
      })
      .catch(function () {
        esperando.remove();
        pintar('assistant', 'No he podido conectar con el asistente. Comprueba tu conexión o escríbenos a oboeyfagotsevilla@gmail.com.', false);
      })
      .then(function () { clearTimeout(t); ocupado = false; enviar.disabled = false; entrada.focus(); });
  }

  form.addEventListener('submit', function (e) { e.preventDefault(); preguntar(entrada.value); });
  entrada.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); preguntar(entrada.value); }
  });

  function abrir() {
    panel.hidden = false; boton.setAttribute('aria-expanded', 'true');
    boton.setAttribute('aria-label', 'Cerrar el asistente virtual de la ADCS');
    if (estado.aceptado) { iniciar(); entrada.focus(); } else { mostrarAviso(); }
  }
  function cerrar() {
    panel.hidden = true; boton.setAttribute('aria-expanded', 'false');
    boton.setAttribute('aria-label', 'Abrir el asistente virtual de la ADCS'); boton.focus();
  }
  boton.addEventListener('click', function () { if (panel.hidden) { abrir(); } else { cerrar(); } });
  panel.querySelector('.adcs-chat-x').addEventListener('click', cerrar);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) { cerrar(); } });

  document.body.appendChild(panel);
  document.body.appendChild(boton);

  // ---- anuncio de novedad: una sola vez por navegador (no por IP: no se rastrea a nadie) ----
  // Solo guarda una marca local ("ya visto"). Si el navegador no puede guardarla, no se muestra, para no molestar.
  var CLAVE_ANUNCIO = 'adcs-anuncio-bot-v1';
  function yaVisto() { try { return localStorage.getItem(CLAVE_ANUNCIO) === '1'; } catch (e) { return true; } }
  function marcarVisto() { try { localStorage.setItem(CLAVE_ANUNCIO, '1'); } catch (e) {} }

  function anunciar() {
    if (yaVisto() || estado.aceptado || !panel.hidden) { return; }
    marcarVisto();
    var previo = document.activeElement;
    var fondo = el('div', 'adcs-anuncio-fondo');
    var caja = el('div', 'adcs-anuncio', { role: 'dialog', 'aria-modal': 'true', 'aria-labelledby': 'adcs-anuncio-t', 'aria-describedby': 'adcs-anuncio-d' });
    caja.innerHTML =
      '<p class="adcs-anuncio-etq" aria-hidden="true">Novedad</p>' +
      '<h2 id="adcs-anuncio-t">Nuevo asistente virtual</h2>' +
      '<p id="adcs-anuncio-d">Seguimos incorporando mejoras a la web: ahora contamos con un <strong>asistente virtual</strong> que te echa una mano. ' +
      'Por ahora responde a cualquier pregunta relacionada con la información de este sitio web. ' +
      'Puedes navegar por ella o preguntarle al asistente lo que necesites con el <strong>botón de chat 💬</strong> que verás abajo a la derecha.</p>';
    var ok = el('button', 'adcs-anuncio-ok', { type: 'button' });
    ok.textContent = 'Entendido';
    caja.appendChild(ok);
    fondo.appendChild(caja);

    function cerrarAnuncio() {
      document.removeEventListener('keydown', tecla, true);
      fondo.remove();
      if (previo && previo.focus) { try { previo.focus(); } catch (e) {} }
    }
    function tecla(e) {
      if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); cerrarAnuncio(); }
      else if (e.key === 'Tab') { e.preventDefault(); ok.focus(); }
    }
    ok.addEventListener('click', cerrarAnuncio);
    fondo.addEventListener('click', function (e) { if (e.target === fondo) { cerrarAnuncio(); } });
    document.addEventListener('keydown', tecla, true);
    document.body.appendChild(fondo);
    ok.focus();
  }
  if (!yaVisto()) { setTimeout(anunciar, 1500); }
})();
