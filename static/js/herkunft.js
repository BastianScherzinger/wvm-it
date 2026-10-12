/* Herkunft einer Anfrage: utm_source/-medium/-campaign/-content aus der Adresse und
   der Host der verweisenden Seite werden beim Absenden als versteckte Felder
   mitgeschickt (nur an die Anfrage, die der Besucher selbst abschickt).
   Bewusst OHNE Speicherung: kein Cookie, kein Web-Speicher des Browsers, keine
   Kennung. Wer vor dem Absenden auf eine andere Seite weiterklickt, verliert die
   Angabe -- mehr ginge nur mit Speicherung und damit mit Einwilligung.
   Gegenstueck: views._herkunft_utm. */
(function () {
  'use strict';
  try {
    var q = new URLSearchParams(location.search);
    var w = {};
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content'].forEach(function (k) {
      var v = (q.get(k) || '').trim().slice(0, 40);
      if (v) w[k] = v;
    });
    if (document.referrer) {
      var r = new URL(document.referrer);
      if (r.host && r.host !== location.host) w.ref_host = r.hostname.slice(0, 60);
    }
    if (!Object.keys(w).length) return;
    document.querySelectorAll('form[method="post" i]').forEach(function (f) {
      if (!f.querySelector('input[name="website"]')) return;   // nur Anfrageformulare
      Object.keys(w).forEach(function (k) {
        var i = document.createElement('input');
        i.type = 'hidden'; i.name = k; i.value = w[k];
        f.appendChild(i);
      });
    });
  } catch (x) { /* Herkunft darf nie stoeren */ }
})();
