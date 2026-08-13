/* ============================================================================
   ARMINAK CARAVAN — real sand, v2
   ----------------------------------------------------------------------------
   The client asked for "настоящая анимация песка". v1 rendered domain-warped
   fBm — it shimmered but nothing *travelled*, so it read as marbled smoke.
   Real wind-blown sand is two regimes, and this renders one layer per regime:

     SUSPENSION (veil layer, behind the caravan)
       A baked tileable noise texture advected along a wind field using
       flow-map cross-fading (two phase-offset samples, triangle-blended, so
       the texture genuinely travels without smearing to infinity). Three
       parallax sub-layers — fine spray leads, coarse puffs lag. Density is
       shaped by the dune lines themselves: it falls off exponentially with
       height above the sand surface and boosts at crests ("smoking dunes").
       A low-frequency gust wave travels with the wind, so fronts visibly
       sweep across the screen instead of throbbing in place.

     SALTATION (streak layer, in front of the caravan)
       A few hundred grain streaks hugging the near dune line — quads
       elongated along their velocity (motion stretch is what makes a grain
       read as wind-borne rather than snow), pulsing with the same gust wave,
       occasionally hopping in small ballistic arcs.

   All WebGL1, no dependency. Returns null when WebGL is missing so callers
   can fall back (canvas-2D dust in the hero, SVG grain tile at the edges).
   Skipped entirely under prefers-reduced-motion by the callers.
   ============================================================================ */
