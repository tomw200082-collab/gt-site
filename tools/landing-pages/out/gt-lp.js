/* gt-lp.js — reveal on scroll + lead capture for the GT category landing pages.
   The form POSTs to the Make webhook set on the section. Make holds
   LEAD_INGEST_TOKEN and calls /ingest; the browser never sees a secret.
   With no webhook set, the form falls back to WhatsApp with the details
   prefilled — a submission is never silently lost. */
(function () {
  'use strict';

  var reveal = document.querySelectorAll('.g-lp .g-drink');
  if (window.IntersectionObserver && reveal.length) {
    // Only arm the hidden start state once we know the observer will undo it.
    Array.prototype.forEach.call(document.querySelectorAll('.g-lp .g-grid'), function (g) {
      g.classList.add('g-reveal');
    });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('g-on'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    Array.prototype.forEach.call(reveal, function (el) { io.observe(el); });
  } else {
    Array.prototype.forEach.call(reveal, function (el) { el.classList.add('g-on'); });
  }

  function waFallback(f, payload) {
    var lines = [
      'היי, הגעתי מהאתר ואשמח לקבל את המחירון.',
      'עסק: ' + payload.display_name,
      'שם: ' + payload.contact_name,
      'טלפון: ' + payload.phone,
      payload.city ? 'עיר: ' + payload.city : '',
      payload.email ? 'אימייל: ' + payload.email : ''
    ].filter(Boolean).join('\n');
    window.open('https://wa.me/' + f.dataset.wa + '?text=' + encodeURIComponent(lines), '_blank', 'noopener');
  }

  Array.prototype.forEach.call(document.querySelectorAll('.g-lp form'), function (f) {
    var msg = f.querySelector('.g-msg');
    var btn = f.querySelector('button[type=submit]');

    function say(text, isError) {
      msg.textContent = text;
      if (isError) { msg.setAttribute('data-err', ''); } else { msg.removeAttribute('data-err'); }
    }

    f.addEventListener('submit', function (ev) {
      ev.preventDefault();
      if (!f.reportValidity()) return;

      var payload = {
        source: f.dataset.source,
        display_name: f.display_name.value.trim(),
        contact_name: f.contact_name.value.trim(),
        phone: f.phone.value.trim(),
        city: f.city.value.trim(),
        email: f.email.value.trim(),
        form_name: 'landing-' + f.dataset.source,
        platform: 'site',
        page_url: location.href
      };

      var endpoint = f.dataset.endpoint;
      if (!endpoint) {
        say('פותחים לכם וואטסאפ עם הפרטים — שלחו ונחזור אליכם.', false);
        waFallback(f, payload);
        return;
      }

      btn.disabled = true;
      say('שולחים…', false);

      fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        f.reset();
        say('תודה — קיבלנו. נחזור אליכם תוך יום עסקים אחד.', false);
      }).catch(function () {
        say('השליחה נכשלה. פותחים וואטסאפ עם הפרטים כדי שלא ילכו לאיבוד.', true);
        waFallback(f, payload);
      }).then(function () {
        btn.disabled = false;
      });
    });
  });
})();
