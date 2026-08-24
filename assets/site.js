/* =========================================================================
   Chery Antigua — site behaviour
   ========================================================================= */

/* ------------------------------------------------------------------ CONFIG
   WHATSAPP_NUMBER — full international number, digits only (no "+" or spaces).
   LEAD_ENDPOINT   — VMP `ingestWebLead` action. It's Origin-guarded and injects
                     the intake secret server-side (no secret lives here) and
                     creates a general lead in the VMP.
                     NOTE: the VMP must allowlist the chery.ag origin and add a
                     Chery notification inbox before this goes live.
   LEAD_APIKEY     — Supabase's public anon key (safe to expose; RLS-protected).
------------------------------------------------------------------------- */
const CONFIG = {
  WHATSAPP_NUMBER: "12684643345",              // +1 (268) 464-3345
  WHATSAPP_GREETING: "Hi Chery Antigua, I'd like more information about",
  LEAD_ENDPOINT: "https://wqlvyeuqaejbtsrlbpvt.supabase.co/functions/v1/api?action=ingestWebLead",
  LEAD_APIKEY: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndxbHZ5ZXVxYWVqYnRzcmxicHZ0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkxNTAyMTcsImV4cCI6MjA5NDcyNjIxN30.VUpoxQHiEaz9gmZNLLikIcjAfSW5LpqVkRfdrOkKMcM",
};

/* --------------------------------------------------------- header scroll */
const header = document.querySelector(".site-header");
if (header) {
  const onScroll = () => header.classList.toggle("scrolled", window.scrollY > 24);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
}

/* ----------------------------------------------------- hero parallax */
const heroEl = document.querySelector(".hero");
const heroImg = document.querySelector(".hero .hero-bg img");
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
if (heroEl && heroImg && !reducedMotion) {
  let heroH = heroEl.offsetHeight || 900;
  window.addEventListener("resize", () => { heroH = heroEl.offsetHeight || 900; }, { passive: true });
  // Eased parallax: the transform glides toward its target each frame instead of
  // snapping, so the background drifts smoothly. FACTOR 0.18 (subtle) stays within
  // the CSS buffer (135% tall, -24% top) so it can never uncover the hero.
  const FACTOR = 0.18, EASE = 0.12;
  let current = 0, running = false;
  const tick = () => {
    const target = Math.min(window.scrollY, heroH) * FACTOR;
    current += (target - current) * EASE;
    if (Math.abs(target - current) < 0.12) current = target;
    heroImg.style.transform = "translate3d(0," + current.toFixed(2) + "px,0)";
    if (current !== target) { window.requestAnimationFrame(tick); }
    else { running = false; }
  };
  const start = () => { if (!running) { running = true; window.requestAnimationFrame(tick); } };
  window.addEventListener("scroll", start, { passive: true });
  start();
}

/* ---------------------------------------------------------- mobile menu */
const hamburger = document.querySelector(".hamburger");
const navLinks = document.querySelector(".nav-links");
if (hamburger && navLinks) {
  hamburger.addEventListener("click", () => navLinks.classList.toggle("mobile-open"));
  navLinks.querySelectorAll("a").forEach(a =>
    a.addEventListener("click", () => navLinks.classList.remove("mobile-open")));
}

/* ---------------------------------------------------------- WhatsApp */
function waLink(modelName) {
  const msg = CONFIG.WHATSAPP_GREETING + (modelName ? " the Chery " + modelName : " your models") + ".";
  return "https://wa.me/" + CONFIG.WHATSAPP_NUMBER + "?text=" + encodeURIComponent(msg);
}
document.querySelectorAll("[data-wa]").forEach(el => {
  el.setAttribute("href", waLink(el.getAttribute("data-model") || ""));
});

/* --------------------------------------------------------- quote modal */
const overlay = document.getElementById("quoteModal");

