/* ============================================================================
   WVM-IT — Interaktionen
   1) Scroll-Scrubbing des Higgsfield-Server-Videos (Apple-Scrollytelling)
   2) Reveal-on-Scroll  3) Nav-Scroll-Status  4) Count-up-Kennzahlen
   Alles transform/opacity-basiert, pausiert ausserhalb des Viewports,
   respektiert prefers-reduced-motion.
   ========================================================================== */
(function () {
  "use strict";
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ── 1) SCROLL-VIDEO-SCRUBBING ──────────────────────────────────────────
     Das MP4 wird nicht abgespielt, sondern „gescrubbt": die Scroll-Position
     in der hohen .scrolly-Sektion wird auf video.currentTime abgebildet. Der
     Wert wird per Lerp geglättet → butterweich. Die Text-Schritte (Hosting,
     Performance, Sicherheit) blenden passend zum Fortschritt ein. */
  const scrolly = document.querySelector("[data-scrolly]");
  const video = document.getElementById("scrollyVideo");
  const bar = document.getElementById("scrollyBar");
  if (scrolly && video) {
    const steps = Array.prototype.slice.call(scrolly.querySelectorAll(".scrolly-step"));
    let duration = 0, ready = false, target = 0, current = 0, active = false, looping = false;

    video.addEventListener("loadedmetadata", function () { duration = video.duration || 0; ready = true; });
    // Safari/iOS: kurz anspielen + pausieren, damit Frame-genaues Seeking erlaubt ist.
    video.addEventListener("canplay", function prime() {
      const p = video.play();
      if (p && p.then) p.then(function () { video.pause(); }).catch(function () {});
      video.removeEventListener("canplay", prime);
    });

    function progress() {
      const rect = scrolly.getBoundingClientRect();
      const total = scrolly.offsetHeight - window.innerHeight;
      return total > 0 ? Math.min(1, Math.max(0, -rect.top / total)) : 0;
    }
    function render() {
      const p = progress();
      if (ready && duration) {
        target = p * (duration - 0.06);
        current += (target - current) * 0.16;            // Lerp → weiches Scrubbing
        if (Math.abs(target - current) < 0.004) current = target;
        try { video.currentTime = current; } catch (e) {}
      }
      if (bar) bar.style.transform = "scaleX(" + p.toFixed(4) + ")";
      const idx = Math.min(steps.length - 1, Math.floor(p * steps.length));
      for (let i = 0; i < steps.length; i++) steps[i].classList.toggle("is-active", i === idx);
    }
    function loop() {
      if (!active) { looping = false; return; }
      looping = true; render(); requestAnimationFrame(loop);
    }
    if (reduce) {
      // Kein Scrubbing: Poster bleibt stehen, erster Text sichtbar.
      if (steps[0]) steps[0].classList.add("is-active");
    } else {
      new IntersectionObserver(function (en) {
        active = en[0].isIntersecting;
        if (active && !looping) requestAnimationFrame(loop);
      }, { threshold: 0 }).observe(scrolly);
      video.load();
    }
  }

  /* ── 2) REVEAL ON SCROLL ───────────────────────────────────────────────── */
  const reveals = document.querySelectorAll("[data-reveal]");
  if (reveals.length) {
    if (reduce) {
      reveals.forEach((el) => el.classList.add("in"));
    } else {
      const io = new IntersectionObserver((entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
        });
      }, { threshold: 0.14, rootMargin: "0px 0px -8% 0px" });
      reveals.forEach((el) => io.observe(el));
    }
  }

  /* ── 3) NAV-SCROLL-STATUS ──────────────────────────────────────────────── */
  const nav = document.getElementById("nav");
  if (nav) {
    const onScrollNav = () => nav.classList.toggle("scrolled", window.scrollY > 12);
    window.addEventListener("scroll", onScrollNav, { passive: true });
    onScrollNav();
  }

  /* ── 4) COUNT-UP-KENNZAHLEN ────────────────────────────────────────────── */
  const counters = document.querySelectorAll("[data-count]");
  if (counters.length && !reduce) {
    const animate = (el) => {
      const end = parseFloat(el.getAttribute("data-count")) || 0;
      const suffix = el.getAttribute("data-suffix") || "";
      const dur = 1200; const start = performance.now();
      const tick = (now) => {
        const t = Math.min(1, (now - start) / dur);
        const eased = 1 - Math.pow(1 - t, 3);
        el.textContent = Math.round(end * eased) + suffix;
        if (t < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    };
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) { animate(e.target); io.unobserve(e.target); }
      });
    }, { threshold: 0.6 });
    counters.forEach((el) => io.observe(el));
  } else {
    counters.forEach((el) => { el.textContent = el.getAttribute("data-count") + (el.getAttribute("data-suffix") || ""); });
  }
})();
