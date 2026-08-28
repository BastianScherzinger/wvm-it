/* Umbau 2026-08 (docs/UMBAU-PLAN.md, U2.4 / U2.6 / U4.8)
   Drei kleine Dinge, alle als Zugabe gedacht: ohne JavaScript funktioniert die Seite
   vollständig weiter (Formulare senden normal, die Reiter zeigen den ersten Inhalt,
   der Rückruf-Dialog fällt auf den Kontaktabschnitt zurück).
   Animiert wird nichts, was der Nutzer nicht angestoßen hat. */
(function () {
  "use strict";

  var T = (window.I18N && window.I18N.lb) || {};

  /* ── 1. Hero-Werkzeug: Reiter „Gratis-Seite" / „Richtpreis" ──────────────── */
  (function tabs() {
    var tabList = document.querySelectorAll(".tool-tab");
    if (!tabList.length) return;

    function zeige(aktiv) {
      tabList.forEach(function (tab) {
        var an = tab === aktiv;
        tab.classList.toggle("is-active", an);
        tab.setAttribute("aria-selected", an ? "true" : "false");
        tab.tabIndex = an ? 0 : -1;
        var panel = document.getElementById(tab.getAttribute("aria-controls"));
        if (panel) panel.hidden = !an;
      });
    }

    tabList.forEach(function (tab, i) {
      tab.addEventListener("click", function () { zeige(tab); });
      tab.addEventListener("keydown", function (e) {
        var richtung = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
        if (!richtung) return;
        e.preventDefault();
        var next = tabList[(i + richtung + tabList.length) % tabList.length];
        next.focus();
        zeige(next);
      });
    });
  })();

  /* ── 2. Richtpreis-Kacheln: springen in den Konfigurator und öffnen die Gruppe ── */
  (function picks() {
    document.querySelectorAll(".tool-pick[data-gruppe]").forEach(function (pick) {
      pick.addEventListener("click", function () {
        var gruppe = pick.getAttribute("data-gruppe");
        // Der Konfigurator hat je Gruppe einen Kopf-Button; ist er da, klappen wir ihn auf.
        var ziel = document.querySelector('[data-rb-group="' + gruppe + '"]');
        if (ziel && ziel.getAttribute("aria-expanded") === "false") ziel.click();
      });
    });
  })();

  /* ── 3. Kurzanfragen ohne Seitenwechsel abschicken ───────────────────────── */
  function istKontaktOk(wert) {
    var mail = wert.indexOf("@") > 0 && wert.indexOf(" ") === -1 && wert.lastIndexOf(".") > wert.indexOf("@");
    var ziffern = (wert.match(/\d/g) || []).length;
    return mail || ziffern >= 7;
  }

  document.querySelectorAll("form[data-anfrage]").forEach(function (form) {
    var fehler = form.querySelector(".lb-err");
    var knopf = form.querySelector(".lb-submit");
    // Beschriftung als Knoten-Kopie sichern (Text + Pfeil-SVG), nicht als HTML-String.
    var beschriftung = knopf ? knopf.cloneNode(true) : null;

    function knopfZurueck() {
      if (!knopf || !beschriftung) return;
      knopf.disabled = false;
      knopf.replaceChildren.apply(knopf, Array.prototype.slice.call(beschriftung.cloneNode(true).childNodes));
    }

    function zeigeFehler(text) {
      if (!fehler) return;
      fehler.textContent = text;
      fehler.hidden = false;
    }

    form.addEventListener("submit", function (e) {
      var kontakt = form.querySelector('[name="kontakt"]');
      if (kontakt && !istKontaktOk(kontakt.value.trim())) {
        e.preventDefault();
        zeigeFehler(T.err_kontakt || "Bitte E-Mail oder Telefonnummer eintragen.");
        kontakt.focus();
        return;
      }
      if (!window.fetch) return;                 // ohne fetch: normales POST
      e.preventDefault();
      if (fehler) fehler.hidden = true;
      if (knopf) { knopf.disabled = true; knopf.textContent = T.sending || "Wird gesendet …"; }

      fetch(form.action, {
        method: "POST",
        headers: { "X-Requested-With": "fetch" },
        body: new FormData(form),
        credentials: "same-origin"
      })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (data) {
          if (!data || !data.ok) throw new Error((data && data.error) || "fehler");
          var behaelter = form.parentElement;
          var fertig = behaelter && behaelter.querySelector(".lb-done");
          form.hidden = true;
          if (fertig) fertig.hidden = false;
        })
        .catch(function (err) {
          var meldung = String(err && err.message) === "kontakt"
            ? (T.err_kontakt || "Bitte E-Mail oder Telefonnummer eintragen.")
            : (T.err_allg || "Das hat nicht geklappt. Bitte per WhatsApp oder Telefon melden.");
          zeigeFehler(meldung);
        })
        .then(knopfZurueck);
    });
  });

  /* ── 4. Rückruf-Dialog ───────────────────────────────────────────────────── */
  (function rueckruf() {
    var dlg = document.getElementById("rueckrufDlg");
    if (!dlg || typeof dlg.showModal !== "function") return;   // sonst bleibt der Link zum Kontakt

    document.querySelectorAll("[data-rueckruf]").forEach(function (ausloeser) {
      ausloeser.addEventListener("click", function () {
        dlg.showModal();
        var erstes = dlg.querySelector('input:not([type="hidden"]):not([tabindex="-1"])');
        if (erstes) erstes.focus();
      });
    });
    dlg.querySelectorAll("[data-rr-close]").forEach(function (knopf) {
      knopf.addEventListener("click", function () { dlg.close(); });
    });
    // Klick auf den Hintergrund schließt ebenfalls.
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
  })();
})();