function openQuote(model) {
  if (!overlay) return;
  overlay.classList.add("open");
  document.body.style.overflow = "hidden";
  // reset to form view (in case it was left on thank-you)
  const form = overlay.querySelector("form");
  const thanks = overlay.querySelector(".thankyou");
  if (form && thanks) { form.style.display = ""; thanks.classList.remove("show"); }
  // preselect the model if one was passed
  const select = overlay.querySelector('select[name="model"]');
  if (select && model) {
    [...select.options].forEach(o => { if (o.value === model) select.value = model; });
  }
  const first = overlay.querySelector('input[name="firstName"]');
  if (first) setTimeout(() => first.focus(), 60);
}
function closeQuote() {
  if (!overlay) return;
  overlay.classList.remove("open");
  document.body.style.overflow = "";
}

document.querySelectorAll("[data-quote]").forEach(btn =>
  btn.addEventListener("click", e => { e.preventDefault(); openQuote(btn.getAttribute("data-model") || ""); }));

if (overlay) {
  overlay.querySelector(".modal-close")?.addEventListener("click", closeQuote);
  overlay.addEventListener("click", e => { if (e.target === overlay) closeQuote(); });
  document.addEventListener("keydown", e => { if (e.key === "Escape") closeQuote(); });

  /* --------------------------------------------- form submission (UI only)
     The lead is captured in the browser and a thank-you is shown.
     >>> TO CONNECT A BACKEND LATER <<<
     Replace the body of `deliverLead()` below with a fetch() to your
     endpoint / form service (Web3Forms, Formspree, your own API, etc.).
     Everything you need is in the `lead` object.
  --------------------------------------------------------------------- */
  const form = overlay.querySelector("form");
  form?.addEventListener("submit", async e => {
    e.preventDefault();
    const data = new FormData(form);
    const lead = {
      type:      "quote",
      source:    "quote-form",
      firstName: (data.get("firstName") || "").toString().trim(),
      lastName:  (data.get("lastName")  || "").toString().trim(),
      phone:     (data.get("phone")     || "").toString().trim(),
      email:     (data.get("email")     || "").toString().trim(),
      interest:  (data.get("interest")  || "").toString().trim(),
      model:     (data.get("model")     || "").toString().trim(),
      message:   (data.get("message")   || "").toString().trim(),
      company:   (data.get("company")   || "").toString(),   // honeypot — humans leave it empty
      submittedAt: new Date().toISOString(),
    };

    const btn = form.querySelector('button[type="submit"]');
    if (btn) { btn.disabled = true; btn.textContent = "Sending…"; }

    await deliverLead(lead);

    // show thank-you state
    const thanks = overlay.querySelector(".thankyou");
    const nameSpan = overlay.querySelector("[data-thanks-name]");
    if (nameSpan) nameSpan.textContent = lead.firstName || "there";
    form.style.display = "none";
    thanks?.classList.add("show");
    form.reset();
    if (btn) { btn.disabled = false; btn.textContent = "Send My Request →"; }
  });
}

/* ------------------------------------------------------- lead delivery
   Every quote / test-drive / message lead flows through here. It POSTs the
   lead JSON to the VMP endpoint (CONFIG.LEAD_ENDPOINT) and always keeps a
   local backup so nothing is lost. Returns true if the VMP accepted it. */
