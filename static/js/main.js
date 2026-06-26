/* ============================================================================
   WVM-IT ,  Interaktionen
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
  const scrollies = [];
  function initScrolly(scrolly) {
    const video = scrolly.querySelector(".scrolly-video");
    const bar = scrolly.querySelector(".scrolly-bar");
    if (!video) return;
    const steps = Array.prototype.slice.call(scrolly.querySelectorAll(".scrolly-step"));
    const ctx = { scrolly, video, bar, steps, duration: 0, ready: false, current: 0 };
    video.addEventListener("loadedmetadata", function () { ctx.duration = video.duration || 0; ctx.ready = true; });
    // Safari/iOS: kurz anspielen + pausieren, damit Frame-genaues Seeking erlaubt ist.
    video.addEventListener("canplay", function prime() {
      const p = video.play();
      if (p && p.then) p.then(function () { video.pause(); }).catch(function () {});
      video.removeEventListener("canplay", prime);
    });
    if (reduce) { if (steps[0]) steps[0].classList.add("is-active"); return; }
    video.load();
    scrollies.push(ctx);
  }
  function renderScrolly(ctx) {
    const rect = ctx.scrolly.getBoundingClientRect();
    // Nur rechnen, wenn die Sektion im oder am Viewport ist.
    if (rect.bottom < -50 || rect.top > window.innerHeight + 50) return;
    const total = ctx.scrolly.offsetHeight - window.innerHeight;
    const p = total > 0 ? Math.min(1, Math.max(0, -rect.top / total)) : 0;
    if (ctx.ready && ctx.duration) {
      const target = p * (ctx.duration - 0.06);
      ctx.current += (target - ctx.current) * 0.16;        // Lerp -> weiches Scrubbing
      if (Math.abs(target - ctx.current) < 0.004) ctx.current = target;
      try { ctx.video.currentTime = ctx.current; } catch (e) {}
    }
    if (ctx.bar) ctx.bar.style.transform = "scaleX(" + p.toFixed(4) + ")";
    const idx = Math.min(ctx.steps.length - 1, Math.floor(p * ctx.steps.length));
    for (let i = 0; i < ctx.steps.length; i++) ctx.steps[i].classList.toggle("is-active", i === idx);
  }
  document.querySelectorAll("[data-scrolly]").forEach(initScrolly);
  if (scrollies.length) {
    (function tick() { for (let i = 0; i < scrollies.length; i++) renderScrolly(scrollies[i]); requestAnimationFrame(tick); })();
  }

  /* ── 1b) SPLINE-ROBOTER (folgt der Maus) ────────────────────────────────
     3D-Szene per <spline-viewer> nachladen. Ohne WebGL oder bei reduced-motion
     bleibt der freigestellte Roboter (robot-fallback) stehen. */
  (function initRobot() {
    const stage = document.getElementById("robotStage");
    if (!stage) return;
    const hasWebGL = (function () {
      try { const c = document.createElement("canvas");
        return !!(window.WebGLRenderingContext && (c.getContext("webgl") || c.getContext("experimental-webgl")));
      } catch (e) { return false; }
    })();
    const isMobile = window.matchMedia("(max-width: 767px)").matches;
    if (reduce || !hasWebGL || isMobile) return;           // Fallback-Bild (Cutout) bleibt sichtbar
    const canvas = document.getElementById("robotCanvas");
    const loader = document.getElementById("robotLoader");
    const url = stage.getAttribute("data-spline");

    const runtime = document.createElement("script");
    runtime.type = "module";
    runtime.src = "https://unpkg.com/@splinetool/viewer@1.12.97/build/spline-viewer.js";
    document.head.appendChild(runtime);

    const viewer = document.createElement("spline-viewer");
    viewer.setAttribute("url", url);
    viewer.style.cssText = "width:100%;height:100%;display:block;background:transparent";
    if (isMobile) viewer.style.pointerEvents = "none"; // Mobile: Scrollen nicht blockieren
    canvas.appendChild(viewer);

    let settled = false;
    const ready = function () {
      if (settled) return; settled = true;
      stage.classList.add("spline-on");                   // blendet Fallback aus, Canvas ein
      if (loader) loader.classList.add("hide");
    };
    // "Made with Spline"-Logo aus dem Shadow-DOM entfernen.
    const killLogo = function (root) { const l = root && root.querySelector('#logo, a[href*="spline.design"]'); if (l) l.remove(); };
    viewer.addEventListener("load", function () { ready(); if (viewer.shadowRoot) killLogo(viewer.shadowRoot); });
    const poll = setInterval(function () {
      const sr = viewer.shadowRoot;
      if (sr) { killLogo(sr); if (sr.querySelector("canvas")) { clearInterval(poll); setTimeout(ready, 300); } }
    }, 150);
    setTimeout(function () { clearInterval(poll); ready(); }, 7000); // Sicherheitsnetz
  })();

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
  const fmt = (el, n) => (el.getAttribute("data-prefix") || "") + n + (el.getAttribute("data-suffix") || "");
  if (counters.length && !reduce) {
    const animate = (el) => {
      const end = parseFloat(el.getAttribute("data-count")) || 0;
      const dur = 1200; const start = performance.now();
      const tick = (now) => {
        const t = Math.min(1, (now - start) / dur);
        const eased = 1 - Math.pow(1 - t, 3);
        el.textContent = fmt(el, Math.round(end * eased));
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
    counters.forEach((el) => { el.textContent = fmt(el, el.getAttribute("data-count")); });
  }

  /* ── 5) SPOTLIGHT ,  Mouse-Follow-Highlight auf [data-spot]-Karten ───────── */
  if (!reduce && window.matchMedia("(pointer:fine)").matches) {
    let raf = 0, pending = null;
    const move = (el, e) => {
      const r = el.getBoundingClientRect();
      pending = () => {
        el.style.setProperty("--mx", (e.clientX - r.left) + "px");
        el.style.setProperty("--my", (e.clientY - r.top) + "px");
      };
      if (!raf) raf = requestAnimationFrame(() => { pending && pending(); raf = 0; });
    };
    document.querySelectorAll("[data-spot]").forEach((el) => {
      el.addEventListener("pointermove", (e) => move(el, e), { passive: true });
    });
  }

  /* ── 6) MAGNETIC ,  Buttons ziehen sanft zum Cursor ─────────────────────── */
  if (!reduce && window.matchMedia("(pointer:fine)").matches) {
    document.querySelectorAll(".btn-magnetic").forEach((btn) => {
      let raf = 0;
      const onMove = (e) => {
        const r = btn.getBoundingClientRect();
        const x = (e.clientX - (r.left + r.width / 2)) * 0.28;
        const y = (e.clientY - (r.top + r.height / 2)) * 0.4;
        if (!raf) raf = requestAnimationFrame(() => { btn.style.transform = `translate(${x}px,${y}px)`; raf = 0; });
      };
      btn.addEventListener("pointermove", onMove, { passive: true });
      btn.addEventListener("pointerleave", () => { btn.style.transform = ""; });
    });
  }
})();
