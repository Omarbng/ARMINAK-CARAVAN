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
      document.dispatchEvent(new CustomEvent('ac:theme', { detail: { theme: theme } }));
    }

    qsa('.theme-toggle').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        apply(next);
      });
    });
  }

  /* --------------------------------------------------------- SAND EDGES -- */
  /* The client asked for sand at the screen edges on every page. This used to
     be a tiled SVG of dots; dots read as snow, so the real shader runs here
     too — low intensity, half resolution, masked to the margins by CSS. The
     SVG stays as the fallback when WebGL is missing. */

  function initSandEdges() {
    var host = qs('.sand-edges');
    if (!host || !window.ACSand) return;
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    var canvas = document.createElement('canvas');
    canvas.className = 'sand-edges__gl';
    host.appendChild(canvas);

    var sand = window.ACSand(canvas, host, {
      mode: 'veil',
      base: 0.62, open: 0.62, openMs: 1,   /* ambient, no entry gust */
      wind: 0.07,                          /* gentler than the hero storm */
      scale: 0.6,                          /* soft veil — half res is invisible */
      fps: 20,                             /* ambient margin texture, no fast motion */
      seed: 11.3
    });
    if (!sand) { host.removeChild(canvas); return; }   /* keep the SVG dots */

    host.classList.add('sand-edges--gl');

    function accentHex() {
      return getComputedStyle(document.documentElement)
               .getPropertyValue('--sand').trim() || '#C7A87A';
    }
    sand.setColor(accentHex());
    sand.resize();
    sand.start();

    var rt = null;
    window.addEventListener('resize', function () {
      clearTimeout(rt);
      rt = setTimeout(sand.resize, 180);
    });
    document.addEventListener('visibilitychange', function () {
      document.visibilityState === 'hidden' ? sand.stop() : sand.start();
    });
    document.addEventListener('ac:theme', function () { sand.setColor(accentHex()); });
  }

  /* ---------------------------------------------------------------- HERO -- */
  /* Gold dust drifts, the loaded caravan develops out of it, the dust thins to
     an ambient trace and the headline rises. No video, so phone and desktop
     behave identically — which is what the client reported as broken.

     The particle field is purpose-built rather than particles.js: ~3KB instead
     of ~25KB, no dependency, and it can be tuned to look like desert wind
     instead of a node graph. */

  function initHero() {
    var hero = qs('#hero');
    if (!hero) return;

    var canvas = qs('#heroDust');
    var reduced = window.matchMedia &&
                  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* The scene is already in the markup — reveal it on the next frame so the
       transition actually runs instead of being skipped on first paint. */
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { hero.classList.add('hero--revealed'); });
    });

    if (!canvas || reduced || !canvas.getContext) return;

    /* Real sand: two GL layers sandwiching the caravan. The veil (suspension)
       drifts behind it, shaped by the dune lines; the streaks (saltation)
       whip past in front, hugging the near dune. Both surge with the same
       travelling gust wave. Only if WebGL is missing do we fall back to the
       canvas-2D dust below. */
    if (window.ACSand) {
      var back = qs('#heroSandBack');
      var dunesSvg = qs('.hero__scene--dunes', hero);
      var ground = dunesSvg ? {
        near: dunesSvg.querySelector('.dune--near'),
        mid: dunesSvg.querySelector('.dune--mid'),
        viewBox: [1600, 900]
      } : null;

      var veil = back ? window.ACSand(back, hero, {
        mode: 'veil', ground: ground, seed: 3.7,
        open: 1.5, base: 1.0, openMs: 3400, fps: 30, wind: 0.13
      }) : null;
      var streaks = window.ACSand(canvas, hero, {
        mode: 'streaks', ground: ground, seed: 3.7,
        open: 1.6, base: 1.0, openMs: 3400, fps: 30
      });

      var layers = [veil, streaks].filter(Boolean);
      if (layers.length) {
        function accentHex() {
          return getComputedStyle(document.documentElement)
                   .getPropertyValue('--accent').trim() || '#B08D57';
        }
        layers.forEach(function (l) { l.setColor(accentHex()); l.resize(); l.start(); });

        var srt = null;
        window.addEventListener('resize', function () {
          clearTimeout(srt);
          srt = setTimeout(function () { layers.forEach(function (l) { l.resize(); }); }, 180);
        });
        document.addEventListener('visibilitychange', function () {
          layers.forEach(function (l) {
            document.visibilityState === 'hidden' ? l.stop() : l.start();
          });
        });
        if ('IntersectionObserver' in window) {
          new IntersectionObserver(function (e) {
            layers.forEach(function (l) { e[0].isIntersecting ? l.start() : l.stop(); });
          }, { threshold: 0 }).observe(hero);
        }
        document.addEventListener('ac:theme', function () {
          layers.forEach(function (l) { l.setColor(accentHex()); });
        });
        if (streaks) return;               /* front canvas is taken by GL */
      }
    }
    /* Canvas-2D fallback needs the CSS mask that keeps dust off the headline. */
    canvas.classList.add('hero__dust--fallback');

    var ctx = canvas.getContext('2d', { alpha: true });
    if (!ctx) return;

    var grains = [];
    var raf = null;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = 0, h = 0;
    var started = 0;
    var sprite = null;

    /* Dense while the caravan develops, then settling to a visible drift. */
    var STORM_MS = 3200;

    function rgb() {
      var hex = (getComputedStyle(document.documentElement)
                  .getPropertyValue('--accent').trim() || '#B08D57').replace('#', '');
      if (hex.length === 3) hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];
      var n = parseInt(hex, 16);
      return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
    }

    /* A soft pre-rendered mote. Drawing a blurred sprite reads as airborne
       dust; hard-edged arcs read as confetti and vanish at small sizes. */
    function buildSprite() {
      var c = rgb();
      var SP = 64;
      sprite = document.createElement('canvas');
      sprite.width = sprite.height = SP;
      var sc = sprite.getContext('2d');
      var g = sc.createRadialGradient(SP / 2, SP / 2, 0, SP / 2, SP / 2, SP / 2);
      g.addColorStop(0,    'rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',1)');
      g.addColorStop(0.35, 'rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',0.6)');
      g.addColorStop(1,    'rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',0)');
      sc.fillStyle = g;
      sc.fillRect(0, 0, SP, SP);
    }

    function resize() {
      var r = hero.getBoundingClientRect();
      w = Math.max(1, Math.round(r.width));
      h = Math.max(1, Math.round(r.height));
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      canvas.style.width = w + 'px';
      canvas.style.height = h + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      seed();
    }

    function seed() {
      /* Enough grains to actually read as blowing sand, still scaled to the
         viewport so a phone runs a fraction of a desktop field. */
      var target = Math.round(Math.min(300, Math.max(90, (w * h) / 4800)));
      grains = [];
      for (var i = 0; i < target; i++) grains.push(grain(true));
    }

    function grain(anywhere) {
      var big = Math.random() < 0.10;          /* a few larger, closer motes */
      return {
        x: anywhere ? Math.random() * w : -40 - Math.random() * 160,
        y: Math.random() * h,
        r: big ? 2.4 + Math.random() * 3.0 : 0.8 + Math.random() * 1.6,
        vx: 26 + Math.random() * 88,           /* px/s, blowing right */
        vy: -9 + Math.random() * 18,
        a: big ? 0.07 + Math.random() * 0.10
               : 0.14 + Math.random() * 0.26,
        drift: Math.random() * Math.PI * 2,
        sway: 4 + Math.random() * 12
      };
    }

    function draw(now) {
      if (!started) started = now;
      var elapsed = now - started;

      /* Opens as a gust, settles to a persistent drift rather than nothing —
         the client wants the sand present throughout, not just on entry. */
      var intensity = elapsed < STORM_MS
        ? 1 - 0.5 * (elapsed / STORM_MS)
        : 0.5;

      ctx.clearRect(0, 0, w, h);

      var dt = 1 / 60;
      for (var i = 0; i < grains.length; i++) {
        var g = grains[i];
        g.drift += 0.014;
        g.x += g.vx * dt;
        g.y += (g.vy + Math.sin(g.drift) * g.sway) * dt;

        if (g.x - g.r > w || g.y < -60 || g.y > h + 60) grains[i] = grain(false);

        ctx.globalAlpha = Math.min(1, g.a * intensity);
        ctx.drawImage(sprite, g.x - g.r, g.y - g.r, g.r * 2, g.r * 2);
      }
      ctx.globalAlpha = 1;
      raf = requestAnimationFrame(draw);
    }

    function start() { if (!raf) raf = requestAnimationFrame(draw); }
    function stop() { if (raf) { cancelAnimationFrame(raf); raf = null; } }

    buildSprite();
    resize();
    start();

    var rt = null;
    window.addEventListener('resize', function () {
      clearTimeout(rt);
      rt = setTimeout(resize, 180);
    });

    document.addEventListener('visibilitychange', function () {
      if (document.visibilityState === 'hidden') stop(); else start();
    });

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        entries[0].isIntersecting ? start() : stop();
      }, { threshold: 0 }).observe(hero);
    }

    document.addEventListener('ac:theme', buildSprite);
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

    /* The hero is a light scene, so the nav no longer needs an over-video
       state — it just picks up its blurred background once the page moves. */
    function onScroll() {
      nav.classList.toggle('nav--scrolled', (window.scrollY || window.pageYOffset) > 8);
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

    var metrics = p.en.metrics.map(function (m, i) {
      return '<span data-i18n="p.' + slug + '.m' + i + '">' + m + '</span>';
    }).join('');

    return '<article class="card"' +
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
      '<h3 class="card__title"><a class="card__link" href="product.html?p=' + slug + '" data-i18n="p.' + slug + '.name">' + p.en.name + '</a></h3>' +
      '<span class="card__price" data-i18n="shop.onRequest">On request</span>' +
      '</div>' +
      '<span class="card__grade" data-i18n="p.' + slug + '.grade">' + p.en.grade + '</span>' +
      '<div class="card__metrics">' + metrics + '</div>' +
      '<div class="card__actions">' +
      '<a class="btn btn--ghost btn--sm" href="assets/docs/' + slug + '.pdf" download data-i18n="cat.spec">Spec PDF</a>' +
      '<button type="button" class="link-quiet card__rfq" data-drawer-trigger data-i18n="cat.rfq">RFQ Price →</button>' +
      '</div>' +
      '<template class="card__spec">' +
      '<table class="spec"><thead><tr>' +
      '<th scope="col" data-i18n="cat.param">Parameter</th>' +
      '<th scope="col" data-i18n="cat.value">Value</th>' +
      '</tr></thead><tbody>' + spec + '</tbody></table>' +
      '<dl class="drawer__meta">' + meta + '</dl>' +
      '</template>' +
      '</article>';
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
      /* The noun has to agree with the count in Russian. */
      var wordEl = qs('#shopCountWord');
      if (wordEl && window.ACI18N && window.ACI18N.plural) {
        var w = window.ACI18N.plural('shop.products', shown);
        if (w) wordEl.textContent = w;
      }
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
    document.addEventListener('ac:lang', apply);
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
  /* Enquiries POST to FORM_ENDPOINT so they land in the company inbox without
     depending on the visitor having a mail client. Until an endpoint is set,
     it falls back to the mailto: behaviour so no lead is ever dropped.

     To go live: create a free form endpoint (Web3Forms, Formspree, or a
     Vercel function) and paste the URL below. If the service needs an access
     key, put it in FORM_KEY — it is a public submission key, not a secret. */

  var FORM_ENDPOINT = '';
  var FORM_KEY = '';

  function initForms() {
    qsa('form[data-mailto]').forEach(function (form) {
      var statusEl = qs('.form__status', form);
      var submitBtn = qs('button[type="submit"]', form);
      var submitKey = submitBtn && submitBtn.getAttribute('data-i18n');

      function labelFor(name) {
        var field = form.elements[name];
        if (field && field.id) {
          var lab = qs('label[for="' + field.id + '"]', form);
          if (lab) return lab.textContent.replace(/\*/g, '').trim();
        }
        return name;
      }

      function say(stateKey, fallback, tone) {
        if (!statusEl) return;
        statusEl.setAttribute('data-i18n', stateKey);
        statusEl.textContent = fallback;
        statusEl.classList.remove('is-error', 'is-ok');
        if (tone) statusEl.classList.add(tone);
        statusEl.classList.add('is-visible');
        if (window.ACI18N) window.ACI18N.retranslate(statusEl.parentNode);
      }

      function busy(on) {
        if (!submitBtn) return;
        submitBtn.disabled = on;
        submitBtn.classList.toggle('is-busy', on);
        if (on) {
          submitBtn.setAttribute('data-i18n', 'form.sending');
          submitBtn.textContent = 'Sending…';
        } else if (submitKey) {
          submitBtn.setAttribute('data-i18n', submitKey);
        }
        if (window.ACI18N) window.ACI18N.retranslate(form);
      }

      function fallbackToMail(payload) {
        var lines = Object.keys(payload).map(function (k) { return k + ': ' + payload[k]; });
        window.location.href = 'mailto:' + form.getAttribute('data-mailto') +
          '?subject=' + encodeURIComponent(form.getAttribute('data-subject') || 'Enquiry') +
          '&body=' + encodeURIComponent(lines.join('\n'));
        say('form.status', 'Your enquiry has been prepared in your mail client. Send it to reach the trading desk.');
      }

      form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (typeof form.reportValidity === 'function' && !form.reportValidity()) return;

        var payload = {};
        new FormData(form).forEach(function (value, key) {
          if (String(value).trim() !== '') payload[labelFor(key)] = value;
        });
        payload.subject = form.getAttribute('data-subject') || 'Enquiry';

        if (!FORM_ENDPOINT) { fallbackToMail(payload); return; }

        if (FORM_KEY) payload.access_key = FORM_KEY;
        busy(true);

        fetch(FORM_ENDPOINT, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify(payload)
        }).then(function (res) {
          if (!res.ok) throw new Error('HTTP ' + res.status);
          busy(false);
          form.reset();
          say('form.sent', 'Thank you — your enquiry has reached the trading desk. We reply within one business day.', 'is-ok');
        }).catch(function () {
          busy(false);
          say('form.failed', 'The enquiry could not be sent. Opening your mail client instead…', 'is-error');
          setTimeout(function () { fallbackToMail(payload); }, 1200);
        });
      });
    });
  }

  /* ----------------------------------------------------------------- GO --- */

  function boot() {
    initTheme();
    initSandEdges();
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