async function deliverLead(lead) {
  console.log("[Chery lead]", lead);
  try {
    const key = "chery_leads";
    const all = JSON.parse(localStorage.getItem(key) || "[]");
    all.push(lead);
    localStorage.setItem(key, JSON.stringify(all));
  } catch (_) { /* ignore storage errors */ }

  if (CONFIG.LEAD_ENDPOINT) {
    try {
      const headers = { "Content-Type": "application/json" };
      if (CONFIG.LEAD_APIKEY) { headers.apikey = CONFIG.LEAD_APIKEY; headers.Authorization = "Bearer " + CONFIG.LEAD_APIKEY; }
      const res = await fetch(CONFIG.LEAD_ENDPOINT, {
        method: "POST",
        headers,
        body: JSON.stringify(vmpPayload(lead)),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok || (data && data.error)) {
        console.error("[Chery lead] VMP rejected:", data && data.error || res.status);
        return false;
      }
      return true;
    } catch (e) {
      console.error("[Chery lead] VMP delivery failed:", e);
      return false;
    }
  }
  return true;   // no endpoint set yet — kept locally
}

/* Shape a website lead into the VMP `ingestLead` schema
   (firstName/lastName, email, phone, brand, model, notes, channel, source). */
function vmpPayload(lead) {
  const notes = [];
  if (lead.type === "test-drive") {
    notes.push("Test-drive request");
    if (lead.date) notes.push("Preferred date: " + lead.date);
    if (lead.time) notes.push("Preferred time: " + lead.time);
    if (lead.notes) notes.push(lead.notes);
  } else if (lead.type === "quote") {
    if (lead.interest) notes.push(lead.interest);
    if (lead.message) notes.push(lead.message);
  } else if (lead.message) {
    notes.push(lead.message);
  }
  return {
    firstName: lead.firstName || "",
    lastName:  lead.lastName || "",
    email:     lead.email || "",
    phone:     lead.phone || "",
    brand:     "Chery",
    model:     lead.model || "",
    channel:   "website",
    source:    lead.source || ("website-" + (lead.type || "lead")),
    notes:     notes.join(" · "),
    company:   lead.company || "",     // honeypot passthrough — server drops if filled
    leadType:  lead.type,
    submittedAt: lead.submittedAt,
  };
}
window.deliverLead = deliverLead;
window.waLink = waLink;

/* ------------------------------- colour picker + 360° spin viewer
   The stage shows either a drag-to-rotate 360 view (chips that carry
   data-spin-base, pointing at images/360/<model>/<colour>/01..NN.jpg)
   or a static image (chips with only data-colour). */
(function () {
  const stage = document.querySelector(".colour-stage");
  if (!stage) return;
  const img = stage.querySelector("img");
  const label = document.querySelector(".colour-name");
  const hint = stage.querySelector(".spin-hint");
  const FRAMES = parseInt(stage.getAttribute("data-frames") || "0", 10);
  const pad = (n) => String(n).padStart(2, "0");

  let base = null;        // current spin folder (null = static mode)
  let idx = 0;            // current frame (0-based)
  let cache = {};         // per-base preloaded Image objects
  let spinTimer = 0;      // gentle auto-rotate until first touch
  let interacted = false;

  function frames(b) {
    if (!cache[b]) cache[b] = Array.from({ length: FRAMES }, (_, i) => {
      const im = new Image(); im.src = `${b}/${pad(i + 1)}.jpg`; return im;
    });
    return cache[b];
  }
  function show(i) {
    if (!base) return;
    idx = ((i % FRAMES) + FRAMES) % FRAMES;
    img.src = frames(base)[idx].src;
  }
  function startAuto() {
    stopAuto();
    if (!base || interacted) return;
    spinTimer = setInterval(() => show(idx + 1), 130);
  }
  function stopAuto() { if (spinTimer) { clearInterval(spinTimer); spinTimer = 0; } }

  function setSpin(b) {
    base = b; stage.classList.add("spinning");
    if (hint) hint.hidden = false;
    frames(b); show(idx); startAuto();
  }
  function setStatic(src, alt) {
    base = null; stopAuto(); stage.classList.remove("spinning");
    if (hint) hint.hidden = true;
    img.src = src; img.alt = alt || "";
  }

  // drag / swipe to rotate
  let down = false, startX = 0, startIdx = 0;
  const SENS = 12;   // px per frame
  stage.addEventListener("pointerdown", (e) => {
    if (!base) return;
    down = true; startX = e.clientX; startIdx = idx;
    interacted = true; stopAuto();
    stage.classList.add("grabbing");
    if (hint) hint.hidden = true;
    e.preventDefault();
  });
  window.addEventListener("pointermove", (e) => {
    if (!down) return;
    show(startIdx + Math.round((startX - e.clientX) / SENS));
  });
  window.addEventListener("pointerup", () => { down = false; stage.classList.remove("grabbing"); });

  // chips
  let userPicked = false;
  document.querySelectorAll(".col-chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      userPicked = true;
      document.querySelectorAll(".col-chip").forEach((c) => c.classList.remove("active"));
      chip.classList.add("active");
      if (label) label.textContent = chip.getAttribute("data-colour-name") || "";
      const spin = chip.getAttribute("data-spin-base");
      if (spin && FRAMES) setSpin(spin);
      else setStatic(chip.getAttribute("data-colour"), chip.getAttribute("data-colour-name"));
    });
  });

  // boot: first chip decides the mode
  const first = document.querySelector(".col-chip.active") || document.querySelector(".col-chip");
  const firstSpin = first && first.getAttribute("data-spin-base");
  if (firstSpin && FRAMES) {
    // start auto-rotate only once the stage is on screen — but never override
    // a colour the user has already picked in the meantime
    if ("IntersectionObserver" in window) {
      const io = new IntersectionObserver((es, obs) => {
        es.forEach((e) => {
          if (e.isIntersecting) { if (!userPicked) setSpin(firstSpin); obs.disconnect(); }
        });
      }, { threshold: 0.3 });
      io.observe(stage);
      base = firstSpin;   // mark spin mode immediately (drag works pre-observe)
      stage.classList.add("spinning");
    } else { setSpin(firstSpin); }
  }
})();

