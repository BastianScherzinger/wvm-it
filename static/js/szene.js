/* Scroll-Szene (Umbau auf Anfragen, 31.10.2026): Handy scrollt durch Rümpelwerk-Ausschnitte,
   zwei Zahlen zählen hoch. Nur transform und Text ändern sich. Ohne JS, bei
   prefers-reduced-motion oder ohne IntersectionObserver bleibt das Standbild mit den
   Endwerten stehen (die Seite sagt dann dasselbe, nur ohne Bewegung). */
(function () {
  "use strict";
  var wurzel = document.querySelector("[data-szene]");
  if (!wurzel) return;
  var reduziert = false;
  try { reduziert = window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) {}
  if (reduziert) return;

  var spur = wurzel.querySelector(".rw-spur");
  var screen = wurzel.querySelector(".rw-screen");
  var bild = wurzel.querySelector(".rw-bild");
  var zahlen = wurzel.querySelectorAll(".rw-zahl");
  var lang = (document.documentElement.lang || "de").slice(0, 2);
  var fmt;
  try { fmt = new Intl.NumberFormat(lang === "ro" ? "ro-RO" : lang === "en" ? "en-GB" : "de-AT", { useGrouping: true }); }
  catch (e) { fmt = { format: function (n) { return String(n); } }; }
  /* Intl gruppiert vierstellige Zahlen im Deutschen erst ab 5 Stellen; wir wollen 5.492 immer. */
  function zeige(n) {
    var s = String(Math.round(n));
    var tz = lang === "en" ? "," : ".";
    return s.replace(/\B(?=(\d{3})+(?!\d))/g, tz);
  }

  wurzel.classList.add("szene-an");
  var laeuft = false;

  function ease(t) { return t < 0 ? 0 : t > 1 ? 1 : 1 - Math.pow(1 - t, 3); }

  function zeichne() {
    laeuft = false;
    var r = spur.getBoundingClientRect();
    var weg = spur.offsetHeight - window.innerHeight;
    var p = weg > 0 ? Math.min(1, Math.max(0, -r.top / weg)) : 1;
    var hoch = bild.clientHeight - screen.clientHeight;
    if (hoch > 0) bild.style.transform = "translate3d(0," + (-hoch * p).toFixed(1) + "px,0)";
    var q = ease((p - 0.08) / 0.8);
    for (var i = 0; i < zahlen.length; i++) {
      var von = parseFloat(zahlen[i].getAttribute("data-von"));
      var bis = parseFloat(zahlen[i].getAttribute("data-bis"));
      zahlen[i].textContent = zeige(von + (bis - von) * q);
    }
  }
  function plane() { if (!laeuft) { laeuft = true; window.requestAnimationFrame(zeichne); } }

  window.addEventListener("scroll", plane, { passive: true });
  window.addEventListener("resize", plane);
  if (bild.complete) zeichne(); else bild.addEventListener("load", zeichne);
  zeichne();
})();
