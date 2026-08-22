/* ============================================================================
   Corridor globe — the trade lanes drawn on the actual planet.

   An engraved paper globe rather than the usual dark sphere with a satellite
   texture on it: the world is line work, because every other surface on this
   site is drawn rather than photographed. Coastlines are Natural Earth 110m,
   decoded to plain polylines at build time so nothing but three.js loads here.

   Arcs are true great circles. That is the whole argument for a globe: the
   shortest path over a sphere is the path a vessel takes, and it is exactly
   what a flat map destroys.

   Mounted lazily by main.js — desktop, WebGL and full-motion only. Everything
   else keeps the flat SVG that ships in the markup.
   ========================================================================== */

import * as THREE from '../vendor/three.module.min.js';
import { OrbitControls } from '../vendor/OrbitControls.js';

const NODES = [
  { name: 'Black Sea',    lat:  44.72, lon: 37.77, role: 'origination' },
  { name: 'Türkiye',      lat:  36.80, lon: 34.63, role: 'origination' },
  { name: 'Central Asia', lat:  43.24, lon: 76.89, role: 'origination' },
  { name: 'UAE',          lat:  25.01, lon: 55.06, role: 'hub' },
  { name: 'East Africa',  lat:  -4.04, lon: 39.67, role: 'delivery' },
];

const R = 1;

const toVec = (lat, lon, r = R) => {
  const phi = (90 - lat) * Math.PI / 180;
  const theta = (lon + 180) * Math.PI / 180;
  return new THREE.Vector3(
    -r * Math.sin(phi) * Math.cos(theta),
     r * Math.cos(phi),
     r * Math.sin(phi) * Math.sin(theta));
};

/* Slerp for the path, a sine for the lift — a route above the world rather
   than a scratch on it. */
function greatCircle(a, b, lift = 0.17, seg = 128) {
  const va = toVec(a.lat, a.lon);
  const vb = toVec(b.lat, b.lon);
  const ang = va.angleTo(vb);
  const pts = [];
  for (let i = 0; i <= seg; i++) {
    const t = i / seg;
    const p = new THREE.Vector3().copy(va).lerp(vb, t).normalize();
    p.multiplyScalar(R + Math.sin(Math.PI * t) * lift * ang);
    pts.push(p);
  }
  return new THREE.CatmullRomCurve3(pts);
}

