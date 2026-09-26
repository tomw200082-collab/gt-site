/* gt-lp.js — reveal on scroll + lead capture for the GT category landing pages.
   The form POSTs to website_lead_intake, the same public intake as the home
   page's enquiry form: it files the lead in sales_core and alerts the sales
   team, and holds every secret itself. If the send fails, the form opens
   WhatsApp with the details prefilled — a submission is never silently lost. */
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

  /* The concentrate line arrives when it is scrolled to. Same contract as the cards:
     arm the hidden state only once the observer that undoes it is known to exist. */
  Array.prototype.forEach.call(document.querySelectorAll('.g-lp .g-line'), function (row) {
    if (!window.IntersectionObserver) return;
    row.classList.add('g-armed');
    var ro = new IntersectionObserver(function (es) {
      if (es[0].isIntersecting) { row.classList.add('g-on'); ro.disconnect(); }
    }, { threshold: 0.25 });
    ro.observe(row);
  });

  /* The product is set down when it is scrolled to. Same contract as the cards and
     the bottle line: arm the hidden state only once the observer that undoes it is
     known to exist, so the bottle can never be left invisible. */
  Array.prototype.forEach.call(document.querySelectorAll('.g-lp .g-plate'), function (sec) {
    if (!window.IntersectionObserver) return;
    sec.classList.add('g-armed');
    var po = new IntersectionObserver(function (es) {
      if (es[0].isIntersecting) { sec.classList.add('g-on'); po.disconnect(); }
    }, { threshold: 0.2 });
    po.observe(sec);
  });

  /* Everything that isn't a drink card, the bottle line or the plate, but still
     wants the same "arrive when scrolled to" feel: the menu heading, both halves
     of the story section, both halves of the capture section. Same contract as
     .g-line/.g-plate above -- armed only where the observer that undoes it is
     known to exist, so a fade-up can never be a permanently blank block. */
  Array.prototype.forEach.call(document.querySelectorAll('.g-lp .g-fade-up'), function (el) {
    if (!window.IntersectionObserver) return;
    el.classList.add('g-armed');
    var fo = new IntersectionObserver(function (es) {
      if (es[0].isIntersecting) { el.classList.add('g-on'); fo.disconnect(); }
    }, { threshold: 0.15 });
    fo.observe(el);
  });

  /* The sticky bar is a second copy of the hero's call to action, so it should not
     appear while the first one is still on screen -- there it just covers content. */
  Array.prototype.forEach.call(document.querySelectorAll('.g-lp'), function (lp) {
    var hero = lp.querySelector('.g-hero');
    if (!hero || !window.IntersectionObserver) { lp.classList.add('g-sticky-on'); return; }
    new IntersectionObserver(function (es) {
      lp.classList.toggle('g-sticky-on', !es[0].isIntersecting);
    }, { threshold: 0 }).observe(hero);
  });

  function waFallback(f, payload) {
    var lines = [
      'היי, הגעתי מהאתר ואשמח לקבל את המחירון.',
      'עסק: ' + payload.venue,
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

      // The fields website_lead_intake reads. form_name is this page's key in
      // sales_core.campaign_map, so the lead is counted against its page.
      var payload = {
        contact_name: f.contact_name.value.trim(),
        venue: f.display_name.value.trim(),
        phone: f.phone.value.trim(),
        city: f.city.value.trim(),
        email: f.email.value.trim(),
        company_website: f.company_website.value,
        form_name: 'landing-' + f.dataset.source,
        // Time on the page, counted from navigation start. The intake answers ok
        // but drops anything under 3 s as a bot, and this deferred script can run
        // seconds after the page began loading, so a clock started here reads short.
        elapsed_ms: Math.round(performance.now()),
        page: location.href,
        referrer: document.referrer
      };

      btn.disabled = true;
      say('שולחים…', false);

      fetch(f.dataset.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (j) {
          if (r.ok && j.ok !== false) {
            f.reset();
            say('תודה — קיבלנו. נחזור אליכם תוך יום עסקים אחד.', false);
            return;
          }
          // A typo is the visitor's to fix, not a reason to leave for WhatsApp.
          if (j.error === 'bad_phone') { say('מספר הטלפון לא נראה תקין. בדקו אותו ונסו שוב.', true); return; }
          if (j.error === 'bad_email') { say('כתובת המייל לא נראית תקינה. בדקו אותה ונסו שוב.', true); return; }
          throw new Error(j.error || 'HTTP ' + r.status);
        });
      }).catch(function () {
        say('השליחה נכשלה. פותחים וואטסאפ עם הפרטים כדי שלא ילכו לאיבוד.', true);
        waFallback(f, payload);
      }).then(function () {
        btn.disabled = false;
      });
    });
  });
})();
