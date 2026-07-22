/* ============================================================================
   WVM-IT ,  Angebots-Konfigurator (mehrstufiger Wizard)
   - Schritt-für-Schritt-Slides: pro Slide nur wenige Leistungen (Weiter/Zurück,
     Schritt-Anzeige, Fortschrittsbalken).
   - Live-Summe: läuft auf jeder Slide mit; auf der letzten Slide die volle
     Aufschlüsselung (Einmalig / Monatlich / Jährlich) + Lead-Formular.
   - Preise kommen aus den data-Attributen (Anzeige); das Django-Backend berechnet
     die Auswahl beim Absenden serverseitig NEU (kein Client-Trust).
   - Progressive Enhancement: ohne JS bleiben alle Slides als lange Liste sichtbar,
     die Checkboxen sind ein normales Formular.
   ========================================================================== */
(function () {
  "use strict";
  var form = document.getElementById("angForm");
  if (!form) return;

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  // Lokalisierte Labels + Zahlenformat (Fallback: Deutsch).
  var I = (window.I18N && window.I18N.ang) || {};
  var NL = (window.I18N && window.I18N.numLocale) || "de-DE";
  var T_ON_REQ = I.on_request || "auf Anfrage";
  var T_FROM = I.from || "ab";
  var T_PM = I.per_month || "€/Mt";
  var T_PY = I.per_year || "€/Jahr";
  var T_ONE = I.leistung || "Leistung";
  var T_MANY = I.leistungen || "Leistungen";
  var T_REMOVE = I.remove || "Entfernen:";

  // ── Wizard-Modus aktivieren ──────────────────────────────────────────────
  form.classList.add("wz-on");
  var panels = Array.prototype.slice.call(form.querySelectorAll(".wz-panel"));
  var steps = Array.prototype.slice.call(form.querySelectorAll(".wz-step"));
  var bar = document.getElementById("wzBar");
  var head = document.getElementById("konfigurator");
  var last = panels.length - 1;
  var current = 0;

  function scrollToWizard() {
    if (!head || !head.scrollIntoView) return;
    head.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
  }

  function show(i, doScroll) {
    i = Math.max(0, Math.min(last, i));
    current = i;
    panels.forEach(function (p, idx) { p.classList.toggle("is-active", idx === i); });
    steps.forEach(function (s, idx) {
      s.classList.toggle("is-active", idx === i);
      s.classList.toggle("is-done", idx < i);
    });
    if (bar) bar.style.width = (last > 0 ? (i / last) * 100 : 100).toFixed(2) + "%";
    if (typeof updateMobar === "function") updateMobar();
    if (doScroll) scrollToWizard();
  }

  form.querySelectorAll(".wz-next").forEach(function (b) {
    b.addEventListener("click", function () { show(current + 1, true); });
  });
  form.querySelectorAll(".wz-back").forEach(function (b) {
    b.addEventListener("click", function () { show(current - 1, true); });
  });
  steps.forEach(function (s, idx) {
    s.addEventListener("click", function () { show(idx, true); });
    s.setAttribute("role", "button");
    s.setAttribute("tabindex", "0");
    s.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); show(idx, true); }
    });
  });

  // ── Live-Summe ───────────────────────────────────────────────────────────
  var boxes = Array.prototype.slice.call(form.querySelectorAll(".ang-check"));
  var runCounts = Array.prototype.slice.call(form.querySelectorAll("[data-run-count]"));
  var runSums = Array.prototype.slice.call(form.querySelectorAll("[data-run-sum]"));
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
  // Mobile Sticky-Summenleiste: zeigt die laufende Summe, solange man noch
  // Leistungen waehlt; auf dem letzten Schritt (Ihr Angebot) versteckt sie sich,
  // weil die volle Aufschluesselung dort schon sichtbar ist.
  var mobar = document.getElementById("angMobar");
  var mobarCount = document.getElementById("angMobarCount");
  var mobarSum = document.getElementById("angMobarSum");
  var mobarBtn = document.getElementById("angMobarBtn");

  function eur(n) { return (n || 0).toLocaleString(NL); }

  function priceLabel(d) {
    if (d.anfrage) return T_ON_REQ;
    var parts = [];
    if (d.once) parts.push(eur(d.once) + " €");
    if (d.mtl) parts.push(d.mtl + " " + T_PM);
    if (d.yr) parts.push(eur(d.yr) + " " + T_PY);
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

  function runSummary(once, mtl, yr) {
    var main = "";
    if (once) main = T_FROM + " " + eur(once) + " €";
    if (mtl) main += (main ? " + " : "") + eur(mtl) + " " + T_PM;
    if (!main && yr) main = eur(yr) + " " + T_PY;
    return main || "0 €";
  }

  function render() {
    var chosen = boxes.filter(function (b) { return b.checked; }).map(read);
    var once = 0, mtl = 0, yr = 0, anfrage = false;

    var frag = document.createDocumentFragment();
    chosen.forEach(function (d) {
      once += d.once; mtl += d.mtl; yr += d.yr;
      if (d.anfrage) anfrage = true;
      var li = document.createElement("li");
      li.className = "ang-ci";
      var nm = document.createElement("span");
      nm.className = "ang-ci-name"; nm.textContent = d.name;
      var pr = document.createElement("span");
      pr.className = "ang-ci-price"; pr.textContent = priceLabel(d);
      var x = document.createElement("button");
      x.type = "button"; x.className = "ang-ci-x";
      x.setAttribute("aria-label", T_REMOVE + " " + d.name);
      x.setAttribute("data-remove", d.id); x.textContent = "×";
      li.appendChild(nm); li.appendChild(pr); li.appendChild(x);
      frag.appendChild(li);
    });

    if (listEl) {
      Array.prototype.slice.call(listEl.querySelectorAll(".ang-ci")).forEach(function (n) { n.remove(); });
      if (emptyEl) emptyEl.hidden = chosen.length > 0;
      listEl.appendChild(frag);
    }

    if (onceEl) onceEl.textContent = eur(once);
    if (mtlEl) mtlEl.textContent = eur(mtl);
    if (yrEl) yrEl.textContent = eur(yr);
    function setRow(name, show) {
      var row = totalsEl ? totalsEl.querySelector('[data-total="' + name + '"]') : null;
      if (row) row.hidden = !show;
    }
    setRow("once", once > 0);
    setRow("mtl", mtl > 0);
    setRow("yr", yr > 0);
    if (anfrageEl) anfrageEl.hidden = !anfrage;
    if (totalsEl) totalsEl.hidden = chosen.length === 0;

    var label = chosen.length + " " + (chosen.length === 1 ? T_ONE : T_MANY);
    var sum = runSummary(once, mtl, yr);
    runCounts.forEach(function (el) { el.textContent = label; });
    runSums.forEach(function (el) { el.textContent = sum; });
    if (countEl) countEl.textContent = label;
    if (submitEl) submitEl.classList.toggle("is-off", chosen.length === 0);
    if (hintEl) hintEl.hidden = chosen.length > 0;
    if (mobarCount) mobarCount.textContent = label;
    if (mobarSum) mobarSum.textContent = sum;
    updateMobar();
  }

  function updateMobar() {
    if (!mobar) return;
    var anySelected = boxes.some(function (b) { return b.checked; });
    // Nur zeigen, solange etwas gewaehlt ist UND man noch nicht auf dem letzten
    // Schritt (Ihr Angebot) steht, dort ist die volle Summe schon sichtbar.
    mobar.hidden = !anySelected || current === last;
  }

  boxes.forEach(function (b) { b.addEventListener("change", render); });
  if (mobarBtn) mobarBtn.addEventListener("click", function () { show(last, true); });

  if (listEl) {
    listEl.addEventListener("click", function (e) {
      var btn = e.target.closest ? e.target.closest("[data-remove]") : null;
      if (!btn) return;
      var id = btn.getAttribute("data-remove");
      var box = form.querySelector('.ang-check[value="' + id + '"]');
      if (box) { box.checked = false; render(); }
    });
  }

  form.addEventListener("submit", function (e) {
    var any = boxes.some(function (b) { return b.checked; });
    if (!any) {
      e.preventDefault();
      if (hintEl) hintEl.hidden = false;
      show(last, true);
    }
  });

  // Vorauswahl per ?kat=<id> (Deep-Link von der Startseite auf einen Schritt)
  var startStep = 0;
  try {
    var kat = new URLSearchParams(window.location.search).get("kat");
    if (kat) {
      for (var pi = 0; pi < panels.length; pi++) {
        if (panels[pi].getAttribute("data-kat") === kat) { startStep = pi; break; }
      }
    }
  } catch (e) {}
  show(startStep, false);
  render();
})();