/* --------------------------------------------------- scroll reveal motion */
const revealEls = document.querySelectorAll(".reveal");
if (revealEls.length && "IntersectionObserver" in window) {
  const io = new IntersectionObserver((entries, obs) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add("in"); obs.unobserve(e.target); }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
  revealEls.forEach(el => io.observe(el));
} else {
  revealEls.forEach(el => el.classList.add("in"));
}

/* ------------------------------------------------ in-page tab scroll-spy */
const pageTabs = document.querySelector(".page-tabs");
if (pageTabs && "IntersectionObserver" in window) {
  const links = [...pageTabs.querySelectorAll("a")];
  const secForLink = new Map();
  links.forEach(a => {
    const id = (a.getAttribute("href") || "").split("#")[1];
    const sec = id && document.getElementById(id);
    if (sec) secForLink.set(sec, a);
  });
  const spy = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        links.forEach(l => l.classList.remove("active"));
        secForLink.get(e.target)?.classList.add("active");
      }
    });
  }, { rootMargin: "-45% 0px -50% 0px", threshold: 0 });
  secForLink.forEach((_a, sec) => spy.observe(sec));
}

/* -------------------------------------- downward-only "settle" scroll snap
   CSS scroll-snap hijacks BOTH directions and fights the user on the way up.
   Instead we gently glide to the next section — but only when:
     • scrolling DOWN (up-scrolls are never touched),
     • the user has committed past ~half a viewport toward the next section,
     • the user has actually paused (scroll settled).
   Any manual input (wheel / trackpad / touch / key) cancels an in-flight
   glide immediately, so it can never wrestle the scroll. Desktop + fine
   pointer only; respects reduced-motion. */
