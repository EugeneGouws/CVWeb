/* ============================================================
   nodemap.js — the signature element.
   A 3Blue1Brown-style transformer diagram: four past domains (left)
   feed forward through three labelled "black-box" hidden layers
   — Data Driven · User Convenience · Corporate Governance — and
   resolve into one output, "Infinite Solutions". Dense wiring carries
   travelling pulses (signals); hovering a domain or a layer heading
   traces the thought; headings deep-link to their case-study panel.
   Dependency-free.
   ============================================================ */
(function () {
  "use strict";

  var mount = document.getElementById("nodemap");
  if (!mount) return;

  var SVGNS = "http://www.w3.org/2000/svg";
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---- Geometry ----
  var W = 1180, H = 480;
  var TOP = 84, BOT = 452, BAND = BOT - TOP;
  var IN_W = 172, IN_H = 46, IN_X = 6;
  var OUT_W = 172, OUT_H = 54, OUT_X = W - 6 - OUT_W;
  var DOT_R = 7;
  var HEAD_Y = 46;
  var COL_X = [375, 590, 805];          // three hidden columns
  var IN_RIGHT = IN_X + IN_W;

  function lerpRows(n) {                  // n vertical centres across the band
    var out = [];
    for (var i = 0; i < n; i++) out.push(Math.round(TOP + (BAND * i) / (n - 1)));
    return out;
  }
  var IN_ROWS = lerpRows(4);
  var DOT_ROWS = lerpRows(6);
  var OUT_ROWS = lerpRows(3);

  // ---- Content (Eugene's spec) — full words throughout ----
  var inputs = ["Mathematics", "Brand Management", "Teaching", "Audio Engineering"];
  var columns = [
    { head: "Data Driven",          target: "#supervet" },
    { head: "User Convenience",     target: "#edutech"  },
    { head: "Corporate Governance", target: "#studio"   }
  ];
  var outputs = ["Transferable Experience", "Problem Solving", "Digital Fluency"];

  function el(name, attrs) {
    var n = document.createElementNS(SVGNS, name);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    return n;
  }
  function curve(x1, y1, x2, y2) {
    var mx = (x1 + x2) / 2;
    return "M" + x1 + "," + y1 + " C" + mx + "," + y1 + " " + mx + "," + y2 + " " + x2 + "," + y2;
  }

  var svg = el("svg", { viewBox: "0 0 " + W + " " + H, role: "group",
                        "aria-label": "Transformer-style skills diagram" });

  // ---- Node registry + adjacency ----
  var nodes = {};            // id -> { el, neighbours:Set, edges:[] }
  function reg(id, gel) { nodes[id] = { el: gel, edges: [] }; }

  // ---- Build layer point sets ----
  var pts = { in: [], h: [[], [], []], out: [] };
  IN_ROWS.forEach(function (cy, i) { pts.in.push({ x: IN_RIGHT, cy: cy, id: "in" + i }); });
  COL_X.forEach(function (cx, c) {
    DOT_ROWS.forEach(function (cy, r) { pts.h[c].push({ x: cx, cy: cy, id: "h" + c + "_" + r }); });
  });
  OUT_ROWS.forEach(function (cy, i) { pts.out.push({ x: OUT_X, cy: cy, id: "out" + i }); });

  // ---- Edges (drawn first, behind everything) ----
  var edges = [];
  function connect(aList, bList, aRightX, bLeftX) {
    aList.forEach(function (a) {
      bList.forEach(function (b) {
        var d = curve(aRightX !== undefined ? aRightX : a.x, a.cy,
                      bLeftX  !== undefined ? bLeftX  : b.x, b.cy);
        var p = el("path", { class: "nm-edge", d: d });
        var rec = { el: p, from: a.id, to: b.id, d: d };
        edges.push(rec);
        svg.appendChild(p);
      });
    });
  }
  connect(pts.in,   pts.h[0], IN_RIGHT, undefined);
  connect(pts.h[0], pts.h[1]);
  connect(pts.h[1], pts.h[2]);
  connect(pts.h[2], pts.out, undefined, OUT_X);   // last hidden column -> three outputs

  // ---- Travelling pulses: clone a subset of edges as animated sparks ----
  var sparkLayer = el("g", { class: "nm-sparks", "aria-hidden": "true" });
  svg.appendChild(sparkLayer);
  shuffle(edges).slice(0, 52).forEach(function (e) {
    var s = el("path", { class: "nm-spark", d: e.d });
    var len = e.el.getTotalLength();
    s.style.setProperty("--len", len);
    s.style.setProperty("--spd", (1.8 + Math.random() * 1.9).toFixed(2) + "s");
    s.style.setProperty("--dly", "-" + (Math.random() * 3).toFixed(2) + "s");
    sparkLayer.appendChild(s);
  });

  // ---- Hidden-layer dots ----
  pts.h.forEach(function (col) {
    col.forEach(function (p) {
      var c = el("circle", { class: "nm-dot", cx: p.x, cy: p.cy, r: DOT_R });
      reg(p.id, c);
      svg.appendChild(c);
    });
  });

  // ---- Input domain boxes ----
  function labelBox(g, x, cy, w, h, lines, opts) {
    g.setAttribute("transform", "translate(" + x + "," + (cy - h / 2) + ")");
    g.appendChild(el("rect", { class: "nm-node-box", width: w, height: h, rx: 6 }));
    var t = el("text", { class: "nm-node-label", x: w / 2, y: h / 2, "text-anchor": "middle" });
    if (lines.length === 1) { t.textContent = lines[0]; }
    else {
      lines.forEach(function (ln, i) {
        var ts = el("tspan", { x: w / 2, dy: i === 0 ? -(lines.length - 1) * 8 : 18 });
        ts.textContent = ln; t.appendChild(ts);
      });
    }
    g.appendChild(t);
  }
  inputs.forEach(function (label, i) {
    var g = el("g", { class: "nm-node", tabindex: "0", "aria-label": label + " — input domain" });
    labelBox(g, IN_X, IN_ROWS[i], IN_W, IN_H, [label]);
    reg(pts.in[i].id, g);
    svg.appendChild(g);
  });

  // ---- Output boxes (the payoff) ----
  outputs.forEach(function (label, i) {
    var g = el("g", { class: "nm-node nm-out", tabindex: "0", "aria-label": label + " — output" });
    labelBox(g, OUT_X, OUT_ROWS[i], OUT_W, OUT_H, label.split(" "));
    reg(pts.out[i].id, g);
    svg.appendChild(g);
  });

  // ---- Column headings (deep-links) ----
  columns.forEach(function (col, c) {
    var g = el("g", { class: "nm-col", role: "link", tabindex: "0",
                      "aria-label": col.head + " — go to case study" });
    g.dataset.col = c;
    g.dataset.target = col.target;
    var words = col.head.split(" ");
    var t = el("text", { class: "nm-head", x: COL_X[c], y: HEAD_Y });
    if (words.length > 1 && col.head.length > 12) {
      words.forEach(function (w, i) {
        var ts = el("tspan", { x: COL_X[c], dy: i === 0 ? 0 : 14 }); ts.textContent = w; t.appendChild(ts);
      });
      t.setAttribute("y", HEAD_Y - 7);
    } else { t.textContent = col.head; }
    g.appendChild(t);
    svg.appendChild(g);
  });

  mount.appendChild(svg);

  // ---- Build adjacency ----
  edges.forEach(function (e) {
    if (nodes[e.from]) nodes[e.from].edges.push(e);
    if (nodes[e.to])   nodes[e.to].edges.push(e);
  });

  // ---- Highlighting ----
  function clear() {
    mount.classList.remove("is-hovering");
    edges.forEach(function (e) { e.el.classList.remove("is-active"); });
    Object.keys(nodes).forEach(function (id) { nodes[id].el.classList.remove("is-active"); });
  }
  function activateNodes(ids) {
    mount.classList.add("is-hovering");
    var set = {};
    ids.forEach(function (id) { set[id] = true; });
    ids.forEach(function (id) {
      var n = nodes[id]; if (!n) return;
      n.el.classList.add("is-active");
      n.edges.forEach(function (e) {
        e.el.classList.add("is-active");
        var other = e.from === id ? e.to : e.from;
        if (nodes[other]) nodes[other].el.classList.add("is-active");
      });
    });
  }

  // input boxes + outputs: hover/focus highlight their cone
  ["in0", "in1", "in2", "in3", "out0", "out1", "out2"].forEach(function (id) {
    var n = nodes[id]; if (!n) return;
    n.el.addEventListener("mouseenter", function () { activateNodes([id]); });
    n.el.addEventListener("mouseleave", clear);
    n.el.addEventListener("focus", function () { activateNodes([id]); });
    n.el.addEventListener("blur", clear);
  });

  // column headings: highlight the whole column + navigate
  function navigate(target) {
    var dest = document.querySelector(target);
    if (!dest) return;
    dest.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
    if (history.replaceState) history.replaceState(null, "", target);
  }
  svg.querySelectorAll(".nm-col").forEach(function (g) {
    var c = +g.dataset.col, target = g.dataset.target;
    var colIds = DOT_ROWS.map(function (_, r) { return "h" + c + "_" + r; });
    g.addEventListener("mouseenter", function () { activateNodes(colIds); });
    g.addEventListener("mouseleave", clear);
    g.addEventListener("focus", function () { activateNodes(colIds); });
    g.addEventListener("blur", clear);
    g.addEventListener("click", function () { navigate(target); });
    g.addEventListener("keydown", function (ev) {
      if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); navigate(target); }
    });
  });

  // ---- Reveal ----
  requestAnimationFrame(function () { mount.classList.add("ready"); });

  // ---- util ----
  function shuffle(a) {
    var b = a.slice();
    for (var i = b.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = b[i]; b[i] = b[j]; b[j] = t;
    }
    return b;
  }
})();