(function () {
  'use strict';

  /* ------------------------------------------------------------ noise bake */
  /* One 256² tileable RGBA texture shared by every instance:
       R — low frequency (wind field / gusts)
       G — mid frequency (veil body)
       B — high frequency (grain sparkle)
       A — mid frequency, different phase (cross-fade partner)
     Baked once in JS (~40ms) instead of computing 22 procedural noise taps
     per pixel per frame like v1 — the per-frame shader is ~12 mip-filtered
     texture fetches, cheaper AND better behaved. */

  var NSIZE = 256;
  var NOISE = null;

  function h2(i, j, seed) {
    var n = (Math.imul(i, 374761393) + Math.imul(j, 668265263) +
             Math.imul(seed, 1442695041)) | 0;
    n = Math.imul(n ^ (n >>> 13), 1274126177);
    n = n ^ (n >>> 16);
    return (n >>> 0) / 4294967296;
  }

  /* Tileable value noise: the lattice wraps at `f`, so the texture repeats. */
  function vnoise(u, v, f, seed) {
    var x = u * f, y = v * f;
    var xi = Math.floor(x), yi = Math.floor(y);
    var xf = x - xi, yf = y - yi;
    var sx = xf * xf * (3 - 2 * xf), sy = yf * yf * (3 - 2 * yf);
    var x0 = ((xi % f) + f) % f, x1 = (x0 + 1) % f;
    var y0 = ((yi % f) + f) % f, y1 = (y0 + 1) % f;
    var a = h2(x0, y0, seed), b = h2(x1, y0, seed);
    var c = h2(x0, y1, seed), d = h2(x1, y1, seed);
    return a + (b - a) * sx + (c - a) * sy + (a - b - c + d) * sx * sy;
  }

  function fbm(u, v, f0, oct, seed) {
    var val = 0, amp = 0.5, f = f0, norm = 0;
    for (var o = 0; o < oct; o++) {
      val += amp * vnoise(u, v, f, seed + o * 17);
      norm += amp; f *= 2; amp *= 0.5;
    }
    return val / norm;
  }

  function getNoise() {
    if (NOISE) return NOISE;
    var d = new Uint8Array(NSIZE * NSIZE * 4);
    for (var y = 0; y < NSIZE; y++) {
      var v = y / NSIZE;
      for (var x = 0; x < NSIZE; x++) {
        var u = x / NSIZE, i = (y * NSIZE + x) * 4;
        d[i]     = 255 * fbm(u, v, 4, 3, 1);
        d[i + 1] = 255 * fbm(u, v, 8, 4, 7);
        d[i + 2] = 255 * fbm(u, v, 18, 4, 13);
        d[i + 3] = 255 * fbm(u, v, 8, 4, 29);
      }
    }
    NOISE = d;
    return d;
  }

  /* JS-side sampler of the G channel, wrapping + bilinear — the streak sim
     reads the SAME gust wave the veil shader does, so both layers surge
     together. One wind, two regimes. */
  function sampleG(u, v) {
    u = u - Math.floor(u); v = v - Math.floor(v);
    var x = u * NSIZE, y = v * NSIZE;
    var xi = Math.floor(x) % NSIZE, yi = Math.floor(y) % NSIZE;
    var xf = x - Math.floor(x), yf = y - Math.floor(y);
    var x1 = (xi + 1) % NSIZE, y1 = (yi + 1) % NSIZE;
    var n = NOISE;
    var a = n[(yi * NSIZE + xi) * 4 + 1], b = n[(yi * NSIZE + x1) * 4 + 1];
    var c = n[(y1 * NSIZE + xi) * 4 + 1], d = n[(y1 * NSIZE + x1) * 4 + 1];
    return (a + (b - a) * xf + (c - a) * yf + (a - b - c + d) * xf * yf) / 255;
  }

  function smoothstepJS(a, b, x) {
    var t = Math.min(1, Math.max(0, (x - a) / (b - a)));
    return t * t * (3 - 2 * t);
  }

  /* Gust wave: low-frequency noise of (x − c·t) — a front that travels. */
  function gustAt(xNorm, t, seed) {
    var g = sampleG(xNorm * 0.16 - t * 0.035 + seed, 0.31);
    return 0.35 + 1.15 * smoothstepJS(0.30, 0.78, g);
  }

  /* --------------------------------------------------------------- ground */
  /* The dune curves already exist as SVG paths; sample their top edge (the
     part before the closing `L…` runs down to the corners) in viewBox space
     once, then re-map through the xMidYMax-slice transform on every resize.
     The browser does the Bézier math via getPointAtLength. */

  var SVGNS = 'http://www.w3.org/2000/svg';

  function sampleCurve(pathEl, n) {
    if (!pathEl) return null;
    try {
      var d = (pathEl.getAttribute('d') || '').split(/\sL\s?/)[0];
      var tmp = document.createElementNS(SVGNS, 'path');
      tmp.setAttribute('d', d);
      tmp.setAttribute('fill', 'none');
      var svg = pathEl.ownerSVGElement;
      svg.appendChild(tmp);                    /* attached ⇒ geometry is safe */
      var L = tmp.getTotalLength();
      var pts = [];
      for (var i = 0; i <= n; i++) pts.push(tmp.getPointAtLength(L * i / n));
      svg.removeChild(tmp);
      return pts.length > 2 ? pts : null;
    } catch (e) { return null; }
  }

  /* pts (viewBox coords) → heights[cols] of viewBox y, indexed along x. */
  function toHeights(pts, vbW, cols) {
    if (!pts) return null;
    var h = new Float32Array(cols);
    var idx = 0;
    for (var c = 0; c < cols; c++) {
      var x = (c + 0.5) / cols * vbW;
      while (idx < pts.length - 2 && pts[idx + 1].x < x) idx++;
      var p0 = pts[idx], p1 = pts[idx + 1];
      var f = p1.x > p0.x ? (x - p0.x) / (p1.x - p0.x) : 0;
      h[c] = p0.y + (p1.y - p0.y) * Math.min(1, Math.max(0, f));
    }
    return h;
  }

  /* Crest factor: local minima of y (viewBox y grows downward), blurred. */
  function crestsOf(hs, cols) {
    var c = new Float32Array(cols), m = 0, i;
    if (!hs) return c;
    for (i = 2; i < cols - 2; i++) {
      var curv = hs[i - 2] + hs[i + 2] - 2 * hs[i];
      c[i] = Math.max(0, curv);
      if (c[i] > m) m = c[i];
    }
    for (var pass = 0; pass < 3; pass++)
      for (i = 1; i < cols - 1; i++) c[i] = (c[i - 1] + c[i] * 2 + c[i + 1]) / 4;
    if (m > 0) for (i = 0; i < cols; i++) c[i] = Math.min(1, c[i] / m * 1.4);
    return c;
  }

  /* xMidYMax slice: how the 1600×900 viewBox maps onto a w×h box. */
  function sliceMap(w, h, vbW, vbH) {
    var s = Math.max(w / vbW, h / vbH);
    return { s: s, ox: (w - vbW * s) / 2, oy: h - vbH * s };
  }

  /* -------------------------------------------------------------- shaders */

  var VERT_FS = [
    'attribute vec2 a;',
    'void main(){ gl_Position = vec4(a, 0.0, 1.0); }'
  ].join('\n');

  var FRAG_VEIL = [
    'precision highp float;',
    'uniform vec2  uRes;',
    'uniform float uTime;',
    'uniform float uIntensity;',
    'uniform float uWind;',
    'uniform float uSeed;',
    'uniform float uHasGround;',
    'uniform vec3  uColThin;',
    'uniform vec3  uColDense;',
    'uniform sampler2D uNoise;',
    'uniform sampler2D uGround;',

    'void main(){',
    '  vec2 uv = gl_FragCoord.xy / uRes;',          /* y up */
    '  float t = uTime;',
    '  vec2 suv = vec2(uv.x * (uRes.x / uRes.y), uv.y);',

    /* Traveling gust front — density fronts sweep with the wind. */
    '  float grr = texture2D(uNoise, vec2(uv.x * 0.16 - t * 0.035 + uSeed, 0.31)).g;',
    '  float gust = 0.35 + 1.15 * smoothstep(0.30, 0.78, grr);',

    /* Wind: base flow + curl of the low-frequency channel, so the stream
       curls over the terrain instead of running flat. Curl of a potential
       is divergence-free — it swirls without piling up. */
    '  vec2 cuv = suv * 0.35 + vec2(t * 0.010, 0.0) + uSeed;',
    '  float e  = 0.012;',
    '  float n0 = texture2D(uNoise, cuv).r;',
    '  float nx = texture2D(uNoise, cuv + vec2(e, 0.0)).r;',
    '  float ny = texture2D(uNoise, cuv + vec2(0.0, e)).r;',
    '  vec2 vel = vec2(uWind, 0.0) + vec2(ny - n0, -(nx - n0)) * (0.020 / e);',
    '  vel   *= (0.55 + 0.65 * gust);',             /* gusts race, lulls crawl */
    '  vel.y += (gust - 0.85) * 0.012;',            /* gusts loft sand upward */

    /* Three advected layers with flow-map cross-fade: two phase-offset
       samples of the SAME field, each re-anchored every cycle before it can
       smear, blended so the reset is invisible. Per-layer speed grows faster
       than scale ⇒ fine spray visibly leads the coarse puffs (dispersion). */
    '  float T   = 3.0;',
    '  float ph0 = fract(t / T);',
    '  float ph1 = fract(t / T + 0.5);',
    '  float w   = abs(ph0 * 2.0 - 1.0);',
    '  vec2 stretch = vec2(0.60, 2.9);',            /* streaks along the wind */
    '  float f = 0.0, amp = 0.5, scl = 1.0, spd = 0.55;',
    '  for (int i = 0; i < 3; i++){',
    '    vec2 base = suv * stretch * scl + vec2(uSeed * 1.7, uSeed * 0.31);',
    '    float s0 = texture2D(uNoise, base - vel * (ph0 * T) * spd).g;',
    '    float s1 = texture2D(uNoise, base - vel * (ph1 * T) * spd + vec2(0.37, 0.11)).a;',
    '    f += amp * mix(s0, s1, w);',
    '    scl *= 2.02; spd *= 2.6; amp *= 0.55;',
    '  }',
    '  float veil = smoothstep(0.42, 0.85, f);',    /* crests only — clear air between */

    /* Grain sparkle inside the veils, advected fast and straight. */
    '  vec2 gp = suv * vec2(3.4, 9.5) - vel * t * 2.6;',
    '  float grains = smoothstep(0.60, 0.94, texture2D(uNoise, gp).b) * veil;',

    /* Ground shaping: sand belongs to the dunes, not the sky. Density decays
       with height above the near and mid dune lines and boosts at crests. */
    '  float band = 1.0;',
    '  if (uHasGround > 0.5){',
    '    vec3 g = texture2D(uGround, vec2(uv.x, 0.5)).rgb;',
    '    float hN = uv.y - g.r;',
    '    float hM = uv.y - g.g;',
    '    band = exp(-max(hN, 0.0) * 6.5) * smoothstep(-0.16, -0.02, hN)',
    '         + 0.55 * exp(-max(hM, 0.0) * 9.0) * smoothstep(-0.10, -0.01, hM);',
    '    band += g.b * 1.5 * exp(-abs(hM) * 13.0) * gust;',   /* smoking crests */
    '    band = min(band, 1.35);',
    '  }',

    '  float d = (veil * 0.85 + grains * 0.90) * band * gust * uIntensity;',
    /* Thin sand is pale gold, dense sand is deep ochre — a translucency ramp
       instead of one flat tint. */
    '  vec3 col = mix(uColThin, uColDense, clamp(d * 0.9, 0.0, 1.0));',
    '  float a = clamp(d, 0.0, 1.0);',
    '  a += (fract(sin(dot(gl_FragCoord.xy, vec2(12.9898, 78.233))) * 43758.5453) - 0.5) * 0.012;',
    '  gl_FragColor = vec4(col, clamp(a, 0.0, 1.0));',
    '}'
  ].join('\n');

  var VERT_STREAK = [
    'attribute vec2 aPos;',
    'attribute vec3 aAux;',                          /* along, across, alpha */
    'uniform vec2 uRes;',
    'varying vec3 vAux;',
    'void main(){',
    '  vAux = aAux;',
    '  vec2 c = aPos / uRes * 2.0 - 1.0;',
    '  gl_Position = vec4(c.x, c.y, 0.0, 1.0);',
    '}'
  ].join('\n');

  var FRAG_STREAK = [
    'precision mediump float;',
    'uniform vec3 uCol;',
    'varying vec3 vAux;',
    'void main(){',
    /* Soft across the width, tapering along the tail — a motion-stretched
       grain, not a dot. */
    '  float across = 1.0 - abs(vAux.y);',
    '  float a = vAux.z * across * across * (1.0 - vAux.x * 0.85);',
    '  gl_FragColor = vec4(uCol, a);',
    '}'
  ].join('\n');

  /* ------------------------------------------------------------- GL utils */

  function compile(gl, type, src) {
    var s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) { gl.deleteShader(s); return null; }
    return s;
  }

  function makeProgram(gl, vsrc, fsrc) {
    var vs = compile(gl, gl.VERTEX_SHADER, vsrc);
    var fs = compile(gl, gl.FRAGMENT_SHADER, fsrc);
    if (!vs || !fs) return null;
    var p = gl.createProgram();
    gl.attachShader(p, vs); gl.attachShader(p, fs); gl.linkProgram(p);
    return gl.getProgramParameter(p, gl.LINK_STATUS) ? p : null;
  }

  function hexToRgb(hex) {
    hex = (hex || '#B08D57').trim().replace('#', '');
    if (hex.length === 3) hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
    var n = parseInt(hex, 16);
    return [((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255];
  }

  function mixRgb(a, b, t) {
    return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];
  }

  var IVORY = hexToRgb('#F8F1E2');
  var OCHRE = hexToRgb('#7C5B2E');
  var AMBER = hexToRgb('#8F6B33');

  /* ============================================================ controller */
  /* window.ACSand(canvas, host, opts) → {start, stop, resize, setColor,
     isRunning} or null when WebGL is unavailable.
       opts.mode    'veil' (default) | 'streaks'
       opts.ground  {near: <path el>, mid: <path el>, viewBox: [w, h]}
       opts.base / opts.open / opts.openMs   settled + entry intensity
       opts.fps     frame cap (default 30)
       opts.scale   render-scale multiplier (veil only)
       opts.wind    base wind speed (veil only)
       opts.seed    pattern offset */

  window.ACSand = function (canvas, host, opts) {
    opts = opts || {};
    var MODE   = opts.mode || 'veil';
    var BASE   = opts.base != null ? opts.base : 1.0;
    var OPEN   = opts.open != null ? opts.open : 1.45;
    var OPEN_S = opts.openMs != null ? opts.openMs / 1000 : 3.4;
    var FPS    = opts.fps != null ? opts.fps : 30;
    var MIN_DT = 1000 / FPS;
    var SEED   = opts.seed != null ? opts.seed : 3.7;

    var gl = null;
    try {
      var attrs = { alpha: true, premultipliedAlpha: false, antialias: false,
                    depth: false, stencil: false };
      gl = canvas.getContext('webgl', attrs) || canvas.getContext('experimental-webgl', attrs);
    } catch (e) { return null; }
    if (!gl) return null;

    var prog = makeProgram(gl, MODE === 'streaks' ? VERT_STREAK : VERT_FS,
                               MODE === 'streaks' ? FRAG_STREAK : FRAG_VEIL);
    if (!prog) return null;
    gl.useProgram(prog);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

    /* ---- ground data (used by both modes) ---- */
    var vb = (opts.ground && opts.ground.viewBox) || [1600, 900];
    var COLS = 192;
    var nearVB = opts.ground ? toHeights(sampleCurve(opts.ground.near, 220), vb[0], COLS) : null;
    var midVB  = opts.ground ? toHeights(sampleCurve(opts.ground.mid, 220), vb[0], COLS) : null;
    var crestVB = crestsOf(midVB, COLS);
    var hasGround = !!(nearVB && midVB);

    var cssW = 1, cssH = 1, renderScale = 1;
    var groundPx = null;                   /* near-dune y in css px, for streaks */

    /* ---- mode-specific GL state ---- */
    var uRes, uTime, uInt, uWindU, uSeedU, uHasG, uThin, uDense, uCol;
    var groundTex = null;

    if (MODE === 'veil') {
      var buf = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, buf);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
      var loc = gl.getAttribLocation(prog, 'a');
      gl.enableVertexAttribArray(loc);
      gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);

      /* noise texture — unit 0 */
      var ntex = gl.createTexture();
      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, ntex);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, NSIZE, NSIZE, 0, gl.RGBA, gl.UNSIGNED_BYTE, getNoise());
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.REPEAT);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.REPEAT);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_NEAREST);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.generateMipmap(gl.TEXTURE_2D);

      /* ground texture — unit 1, rebuilt on resize */
      groundTex = gl.createTexture();
      gl.activeTexture(gl.TEXTURE1);
      gl.bindTexture(gl.TEXTURE_2D, groundTex);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);

      uRes   = gl.getUniformLocation(prog, 'uRes');
      uTime  = gl.getUniformLocation(prog, 'uTime');
      uInt   = gl.getUniformLocation(prog, 'uIntensity');
      uWindU = gl.getUniformLocation(prog, 'uWind');
      uSeedU = gl.getUniformLocation(prog, 'uSeed');
      uHasG  = gl.getUniformLocation(prog, 'uHasGround');
      uThin  = gl.getUniformLocation(prog, 'uColThin');
      uDense = gl.getUniformLocation(prog, 'uColDense');
      gl.uniform1i(gl.getUniformLocation(prog, 'uNoise'), 0);
      gl.uniform1i(gl.getUniformLocation(prog, 'uGround'), 1);
      gl.uniform1f(uSeedU, SEED);
      gl.uniform1f(uWindU, opts.wind != null ? opts.wind : 0.13);
      gl.uniform1f(uHasG, hasGround ? 1 : 0);
    } else {
      getNoise();                            /* the sim samples it in JS */
      uRes = gl.getUniformLocation(prog, 'uRes');
      uCol = gl.getUniformLocation(prog, 'uCol');
      var aPos = gl.getAttribLocation(prog, 'aPos');
      var aAux = gl.getAttribLocation(prog, 'aAux');
      var vbuf = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, vbuf);
      gl.enableVertexAttribArray(aPos);
      gl.enableVertexAttribArray(aAux);
      gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 20, 0);
      gl.vertexAttribPointer(aAux, 3, gl.FLOAT, false, 20, 8);
    }

    /* ---- streak simulation ---- */
    var streaks = [];
    var verts = null;

    function groundYAt(x) {                  /* css px → css px */
      if (!groundPx) return cssH * 0.86;
      var f = Math.min(COLS - 1.001, Math.max(0, x / cssW * COLS));
      var i = Math.floor(f), fr = f - i;
      return groundPx[i] + (groundPx[Math.min(COLS - 1, i + 1)] - groundPx[i]) * fr;
    }

    function spawnStreak(anywhere) {
      var lifted = Math.random() < 0.18;     /* a few ride higher in the air */
      return {
        x: anywhere ? Math.random() * cssW : -20 - Math.random() * 120,
        lift: lifted ? 8 + Math.random() * 26 : 1 + Math.random() * 5,
        y: 0, vy: 0, vx: 0,
        jit: 0.7 + Math.random() * 0.6,
        w: 1.3 + Math.random() * 1.5,
        a0: 0.34 + Math.random() * 0.44,
        placed: false
      };
    }

    function seedStreaks() {
      var target = Math.round(Math.min(240, Math.max(60, cssW / 7)));
      streaks = [];
      for (var i = 0; i < target; i++) streaks.push(spawnStreak(true));
      verts = new Float32Array(target * 6 * 5);
    }

    function simStreaks(dt, t, intensity) {
      var vi = 0;
      var G = 480;                           /* gravity, px/s² */
      for (var i = 0; i < streaks.length; i++) {
        var s = streaks[i];
        var gust = gustAt(s.x / cssW, t, SEED);
        var gn = (gust - 0.35) / 1.15;       /* 0..1 */

        /* Saltation: speed surges quadratically with the gust — pulses of
           fast travel between near-stalls, not a constant conveyor. */
        var vTarget = cssW * (0.030 + 0.30 * gn * gn) * s.jit;
        s.vx += (vTarget - s.vx) * Math.min(1, dt * 3.0);

        var gy = groundYAt(s.x) - s.lift;
        if (!s.placed) { s.y = gy + (Math.random() * 8 - 4); s.placed = true; }

        if (s.vy !== 0) {                    /* mid-hop: ballistic arc */
          s.vy += G * dt;
          s.y += s.vy * dt;
          if (s.y >= gy) { s.y = gy; s.vy = 0; }
        } else {
          s.y += (gy - s.y) * Math.min(1, dt * 4.0);
          s.y += Math.sin(t * 2.1 + s.x * 0.02) * 6 * dt;
          if (gn > 0.62 && Math.random() < dt * 1.1)   /* gusts kick grains up */
            s.vy = -(40 + Math.random() * 90);
        }

        s.x += s.vx * dt;
        if (s.x > cssW + 40) { streaks[i] = spawnStreak(false); continue; }

        /* Motion stretch: the tail is where the grain just was. */
        var tail = Math.min(64, Math.max(5, s.vx * 0.075));
        var alpha = Math.min(0.9, s.a0 * (0.35 + 0.85 * gn) * intensity);
        if (alpha < 0.02) continue;

        var x0 = s.x * renderScale,          y0 = (cssH - s.y) * renderScale;
        var x1 = (s.x - tail) * renderScale, y1 = (cssH - (s.y - s.vy * 0.05)) * renderScale;
        var hw = Math.max(0.5, s.w * renderScale * 0.5);

        /* Two triangles: head (along=0) → tail (along=1), across −1…1. */
        verts[vi++] = x0; verts[vi++] = y0 - hw; verts[vi++] = 0; verts[vi++] = -1; verts[vi++] = alpha;
        verts[vi++] = x0; verts[vi++] = y0 + hw; verts[vi++] = 0; verts[vi++] = 1;  verts[vi++] = alpha;
        verts[vi++] = x1; verts[vi++] = y1 + hw; verts[vi++] = 1; verts[vi++] = 1;  verts[vi++] = alpha;
        verts[vi++] = x0; verts[vi++] = y0 - hw; verts[vi++] = 0; verts[vi++] = -1; verts[vi++] = alpha;
        verts[vi++] = x1; verts[vi++] = y1 + hw; verts[vi++] = 1; verts[vi++] = 1;  verts[vi++] = alpha;
        verts[vi++] = x1; verts[vi++] = y1 - hw; verts[vi++] = 1; verts[vi++] = -1; verts[vi++] = alpha;
      }
      return vi;
    }

    /* ---- shared plumbing ---- */

    /* Adaptive quality: most devices render this for free, but a machine with
       no GPU (software GL) or a very old phone can't. Instead of degrading
       everyone, measure the real frame interval and step down — resolution
       first, then frame rate — only when the budget is actually blown. */
    var qMult = 1, degradeStep = 0, lastAdapt = 0, emaMs = 0;

    function scaleFor() {
      var dpr = window.devicePixelRatio || 1;
      if (MODE === 'streaks') return Math.min(dpr, 2);   /* thin quads need dpr */
      var q = opts.scale != null ? opts.scale : 1;
      return Math.min(dpr, window.innerWidth < 768 ? 0.8 : 1.0) * q * qMult;
    }

    function adapt(now, renderedMs) {
      if (MODE !== 'veil' || degradeStep >= 3) return;
      emaMs = emaMs ? emaMs * 0.88 + renderedMs * 0.12 : renderedMs;
      if (!lastAdapt) { lastAdapt = now; return; }
      if (now - lastAdapt < 2200 || emaMs < MIN_DT * 1.55) return;
      degradeStep++; lastAdapt = now; emaMs = 0;
      if (degradeStep === 2) { MIN_DT = 1000 / 18; }
      else { qMult *= 0.68; resize(); }
    }

    function rebuildGroundTex() {
      if (!hasGround) return;
      var m = sliceMap(cssW, cssH, vb[0], vb[1]);
      var px = new Uint8Array(COLS * 4);
      for (var i = 0; i < COLS; i++) {
        var xCss = (i + 0.5) / COLS * cssW;
        var xVB = Math.min(COLS - 1, Math.max(0, Math.round((xCss - m.ox) / m.s / vb[0] * COLS)));
        var yN = 1 - (m.oy + nearVB[xVB] * m.s) / cssH;  /* uv, y up */
        var yM = 1 - (m.oy + midVB[xVB] * m.s) / cssH;
        px[i * 4]     = 255 * Math.min(1, Math.max(0, yN));
        px[i * 4 + 1] = 255 * Math.min(1, Math.max(0, yM));
        px[i * 4 + 2] = 255 * crestVB[xVB];
        px[i * 4 + 3] = 255;
      }
      gl.activeTexture(gl.TEXTURE1);
      gl.bindTexture(gl.TEXTURE_2D, groundTex);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, COLS, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, px);
    }

    function rebuildGroundPx() {
      if (!nearVB) { groundPx = null; return; }
      var m = sliceMap(cssW, cssH, vb[0], vb[1]);
      groundPx = new Float32Array(COLS);
      for (var i = 0; i < COLS; i++) {
        var xCss = (i + 0.5) / COLS * cssW;
        var xVB = Math.min(COLS - 1, Math.max(0, Math.round((xCss - m.ox) / m.s / vb[0] * COLS)));
        groundPx[i] = m.oy + nearVB[xVB] * m.s;
      }
    }

    function resize() {
      var r = host.getBoundingClientRect();
      cssW = Math.max(1, Math.round(r.width));
      cssH = Math.max(1, Math.round(r.height));
      renderScale = scaleFor();
      var w = Math.max(1, Math.round(cssW * renderScale));
      var h = Math.max(1, Math.round(cssH * renderScale));
      if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
      canvas.style.width = cssW + 'px';
      canvas.style.height = cssH + 'px';
      gl.viewport(0, 0, w, h);
      gl.useProgram(prog);
      gl.uniform2f(uRes, w, h);
      if (MODE === 'veil') rebuildGroundTex();
      else { rebuildGroundPx(); seedStreaks(); }
    }

    /* Thin sand pale, dense sand deep — both derived from the theme accent. */
    function setColor(hex) {
      var c = hexToRgb(hex);
      gl.useProgram(prog);
      if (MODE === 'veil') {
        var thin = mixRgb(c, IVORY, 0.52);
        var dense = mixRgb(c, AMBER, 0.26);
        gl.uniform3f(uThin, thin[0], thin[1], thin[2]);
        gl.uniform3f(uDense, dense[0], dense[1], dense[2]);
      } else {
        var sc = mixRgb(c, OCHRE, 0.55);
        gl.uniform3f(uCol, sc[0], sc[1], sc[2]);
      }
    }

    var raf = null, t0 = 0, last = 0, running = false;

    function frame(now) {
      raf = requestAnimationFrame(frame);
      if (!t0) { t0 = now; last = now; return; }
      if (now - last < MIN_DT) return;
      var renderedMs = now - last;
      var dt = Math.min(0.1, renderedMs / 1000);
      last = now;
      adapt(now, renderedMs);
      var t = (now - t0) / 1000;
      var intensity = t < OPEN_S ? OPEN - (OPEN - BASE) * (t / OPEN_S) : BASE;

      gl.useProgram(prog);
      gl.clearColor(0, 0, 0, 0);
      gl.clear(gl.COLOR_BUFFER_BIT);

      if (MODE === 'veil') {
        gl.uniform1f(uTime, t);
        gl.uniform1f(uInt, intensity);
        gl.drawArrays(gl.TRIANGLES, 0, 3);
      } else {
        var count = simStreaks(dt, t, intensity);
        if (count > 0) {
          gl.bufferData(gl.ARRAY_BUFFER, verts.subarray(0, count), gl.DYNAMIC_DRAW);
          gl.drawArrays(gl.TRIANGLES, 0, count / 5);
        }
      }
    }

    return {
      start: function () { if (!raf) { running = true; raf = requestAnimationFrame(frame); } },
      stop:  function () { if (raf) { cancelAnimationFrame(raf); raf = null; running = false; } },
      resize: resize,
      setColor: setColor,
      isRunning: function () { return running; }
    };
  };
})();
