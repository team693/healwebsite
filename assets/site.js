(function () {
  var root = document.documentElement;
  root.classList.remove('no-js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* mobile menu */
  var btn = document.querySelector('.menu-btn');
  var panel = document.querySelector('.mobile-panel');
  function menu(open) {
    document.body.classList.toggle('menu-open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    panel.querySelectorAll('a').forEach(function (a, i) { a.style.transitionDelay = open ? Math.min(i * 60, 400) + 'ms' : '0ms'; });
    document.body.style.overflow = open ? 'hidden' : '';
  }
  if (btn && panel) {
    btn.addEventListener('click', function () { menu(!document.body.classList.contains('menu-open')); });
    panel.addEventListener('click', function (e) { if (e.target.closest('a')) menu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && document.body.classList.contains('menu-open')) { menu(false); btn.focus(); } });
  }

  /* scroll reveals, once each */
  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -10% 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else { els.forEach(function (el) { el.classList.add('in'); }); }

  /* tagline: words light up one at a time as they cross a line 70% down the viewport */
  var ticking = false;
  function initTagline() {
    document.querySelectorAll('.tagline [data-words]').forEach(function (p) {
      if (!p.dataset.split) {
        p.innerHTML = p.textContent.trim().split(/\s+/).map(function (w) {
          var accent = /drops/.test(w) ? ' accent' : '';
          return '<span class="w' + accent + '">' + w + '</span>';
        }).join(' ');
        p.dataset.split = '1';
      }
    });
    if (reduce) document.querySelectorAll('.tagline .w').forEach(function (w) { w.classList.add('on'); });
    else update();
  }
  function update() {
    ticking = false;
    var line = window.innerHeight * 0.7;
    document.querySelectorAll('.tagline .w').forEach(function (w) {
      if (w.offsetParent && w.getBoundingClientRect().top < line) w.classList.add('on');
    });
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  initTagline();

  /* in-page section nav highlights the section in view */
  var chips = document.querySelectorAll('.chipnav a');
  if (chips.length && 'IntersectionObserver' in window) {
    var so = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) chips.forEach(function (c) { c.classList.toggle('on', c.getAttribute('href') === '#' + en.target.id); }); });
    }, { rootMargin: '-45% 0px -50% 0px' });
    chips.forEach(function (c) { var t = document.querySelector(c.getAttribute('href')); if (t) so.observe(t); });
  }

  /* copy buttons */
  var toast = document.querySelector('.toast');
  function say(msg) { if (!toast) return; toast.textContent = msg; toast.classList.add('on'); clearTimeout(say.t); say.t = setTimeout(function () { toast.classList.remove('on'); }, 2200); }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-copy]');
    if (!b) return;
    var text = b.getAttribute('data-copy');
    var label = b.querySelector('[data-label]');
    function ok() {
      b.classList.add('done');
      if (label) { label.dataset.orig = label.dataset.orig || label.textContent; label.textContent = 'Copied'; }
      say('Copied: ' + text);
      setTimeout(function () { b.classList.remove('done'); if (label) label.textContent = label.dataset.orig; }, 1800);
    }
    function fallback() {
      var r = document.createRange(); var v = b.closest('.bank-row').querySelector('.v');
      r.selectNodeContents(v); var s = getSelection(); s.removeAllRanges(); s.addRange(r);
      say('Selected. Press Ctrl+C to copy.');
    }
    try { navigator.clipboard.writeText(text).then(ok, fallback); } catch (err) { fallback(); }
  });

  /* same-origin embeds size to their content */
  document.querySelectorAll('iframe[data-autoheight]').forEach(function (f) {
    function fit() { try { f.style.height = f.contentWindow.document.documentElement.scrollHeight + 'px'; } catch (e) {} }
    f.addEventListener('load', function () { fit(); setTimeout(fit, 600); setTimeout(fit, 2000); });
    window.addEventListener('resize', fit);
  });

  /* footer year */
  document.querySelectorAll('[data-year]').forEach(function (y) { y.textContent = new Date().getFullYear(); });
})();
