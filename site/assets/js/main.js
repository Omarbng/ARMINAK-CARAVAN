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
    /* Two shapes of control, one state. The footer keeps the pill toggle it
       has always had; the navigation panel carries a two-up segmented control
       beside the language pair, because in a preferences strip a switch next
       to a text pair reads as two unrelated widgets.

       .theme-toggle is pressed when dark (it is one button that flips).
       .theme-set names the theme it selects, so it is pressed when the page is
       already on that theme. Both are synced here rather than in their own
       handlers, so any number of either can exist on a page. */
    function sync(theme) {
      qsa('.theme-toggle').forEach(function (b) {
        b.setAttribute('aria-pressed', String(theme === 'dark'));
      });
      qsa('.theme-set').forEach(function (b) {
        b.setAttribute('aria-pressed', String(b.getAttribute('data-theme-set') === theme));
      });
    }

    function apply(theme) {
      document.documentElement.setAttribute('data-theme', theme);
      try { localStorage.setItem(THEME_KEY, theme); } catch (e) {}
      sync(theme);
      document.dispatchEvent(new CustomEvent('ac:theme', { detail: { theme: theme } }));
    }

    function current() {
      return document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    }

    qsa('.theme-toggle').forEach(function (btn) {
      btn.addEventListener('click', function () {
        apply(current() === 'dark' ? 'light' : 'dark');
      });
    });

    qsa('.theme-set').forEach(function (btn) {
      btn.addEventListener('click', function () {
        apply(btn.getAttribute('data-theme-set') === 'dark' ? 'dark' : 'light');
      });
    });

    /* The pre-paint script in <head> sets data-theme straight from storage and
       nothing has told the controls about it, so the segmented control would
       load showing Light on a dark page. */
    sync(current());
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

  /* ----------------------------------------------------- NAVIGATION ------ */
  /* One panel, every page, every width. It replaced three separate things: the
     page links in the bar at desktop, the burger panel those folded into below
     1024, and a floating rail that listed the current page's sections. Three
     mechanisms for one job, none of which knew about the others.

     Two responsibilities: open and close the panel, and keep the "on this page"
     list pointing at the section actually being read.

     Note this runs on every page, and on pages with no section group the second
     half returns early — the panel is still the navigation, it just has nothing
     local to track. */

  function initNavPanel() {
    var panel = qs('#navPanel');
    var trig = qs('#navTrig');
    if (!panel || !trig) return;

    var sheet = qs('.navpanel__sheet', panel);
    var lastFocus = null;

    function setOpen(open) {
      panel.setAttribute('data-open', open ? 'true' : 'false');
      trig.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.classList.toggle('no-scroll', open);

      if (open) {
        lastFocus = document.activeElement;
        /* The first link, not the sheet — a keyboard user should land on
           something actionable rather than tab past the close button first. */
        var first = qs('.navpanel__link', panel);
        if (first) first.focus();
      } else if (lastFocus && lastFocus.focus) {
        lastFocus.focus();
      }
    }

    trig.addEventListener('click', function () {
      setOpen(panel.getAttribute('data-open') !== 'true');
    });

    qsa('[data-nav-close]', panel).forEach(function (el) {
      el.addEventListener('click', function () { setOpen(false); });
    });

    /* Every link closes it, in-page ones included — those otherwise leave a
       full-height sheet sitting over the section just scrolled to. */
    qsa('a', panel).forEach(function (a) {
      a.addEventListener('click', function () { setOpen(false); });
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && panel.getAttribute('data-open') === 'true') setOpen(false);
    });

    /* Focus must not walk out of an open sheet into the page behind it. */
    if (sheet) {
      sheet.addEventListener('keydown', function (e) {
        if (e.key !== 'Tab') return;
        var f = qsa('a[href], button:not([disabled])', sheet);
        if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      });
    }

    /* ---- which section am I in ---- */

    var secs = [];
    qsa('.navpanel__link--sec', panel).forEach(function (a) {
      var el = document.getElementById(a.getAttribute('href').slice(1));
      if (el) secs.push({ a: a, el: el });
      else a.parentNode.hidden = true;        /* anchor with no target: build bug */
    });
    if (!secs.length) return;

    var current = null, ticking = false;

    function mark() {
      ticking = false;
      var y = window.scrollY || window.pageYOffset;
      var vh = window.innerHeight || document.documentElement.clientHeight;

      /* One line at 38% of the viewport, walked bottom-up. These sections are
         taller than the viewport, so several are on screen at once and an
         IntersectionObserver cannot say which is being read; one comparison
         against one line can. */
      var line = y + vh * 0.38;
      var found = secs[0];
      for (var i = secs.length - 1; i >= 0; i--) {
        if (secs[i].el.offsetTop <= line) { found = secs[i]; break; }
      }

      if (found.a === current) return;
      if (current) { current.classList.remove('is-current'); current.removeAttribute('aria-current'); }
      found.a.classList.add('is-current');
      found.a.setAttribute('aria-current', 'true');
      current = found.a;
    }

    function onScroll() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(mark);
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    mark();
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
    /* There is no drawn fallback behind this any more, so whenever the globe is
       not going to run the manifest has to carry the section by itself — shown,
       and fully lit, since there is no scroll reveal to light it. */
    function manifestOnly() {
      var t = qs('#corridorLanes');
      if (!t) return;
      t.hidden = false;
      [].slice.call(t.querySelectorAll('tr')).slice(1).forEach(function (r) {
        r.classList.add('is-lit');
      });
    }

    if (matchMedia('(prefers-reduced-motion: reduce)').matches) { manifestOnly(); return; }

    var conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    if (conn && conn.saveData) { manifestOnly(); return; }

    /* Cheap probe first — mounting three.js only to discover there is no
       context wastes the whole download. */
    try {
      var c = document.createElement('canvas');
      if (!(c.getContext('webgl') || c.getContext('experimental-webgl'))) { manifestOnly(); return; }
    } catch (e) { manifestOnly(); return; }

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
        if (!g) { manifestOnly(); return; }   /* no context after all */
        view = g;
        host.classList.add('is-live');
        var hint = qs('#corridorHint');
        if (hint) hint.hidden = false;
        var lanes = qs('#corridorLanes');
        if (lanes) lanes.hidden = false;
        initCorridorReveal(g);
        initCorridorPicking(g);
      }).catch(function () {
        /* Older engine, blocked module, anything at all. */
        manifestOnly();
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

    /* The landing page opens on the film; every interior page now opens on a
       still from it (.pagehero). Both want the cream bar while that band is
       still behind it, so "over the film" resolves to either. A page with
       neither is never over one — see the note in onScroll. */
    var film = hero || qs('.pagehero');

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

      /* "Over the film" requires a film. This used to read `y <= 8` on pages
         with no hero, which made every interior page start life over an
         imaginary one: at scroll 0 the bar took .nav--over and painted the
         wordmark, the language pair and the quotation button cream #FDF6EA —
         on a white page. The header was invisible on load on catalogue,
         about, insights, contact, product and all four notes; the trigger was
         the only thing you could see, because it is the one control the class
         does not recolour. A page with no film is never over one. */
      var onFilm = film ? y < film.offsetHeight - nav.offsetHeight : false;

      /* Cream type needs the film behind it. During the window beat the ground
         is still ivory, so the bar keeps page colours even though it has not
         scrolled yet. */
      nav.classList.toggle('nav--over', onFilm && !intro);

      /* Solid once anything is actually passing underneath — which is also
         what gives an interior page a full-height bar in page colours at rest,
         rather than a condensed one occluding nothing. Past a hero, y is
         always well beyond 8, so film pages are unchanged. */
      nav.classList.toggle('nav--scrolled', !onFilm && y > 8);
    }

    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    document.addEventListener('ac:herosettled', onScroll);

  }

  /* -------------------------------------------------------- SCROLL REVEAL -- */

  function initReveal() {
    /* .footer__sign joins the list so the seal performs its sunrise the first
       time it is scrolled to — the CSS hangs the one-shot off .in-view. Only
       the footer lockup is observed: the one in the bar is on screen at load,
       so it would fire against the bar's own entrance and read as two
       animations arguing. That one lights on hover, which is the only way you
       can ask it to. */
    var els = qsa('.fade-up, .corridor, .footer__sign');
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

  /* ----------------------------------------------------------- SCROLL CUE -- */
  /* [data-scroll-to="#id"] advances one section. The page sets
     scroll-behavior:smooth and scroll-padding-top on <html>, so scrollIntoView
     inherits both and the target clears the bar without a second offset to
     keep in sync here. Reduced motion is honoured by the CSS that turns
     scroll-behavior back to auto, not by a branch in this function. */

  function initScrollCue() {
    qsa('[data-scroll-to]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var target = qs(btn.getAttribute('data-scroll-to'));
        if (target) target.scrollIntoView({ block: 'start' });
      });
    });
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
  /* The tile image. A commodity we have a real photograph of paints it edge to
     edge; everything else keeps the line-art placeholder floating on the sand
     tile. Mirrors art_tag() in build_catalogue.py — the static cards and these
     JS-rendered rails have to agree or the grid reads as two grids. */
  function artTag(p) {
    if (!p.photo) {
      return '<img class="card__art" src="assets/img/products/' + p.art +
             '.svg" alt="" loading="lazy" width="400" height="500">';
    }
    var base = 'assets/img/products/photo/' + p.art;
    return '<picture>' +
      '<source type="image/webp" srcset="' + base + '.webp">' +
      '<img class="card__art card__art--photo" src="' + base +
      '.jpg" alt="" loading="lazy" width="400" height="420">' +
      '</picture>';
  }

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
      artTag(p) +
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
     key, put it in FORM_KEY — it is a public submission key, not a secret.

     ATTACHMENTS. The enquiry desk on the contact page offers a file upload —
     a company profile from a buyer, a quality passport from a supplier. A
     static page cannot deliver a file on its own, and a mailto: link cannot
     attach one, so until FORM_ENDPOINT is set the form carries the filename
     into the email body with an instruction to attach it by hand. That is the
     honest degradation, not the intended behaviour.

     Once an endpoint is set the file is posted for real: submissions carrying
     a file are sent as multipart/form-data instead of JSON (see the submit
     handler below), which is what both Web3Forms and Formspree expect. Check
     that the plan you sign up for actually accepts attachments — on both
     services file upload is a paid feature, and a free endpoint will take the
     text fields and silently drop the file. */

  var FORM_ENDPOINT = '';
  var FORM_KEY = '';

  function initForms() {
    qsa('form[data-mailto]').forEach(function (form) {
      var statusEl = qs('.form__status', form);
      var submitBtn = qs('button[type="submit"]', form);
      var submitKey = submitBtn && submitBtn.getAttribute('data-i18n');

      function labelFor(name) {
        var field = form.elements[name];
        /* The enquiry desk gives the same name to a field on more than one
           route ("Commodity", "Attachment"), so elements[name] hands back a
           RadioNodeList. Only one route is ever enabled — label from that. */
        if (field && !field.tagName && typeof field.length === 'number') {
          for (var i = 0; i < field.length; i++) {
            if (!field[i].disabled) { field = field[i]; break; }
          }
        }
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

      function fallbackToMail(payload, attachment) {
        var lines = Object.keys(payload).map(function (k) { return k + ': ' + payload[k]; });

        /* A mailto: URL cannot attach a file — no browser permits it, for good
           reason. Say so in the body the visitor is about to send, rather than
           letting them believe the document went with it. */
        if (attachment) {
          lines.push('');
          lines.push('--- ' + (window.ACI18N && window.ACI18N.current() === 'ru'
            ? 'ВЛОЖЕНИЕ: прикрепите к этому письму файл ' + attachment.file.name
            : 'ATTACHMENT: please attach ' + attachment.file.name + ' to this email') + ' ---');
        }

        window.location.href = 'mailto:' + form.getAttribute('data-mailto') +
          '?subject=' + encodeURIComponent(form.getAttribute('data-subject') || 'Enquiry') +
          '&body=' + encodeURIComponent(lines.join('\n'));

        say(attachment ? 'form.statusFile' : 'form.status',
            attachment
              ? 'Your enquiry has been prepared in your mail client. Attach ' +
                attachment.file.name + ' before sending it.'
              : 'Your enquiry has been prepared in your mail client. Send it to reach the trading desk.');
      }

      form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (typeof form.reportValidity === 'function' && !form.reportValidity()) return;

        var payload = {};
        var attachment = null;

        new FormData(form).forEach(function (value, key) {
          /* A File stringifies to "[object File]", which is how an attachment
             silently becomes nothing. Carry the file itself for the POST and
             its name for the human-readable copy. */
          if (typeof File !== 'undefined' && value instanceof File) {
            if (value.size) {
              attachment = { field: key, file: value };
              payload[labelFor(key)] = value.name + ' (' + fmtSize(value.size) + ')';
            }
            return;
          }
          if (String(value).trim() !== '') payload[labelFor(key)] = value;
        });
        payload.subject = form.getAttribute('data-subject') || 'Enquiry';

        if (!FORM_ENDPOINT) { fallbackToMail(payload, attachment); return; }

        if (FORM_KEY) payload.access_key = FORM_KEY;
        busy(true);

        /* With a file the request has to be multipart — a JSON body cannot
           carry one. Both Web3Forms and Formspree accept either shape, so the
           endpoint does not change, only the encoding. */
        var request = attachment
          ? { body: (function () {
                var fd = new FormData();
                Object.keys(payload).forEach(function (k) { fd.append(k, payload[k]); });
                fd.append(attachment.field, attachment.file, attachment.file.name);
                return fd;
              })(),
              headers: { 'Accept': 'application/json' } }
          : { body: JSON.stringify(payload),
              headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' } };

        fetch(FORM_ENDPOINT, {
          method: 'POST',
          headers: request.headers,
          body: request.body
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

  /* ------------------------------------------------------- ENQUIRY DESK -- */
  /* One form, three routes: a buyer asking for a quotation, a producer
     offering a cargo, and everyone else.

     Routes are switched by DISABLING the fields of the routes you are not on,
     not merely by hiding them. Two reasons, both load-bearing:

       · a required field inside [hidden] still fails constraint validation, so
         reportValidity() would refuse to submit and point at something the
         visitor cannot see or fix;
       · a disabled field is dropped from FormData, so the desk never receives
         a supplier's country of origin appended to a buyer's RFQ.

     The commodity list is read from window.PRODUCTS rather than written out
     here, so it cannot drift from the catalogue and it follows the language
     toggle for free. */

  function initEnquiry() {
    var form = qs('#enqForm');
    if (!form) return;

    var tabs = qsa('.enq__tab');
    var panels = qsa('[data-enq-panel]', form);

    var SUBJECTS = {
      buy: 'Request for Quotation',
      sell: 'Cargo Offer — Supplier',
      general: 'General Enquiry'
    };

    /* ------------------------------------------------------------ routing */

    function select(route, moveFocus) {
      if (!SUBJECTS[route]) route = 'buy';

      tabs.forEach(function (tab) {
        var on = tab.getAttribute('data-enq-tab') === route;
        tab.classList.toggle('is-active', on);
        tab.setAttribute('aria-selected', on ? 'true' : 'false');
        tab.tabIndex = on ? 0 : -1;
        if (on && moveFocus) tab.focus();
      });

      panels.forEach(function (panel) {
        var on = panel.getAttribute('data-enq-panel') === route;
        panel.hidden = !on;
        qsa('input, select, textarea', panel).forEach(function (el) {
          el.disabled = !on;
        });
      });

      form.setAttribute('data-subject', SUBJECTS[route]);
    }

    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        select(tab.getAttribute('data-enq-tab'));
      });
    });

    /* Left/right walks the group, as a tablist is expected to. */
    var order = tabs.map(function (t) { return t.getAttribute('data-enq-tab'); });
    qs('.enq__tabs').addEventListener('keydown', function (e) {
      var step = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (!step) return;
      e.preventDefault();
      var at = order.indexOf(qs('.enq__tab.is-active').getAttribute('data-enq-tab'));
      select(order[(at + step + order.length) % order.length], true);
    });

    /* The two cards in the sourcing block above open the matching route. */
    qsa('[data-enq-go]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        select(btn.getAttribute('data-enq-go'));
        qs('#enq').scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });

    /* --------------------------------------------------- commodity lists */

    function fillCommodities() {
      if (!window.PRODUCTS || !window.PRODUCT_ORDER) return;
      var ru = window.ACI18N && window.ACI18N.current() === 'ru';

      qsa('[data-commodity]', form).forEach(function (sel) {
        var chosen = sel.value;
        /* Keep the placeholder and the "Other" escape hatch; everything
           between them is the catalogue and is rebuilt on every language
           change. */
        qsa('option[data-from-catalogue]', sel).forEach(function (o) { o.remove(); });
        var other = qs('option[value="Other / Custom Commodity"]', sel);

        window.PRODUCT_ORDER.forEach(function (slug) {
          var p = window.PRODUCTS[slug];
          if (!p) return;
          var L = (ru && p.ru) ? p.ru : p.en;
          var opt = document.createElement('option');
          /* The value stays English — the trading desk reads the enquiry, and
             an RFQ that names the commodity in the visitor's language is one
             more thing to translate before it can be quoted. */
          opt.value = p.en.name + ' — ' + p.en.grade;
          opt.textContent = L.name + ' — ' + L.grade;
          opt.setAttribute('data-from-catalogue', '');
          sel.insertBefore(opt, other);
        });

        if (chosen) sel.value = chosen;
      });
    }

    fillCommodities();
    document.addEventListener('ac:lang', fillCommodities);

    /* "Other" reveals a free-text field, and only then is it required. */
    qsa('[data-commodity]', form).forEach(function (sel) {
      var extra = qs('[data-commodity-other]', sel.closest('.field-row') || form);
      if (!extra) return;
      var input = qs('input', extra);

      sel.addEventListener('change', function () {
        var other = sel.value === 'Other / Custom Commodity';
        extra.hidden = !other;
        input.required = other;
        /* select() owns the disabled flag for the whole panel, so this only
           steps in while the panel is live. */
        if (other && !sel.disabled) input.focus();
        if (!other) input.value = '';
      });
    });

    /* Deep link, so a supplier-facing link can open on the supplier's route:
       contact.html?enq=sell, or #sell. Defaults to the buyer. */
    var asked = (/[?&]enq=(buy|sell|general)\b/.exec(location.search) ||
                 /^#(buy|sell|general)$/.exec(location.hash) || [])[1];
    select(asked || 'buy');
  }

  /* ---------------------------------------------------------- FILE FIELD -- */
  /* The native control cannot be styled and announces the filename in a
     system font. The input keeps doing the work; the label is what you see.
     Type and size are checked here so the visitor is told before they submit
     rather than by a rejected POST. */

  var FILE_MAX = 10 * 1024 * 1024;

  function fmtSize(bytes) {
    return bytes >= 1048576
      ? (bytes / 1048576).toFixed(1) + ' MB'
      : Math.max(1, Math.round(bytes / 1024)) + ' kB';
  }

  function initFileFields() {
    qsa('[data-filefield]').forEach(function (wrap) {
      var input = qs('input[type="file"]', wrap);
      var name = qs('[data-filename]', wrap);
      if (!input || !name) return;

      input.addEventListener('change', function () {
        var file = input.files && input.files[0];
        wrap.classList.remove('has-file', 'is-invalid');
        input.setCustomValidity('');

        if (!file) { name.textContent = ''; return; }

        if (file.size > FILE_MAX) {
          wrap.classList.add('is-invalid');
          name.textContent = file.name + ' — ' + fmtSize(file.size);
          input.setCustomValidity(
            window.ACI18N && window.ACI18N.current() === 'ru'
              ? 'Файл больше 10 МБ. Пришлите его письмом на trading@arminakcaravan.ae.'
              : 'That file is over 10 MB. Email it to trading@arminakcaravan.ae instead.');
          input.reportValidity();
          return;
        }

        wrap.classList.add('has-file');
        name.textContent = file.name + ' · ' + fmtSize(file.size);
      });
    });
  }

  /* ----------------------------------------------------------------- GO --- */

  function boot() {
    initTheme();
    initDeskClock();
    initNav();
    initReveal();
    initScrollCue();
    initTabs();
    initFavs();
    initRails();
    initShop();
    initAccordions();
    initDrawer();
    initForms();
    initEnquiry();
    initFileFields();
    initHero();
    initNavPanel();
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
