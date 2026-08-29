/* Schnellstart-Pakete über dem Konfigurator (UX-Ausbau 2026-08)
 *
 * Ein Klick auf eine Paketkachel setzt die Haken der enthaltenen Positionen.
 * Das Skript rechnet NICHTS: Es setzt nur `checked` und löst ein `change`-
 * Ereignis aus — die Summenrechnung liegt weiterhin dort, wo sie vorher lag
 * (angebot.js auf /angebot/, main.js im Inline-Block der Startseite).
 *
 * Ohne dieses Skript funktioniert alles unverändert: Die Kacheln sind Links auf
 * ?paket=<id>, und der Server setzt die Haken beim Rendern. Das Skript spart
 * nur den Seitenaufruf und behält die Scrollposition.
 */
(function () {
  "use strict";

  var behaelter = document.querySelector("[data-startpakete]");
  if (!behaelter) return;

  // Das Formular, dessen Haken gesetzt werden: der Konfigurator auf dieser Seite.
  var form = document.getElementById("angForm") || document.getElementById("rbForm");
  if (!form) return;

  function setze(ids) {
    var gewuenscht = {};
    ids.forEach(function (id) { gewuenscht[id] = true; });
    form.querySelectorAll('input[name="item"]').forEach(function (feld) {
      var soll = !!gewuenscht[feld.value];
      if (feld.checked !== soll) {
        feld.checked = soll;
        // Beide Ereignisse: die eine Summenrechnung hört auf `change`,
        // die andere auf `input`. Doppelt gesendet schadet keiner von beiden.
        feld.dispatchEvent(new Event("input", { bubbles: true }));
        feld.dispatchEvent(new Event("change", { bubbles: true }));
      }
    });
  }

  function markiere(karte) {
    behaelter.querySelectorAll("[data-paket]").forEach(function (k) {
      k.classList.toggle("is-aktiv", k === karte);
    });
  }

  behaelter.querySelectorAll("[data-paket]").forEach(function (karte) {
    karte.addEventListener("click", function (ereignis) {
      var roh = (karte.getAttribute("data-paket") || "").trim();
      if (!roh) return;                       // leeres Paket: Link normal folgen
      ereignis.preventDefault();
      setze(roh.split(/\s+/));
      markiere(karte);
      // Der Konfigurator steht direkt darunter — dorthin scrollen, damit die
      // gesetzten Haken und die Summe sichtbar werden.
      var ziel = document.getElementById("konfigurator") || form;
      if (ziel && ziel.scrollIntoView) {
        // Wer weiche Bewegung abgestellt hat, bekommt sie auch hier nicht.
        var sanft = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
        ziel.scrollIntoView({ behavior: sanft ? "smooth" : "auto", block: "start" });
      }
    });
  });

  var reset = behaelter.querySelector("[data-paket-reset]");
  if (reset) {
    reset.addEventListener("click", function (ereignis) {
      ereignis.preventDefault();
      setze([]);
      markiere(null);
    });
  }
})();
