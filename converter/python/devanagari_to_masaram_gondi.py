#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Devanagari (Hindi) → Masaram Gondi converter
Unicode 1:1 phonetic mapping + conjuncts + repha/ra-kara.

Usage:
    python3 devanagari_to_masaram_gondi.py
    python3 devanagari_to_masaram_gondi.py "नमस्ते भारत"
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# 1:1 code-point map (Devanagari → Masaram Gondi)
# ---------------------------------------------------------------------------
DEVA2GONDI: dict[int, int] = {
    # Independent vowels (swar)
    0x0905: 0x11D00,  # अ → 𑴀
    0x0906: 0x11D01,  # आ → 𑴁
    0x0907: 0x11D02,  # इ → 𑴂
    0x0908: 0x11D03,  # ई → 𑴃
    0x0909: 0x11D04,  # उ → 𑴄
    0x090A: 0x11D05,  # ऊ → 𑴅
    0x090F: 0x11D06,  # ए → 𑴆
    0x0910: 0x11D08,  # ऐ → 𑴈
    0x0913: 0x11D09,  # ओ → 𑴉
    0x0914: 0x11D0B,  # औ → 𑴋
    # Short / candra independents (approx)
    0x090E: 0x11D06,  # ऎ → ए
    0x0912: 0x11D09,  # ऒ → ओ
    0x090D: 0x11D06,  # ऍ → ए  (candra applied separately if needed)
    # Consonants (vyanjan)
    0x0915: 0x11D0C,  # क
    0x0916: 0x11D0D,  # ख
    0x0917: 0x11D0E,  # ग
    0x0918: 0x11D0F,  # घ
    0x0919: 0x11D10,  # ङ
    0x091A: 0x11D11,  # च
    0x091B: 0x11D12,  # छ
    0x091C: 0x11D13,  # ज
    0x091D: 0x11D14,  # झ
    0x091E: 0x11D15,  # ञ
    0x091F: 0x11D16,  # ट
    0x0920: 0x11D17,  # ठ
    0x0921: 0x11D18,  # ड
    0x0922: 0x11D19,  # ढ
    0x0923: 0x11D1A,  # ण
    0x0924: 0x11D1B,  # त
    0x0925: 0x11D1C,  # थ
    0x0926: 0x11D1D,  # द
    0x0927: 0x11D1E,  # ध
    0x0928: 0x11D1F,  # न
    0x0929: 0x11D1F,  # ऩ → न
    0x092A: 0x11D20,  # प
    0x092B: 0x11D21,  # फ
    0x092C: 0x11D22,  # ब
    0x092D: 0x11D23,  # भ
    0x092E: 0x11D24,  # म
    0x092F: 0x11D25,  # य
    0x0930: 0x11D26,  # र
    0x0931: 0x11D26,  # ऱ → र
    0x0932: 0x11D27,  # ल
    0x0933: 0x11D2D,  # ळ
    0x0934: 0x11D2D,  # ऴ → ळ
    0x0935: 0x11D28,  # व
    0x0936: 0x11D29,  # श
    0x0937: 0x11D2A,  # ष
    0x0938: 0x11D2B,  # स
    0x0939: 0x11D2C,  # ह
    # Dependent vowel signs (matra)
    0x093E: 0x11D31,  # ा
    0x093F: 0x11D32,  # ि
    0x0940: 0x11D33,  # ी
    0x0941: 0x11D34,  # ु
    0x0942: 0x11D35,  # ू
    0x0943: 0x11D36,  # ृ
    0x0946: 0x11D3A,  # ॆ → े
    0x0947: 0x11D3A,  # े
    0x0948: 0x11D3C,  # ै
    0x094A: 0x11D3D,  # ॊ → ो
    0x094B: 0x11D3D,  # ो
    0x094C: 0x11D3F,  # ौ
    # Signs
    0x0901: 0x11D40,  # ँ candrabindu → anusvara (approx)
    0x0902: 0x11D40,  # ं anusvara
    0x0903: 0x11D41,  # ः visarga
    0x093C: 0x11D42,  # ़ nukta
    0x0945: 0x11D43,  # ॅ candra e
    0x0949: 0x11D43,  # ॉ candra o  (applied on top of ओ-matra if present)
    0x094D: 0x11D45,  # ् virama (conjunct former)
    # Digits
    0x0966: 0x11D50,  # ०
    0x0967: 0x11D51,  # १
    0x0968: 0x11D52,  # २
    0x0969: 0x11D53,  # ३
    0x096A: 0x11D54,  # ४
    0x096B: 0x11D55,  # ५
    0x096C: 0x11D56,  # ६
    0x096D: 0x11D57,  # ७
    0x096E: 0x11D58,  # ८
    0x096F: 0x11D59,  # ९
}

