/* media.js — respect reduced-motion for autoplaying video.
   If the visitor prefers reduced motion, don't autoplay/loop the studio clip;
   show the poster with native controls so they can play it deliberately. */
(function () {
  "use strict";
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var vids = document.querySelectorAll("video[autoplay]");
  Array.prototype.forEach.call(vids, function (v) {
    v.removeAttribute("autoplay");
    v.removeAttribute("loop");
    v.setAttribute("controls", "");
    try { v.pause(); } catch (e) {}
  });
})();
