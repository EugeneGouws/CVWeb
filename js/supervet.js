/* ============================================================
   supervet.js — Case study 1, the SuperVet "dish".
   Illustrative projection: for each of the three product lines, sales
   without the packaging redesign (declining trend) against sales with
   it (dip while the reprint cost is absorbed, then overtaking). Shape
   is illustrative, not measured data — the point is the crossover, not
   the numbers. Draws in real time, left to right, like a stock ticker.
   Colours match the product packaging lines.
   ============================================================ */
(function () {
  "use strict";

  // seeded PRNG so the "jagged" noise is stable across reloads
  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  var rand = mulberry32(20260701);

  function jaggedSeries(points, noiseFrac) {
    return points.map(function (p) {
      var jitter = (rand() * 2 - 1) * noiseFrac * p.y;
      return { x: p.x, y: Math.max(0, p.y + jitter) };
    });
  }

  // smooth base curve helper: exponential decay / logistic growth
  function decayCurve(start, floor, rate, months) {
    var pts = [];
    for (var m = 0; m <= months; m++) {
      pts.push({ x: m, y: floor + (start - floor) * Math.exp(-rate * m) });
    }
    return pts;
  }
  function growthCurve(low, high, mid, steep, months) {
    var pts = [];
    for (var m = 0; m <= months; m++) {
      var s = 1 / (1 + Math.exp(-steep * (m - mid)));
      pts.push({ x: m, y: low + (high - low) * s });
    }
    return pts;
  }

  function start() {
    var mount = document.getElementById("supervet-chart");
    if (!mount || typeof Chart === "undefined") return;

    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var MONTHS = 24;

    // three product lines, brand-matched colours; "before" = dashed/dim,
    // "after" = solid/bright, same hue per product
    var P = [
      { name: "Adult",     before: "#4E6B48", after: "#4FE048",
        beforePts: decayCurve(92, 30, 0.075, MONTHS),
        afterPts:  growthCurve(38, 150, 9, 0.55, MONTHS) },
      { name: "LB Puppy",  before: "#7A4D62", after: "#E8559E",
        beforePts: decayCurve(70, 18, 0.09, MONTHS),
        afterPts:  growthCurve(24, 118, 10, 0.5, MONTHS) },
      { name: "Puppy",     before: "#3F5670", after: "#4F90F2",
        beforePts: decayCurve(58, 14, 0.1, MONTHS),
        afterPts:  growthCurve(18, 96, 11, 0.5, MONTHS) }
    ];

    // light cream/white-card theme: dark, high-contrast legend + axis text
    var ink = "#1B1B1B", dim = "#5E5645", grid = "rgba(27,27,27,0.10)";

    var datasets = [];
    P.forEach(function (p) {
      datasets.push({
        label: p.name + " — without redesign",
        fullData: jaggedSeries(p.beforePts, 0.05),
        data: [],
        borderColor: p.before,
        backgroundColor: p.before,
        borderWidth: 2,
        borderDash: [6, 5],
        pointRadius: 0,
        pointHoverRadius: 3,
        tension: 0.25
      });
      datasets.push({
        label: p.name + " — with redesign",
        fullData: jaggedSeries(p.afterPts, 0.05),
        data: [],
        borderColor: p.after,
        backgroundColor: p.after,
        borderWidth: 2.5,
        borderDash: [],
        pointRadius: 0,
        pointHoverRadius: 3,
        tension: 0.25
      });
    });

    // build the mount: canvas + caption
    mount.classList.add("is-filled");
    mount.innerHTML = "";
    var wrap = document.createElement("div");
    wrap.className = "exp-chart";
    var canvas = document.createElement("canvas");
    wrap.appendChild(canvas);
    var cap = document.createElement("p");
    cap.className = "exp-caption";
    cap.innerHTML =
      "Illustrative projection, not measured data: without the redesign, each product&rsquo;s sales " +
      "trend flattens off. With it, sales dip while the reprint cost is absorbed &mdash; then " +
      "<strong>overtake within a year</strong>, product by product.";
    mount.appendChild(wrap);
    mount.appendChild(cap);

    var chart = new Chart(canvas.getContext("2d"), {
      type: "line",
      data: { datasets: datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "nearest", intersect: false },
        animation: false,
        scales: {
          x: {
            type: "linear",
            min: 0,
            max: MONTHS,
            title: { display: true, text: "Months since redesign", color: dim,
                     font: { size: 12, weight: "600" } },
            ticks: { color: dim, stepSize: 3, font: { size: 11 } },
            grid: { color: grid }
          },
          y: {
            min: 0,
            title: { display: true, text: "Sales (index)", color: dim,
                     font: { size: 12, weight: "600" } },
            ticks: { color: dim, font: { size: 11 } },
            grid: { color: grid }
          }
        },
        plugins: {
          legend: {
            position: "top",
            align: "start",
            labels: { color: ink, usePointStyle: true, pointStyle: "line",
                      boxWidth: 28, font: { size: 12, weight: "700" } }
          },
          tooltip: {
            callbacks: {
              label: function (c) {
                return c.dataset.label + ": " + c.parsed.y.toFixed(0) + " at month " +
                       c.parsed.x.toFixed(0);
              }
            }
          }
        }
      }
    });

    if (reduce) {
      datasets.forEach(function (d) { d.data = d.fullData; });
      chart.update("none");
      return;
    }

    // three-at-a-time reveal: all "without redesign" lines draw together,
    // then all "with redesign" lines draw together, then hold, then loop
    var total = MONTHS + 1;
    var beforeSet = datasets.filter(function (_, i) { return i % 2 === 0; });
    var afterSet  = datasets.filter(function (_, i) { return i % 2 === 1; });

    function revealGroup(group, durationMs, onDone) {
      var startTime = null;
      function step(now) {
        if (startTime === null) startTime = now;
        var frac = Math.min(1, (now - startTime) / durationMs);
        var count = Math.max(2, Math.round(frac * total));
        group.forEach(function (d) { d.data = d.fullData.slice(0, count); });
        chart.update("none");
        if (frac < 1) requestAnimationFrame(step);
        else onDone();
      }
      requestAnimationFrame(step);
    }

    function playOnce(onDone) {
      datasets.forEach(function (d) { d.data = []; });
      chart.update("none");
      revealGroup(beforeSet, 1400, function () {
        revealGroup(afterSet, 1400, onDone);
      });
    }

    (function loop() {
      playOnce(function () { setTimeout(loop, 3000); });
    })();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { setTimeout(start, 0); });
  } else { start(); }
})();
