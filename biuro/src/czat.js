"use strict";
// Okno czatu w biurze: Pablo ↔ pracownik.
// Wysyłka: POST /api/czat (budzi sesję Klaudiusza → przekazanie do pracownika). Załączniki: POST /api/plik (Vercel Blob).
// Odpowiedzi: pracownicy zapisują je w archiwum (scripts/czat.py) → strona przebudowuje się w kilka sekund → /czat/<id>.json.
// Korzysta z funkcji app.js: $, esc, kiedy, renderMd, znajdz, stanEf, toast, wczytaj, DANE.
const Czat = (() => {
  const LS_WYSLANE = "biuro-czat-wyslane", LS_PRZECZYTANE = "biuro-czat-przeczytane", LS_SZKICE = "biuro-czat-szkice";
  const MAX_PLIK = 4_300_000, MAX_NAGRANIE_S = 600;
  const dotyk = matchMedia("(pointer: coarse)").matches;

  let biezacy = null, el = null, widac = false;
  let wiadomosci = [], zbudowano = null, podpis = "";
  let zalaczniki = [], odpowiedz = null, nagrywanie = null, polaczenie = undefined;
  let timer = null, szybkoDo = 0, przyklejony = true, obserwator = null;

  const ls = {
    get(k, d) { try { const v = JSON.parse(localStorage.getItem(k)); return v ?? d; } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* tryb prywatny – trudno */ } },
  };
  const czasMs = (iso) => Date.parse(iso || "") || 0;
  const rozmiarTxt = (b) => !b ? "" : b > 1e6 ? `${(b / 1e6).toFixed(1)} MB` : `${Math.max(1, Math.round(b / 1e3))} kB`;
  const osoba = (id) => znajdz(id) || { id, imie: id, emoji: "" };
  const KOBIETY = new Set(["marketing", "grafika", "rynki-zagraniczne"]);   // Ola, Zosia, Greta
  const forma = (o) => KOBIETY.has(o.id) ? "a" : "";                       // Ola odebrała / Mietek odebrał

  function noweId() {
    const p = Object.fromEntries(new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/Warsaw", year: "numeric", month: "2-digit", day: "2-digit",
      hour: "2-digit", minute: "2-digit", second: "2-digit", hourCycle: "h23" }).formatToParts(new Date()).map((x) => [x.type, x.value]));
    const los = Array.from(crypto.getRandomValues(new Uint8Array(3)), (b) => b.toString(16).padStart(2, "0")).join("");
    return `m_${p.year}${p.month}${p.day}${p.hour}${p.minute}${p.second}_${los}`;
  }

  /* ---------------- wysłane (skrzynka nadawcza w przeglądarce – do czasu, aż wiadomość trafi do archiwum) ---------------- */
  function wyslane() {
    const teraz = Date.now();
    return ls.get(LS_WYSLANE, []).filter((w) => teraz - czasMs(w.czas) < 3 * 864e5);
  }
  function zapiszWyslane(lista) { ls.set(LS_WYSLANE, lista.slice(-60)); }
  function aktualizujWyslana(id, zmiany) { zapiszWyslane(wyslane().map((w) => (w.id === id ? { ...w, ...zmiany } : w))); render(); }

  /* ---------------- nieprzeczytane ---------------- */
  function nieprzeczytane(id) {
    const ost = DANE.czat?.[id]?.ostatnia;
    if (!ost || ost.od === "pablo") return false;
    if (widac && biezacy === id) return false;
    return czasMs(ost.czas) > czasMs(ls.get(LS_PRZECZYTANE, {})[id]);
  }
  function oznaczPrzeczytane() {
    if (!biezacy || !widac || document.hidden) return;
    const ost = [...wiadomosci].reverse().find((w) => w.od !== "pablo");
    const p = ls.get(LS_PRZECZYTANE, {});
    const czas = [ost?.czas, DANE.czat?.[biezacy]?.ostatnia?.czas].filter(Boolean).sort((a, b) => czasMs(b) - czasMs(a))[0];
    if (czas && czasMs(czas) > czasMs(p[biezacy])) { p[biezacy] = czas; ls.set(LS_PRZECZYTANE, p); }
    if (typeof odswiezUI === "function") odswiezUI(false);   // liczniki 💬 w nagłówku i na kartach
  }

  /* ---------------- budowa okna ---------------- */
  function zbuduj(kontener, id) {
    const o = osoba(id);
    kontener.innerHTML = `<div class="czat" data-osoba="${esc(id)}">
      <div class="cz-baner" hidden></div>
      <div class="cz-lista" role="log" aria-live="polite" aria-label="Rozmowa z ${esc(o.imie)}"></div>
      <div class="cz-nagr" hidden><span class="cz-kropka"></span><b class="cz-czas">0:00</b><span class="cz-dykt">Mów – nagrywam…</span>
        <button type="button" class="cz-btn cz-stop">■ Gotowe</button><button type="button" class="cz-btn cz-anuluj" aria-label="Anuluj nagranie">✕</button></div>
      <div class="cz-re" hidden><span></span><button type="button" class="cz-x" aria-label="Nie odpowiadaj na to">✕</button></div>
      <div class="cz-zal"></div>
      <form class="cz-forma" autocomplete="off">
        <textarea rows="1" placeholder="Napisz do: ${esc(o.imie)}… (możesz wkleić zdjęcie)" aria-label="Wiadomość do ${esc(o.imie)}"></textarea>
        <div class="cz-przyciski">
          <button type="button" class="cz-btn cz-plik" title="Dodaj zdjęcie lub plik" aria-label="Dodaj zdjęcie lub plik">📎</button>
          <button type="button" class="cz-btn cz-mikro" title="Nagraj wiadomość głosową" aria-label="Nagraj wiadomość głosową">🎤</button>
          <button type="submit" class="cz-btn cz-wyslij">Wyślij ➤</button>
        </div>
        <input type="file" multiple hidden accept="image/*,audio/*,video/*,application/pdf,.pdf,.doc,.docx,.xls,.xlsx,.csv,.txt,.md">
      </form></div>`;
    el = kontener.querySelector(".czat");
    const pole = el.querySelector("textarea"), plik = el.querySelector("input[type=file]");
    pole.value = ls.get(LS_SZKICE, {})[id] || "";
    dopasuj(pole);
    pole.addEventListener("input", () => { dopasuj(pole); zapiszSzkic(); });
    pole.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey && !e.isComposing && !dotyk) { e.preventDefault(); wyslij(); }
    });
    pole.addEventListener("paste", (e) => {
      const pliki = [...(e.clipboardData?.files || [])];
      if (pliki.length) { e.preventDefault(); pliki.forEach(dodajPlik); }
    });
    el.addEventListener("dragover", (e) => { if (e.dataTransfer?.types?.includes("Files")) { e.preventDefault(); el.classList.add("upusc"); } });
    el.addEventListener("dragleave", (e) => { if (!el.contains(e.relatedTarget)) el.classList.remove("upusc"); });
    el.addEventListener("drop", (e) => { e.preventDefault(); el.classList.remove("upusc"); [...(e.dataTransfer?.files || [])].forEach(dodajPlik); });
    el.querySelector(".cz-forma").addEventListener("submit", (e) => { e.preventDefault(); wyslij(); });
    el.querySelector(".cz-plik").addEventListener("click", () => plik.click());
    plik.addEventListener("change", () => { [...plik.files].forEach(dodajPlik); plik.value = ""; });
    el.querySelector(".cz-mikro").addEventListener("click", nagraj);
    el.querySelector(".cz-stop").addEventListener("click", () => zatrzymaj(true));
    el.querySelector(".cz-anuluj").addEventListener("click", () => zatrzymaj(false));
    el.querySelector(".cz-re .cz-x").addEventListener("click", () => ustawOdpowiedz(null));
    el.addEventListener("click", klikWLiscie);
    // lista „przyklejona” do dołu: nowe wiadomości, załączniki i baner nie chowają ostatniej wiadomości
    const box = el.querySelector(".cz-lista");
    box.addEventListener("scroll", () => { przyklejony = box.scrollHeight - box.scrollTop - box.clientHeight < 80; }, { passive: true });
    obserwator?.disconnect();
    if (window.ResizeObserver) { obserwator = new ResizeObserver(() => { if (przyklejony) box.scrollTop = box.scrollHeight; }); obserwator.observe(box); }
  }
  function dopasuj(pole) { pole.style.height = "auto"; pole.style.height = Math.min(pole.scrollHeight, 180) + "px"; }
  function zapiszSzkic() {
    if (!el || !biezacy) return;
    const sz = ls.get(LS_SZKICE, {}); sz[biezacy] = el.querySelector("textarea").value; ls.set(LS_SZKICE, sz);
  }

  /* ---------------- render listy ---------------- */
  function lista() {
    const zSerwera = new Set(wiadomosci.map((w) => w.id));
    const moje = wyslane().filter((w) => w.do === biezacy && !zSerwera.has(w.id));
    return [...wiadomosci, ...moje].sort((a, b) => czasMs(a.czas) - czasMs(b.czas));
  }
  function render(wymus) {
    if (!el) return;
    const o = osoba(biezacy), wsz = lista();
    const pisze = htmlPisze(o, wsz);
    const nowyPodpis = wsz.map((w) => `${w.id}:${w.stan || ""}`).join(",") + "|" + pisze + "|" + (zbudowano || "");
    if (!wymus && nowyPodpis === podpis) return;
    podpis = nowyPodpis;
    const box = el.querySelector(".cz-lista");
    if (wymus) przyklejony = true;
    box.innerHTML = (wsz.length ? "" : htmlPowitanie(o)) + wsz.map((w, i) => htmlDzien(w, wsz[i - 1]) + htmlWiadomosc(w, o)).join("") + pisze;
    const naDol = () => { if (przyklejony) box.scrollTop = box.scrollHeight; };
    naDol();
    box.querySelectorAll("img, video").forEach((m) => { m.addEventListener("load", naDol, { once: true }); m.addEventListener("loadedmetadata", naDol, { once: true }); });
  }
  function htmlPowitanie(o) {
    const czym = o.id === "klaudiusz" ? "Napisz, co trzeba zrobić – Klaudiusz rozdzieli pracę w zespole." : `Napisz, czego potrzebujesz – ${esc(o.imie)} dostanie wiadomość od razu.`;
    return `<div class="cz-pusto">👋 To początek rozmowy z ${esc(o.emoji || "")} <b>${esc(o.imie)}</b>.<br>${czym}<br><span class="male">Możesz wkleić zdjęcie (Ctrl+V), dodać plik 📎 albo nagrać głosówkę 🎤.</span></div>`;
  }
  function htmlDzien(w, poprz) {
    const d = (x) => new Intl.DateTimeFormat("pl-PL", { timeZone: "Europe/Warsaw", weekday: "long", day: "numeric", month: "long" }).format(new Date(x.czas));
    if (!w.czas || (poprz && d(poprz) === d(w))) return "";
    return `<div class="cz-dzien"><span>${esc(d(w))}</span></div>`;
  }
  function tekstPablo(t) {
    return esc(t || "").replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>').replace(/\n/g, "<br>");
  }
  function htmlPlik(p) {
    const url = p.url || "", nazwa = esc(p.nazwa || (p.sciezka || "plik").split("/").pop()), typ = p.typ || "";
    const tr = p.transkrypcja ? `<div class="cz-transkr">🎤 „${esc(p.transkrypcja)}”</div>` : "";
    if (!url) return `<span class="cz-plik-link">📎 ${nazwa} <small>(w archiwum)</small></span>`;
    if (typ.startsWith("image/")) return `<a class="cz-obraz" href="${esc(url)}" target="_blank" rel="noopener"><img src="${esc(url)}" alt="${nazwa}" loading="lazy"></a>`;
    if (typ.startsWith("audio/")) return `<div class="cz-audio"><audio controls preload="none" src="${esc(url)}"></audio>${tr}</div>`;
    if (typ.startsWith("video/")) return `<video class="cz-wideo" controls preload="metadata" src="${esc(url)}"></video>`;
    if (/\.md$/i.test(p.sciezka || p.nazwa || "")) return `<button type="button" class="plik cz-plik-link" data-plik="${esc(url)}" data-tytul="${esc(p.sciezka || p.nazwa)}">📄 ${nazwa}<small>kliknij, żeby przeczytać</small></button>`;
    return `<a class="cz-plik-link" href="${esc(url)}" target="_blank" rel="noopener" download>📎 ${nazwa}${p.rozmiar ? ` <small>${rozmiarTxt(p.rozmiar)}</small>` : ""}</a>`;
  }
  function htmlStan(w) {
    if (w.stan === "wysylam") return ` · <span class="cz-stan">⏳ wysyłam…</span>`;
    if (w.stan === "dostarczone") return ` · <span class="cz-stan" title="Listonosz zabrał wiadomość – za chwilę trafi do adresata">✓ wysłane</span>`;
    if (w.stan === "blad") return ` · <span class="cz-stan blad">❌ ${esc(w.blad || "nie wysłano")}</span> <button type="button" class="cz-mini" data-cz-ponow="${esc(w.id)}">↻ Ponów</button> <button type="button" class="cz-mini" data-cz-usun="${esc(w.id)}">Usuń</button>`;
    return ` · <span class="cz-stan ok" title="Wiadomość zapisana w archiwum – adresat ją dostał">✓✓ dostarczone</span>`;
  }
  function htmlWiadomosc(w, o) {
    const moja = w.od === "pablo";
    const etyk = { prosba: "🙋 Prośba do Ciebie", koniec: "✅ Zrobione", info: "ℹ️ Informacja", test: "🔌 Test połączenia" }[w.typ] || "";
    const re = w.re_tekst ? `<blockquote class="cz-cytat">↩ ${esc(w.re_tekst)}</blockquote>` : "";
    const tresc = !w.tekst ? "" : moja ? `<div class="cz-tekst">${tekstPablo(w.tekst)}</div>` : `<div class="cz-tekst md">${renderMd(w.tekst)}</div>`;
    const pliki = (w.pliki?.length ? w.pliki : w.zalaczniki || []).map(htmlPlik).join("");
    const odp = !moja && w.typ === "prosba" ? ` <button type="button" class="cz-mini" data-cz-odpowiedz="${esc(w.id)}">↩ Odpowiedz</button>` : "";
    return `<div class="cz-w ${moja ? "moja" : "jego"}${w.typ ? " typ-" + esc(w.typ) : ""}" data-id="${esc(w.id)}">
      <div class="cz-dymek">${etyk ? `<div class="cz-etyk">${etyk}</div>` : ""}${re}${tresc}${pliki ? `<div class="cz-pliki">${pliki}</div>` : ""}</div>
      <div class="cz-meta">${moja ? "Ty" : `${esc(o.emoji || "")} ${esc(o.imie)}`} · <time title="${esc(w.czas)}">${esc(kiedy(w.czas))}</time>${moja ? htmlStan(w) : ""}${odp}</div></div>`;
  }
  function htmlPisze(o, wsz) {
    const ost = wsz.at(-1);
    if (!ost || ost.od !== "pablo" || ost.stan === "blad" || ost.stan === "wysylam") return "";
    if (Date.now() - czasMs(ost.czas) > 45 * 60e3) return "";
    const kropki = `<span class="kropki"><i></i><i></i><i></i></span>`;
    if (!ost.stan && stanEf(o) === "pracuje") return `<div class="cz-pisze">✍️ ${esc(o.imie)} pracuje nad tym ${kropki}</div>`;
    if (!ost.stan) return `<div class="cz-pisze">📨 ${esc(o.imie)} odebrał${forma(o)} wiadomość – odpowiedź pojawi się tutaj ${kropki}</div>`;
    return `<div class="cz-pisze">📨 Wiadomość w drodze – ${esc(o.imie)} dostanie ją za ok. 2 minuty ${kropki}</div>`;
  }

  function klikWLiscie(e) {
    const ponow = e.target.closest("[data-cz-ponow]");
    if (ponow) { const w = wyslane().find((x) => x.id === ponow.dataset.czPonow); if (w) { aktualizujWyslana(w.id, { stan: "wysylam", blad: "" }); doSerwera(w); } return; }
    const usun = e.target.closest("[data-cz-usun]");
    if (usun) { zapiszWyslane(wyslane().filter((x) => x.id !== usun.dataset.czUsun)); render(true); return; }
    const odp = e.target.closest("[data-cz-odpowiedz]");
    if (odp) { const w = wiadomosci.find((x) => x.id === odp.dataset.czOdpowiedz); if (w) ustawOdpowiedz({ id: w.id, tekst: w.tekst }); }
  }
  function ustawOdpowiedz(r) {
    odpowiedz = r && r.tekst ? { id: r.id || "", tekst: String(r.tekst).slice(0, 500) } : null;
    if (!el) return;
    const box = el.querySelector(".cz-re");
    box.hidden = !odpowiedz;
    if (odpowiedz) box.querySelector("span").textContent = `↩ Odpowiadasz na: „${odpowiedz.tekst.length > 140 ? odpowiedz.tekst.slice(0, 140) + "…" : odpowiedz.tekst}”`;
    if (odpowiedz && !dotyk) el.querySelector("textarea").focus();
  }

  /* ---------------- załączniki ---------------- */
  function renderZal() {
    if (!el) return;
    el.querySelector(".cz-zal").innerHTML = zalaczniki.map((z) => `<span class="cz-chip ${z.stan}" title="${esc(z.blad || z.nazwa)}">
      ${z.podglad ? `<img src="${esc(z.podglad)}" alt="">` : `<i>${z.typ.startsWith("audio/") ? "🎤" : z.typ.startsWith("video/") ? "🎬" : "📎"}</i>`}
      <span>${esc(z.nazwa)}<small>${z.stan === "wysylam" ? "wgrywam…" : z.stan === "blad" ? "❌ " + esc(z.blad) : rozmiarTxt(z.rozmiar)}</small></span>
      <button type="button" class="cz-x" data-cz-zal="${esc(z.lid)}" aria-label="Usuń załącznik">✕</button></span>`).join("");
    el.querySelectorAll("[data-cz-zal]").forEach((b) => b.addEventListener("click", () => {
      const z = zalaczniki.find((x) => x.lid === b.dataset.czZal); if (z?.podglad) URL.revokeObjectURL(z.podglad);
      zalaczniki = zalaczniki.filter((x) => x.lid !== b.dataset.czZal); renderZal();
    }));
  }
  async function zmniejsz(plik) {
    if (!/^image\/(jpeg|png|webp)$/.test(plik.type) || !window.createImageBitmap) return plik;
    const bmp = await createImageBitmap(plik).catch(() => null);
    if (!bmp) return plik;
    const skala = Math.min(1, 2000 / Math.max(bmp.width, bmp.height));
    if (skala === 1 && plik.size < 1_500_000) return plik;
    const c = document.createElement("canvas");
    c.width = Math.round(bmp.width * skala); c.height = Math.round(bmp.height * skala);
    const g = c.getContext("2d"); g.fillStyle = "#fff"; g.fillRect(0, 0, c.width, c.height); g.drawImage(bmp, 0, 0, c.width, c.height);
    const blob = await new Promise((ok) => c.toBlob(ok, "image/jpeg", 0.86));
    return blob ? new File([blob], plik.name.replace(/\.\w+$/, "") + ".jpg", { type: "image/jpeg" }) : plik;
  }
  async function dodajPlik(plik) {
    if (!el) return;
    const hhmm = new Intl.DateTimeFormat("pl-PL", { timeZone: "Europe/Warsaw", hour: "2-digit", minute: "2-digit" }).format(new Date()).replace(":", "");
    let nazwa = plik.name && !/^image\.\w+$/i.test(plik.name) ? plik.name : `zdjecie-${hhmm}.${(plik.type.split("/")[1] || "bin").replace("jpeg", "jpg")}`;
    const z = { lid: Math.random().toString(36).slice(2), nazwa, typ: plik.type || "application/octet-stream", rozmiar: plik.size, stan: "wysylam" };
    zalaczniki.push(z); renderZal();
    const dlaKogo = biezacy;
    try {
      const dane = await zmniejsz(plik);
      if (dane !== plik) { z.nazwa = nazwa.replace(/\.\w+$/, "") + ".jpg"; }
      z.typ = dane.type || z.typ; z.rozmiar = dane.size;
      if (z.typ.startsWith("image/")) z.podglad = URL.createObjectURL(dane);
      renderZal();
      if (dane.size > MAX_PLIK) throw new Error("za duży – max 4 MB");
      const r = await fetch(`/api/plik?do=${encodeURIComponent(dlaKogo)}&nazwa=${encodeURIComponent(z.nazwa)}`, {
        method: "POST", headers: { "content-type": z.typ, "x-biuro": "1" }, body: dane,
      });
      const d = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(d.blad || `błąd ${r.status}`);
      Object.assign(z, { url: d.url, stan: "ok", nazwa: d.nazwa || z.nazwa });
    } catch (e) { z.stan = "blad"; z.blad = e.message || "nie wgrano"; }
    renderZal();
  }

  /* ---------------- nagrywanie głosu (MediaRecorder) + dyktowanie (rozpoznawanie mowy w przeglądarce, jeśli jest) ---------------- */
  async function nagraj() {
    if (nagrywanie) return zatrzymaj(true);
    if (!navigator.mediaDevices?.getUserMedia || !window.MediaRecorder) { toast("Ta przeglądarka nie nagrywa dźwięku – spróbuj w Chrome albo Safari."); return; }
    let strumien;
    try { strumien = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true } }); }
    catch { toast("Brak dostępu do mikrofonu – zezwól na mikrofon dla tej strony (ikonka 🔒 obok adresu)."); return; }
    const mime = ["audio/webm;codecs=opus", "audio/mp4", "audio/ogg;codecs=opus", "audio/webm"].find((m) => MediaRecorder.isTypeSupported?.(m)) || "";
    const rec = new MediaRecorder(strumien, mime ? { mimeType: mime, audioBitsPerSecond: 48000 } : undefined);
    const n = nagrywanie = { rec, strumien, kawalki: [], start: Date.now(), gotowe: "", biezace: "", anuluj: false, koniec: false, rozp: null, tik: null };
    rec.ondataavailable = (e) => { if (e.data?.size) n.kawalki.push(e.data); };
    rec.onstop = () => {
      const typ = (rec.mimeType || mime || "audio/webm").split(";")[0];
      const blob = new Blob(n.kawalki, { type: typ });
      const sek = Math.round((Date.now() - n.start) / 1000);
      clearInterval(n.tik);
      if (!n.anuluj && blob.size > 1000) {
        const ext = typ.includes("mp4") ? "m4a" : typ.includes("ogg") ? "ogg" : "webm";
        const hhmm = new Intl.DateTimeFormat("pl-PL", { timeZone: "Europe/Warsaw", hour: "2-digit", minute: "2-digit" }).format(new Date()).replace(":", "");
        dodajPlik(new File([blob], `nagranie-${hhmm}-${sek}s.${ext}`, { type: typ }));
        const tekst = (n.gotowe + " " + n.biezace).trim();
        if (tekst && el) { const pole = el.querySelector("textarea"); pole.value = (pole.value ? pole.value.trimEnd() + "\n" : "") + "🎤 " + tekst; dopasuj(pole); zapiszSzkic(); }
      }
      if (nagrywanie === n) nagrywanie = null;
      pasekNagrania();
    };
    rec.start(1000);
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SR) {
      try {
        const r = new SR(); r.lang = "pl-PL"; r.continuous = true; r.interimResults = true;
        r.onresult = (e) => {
          let tymcz = "";
          for (let i = e.resultIndex; i < e.results.length; i++) {
            if (e.results[i].isFinal) n.gotowe += " " + e.results[i][0].transcript; else tymcz += e.results[i][0].transcript;
          }
          n.biezace = tymcz; pasekNagrania();
        };
        r.onerror = () => {};
        r.onend = () => { if (!n.koniec && nagrywanie === n) { try { r.start(); } catch { /* koniec */ } } };
        r.start(); n.rozp = r;
      } catch { n.rozp = null; }
    }
    n.tik = setInterval(() => { pasekNagrania(); if ((Date.now() - n.start) / 1000 > MAX_NAGRANIE_S) zatrzymaj(true); }, 500);
    pasekNagrania();
  }
  function zatrzymaj(zapisz) {
    const n = nagrywanie; if (!n) return;
    n.anuluj = !zapisz; n.koniec = true;
    try { n.rozp?.stop(); } catch { /* nic */ }
    try { if (n.rec.state !== "inactive") n.rec.stop(); } catch { /* nic */ }
    n.strumien.getTracks().forEach((t) => t.stop());
  }
  function pasekNagrania() {
    if (!el) return;
    const p = el.querySelector(".cz-nagr"), n = nagrywanie;
    p.hidden = !n;
    el.querySelector(".cz-mikro").classList.toggle("aktywny", !!n);
    if (!n) return;
    const s = Math.floor((Date.now() - n.start) / 1000);
    p.querySelector(".cz-czas").textContent = `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
    const t = (n.gotowe + " " + n.biezace).trim();
    p.querySelector(".cz-dykt").textContent = t ? `„${t.length > 90 ? "…" + t.slice(-90) : t}”` : (n.rozp ? "Mów – nagrywam i spisuję…" : "Mów – nagrywam…");
  }

  /* ---------------- wysyłka ---------------- */
  async function wyslij() {
    if (!el || !biezacy) return;
    if (nagrywanie) { zatrzymaj(true); setTimeout(wyslij, 600); return; }
    if (zalaczniki.some((z) => z.stan === "wysylam")) { toast("Chwilka – kończę wgrywać załączniki…"); setTimeout(wyslij, 1200); return; }
    const pole = el.querySelector("textarea");
    const tekst = pole.value.trim();
    const pliki = zalaczniki.filter((z) => z.stan === "ok").map(({ url, nazwa, typ, rozmiar }) => ({ url, nazwa, typ, rozmiar }));
    if (!tekst && !pliki.length) { if (zalaczniki.length) toast("Załącznik się nie wgrał – usuń go albo dodaj ponownie."); return; }
    const w = { id: noweId(), do: biezacy, od: "pablo", czas: new Date().toISOString(), typ: "wiadomosc", tekst, zalaczniki: pliki, stan: "wysylam",
      ...(odpowiedz ? { re: odpowiedz.id, re_tekst: odpowiedz.tekst } : {}) };
    zapiszWyslane([...wyslane(), w]);
    pole.value = ""; dopasuj(pole); zapiszSzkic();
    zalaczniki.forEach((z) => z.podglad && URL.revokeObjectURL(z.podglad));
    zalaczniki = []; renderZal(); ustawOdpowiedz(null);
    render(true);
    await doSerwera(w);
  }
  async function doSerwera(w) {
    try {
      const r = await fetch("/api/czat", { method: "POST", headers: { "content-type": "application/json", "x-biuro": "1" },
        body: JSON.stringify({ id: w.id, do: w.do, tekst: w.tekst, zalaczniki: w.zalaczniki, re: w.re, re_tekst: w.re_tekst }) });
      const d = await r.json().catch(() => ({}));
      if (r.ok) aktualizujWyslana(w.id, { stan: "dostarczone", czas: d.czas || w.czas });
      else {
        aktualizujWyslana(w.id, { stan: "blad", blad: d.opis || d.blad || `błąd ${r.status}` });
        if (d.blad === "brak_polaczenia") { polaczenie = { ...(polaczenie || {}), polaczony: false }; baner(); }
      }
    } catch { aktualizujWyslana(w.id, { stan: "blad", blad: "brak połączenia z internetem?" }); }
    szybkoDo = Date.now() + 4 * 60e3; planuj(2500);
  }

  /* ---------------- połączenie z Klaudiuszem (jednorazowo: token zadania „📨 Czat z biura”) ---------------- */
  async function sprawdzPolaczenie() {
    try { const r = await fetch("/api/ustawienia", { cache: "no-store" }); polaczenie = r.ok ? await r.json() : null; }
    catch { polaczenie = null; }
    baner();
  }
  function baner() {
    if (!el) return;
    const b = el.querySelector(".cz-baner");
    if (polaczenie === undefined || (polaczenie && polaczenie.polaczony)) { b.hidden = true; return; }
    b.hidden = false;
    if (polaczenie === null) { b.innerHTML = `<p>⚠️ Serwer czatu chwilowo nie odpowiada – wiadomości mogą nie dojść. Odśwież stronę za minutę.</p>`; return; }
    const link = esc(polaczenie.link || "https://claude.ai/code/routines");
    b.innerHTML = `<h4>🔌 Połącz czat z zespołem – jednorazowo, ok. 2 minut</h4>
      <ol>
        <li>Otwórz zadanie <b>„📨 Czat z biura (listonosz)”</b> w Claude: <a href="${link}" target="_blank" rel="noopener">otwórz ↗</a>
          <small>(jeśli link nie trafi – <a href="https://claude.ai/code/routines" target="_blank" rel="noopener">lista zadań</a> i kliknij „📨 Czat z biura (listonosz)”)</small></li>
        <li>Kliknij <b>Edytuj</b>. W polu z instrukcją usuń stary tekst i wklej nowy: <button type="button" class="cz-btn cz-kopiuj">📋 Kopiuj treść zadania</button></li>
        <li>Przy „Trigger” kliknij <b>+</b> → <b>API</b> → <b>Generate token</b>, skopiuj token (pokazuje się tylko raz) i zapisz zmiany.</li>
        <li>Wklej token tutaj:</li>
      </ol>
      <form class="cz-token"><input type="password" placeholder="sk-ant-…" autocomplete="off" spellcheck="false" aria-label="Token">
        <button type="submit" class="cz-btn">Połącz</button></form>
      <p class="cz-info male">Token zostaje zaszyfrowany na serwerze biura. Po połączeniu Klaudiusz odpisze w swoim oknie, że działa (ok. 2–3 min).</p>`;
    b.querySelector(".cz-kopiuj").addEventListener("click", async (e) => {
      const t = DANE.czat_prompt || "";
      try { await navigator.clipboard.writeText(t); e.target.textContent = "✅ Skopiowane – wklej w Claude"; }
      catch { window.prompt("Skopiuj ten tekst (Ctrl+C):", t); }
    });
    b.querySelector(".cz-token").addEventListener("submit", async (e) => {
      e.preventDefault();
      const inp = b.querySelector("input"), info = b.querySelector(".cz-info"), btn = b.querySelector("button");
      if (!inp.value.trim()) return;
      btn.disabled = true; info.textContent = "Sprawdzam token i budzę Klaudiusza…";
      try {
        const r = await fetch("/api/ustawienia", { method: "POST", headers: { "content-type": "application/json", "x-biuro": "1" }, body: JSON.stringify({ token: inp.value }) });
        const d = await r.json().catch(() => ({}));
        if (!r.ok) throw new Error(d.blad || `błąd ${r.status}`);
        polaczenie = { ...polaczenie, polaczony: true };
        b.innerHTML = `<p>✅ Połączone! Klaudiusz odpisze w swoim oknie za 2–3 minuty. Wiadomości, które się nie wysłały, wyślij ponownie (↻ Ponów).</p>`;
        szybkoDo = Date.now() + 4 * 60e3; planuj(3000);
        setTimeout(() => { if (polaczenie?.polaczony) b.hidden = true; }, 15000);
      } catch (err) { info.textContent = "❌ " + err.message; btn.disabled = false; }
    });
  }

  /* ---------------- odświeżanie ---------------- */
  async function pobierz() {
    if (!biezacy) return;
    const id = biezacy;
    try {
      let r = await fetch(`/api/na-zywo?co=czat&id=${encodeURIComponent(id)}`, { cache: "no-store" }).catch(() => null);
      if (!r || !r.ok) r = await fetch(`/czat/${encodeURIComponent(id)}.json`, { cache: "no-store" }); // zapas: kopia ze strony
      if (!r.ok) throw new Error(r.status);
      const d = await r.json();
      if (id !== biezacy) return;
      wiadomosci = d.wiadomosci || []; zbudowano = d.zbudowano;
      const zSerwera = new Set(wiadomosci.map((w) => w.id));
      if (wyslane().some((w) => zSerwera.has(w.id))) zapiszWyslane(wyslane().filter((w) => !zSerwera.has(w.id)));
      // nowa odpowiedź → odśwież też statusy (biurko, mapa)
      const ost = wiadomosci.at(-1);
      if (ost && ost.od !== "pablo" && DANE.czat?.[id]?.ostatnia?.id !== ost.id) wczytaj(false);
    } catch { /* brak pliku = jeszcze brak rozmowy */ wiadomosci = wiadomosci || []; }
    render(); oznaczPrzeczytane();
  }
  function planuj(za) {
    clearTimeout(timer);
    if (!biezacy) return;
    const szybko = Date.now() < szybkoDo;
    timer = setTimeout(async () => {
      if (!document.hidden) { await pobierz(); if (szybko && Math.random() < 0.34) wczytaj(false); }
      planuj();
    }, za ?? (szybko ? 4000 : 15000));
  }

  /* ---------------- API dla app.js ---------------- */
  function otworz(id, kontener) {
    if (biezacy === id && el && kontener.contains(el)) { render(); return; }
    if (nagrywanie) zatrzymaj(false);
    zapiszSzkic();
    zalaczniki = []; odpowiedz = null; wiadomosci = []; podpis = ""; zbudowano = null;
    biezacy = id;
    zbuduj(kontener, id);
    render(true);
    pobierz().then(() => render(true));
    if (polaczenie === undefined || polaczenie === null || !polaczenie.polaczony) sprawdzPolaczenie(); else baner();
    planuj();
    try { history.replaceState(null, "", "#czat-" + id); } catch { /* nic */ }
  }
  function zamknij() {
    if (nagrywanie) zatrzymaj(false);
    zapiszSzkic();
    clearTimeout(timer);
    biezacy = null; el = null; widac = false; obserwator?.disconnect(); obserwator = null;
    try { history.replaceState(null, "", location.pathname); } catch { /* nic */ }
  }
  function widoczny(tak) {
    widac = tak && !!biezacy;
    if (widac) { oznaczPrzeczytane(); if (!dotyk && el) setTimeout(() => el?.querySelector("textarea")?.focus({ preventScroll: true }), 50); }
  }
  document.addEventListener("visibilitychange", () => { if (!document.hidden && biezacy) { pobierz(); planuj(); } });

  return {
    otworz, zamknij, widoczny, nieprzeczytane,
    aktywny: () => !!biezacy && widac,
    odpowiedzNa: (r) => ustawOdpowiedz(r),
  };
})();

window.Czat = Czat;
