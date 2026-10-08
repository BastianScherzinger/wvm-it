/* Zwei-Klick-Karte: das iframe entsteht erst nach dem Klick (kein Kontakt zu Google
   vorher, Datenschutz). Nur Adressen, die mit https://www.google.com/maps beginnen. */
(function () {
  'use strict';
  var knopf = document.querySelector('[data-karte-laden]');
  if (!knopf) return;
  knopf.addEventListener('click', function () {
    var src = knopf.getAttribute('data-src') || '';
    if (src.indexOf('https://www.google.com/maps') !== 0) return;
    var box = knopf.closest('[data-karte]');
    var platz = box && box.querySelector('[data-karte-platzhalter]');
    var f = document.createElement('iframe');
    f.src = src;
    f.title = knopf.getAttribute('data-titel') || 'Karte';
    f.loading = 'lazy';
    f.referrerPolicy = 'strict-origin-when-cross-origin';
    f.setAttribute('allowfullscreen', '');
    f.className = 'karte-frame';
    if (platz) platz.hidden = true;
    box.appendChild(f);
  });
})();
