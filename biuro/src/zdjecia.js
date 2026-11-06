// 📸 Biblioteka zdjęć – Pablo wgrywa prawdziwe zdjęcia (tła / produkty / gotowe); trafiają do Zosi, która dopisuje je do biblioteki.
(() => {
  const $ = (s) => document.querySelector(s);
  const SEKCJE = {
    tla: ["Tła", "Prawdziwe tła: salon, taras, ogród, wnętrza – miejsca, w które wstawiamy produkty."],
    produkty: ["Produkty", "Prawdziwe zdjęcia produktów (leżak, stolik…) – najlepiej na prostym tle, cały produkt w kadrze."],
    gotowe: ["Gotowe ujęcia", "Prawdziwe zdjęcia gotowe do postów od razu – produkt w realnym miejscu."],
  };
  const MAX = 4_000_000, NA_WIADOMOSC = 12;
  let sekcja = "tla", zdjecia = [], kolejka = [];
  const esc = (t) => String(t ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  function toast(t) { const el = $("#toast"); el.textContent = t; el.hidden = false; clearTimeout(toast.t); toast.t = setTimeout(() => (el.hidden = true), 4000); }

  async function zmniejsz(plik) {
    if (!plik.type.startsWith("image/") || plik.type === "image/gif") return plik;
    try {
      const bmp = await createImageBitmap(plik);
      for (const [bok, q] of [[2560, 0.9], [2048, 0.85], [1600, 0.8]]) {
        const s = Math.min(1, bok / Math.max(bmp.width, bmp.height));
        const c = document.createElement("canvas");
        c.width = Math.round(bmp.width * s); c.height = Math.round(bmp.height * s);
        c.getContext("2d").drawImage(bmp, 0, 0, c.width, c.height);
        const b = await new Promise((r) => c.toBlob(r, "image/jpeg", q));
        if (b && b.size <= MAX) return new File([b], plik.name.replace(/\.\w+$/, "") + ".jpg", { type: "image/jpeg" });
      }
    } catch { /* przeglądarka nie odczytała – wyślij oryginał */ }
    return plik;
  }

  async function dodajPliki(lista) {
    for (const plik of lista) {
      const z = { nazwa: plik.name || "zdjecie.jpg", stan: "wgrywam", podglad: plik.type.startsWith("image/") ? URL.createObjectURL(plik) : "" };
      kolejka.push(z); rysujKolejke();
      try {
        const dane = await zmniejsz(plik);
        if (dane.size > MAX) throw new Error("za duży plik (max 4 MB) – filmy skróć albo wyślij w czacie");
        const r = await fetch(`/api/plik?do=grafika&nazwa=${encodeURIComponent(dane.name || z.nazwa)}`, {
          method: "POST", headers: { "content-type": dane.type || "application/octet-stream", "x-biuro": "1" }, body: dane });
        const d = await r.json().catch(() => ({}));
        if (!r.ok) throw new Error(d.blad || `błąd ${r.status}`);
        Object.assign(z, { stan: "ok", url: d.url, nazwa: d.nazwa, typ: d.typ, rozmiar: d.rozmiar });
      } catch (e) { z.stan = "blad"; z.blad = e.message; toast(`${z.nazwa}: ${e.message}`); }
      rysujKolejke();
    }
  }

  function rysujKolejke() {
    $("#kolejka").innerHTML = kolejka.map((z) => `<figure class="${z.stan}">${z.podglad ? `<img src="${z.podglad}" alt="">` : "🎬"}
      <figcaption>${z.stan === "wgrywam" ? "⏳ wgrywam" : z.stan === "ok" ? "✔ gotowe" : "✖ " + esc(z.blad)}</figcaption></figure>`).join("");
    const gotowe = kolejka.filter((z) => z.stan === "ok").length;
    const w = $("#wyslij");
    w.disabled = !gotowe || kolejka.some((z) => z.stan === "wgrywam");
    w.textContent = gotowe ? `📨 Dodaj do biblioteki (${gotowe})` : "📨 Dodaj do biblioteki";
  }

  $("#wyslij").onclick = async () => {
    const gotowe = kolejka.filter((z) => z.stan === "ok");
    const opis = $("#opis").value.trim();
    $("#wyslij").disabled = true;
    try {
      for (let i = 0; i < gotowe.length; i += NA_WIADOMOSC) {
        const paczka = gotowe.slice(i, i + NA_WIADOMOSC);
        const tekst = `📸 NOWE ZDJĘCIA DO BIBLIOTEKI – sekcja: ${sekcja} (${SEKCJE[sekcja][0]}), ${paczka.length} szt.` +
          (opis ? `\nOpis od Pablo: ${opis}` : "") +
          `\n\nZosia: dopisz je do biblioteki: python3 scripts/zdjecia.py dodaj --sekcja ${sekcja} <ścieżki załączników>` +
          (opis ? ` --opis "${opis.replace(/"/g, "'")}"` : "") + ` (obejrzyj każde i dopisz opis/tagi: zdjecia.py opisz). Nie odpisuj Pablo – wystarczy, że zdjęcia pojawią się w bibliotece.`;
        const r = await fetch("/api/czat", { method: "POST", headers: { "content-type": "application/json", "x-biuro": "1" },
          body: JSON.stringify({ do: "grafika", tekst, zalaczniki: paczka.map(({ url, nazwa, typ, rozmiar }) => ({ url, nazwa, typ, rozmiar })) }) });
        const d = await r.json().catch(() => ({}));
        if (!r.ok) throw new Error(d.opis || d.blad || r.status);
      }
      toast(`Wysłane ✔ – ${gotowe.length} zdj. Zosia dopisze je do biblioteki (pojawią się tu za kilka minut).`);
      kolejka = kolejka.filter((z) => z.stan !== "ok"); $("#opis").value = ""; rysujKolejke();
    } catch (e) { toast("Nie udało się: " + e.message); rysujKolejke(); }
  };

  const strefa = $("#strefa"), inp = $("#pliki");
  inp.onchange = () => { dodajPliki([...inp.files]); inp.value = ""; };
  strefa.ondragover = (e) => { e.preventDefault(); strefa.classList.add("nad"); };
  strefa.ondragleave = () => strefa.classList.remove("nad");
  strefa.ondrop = (e) => { e.preventDefault(); strefa.classList.remove("nad"); dodajPliki([...e.dataTransfer.files]); };

  function rysuj() {
    $("#nazwa-sekcji").textContent = SEKCJE[sekcja][0];
    $("#opis-sekcji").textContent = SEKCJE[sekcja][1];
    const lista = zdjecia.filter((z) => z.sekcja === sekcja);
    $("#galeria").innerHTML = lista.length ? "" : `<p class="pusto">Ta sekcja jest jeszcze pusta – wgraj pierwsze zdjęcia powyżej.</p>`;
    for (const z of lista) {
      const f = document.createElement("figure");
      f.className = "zdj";
      const film = /\.(mp4|mov)$/i.test(z.url);
      f.innerHTML = `${film ? `<video src="${esc(z.url)}" preload="metadata" controls></video>` : `<img src="${esc(z.url)}" alt="${esc(z.opis)}" loading="lazy">`}
        <figcaption><span>${esc(z.opis || z.nazwa)}</span>${z.tagi?.length ? `<span class="uzycia">${esc(z.tagi.join(" · "))}</span>` : ""}
        <span class="${z.uzycia ? "uzycia" : "nowe"}">${z.uzycia ? `użyte ${z.uzycia}×` : "jeszcze nieużyte"}</span></figcaption>`;
      const img = f.querySelector("img");
      if (img) img.onclick = () => { const l = $("#lupa"); l.querySelector("img").src = img.src; l.hidden = false; };
      $("#galeria").append(f);
    }
  }
  $("#sekcje").onclick = (e) => {
    const b = e.target.closest("button"); if (!b) return;
    sekcja = b.dataset.s;
    $("#sekcje").querySelectorAll("button").forEach((x) => x.classList.toggle("wl", x === b));
    rysuj();
  };
  $("#lupa").onclick = () => ($("#lupa").hidden = true);

  fetch("zdjecia.json", { cache: "no-cache" }).then((r) => r.json()).then((d) => { zdjecia = d.zdjecia || []; rysuj(); })
    .catch(() => { zdjecia = []; rysuj(); });
})();
