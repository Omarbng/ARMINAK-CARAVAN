/* ============================================================================
   ARMINAK CARAVAN — site behaviour (v2)
   Vanilla JS, no dependencies.
   ============================================================================ */
(function () {
  'use strict';

  /* -------------------------------------------------------------- CONFIG -- */

  var MOBILE_BP = 768;
  var THEME_KEY = 'ac_theme';

  function qs(sel, ctx) { return (ctx || document).querySelector(sel); }
  function qsa(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  /* --------------------------------------------------------------- THEME -- */
  /* data-theme is stamped on <html> by the inline head script before paint;
     this wires the toggles and persists the choice. */

  function initTheme() {
    function apply(theme) {
      document.documentElement.setAttribute('data-theme', theme);
      try { localStorage.setItem(THEME_KEY, theme); } catch (e) {}
      qsa('.theme-toggle').forEach(function (b) {
        b.setAttribute('aria-pressed', String(theme === 'dark'));
      });
    }

    qsa('.theme-toggle').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        apply(next);
      });
    });
  }

  /* ---------------------------------------------------------------- HERO -- */
  /* The film is ambience, not a gate: the headline lands immediately and the
     video loops continuously. The mp4 is authored with a crossfaded seam, so
     native `loop` runs unbroken — no state machine, no freeze frame. The one
     control hands playback to the visitor. */

  function initHero() {
    var hero = qs('#hero');
    if (!hero) return;

    var video = qs('#heroVideo');
    var toggle = qs('#heroPlayback');
    var ring = qs('#heroRing');
    var label = toggle && qs('.hero__playback-label', toggle);

    var RING_LEN = 128.2;   /* circumference baked into the markup */

    var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var small = window.innerWidth < MOBILE_BP;
    var playable = !!video && !reduced;

    var running = false;
    var raf = null;

    function syncToggle() {
      if (!toggle) return;
      toggle.setAttribute('aria-pressed', String(running));
      toggle.setAttribute('aria-label', running ? 'Pause background film' : 'Play background film');
      if (label) {
        label.setAttribute('data-i18n', running ? 'hero.pause' : 'hero.play');
        if (window.ACI18N) window.ACI18N.retranslate(toggle);
        else label.textContent = running ? 'Pause' : 'Play';
      }
    }

    /* Progress ring tracks the position within the loop. */
    function tick() {
      var d = video.duration;
      if (ring && d && isFinite(d)) {
        ring.style.strokeDashoffset = (RING_LEN * (1 - (video.currentTime / d))).toFixed(1);
      }
      raf = requestAnimationFrame(tick);
    }
    function startRing() { if (!raf && ring) raf = requestAnimationFrame(tick); }
    function stopRing() { if (raf) { cancelAnimationFrame(raf); raf = null; } }

    function usePoster() {
      hero.classList.add('hero--static');
      running = false;
      stopRing();
      if (video) { try { video.pause(); } catch (e) {} }
      syncToggle();
    }

    function play() {
      hero.classList.remove('hero--static');
      running = true;
      video.preload = 'auto';
      video.classList.add('is-active');

      var p = video.play();
      if (p && typeof p.catch === 'function') {
        p.catch(function () {
          /* Background tabs refuse playback; retry once when visible. */
          if (document.visibilityState === 'hidden') {
            var onVisible = function () {
              if (document.visibilityState !== 'visible') return;
              document.removeEventListener('visibilitychange', onVisible);
              if (running) play();
            };
            document.addEventListener('visibilitychange', onVisible);
          } else {
            usePoster();
          }
        });
      }

      startRing();
      syncToggle();
    }

    function pause() {
      running = false;
      try { video.pause(); } catch (e) {}
      stopRing();
      syncToggle();
    }

    /* --- wiring ------------------------------------------------------- */

    if (toggle) {
      if (!playable) toggle.hidden = true;
      else toggle.addEventListener('click', function () { running ? pause() : play(); });
    }

    /* Text lands right away — nothing waits on the film. */
    setTimeout(function () { hero.classList.add('hero--revealed'); }, 80);

    if (!playable) { usePoster(); return; }

    video.addEventListener('error', usePoster);

    /* Don't burn a decoder on a hero nobody is looking at. */
    document.addEventListener('visibilitychange', function () {
      if (!running) return;
      if (document.visibilityState === 'hidden') {
        try { video.pause(); } catch (e) {}
        stopRing();
      } else {
        var p = video.play();
        if (p && typeof p.catch === 'function') p.catch(function () {});
        startRing();
      }
    });

    /* Mobile starts on the poster: the visitor opts in with the control, so no
       phone pays for the film unless it is asked for. */
    if (small) { usePoster(); return; }

    play();
  }

  /* ------------------------------------------------------- HERO SCRAMBLE -- */
  /* Decodes the coordinate readout once on load. Purely decorative: the final
     text is already in the markup, so it survives a JS-less render. */

  function initScramble() {
    var el = qs('#heroCoord');
    if (!el) return;
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    var final = el.textContent;
    var chars = final.split('');
    var glyphs = '0123456789ABCDEF°NEW.';
    var settle = chars.map(function () { return Math.floor(Math.random() * 16) + 8; });
    var frame = 0;

    function isFixed(ch) { return ch === ' ' || ch === ' '; }

    function step() {
      var out = '';
      var done = 0;
      for (var i = 0; i < chars.length; i++) {
        if (isFixed(chars[i]) || frame >= settle[i]) { out += chars[i]; done++; }
        else out += glyphs[Math.floor(Math.random() * glyphs.length)];
      }
      el.textContent = out;
      frame++;
      if (done < chars.length) requestAnimationFrame(step);
    }

    requestAnimationFrame(step);
  }

  /* -------------------------------------------------------- HERO PARALLAX -- */
  /* Fine-pointer only: the film drifts a few pixels toward the cursor.
     One rAF loop that lerps toward the target and stops itself when idle —
     transform + scale only, fully compositor-friendly. */

  function initHeroParallax() {
    var hero = qs('#hero');
    if (!hero || !window.matchMedia) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (!window.matchMedia('(pointer: fine)').matches) return;

    var media = qs('.hero__media', hero);
    if (!media) return;

    var tx = 0, ty = 0, ta = 0;   /* targets: offset x/y, activation 0..1 */
    var cx = 0, cy = 0, ca = 0;   /* currents */
    var raf = null;

    function tick() {
      cx += (tx - cx) * 0.07;
      cy += (ty - cy) * 0.07;
      ca += (ta - ca) * 0.07;

      var scale = 1 + 0.045 * ca;
      media.style.transform =
        'translate3d(' + cx.toFixed(2) + 'px,' + cy.toFixed(2) + 'px,0) scale(' + scale.toFixed(4) + ')';

      if (Math.abs(tx - cx) > 0.05 || Math.abs(ty - cy) > 0.05 || Math.abs(ta - ca) > 0.002) {
        raf = requestAnimationFrame(tick);
      } else {
        raf = null;
        if (ta === 0) media.style.transform = '';
      }
    }

    function kick() { if (!raf) raf = requestAnimationFrame(tick); }

    hero.addEventListener('pointermove', function (e) {
      var r = hero.getBoundingClientRect();
      tx = (e.clientX / r.width - 0.5) * 18;
      ty = ((e.clientY - r.top) / r.height - 0.5) * 12;
      ta = 1;
      kick();
    });

    hero.addEventListener('pointerleave', function () {
      tx = 0; ty = 0; ta = 0;
      kick();
    });
  }

  /* ----------------------------------------------------------------- NAV -- */

  function initNav() {
    var nav = qs('#nav');
    if (!nav) return;

    var hero = qs('#hero');
    var burger = qs('#navBurger');
    var menu = qs('#navMenu');

    function onScroll() {
      var y = window.scrollY || window.pageYOffset;
      if (hero) {
        if (y < hero.offsetHeight - nav.offsetHeight) {
          nav.classList.add('nav--over');
          nav.classList.remove('nav--scrolled');
        } else {
          nav.classList.remove('nav--over');
          nav.classList.add('nav--scrolled');
        }
      } else {
        nav.classList.toggle('nav--scrolled', y > 8);
      }
    }

    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);

    if (!burger || !menu) return;

    function closeMenu() {
      burger.setAttribute('aria-expanded', 'false');
      menu.classList.remove('is-open');
      document.body.classList.remove('no-scroll');
    }

    burger.addEventListener('click', function () {
      var open = burger.getAttribute('aria-expanded') === 'true';
      burger.setAttribute('aria-expanded', open ? 'false' : 'true');
      menu.classList.toggle('is-open', !open);
      document.body.classList.toggle('no-scroll', !open);
    });

    qsa('.nav__link', menu).forEach(function (a) { a.addEventListener('click', closeMenu); });
    window.addEventListener('resize', function () { if (window.innerWidth > 1024) closeMenu(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenu(); });
  }

  /* -------------------------------------------------------- SCROLL REVEAL -- */

  function initReveal() {
    var els = qsa('.fade-up, .corridor');
    if (!els.length) return;

    if (!('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.classList.add('in-view'); });
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('in-view');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });

    els.forEach(function (el) { io.observe(el); });
  }

  /* ------------------------------------------------------------ CORRIDOR -- */

  function initCorridor() {
    var route = qs('#corridorRoute');
    if (!route || typeof route.getTotalLength !== 'function') return;
    route.style.setProperty('--len', Math.ceil(route.getTotalLength()));
  }

  /* ------------------------------------------------------------ TAB RAILS -- */
  /* <div data-tabs> [.tabs__btn data-tab=x] ... [data-tab-panel=x] */

  function initTabs() {
    qsa('[data-tabs]').forEach(function (root) {
      var btns = qsa('.tabs__btn', root);
      var panels = qsa('[data-tab-panel]', root);
      if (!btns.length) return;

      btns.forEach(function (btn) {
        btn.addEventListener('click', function () {
          var key = btn.getAttribute('data-tab');
          btns.forEach(function (b) { b.classList.toggle('is-active', b === btn); });
          panels.forEach(function (p) {
            p.hidden = p.getAttribute('data-tab-panel') !== key;
          });
        });
      });
    });
  }

  /* ------------------------------------------------------------ FAVOURITES -- */
  /* Cosmetic wishlist hearts (no backend) — state kept for the session. */

  function initFavs() {
    document.addEventListener('click', function (e) {
      var fav = e.target.closest('.card__fav');
      if (!fav) return;
      e.preventDefault();
      e.stopPropagation();
      fav.classList.toggle('is-active');
    });
  }

  /* ------------------------------------------------------------ HOME RAILS -- */
  /* <div class="grid-products" data-rail data-slugs="a,b,c,d"> is filled from
     window.PRODUCTS — one card renderer shared with the shop grid markup. */

  function cardHTML(slug) {
    var p = window.PRODUCTS && window.PRODUCTS[slug];
    if (!p) return '';

    var badge = '';
    if (p.badge === 'new') badge = '<span class="card__badge" data-i18n="shop.badgeNew">New</span>';
    if (p.badge === 'best') badge = '<span class="card__badge" data-i18n="shop.badgeBest">Bestseller</span>';

    var spec = p.en.spec.map(function (row, i) {
      return '<tr><th scope="row" data-i18n="p.' + slug + '.sp' + i + '">' + row[0] +
             '</th><td data-i18n="p.' + slug + '.sv' + i + '">' + row[1] + '</td></tr>';
    }).join('');

    var meta = p.en.meta.map(function (row, i) {
      return '<div><dt data-i18n="p.' + slug + '.mp' + i + '">' + row[0] +
             '</dt><dd data-i18n="p.' + slug + '.mv' + i + '">' + row[1] + '</dd></div>';
    }).join('');

    return '<a class="card" href="product.html?p=' + slug + '"' +
      ' data-product="' + p.en.name + '" data-grade="' + p.en.grade + '"' +
      ' data-product-key="p.' + slug + '.name" data-grade-key="p.' + slug + '.grade"' +
      ' data-cat="' + p.cat + '" data-name="' + p.en.name + '">' +
      '<div class="card__figure">' + badge +
      '<button type="button" class="card__fav" aria-label="Save to favourites">' +
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20.3 4.9 13a4.6 4.6 0 0 1 0-6.5 4.5 4.5 0 0 1 6.4 0l.7.7.7-.7a4.5 4.5 0 0 1 6.4 0 4.6 4.6 0 0 1 0 6.5Z"/></svg></button>' +
      '<img class="card__art" src="assets/img/products/' + p.art + '.svg" alt="" loading="lazy" width="400" height="500">' +
      '<button type="button" class="card__quick" data-drawer-trigger data-i18n="shop.quickRfq">Quick RFQ</button>' +
      '</div>' +
      '<div class="card__row">' +
      '<h3 class="card__title" data-i18n="p.' + slug + '.name">' + p.en.name + '</h3>' +
      '<span class="card__price" data-i18n="shop.onRequest">On request</span>' +
      '</div>' +
      '<span class="card__cat" data-i18n="cat.c.' + p.cat + '">' + p.en.catName + '</span>' +
      '<template class="card__spec">' +
      '<table class="spec"><thead><tr>' +
      '<th scope="col" data-i18n="cat.param">Parameter</th>' +
      '<th scope="col" data-i18n="cat.value">Value</th>' +
      '</tr></thead><tbody>' + spec + '</tbody></table>' +
      '<dl class="drawer__meta">' + meta + '</dl>' +
      '</template>' +
      '</a>';
  }

  function renderRail(rail) {
    var slugs = (rail.getAttribute('data-slugs') || '').split(',');
    rail.innerHTML = slugs.map(function (s) { return cardHTML(s.trim()); }).join('');
    if (window.ACI18N) window.ACI18N.retranslate(rail);
  }

  function initRails() {
    if (!window.PRODUCTS) return;
    qsa('[data-rail]').forEach(renderRail);
  }

  /* The product page sets a rail's slugs after this file boots. */
  window.ACRails = { render: renderRail };

  /* ---------------------------------------------------------- SHOP FILTERS -- */

  function initShop() {
    var grid = qs('#shopGrid');
    if (!grid) return;

    var cards = qsa('.card', grid);
    var catBoxes = qsa('input[data-filter-cat]');
    var colBoxes = qsa('input[data-filter-col]');
    var sortSel = qs('#shopSort');
    var countEl = qs('#shopCount');
    var emptyEl = qs('#shopEmpty');
    var original = cards.slice();

    function activeSet(boxes, attr) {
      return boxes.filter(function (b) { return b.checked; })
                  .map(function (b) { return b.getAttribute(attr); });
    }

    function apply() {
      var cats = activeSet(catBoxes, 'data-filter-cat');
      var cols = activeSet(colBoxes, 'data-filter-col');
      var shown = 0;

      cards.forEach(function (card) {
        var okCat = !cats.length || cats.indexOf(card.getAttribute('data-cat')) > -1;
        var cardCols = (card.getAttribute('data-collections') || '').split(' ');
        var okCol = !cols.length || cols.some(function (c) { return cardCols.indexOf(c) > -1; });
        var show = okCat && okCol;
        card.style.display = show ? '' : 'none';
        if (show) shown++;
      });

      if (countEl) countEl.textContent = countEl.getAttribute('data-tpl').replace('%n', shown);
      if (emptyEl) emptyEl.classList.toggle('is-visible', shown === 0);
    }

    function sortCards() {
      var mode = sortSel ? sortSel.value : 'relevance';
      var list = original.slice();

      if (mode === 'name') {
        list.sort(function (a, b) {
          return a.getAttribute('data-name').localeCompare(b.getAttribute('data-name'));
        });
      } else if (mode === 'category') {
        list.sort(function (a, b) {
          return a.getAttribute('data-cat').localeCompare(b.getAttribute('data-cat')) ||
                 a.getAttribute('data-name').localeCompare(b.getAttribute('data-name'));
        });
      }

      list.forEach(function (card) { grid.appendChild(card); });
    }

    catBoxes.concat(colBoxes).forEach(function (b) { b.addEventListener('change', apply); });
    if (sortSel) sortSel.addEventListener('change', sortCards);

    /* Collapsible filter groups */
    qsa('.fgroup__head').forEach(function (head) {
      head.addEventListener('click', function () {
        head.closest('.fgroup').classList.toggle('is-closed');
      });
    });

    /* Deep link: catalogue.html?cat=grains pre-checks a category */
    var m = /[?&]cat=([a-z]+)/.exec(location.search);
    if (m) {
      var box = qs('input[data-filter-cat="' + m[1] + '"]');
      if (box) { box.checked = true; }
    }

    apply();
  }

  /* ------------------------------------------------------------ ACCORDIONS -- */

  function initAccordions() {
    qsa('.acc__head').forEach(function (head) {
      head.addEventListener('click', function () {
        var item = head.closest('.acc__item');
        var open = item.classList.contains('is-open');
        item.classList.toggle('is-open', !open);
        head.setAttribute('aria-expanded', String(!open));
      });
    });
  }

  /* -------------------------------------------------------------- DRAWER -- */

  function initDrawer() {
    var drawer = qs('#drawer');
    if (!drawer) return;

    var backdrop = qs('#drawerBackdrop');
    var closeBtn = qs('.drawer__close', drawer);
    var titleEl = qs('#drawerTitle');
    var eyebrowEl = qs('#drawerEyebrow');
    var specEl = qs('#drawerSpec');
    var bodyEl = qs('.drawer__body', drawer);
    var form = qs('#rfqForm');
    var productIn = qs('#rfqProduct');
    var lastFocus = null;

    function open(source) {
      var name = source.getAttribute('data-product') || '';
      var grade = source.getAttribute('data-grade') || '';
      var tpl = qs('.card__spec', source);

      if (titleEl) titleEl.textContent = name;
      if (eyebrowEl) eyebrowEl.textContent = grade;
      if (specEl) {
        specEl.innerHTML = '';
        if (tpl) {
          specEl.appendChild(tpl.content.cloneNode(true));
          if (window.ACI18N) window.ACI18N.retranslate(specEl);
        }
      }
      if (productIn) productIn.value = name;
      if (form) form.setAttribute('data-subject', 'RFQ — ' + name);

      var status = form && qs('.form__status', form);
      if (status) status.classList.remove('is-visible');

      lastFocus = document.activeElement;
      drawer.classList.add('is-open');
      drawer.setAttribute('aria-hidden', 'false');
      if (backdrop) backdrop.classList.add('is-open');
      document.body.classList.add('no-scroll');
      if (bodyEl) bodyEl.scrollTop = 0;
      if (closeBtn) closeBtn.focus();
    }

    function close() {
      drawer.classList.remove('is-open');
      drawer.setAttribute('aria-hidden', 'true');
      if (backdrop) backdrop.classList.remove('is-open');
      document.body.classList.remove('no-scroll');
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    /* Triggers carry data-drawer-trigger. When one lives inside a product-card
       link, the click must not navigate — preventDefault covers both. */
    document.addEventListener('click', function (e) {
      var trigger = e.target.closest('[data-drawer-trigger]');
      if (!trigger) return;

      e.preventDefault();
      e.stopPropagation();
      open(trigger.closest('[data-drawer-source]') || trigger.closest('.card') || trigger);
    });

    if (closeBtn) closeBtn.addEventListener('click', close);
    if (backdrop) backdrop.addEventListener('click', close);

    document.addEventListener('keydown', function (e) {
      if (!drawer.classList.contains('is-open')) return;
      if (e.key === 'Escape') { close(); return; }
      if (e.key !== 'Tab') return;

      var focusables = qsa(
        'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])',
        drawer
      ).filter(function (el) { return el.offsetParent !== null; });
      if (!focusables.length) return;

      var first = focusables[0];
      var last = focusables[focusables.length - 1];

      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }

  /* --------------------------------------------------------------- FORMS -- */
  /* Static site: enquiries open the operator's mail client, per the brief.
     Swap for a POST endpoint when a backend exists. */

  function initForms() {
    qsa('form[data-mailto]').forEach(function (form) {

      function labelFor(name) {
        var field = form.elements[name];
        if (field && field.id) {
          var lab = qs('label[for="' + field.id + '"]', form);
          if (lab) return lab.textContent.replace(/\*/g, '').trim();
        }
        return name;
      }

      form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (typeof form.reportValidity === 'function' && !form.reportValidity()) return;

        var lines = [];
        new FormData(form).forEach(function (value, key) {
          if (String(value).trim() !== '') lines.push(labelFor(key) + ': ' + value);
        });

        window.location.href = 'mailto:' + form.getAttribute('data-mailto') +
          '?subject=' + encodeURIComponent(form.getAttribute('data-subject') || 'Enquiry') +
          '&body=' + encodeURIComponent(lines.join('\n'));

        var status = qs('.form__status', form);
        if (status) status.classList.add('is-visible');
      });
    });
  }

  /* ----------------------------------------------------------------- GO --- */

  function boot() {
    initTheme();
    initNav();
    initCorridor();
    initReveal();
    initTabs();
    initFavs();
    initRails();
    initShop();
    initAccordions();
    initDrawer();
    initForms();
    initHero();
    initScramble();
    initHeroParallax();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