export async function mountGlobe(host, opts = {}) {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const dataUrl = opts.dataUrl || 'assets/data/coastlines.json';

  /* Phone build. Matched to the CSS breakpoint rather than to a guess about
     screen size, so the layout and the geometry budget can never disagree. */
  const compact = matchMedia('(max-width: 999px)').matches;
  const touch = matchMedia('(pointer: coarse)').matches;

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  } catch (e) {
    return null;                       /* caller keeps the flat fallback */
  }

  /* Palette notes, learned the hard way in dark mode:

     --ink inverts between themes (navy on ivory, cream on matte black), so a
     lane painted with it is quiet in one theme and the loudest object on the
     page in the other. Both lane types are therefore brand gold, and the
     hierarchy is carried by weight and opacity instead of by hue — which is
     how the rest of this site separates primary from secondary anyway.

     The sphere uses --tile rather than --bg-elev: in dark, bg-elev sits a
     hair off the page colour and the globe reads as a hole. */
  const css = getComputedStyle(document.documentElement);
  const tok = (n, fb) => new THREE.Color(css.getPropertyValue(n).trim() || fb);
  let INK    = tok('--ink', '#1B2A41');
  let ACCENT = tok('--accent', '#B08D57');
  let PAPER  = tok('--tile', '#EFEAE0');

  const size = host.clientWidth;
  renderer.setPixelRatio(Math.min(devicePixelRatio, innerWidth < 700 ? 1.5 : 2));
  renderer.setSize(size, size, false);
  host.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 100);
  camera.position.copy(toVec(22, 52, 3.75));

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.06;
  controls.enablePan = false;
  controls.enableZoom = false;          /* the page owns the scroll wheel */
  controls.rotateSpeed = 0.42;
  controls.autoRotate = !reduced;
  controls.autoRotateSpeed = 0.28;

  /* Touch needs the two gestures separated, and disabling the controls was the
     wrong tool: OrbitControls stamps `touch-action: none` on the canvas inside
     connect(), so the browser refuses to scroll over it whatever the enabled
     flag says. The globe was interactive-looking but frozen, and the page would
     not scroll past it either.

     touch-action does the split properly instead. `pan-y` hands vertical
     swipes to the browser — the page scrolls through the globe as it should —
     while horizontal drags never become scrolls and so arrive as pointer
     events, which is exactly the axis you want for turning a planet. Taps still
     pick. Set after construction because connect() has already written it. */
  if (touch) renderer.domElement.style.touchAction = 'pan-y';

  const world = new THREE.Group();
  scene.add(world);

  /* three r155+ dropped legacy lighting, so these intensities are deliberate:
     anything lower renders the paper as mud. */
  const globeMat = new THREE.MeshLambertMaterial({ color: PAPER });
  const globeMesh = new THREE.Mesh(new THREE.SphereGeometry(R, compact ? 56 : 96, compact ? 56 : 96), globeMat);
  world.add(globeMesh);
  scene.add(new THREE.AmbientLight(0xffffff, 2.5));
  const key = new THREE.DirectionalLight(0xffffff, 1.9);
  key.position.set(-1.1, 1.3, 1.9);
  scene.add(key);
  const fill = new THREE.DirectionalLight(0xffffff, 0.5);
  fill.position.set(1.4, -0.8, -1.2);
  scene.add(fill);

  /* Graticule */
  /* A phone shows this at roughly a third the diameter, so a graticule at full
     density is a moiré rather than a grid — and thousands of extra segments for
     a mesh nobody can resolve. */
  const gStep = compact ? 30 : 15;           /* degrees between lines */
  const gSeg  = compact ? 10 : 5;            /* tessellation along a line */
  const gpts = [];
  for (let lon = -180; lon < 180; lon += gStep)
    for (let lat = -85; lat < 85; lat += gSeg)
      gpts.push(toVec(lat, lon, R * 1.001), toVec(lat + gSeg, lon, R * 1.001));
  for (let lat = -60; lat <= 60; lat += gStep)
    for (let lon = -180; lon < 180; lon += gSeg)
      gpts.push(toVec(lat, lon, R * 1.001), toVec(lat, lon + gSeg, R * 1.001));
  const gratMat = new THREE.LineBasicMaterial({ color: INK, transparent: true, opacity: 0.09 });
  world.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(gpts), gratMat));

  /* Coastlines */
  const coastMat = new THREE.LineBasicMaterial({ color: INK, transparent: true, opacity: 0.5 });
  try {
    const data = await (await fetch(dataUrl)).json();
    const cpts = [];
    /* Every other vertex on a phone: at this diameter the dropped detail is
       well under a pixel, and it halves the coastline geometry. */
    const step = compact ? 2 : 1;
    for (const line of data.lines)
      for (let i = 0; i + step < line.length; i += step)
        cpts.push(toVec(line[i][1], line[i][0], R * 1.003),
                  toVec(line[i + step][1], line[i + step][0], R * 1.003));
    world.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(cpts), coastMat));
  } catch (e) { /* the lanes still read without a coastline */ }

  /* Lanes: three feeding in, one leaving. Same gold, different weight — the
     feeders recede, the delivery lane leads.

     Each lane keeps its index geometry so setProgress can draw it on rather
     than fade it in. A TubeGeometry's indices run in order along the curve, so
     clamping the draw range to a fraction of them literally extends the tube
     from origin toward the Gulf — the route is drawn the way it is travelled,
     which is the entire point of showing a corridor rather than a dot. */
  const hub = NODES.find(n => n.role === 'hub');
  const laneMats = [];
  const lanes = [];                          /* one per origination, in NODES order */

  function addLane(from, to, lift, radius, opacity, segs) {
    const curve = greatCircle(from, to, lift);
    const geo = new THREE.TubeGeometry(curve, segs, radius, 8, false);
    const m = new THREE.MeshBasicMaterial({ color: ACCENT, transparent: true, opacity: opacity });
    laneMats.push(['accent', m]);
    const mesh = new THREE.Mesh(geo, m);
    mesh.visible = false;
    world.add(mesh);
    return { mesh, geo, curve, total: geo.index.count, baseOpacity: opacity };
  }

  for (const n of NODES) {
    if (n.role !== 'origination') continue;
    lanes.push(addLane(n, hub, 0.17, 0.0038, 0.5, 128));
  }

  const out = NODES.find(n => n.role === 'delivery');
  const outLane = addLane(hub, out, 0.2, 0.0072, 0.95, 160);
  const pulseCurve = outLane.curve;

  const pulseMat = new THREE.MeshBasicMaterial({ color: ACCENT, transparent: true, opacity: 1 });
  laneMats.push(['accent', pulseMat]);
  const pulse = new THREE.Mesh(new THREE.SphereGeometry(0.017, 16, 16), pulseMat);
  pulse.visible = false;
  world.add(pulse);

  /* Markers for a picked waypoint. Three, because picking the hub lights all
     three feeders at once and they should run together rather than in turn —
     the hub's whole story is that everything arrives there. */
  const focusDots = [];
  for (let i = 0; i < 3; i++) {
    const fm = new THREE.MeshBasicMaterial({ color: ACCENT });
    laneMats.push(['accent', fm]);
    const d = new THREE.Mesh(new THREE.SphereGeometry(0.022, 16, 16), fm);
    d.visible = false;
    world.add(d);
    focusDots.push(d);
  }

  /* Nodes, and HTML labels so the type stays the site's own. */
  const labels = [];
  const marks = [];                          /* dot + ring + label, in NODES order */
  for (const n of NODES) {
    const v = toVec(n.lat, n.lon, R * 1.004);
    const isHub = n.role === 'hub';

    /* The hub is the one node that outranks the others, so it gets size and a
       wider ring — not a different colour. */
    const dotMat = new THREE.MeshBasicMaterial({ color: ACCENT });
    laneMats.push(['accent', dotMat]);
    const dot = new THREE.Mesh(new THREE.SphereGeometry(isHub ? 0.019 : 0.011, 16, 16), dotMat);
    dot.position.copy(v);
    world.add(dot);

    const ringMat = new THREE.MeshBasicMaterial({
      color: ACCENT, transparent: true, opacity: isHub ? 0.8 : 0.5, side: THREE.DoubleSide });
    laneMats.push(['accent', ringMat]);
    const ring = new THREE.Mesh(
      new THREE.RingGeometry(isHub ? 0.032 : 0.024, isHub ? 0.036 : 0.027, 48), ringMat);
    ring.position.copy(v);
    ring.lookAt(0, 0, 0);
    world.add(ring);

    const el = document.createElement('div');
    el.className = 'globe__lbl';
    el.innerHTML = '<b>' + n.name + '</b>';
    host.appendChild(el);
    const label = { el, v, lit: 0 };
    labels.push(label);

    dot.visible = false;
    ring.visible = false;
    marks.push({ dot, ring, ringMat, dotMat, label, isHub });
  }

  /* ---- scroll reveal -------------------------------------------------------
     One 0..1 value drives the whole instrument, and it is the ONLY source of
     truth: setProgress returns the per-waypoint connected state and the page's
     manifest reads that array rather than recomputing the same thresholds.
     The two used to be worked out independently and had drifted — rows lit
     when their lane was 8% drawn, not when it landed.

     The five slices read as the trade actually runs: three originations each
     draw their own feeder into the Gulf, the hub slice lands them (the feeders
     brighten as it arrives), and the delivery slice draws the outbound leg.
     The delivery lane belongs to East Africa, not to the Gulf node — parked on the
     hub it left the final fifth of the scroll with nothing to draw.

     Reversible by construction, because everything is recomputed from p rather
     than advanced by events: scrolling back up unbuilds it in the same order.

     The build completes at REVEAL_END rather than at 1.0, so the last lane
     lands slightly before the reader stops scrolling instead of needing the
     timeline pushed to its exact end. */
  const STEPS = NODES.length;                /* 5 */
  const REVEAL_END = 0.9;
  let progress = -1;
  let lastP = 0;                             /* so a pick can repaint at the
                                                scroll position it happened at */

  /* Per-waypoint: has this leg finished connecting? Read by the manifest. */
  const connected = new Array(STEPS).fill(false);

  /* ---- picking -------------------------------------------------------------
     Which legs belong to a waypoint. An origination owns the feeder it sends
     into the Gulf; the hub owns all three arriving at it; the delivery node
     owns the outbound leg. */
  function routeOf(i) {
    if (i == null) return null;
    if (i < lanes.length) return [lanes[i]];
    if (NODES[i].role === 'hub') return lanes.slice();
    return [outLane];
  }

  let selected = null;
  let scrollHubIn = 0;
  let onSelect = opts.onSelect || null;      /* set later via setOnSelect */

  /* Every lane's weight is decided in one place, because two things want a
     say: how far the scroll has built, and whether something is picked. A
     picked route goes to full and forces itself drawn — clicking a waypoint
     you have not scrolled to yet should still show you its route — and
     everything else drops back so the picked one is the only thing read. */
  function paintLanes() {
    const route = routeOf(selected);
    const all = lanes.concat([outLane]);
    for (const l of all) {
      const inRoute = route ? route.indexOf(l) > -1 : false;
      if (route) {
        l.mesh.material.opacity = inRoute ? 1 : 0.09;
        if (inRoute) {
          l.mesh.visible = true;
          l.geo.setDrawRange(0, l.total);
        }
      } else {
        l.mesh.material.opacity = l === outLane
          ? outLane.baseOpacity
          : l.baseOpacity + 0.22 * scrollHubIn;
      }
    }

    /* A picked waypoint's own mark leads; the others step back so the eye
       goes to the leg, not to the field of dots. */
    for (let i = 0; i < STEPS; i++) {
      const m = marks[i];
      const dim = selected !== null && selected !== i;
      m.dotMat.opacity = dim ? 0.35 : 1;
      m.dotMat.transparent = true;
      m.label.dim = dim;
    }
  }

  function setProgress(p) {
    p = p < 0 ? 0 : p > 1 ? 1 : p;
    lastP = p;
    if (Math.abs(p - progress) < 0.001) return connected;
    progress = p;

    const scaled = Math.min(STEPS, (p / REVEAL_END) * STEPS);

    for (let i = 0; i < STEPS; i++) {
      const local = Math.min(1, Math.max(0, scaled - i));   /* this step's own 0..1 */
      const m = marks[i];

      /* Node lands in the first third of its slice, lane draws over the rest. */
      const nodeIn = Math.min(1, local / 0.30);
      m.dot.visible = nodeIn > 0;
      m.ring.visible = nodeIn > 0;
      if (nodeIn > 0) {
        const s = 0.4 + 0.6 * nodeIn;
        m.dot.scale.setScalar(s);
        m.ring.scale.setScalar(0.6 + 0.4 * nodeIn);
        m.ringMat.opacity = (m.isHub ? 0.8 : 0.5) * nodeIn;
      }
      m.label.lit = nodeIn;

      /* Originations feed the hub; the delivery node draws the outbound leg.
         The hub itself has no lane — its slice is the arrival, and it is paid
         off by the feeders brightening below. */
      const lane = i < lanes.length ? lanes[i]
                 : (NODES[i].role === 'delivery' ? outLane : null);

      let drawn = 0;
      if (lane) {
        drawn = Math.min(1, Math.max(0, (local - 0.25) / 0.75));
        lane.mesh.visible = drawn > 0;
        /* Round to a whole triangle or the tube ends in a torn face. */
        lane.geo.setDrawRange(0, Math.floor(lane.total * drawn / 3) * 3);
      }

      /* A leg counts as connected when its lane lands. The hub has no lane of
         its own, so it takes the same end-of-slice phase — gating it on the
         node alone lit it a third of the way in, which bunched it against the
         waypoint before it. */
      connected[i] = local >= 0.92 && (lane ? drawn >= 0.92 : nodeIn >= 1);
    }

    /* The hub arriving is what completes the three feeders, so they step up
       out of their receding weight as its slice runs. */
    scrollHubIn = Math.min(1, Math.max(0, scaled - lanes.length));
    paintLanes();

    return connected;
  }

  /* Pick a waypoint, or pass null to release. Everything is recomputed from
     the stored scroll position rather than nudged, so releasing a pick lands
     back exactly on whatever the scroll had built.

     Picking deliberately does NOT turn the globe. The default view already
     frames all five waypoints — Black Sea through to East Africa sit inside
     one hemisphere — so swinging the sphere on every click only pushed them
     out toward the limb where the projection squashes them and the outermost
     one clips off the edge. The sphere holds still; the lanes do the talking.
     Auto-rotation is parked for the same reason: a highlighted route that
     slowly drifts away is not a highlight. */
  function select(i, silent) {
    if (i === selected) i = null;            /* clicking the same one releases */
    selected = i;
    controls.autoRotate = !reduced && selected === null;

    progress = -1;                           /* force a full recompute */
    setProgress(lastP);
    if (!silent && onSelect) onSelect(selected);
    return selected;
  }

  /* Nearest-node-to-the-hit-point rather than a hitbox per dot: the dots are
     0.011 of a unit sphere, which is far too small to ask anyone to hit. */
  const ray = new THREE.Raycaster();
  const ndc = new THREE.Vector2();
  /* ~14° of arc counts as "on it" — more on touch, where the target is a
     fingertip and the sphere is a third the size. */
  const PICK_ANGLE = touch ? 0.34 : 0.24;
  const MOVE_TOL = touch ? 14 : 6;           /* px of travel that still reads as a tap */

  function hitTest(ev) {
    const r = renderer.domElement.getBoundingClientRect();
    ndc.x = ((ev.clientX - r.left) / r.width) * 2 - 1;
    ndc.y = -((ev.clientY - r.top) / r.height) * 2 + 1;
    ray.setFromCamera(ndc, camera);
    const hit = ray.intersectObject(globeMesh, false)[0];
    if (!hit) return null;
    const local = world.worldToLocal(hit.point.clone()).normalize();
    let best = null, bestAng = PICK_ANGLE;
    for (let i = 0; i < STEPS; i++) {
      if (!marks[i].dot.visible) continue;    /* not revealed yet — not pickable */
      const ang = local.angleTo(marks[i].label.v.clone().normalize());
      if (ang < bestAng) { bestAng = ang; best = i; }
    }
    return best;
  }

  /* OrbitControls owns the drag, so only a press that did not travel counts
     as a click — otherwise every turn of the globe would also pick something. */
  let downAt = null;
  renderer.domElement.addEventListener('pointerdown', function (e) {
    downAt = { x: e.clientX, y: e.clientY, t: performance.now() };
  });
  renderer.domElement.addEventListener('pointerup', function (e) {
    if (!downAt) return;
    const moved = Math.hypot(e.clientX - downAt.x, e.clientY - downAt.y);
    const quick = performance.now() - downAt.t < 500;
    downAt = null;
    if (moved > MOVE_TOL || !quick) return;
    select(hitTest(e));
  });
  if (!touch) renderer.domElement.addEventListener('pointermove', function (e) {
    if (downAt) return;                       /* mid-drag: leave the cursor */
    renderer.domElement.style.cursor = hitTest(e) === null ? '' : 'pointer';
  });
  renderer.domElement.addEventListener('pointerleave', function () {
    renderer.domElement.style.cursor = '';
  });

  function onResize() {
    const s = host.clientWidth;
    renderer.setSize(s, s, false);
    camera.aspect = 1;
    camera.updateProjectionMatrix();
  }
  addEventListener('resize', onResize);
  onResize();

  /* Theme is a runtime switch on this site, so the instrument follows it. */
  document.addEventListener('ac:theme', function () {
    const c = getComputedStyle(document.documentElement);
    INK    = new THREE.Color(c.getPropertyValue('--ink').trim());
    ACCENT = new THREE.Color(c.getPropertyValue('--accent').trim());
    PAPER  = new THREE.Color(c.getPropertyValue('--tile').trim());
    globeMat.color.copy(PAPER);
    gratMat.color.copy(INK);
    coastMat.color.copy(INK);
    for (const [kind, m] of laneMats) m.color.copy(kind === 'ink' ? INK : ACCENT);
  });

  const tmp = new THREE.Vector3();
  let running = true;

  function loop(time) {
    controls.update();

    if (selected !== null) {
      /* One marker per leg of the picked route, all running together. */
      const route = routeOf(selected);
      const t = (time / 2400) % 1;
      for (let i = 0; i < focusDots.length; i++) {
        const on = i < route.length;
        focusDots[i].visible = on;
        if (on) focusDots[i].position.copy(route[i].curve.getPointAt(t));
      }
      pulse.visible = false;                 /* the ambient one would compete */
    } else {
      for (const d of focusDots) d.visible = false;
      pulse.position.copy(pulseCurve.getPointAt((time / 7000) % 1));
      pulse.visible = outLane.mesh.visible;
    }

    const rect = host.getBoundingClientRect();
    const camDir = camera.position.clone().normalize();
    for (const l of labels) {
      tmp.copy(l.v).applyMatrix4(world.matrixWorld);
      /* Anything on the far side is hidden rather than allowed to bleed
         through the sphere — the one thing that instantly reads as broken. */
      const facing = tmp.clone().normalize().dot(camDir);
      tmp.project(camera);
      l.el.style.left = ((tmp.x * 0.5 + 0.5) * rect.width) + 'px';
      l.el.style.top  = ((-tmp.y * 0.5 + 0.5) * rect.height - 30) + 'px';
      /* Two gates, both of which must pass: facing the camera, and revealed by
         the scroll. A label for a waypoint that has not arrived yet would give
         the reveal away before it happens. */
      l.el.style.opacity = facing > 0.12 ? String(l.lit * (l.dim ? 0.4 : 1)) : '0';
    }
    renderer.render(scene, camera);
  }

  renderer.setAnimationLoop(loop);

  /* Nothing is visible until the page says how far it has scrolled. Reduced
     motion has no scroll choreography to hook into, so it gets the finished
     state immediately rather than an empty globe. */
  setProgress(reduced ? 1 : 0);

  return {
    /* Nothing to render while it is off screen. */
    pause() { if (running) { renderer.setAnimationLoop(null); running = false; } },
    resume() { if (!running) { renderer.setAnimationLoop(loop); running = true; } },
    /* Reduced motion gets the finished state, and must still tell the
       manifest every leg is connected — otherwise the table stays grey. */
    setProgress: reduced ? function () { return connected.fill(true); } : setProgress,
    /* Picking from the manifest table. silent=true suppresses onSelect so the
       table can drive without being told what it already knows. */
    select: select,
    selected: function () { return selected; },
    /* The page registers this after mount so a pick on the sphere can move the
       manifest's own highlight. */
    setOnSelect: function (fn) { onSelect = fn; },
    dom: renderer.domElement,
  };
}