# Precomposed nukta letters (NFC) → base + nukta in Gondi
NUKTA_LETTERS: dict[str, str] = {
    "\u0958": "\U00011D0C\U00011D42",  # क़
    "\u0959": "\U00011D0D\U00011D42",  # ख़
    "\u095A": "\U00011D0E\U00011D42",  # ग़
    "\u095B": "\U00011D13\U00011D42",  # ज़
    "\u095C": "\U00011D18\U00011D42",  # ड़
    "\u095D": "\U00011D19\U00011D42",  # ढ़
    "\u095E": "\U00011D21\U00011D42",  # फ़
    "\u095F": "\U00011D25\U00011D42",  # य़
}

# Multi-char replacements applied FIRST (longest first)
# Precomposed Masaram Gondi conjuncts
CONJUNCTS: dict[str, str] = {
    "\u0915\u094d\u0937": "\U00011D2E",  # क्ष → 𑴮 KSSA
    "\u091c\u094d\u091e": "\U00011D2F",  # ज्ञ → 𑴯 JNYA
    "\u0924\u094d\u0930": "\U00011D30",  # त्र → 𑴰 TRA
}

# Independent vocalic R / RR → र + vocalic-r sign
VOCALIC: dict[str, str] = {
    "\u090B": "\U00011D26\U00011D36",  # ऋ
    "\u0960": "\U00011D26\U00011D36",  # ॠ
    "\u0944": "\U00011D36",            # ॄ → vocalic r sign
}

# ऑ / ऍ (foreign vowels) → base + candra
FOREIGN_VOWELS: dict[str, str] = {
    "\u0911": "\U00011D09\U00011D43",  # ऑ → ओ + candra
}

# Devanagari consonants (for repha / ra-kara detection)
_DEVA_CONS = set(range(0x0915, 0x093A)) | set(NUKTA_LETTERS.keys())
# also include nukta-composed
for _ch in NUKTA_LETTERS:
    _DEVA_CONS.add(ord(_ch))

GONDI_VIRAMA = chr(0x11D45)
GONDI_HALANTA = chr(0x11D44)
GONDI_REPHA = chr(0x11D46)
GONDI_RAKARA = chr(0x11D47)

# Reverse map — first-wins so aliases (ऩ ऱ ऴ ऎ ॊ) do not override canon
GONDI2DEVA: dict[int, int] = {}
for _src, _dst in DEVA2GONDI.items():
    GONDI2DEVA.setdefault(_dst, _src)
GONDI2DEVA.update(
    {
        0x11D06: 0x090F,  # ए
        0x11D09: 0x0913,  # ओ
        0x11D1F: 0x0928,  # न
        0x11D26: 0x0930,  # र
        0x11D2D: 0x0933,  # ळ
        0x11D3A: 0x0947,  # े
        0x11D3D: 0x094B,  # ो
        0x11D40: 0x0902,  # ं
        0x11D44: 0x094D,  # ्
        0x11D45: 0x094D,  # ्
    }
)
REVERSE_CONJUNCTS: dict[str, str] = {
    chr(0x11D2E): "\u0915\u094d\u0937",  # क्ष
    chr(0x11D2F): "\u091c\u094d\u091e",  # ज्ञ
    chr(0x11D30): "\u0924\u094d\u0930",  # त्र
}


def _is_deva_consonant(ch: str) -> bool:
    o = ord(ch)
    return 0x0915 <= o <= 0x0939 or o in (0x0958, 0x0959, 0x095A, 0x095B, 0x095C, 0x095D, 0x095E, 0x095F)


def convert(text: str, *, smart_ra: bool = True, map_digits: bool = True) -> str:
    """Convert Devanagari text to Masaram Gondi.

    smart_ra: र्C → Repha+C and C्र → C+Ra-kara (Unicode-recommended).
    map_digits: map ०-९ (and optionally leave ASCII 0-9 untouched).
    """
    if not text:
        return text

    # 0) NFC-style nukta letters
    for src, dst in NUKTA_LETTERS.items():
        text = text.replace(src, dst)

    # 1) Foreign vowels / vocalic R
    for src, dst in FOREIGN_VOWELS.items():
        text = text.replace(src, dst)
    for src, dst in VOCALIC.items():
        text = text.replace(src, dst)

    # 2) Precomposed conjuncts (क्ष ज्ञ त्र) — before ra-rules
    for src, dst in CONJUNCTS.items():
        text = text.replace(src, dst)

    # 3) Smart ra: Repha (र् + C) and Ra-kara (C + ् + र)
    if smart_ra:
        chars = list(text)
        out: list[str] = []
        i = 0
        n = len(chars)
        while i < n:
            ch = chars[i]
            # Repha: र + ् + consonant
            if (
                ch == "\u0930"
                and i + 2 < n
                and chars[i + 1] == "\u094d"
                and _is_deva_consonant(chars[i + 2])
            ):
                cons = chars[i + 2]
                mapped = chr(DEVA2GONDI.get(ord(cons), ord(cons)))
                out.append(GONDI_REPHA)
                out.append(mapped)
                i += 3
                continue
            # Ra-kara: consonant + ् + र  (र not itself followed by ् forming another cluster start)
            if (
                _is_deva_consonant(ch)
                and i + 2 < n
                and chars[i + 1] == "\u094d"
                and chars[i + 2] == "\u0930"
            ):
                mapped = chr(DEVA2GONDI.get(ord(ch), ord(ch)))
                out.append(mapped)
                out.append(GONDI_RAKARA)
                i += 3
                continue
            out.append(ch)
            i += 1
        text = "".join(out)

    # 4) Remaining 1:1
    result: list[str] = []
    for ch in text:
        o = ord(ch)
        if not map_digits and 0x0966 <= o <= 0x096F:
            result.append(ch)
            continue
        result.append(chr(DEVA2GONDI.get(o, o)))
    return "".join(result)


