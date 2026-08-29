/* Kostenrechner — mitlaufende Anzeige (docs/SEO-AUSBAU-3.md, W1)
 *
 * Dieses Skript rechnet NICHT eigenständig: Es liest die Sätze aus dem
 * JSON-Block #rechner-saetze, den der Server aus ANGEBOT_GROUPS erzeugt hat.
 * Es gibt hier keine einzige eingetippte Zahl — die Lehre aus Rümpelwerk, wo
 * eine zweite Rechnung in JavaScript bei 9,6 % aller Eingaben um 1 € vom
 * Serverergebnis abwich (docs/preise-und-rechner.md dort).
 *
 * Ohne dieses Skript funktioniert die Seite vollständig: Das Formular ist ein
 * GET-Formular, der Server rechnet ohnehin. Das Skript spart nur den Seitenaufruf.
 */
(function () {
  "use strict";

  var quelle = document.getElementById("rechner-saetze");
  var form = document.getElementById("krForm");
  if (!quelle || !form) return;

  var S;
  try {
    S = JSON.parse(quelle.textContent);
  } catch (e) {
    return;                       // ohne Sätze lieber gar nichts als falsch
  }

  var felder = form.querySelectorAll("[data-kr]");
  var ausgaben = {};
  form.querySelectorAll("[data-kr-out]").forEach(function (el) {
    ausgaben[el.getAttribute("data-kr-out")] = el;
  });
  var posten = form.querySelector("[data-kr-posten]");
  var leer = form.querySelector("[data-kr-leer]");
  var zahlFormat = new Intl.NumberFormat((window.I18N && window.I18N.numLocale) || "de-AT",
                                         { maximumFractionDigits: 0 });

  function wert(name) {
    var el = form.querySelector('[data-kr="' + name + '"]');
    if (!el) return 0;
    if (el.type === "checkbox") return el.checked ? 1 : 0;
    var n = parseInt(el.value, 10);
    if (isNaN(n) || n < 0) n = 0;
    var max = (S[name] && S[name].max) || 0;
    if (max && n > max) n = max;
    return n;
  }

  function satz(name) {
    return (S[name] && S[name].satz) || 0;
  }

  function setze(name, zahl) {
    if (ausgaben[name]) ausgaben[name].textContent = zahlFormat.format(zahl);
  }

  function rechne() {
    var laufend = ["ap", "srv", "backup"];
    var einmal = ["neu", "m365"];
    var mtl = 0, once = 0;
    var zeilen = [];

    laufend.forEach(function (id) {
      var menge = wert(id);
      if (!menge) return;
      var summe = menge * satz(id);
      mtl += summe;
      zeilen.push({ id: id, menge: menge, satz: satz(id), summe: summe, once: false });
    });
    einmal.forEach(function (id) {
      var menge = wert(id);
      if (!menge) return;
      var summe = menge * satz(id);
      once += summe;
      zeilen.push({ id: id, menge: menge, satz: satz(id), summe: summe, once: true });
    });

    var stundensatz = satz("std");
    var stunden = wert("std");

    setze("mtl", mtl);
    setze("jahr", mtl * 12);
    setze("once", once);
    setze("vergleich_mtl", stundensatz * stunden);
    setze("schwelle", stundensatz ? Math.ceil(mtl / stundensatz) : 0);

    if (posten) {
      // Alle Zeilen stehen bereits im HTML — serverseitig gerendert, in der
      // richtigen Sprache. Hier werden sie nur ein- und ausgeblendet und die
      // beiden Zahlenspalten nachgezogen.
      posten.querySelectorAll("tr").forEach(function (tr) {
        var th = tr.querySelector("th");
        var id = th && th.dataset.krId;
        var treffer = zeilen.filter(function (z) { return z.id === id; })[0];
        if (!treffer) { tr.hidden = true; return; }
        tr.hidden = false;
        var tds = tr.querySelectorAll("td");
        if (tds[0]) tds[0].textContent = treffer.menge + " × " + zahlFormat.format(treffer.satz) + " €";
        if (tds[1]) tds[1].textContent = zahlFormat.format(treffer.summe) + " €";
      });
    }
    if (leer) leer.hidden = zeilen.length > 0;
  }

  felder.forEach(function (el) {
    el.addEventListener("input", rechne);
    el.addEventListener("change", rechne);
  });
  rechne();
})();