(function () {
  const okMedia = window.matchMedia("(min-width: 900px) and (prefers-reduced-motion: no-preference)");
  const coarse = window.matchMedia("(pointer: coarse)");
  // Checked live (not once at load) so it survives resize/rotate and a
  // late-sized viewport rather than disabling itself forever.
  const active = () => okMedia.matches && !coarse.matches;

  const header = document.querySelector(".site-header");
  const tabs = document.querySelector(".page-tabs");
  const topOffset = el =>
    (header ? header.offsetHeight : 64) +
    (tabs && el.closest(".page-scope") ? tabs.offsetHeight : 0);

  const snapEls = () => [...document.querySelectorAll(".snap, .mband")]
    .filter(el => el.offsetHeight > 0 && getComputedStyle(el).display !== "none");

  let lastY = window.scrollY, dir = 0, settleTimer, animating = false, raf = 0;

  function cancel() {
    if (raf) cancelAnimationFrame(raf);
    raf = 0; animating = false;
    document.documentElement.style.scrollBehavior = "";
  }

  function glideTo(dest) {
    const startY = window.scrollY, delta = dest - startY;
    if (Math.abs(delta) < 2) return;
    const dur = Math.min(520, 240 + Math.abs(delta) * 0.32);
    const root = document.documentElement;
    root.style.scrollBehavior = "auto";   // stop CSS smooth from compounding our rAF
    const ease = p => 1 - Math.pow(1 - p, 3);   // easeOutCubic
    let t0 = null; animating = true;
    const step = ts => {
      if (!animating) return;
      if (t0 === null) t0 = ts;
      const p = Math.min(1, (ts - t0) / dur);
      window.scrollTo(0, Math.round(startY + delta * ease(p)));
      if (p < 1) { raf = requestAnimationFrame(step); }
      else { animating = false; raf = 0; lastY = window.scrollY; root.style.scrollBehavior = ""; }
    };
    raf = requestAnimationFrame(step);
  }

  function onSettle() {
    if (dir <= 0 || animating || !active()) return;     // downward only, desktop fine-pointer
    const y = window.scrollY, vh = window.innerHeight;
    let best = null;                                    // nearest section start ahead
    for (const el of snapEls()) {
      const dest = el.getBoundingClientRect().top + y - topOffset(el);
      if (dest > y + 4 && (best === null || dest < best)) best = dest;
    }
    if (best === null) return;
    if (best - y > vh * 0.5) return;                    // not committed yet — leave it
    glideTo(best);
  }

  window.addEventListener("scroll", () => {
    const y = window.scrollY;
    dir = y > lastY ? 1 : (y < lastY ? -1 : dir);
    lastY = y;
    if (animating) return;                             // ignore our own programmatic scroll
    clearTimeout(settleTimer);
    settleTimer = setTimeout(onSettle, 110);
  }, { passive: true });

  // Manual intent always wins — abort any in-flight glide instantly.
  ["wheel", "touchstart", "touchmove", "keydown", "pointerdown"].forEach(ev =>
    window.addEventListener(ev, () => { if (animating) cancel(); }, { passive: true }));
})();

/* expose for inline onclick fallbacks if ever needed */
window.openQuote = openQuote;


/* ==========================================================================
   Analytics events (GA4)
   --------------------------------------------------------------------------
   Every call goes through track(), which is a no-op unless a GA4 tag is on
   the page — so with GA4_ID empty in build.py the site behaves exactly as it
   did before, with no network calls and no cookies.

   Events sent:
     generate_lead     any form submitted   (lead_type: quote|test_drive|message)
     book_test_drive   the test-drive wizard completed
     view_quote_form   the quote modal opened
     contact_whatsapp  a WhatsApp button/link clicked
     contact_call      a Call button / tel: link clicked
     download_brochure a brochure PDF clicked
   ========================================================================== */
(function () {
  function track(name, params) {
    if (typeof window.gtag === "function") window.gtag("event", name, params || {});
  }
  window.trackEvent = track;

  function modelOf(el) {
    if (!el) return "";
    const holder = el.closest("[data-model]");
    return (holder && holder.getAttribute("data-model")) || "";
  }

  document.addEventListener("click", function (e) {
    const t = e.target;
    if (!t || !t.closest) return;

    const wa = t.closest("[data-wa], a[href*='wa.me']");
    if (wa) return track("contact_whatsapp", { model: modelOf(wa) });

    const call = t.closest("[data-call], a[href^='tel:']");
    if (call) return track("contact_call", {});

    const quote = t.closest("[data-quote]");
    if (quote) return track("view_quote_form", { model: modelOf(quote) });

    const pdf = t.closest("a[href$='.pdf']");
    if (pdf) return track("download_brochure", {
      file_name: (pdf.getAttribute("href") || "").split("/").pop()
    });
  }, true);

  document.addEventListener("submit", function (e) {
    const f = e.target;
    if (!f || f.tagName !== "FORM") return;

    // honeypot filled in = bot; don't report it as a lead
    const hp = f.querySelector("input[name='company']");
    if (hp && hp.value) return;

    const data = new FormData(f);
    const model = (data.get("model") || "").toString();
    const kind = f.id === "tdForm" ? "test_drive" : f.id === "msgForm" ? "message" : "quote";

    if (kind === "test_drive") track("book_test_drive", { model: model });
    track("generate_lead", { lead_type: kind, model: model, currency: "XCD", value: 0 });
  }, true);
})();
