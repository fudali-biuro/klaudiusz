// Biuro akceptacji – Pablo przegląda posty i klika ✅ OK / ✏️ Popraw / ❌ Odrzuć; „Wyślij decyzje” → jedna wiadomość do Oli.
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const NAZWY_KANALOW = { instagram: "Instagram", "instagram-relacja": "IG relacja", facebook: "Facebook", pinterest: "Pinterest", tiktok: "TikTok", etsy: "Etsy" };
  const STANY = { czeka: "🕐 czeka na Ciebie", ok: "✅ zatwierdzony", popraw: "✏️ w poprawkach", odrzucone: "❌ odrzucony", "w-bufferze": "📤 szkic w Bufferze", opublikowane: "🌍 opublikowany" };
  let posty = [], decyzje = {}, filtrStan = "czeka", filtrKanal = "";

  const esc = (t) => String(t ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  function toast(t) { const el = $("#toast"); el.textContent = t; el.hidden = false; clearTimeout(toast.t); toast.t = setTimeout(() => (el.hidden = true), 3500); }
  const dataPL = (d) => d ? new Date(d + "T12:00:00").toLocaleDateString("pl-PL", { weekday: "short", day: "numeric", month: "long" }) : "bez daty";

  // decyzja Pablo z biura liczy się, dopóki zespół nie wpisze jej do archiwum (post nadal „czeka” w tej samej wersji)
  function decyzjaDla(p) {
    const d = decyzje[p.id];
    return d && p.stan === "czeka" && (d.wersja || 1) >= (p.wersja || 1) ? d : null;
  }
  function pasuje(p) {
    if (filtrKanal && !p.kanal.startsWith(filtrKanal)) return false;
    const d = decyzjaDla(p);
    if (filtrStan === "czeka") return p.stan === "czeka" && !d;
    if (filtrStan === "decyzje") return !!d;
    if (filtrStan === "w-toku") return ["ok", "popraw", "w-bufferze"].includes(p.stan);
    return true;
  }

  function karta(p) {
    const d = decyzjaDla(p);
    const klasa = d ? `d-${d.decyzja}` : "";
    const media = [...(p.obrazy || []).map((u) => `<img src="${esc(u)}" alt="${esc(p.tytul)}" loading="lazy">`),
      ...(p.wideo || []).map((u) => `<video src="${esc(u)}" controls preload="metadata"></video>`)];
    const stanTekst = d ? { ok: "✅ Twoje OK", popraw: "✏️ do poprawy", odrzucone: "❌ odrzucasz" }[d.decyzja] + (d.wyslano ? " · wysłane" : " · niewysłane") : STANY[p.stan] || p.stan;
    const el = document.createElement("article");
    el.className = `post ${klasa}`;
    el.innerHTML = `
      <div class="naglowek"><span class="kanal k-${esc(p.kanal)}">${esc(NAZWY_KANALOW[p.kanal] || p.kanal)}</span>
        <span>${esc(dataPL(p.data))}${p.godzina ? " · " + esc(p.godzina) : ""}</span>
        ${p.wersja > 1 ? `<span>wersja ${p.wersja}</span>` : ""}<span class="stan">${esc(stanTekst)}</span></div>
      <h3>${esc(p.tytul)}${p.produkt ? ` <small style="color:var(--tekst2)">· ${esc(p.produkt)}</small>` : ""}</h3>
      ${media.length ? `<div class="galeria ${media.length === 1 ? "jeden" : ""}">${media.join("")}</div>` : `<p class="notka">brak grafiki</p>`}
      <div class="tekst">${esc(p.tekst)}</div><button class="wiecej" type="button">pokaż cały tekst</button>
      ${p.hashtagi ? `<div class="hashtagi">${esc(p.hashtagi)}</div>` : ""}
      ${p.stan !== "czeka" && p.komentarz ? `<p class="notka">Twój komentarz: ${esc(p.komentarz)}</p>` : ""}
      ${p.stan === "czeka" ? `<div class="decyzja">
        <div class="przyciski">
          <button type="button" class="b-ok ${d?.decyzja === "ok" ? "on" : ""}" data-d="ok">✅ OK</button>
          <button type="button" class="b-popraw ${d?.decyzja === "popraw" ? "on" : ""}" data-d="popraw">✏️ Popraw</button>
          <button type="button" class="b-odrzucone ${d?.decyzja === "odrzucone" ? "on" : ""}" data-d="odrzucone">❌ Odrzuć</button>
        </div>
        <textarea placeholder="Komentarz (co poprawić, co się podoba)…">${esc(d?.komentarz || "")}</textarea>
        <div class="info">${d ? (d.wyslano ? "Decyzja wysłana zespołowi." : "Zapisane – wyślesz wszystko jednym przyciskiem na górze.") : "Kliknij decyzję. Komentarz zapisuje się sam."}</div>
      </div>` : ""}`;
    el.querySelector(".wiecej").onclick = (e) => { const t = el.querySelector(".tekst"); t.classList.toggle("rozwin"); e.target.textContent = t.classList.contains("rozwin") ? "zwiń" : "pokaż cały tekst"; };
    el.querySelectorAll(".galeria img").forEach((img) => (img.onclick = () => { const pg = $("#lupa"); pg.querySelector("img").src = img.src; pg.hidden = false; }));
    const ta = el.querySelector("textarea");
    el.querySelectorAll(".przyciski button").forEach((b) => (b.onclick = () => {
      const nowa = decyzjaDla(p)?.decyzja === b.dataset.d ? "" : b.dataset.d;
      if (nowa === "popraw" && !ta.value.trim()) { ta.focus(); toast("Napisz w komentarzu, co poprawić 🙂"); }
      zapisz(p, nowa, ta.value);
    }));
    // komentarz: zapis od razu tylko, gdy decyzja już jest; inaczej idzie razem z kliknięciem przycisku
    if (ta) ta.onchange = () => { const d2 = decyzjaDla(p); if (d2) setTimeout(() => zapisz(p, decyzjaDla(p)?.decyzja || d2.decyzja, ta.value), 150); };
    return el;
  }

  async function zapisz(p, decyzja, komentarz) {
    try {
      const r = await fetch("/api/akceptacja", { method: "POST", headers: { "content-type": "application/json", "x-biuro": "1" },
        body: JSON.stringify({ id: p.id, decyzja, komentarz, tytul: p.tytul, wersja: p.wersja || 1 }) });
      const j = await r.json();
      if (!r.ok) throw new Error(j.opis || j.blad || r.status);
      if (decyzja) decyzje[p.id] = j.decyzja; else delete decyzje[p.id];
      rysuj();
    } catch (e) { toast("Nie zapisało się: " + e.message); }
  }

  function rysuj() {
    const b = $("#biblioteka");
    const widoczne = posty.filter(pasuje);
    b.innerHTML = "";
    if (!widoczne.length) b.innerHTML = `<p class="pusto">${filtrStan === "czeka" ? "🎉 Nic nie czeka na Ciebie – wszystko przejrzane." : "Brak postów w tym widoku."}</p>`;
    for (const p of widoczne) b.append(karta(p));
    const czeka = posty.filter((p) => p.stan === "czeka" && !decyzjaDla(p)).length;
    const niewyslane = posty.filter((p) => { const d = decyzjaDla(p); return d && !d.wyslano; }).length;
    $("#licznik").textContent = `🕐 Do przejrzenia: ${czeka} · decyzji do wysłania: ${niewyslane}`;
    const w = $("#wyslij");
    w.disabled = !niewyslane;
    w.classList.toggle("sa", niewyslane > 0 && czeka === 0);
    w.textContent = niewyslane ? `📨 Wyślij decyzje zespołowi (${niewyslane})` : "📨 Wyślij decyzje zespołowi";
  }

  $("#wyslij").onclick = async () => {
    const w = $("#wyslij"); w.disabled = true;
    try {
      const r = await fetch("/api/akceptacja", { method: "POST", headers: { "content-type": "application/json", "x-biuro": "1" }, body: JSON.stringify({ wyslij: true }) });
      const j = await r.json();
      if (!r.ok) throw new Error(j.opis || j.blad || r.status);
      toast(j.wyslano ? `Wysłane ✔ (${j.wyslano}) – Ola i Zosia biorą się do pracy.` : "Nie było nic do wysłania.");
      await wczytaj();
    } catch (e) { toast("Nie udało się wysłać: " + e.message); w.disabled = false; }
  };
  $("#filtry").onclick = (e) => {
    const b = e.target.closest("button"); if (!b) return;
    if (b.dataset.stan !== undefined) { filtrStan = b.dataset.stan; $("#filtry").querySelectorAll("[data-stan]").forEach((x) => x.classList.toggle("wl", x === b)); }
    if (b.dataset.kanal !== undefined) { filtrKanal = b.dataset.kanal; $("#filtry").querySelectorAll("[data-kanal]").forEach((x) => x.classList.toggle("wl", x === b)); }
    rysuj();
  };
  $("#lupa").onclick = () => ($("#lupa").hidden = true);
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") $("#lupa").hidden = true; });

  async function wczytaj() {
    try { const r = await fetch("akceptacja.json", { cache: "no-cache" }); posty = (await r.json()).posty || []; } catch { posty = []; }
    try { const r = await fetch("/api/akceptacja", { cache: "no-store" }); decyzje = r.ok ? (await r.json()).decyzje || {} : {}; } catch { decyzje = {}; }
    posty.sort((a, b) => (a.data || "9999").localeCompare(b.data || "9999") || (a.godzina || "").localeCompare(b.godzina || ""));
    rysuj();
  }
  wczytaj();
  setInterval(wczytaj, 5 * 60 * 1000);
})();