def convert_to_halanta_final(text: str, **kwargs) -> str:
    """Like convert(), but a trailing virama (dead consonant at end of a run)
    is emitted as Halanta 𑵄 instead of Virama 𑵅 — use when you want the
    inherent vowel silenced without forming a conjunct.
    """
    out = convert(text, **kwargs)
    # word-final virama → halanta
    import re

    return re.sub(GONDI_VIRAMA + r"(?=$|\s|[।॥,.!?;:])", GONDI_HALANTA, out)


def convert_reverse(text: str) -> str:
    """Masaram Gondi → Devanagari (best-effort inverse)."""
    for src, dst in REVERSE_CONJUNCTS.items():
        text = text.replace(src, dst)
    text = text.replace(GONDI_REPHA, "\u0930\u094d")  # र्
    text = text.replace(GONDI_RAKARA, "\u094d\u0930")  # ्र
    text = text.replace(GONDI_HALANTA, "\u094d")
    return "".join(chr(GONDI2DEVA.get(ord(ch), ord(ch))) for ch in text)


GOLDEN = {
    "मसराम": "𑴤𑴫𑴦𑴱𑴤",
    "गोंडी": "𑴎𑴽𑵀𑴘𑴳",
    # नमस्ते = न म स ् त े  — virama is required (स् + त conjunct)
    "नमस्ते": "𑴟𑴤𑴫𑵅𑴛𑴺",
    "भारत": "𑴣𑴱𑴦𑴛",
    "हिन्दी": "𑴬𑴲𑴟𑵅𑴝𑴳",
    "जय हिन्द": "𑴓𑴥 𑴬𑴲𑴟𑵅𑴝",
    "क्षेत्र": "𑴮𑴺𑴰",
}


def self_test() -> int:
    failed = 0
    print("=== Golden tests (1:1 + conjuncts) ===")
    for src, expected in GOLDEN.items():
        got = convert(src, smart_ra=True)
        ok = got == expected
        failed += not ok
        mark = "OK " if ok else "FAIL"
        print(f"  {mark}  {src:12} → {got}")
        if not ok:
            print(f"         expected {expected}")
            print(f"         cps got  {[hex(ord(c)) for c in got]}")
            print(f"         cps exp  {[hex(ord(c)) for c in expected]}")

    print("\n=== Smart ra ===")
    ra_cases = {
        "कर्म": None,   # र् + म → repha
        "क्रम": None,   # क् + र → ra-kara
        "प्रणाम": None,
    }
    for src in ra_cases:
        got = convert(src, smart_ra=True)
        simple = convert(src, smart_ra=False)
        print(f"  {src:12} smart={got}   simple={simple}")

    print("\n=== Reverse ===")
    for src in GOLDEN:
        back = convert_reverse(convert(src))
        # reverse of smart-ra words may differ slightly; check golden only
        ok = back == src or convert(back) == convert(src)
        failed += not ok
        print(f"  {'OK ' if ok else 'FAIL'}  {src} ↔ {back}")

    print("\n=== Extra ===")
    extras = ["पानी", "घर", "नाम", "दिन", "क़लम", "ऑफिस", "ऋषि", "१२३"]
    for w in extras:
        print(f"  {w:12} → {convert(w)}")

    print(f"\n{'ALL PASSED' if failed == 0 else f'{failed} FAILED'}")
    return failed


def export_mapping_json(path: Path) -> None:
    mapping = {f"{k:04X}": f"{v:04X}" for k, v in DEVA2GONDI.items()}
    data = {
        "name": "Devanagari to Masaram Gondi",
        "id": "hin2gon",
        "version": "1.1",
        "unicode_block": "U+11D00–U+11D5F",
        "mapping": mapping,
        "conjuncts": {
            "0915 094D 0937": "11D2E",
            "091C 094D 091E": "11D2F",
            "0924 094D 0930": "11D30",
        },
        "nukta_letters": {f"{ord(k):04X}": [f"{ord(c):04X}" for c in v] for k, v in NUKTA_LETTERS.items()},
        "special": {
            "repha": "11D46",
            "ra_kara": "11D47",
            "halanta": "11D44",
            "virama": "11D45",
            "candra": "11D43",
        },
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in {"--test", "-t"}:
        sys.exit(self_test())
    if len(sys.argv) > 1 and sys.argv[1] == "--export":
        out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parents[1] / "mapping.json"
        export_mapping_json(out)
        sys.exit(0)
    if len(sys.argv) > 1:
        print(convert(" ".join(sys.argv[1:])))
    else:
        sys.exit(self_test())
