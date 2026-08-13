/* ============================================================================
   ARMINAK CARAVAN — real sand
   ----------------------------------------------------------------------------
   The client asked for "настоящая анимация песка" — actual blowing sand, not
   drifting dots. Dots read as snow; sand reads as *streaked veils* of grain
   carried by wind, with individual grains catching light inside them.

   That is a noise problem, not a particle problem. This renders a single
   full-screen quad with domain-warped fBm — fbm(p + fbm(p + fbm(p))) — which
   is the standard way to get organic, swirling, wind-driven media
   (Quilez, iquilezles.org/articles/warp).

   Two layers in one pass:
     veils  — low-frequency warped fBm, stretched hard along the wind axis
     grains — high-frequency noise advected faster, masked to live inside veils

   All GPU, one draw call, no dependency (~6KB). Falls back to the canvas-2D
   dust if WebGL is unavailable, and is skipped entirely under reduced motion.
   ============================================================================ */
(function () {
  'use strict';

  var VERT = [
    'attribute vec2 a;',
    'void main(){ gl_Position = vec4(a, 0.0, 1.0); }'
  ].join('\n');

  var FRAG = [
    'precision highp float;',
    'uniform vec2  uRes;',
    'uniform float uTime;',
    'uniform vec3  uColor;',
    'uniform float uIntensity;',
    'uniform float uSeed;',

    'float hash(vec2 p){',
    '  p = fract(p * vec2(123.34, 456.21));',
    '  p += dot(p, p + 45.32);',
    '  return fract(p.x * p.y);',
    '}',

    'float noise(vec2 p){',
    '  vec2 i = floor(p), f = fract(p);',
    '  f = f * f * (3.0 - 2.0 * f);',
    '  float a = hash(i);',
    '  float b = hash(i + vec2(1.0, 0.0));',
    '  float c = hash(i + vec2(0.0, 1.0));',
    '  float d = hash(i + vec2(1.0, 1.0));',
    '  return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);',
    '}',

    'float fbm(vec2 p){',
    '  float v = 0.0, amp = 0.5;',
    '  for (int i = 0; i < 4; i++){',
    '    v += amp * noise(p);',
    '    p *= 2.03; amp *= 0.5;',
    '  }',
    '  return v;',
    '}',

    'void main(){',
    '  vec2 uv = gl_FragCoord.xy / uRes;',
    /* Anisotropic domain: wide in x, tight in y, so the noise smears into
       horizontal streaks the way wind-carried sand actually moves. */
    '  vec2 p = vec2(uv.x * 2.4, uv.y * 8.5) + uSeed;',
    '  float t = uTime * 0.055;',

    /* --- domain warp, two levels ------------------------------------- */
    '  vec2 q = vec2(fbm(p + vec2(t * 1.8, 0.0)),',
    '                fbm(p + vec2(5.2, 1.3) + vec2(t * 1.3, 0.0)));',
    '  vec2 r = vec2(fbm(p + 3.2 * q + vec2(1.7, 9.2) + vec2(t * 2.6, 0.0)),',
    '                fbm(p + 3.2 * q + vec2(8.3, 2.8) + vec2(t * 2.1, 0.0)));',
    '  float f = fbm(p + 3.6 * r + vec2(t * 3.1, 0.0));',

    /* Veils: only the crests of the field become visible sand. */
    '  float veil = smoothstep(0.45, 0.93, f);',

    /* Grains: fine noise blowing faster, only where a veil already exists. */
    '  vec2 gp = p * 13.0 + vec2(t * 26.0, 0.0);',
    '  float gn = noise(gp) * 0.62 + noise(gp * 2.3) * 0.38;',
    '  float grains = smoothstep(0.58, 0.95, gn) * veil;',

    /* Gusts: a slow swell so the wind breathes instead of running flat. */
    '  float gust = 0.72 + 0.28 * sin(uTime * 0.21 + f * 2.0);',

    '  float a = (veil * 0.92 + grains * 0.98) * uIntensity * gust;',
    /* A touch of dither: smooth gradients this wide band on 8-bit screens. */
    '  a += (hash(gl_FragCoord.xy * 0.7) - 0.5) * 0.014;',
    '  gl_FragColor = vec4(uColor, clamp(a, 0.0, 1.0));',
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
    hex = (hex || '#B08D57').trim().replace('#', '');
    if (hex.length === 3) hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
    var n = parseInt(hex, 16);
    return [((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255];
  }

  /* Returns a controller, or null if WebGL is unavailable so the caller can
     fall back rather than leaving the hero bare. */
  window.ACSand = function (canvas, host, opts) {
    opts = opts || {};
    var BASE   = opts.base   != null ? opts.base   : 0.95;  /* settled */
    var OPEN   = opts.open   != null ? opts.open   : 1.35;  /* entry gust */
    var OPEN_S = opts.openMs != null ? opts.openMs / 1000 : 3.4;
    var QUALITY = opts.scale != null ? opts.scale : 1;
    /* Sand drifts slowly — 30fps is indistinguishable from 60 here and
       halves the fill cost, which matters on fill-rate-limited phones. */
    var MIN_DT  = 1000 / (opts.fps != null ? opts.fps : 30);
    var gl = null;
    try {
      var attrs = { alpha: true, premultipliedAlpha: false, antialias: false, depth: false, stencil: false };
      gl = canvas.getContext('webgl', attrs) || canvas.getContext('experimental-webgl', attrs);
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
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 3,-1, -1,3]), gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(prog, 'a');
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);

    var uRes = gl.getUniformLocation(prog, 'uRes');
    var uTime = gl.getUniformLocation(prog, 'uTime');
    var uColor = gl.getUniformLocation(prog, 'uColor');
    var uInt = gl.getUniformLocation(prog, 'uIntensity');
    var uSeed = gl.getUniformLocation(prog, 'uSeed');

    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
    gl.uniform1f(uSeed, opts.seed != null ? opts.seed : 3.7);

    var raf = null, t0 = 0, last = 0, running = false;

    /* Sand is a texture, not detail — rendering below device pixel ratio is
       invisible here and keeps phones comfortable. */
    function scaleFor() {
      var dpr = window.devicePixelRatio || 1;
      return Math.min(dpr, window.innerWidth < 768 ? 0.85 : 1.35) * QUALITY;
    }

    function resize() {
      var r = host.getBoundingClientRect();
      var s = scaleFor();
      var w = Math.max(1, Math.round(r.width * s));
      var h = Math.max(1, Math.round(r.height * s));
      if (canvas.width !== w || canvas.height !== h) {
        canvas.width = w; canvas.height = h;
      }
      canvas.style.width = Math.round(r.width) + 'px';
      canvas.style.height = Math.round(r.height) + 'px';
      gl.viewport(0, 0, w, h);
      gl.uniform2f(uRes, w, h);
    }

    function setColor(hex) {
      var c = hexToRgb(hex);
      gl.useProgram(prog);
      gl.uniform3f(uColor, c[0], c[1], c[2]);
    }

    function frame(now) {
      raf = requestAnimationFrame(frame);
      if (!t0) t0 = now;
      if (now - last < MIN_DT) return;
      last = now;
      var elapsed = (now - t0) / 1000;

      /* Opens as a gust that reveals the caravan, then settles to a drift. */
      var intensity = elapsed < OPEN_S
        ? OPEN - (OPEN - BASE) * (elapsed / OPEN_S)
        : BASE;

      gl.useProgram(prog);
      gl.uniform1f(uTime, elapsed);
      gl.uniform1f(uInt, intensity);
      gl.clearColor(0, 0, 0, 0);
      gl.clear(gl.COLOR_BUFFER_BIT);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
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
