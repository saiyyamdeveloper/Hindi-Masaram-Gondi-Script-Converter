## Hindi → Masaram Gondi Script Converter

![Masaram Gondi Hindi Converter](masaram-gondi-converter.jpg)
# देवनागरी → मसराम गोंडी

[![Converter tests](https://github.com/saiyyamdeveloper/Hindi-Masaram-Gondi-Script-Converter/actions/workflows/test.yml/badge.svg)](https://github.com/saiyyamdeveloper/Hindi-Masaram-Gondi-Script-Converter/actions/workflows/test.yml)
[![Pages](https://github.com/saiyyamdeveloper/Hindi-Masaram-Gondi-Script-Converter/actions/workflows/pages.yml/badge.svg)](https://github.com/saiyyamdeveloper/Hindi-Masaram-Gondi-Script-Converter/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-d4a017.svg)](LICENSE)

Munshi Mangal Singh Masaram (1918) ki lipi. Unicode block **U+11D00–U+11D5F** — **75 characters**.

**Live app (Primary):** [https://saiyyamdeveloper.github.io/Hindi-Masaram-Gondi-Script-Converter/](https://saiyyamdeveloper.github.io/Hindi-Masaram-Gondi-Script-Converter/)
**Mirror (old):** [https://aimanage750.github.io/masaram-gondi/](https://aimanage750.github.io/masaram-gondi/)

**Source (Primary):** [github.com/saiyyamdeveloper/Hindi-Masaram-Gondi-Script-Converter](https://github.com/saiyyamdeveloper/Hindi-Masaram-Gondi-Script-Converter)
**Mirror:** [github.com/aimanage750/masaram-gondi](https://github.com/aimanage750/masaram-gondi)

> Username update: `aimanage750 → saiyyamdeveloper` — dono URLs active hain, primary ab `saiyyamdeveloper` hai.

Hindi type karo — Masaram Gondi nikalta hai. Saath mein 75-key keyboard, FlorisBoard/HeliBoard layouts, Kotlin IME converter, aur Hindi–Gondi dictionary.

---

## Demo

```
मसराम     →  𑴤𑴫𑴦𑴱𑴤
गोंडी     →  𑴎𑴽𑵀𑴘𑴳
नमस्ते    →  𑴟𑴤𑴫𑵅𑴛𑴺
भारत      →  𑴣𑴱𑴦𑴛
हिन्दी    →  𑴬𑴲𑴟𑵅𑴝𑴳
जय हिन्द  →  𑴓𑴥 𑴬𑴲𑴟𑵅𑴝
क्षेत्र   →  𑴮𑴺𑴰
पानी      →  𑴠𑴱𑴟𑴳
घर        →  𑴏𑴦
कर्म      →  𑴌𑵆𑴤      (Repha)
क्रम      →  𑴌𑵇𑴤      (Ra-kara)
```

`नमस्ते` me virama `𑵅` zaroori hai (स् + त). Bina virama wala purana draft galat tha.

## Repo map

| Path | Kya hai |
|---|---|
| [`web/`](web/) | Live converter + 75-key keyboard + dictionary UI |
| [`florisboard/`](florisboard/) | Phonetic + InScript layouts (HeliBoard / FlorisBoard) |
| [`converter/python/`](converter/python/) | CLI + golden tests |
| [`converter/kotlin/`](converter/kotlin/) | Android IME live converter |
| [`converter/mapping.json`](converter/mapping.json) | Complete 1:1 map |
| [`dictionary/`](dictionary/) | 108 everyday Hindi ↔ Gondi words |
| [`web/android-guide.html`](web/android-guide.html) | Full Android + Web visual guide |

---

## 🌐 Web Converter Guide — Bina install ke + Local

### Option 1 — Online (GitHub Pages) — Sabse easy
Koi install nahi, browser me kholo:

**Primary:** `https://saiyyamdeveloper.github.io/Hindi-Masaram-Gondi-Script-Converter/`
**Mirror:** `https://aimanage750.github.io/masaram-gondi/`

**Tabs ka use:**
- **लिखो** — बायें Hindi type karo, दायें तुरंत Gondi निकलेगा। Chip se example (`मसराम`, `नमस्ते`, `क्षेत्र`) try karo। `कॉपी` / `⇄ उलटो` (Gondi→Devanagari) / `स्मार्ट र` toggle available hai।
- **कुंजी · ७५** — Poore 75 akshar ka on-screen keyboard। Gondi me type karo → `देवनागरी में देखो` se reverse check।
- **शब्दकोश** — 108 Hindi↔Gondi shabd (पानी=ईर→𑴃𑴦, घर=रोन→𑴦𑴽𑴟)। Search + category filter, card dabao = copy।
- **मानचित्र** — Saare 1:1 Devanagari→Gondi map, virama 𑵅 / halanta 𑵄 / repha 𑵆 / ra-kara 𑵇 samjho।

> Bina `Noto Sans Masaram Gondi` font ke boxes (□) dikhenge — web me font bundled hai (`web/fonts/NotoSansMasaramGondi-Regular.ttf`), isliye online sahi dikhega।

### Option 2 — Local (Laptop par offline)

```bash
# 1) Clone
git clone https://github.com/saiyyamdeveloper/Hindi-Masaram-Gondi-Script-Converter.git
cd Hindi-Masaram-Gondi-Script-Converter

# 2) Converter test (golden tests — sab pass hona chahiye)
python3 converter/python/devanagari_to_masaram_gondi.py --test
# → मसराम → 𑴤𑴫𑴦𑴱𑴤 ... ALL PASSED

# 3) CLI se convert
python3 converter/python/devanagari_to_masaram_gondi.py "जय हिन्द"
# → 𑴓𑴥 𑴬𑴲𑴟𑵅𑴝

# 4) Web converter local run
python3 -m http.server 8765 --directory web --bind 127.0.0.1
# Browser me: http://127.0.0.1:8765
```

**CLI options:**
```bash
python3 converter/python/devanagari_to_masaram_gondi.py --help  # (default: smart_ra ON)
# Reverse:
python3 -c "from converter.python.devanagari_to_masaram_gondi import convert_reverse; print(convert_reverse('𑴟𑴤𑴫𑵅𑴛𑴺'))" # → नमस्ते
```

---

## 📱 Android Install Guide — Dono Option chalte hain

### Option A — Direct Gondi type (No-code, HeliBoard) — 5 min
User **सीधे गोंडी keys** (`𑴌 𑴟 𑴤`) dabake likhega। Hindi aana zaroori nahi।

**Step 1 — HeliBoard install karo**
- Play Store me “HeliBoard” search karo ya F-Droid se `heliboard-*.apk` lo।
- Install ke baad: `Settings → System → Languages & input → On-screen keyboard` → HeliBoard **Enable** aur **Default** banao।
- *FlorisBoard v0.4* me extension abhi partial hai — HeliBoard recommended, FlorisBoard v0.5 me same ZIP chalega।

**Step 2 — Font install karo (sabse zaroori)**
- File: `web/fonts/NotoSansMasaramGondi-Regular.ttf` (SIL OFL) download karo।
- File Manager me TTF kholo → **Install** दबाओ।
- Ya `Settings → Display → Font` me add karo (Samsung/Xiaomi me “zFont 3” app se bina root ke install hota hai)।
- Sabse reliable: App/APK me font bundle karo (Option B dekho)।
- Bina font ke Gondi □□□ dikhegi — converter sahi hai, sirf display missing hai।

**Step 3 — Extension ZIP import karo**
- File: `florisboard/layouts/characters/masaram_gondi.json` (Phonetic) + `masaram_gondi_inscript.json` (InScript) + `extension.json`
- Ready ZIP: `web/masaram-gondi-florisboard-v1.0.0.zip` (is repo me)
- HeliBoard me: `Settings → Languages & layouts → Add keyboard → Import` → ZIP select karo।
- Ya manual: `Settings → Advanced → Custom layout → Paste JSON` → `masaram_gondi.json` ka pura content paste karo।
- Dono layouts dikhenge:
  - `𑴤𑴫𑴦𑴱𑴤 𑴎𑴽𑵀𑴘𑴳 (Phonetic)` — Hindi QWERTY jaisa `क→𑴌`, Hindi typist ke liye
  - `𑴤𑴫𑴦𑴱𑴤 𑴎𑴽𑵀𑴘𑴳 (InScript)` — Sarkari InScript muscle-memory

**Step 4 — Language enable karo**
- HeliBoard → `Languages → Masaram Gondi` enable karo। Globe 🌐 se keyboard switch kar sako ge।

**Step 5 — Type karo (Shift / Long-press)**
- Har key: `lower` = normal, `upper` = Shift, popup = long-press।
- Virama `𑵅` (11D45) = yuktakshar banata hai (`स् + त → स्त`), Halanta `𑵄` (11D44) = shabd-ant par vowel kill।
- Repha `𑵆` / Ra-kara `𑵇` — `कर्म → 𑴌𑵆𑴤` vs `क्रम → 𑴌𑵇𑴤`
- Test: `𑴤𑴫𑴦𑴱𑴤 𑴎𑴽𑵀𑴘𑴳 · 𑴟𑴤𑴫𑵅𑴛𑴺 𑴣𑴱𑴦𑴛 · 𑴮𑴺𑴰` sahi dikhe to font OK।

### Option B — Hindi type → Auto Gondi (Kotlin IME) — Developer ke liye
User **Hindi (Devanagari) me type kare**, IME **turant Gondi** me badal de — `नमस्ते` → `𑴟𑴤𑴫𑵅𑴛𑴺`

**Step 1 — File copy karo**
```bash
# Android Studio → New Project → Empty Activity (Kotlin)
# Copy:
app/src/main/java/org/masaram/gondi/DevanagariToMasaramGondi.kt  ← converter/kotlin/
app/src/main/assets/fonts/NotoSansMasaramGondi-Regular.ttf
```

**Step 2 — Commit se pehle convert (sabse simple)**
```kotlin
import org.masaram.gondi.DevanagariToMasaramGondi

class GondiInputMethod : InputMethodService() {
    private val ic get() = currentInputConnection
    fun onHindiCommitted(hindi: String) {
        val gondi = DevanagariToMasaramGondi.convert(hindi) // कर्म→𑴌𑵆𑴤, क्रम→𑴌𑵇𑴤 auto
        ic?.commitText(gondi, 1)
    }
}
```

**Step 3 — Live replace (current word ko Gondi me badlo)**
```kotlin
fun onUpdateSelection(...) {
    val before = ic?.getTextBeforeCursor(64, 0)?.toString() ?: return
    val pair = DevanagariToMasaramGondi.convertLastWord(before) ?: return
    val wordLen = before.length - pair.first
    if (before.substring(pair.first) == pair.second) return // loop se bacho
    ic?.deleteSurroundingText(wordLen, 0)
    ic?.commitText(pair.second, 1)
}
```

**Step 4 — Font bundling (boxes se bacho)**
```kotlin
val tf = Typeface.createFromAsset(assets, "fonts/NotoSansMasaramGondi-Regular.ttf")
keyView.typeface = tf
// WebView me CSS: @font-face { font-family:'Gondi'; src:url('fonts/NotoSansMasaramGondi-Regular.ttf'); }
```

**Step 5 — Build & Install**
```bash
# AndroidManifest me:
# <service android:name=".GondiInputMethod" android:permission="android.permission.BIND_INPUT_METHOD">
#   <intent-filter><action android:name="android.view.InputMethod" /></intent-filter>
# </service>
# Build → APK → adb install app-debug.apk
# Settings → Languages & input → Gondi IME enable
```

> Dono Android options active hain — **A:** direct Gondi keys (75 chars, HeliBoard) **B:** Hindi→Gondi auto (Kotlin). Detail visual guide: `web/android-guide.html`

**Quick check — Phone sahi dikha raha hai?**
```
𑴤𑴫𑴦𑴱𑴤 𑴎𑴽𑵀𑴘𑴳 · 𑴟𑴤𑴫𑵅𑴛𑴺 𑴣𑴱𑴦𑴛 · 𑴮𑴺𑴰
मसराम गोंडी · नमस्ते भारत · क्षेत्र
```
Boxes dikhe → font reinstall / bundle karo।

---

## GitHub Pages

**Primary repo:** [saiyyamdeveloper/Hindi-Masaram-Gondi-Script-Converter](https://github.com/saiyyamdeveloper/Hindi-Masaram-Gondi-Script-Converter)

**Settings → Pages → Source: GitHub Actions**. Site:

`https://saiyyamdeveloper.github.io/Hindi-Masaram-Gondi-Script-Converter/`

**Mirror repo:** [aimanage750/masaram-gondi](https://github.com/aimanage750/masaram-gondi) → `https://aimanage750.github.io/masaram-gondi/`

Dono options active hain — primary `saiyyamdeveloper` hai। Pages workflow `web/` folder ko deploy karta hai (`pages.yml`) aur tests har push par chalte hain (`test.yml`)।

## Smart रा

| Hindi | Rule | Gondi |
|---|---|---|
| र् + C (कर्म) | cluster-initial → **Repha 𑵆** | 𑴌𑵆𑴤 |
| C + ्र (क्रम) | cluster-final → **Ra-kara 𑵇** | 𑴌𑵇𑴤 |
| त्र क्ष ज्ञ | precomposed | 𑴰 𑴮 𑴯 |
| ् conjunct | **Virama 𑵅** | हिन्दी |
| ् vowel-kill | **Halanta 𑵄** | word-final dead C |

## Dictionary

Har entry mein dono hain:

- `hindi_gondi` — Hindi shabd ka lipyantaran (पानी → 𑴠𑴱𑴟𑴳)
- `gondi_masaram` — Gondi *bhasha* ka shabd (पानी = ईर → 𑴃𑴦, घर = रोन → 𑴦𑴽𑴟)

Gondi ki kai boliyaan hain (Adilabad, Bastar, Mandla). Yeh prchalit roop hain, ek official standard nahi। Web ke **शब्दकोश** tab me search + category filter hai।

## Font & license

- Code: [MIT](LICENSE)
- Font `web/fonts/NotoSansMasaramGondi-Regular.ttf`: [SIL OFL 1.1](web/fonts/OFL.txt)

Bina is font ke boxes (□) dikhenge। Web me font bundled hai, Android par manually install / APK me bundle karna padta hai।

---

**Help:** Issue kholo ya `web/android-guide.html` ka visual guide dekho — wahan 75 keys, shift/long-press, aur font troubleshooting screenshots ke saath hai।

