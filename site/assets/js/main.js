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
  /* The client asked for sand at the screen edges on every page, and then for
     that sand to be real rather than drawn. Three tiers, best first:

       1. the rendered clip — the same grains that blow across the hero
       2. the WebGL veil — procedural, when the film can't play
       3. the tiled SVG in the stylesheet — static, when neither can

     All three wear the same CSS mask, so the desert stays in the margins and
     never sits under body copy. */

  var SAND_WEBM = 'assets/hero/sand.webm';   /* VP8 + alpha  */
  var SAND_MP4  = 'assets/hero/sand.mp4';    /* HEVC + alpha, for WebKit */

  function initSandEdges() {
    var host = qs('.sand-edges');
    if (!host) return;
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    var conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    if (conn && conn.saveData) return;        /* the static tile is free */

    if (initSandFilm(host)) return;           /* real grains win */
    initSandVeilGL(host);
  }

  /* Returns true once the rendered sand is on the page. */
  function initSandFilm(host) {
    var src = sandSource();
    if (!src) return false;

    var film = makeBackgroundVideo('sand-edges__film', src);
    revealWhenTransparent(film, src === SAND_MP4 ? SAND_WEBM : SAND_MP4);
    host.appendChild(film);
    host.classList.add('sand-edges--film');

    /* If the alpha check pulls the film, the margins fall back to the shader
       veil rather than being left bare. */
    film.addEventListener('ac:sandpulled', function () {
      host.classList.remove('sand-edges--film');
      initSandVeilGL(host);
    });

    function play() {
      var p = film.play();
      if (p && p.catch) p.catch(function () {});
    }
    play();

    document.addEventListener('visibilitychange', function () {
      if (document.visibilityState === 'visible') play(); else film.pause();
    });

    /* On the landing page the hero film carries its own storm, composited into
       the plate at render time. Grains in the margins on top of that is double
       the sand for a second decode, so the margins stand down while the hero
       holds the screen — but only once the film is actually holding it.

       During the window beat the film is a small frame on the ivory ground and
       these margins are the only sand around it, which is the half of the
       brief that asks for the sand to be real too. So the handover waits for
       hero--revealed. The 1600ms opacity transition on the film makes it a
       fade, not a cut, and it lands while the window is still opening. */
    var hero = qs('#hero');
    if (hero && 'IntersectionObserver' in window) {
      var onScreen = false;

      function sync() {
        /* Keyed to the film, not to a separate sand layer: if the hero fell
           back to its poster the plate is still, and the margins are then the
           only sand there is. Both cuts carry the storm, so this holds on a
           phone as well. */
        var covered = onScreen &&
                      hero.classList.contains('hero--revealed') &&
                      !!hero.querySelector('.hero__video');
        film.style.opacity = covered ? '0' : '';
        if (covered) film.pause(); else play();
      }

      new IntersectionObserver(function (entries) {
        onScreen = entries[0].isIntersecting;
        sync();
      }, { threshold: 0 }).observe(hero);

      /* Opening the window is not an intersection change, so the observer
         alone would leave the margins running under a full-bleed film. */
      document.addEventListener('ac:herosettled', sync);
    }

    return true;
  }

  function initSandVeilGL(host) {
    if (!window.ACSand) return;

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

    mountHeroSand(hero, mqMobile);

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

  /* The sand over the film, rendered live rather than baked or filmed.
     Two layers, because wind-blown sand is two different things and drawing
     only the second is what made the old version look like light streaking
     past the camera:

       veil   — suspension. The fine fraction hanging in the air, which is
                what actually reads as "there is sand in this shot": it lowers
                contrast and warms the plate. Does most of the work, and you
                are not meant to notice it as an object.
       grain  — saltation. The heavier fraction skipping along the surface.
                An accent on top of the veil, dense and faint. See sand.js —
                a thousand near-invisible dashes, not two hundred bright ones.

     Desktop only: two more full-screen GL passes is a battery tax on a phone,
     and the portrait crop is mostly sky and dune face anyway. Skipped whole
     under reduced motion and Data Saver, since initHero has already returned
     by then and never calls this. */
  function mountHeroSand(hero, mqMobile) {
    if (!window.ACSand || mqMobile.matches) return;

    var wrap = document.createElement('div');
    wrap.className = 'hero__sandwrap';
    wrap.setAttribute('aria-hidden', 'true');

    var layers = [
      { cls: 'hero__sand hero__sand--veil',  opts: { mode: 'veil',    base: 0.72, open: 1.30, openMs: 3200, wind: 0.11, scale: 0.7, fps: 30, seed: 4.1 } },
      { cls: 'hero__sand hero__sand--grain', opts: { mode: 'streaks', base: 0.95, open: 1.25, openMs: 2600, fps: 45, seed: 9.2 } }
    ];

    var made = [];
    layers.forEach(function (L) {
      var canvas = document.createElement('canvas');
      canvas.className = L.cls;
      wrap.appendChild(canvas);
      var s = window.ACSand(canvas, hero, L.opts);
      if (s) made.push({ sand: s, canvas: canvas });
      else wrap.removeChild(canvas);
    });

    if (!made.length) return;            /* no WebGL: the film stands alone */
    hero.appendChild(wrap);

    function sandHex() {
      return getComputedStyle(document.documentElement)
               .getPropertyValue('--sand').trim() || '#C7A87A';
    }

    made.forEach(function (m) {
      m.sand.setColor(sandHex());
      m.sand.resize();
      m.sand.start();
      m.canvas.classList.add('is-ready');
    });

    var rt = null;
    window.addEventListener('resize', function () {
      clearTimeout(rt);
      rt = setTimeout(function () {
        made.forEach(function (m) { m.sand.resize(); });
      }, 180);
    });

    /* Nothing to draw while the hero is off screen or the tab is hidden. */
    function run(on) {
      made.forEach(function (m) { on ? m.sand.start() : m.sand.stop(); });
    }
    document.addEventListener('visibilitychange', function () {
      run(document.visibilityState === 'visible');
    });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (e) { run(e[0].isIntersecting); },
                               { threshold: 0 }).observe(hero);
    }
    document.addEventListener('ac:theme', function () {
      made.forEach(function (m) { m.sand.setColor(sandHex()); });
    });
  }

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

  /* Transparent video is the one place the codecs genuinely diverge: VP8 with
     alpha in WebM everywhere except WebKit, HEVC with alpha in MP4 on WebKit.
     Guessing wrong paints an opaque cream rectangle over the hero, so anything
     unrecognised gets no sand layer at all — the film's own storm still runs. */
  function sandSource() {
    var ua = navigator.userAgent;
    var webkit = /Safari/.test(ua) && !/Chrome|Chromium|Android|CriOS|FxiOS|Edg/.test(ua);
    var probe = document.createElement('video');

    if (webkit) {
      return probe.canPlayType('video/mp4; codecs="hvc1"') ? SAND_MP4 : null;
    }
    return probe.canPlayType('video/webm; codecs="vp8"') ? SAND_WEBM : null;
  }

  /* The user-agent string only says which file to TRY. Whether the browser
     actually composites that file's alpha is a different question, and getting
     it wrong is not a subtle bug: Chrome decodes HEVC happily and then paints
     the colour plane as an opaque slab over the hero. Verified in Chrome —
     it is as bad as it sounds.

     So the picture is checked, not assumed. One frame goes into a 64x36
     canvas and the alpha channel is read back. Alpha compositing working means
     transparent pixels stay transparent; a browser ignoring alpha returns 255
     everywhere. Same-origin, so the canvas is never tainted, and it costs one
     read of 2304 pixels, once. */
  function verifyAlpha(video) {
    try {
      var c = document.createElement('canvas');
      c.width = 64; c.height = 36;
      var ctx = c.getContext('2d', { willReadFrequently: false });
      if (!ctx) return null;                        /* can't tell — caller decides */
      ctx.clearRect(0, 0, 64, 36);
      ctx.drawImage(video, 0, 0, 64, 36);
      var data = ctx.getImageData(0, 0, 64, 36).data;
      var min = 255;
      for (var i = 3; i < data.length; i += 4) {
        if (data[i] < min) min = data[i];
        if (min < 250) return true;                 /* genuine transparency found */
      }
      return false;                                 /* fully opaque: alpha ignored */
    } catch (e) {
      return null;                                  /* blocked — treat as unknown */
    }
  }

  /* Fade the sand in only once its transparency is confirmed. If the picture
     comes back opaque, the layer is pulled before it can ever be seen, and the
     other codec gets one chance in case the engine guess was simply wrong. */
  function revealWhenTransparent(video, altSrc) {
    var checked = false;

    video.addEventListener('loadeddata', function () {
      if (checked) return;
      checked = true;

      var ok = verifyAlpha(video);
      if (ok === false) {
        video.classList.remove('is-ready');
        if (altSrc) {
          checked = false;                          /* one retry, other codec */
          video.src = altSrc;
          var p = video.play();
          if (p && p.catch) p.catch(function () {});
          return;
        }
        try { video.dispatchEvent(new CustomEvent('ac:sandpulled')); } catch (e) {}
        if (video.parentNode) video.parentNode.removeChild(video);
        return;
      }
      /* true, or null when the check itself was unavailable — the film's own
         composited storm is the fallback either way, so showing it is safe. */
      video.classList.add('is-ready');
    });
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
     transform + scale only, fully compositor-friendly.

     The sand rides the same loop at nearly twice the distance. Grains hanging
     in the air are the closest thing to the camera, so they have to travel
     further than the dunes behind them or the two layers read as one flat
     picture with specks painted on. The extra scale is not decoration: it
     covers the edge the larger offset would otherwise drag into frame. */

  var SAND_DEPTH = 1.8;

  function initHeroParallax() {
    var hero = qs('#hero');
    if (!hero || !window.matchMedia) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (!window.matchMedia('(pointer: fine)').matches) return;

    var media = qs('.hero__media', hero);
    if (!media) return;

    /* Mounted by initHero a moment earlier, and absent on phones, Data Saver
       and machines without WebGL — so it is optional, not assumed. */
    var sand = qs('.hero__sandwrap', hero);

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

      if (sand) {
        var sScale = 1 + 0.045 * SAND_DEPTH * ca;
        sand.style.transform =
          'translate3d(' + (cx * SAND_DEPTH).toFixed(2) + 'px,' +
                           (cy * SAND_DEPTH).toFixed(2) + 'px,0) scale(' + sScale.toFixed(4) + ')';
      }

      if (Math.abs(tx - cx) > 0.05 || Math.abs(ty - cy) > 0.05 || Math.abs(ta - ca) > 0.002) {
        raf = requestAnimationFrame(tick);
      } else {
        raf = null;
        if (ta === 0) {
          media.style.transform = '';
          if (sand) sand.style.transform = '';
        }
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

    if (!matchMedia('(min-width: 1000px)').matches) return;
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
      }).catch(function () {
        /* Older engine, blocked module, anything at all — the SVG is still
           sitting there doing its job. */
      });
    }, { rootMargin: '200px 0px' }).observe(host);
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
    function onScroll() {
      var y = window.scrollY || window.pageYOffset;
      if (!hero) {
        nav.classList.toggle('nav--scrolled', y > 8);
        return;
      }
      if (document.documentElement.classList.contains('ac-intro')) {
        nav.classList.remove('nav--over', 'nav--scrolled');
        return;
      }
      var over = y < hero.offsetHeight - nav.offsetHeight;
      nav.classList.toggle('nav--over', over);
      nav.classList.toggle('nav--scrolled', !over);
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
    initCorridorGlobe();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
