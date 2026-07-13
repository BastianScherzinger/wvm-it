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
    if (steps[0]) steps[0].classList.add("is-active");
    if (reduce) return;                                   // Reduced-Motion: nur Poster + Text
    // Mobil: KEIN Scroll-Scrubbing (ruckelt). Stattdessen sanfter, leiser Autoplay-Loop,
    // der nur läuft, während die Sektion sichtbar ist -> flüssiges Scrollen, hochwertige Optik.
    if (window.matchMedia("(max-width: 980px)").matches) {
      video.loop = true; video.muted = true; video.setAttribute("playsinline", "");
      new IntersectionObserver(function (en) {
        if (en[0].isIntersecting) { video.preload = "auto"; const p = video.play(); if (p && p.catch) p.catch(function () {}); }
        else { try { video.pause(); } catch (e) {} }
      }, { threshold: 0.25 }).observe(scrolly);
      return;
    }
    video.addEventListener("loadedmetadata", function () { ctx.duration = video.duration || 0; });
    // Frame-genaues Seeking erst freigeben, NACHDEM das Video durch play+pause aktiviert
    // wurde. Sonst ignoriert der Browser gesetzte currentTime-Werte (Seek-Sperre).
    video.addEventListener("canplay", function prime() {
      video.removeEventListener("canplay", prime);
      const done = function () { try { video.pause(); } catch (e) {} ctx.duration = video.duration || 0; ctx.ready = true; };
      const p = video.play();
      if (p && p.then) p.then(done).catch(done); else done();
    });
    // Lazy: Video erst voll laden, wenn die Sektion näher kommt (schnellerer Erst-Load,
    // keine Decoder-Konkurrenz). Einmaliger load()-Aufruf, danach Observer trennen.
    new IntersectionObserver(function (en, obs) {
      if (en[0].isIntersecting) { video.preload = "auto"; video.load(); obs.disconnect(); }
    }, { rootMargin: "1200px 0px" }).observe(scrolly);
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

    // Klickbarer Assistent (wie RTC): Sprechblase + Hinweis. Funktioniert immer,
    // egal ob der 3D-Roboter oder der Fallback-Cutout angezeigt wird.
    let viewer = null;
    (function enableRobotChat() {
      const bubble = document.getElementById("robotBubble");
      const hint = document.getElementById("robotHint");
      const tap = document.getElementById("robotTap");
      if (!bubble) return;
      // Sprechblasen-Texte kommen lokalisiert aus window.I18N (Fallback: Deutsch).
      const msgs = (window.I18N && window.I18N.robot && window.I18N.robot.length) ? window.I18N.robot : [
        "Hi! Schön, dass du da bist.",
        "Wir bauen Webseiten, Hosting, KI und SEO. Alles aus einer Hand.",
        "Schon ab 350 Euro hast du deine eigene Webseite.",
        "Tipp: Hol dir ein unverbindliches Angebot in 24 Stunden.",
        "Bereit? Klick auf Projekt anfragen, wir melden uns schnell.",
      ];
      let idx = -1, hideT, started = false;
      function say() {
        started = true;
        idx = (idx + 1) % msgs.length;
        bubble.textContent = msgs[idx];
        bubble.classList.add("show");
        if (hint) hint.classList.remove("show");
        clearTimeout(hideT);
        hideT = setTimeout(function () { bubble.classList.remove("show"); }, 4400);
      }
      stage.addEventListener("click", say);
      stage.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); say(); } });
      if (hint) hint.addEventListener("click", function (e) { e.stopPropagation(); say(); });
      if (tap) tap.addEventListener("click", function (e) { e.stopPropagation(); say(); });
      stage.classList.add("chat-on");
      if (hint && !reduce) setTimeout(function () {
        if (!started) { hint.classList.add("show"); setTimeout(function () { if (!started) hint.classList.remove("show"); }, 6000); }
      }, 1800);
    })();

    const hasWebGL = (function () {
      try { const c = document.createElement("canvas");
        return !!(window.WebGLRenderingContext && (c.getContext("webgl") || c.getContext("experimental-webgl")));
      } catch (e) { return false; }
    })();
    // 3D-Roboter auch auf Mobile laden (WebGL vorausgesetzt). Faellt die Szene aus,
    // bleibt der selbst gehostete Cutout stehen (siehe Sicherheitsnetz unten).
    if (reduce || !hasWebGL) return;                        // Fallback-Bild (Cutout) bleibt sichtbar
    const canvas = document.getElementById("robotCanvas");
    const loader = document.getElementById("robotLoader");
    const url = stage.getAttribute("data-spline");

    const loadSpline = function () {
    const runtime = document.createElement("script");
    runtime.type = "module";
    runtime.src = "https://unpkg.com/@splinetool/viewer@1.12.97/build/spline-viewer.js";
    document.head.appendChild(runtime);

    viewer = document.createElement("spline-viewer");
    viewer.setAttribute("url", url);
    viewer.style.cssText = "width:100%;height:100%;display:block;background:transparent";
    canvas.appendChild(viewer);
    viewer.addEventListener("click", function () { stage.click(); }); // Klick auf 3D-Roboter -> Sprechblase

    let settled = false;
    const hasCanvas = function () { const sr = viewer.shadowRoot; return !!(sr && sr.querySelector("canvas")); };
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
    // Sicherheitsnetz: nur einblenden, wenn Spline wirklich ein Canvas gerendert hat.
    // Sonst (z. B. schwaches Mobilgeraet) Fallback-Cutout sichtbar lassen, nur Loader ausblenden.
    setTimeout(function () {
      clearInterval(poll);
      if (hasCanvas()) ready();
      else if (loader) loader.classList.add("hide");
    }, 7000);
    };
    // Externe 3D-Inhalte (Spline via unpkg/prod.spline.design) NUR mit Cookie-Einwilligung
    // laden (DSGVO) — ohne Zustimmung bleibt der selbst gehostete Fallback-Cutout sichtbar.
    let started = false;
    const startSpline = function () {
      if (started) return; started = true;
      (window.requestAnimationFrame || function (f) { return setTimeout(f, 16); })(loadSpline);
    };
    const consentAll = function () {
      const m = document.cookie.match(/(?:^|;\s*)wvm_consent=([^;]+)/);
      return !!m && m[1] === "all";
    };
    if (consentAll()) startSpline();
    else window.addEventListener("wvm:consent", function (e) {
      if (!e || e.detail === "all") startSpline();
    }, { once: true });
  })();

  /* ── 2) REVEAL ON SCROLL ───────────────────────────────────────────────── */
  const reveals = document.querySelectorAll("[data-reveal]");
  if (reveals.length) {
    if (reduce) {
      reveals.forEach((el) => el.classList.add("in"));
    } else {
      // sanfte Staffelung: benachbarte data-reveal-Geschwister kaskadieren (max 260ms)
      reveals.forEach((el) => {
        const kids = el.parentNode ? el.parentNode.children : [];
        const sibs = Array.prototype.filter.call(kids, (c) => c.hasAttribute && c.hasAttribute("data-reveal"));
        const i = sibs.indexOf(el);
        if (i > 0) el.style.transitionDelay = Math.min(i * 70, 260) + "ms";
      });
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
    // Mobile-Menü (Burger) öffnen/schließen
    const burger = document.getElementById("navBurger");
    if (burger) {
      const close = function () { nav.classList.remove("open"); burger.setAttribute("aria-expanded", "false"); };
      burger.addEventListener("click", function () {
        const open = nav.classList.toggle("open");
        burger.setAttribute("aria-expanded", open ? "true" : "false");
      });
      nav.querySelectorAll(".nav-menu a").forEach(function (a) { a.addEventListener("click", close); });
      document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
    }
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
