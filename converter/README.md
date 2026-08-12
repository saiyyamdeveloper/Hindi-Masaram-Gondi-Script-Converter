# Converters

## Python

```bash
python3 python/devanagari_to_masaram_gondi.py --test
python3 python/devanagari_to_masaram_gondi.py "नमस्ते भारत"
python3 python/devanagari_to_masaram_gondi.py --export mapping.json
```

`convert(text, smart_ra=True)` · `convert_reverse(text)` · `convert_to_halanta_final(text)`

## Kotlin (Android IME)

`kotlin/DevanagariToMasaramGondi.kt` — copy into your IME module.

```kotlin
val gondi = DevanagariToMasaramGondi.convert(hindi)
ic.commitText(gondi, 1)

// live last-word replace
val pair = DevanagariToMasaramGondi.convertLastWord(textBeforeCursor)
```

Gboard khud custom composer nahi deta; options:

1. Apna `InputMethodService` (recommended)
2. Accessibility overlay / clipboard converter
3. FlorisBoard/HeliBoard pe direct Gondi layout (conversion ki zaroorat nahi)
