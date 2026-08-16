/* ============================================================================
   ARMINAK CARAVAN — GLSL dune field (hero backdrop)
   ----------------------------------------------------------------------------
   Replaces the two DISTANT bezier dunes (.dune--far / .dune--mid) with a
   raymarched dune landscape: real wind-carved ridges, asymmetric slip faces,
   parallax between dune trains. The NEAR dune stays as SVG — it is the ground
   the caravan was drawn to stand on, and a crisp foreground against a hazy
   distance is the composition we already had.

   Restraint is the whole point. The SVG dunes are var(--sand) at 0.20–0.42
   opacity over ivory: whispers, not photography. So the raymarch is used for
   FORM, and its lighting is mapped into that same whisper palette — shading
   drives ALPHA of a single brand colour rather than painting a literal desert.
   Drop a photoreal Sahara in here and the page stops being this brand.

   Static by design. The camera does not drift: the caravan is anchored to the
   ground, so a moving camera would make it slide. The terrain is the stage;
   the motion is the sand blowing over it (sand.js). Being static means it
   renders ONCE — near-zero ongoing cost, and reduced-motion users still get
   the full landscape because nothing about it animates.

   Returns null when WebGL is unavailable so the caller can simply leave the
   original SVG dunes visible.
   ============================================================================ */
