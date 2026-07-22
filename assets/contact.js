/* =========================================================================
   Chery Antigua — contact page: tabs, test-drive wizard, message form.
   Leads are submitted through window.deliverLead (defined in site.js), which
   POSTs them to the VMP endpoint (CONFIG.LEAD_ENDPOINT).
   ========================================================================= */
(function () {
  const card = document.querySelector(".contact-card");
  if (!card) return;

  /* ---- tabs ---- */
  const tabs = card.querySelectorAll(".cc-tab");
  const panes = card.querySelectorAll(".cc-pane");
  tabs.forEach(t => t.addEventListener("click", () => {
    tabs.forEach(x => x.classList.toggle("active", x === t));
    panes.forEach(p => { p.hidden = p.dataset.pane !== t.dataset.tab; });
  }));

  const send = lead => (window.deliverLead ? window.deliverLead(lead) : Promise.resolve(true));

  /* ---- test-drive wizard ---- */
  const tdForm = document.getElementById("tdForm");
  if (tdForm) {
    const pane = tdForm.closest(".cc-pane");
    const panels = [...tdForm.querySelectorAll(".td-panel")];
    const titles = ["Choose your model", "Pick a date & time", "Your details"];
    const total = panels.length;
    const bar = pane.querySelector(".td-bar span");
    const curEl = pane.querySelector(".td-cur");
    const titleEl = pane.querySelector(".td-title");
    const back = tdForm.querySelector(".td-back");
    const next = tdForm.querySelector(".td-next");
    const submit = tdForm.querySelector(".td-submit");
    let step = 1;

    // date can't be in the past, and test drives run Monday–Friday only
    const dateInput = tdForm.querySelector('input[name="date"]');
    if (dateInput) {
      const d = new Date();
      dateInput.min = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
      const isWeekend = v => { const day = new Date(v + "T12:00:00").getDay(); return day === 0 || day === 6; };
      const checkDay = () => {
        if (dateInput.value && isWeekend(dateInput.value)) {
          dateInput.setCustomValidity("Test drives run Monday to Friday — please pick a weekday.");
          dateInput.reportValidity();
        } else dateInput.setCustomValidity("");
      };
      dateInput.addEventListener("input", checkDay);
      dateInput.addEventListener("change", checkDay);
    }

    function render() {
      panels.forEach(pl => { pl.hidden = Number(pl.dataset.step) !== step; });
      bar.style.width = (step / total * 100) + "%";
      curEl.textContent = step;
      titleEl.textContent = titles[step - 1];
      back.hidden = step === 1;
      next.hidden = step === total;
      submit.hidden = step !== total;
    }

    function validateStep() {
      const panel = tdForm.querySelector('.td-panel[data-step="' + step + '"]');
      const radioNames = [...new Set([...panel.querySelectorAll('input[type="radio"]')].map(r => r.name))];
      for (const nm of radioNames) {
        if (![...panel.querySelectorAll('input[name="' + nm + '"]')].some(r => r.checked)) {
          panel.querySelector('input[name="' + nm + '"]').focus();
          return false;
        }
      }
      for (const el of panel.querySelectorAll("input[required], textarea[required]")) {
        if (!el.checkValidity()) { el.reportValidity(); return false; }
      }
      return true;
    }

    next.addEventListener("click", () => {
      if (validateStep() && step < total) { step++; render(); pane.scrollIntoView({ behavior: "smooth", block: "nearest" }); }
    });
    back.addEventListener("click", () => { if (step > 1) { step--; render(); } });

    tdForm.addEventListener("submit", async e => {
      e.preventDefault();
      // belt & braces: validate EVERY step, jumping back to the first
      // incomplete one — a stray submit can never skip the details.
      for (let s = 1; s <= total; s++) {
        step = s; render();
        if (!validateStep()) return;
      }
      const f = new FormData(tdForm);
      const lead = {
        type: "test-drive", source: "test-drive-form",
        model: (f.get("model") || "").toString(),
        date: (f.get("date") || "").toString(),
        time: (f.get("time") || "").toString(),
        firstName: (f.get("firstName") || "").toString().trim(),
        lastName: (f.get("lastName") || "").toString().trim(),
        phone: (f.get("phone") || "").toString().trim(),
        email: (f.get("email") || "").toString().trim(),
        notes: (f.get("notes") || "").toString().trim(),
        company: (f.get("company") || "").toString(),   // honeypot
        submittedAt: new Date().toISOString(),
      };
      submit.disabled = true; submit.textContent = "Sending…";
      await send(lead);
      submit.disabled = false; submit.textContent = "Confirm booking →";
      const done = pane.querySelector(".td-done");
      done.querySelector(".td-name").textContent = lead.firstName || "there";
      done.querySelector(".td-model-name").textContent = "Chery " + lead.model;
      tdForm.hidden = true;
      pane.querySelector(".td-progress").hidden = true;
      done.hidden = false;
    });

    render();
  }

  /* ---- message form ---- */
  const msgForm = document.getElementById("msgForm");
  if (msgForm) {
    msgForm.addEventListener("submit", async e => {
      e.preventDefault();
      if (!msgForm.checkValidity()) { msgForm.reportValidity(); return; }
      const f = new FormData(msgForm);
      const lead = {
        type: "message", source: "contact-form",
        firstName: (f.get("firstName") || "").toString().trim(),
        lastName: (f.get("lastName") || "").toString().trim(),
        email: (f.get("email") || "").toString().trim(),
        phone: (f.get("phone") || "").toString().trim(),
        model: (f.get("model") || "").toString(),
        message: (f.get("message") || "").toString().trim(),
        company: (f.get("company") || "").toString(),   // honeypot
        submittedAt: new Date().toISOString(),
      };
      const btn = msgForm.querySelector('button[type="submit"]');
      btn.disabled = true; btn.textContent = "Sending…";
      await send(lead);
      btn.disabled = false; btn.textContent = "Send Message →";
      const pane = msgForm.closest(".cc-pane");
      pane.querySelector(".msg-name").textContent = lead.firstName || "there";
      msgForm.hidden = true;
      pane.querySelector(".msg-done").hidden = false;
    });
  }
})();
