/* Erklärfilme: der stumme Film startet selbst, sobald er beim Scrollen zu mindestens 40 % sichtbar ist
   (IntersectionObserver), und pausiert, wenn er den Bildschirm verlässt. Kein Ladezustand: das Poster ist das erste
   Filmbild, die Datei wird schon vor dem Sichtbarwerden angefordert (preload per Skript, nicht im Tag).
   prefers-reduced-motion oder kein IntersectionObserver: nur das Poster, dazu ein Abspielen-Knopf.
   Der Pause-Knopf erfüllt WCAG 2.2.2 (automatisch startende Bewegung > 5 s). */
(function () {
  "use strict";
  var videos = document.querySelectorAll("video[data-vid]");
  if (!videos.length) return;
  var reduce = false;
  try { reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) {}

  videos.forEach(function (v) {
    var rahmen = v.parentNode;
    var knopf = rahmen.querySelector("[data-vid-knopf]");
    var label = knopf && knopf.querySelector(".vid-knopf-t");
    var vomNutzerPausiert = false;

    function setze(spielt) {
      if (!knopf) return;
      knopf.setAttribute("aria-pressed", spielt ? "false" : "true");
      if (label) label.textContent = spielt ? "Pausieren" : "Abspielen";
      rahmen.classList.toggle("vid-spielt", spielt);
    }
    function spiele() {
      var p = v.play();
      if (p && p.catch) p.catch(function () { setze(false); });
    }
    function umschalten() {
      if (v.paused) { vomNutzerPausiert = false; spiele(); } else { vomNutzerPausiert = true; v.pause(); }
    }

    var ohneBewegung = reduce || !("IntersectionObserver" in window);
    if (knopf) {
      knopf.hidden = false;
      knopf.addEventListener("click", umschalten);
    }
    if (ohneBewegung) {
      rahmen.classList.add("vid-ruhig");   /* großer Abspielen-Knopf über dem Poster */
      setze(false);
      return;
    }
    v.addEventListener("play", function () { setze(true); });
    v.addEventListener("pause", function () { setze(false); });

    /* Datei früh holen, damit der Start ohne Ladepause kommt */
    new IntersectionObserver(function (eintraege, beob) {
      if (eintraege.some(function (e) { return e.isIntersecting; })) {
        if (v.preload !== "auto") v.preload = "auto";
        beob.disconnect();
      }
    }, {rootMargin: "900px 0px"}).observe(v);

    new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (e) {
        if (e.isIntersecting) {
          if (!vomNutzerPausiert) spiele();
        } else if (!v.paused) {
          v.pause();
        }
      });
    }, {threshold: 0.4}).observe(v);
  });
})();
