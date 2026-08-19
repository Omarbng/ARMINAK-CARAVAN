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

  /* ------------------------------------- (SAND EDGES, REMOVED) ---------- */
  /* The screen-margin grains are gone at the client's request — "remove the
     elements on the sides of the site and keep just the video itself".

     Three tiers went with them, and they were the most delicate code in this
     file: a rendered alpha clip, a UA probe to pick VP8-in-WebM vs
     HEVC-in-MP4, a canvas read-back to verify the browser actually composited
     that alpha (Chrome decodes HEVC happily and then paints the colour plane
     as an opaque slab), a retry on the other codec, and a WebGL veil behind
     all of it. Roughly 150 lines whose entire job was to put grains in a
     margin that no longer exists.

     Deleted rather than left unreferenced: nothing calls it, and a dormant
     codec-probing stack is the kind of thing that gets "fixed" by someone
     later. */

  /* --------------------------------------------------------- QUALIFY ----- */
  /* Reads the four checkboxes and moves three things: the count, the meter,
     and one data-state that the stylesheet turns into wording and into the
     quotation button appearing.

     The wording lives in the markup and the language file, not here — this
     function never writes a sentence, so the RU/EN switch keeps ownership of
     the copy and there is nothing to translate twice. */

  function initQualify() {
    var list = qs('#qualList');
    var result = qs('#qualResult');
    if (!list || !result) return;

    var boxes = [].slice.call(list.querySelectorAll('.qual__box'));
    if (!boxes.length) return;

    var count = qs('#qualCount');
    var meter = qs('#qualMeter');

    /* Opts the section into the reveal behaviour. Until this lands the
       quotation button is simply visible, which is the correct no-JS state. */
    result.classList.add('is-live');

    function sync() {
      var n = 0;
      boxes.forEach(function (b) { if (b.checked) n++; });

      if (count) count.textContent = String(n);
      if (meter) meter.style.width = (n / boxes.length * 100) + '%';
      result.setAttribute('data-state', n === 0 ? '0' : n === boxes.length ? 'all' : 'some');
    }

    /* One listener on the list rather than four on the inputs: change bubbles,
       and the section is generated so the count can grow without touching
       this. */
    list.addEventListener('change', sync);
    sync();                              /* a reload can restore ticks */
  }

  /* -------------------------------------------------------- SECTION RAIL -- */
  /* The left-margin index. Two jobs: appear once the film is behind you, and
     say which section you are in.

     "Which section" is resolved by scroll position against each target's top,
     walking from the bottom up and taking the first one that has passed the
     mark. An IntersectionObserver is the usual reflex here and it is the wrong
     tool: these sections are taller than the viewport, so several are
     intersecting at once and the observer cannot say which one you are
     reading. A single comparison against one line can.

     The line sits at 38% of the viewport rather than the top, so a section
     becomes current when it dominates the screen, not when its first pixel
     appears. */

  function initRail() {
    var rail = qs('#rail');
    if (!rail) return;

    var items = [].slice.call(rail.querySelectorAll('.rail__item'));
    if (!items.length) return;

    /* Resolve the anchors once. A missing target is dropped rather than
       guarded on every frame — the rail is generated with the page, so a
       broken href is a build error, not a runtime condition. */
    var targets = [];
    items.forEach(function (a) {
      var el = document.getElementById(a.getAttribute('href').slice(1));
      if (el) targets.push({ a: a, el: el });
      else a.parentNode.hidden = true;
    });
    if (!targets.length) return;

    var hero = qs('#hero');
    var current = null;
    var ticking = false;

    function apply() {
      ticking = false;
      var y = window.scrollY || window.pageYOffset;
      var vh = window.innerHeight || document.documentElement.clientHeight;

      /* Off over the film: the hero has its own scroll cue, and an index of a
         page you have not started reading is noise. */
      var past = hero ? y > hero.offsetHeight * 0.66 : y > 8;
      rail.classList.toggle('is-on', past);

      var mark = y + vh * 0.38;
      var found = targets[0];
      for (var i = targets.length - 1; i >= 0; i--) {
        if (targets[i].el.offsetTop <= mark) { found = targets[i]; break; }
      }

      if (found.a === current) return;
      if (current) current.classList.remove('is-current');
      found.a.classList.add('is-current');
      found.a.setAttribute('aria-current', 'true');
      if (current) current.removeAttribute('aria-current');
      current = found.a;
    }

    function onScroll() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(apply);
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    apply();
  }

  /* ---------------------------------------------------------------- HERO -- */
  /* Full-bleed desert film with a windowed entrance: the caravan opens inside
     a framed window on the ivory ground, then the window opens outward and the
     film becomes the background.

     The sand is in the film. v1 layered a transparent alpha clip over the
     plate at runtime, which meant probing for VP8-vs-HEVC alpha and sampling a
     frame to catch WebKit painting the colour plane as an opaque slab. v2 has
     the storm composited in at render time, so none of that runs on the hero
     any more — one decode, no codec branch, nothing to verify. The alpha clip
     still drives the sand in the page margins, where there is no film to bake
     it into.

     Exactly one hero mp4 is loaded (portrait cut for phones, wide cut for
     everything else) so the browser never downloads both, and the cut is
     re-checked on resize and rotation rather than stranded at its mount-time
     value. Reduced motion and Data Saver skip the film and leave the poster
     up. */

  var HOLD_MS = 1150;      /* how long the window holds before it opens */
  var READY_CAP_MS = 2000; /* open anyway if the film is still buffering */

  function initHero() {
    var hero = qs('#hero');
    if (!hero) return;

    var root = document.documentElement;
    var intro = root.classList.contains('ac-intro');   /* set before first paint */
    var opened = false;

    /* Opening the window is also what starts the copy, so the two read as one
       move. Without an intro this runs on the next frame, which is the old
       behaviour exactly. */
    function open(fast) {
      if (opened) return;
      opened = true;
      if (fast) hero.classList.add('hero--fast');
      root.classList.remove('ac-intro', 'ac-mounted');
      hero.classList.add('hero--revealed', 'hero--settled');
      /* Read back by the pre-paint script in the <head>, which is what
         actually decides whether the next page load gets the window.
         Private mode can throw on write; then the intro simply replays. */
      try { sessionStorage.setItem('ac_intro', '1'); } catch (e) {}
      document.dispatchEvent(new CustomEvent('ac:herosettled'));
    }

    if (!intro) {
      requestAnimationFrame(function () {
        requestAnimationFrame(function () { open(false); });
      });
    } else {
      /* The plate rises into place rather than being there from the first
         frame — which needs a paint at the start value before the class that
         moves it lands. */
      requestAnimationFrame(function () {
        requestAnimationFrame(function () { root.classList.add('ac-mounted'); });
      });

      /* A reader who scrolls or clicks during the window has told us they are
         done watching — finish in 260ms rather than cut. */
      var skip = function () { open(true); teardown(); };
      var events = ['wheel', 'touchstart', 'keydown', 'pointerdown', 'scroll'];
      function teardown() {
        events.forEach(function (e) { window.removeEventListener(e, skip); });
      }
      events.forEach(function (e) {
        window.addEventListener(e, skip, { passive: true, once: true });
      });
    }

    var layer = qs('.hero__layer', hero);
    if (!layer) return;

    var mm = window.matchMedia;
    if (!mm) { open(false); return; }                  /* poster stays up */

    if (mm('(prefers-reduced-motion: reduce)').matches) { open(false); return; }

    /* A 1MB autoplaying background is exactly what Data Saver exists to
       prevent. */
    var conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    if (conn && conn.saveData) { open(false); return; }

    var mqMobile = mm('(max-width: 768px), (orientation: portrait)');

    function srcNow() {
      return hero.getAttribute(mqMobile.matches ? 'data-video-mobile' : 'data-video-desktop');
    }

    var src = srcNow();
    if (!src) { open(false); return; }

    var video = makeBackgroundVideo('hero__video', src);
    video.addEventListener('canplay', function () {
      video.classList.add('is-ready');
      arm();
    });
    layer.appendChild(video);

    /* Hold the window until the film is actually moving in it — a window onto
       a still poster is a worse first impression than a slightly later open. */
    var t0 = now();
    var armed = false;
    function arm() {
      if (armed || !intro) return;
      armed = true;
      setTimeout(function () { open(false); }, Math.max(0, HOLD_MS - (now() - t0)));
    }
    if (intro) setTimeout(arm, READY_CAP_MS);

    function play() {
      var p = video.play();
      if (p && p.catch) p.catch(function () {});     /* poster stays up if refused */
    }
    play();


    /* Rotating a phone, or dragging a desktop window across 768px, otherwise
       strands the wrong cut for the rest of the session — a 9:16 crop stretched
       across a laptop, or the reverse. The poster swaps itself through
       <picture media>; this is the film half of the same move.

       load() runs only on a genuine change of source. Calling it at mount
       aborts the request the browser has already started and fetches it twice,
       which is the bug this guard exists to prevent. */
    var loadedSrc = src;
    function onBreakpoint() {
      var next = srcNow();
      if (!next || next === loadedSrc) return;
      loadedSrc = next;
      video.classList.remove('is-ready');   /* fall back to the poster mid-swap */
      video.src = next;
      video.load();
      play();
    }
    if (mqMobile.addEventListener) mqMobile.addEventListener('change', onBreakpoint);
    else if (mqMobile.addListener) mqMobile.addListener(onBreakpoint);  /* Safari < 14 */

    /* Safari intermittently ignores autoplay, and a tab restored from the
       background can come back paused. */
    document.addEventListener('visibilitychange', function () {
      if (document.visibilityState !== 'visible') return;
      play();
    });

    /* Nothing to decode while the hero is off screen. */
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting) play();
        else video.pause();
      }, { threshold: 0 }).observe(hero);
    }
  }

  /* No sand drawn over the film, and no pointer parallax on it either. Both
     were removed at the client's request — "remove any effect from the video".
     The plate now plays exactly as it was rendered.

     What is left on the hero is not effects on the video: the scrim (white type
     is illegible on lit sand without it), the fade where the film becomes the
     page, and the window the film opens out of.

     This left ACSand with no callers anywhere, so sand.js is no longer loaded
     on any page — 29KB of shader that nothing asks for. The file itself is
     kept in the tree; it is the only real sand renderer here and re-adding a
     script tag is cheaper than writing it again. */

  function now() {
    return (window.performance && performance.now) ? performance.now() : Date.now();
  }

  /* Muted, looping, inline, invisible to assistive tech — the page's <h1>
     stays the first real content. */
  function makeBackgroundVideo(className, src) {
    var v = document.createElement('video');
    v.className = className;
    v.muted = true;                     /* property, not attribute: iOS reads this */
    v.defaultMuted = true;
    v.loop = true;
    v.autoplay = true;
    v.preload = 'auto';
    v.setAttribute('muted', '');
    v.setAttribute('playsinline', '');
    v.setAttribute('webkit-playsinline', '');
    v.setAttribute('aria-hidden', 'true');
    v.tabIndex = -1;
    v.src = src;
    return v;
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

  /* -------------------------------------------------------- CORRIDOR GLOBE -- */
  /* The trade lanes on the actual planet. three.js is ~780KB of geometry and
     library, so it is never part of first paint: the flat SVG ships in the
     markup and the globe only replaces it once this section is scrolled to,
     on a wide viewport, with WebGL, at full motion and off Data Saver. Any of
     those failing simply leaves the drawn route in place. */

  function initCorridorGlobe() {
    var host = qs('#corridorGlobe');
    if (!host || !window.matchMedia) return;
    if (!window.IntersectionObserver || !window.Promise) return;

    /* The globe used to be desktop-only, which left phones on the old flat
       route diagram. It now mounts everywhere WebGL exists — but it is ~856KB
       of three.js, OrbitControls and coastline data, so the gates that matter
       on a phone stay: it is imported lazily when the section scrolls into
       view, never on Data Saver, and never against reduced motion. */
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    var conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    if (conn && conn.saveData) return;

    /* Cheap probe first — mounting three.js only to discover there is no
       context wastes the whole download. */
    try {
      var c = document.createElement('canvas');
      if (!(c.getContext('webgl') || c.getContext('experimental-webgl'))) return;
    } catch (e) { return; }

    var started = false;
    var view = null;

    new IntersectionObserver(function (entries, obs) {
      if (!entries[0].isIntersecting) { if (view) view.pause(); return; }
      if (view) { view.resume(); return; }
      if (started) return;
      started = true;

      /* Sibling of this file: import() in a classic script resolves against
         the script's own URL, not the document's. */
      import('./globe.js').then(function (mod) {
        return mod.mountGlobe(host);
      }).then(function (g) {
        if (!g) return;                       /* keep the flat route */
        view = g;
        host.classList.add('is-live');
        var flat = qs('#corridorFlat');
        if (flat) flat.hidden = true;
        var hint = qs('#corridorHint');
        if (hint) hint.hidden = false;
        var lanes = qs('#corridorLanes');
        if (lanes) lanes.hidden = false;
        initCorridorReveal(g);
        initCorridorPicking(g);
      }).catch(function () {
        /* Older engine, blocked module, anything at all — the SVG is still
           sitting there doing its job. */
      });
    }, { rootMargin: '200px 0px' }).observe(host);
  }

  /* The corridors build as you arrive at them rather than playing once and
     stopping. Scroll position is the timeline: the section's travel through
     the viewport maps to 0..1, each waypoint owns a fifth of it, and the globe
     and the manifest read the same number — so a row lights at the exact
     moment its lane finishes drawing.

     Tied to scroll rather than to a timer because the two then cannot drift,
     and because scrolling back up unwinds it. A reader who scrolls half way,
     stops, and comes back gets the corridor half drawn and waiting, which is
     the behaviour that makes it feel like an instrument rather than a video. */
  function initCorridorReveal(globe) {
    var section = qs('#corridors');
    if (!section) return;

    var rows = [].slice.call(document.querySelectorAll('#corridorLanes tr'))
                 .slice(1);                  /* drop the head row */
    var ticking = false;

    /* The timeline is the section's arrival, not its exit.

       It used to end when the section's *bottom* edge reached a quarter up the
       viewport — which is only true once the section has almost entirely
       scrolled off the top. So a reader looking straight at the globe was at
       p≈0.55, and Jebel Ali and East Africa never connected until they had
       scrolled well past the thing they were meant to be watching.

       Now p runs from "top edge entering at the bottom" to "top edge near the
       top of the viewport" — the natural reading position — so the build
       completes with the globe framed. The span is viewport-relative but
       clamped, because tying it to the section's own height made the pacing a
       function of however tall the sphere happened to render: a ~850px section
       needed ~1280px of scroll for five waypoints. */
    var SPAN_MIN = 380, SPAN_MAX = 760;

    function measure() {
      var r = section.getBoundingClientRect();
      var vh = window.innerHeight || document.documentElement.clientHeight;
      var start = vh * 0.90;                 /* p=0: section top entering     */
      var end   = vh * 0.12;                 /* p=1: section top nearly aloft */
      var span  = Math.max(SPAN_MIN, Math.min(SPAN_MAX, start - end));
      return (start - r.top) / span;
    }

    function apply() {
      ticking = false;
      if (!globe || !globe.setProgress) return;

      /* The globe owns the thresholds and hands back the per-waypoint state,
         so a row can no longer light out of step with its own lane. */
      var lit = globe.setProgress(measure());
      if (!lit) return;

      for (var i = 0; i < rows.length; i++) {
        rows[i].classList.toggle('is-lit', !!lit[i]);
      }
    }

    function onScroll() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(apply);
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    apply();
  }

  /* Picking a waypoint — from the sphere or from the manifest, same state.

     The globe is aria-hidden and cannot take focus, so the table is the real
     control: rows are the keyboard path in, and the sphere is the pointer path.
     Both call the same select(), and the globe reports back through onSelect so
     whichever one you used, the other agrees.

     The attributes are added here rather than in the markup because the
     language switcher assigns textContent to those cells — anything nested in
     them would be wiped on the first EN/RU switch. */
  function initCorridorPicking(globe) {
    if (!globe || !globe.select) return;

    var rows = [].slice.call(document.querySelectorAll('#corridorLanes tr')).slice(1);
    if (!rows.length) return;

    function paint(i) {
      rows.forEach(function (row, k) {
        var on = k === i;
        row.classList.toggle('is-picked', on);
        row.setAttribute('aria-pressed', String(on));
      });
    }

    rows.forEach(function (row, i) {
      row.tabIndex = 0;
      row.setAttribute('role', 'button');
      row.setAttribute('aria-pressed', 'false');
      /* silent: the table already knows, so it paints from the return value
         rather than being told again through the callback. */
      row.addEventListener('click', function () { paint(globe.select(i, true)); });
      row.addEventListener('keydown', function (e) {
        if (e.key !== 'Enter' && e.key !== ' ') return;
        e.preventDefault();                  /* Space would scroll the page */
        paint(globe.select(i, true));
      });
    });

    /* The sphere reports its own picks so the table follows the pointer. */
    if (globe.setOnSelect) globe.setOnSelect(paint);

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && globe.selected() !== null) paint(globe.select(null, true));
    });
  }

  /* ----------------------------------------------------------------- NAV -- */

  function initNav() {
    var nav = qs('#nav');
    if (!nav) return;

    var hero = qs('#hero');
    var burger = qs('#navBurger');
    var menu = qs('#navMenu');

    /* Over the film the bar is transparent and cream; past the hero it picks
       up its blurred page-coloured background. Pages without a hero only ever
       do the second half.

       During the intro the ground behind the bar is ivory, not film, so cream
       would be invisible — the bar keeps page colours until the window opens
       and the film actually reaches the top of the screen. */
    /* Exactly one of three states, always. The previous version had a fourth,
       unnamed one: during the intro it removed BOTH classes and returned, which
       leaves a bar with no background over page content. That is the overlap —
       the mark and the quotation button sitting directly on whatever scrolls
       under them, with the press marquee reading straight through the bar.

       The fix is that "solid" is decided by scroll position alone. Whether the
       intro is still running only decides the text colour, never whether the
       bar has a background. */
    function onScroll() {
      var y = window.scrollY || window.pageYOffset;
      var intro = document.documentElement.classList.contains('ac-intro');

      /* No hero on this page: the bar is over page content from 8px down. */
      var onFilm = hero ? y < hero.offsetHeight - nav.offsetHeight : y <= 8;

      /* Cream type needs the film behind it. During the window beat the ground
         is still ivory, so the bar keeps page colours even though it has not
         scrolled yet. */
      nav.classList.toggle('nav--over', onFilm && !intro);
      nav.classList.toggle('nav--scrolled', !onFilm);
    }

    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    document.addEventListener('ac:herosettled', onScroll);

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

    /* Every link in the panel, not just .nav__link — the panel's quotation
       button and mail line are same-page anchors on contact.html, and would
       otherwise leave the menu open over a body still locked to no-scroll. */
    qsa('a', menu).forEach(function (a) { a.addEventListener('click', closeMenu); });
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

  /* Rail cards are for browsing, not transacting. Each one used to carry a
     hover-only Quick RFQ, a Spec PDF button and an RFQ Price link — twenty-four
     buttons across the twelve cards on the landing page, which is most of what
     made it feel busy. The card title links to the product page, where both
     actions live in full. The catalogue grid is built by build_catalogue.py and
     still carries them, because that is the shopping context. */
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
      '</div>' +
      '<div class="card__row">' +
      '<h3 class="card__title"><a class="card__link" href="product.html?p=' + slug + '" data-i18n="p.' + slug + '.name">' + p.en.name + '</a></h3>' +
      '<span class="card__price" data-i18n="shop.onRequest">On request</span>' +
      '</div>' +
      '<span class="card__grade" data-i18n="p.' + slug + '.grade">' + p.en.grade + '</span>' +
      '<div class="card__metrics">' + metrics + '</div>' +
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

  /* ----------------------------------------------------------- DESK CLOCK -- */
  /* The footer states whether the trading desk is actually staffed right now,
     in Abu Dhabi time rather than the visitor's. The UAE moved its weekend to
     Saturday–Sunday in January 2022, so the working week is Mon–Fri — not the
     Sun–Thu that older references still give. The markup ships with the plain
     opening hours and no data-open attribute, so a visitor without JS reads
     something true rather than a stale "open".

     Only the attribute and the clock digits are written here — never the
     label text, which belongs to i18n.js. */

  function initDeskClock() {
    var host = qs('#deskStatus');
    var out = qs('#deskClock');
    if (!host || !out) return;

    var OPEN_H = 9, CLOSE_H = 18;
    var WORKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];

    var fmt;
    try {
      fmt = new Intl.DateTimeFormat('en-GB', {
        timeZone: 'Asia/Dubai', hour: '2-digit', minute: '2-digit',
        weekday: 'short', hour12: false
      });
      fmt.formatToParts(new Date());
    } catch (e) {
      return;                     /* no tz database — the hours line stands */
    }

    function tick() {
      var part = {};
      fmt.formatToParts(new Date()).forEach(function (p) { part[p.type] = p.value; });

      var h = parseInt(part.hour, 10);
      if (h === 24) h = 0;         /* some engines emit 24 at midnight */

      var open = WORKDAYS.indexOf(part.weekday) > -1 && h >= OPEN_H && h < CLOSE_H;

      out.textContent = (h < 10 ? '0' + h : h) + ':' + part.minute;
      host.setAttribute('data-open', open ? '1' : '0');
    }

    tick();
    setInterval(tick, 30000);
  }

  /* ----------------------------------------------------------------- GO --- */

  function boot() {
    initTheme();
    initDeskClock();
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
    initRail();
    initQualify();
    initScramble();
    initCorridorGlobe();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
