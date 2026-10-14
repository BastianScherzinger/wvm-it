/* Erklärfilme: stummer Loop startet erst im Viewport (IntersectionObserver), pausiert außerhalb.
   prefers-reduced-motion oder fehlender IntersectionObserver: nur Poster, dazu Bedienleiste zum Selbststarten.
   Der Pause-Knopf erfüllt WCAG 2.2.2 (automatisch startende Bewegung > 5 s). */
(function () {
  "use strict";
  var videos = document.querySelectorAll("video[data-vid]");
  if (!videos.length) return;
  var reduce = false;
  try { reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) {}

  videos.forEach(function (v) {
    var knopf = v.parentNode.querySelector("[data-vid-knopf]");
    var label = knopf && knopf.querySelector(".vid-knopf-t");
    var vomNutzerPausiert = false;

    function setze(spielt) {
      if (!knopf) return;
      knopf.setAttribute("aria-pressed", spielt ? "false" : "true");
      if (label) label.textContent = spielt ? "Pausieren" : "Abspielen";
    }
    function spiele() {
      var p = v.play();
      if (p && p.catch) p.catch(function () { setze(false); });
    }

    if (reduce || !("IntersectionObserver" in window)) {
      v.controls = true;                // Poster bleibt stehen, Abspielen nur auf Wunsch
      return;
    }

    if (knopf) {
      knopf.hidden = false;
      knopf.addEventListener("click", function () {
        if (v.paused) { vomNutzerPausiert = false; spiele(); } else { vomNutzerPausiert = true; v.pause(); }
      });
    }
    v.addEventListener("play", function () { setze(true); });
    v.addEventListener("pause", function () { setze(false); });

    new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (e) {
        if (e.isIntersecting) {
          if (v.preload !== "auto") v.preload = "auto";
          if (!vomNutzerPausiert) spiele();
        } else if (!v.paused) {
          v.pause();
        }
      });
    }, {threshold: 0.4}).observe(v);
  });
})();
