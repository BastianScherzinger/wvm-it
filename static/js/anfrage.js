/* ============================================================================
   WVM-IT ,  Anfrage-Bogen (Detail-Formular nach Newsletter-Bestätigung) als Wizard
   - Ein Schritt pro Ansicht (6 Sektionen), Fortschrittsbalken + klickbare Schritte,
     Weiter/Zurück, sanfte Übergänge (nutzt dieselben .wz-*-Klassen wie der
     Angebots-Konfigurator, siehe angebot.js).
   - Autosave: alle Eingaben (außer Datei-/versteckte Felder) landen live in
     localStorage und werden bei Rückkehr auf die Seite automatisch wiederhergestellt;
     nach erfolgreichem Absenden wird der Entwurf gelöscht.
   - Progressive Enhancement: ohne JS bleiben alle Sektionen als lange, funktionierende
     Ein-Seiten-Form sichtbar (kein Wizard-Zustand wird gesetzt, das Formular sendet
     ganz normal per POST ab). Der Cloudinary-Bild-Upload (separates Inline-Script im
     Template) bleibt davon unberührt.
   ========================================================================== */
(function () {
  "use strict";
  var form = document.getElementById("anfrageForm");
  if (!form) return;

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var I = (window.I18N && window.I18N.af) || {};
  var T_STEP = I.stepWord || "Schritt";
  var T_OF = I.ofWord || "von";
  var T_RESTORED = I.restored || "";

  // ── Wizard-Modus aktivieren ──────────────────────────────────────────────
  form.classList.add("wz-on");
  var panels = Array.prototype.slice.call(form.querySelectorAll(".af-section"));
  var steps = Array.prototype.slice.call(form.querySelectorAll(".wz-step"));
  var bar = document.getElementById("afBar");
  var runLabels = Array.prototype.slice.call(form.querySelectorAll("[data-run-count]"));
  var last = panels.length - 1;
  var current = 0;

  function setRunLabels() {
    var label = T_STEP + " " + (current + 1) + " " + T_OF + " " + (last + 1);
    runLabels.forEach(function (el) { el.textContent = label; });
  }

  function scrollToWizard() {
    if (!form.scrollIntoView) return;
    form.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
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
    setRunLabels();
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

  show(0, false);

  // ── Autosave (localStorage) ──────────────────────────────────────────────
  var STORAGE_KEY = "wvmAnfrageDraft";
  var restoreNotice = document.getElementById("afRestore");

  function trackedFields() {
    return Array.prototype.slice.call(form.querySelectorAll("input,textarea,select")).filter(function (el) {
      return el.name && el.type !== "hidden" && el.type !== "file" && el.type !== "submit";
    });
  }

  function saveDraft() {
    var data = {};
    trackedFields().forEach(function (el) {
      if (el.type === "checkbox" || el.type === "radio") {
        if (el.checked) { (data[el.name] = data[el.name] || []).push(el.value); }
      } else {
        data[el.name] = el.value;
      }
    });
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(data)); } catch (e) { /* Storage evtl. gesperrt (privat/Quota) */ }
  }

  function restoreDraft() {
    var raw;
    try { raw = localStorage.getItem(STORAGE_KEY); } catch (e) { raw = null; }
    if (!raw) return;
    var data;
    try { data = JSON.parse(raw); } catch (e) { return; }
    if (!data || typeof data !== "object") return;
    var restoredAny = false;
    trackedFields().forEach(function (el) {
      if (!(el.name in data)) return;
      if (el.type === "checkbox" || el.type === "radio") {
        var vals = data[el.name];
        if (!Array.isArray(vals)) vals = [vals];
        var was = el.checked;
        el.checked = vals.indexOf(el.value) !== -1;
        if (el.checked !== was) restoredAny = true;
      } else if (data[el.name]) {
        el.value = data[el.name];
        restoredAny = true;
      }
    });
    if (restoredAny && restoreNotice) {
      restoreNotice.hidden = false;
      if (T_RESTORED) restoreNotice.querySelector("span").textContent = T_RESTORED;
    }
  }

  restoreDraft();

  var saveTimer = null;
  form.addEventListener("input", function () {
    if (saveTimer) clearTimeout(saveTimer);
    saveTimer = setTimeout(saveDraft, 300);
  });
  form.addEventListener("change", saveDraft);

  // Nach echtem Absenden (normaler POST, keine AJAX-Umleitung) den Entwurf löschen ,
  // läuft synchron vor der Navigation.
  form.addEventListener("submit", function () {
    try { localStorage.removeItem(STORAGE_KEY); } catch (e) {}
  });
})();
