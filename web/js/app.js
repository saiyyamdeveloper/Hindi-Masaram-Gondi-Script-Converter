(function () {
  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));

  function toast(msg) {
    const el = $("#toast");
    el.textContent = msg;
    el.classList.add("show");
    clearTimeout(toast._t);
    toast._t = setTimeout(() => el.classList.remove("show"), 1600);
  }

  async function copyText(text) {
    try {
      await navigator.clipboard.writeText(text);
      toast("कॉपी हो गया");
    } catch (_) {
      toast("कॉपी नहीं हो सका");
    }
  }

  /* ---------- tabs ---------- */
  $$(".tabs button").forEach((btn) => {
    btn.addEventListener("click", () => {
      $$(".tabs button").forEach((b) => b.classList.remove("active"));
      $$(".panel").forEach((p) => p.classList.remove("active"));
      btn.classList.add("active");
      $("#panel-" + btn.dataset.tab).classList.add("active");
    });
  });

  /* ---------- converter ---------- */
  const input = $("#hi-in");
  const output = $("#gon-out");
  const smart = $("#smart-ra");
  const dirBtn = $("#dir-toggle");
  let hiToGon = true;

  function runConvert() {
    const src = input.value;
    const on = smart.checked;
    output.textContent = hiToGon
      ? Gondi.convert(src, on)
      : Gondi.convertReverse(src);
  }

  input.addEventListener("input", runConvert);
  smart.addEventListener("change", runConvert);

  $("#btn-copy").addEventListener("click", () => copyText(output.textContent || ""));
  $("#btn-clear").addEventListener("click", () => {
    input.value = "";
    runConvert();
    input.focus();
  });
  $("#btn-swap").addEventListener("click", () => {
    const a = input.value;
    const b = output.textContent;
    hiToGon = !hiToGon;
    input.value = b;
    dirBtn.textContent = hiToGon ? "देवनागरी → मसराम" : "मसराम → देवनागरी";
    $("#lbl-in").textContent = hiToGon ? "हिन्दी / देवनागरी लिखें" : "मसराम गोंडी लिखें";
    $("#lbl-out").textContent = hiToGon ? "मसराम गोंडी" : "देवनागरी";
    input.style.fontFamily = hiToGon
      ? "var(--deva)"
      : '"Masaram Gondi", var(--deva)';
    runConvert();
  });

  $$("#examples .chip").forEach((c) => {
    c.addEventListener("click", () => {
      hiToGon = true;
      dirBtn.textContent = "देवनागरी → मसराम";
      $("#lbl-in").textContent = "हिन्दी / देवनागरी लिखें";
      $("#lbl-out").textContent = "मसराम गोंडी";
      input.style.fontFamily = "var(--deva)";
      input.value = c.dataset.w;
      runConvert();
    });
  });

  /* ---------- keyboard ---------- */
  const kbOut = $("#kb-out");
  function insertAtCursor(el, text) {
    const start = el.selectionStart ?? el.value.length;
    const end = el.selectionEnd ?? el.value.length;
    el.value = el.value.slice(0, start) + text + el.value.slice(end);
    const pos = start + text.length;
    el.selectionStart = el.selectionEnd = pos;
    el.focus();
  }

  function makeKey(gondi, deva, extraClass) {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "key" + (extraClass ? " " + extraClass : "");
    b.innerHTML = '<span class="g">' + gondi + '</span><span class="d">' + (deva || "") + "</span>";
    b.addEventListener("click", () => insertAtCursor(kbOut, gondi));
    return b;
  }

  const sections = [
    ["स्वर", "vowels"],
    ["क-वर्ग", "ka"],
    ["च-वर्ग", "ca"],
    ["ट-वर्ग", "tta"],
    ["त-वर्ग", "ta"],
    ["प-वर्ग", "pa"],
    ["अन्त्य / ऊष्म", "ya"],
    ["संयुक्त", "conj"],
    ["मात्राएँ", "matra"],
    ["चिह्न", "signs"],
    ["अंक", "digits"],
  ];
  const host = $("#kb-host");
  sections.forEach(([title, key]) => {
    const box = document.createElement("div");
    box.className = "kb-section";
    box.innerHTML = "<h3>" + title + "</h3>";
    const row = document.createElement("div");
    row.className = "kb-row";
    Gondi.CHARSET[key].forEach((pair) => row.appendChild(makeKey(pair[0], pair[1])));
    box.appendChild(row);
    host.appendChild(box);
  });

  const util = document.createElement("div");
  util.className = "kb-section";
  util.innerHTML = "<h3>उपकरण</h3>";
  const urow = document.createElement("div");
  urow.className = "kb-row";
  const space = makeKey(" ", "स्पेस", "wide");
  space.querySelector(".g").textContent = "␣";
  space.addEventListener("click", () => insertAtCursor(kbOut, " "), true);
  const danda = makeKey("।", "दण्ड");
  const ddanda = makeKey("॥", "॥");
  const back = document.createElement("button");
  back.type = "button";
  back.className = "key danger wide";
  back.innerHTML = '<span class="g">⌫</span><span class="d">मिटाओ</span>';
  back.addEventListener("click", () => {
    const s = kbOut.selectionStart ?? kbOut.value.length;
    const e = kbOut.selectionEnd ?? kbOut.value.length;
    if (s !== e) {
      kbOut.value = kbOut.value.slice(0, s) + kbOut.value.slice(e);
      kbOut.selectionStart = kbOut.selectionEnd = s;
    } else if (s > 0) {
      const chars = Array.from(kbOut.value);
      // delete one unicode scalar before caret
      let acc = 0, idx = 0;
      for (let i = 0; i < chars.length; i++) {
        acc += chars[i].length;
        if (acc >= s) { idx = i; break; }
      }
      chars.splice(idx, 1);
      const next = chars.join("");
      // recompute caret
      kbOut.value = next;
      const newPos = Array.from(next).slice(0, idx).join("").length;
      kbOut.selectionStart = kbOut.selectionEnd = newPos;
    }
    kbOut.focus();
  });
  urow.append(space, danda, ddanda, back);
  util.appendChild(urow);
  host.appendChild(util);

  $("#kb-copy").addEventListener("click", () => copyText(kbOut.value));
  $("#kb-clear").addEventListener("click", () => { kbOut.value = ""; kbOut.focus(); });
  $("#kb-to-hi").addEventListener("click", () => {
    const hi = Gondi.convertReverse(kbOut.value);
    toast(hi || "खाली");
    copyText(hi);
  });

  /* ---------- dictionary ---------- */
  const dict = (window.GONDI_DICTIONARY && window.GONDI_DICTIONARY.entries) || [];
  const cats = ["सभी"].concat((window.GONDI_DICTIONARY && window.GONDI_DICTIONARY.categories) || []);
  let activeCat = "सभी";

  const filters = $("#filters");
  cats.forEach((c) => {
    const b = document.createElement("button");
    b.textContent = c;
    if (c === "सभी") b.classList.add("on");
    b.addEventListener("click", () => {
      activeCat = c;
      $$("#filters button").forEach((x) => x.classList.remove("on"));
      b.classList.add("on");
      renderDict();
    });
    filters.appendChild(b);
  });

  function renderDict() {
    const q = ($("#q").value || "").trim().toLowerCase();
    const list = $("#dict-list");
    list.innerHTML = "";
    const rows = dict.filter((e) => {
      if (activeCat !== "सभी" && e.category !== activeCat) return false;
      if (!q) return true;
      const blob = [e.hindi, e.english, e.gondi_deva, e.gondi_masaram, e.hindi_gondi, e.note]
        .join(" ").toLowerCase();
      return blob.indexOf(q) !== -1;
    });
    $("#dict-count").textContent = rows.length + " शब्द";
    rows.forEach((e) => {
      const div = document.createElement("div");
      div.className = "dict-item";
      div.innerHTML =
        '<div><div class="hi">' + e.hindi +
        ' <span class="cat-pill">' + e.category + "</span></div>" +
        '<div class="en">' + e.english + " · गोंडी: " + e.gondi_deva + "</div>" +
        '<div class="meta">' + e.note + "</div></div>" +
        '<div><div class="gon" title="गोंडी भाषा, मसराम लिपि">' + e.gondi_masaram + "</div>" +
        '<div class="meta">हिन्दी लिप्यंतरण: <span class="gon" style="font-size:18px">' +
        e.hindi_gondi + "</span></div></div>";
      div.addEventListener("click", () => copyText(e.gondi_masaram));
      list.appendChild(div);
    });
  }
  $("#q").addEventListener("input", renderDict);
  renderDict();

  /* ---------- mapping ---------- */
  function fillTable(id, rows) {
    const tb = $("#" + id);
    tb.innerHTML = rows.map((r) =>
      "<tr><td>" + r[1] + '</td><td class="gcell">' + r[0] +
      "</td><td><code>U+" + r[0].codePointAt(0).toString(16).toUpperCase() +
      "</code></td></tr>"
    ).join("");
  }
  fillTable("map-vowels", Gondi.CHARSET.vowels);
  fillTable("map-cons", [].concat(Gondi.CHARSET.ka, Gondi.CHARSET.ca, Gondi.CHARSET.tta, Gondi.CHARSET.ta, Gondi.CHARSET.pa, Gondi.CHARSET.ya));
  fillTable("map-matra", Gondi.CHARSET.matra);
  fillTable("map-signs", Gondi.CHARSET.signs.concat(Gondi.CHARSET.conj));
  fillTable("map-digits", Gondi.CHARSET.digits);

  runConvert();
})();
