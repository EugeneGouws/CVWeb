/* ============================================================
   supervet.js — Case study 1, the SuperVet "dish".
   A stock-ticker-style line chart of real packaging data: each
   variant's minimum print order drawn down at its actual monthly
   sell-through. Fast movers clear in months; slow movers sit for
   years — the hidden overstock problem. Numbers are hard-coded from
   data/Packaging.xlsx (data/ is gitignored; nothing invented here).
   Colours match the product packaging lines.
   ============================================================ */
(function () {
  "use strict";

  function start() {
    var mount = document.getElementById("supervet-chart");
    if (!mount || typeof Chart === "undefined") return;

    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    // Real figures: starting stock (tonnes) from one minimum order, and the
    // months it takes to deplete at the current monthly sell-through.
    // Colour = product line (Adult green / LB Puppy pink / Puppy blue);
    // size encoded by shade + dash (20kg = brand shade solid, 8kg = deeper dashed).
    var V = [
      { name: "Adult 20kg",     start: 120, months: 6.42,  color: "#4FE048", dash: false },
      { name: "Adult 8kg",      start: 32,  months: 12.09, color: "#79C96A", dash: true  },
      { name: "LB Puppy 20kg",  start: 60,  months: 21.33, color: "#E8559E", dash: false },
      { name: "LB Puppy 8kg",   start: 32,  months: 51.95, color: "#F09AC6", dash: true  },
      { name: "Puppy 8kg",      start: 32,  months: 34.68, color: "#4F90F2", dash: false }
    ];

    // dark-navy canvas: light text/grid
    var ink = "#EDEDE6", dim = "#AEB4D0", grid = "rgba(237,237,230,0.10)";

    var datasets = V.map(function (v) {
      return {
        label: v.name,
        data: [{ x: 0, y: v.start }, { x: v.months, y: 0 }],
        borderColor: v.color,
        backgroundColor: v.color,
        borderWidth: 2.5,
        borderDash: v.dash ? [6, 5] : [],
        pointRadius: 0,
        pointHoverRadius: 4,
        tension: 0,
        spanGaps: true
      };
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
      "Each line is the stock left from one minimum print order, drawn down at the real monthly " +
      "sell-through. Adult&nbsp;20kg clears in ~6&nbsp;months; <strong>LB&nbsp;Puppy&nbsp;8kg sits " +
      "for nearly 52</strong> — over four years of stock from a single run. Fixed setup " +
      "R108,660 · total R352,710.";
    mount.appendChild(wrap);
    mount.appendChild(cap);

    new Chart(canvas.getContext("2d"), {
      type: "line",
      data: { datasets: datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "nearest", intersect: false },
        animation: reduce ? false : { duration: 1500, easing: "easeInOutQuart" },
        scales: {
          x: {
            type: "linear",
            min: 0,
            max: 54,
            title: { display: true, text: "Months of stock on hand", color: dim,
                     font: { size: 12, weight: "600" } },
            ticks: { color: dim, stepSize: 6, font: { size: 11 } },
            grid: { color: grid }
          },
          y: {
            min: 0,
            title: { display: true, text: "Stock remaining (tonnes)", color: dim,
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
                      boxWidth: 28, font: { size: 12, weight: "600" } }
          },
          tooltip: {
            callbacks: {
              label: function (c) {
                return c.dataset.label + ": " + c.parsed.y.toFixed(0) + " T at month " +
                       c.parsed.x.toFixed(1);
              }
            }
          }
        }
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { setTimeout(start, 0); });
  } else { start(); }
})();
