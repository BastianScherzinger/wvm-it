/* Zaehlt Klicks auf Anruf-, WhatsApp- und E-Mail-Links -- als Summe je Seite.
   Keine IP, kein Cookie, keine Kennung (siehe landing/messung.py, landing/klicks.py).
   sendBeacon ueberlebt den Seitenwechsel, den ein tel:-/mailto:-Link ausloest. */
(function () {
  'use strict';
  if (!navigator.sendBeacon) return;
  function art(href) {
    if (!href) return '';
    var h = href.toLowerCase();
    if (h.indexOf('tel:') === 0) return 'tel';
    if (h.indexOf('mailto:') === 0) return 'mail';
    if (h.indexOf('https://wa.me/') === 0 || h.indexOf('https://api.whatsapp.com/') === 0) return 'wa';
    return '';
  }
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var k = art(a.getAttribute('href'));
    if (!k) return;
    try {
      var d = new URLSearchParams();
      d.set('art', k);
      d.set('pfad', location.pathname);
      navigator.sendBeacon('/m/klick/', d);
    } catch (x) { /* Messung darf nie stoeren */ }
  }, true);
})();
