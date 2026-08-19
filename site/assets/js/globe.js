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
  { name: 'Turkey',       lat:  36.80, lon: 34.63, role: 'origination' },
  { name: 'Central Asia', lat:  43.24, lon: 76.89, role: 'origination' },
  { name: 'Jebel Ali',    lat:  25.01, lon: 55.06, role: 'hub' },
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

  const world = new THREE.Group();
  scene.add(world);

  /* three r155+ dropped legacy lighting, so these intensities are deliberate:
     anything lower renders the paper as mud. */
  const globeMat = new THREE.MeshLambertMaterial({ color: PAPER });
  world.add(new THREE.Mesh(new THREE.SphereGeometry(R, 96, 96), globeMat));
  scene.add(new THREE.AmbientLight(0xffffff, 2.5));
  const key = new THREE.DirectionalLight(0xffffff, 1.9);
  key.position.set(-1.1, 1.3, 1.9);
  scene.add(key);
  const fill = new THREE.DirectionalLight(0xffffff, 0.5);
  fill.position.set(1.4, -0.8, -1.2);
  scene.add(fill);

  /* Graticule */
  const gpts = [];
  for (let lon = -180; lon < 180; lon += 15)
    for (let lat = -85; lat < 85; lat += 5)
      gpts.push(toVec(lat, lon, R * 1.001), toVec(lat + 5, lon, R * 1.001));
  for (let lat = -60; lat <= 60; lat += 15)
    for (let lon = -180; lon < 180; lon += 5)
      gpts.push(toVec(lat, lon, R * 1.001), toVec(lat, lon + 5, R * 1.001));
  const gratMat = new THREE.LineBasicMaterial({ color: INK, transparent: true, opacity: 0.09 });
  world.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(gpts), gratMat));

  /* Coastlines */
  const coastMat = new THREE.LineBasicMaterial({ color: INK, transparent: true, opacity: 0.5 });
  try {
    const data = await (await fetch(dataUrl)).json();
    const cpts = [];
    for (const line of data.lines)
      for (let i = 0; i < line.length - 1; i++)
        cpts.push(toVec(line[i][1], line[i][0], R * 1.003),
                  toVec(line[i + 1][1], line[i + 1][0], R * 1.003));
    world.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(cpts), coastMat));
  } catch (e) { /* the lanes still read without a coastline */ }

  /* Lanes: three feeding in, one leaving. Same gold, different weight — the
     feeders recede, the delivery lane leads.

     Each lane keeps its index geometry so setProgress can draw it on rather
     than fade it in. A TubeGeometry's indices run in order along the curve, so
     clamping the draw range to a fraction of them literally extends the tube
     from origin toward the hub — the route is drawn the way it is travelled,
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
     The delivery lane belongs to East Africa, not to Jebel Ali — parked on the
     hub it left the final fifth of the scroll with nothing to draw.

     Reversible by construction, because everything is recomputed from p rather
     than advanced by events: scrolling back up unbuilds it in the same order.

     The build completes at REVEAL_END rather than at 1.0, so the last lane
     lands slightly before the reader stops scrolling instead of needing the
     timeline pushed to its exact end. */
  const STEPS = NODES.length;                /* 5 */
  const REVEAL_END = 0.9;
  let progress = -1;

  /* Per-waypoint: has this leg finished connecting? Read by the manifest. */
  const connected = new Array(STEPS).fill(false);

  function setProgress(p) {
    p = p < 0 ? 0 : p > 1 ? 1 : p;
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
         its own, so it counts once the node itself is fully in. */
      connected[i] = lane ? drawn >= 0.92 : nodeIn >= 1;
    }

    /* The hub arriving is what completes the three feeders, so they step up
       out of their receding weight as its slice runs. */
    const hubIn = Math.min(1, Math.max(0, scaled - lanes.length));
    for (const l of lanes) l.mesh.material.opacity = l.baseOpacity + 0.22 * hubIn;

    /* The pulse rides the outbound leg, so it appears with that leg rather
       than in the last three per cent of the timeline. */
    pulse.visible = outLane.mesh.visible;

    return connected;
  }

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
    pulse.position.copy(pulseCurve.getPointAt((time / 7000) % 1));

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
      l.el.style.opacity = facing > 0.12 ? String(l.lit) : '0';
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
    dom: renderer.domElement,
  };
}