(function () {
  'use strict';

  var VERT = 'attribute vec2 a; void main(){ gl_Position = vec4(a, 0.0, 1.0); }';

  var FRAG = [
    'precision highp float;',
    'uniform vec2  uRes;',
    'uniform float uHorizon;',      /* centred-uv y where the horizon sits */
    'uniform float uOpacity;',      /* ceiling, matched to the SVG dunes */
    'uniform vec3  uSand;',
    'uniform vec3  uDeep;',         /* slip-face tint, toward --ink */

    'float hash(vec2 p){',
    '  p = fract(p * vec2(123.34, 456.21));',
    '  p += dot(p, p + 45.32);',
    '  return fract(p.x * p.y);',
    '}',
    'float noise(vec2 p){',
    '  vec2 i = floor(p), f = fract(p);',
    '  f = f * f * (3.0 - 2.0 * f);',
    '  float a = hash(i), b = hash(i + vec2(1.0, 0.0));',
    '  float c = hash(i + vec2(0.0, 1.0)), d = hash(i + vec2(1.0, 1.0));',
    '  return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);',
    '}',

    /* Asymmetric dune profile: long windward climb, creased crest, steep slip
       face. This silhouette is what separates a dune from a hill. */
    'float duneWave(float x){',
    '  x = fract(x);',
    '  float up = pow(smoothstep(0.0, 0.74, x), 1.35);',
    '  float down = smoothstep(0.99, 0.76, x);',
    '  return min(up, down);',
    '}',

    /* Two dune trains at different scales, meandering along their ridge axis,
       riding on low fBm swell. */
    /* p is world (x = lateral, y = depth away from camera).
       The ridge axis runs ACROSS the view, not along it. Transverse dunes
       form perpendicular to the prevailing wind, and it is the difference
       between a desert and a mountain range: vary the profile with DEPTH and
       you get successive crest lines sweeping to the horizon — the same
       language as the stacked bezier curves this replaces. Vary it laterally
       instead and you stare down the length of the ridges and get pyramids. */
    'float height(vec2 p){',
    '  float mA = noise(vec2(p.x * 0.011, 3.1)) * 30.0;',   /* crests meander laterally */
    '  float mB = noise(vec2(p.x * 0.024, 8.7)) * 14.0;',
    '  float d1 = duneWave(p.y * 0.0125 + mA * 0.0125) * 15.0;',
    '  float d2 = duneWave(p.y * 0.030 + 0.37 + mB * 0.030) * 4.2;',
    '  float swell = noise(p * 0.016) * 2.6;',
    '  return d1 + d2 + swell;',
    '}',

    'float march(vec3 ro, vec3 rd, out float hitT){',
    '  float t = 0.6, ph = 0.0, pt = 0.0;',
    '  for (int i = 0; i < 160; i++){',
    '    vec3 p = ro + rd * t;',
    '    float h = p.y - height(p.xz);',
    '    if (h < 0.0025 * t){',
    '      hitT = pt + (t - pt) * ph / (ph - h);',   /* back off to the crossing */
    '      return 1.0;',
    '    }',
    '    if (t > 420.0) break;',
    '    ph = h; pt = t;',
    '    t += min(h * 0.32, 3.0) + 0.009 * t;',
    '  }',
    '  hitT = 420.0;',
    '  return 0.0;',
    '}',

    'vec3 normalAt(vec2 p, float t){',
    '  vec2 e = vec2(0.12 + 0.012 * t, 0.0);',
    '  return normalize(vec3(height(p - e.xy) - height(p + e.xy),',
    '                        2.0 * e.x,',
    '                        height(p - e.yx) - height(p + e.yx)));',
    '}',

    'void main(){',
    '  vec2 uv = (gl_FragCoord.xy * 2.0 - uRes) / uRes.y;',

    /* Static camera. rd.y = 0 exactly at uHorizon, so the horizon lands on the
       line the layout asks for at any viewport size. */
    '  vec3 ro = vec3(0.0, 21.0, 0.0);',   /* high crest: sees over the front dune to the layers behind */
    '  vec3 rd = normalize(vec3(uv.x * 0.62, (uv.y - uHorizon) * 0.62, 1.0));',

    '  if (rd.y >= -0.0015) { gl_FragColor = vec4(0.0); return; }',  /* sky: page shows through */

    '  vec3 sun = normalize(vec3(-0.62, 0.34, -0.42));',
    '  float t;',
    '  if (march(ro, rd, t) < 0.5) { gl_FragColor = vec4(0.0); return; }',

    '  vec3 p = ro + rd * t;',
    '  vec3 n = normalAt(p.xz, t);',
    '  float steep = smoothstep(0.26, 0.60, 1.0 - n.y);',   /* lee / slip faces */

    /* ---- layered silhouettes, not a shaded surface -------------------------
       The brand draws dunes as flat tinted planes stacked by depth. So instead
       of shading a continuous surface (which reads as a photographic wash and
       can only ever fade in horizontal bands), quantise the hit distance into
       discrete depth plates and give each a FLAT opacity. Ridges occlude what
       lies behind them, so every plate boundary traces a real dune crest —
       authentic wind-carved profiles in the existing flat-tint idiom. */
    '  float a = 0.055;',
    '  if (t < 275.0) a = 0.100;',
    '  if (t < 190.0) a = 0.165;',
    '  if (t < 118.0) a = 0.250;',
    '  if (t < 56.0) a = 0.355;',

    /* A whisper of relief inside each plate so slip faces are felt, never so
       much that the plate stops reading as flat. */
    '  a *= 0.94 + 0.20 * steep;',

    /* Only the farthest plate dissolves, so the horizon has no hard edge. */
    '  a *= 1.0 - smoothstep(230.0, 400.0, t);',

    '  vec3 col = mix(uSand, uDeep, steep * 0.16);',
    '  a *= uOpacity;',
    '  a += (fract(sin(dot(gl_FragCoord.xy, vec2(12.9898, 78.233))) * 43758.5453) - 0.5) * 0.004;',
    '  gl_FragColor = vec4(col, clamp(a, 0.0, 1.0));',
    '}'
  ].join('\n');

  function compile(gl, type, src) {
    var s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) { gl.deleteShader(s); return null; }
    return s;
  }

  function hexToRgb(hex) {
    hex = (hex || '#C7A87A').trim().replace('#', '');
    if (hex.length === 3) hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];
    var n = parseInt(hex, 16);
    return [((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255];
  }

  function token(name, fallback) {
    var v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    return v || fallback;
  }

  /* xMidYMax slice — identical mapping to the hero SVGs, so the horizon lands
     on the same viewBox line the layout was designed around. */
  function sliceMap(w, h, vbW, vbH) {
    var s = Math.max(w / vbW, h / vbH);
    return { s: s, oy: h - vbH * s };
  }

  window.ACDunes = function (canvas, host, opts) {
    opts = opts || {};
    var VB = opts.viewBox || [1600, 900];
    var HORIZON_VB = opts.horizonY != null ? opts.horizonY : 545;

    var gl = null;
    try {
      gl = canvas.getContext('webgl', {
        alpha: true, premultipliedAlpha: false, antialias: false,
        depth: false, stencil: false,
        preserveDrawingBuffer: true      /* render once, keep the frame */
      });
    } catch (e) { return null; }
    if (!gl) return null;

    var vs = compile(gl, gl.VERTEX_SHADER, VERT);
    var fs = compile(gl, gl.FRAGMENT_SHADER, FRAG);
    if (!vs || !fs) return null;
    var prog = gl.createProgram();
    gl.attachShader(prog, vs); gl.attachShader(prog, fs); gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return null;
    gl.useProgram(prog);

    var buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(prog, 'a');
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);

    var uRes = gl.getUniformLocation(prog, 'uRes');
    var uHorizon = gl.getUniformLocation(prog, 'uHorizon');
    var uOpacity = gl.getUniformLocation(prog, 'uOpacity');
    var uSand = gl.getUniformLocation(prog, 'uSand');
    var uDeep = gl.getUniformLocation(prog, 'uDeep');

    var cssW = 1, cssH = 1;

    function applyTheme() {
      var dark = document.documentElement.getAttribute('data-theme') === 'dark';
      var sand = hexToRgb(token('--sand', dark ? '#C9A570' : '#C7A87A'));
      var ink = hexToRgb(token('--ink', dark ? '#F2EDE3' : '#1B2A41'));
      gl.useProgram(prog);
      gl.uniform3f(uSand, sand[0], sand[1], sand[2]);
      /* Dark mode: "deep" must go lighter, not darker — the ground is near-black
         there, so shadow reads as glow. */
      gl.uniform3f(uDeep, ink[0], ink[1], ink[2]);
      /* Matched to .dune--far/.dune--mid: whispers, not photography. */
      gl.uniform1f(uOpacity, dark ? 0.52 : 1.0);
    }

    /* A zero-sized host (hidden tab, pane mid-resize, hero not laid out yet)
       would bake a 1px-wide terrain that never recovers, since this only
       redraws on demand. Refuse to render until the box is real, and let the
       ResizeObserver below call back when it becomes real. */
    function resize() {
      var r = host.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) return false;
      cssW = Math.round(r.width);
      cssH = Math.round(r.height);
      /* Renders once, so we can afford above-CSS resolution — but the forms are
         soft, and a raymarch is per-pixel, so 1.25x is the sweet spot. */
      var scale = Math.min((window.devicePixelRatio || 1) * 1.4, 2.0);
      var w = Math.max(1, Math.round(cssW * scale));
      var h = Math.max(1, Math.round(cssH * scale));
      canvas.width = w; canvas.height = h;
      canvas.style.width = cssW + 'px';
      canvas.style.height = cssH + 'px';
      gl.viewport(0, 0, w, h);
      gl.useProgram(prog);
      gl.uniform2f(uRes, w, h);

      /* Horizon: map the target viewBox line through the same slice transform
         the SVGs use, then convert to centred-uv. */
      var m = sliceMap(cssW, cssH, VB[0], VB[1]);
      var horizonCss = m.oy + HORIZON_VB * m.s;
      gl.uniform1f(uHorizon, 1 - 2 * (horizonCss / cssH));
      return true;
    }

    function render() {
      gl.useProgram(prog);
      gl.clearColor(0, 0, 0, 0);
      gl.clear(gl.COLOR_BUFFER_BIT);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      gl.flush();
    }

    function draw() { return resize() ? (render(), true) : false; }

    /* Self-healing: the hero can get its real size after init (fonts, layout,
       a hidden tab becoming visible). Redraw whenever the box actually
       changes, which also covers the zero-size case above. */
    var lastW = 0, lastH = 0;
    if (typeof ResizeObserver === 'function') {
      new ResizeObserver(function () {
        var r = host.getBoundingClientRect();
        var w = Math.round(r.width), h = Math.round(r.height);
        if (w < 2 || h < 2 || (w === lastW && h === lastH)) return;
        lastW = w; lastH = h;
        draw();
      }).observe(host);
    }

    return {
      redraw: function () { applyTheme(); return draw(); },
      render: render,
      resize: draw,
      setTheme: function () { applyTheme(); render(); }
    };
  };
})();
