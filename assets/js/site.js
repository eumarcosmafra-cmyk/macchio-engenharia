// Macchio Engenharia — interações (sem dependências)
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = window.matchMedia("(pointer: fine)").matches;
  const WHATSAPP = "5547991723557";

  // Medição: cliques de CTA vão para o dataLayer (GTM/GA4)
  const track = (cta, extra = {}) => {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: "cta_click", cta, ...extra });
  };
  document.addEventListener("click", (e) => {
    const el = e.target.closest("[data-track]");
    if (el) track(el.dataset.track);
  });

  // Header: transparente sobre o hero, sólido depois; esconde ao descer e volta ao subir
  const header = $("[data-header]");
  const hero = $("[data-hero]");
  let lastY = window.scrollY;
  const onScroll = () => {
    const y = window.scrollY;
    const limit = hero ? hero.offsetHeight - 120 : 40;
    header.classList.toggle("is-solid", y > limit);
    if (!$("[data-menu]")?.open) header.classList.toggle("is-hidden", y > 240 && y > lastY + 4);
    if (y < lastY - 4) header.classList.remove("is-hidden");
    lastY = y;
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
  // Ao navegar por âncora, o header volta a aparecer e não encobre o título
  window.addEventListener("hashchange", () => header.classList.remove("is-hidden"));

  // Menu (mobile)
  const menu = $("[data-menu]");
  if (menu) {
    const opener = $("[data-menu-open]");
    opener.addEventListener("click", () => { menu.showModal(); opener.setAttribute("aria-expanded", "true"); });
    menu.addEventListener("close", () => opener.setAttribute("aria-expanded", "false"));
    $$("[data-menu-close], a", menu).forEach((el) => el.addEventListener("click", () => menu.close()));
  }

  // Cursor "Ver projeto" (só com mouse)
  if (finePointer && !reduced) {
    const targets = $$("[data-cursor]");
    if (targets.length) {
      const c = document.createElement("div");
      c.className = "cursor";
      c.setAttribute("aria-hidden", "true");
      document.body.appendChild(c);
      window.addEventListener("pointermove", (e) => { c.style.setProperty("--x", `${e.clientX}px`); c.style.setProperty("--y", `${e.clientY}px`); }, { passive: true });
      targets.forEach((t) => {
        t.addEventListener("pointerenter", () => { c.textContent = t.dataset.cursor; c.classList.add("is-on"); });
        t.addEventListener("pointerleave", () => c.classList.remove("is-on"));
      });
    }
  }

  // Índice de projetos: filtro, grade/lista e prévia no hover
  const pidx = $("[data-pidx]");
  if (pidx) {
    const grid = $("[data-pgrid]", pidx);
    const list = $("[data-plist]", pidx);
    const cards = $$(".card", grid);
    const rows = $$(".prow", list);
    const status = $("[data-filter-status]", pidx);
    const withTransition = (fn) => (document.startViewTransition && !reduced ? document.startViewTransition(fn) : fn());
    const apply = (btn) => {
      const cat = btn.dataset.filter;
      let n = 0;
      cards.forEach((c, j) => {
        const show = cat === "all" || c.dataset.cat === cat;
        c.hidden = !show;
        rows[j].hidden = !show;
        if (show) n++;
      });
      status.textContent = `${n} projetos exibidos`;
    };
    $$("[data-filter]", pidx).forEach((b) => b.addEventListener("click", () => {
      $$("[data-filter]", pidx).forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      withTransition(() => apply(b));
    }));
    $$("[data-view]", pidx).forEach((b) => b.addEventListener("click", () => {
      $$("[data-view]", pidx).forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      withTransition(() => { grid.hidden = b.dataset.view !== "grid"; list.hidden = b.dataset.view !== "list"; });
    }));
    if (finePointer && !reduced) {
      const pv = document.createElement("div");
      pv.className = "preview";
      pv.setAttribute("aria-hidden", "true");
      pv.innerHTML = "<img alt=''>";
      document.body.appendChild(pv);
      const pvImg = $("img", pv);
      window.addEventListener("pointermove", (e) => { pv.style.setProperty("--x", `${e.clientX + 24}px`); pv.style.setProperty("--y", `${e.clientY - 100}px`); }, { passive: true });
      rows.forEach((r) => {
        r.addEventListener("pointerenter", () => { pvImg.src = r.dataset.preview; pv.classList.add("is-on"); });
        r.addEventListener("pointerleave", () => pv.classList.remove("is-on"));
      });
    }
  }

  // Galeria do projeto: lightbox (teclado, toque e botões)
  const lb = $("[data-lb]");
  if (lb) {
    const items = $$("[data-lb-item]");
    const img = $("img", lb);
    const count = $("[data-lb-count]", lb);
    let k = 0;
    const show = (n) => {
      k = (n + items.length) % items.length;
      const it = items[k];
      img.src = it.dataset.full;
      img.alt = $("img", it).alt;
      count.textContent = `Imagem ${k + 1} de ${items.length}`;
    };
    items.forEach((it, j) => it.addEventListener("click", () => { show(j); lb.showModal(); track("galeria_ampliar"); }));
    $("[data-lb-prev]", lb).addEventListener("click", () => show(k - 1));
    $("[data-lb-next]", lb).addEventListener("click", () => show(k + 1));
    $("[data-lb-close]", lb).addEventListener("click", () => lb.close());
    lb.addEventListener("keydown", (e) => { if (e.key === "ArrowLeft") show(k - 1); if (e.key === "ArrowRight") show(k + 1); });
    lb.addEventListener("click", (e) => { if (e.target === lb || e.target.classList.contains("lb-fig")) lb.close(); });
    let x0 = null;
    lb.addEventListener("touchstart", (e) => { x0 = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener("touchend", (e) => {
      if (x0 === null) return;
      const dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 50) show(k + (dx < 0 ? 1 : -1));
      x0 = null;
    });
  }

  // Formulário de contato → WhatsApp com mensagem do serviço escolhido
  const form = $("[data-lead-form]");
  if (form) {
    const err = $("[data-form-err]", form);
    const ok = $("[data-form-ok]", form);
    const okLink = $("[data-form-link]", form);
    const fail = (field, msg) => {
      err.textContent = msg;
      field.setAttribute("aria-invalid", "true");
      field.focus();
    };
    form.addEventListener("input", (e) => e.target.removeAttribute("aria-invalid"));
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const sel = form.elements.interesse;
      const nome = form.elements.nome.value.trim();
      if (!sel.value) return fail(sel, "Escolha a área de interesse.");
      if (!nome) return fail(form.elements.nome, "Informe seu nome para continuarmos.");
      err.textContent = "";
      const lines = [sel.selectedOptions[0].dataset.msg, `Meu nome é ${nome}.`];
      const msg = form.elements.mensagem.value.trim();
      if (msg) lines.push(msg);
      lines.push("(Mensagem enviada pelo site)");
      track("whatsapp_formulario", { interesse: sel.value });
      const url = `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(lines.join("\n"))}`;
      okLink.href = url;
      ok.hidden = false;
      const win = window.open(url, "_blank");
      if (win) win.opener = null; else window.location.href = url;
    });
  }

  // Botão flutuante (mobile): aparece depois do hero, some no contato e no rodapé
  const fab = $("[data-fab]");
  if (fab && "IntersectionObserver" in window) {
    const watch = [hero || $(".phead") || $(".pidx-head"), $("#contato"), $("[data-footer]")].filter(Boolean);
    const visible = new Map();
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => visible.set(en.target, en.isIntersecting));
      fab.classList.toggle("is-on", ![...visible.values()].some(Boolean));
    });
    watch.forEach((el) => { visible.set(el, true); io.observe(el); });
  }

  $$("[data-year]").forEach((el) => { el.textContent = new Date().getFullYear(); });
})();
