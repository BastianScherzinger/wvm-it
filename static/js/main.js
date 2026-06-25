/* ============================================================================
   WVM-IT — Interaktionen
   1) Scrollgesteuerte Hero-Canvas-Animation ("Aus einer Idee wird Infrastruktur")
   2) Reveal-on-Scroll  3) Nav-Scroll-Status  4) Count-up-Kennzahlen
   Alles transform/opacity-basiert, pausiert ausserhalb des Viewports,
   respektiert prefers-reduced-motion.
   ========================================================================== */
(function () {
  "use strict";
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ── 1) HERO-CANVAS ─────────────────────────────────────────────────────
     Ein Netz aus Knoten driftet sanft. Beim Scrollen durch den Hero
     "verdichtet" sich das Netz (Linien werden sichtbar) und die Kamera fährt
     leicht hinein (Zoom um das Zentrum) — eine dezente Dolly-Bewegung. */
  const canvas = document.getElementById("heroCanvas");
  const hero = document.querySelector(".hero");
  if (canvas && hero && !reduce) {
    const ctx = canvas.getContext("2d", { alpha: true });
    const ACCENT = getComputedStyle(document.documentElement).getPropertyValue("--accent").trim() || "#6d5efc";
    const ACCENT2 = getComputedStyle(document.documentElement).getPropertyValue("--accent2").trim() || "#22d3ee";
    let dpr = Math.min(window.devicePixelRatio || 1, 2);
    let W = 0, H = 0, nodes = [], running = true, progress = 0;
    const mouse = { x: 0.5, y: 0.5, tx: 0.5, ty: 0.5 };

    function rgb(hex) {
      const h = hex.replace("#", "");
      return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
    }
    const cA = rgb(ACCENT), cB = rgb(ACCENT2);

    function resize() {
      const r = hero.getBoundingClientRect();
      W = r.width; H = r.height;
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = W * dpr; canvas.height = H * dpr;
      canvas.style.width = W + "px"; canvas.style.height = H + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      // Knotenzahl an die Fläche koppeln (Performance auf Mobile schonen).
      const target = Math.round(Math.min(120, Math.max(34, (W * H) / 14000)));
      nodes = [];
      for (let i = 0; i < target; i++) {
        nodes.push({
          x: Math.random() * W, y: Math.random() * H,
          vx: (Math.random() - 0.5) * 0.16, vy: (Math.random() - 0.5) * 0.16,
          z: 0.3 + Math.random() * 0.7, // Tiefe → Grösse & Parallax
        });
      }
    }

    function frame() {
      if (!running) return;
      requestAnimationFrame(frame);
      ctx.clearRect(0, 0, W, H);
      // Sanfte Maus-Parallax (Dämpfung).
      mouse.x += (mouse.tx - mouse.x) * 0.05;
      mouse.y += (mouse.ty - mouse.y) * 0.05;
      const cx = W / 2, cy = H * 0.42;
      const zoom = 1 + progress * 0.28;                 // Kamera-Dolly beim Scrollen
      const px = (mouse.x - 0.5) * 26, py = (mouse.y - 0.5) * 20;
      const linkBoost = 0.25 + progress * 0.75;          // Netz "verdichtet" sich
      const fade = 1 - Math.pow(progress, 2) * 0.7;      // blendet zum Ende sanft aus
      const maxD = Math.min(W, H) * (0.16 + progress * 0.05);

      // Position im Bildraum (mit Zoom um Zentrum + Parallax nach Tiefe).
      const P = nodes.map((n) => {
        n.x += n.vx; n.y += n.vy;
        if (n.x < -20) n.x = W + 20; if (n.x > W + 20) n.x = -20;
        if (n.y < -20) n.y = H + 20; if (n.y > H + 20) n.y = -20;
        const sx = cx + (n.x - cx) * zoom + px * n.z;
        const sy = cy + (n.y - cy) * zoom + py * n.z;
        return { x: sx, y: sy, z: n.z };
      });

      // Verbindungen.
      ctx.lineWidth = 1;
      for (let i = 0; i < P.length; i++) {
        for (let j = i + 1; j < P.length; j++) {
          const dx = P[i].x - P[j].x, dy = P[i].y - P[j].y;
          const d = Math.hypot(dx, dy);
          if (d < maxD) {
            const t = 1 - d / maxD;
            const m = (P[i].z + P[j].z) / 2;
            const r = Math.round(cA[0] + (cB[0] - cA[0]) * m);
            const g = Math.round(cA[1] + (cB[1] - cA[1]) * m);
            const b = Math.round(cA[2] + (cB[2] - cA[2]) * m);
            ctx.strokeStyle = `rgba(${r},${g},${b},${(t * 0.5 * linkBoost * fade).toFixed(3)})`;
            ctx.beginPath(); ctx.moveTo(P[i].x, P[i].y); ctx.lineTo(P[j].x, P[j].y); ctx.stroke();
          }
        }
      }
      // Knotenpunkte.
      for (let i = 0; i < P.length; i++) {
        const s = (0.8 + P[i].z * 1.8);
        ctx.fillStyle = `rgba(${cB[0]},${cB[1]},${cB[2]},${(0.5 * fade).toFixed(3)})`;
        ctx.beginPath(); ctx.arc(P[i].x, P[i].y, s, 0, Math.PI * 2); ctx.fill();
      }
      // Zentraler "Idee"-Kern mit Glow.
      const pulse = 0.5 + 0.5 * Math.sin(Date.now() / 900);
      const gx = cx + px * 0.4, gy = cy + py * 0.4;
      const grad = ctx.createRadialGradient(gx, gy, 0, gx, gy, 120 + progress * 80);
      grad.addColorStop(0, `rgba(${cA[0]},${cA[1]},${cA[2]},${(0.45 * fade * (0.7 + pulse * 0.3)).toFixed(3)})`);
      grad.addColorStop(1, "rgba(0,0,0,0)");
      ctx.fillStyle = grad;
      ctx.fillRect(gx - 200, gy - 200, 400, 400);
      ctx.fillStyle = `rgba(255,255,255,${(0.85 * fade).toFixed(3)})`;
      ctx.beginPath(); ctx.arc(gx, gy, 2.6 + pulse * 1.4, 0, Math.PI * 2); ctx.fill();
    }

    function onScroll() {
      const r = hero.getBoundingClientRect();
      // 0 oben im Bild → 1 wenn der Hero gerade vollständig hochgescrollt ist.
      progress = Math.min(1, Math.max(0, -r.top / (r.height || 1)));
    }
    window.addEventListener("mousemove", (e) => {
      mouse.tx = e.clientX / window.innerWidth; mouse.ty = e.clientY / window.innerHeight;
    }, { passive: true });
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", resize);
    // Animation nur laufen lassen, solange der Hero sichtbar ist.
    new IntersectionObserver((en) => {
      running = en[0].isIntersecting;
      if (running) requestAnimationFrame(frame);
    }, { threshold: 0 }).observe(hero);

    resize(); onScroll(); requestAnimationFrame(frame);
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
