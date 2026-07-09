/* ============================================================================
   WVM-IT ,  Angebots-Konfigurator
   Liest die Preise aus den data-Attributen der Checkboxen (einzige Quelle bleibt
   das Django-Backend, das die Auswahl beim Absenden neu berechnet) und aktualisiert
   Warenkorb, Summen (Einmalig / Monatlich / Jährlich) und die Mobil-Leiste live.
   Progressive Enhancement: ohne JS bleiben die Checkboxen ein normales Formular.
   ========================================================================== */
(function () {
  "use strict";
  var form = document.getElementById("angForm");
  if (!form) return;

  var boxes = Array.prototype.slice.call(form.querySelectorAll(".ang-check"));
  var listEl = document.getElementById("angCartList");
  var emptyEl = document.getElementById("angCartEmpty");
  var totalsEl = document.getElementById("angTotals");
  var onceEl = document.getElementById("angOnce");
  var mtlEl = document.getElementById("angMtl");
  var yrEl = document.getElementById("angYr");
  var anfrageEl = document.getElementById("angAnfrage");
  var countEl = document.getElementById("angCount");
  var submitEl = document.getElementById("angSubmit");
  var hintEl = document.getElementById("angHint");
  var mobar = document.getElementById("angMobar");
  var mobarCount = document.getElementById("angMobarCount");
  var mobarPrice = document.getElementById("angMobarPrice");

  function eur(n) { return (n || 0).toLocaleString("de-DE"); }

  // Kurzes Preis-Label pro Position (spiegelt die Backend-Logik).
  function priceLabel(d) {
    if (d.anfrage) return "auf Anfrage";
    var parts = [];
    if (d.once) parts.push(eur(d.once) + " €");
    if (d.mtl) parts.push(d.mtl + " €/Mt");
    if (d.yr) parts.push(eur(d.yr) + " €/Jahr");
    return parts.join(" + ") || "-";
  }

  function read(box) {
    return {
      id: box.value,
      name: box.getAttribute("data-name") || box.value,
      once: parseInt(box.getAttribute("data-once"), 10) || 0,
      mtl: parseInt(box.getAttribute("data-mtl"), 10) || 0,
      yr: parseInt(box.getAttribute("data-yr"), 10) || 0,
      anfrage: box.getAttribute("data-anfrage") === "1"
    };
  }

  function setRow(name, value, show) {
    var row = totalsEl ? totalsEl.querySelector('[data-total="' + name + '"]') : null;
    if (!row) return;
    row.hidden = !show;
  }

  function render() {
    var chosen = boxes.filter(function (b) { return b.checked; }).map(read);
    var once = 0, mtl = 0, yr = 0, anfrage = false;

    // Warenkorb-Zeilen
    var frag = document.createDocumentFragment();
    chosen.forEach(function (d) {
      once += d.once; mtl += d.mtl; yr += d.yr;
      if (d.anfrage) anfrage = true;
      var li = document.createElement("li");
      li.className = "ang-ci";
      var nm = document.createElement("span");
      nm.className = "ang-ci-name";
      nm.textContent = d.name;
      var pr = document.createElement("span");
      pr.className = "ang-ci-price";
      pr.textContent = priceLabel(d);
      var x = document.createElement("button");
      x.type = "button";
      x.className = "ang-ci-x";
      x.setAttribute("aria-label", "Entfernen: " + d.name);
      x.setAttribute("data-remove", d.id);
      x.textContent = "×";
      li.appendChild(nm); li.appendChild(pr); li.appendChild(x);
      frag.appendChild(li);
    });

    // Liste neu befüllen (Empty-State erhalten)
    Array.prototype.slice.call(listEl.querySelectorAll(".ang-ci")).forEach(function (n) { n.remove(); });
    if (emptyEl) emptyEl.hidden = chosen.length > 0;
    listEl.appendChild(frag);

    // Summen
    if (onceEl) onceEl.textContent = eur(once);
    if (mtlEl) mtlEl.textContent = eur(mtl);
    if (yrEl) yrEl.textContent = eur(yr);
    setRow("once", once, once > 0);
    setRow("mtl", mtl, mtl > 0);
    setRow("yr", yr, yr > 0);
    if (anfrageEl) anfrageEl.hidden = !anfrage;
    if (totalsEl) totalsEl.hidden = chosen.length === 0;

    // Zähler + Submit-Status
    var label = chosen.length === 1 ? "1 Leistung" : chosen.length + " Leistungen";
    if (countEl) countEl.textContent = label;
    if (submitEl) submitEl.classList.toggle("is-off", chosen.length === 0);
    if (hintEl) hintEl.hidden = chosen.length > 0;

    // Mobil-Leiste
    if (mobar) {
      mobar.hidden = chosen.length === 0;
      if (mobarCount) mobarCount.textContent = label;
      if (mobarPrice) {
        var main = once > 0 ? ("ab " + eur(once) + " €") : (mtl > 0 ? (eur(mtl) + " €/Mt") : (yr > 0 ? (eur(yr) + " €/Jahr") : ""));
        mobarPrice.textContent = main;
      }
    }
  }

  boxes.forEach(function (b) { b.addEventListener("change", render); });

  // Entfernen-Buttons (Event-Delegation)
  if (listEl) {
    listEl.addEventListener("click", function (e) {
      var btn = e.target.closest ? e.target.closest("[data-remove]") : null;
      if (!btn) return;
      var id = btn.getAttribute("data-remove");
      var box = form.querySelector('.ang-check[value="' + id + '"]');
      if (box) { box.checked = false; render(); }
    });
  }

  // Absenden nur mit mindestens einer Leistung
  form.addEventListener("submit", function (e) {
    var any = boxes.some(function (b) { return b.checked; });
    if (!any) {
      e.preventDefault();
      if (hintEl) hintEl.hidden = false;
      var head = document.getElementById("konfigurator");
      if (head && head.scrollIntoView) head.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });

  render();
})();
