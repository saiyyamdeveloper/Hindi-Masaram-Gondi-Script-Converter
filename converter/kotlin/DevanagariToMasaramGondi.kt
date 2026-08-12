package org.masaram.gondi

/**
 * Devanagari (Hindi) → Masaram Gondi live converter.
 *
 * Drop this object into an Android IME (Gboard companion, FlorisBoard
 * composer, or your own InputMethodService) and call [convert] on the
 * composing text / after every key.
 *
 *     val gondi = DevanagariToMasaramGondi.convert(hindiTyped)
 *     ic.commitText(gondi, 1)
 */
object DevanagariToMasaramGondi {

    /** Independent vowels, consonants, matras, signs, digits. */
    private val DEVA2GONDI: Map<Int, Int> = hashMapOf(
        // Swar
        0x0905 to 0x11D00, 0x0906 to 0x11D01, 0x0907 to 0x11D02, 0x0908 to 0x11D03,
        0x0909 to 0x11D04, 0x090A to 0x11D05, 0x090F to 0x11D06, 0x0910 to 0x11D08,
        0x0913 to 0x11D09, 0x0914 to 0x11D0B,
        0x090E to 0x11D06, 0x0912 to 0x11D09, 0x090D to 0x11D06,
        // Vyanjan
        0x0915 to 0x11D0C, 0x0916 to 0x11D0D, 0x0917 to 0x11D0E, 0x0918 to 0x11D0F,
        0x0919 to 0x11D10, 0x091A to 0x11D11, 0x091B to 0x11D12, 0x091C to 0x11D13,
        0x091D to 0x11D14, 0x091E to 0x11D15, 0x091F to 0x11D16, 0x0920 to 0x11D17,
        0x0921 to 0x11D18, 0x0922 to 0x11D19, 0x0923 to 0x11D1A, 0x0924 to 0x11D1B,
        0x0925 to 0x11D1C, 0x0926 to 0x11D1D, 0x0927 to 0x11D1E, 0x0928 to 0x11D1F,
        0x0929 to 0x11D1F, 0x092A to 0x11D20, 0x092B to 0x11D21, 0x092C to 0x11D22,
        0x092D to 0x11D23, 0x092E to 0x11D24, 0x092F to 0x11D25, 0x0930 to 0x11D26,
        0x0931 to 0x11D26, 0x0932 to 0x11D27, 0x0933 to 0x11D2D, 0x0934 to 0x11D2D,
        0x0935 to 0x11D28, 0x0936 to 0x11D29, 0x0937 to 0x11D2A, 0x0938 to 0x11D2B,
        0x0939 to 0x11D2C,
        // Matra
        0x093E to 0x11D31, 0x093F to 0x11D32, 0x0940 to 0x11D33, 0x0941 to 0x11D34,
        0x0942 to 0x11D35, 0x0943 to 0x11D36, 0x0946 to 0x11D3A, 0x0947 to 0x11D3A,
        0x0948 to 0x11D3C, 0x094A to 0x11D3D, 0x094B to 0x11D3D, 0x094C to 0x11D3F,
        // Signs
        0x0901 to 0x11D40, 0x0902 to 0x11D40, 0x0903 to 0x11D41,
        0x093C to 0x11D42, 0x0945 to 0x11D43, 0x0949 to 0x11D43, 0x094D to 0x11D45,
        // Digits
        0x0966 to 0x11D50, 0x0967 to 0x11D51, 0x0968 to 0x11D52, 0x0969 to 0x11D53,
        0x096A to 0x11D54, 0x096B to 0x11D55, 0x096C to 0x11D56, 0x096D to 0x11D57,
        0x096E to 0x11D58, 0x096F to 0x11D59,
    )

    private val NUKTA_LETTERS = linkedMapOf(
        "\u0958" to cp(0x11D0C, 0x11D42), // क़
        "\u0959" to cp(0x11D0D, 0x11D42),
        "\u095A" to cp(0x11D0E, 0x11D42),
        "\u095B" to cp(0x11D13, 0x11D42),
        "\u095C" to cp(0x11D18, 0x11D42),
        "\u095D" to cp(0x11D19, 0x11D42),
        "\u095E" to cp(0x11D21, 0x11D42),
        "\u095F" to cp(0x11D25, 0x11D42),
    )

    private val CONJUNCTS = linkedMapOf(
        "\u0915\u094d\u0937" to cp(0x11D2E), // क्ष
        "\u091c\u094d\u091e" to cp(0x11D2F), // ज्ञ
        "\u0924\u094d\u0930" to cp(0x11D30), // त्र
    )

    private val VOCALIC = linkedMapOf(
        "\u090B" to cp(0x11D26, 0x11D36), // ऋ
        "\u0960" to cp(0x11D26, 0x11D36),
        "\u0944" to cp(0x11D36),
    )

    private val FOREIGN = linkedMapOf(
        "\u0911" to cp(0x11D09, 0x11D43), // ऑ
    )

    const val VIRAMA = 0x11D45
    const val HALANTA = 0x11D44
    const val REPHA = 0x11D46
    const val RA_KARA = 0x11D47

    private fun cp(vararg cps: Int): String = buildString { cps.forEach { appendCodePoint(it) } }

    private fun isDevaConsonant(cp: Int): Boolean =
        cp in 0x0915..0x0939 || cp in 0x0958..0x095F

    /**
     * Convert a Devanagari string to Masaram Gondi.
     *
     * @param smartRa  र्C → Repha+C and C्र → C+Ra-kara (Unicode recommended).
     */
    @JvmStatic
    @JvmOverloads
    fun convert(text: String, smartRa: Boolean = true): String {
        if (text.isEmpty()) return text
        var s = text
        NUKTA_LETTERS.forEach { (a, b) -> s = s.replace(a, b) }
        FOREIGN.forEach { (a, b) -> s = s.replace(a, b) }
        VOCALIC.forEach { (a, b) -> s = s.replace(a, b) }
        CONJUNCTS.forEach { (a, b) -> s = s.replace(a, b) }

        if (smartRa) {
            val chars = s.toCodePointList()
            val out = ArrayList<Int>(chars.size)
            var i = 0
            while (i < chars.size) {
                val ch = chars[i]
                if (ch == 0x0930 && i + 2 < chars.size &&
                    chars[i + 1] == 0x094D && isDevaConsonant(chars[i + 2])
                ) {
                    out += REPHA
                    out += DEVA2GONDI[chars[i + 2]] ?: chars[i + 2]
                    i += 3
                    continue
                }
                if (isDevaConsonant(ch) && i + 2 < chars.size &&
                    chars[i + 1] == 0x094D && chars[i + 2] == 0x0930
                ) {
                    out += DEVA2GONDI[ch] ?: ch
                    out += RA_KARA
                    i += 3
                    continue
                }
                out += ch
                i++
            }
            s = out.toStringFromCodePoints()
        }

        val result = StringBuilder(s.length * 2)
        var i = 0
        while (i < s.length) {
            val cp = s.codePointAt(i)
            result.appendCodePoint(DEVA2GONDI[cp] ?: cp)
            i += Character.charCount(cp)
        }
        return result.toString()
    }

    /** Word-final virama becomes Halanta (vowel killer, not conjunct). */
    @JvmStatic
    fun convertWithFinalHalanta(text: String, smartRa: Boolean = true): String {
        val out = convert(text, smartRa)
        val vir = cp(VIRAMA)
        val hal = cp(HALANTA)
        return Regex("${Regex.escape(vir)}(?=$|\\s|[।॥,.!?;:])").replace(out, hal)
    }

    // ------------------------------------------------------------------
    // IME helper — convert only the last Devanagari run so Latin stays
    // ------------------------------------------------------------------

    /**
     * Walk backwards from [cursor] and convert the current Devanagari
     * word. Returns Pair(startIndex, convertedWord) or null if nothing
     * to convert. Call from InputConnection after each composing update.
     */
    @JvmStatic
    fun convertLastWord(full: String, cursor: Int = full.length): Pair<Int, String>? {
        if (cursor <= 0) return null
        var start = cursor
        while (start > 0) {
            val cp = full.codePointBefore(start)
            val count = Character.charCount(cp)
            if (!isIndicRun(cp)) break
            start -= count
        }
        if (start == cursor) return null
        val word = full.substring(start, cursor)
        return start to convert(word)
    }

    private fun isIndicRun(cp: Int): Boolean =
        cp in 0x0900..0x097F || cp in 0x11D00..0x11D5F

    private fun String.toCodePointList(): List<Int> {
        val list = ArrayList<Int>(length)
        var i = 0
        while (i < length) {
            val cp = codePointAt(i)
            list += cp
            i += Character.charCount(cp)
        }
        return list
    }

    private fun List<Int>.toStringFromCodePoints(): String =
        buildString { forEach { appendCodePoint(it) } }
}

/* ------------------------------------------------------------------
 * Example hook for a custom InputMethodService / TextWatcher
 * ------------------------------------------------------------------
 *
 * class GondiInputMethod : InputMethodService() {
 *     private val ic get() = currentInputConnection
 *
 *     fun onHindiCommitted(hindi: String) {
 *         val gondi = DevanagariToMasaramGondi.convert(hindi)
 *         ic?.commitText(gondi, 1)
 *     }
 *
 *     // Or live-replace the current word:
 *     fun onUpdateSelection(...) {
 *         val before = ic?.getTextBeforeCursor(64, 0)?.toString() ?: return
 *         val pair = DevanagariToMasaramGondi.convertLastWord(before) ?: return
 *         val wordLen = before.length - pair.first
 *         if (before.substring(pair.first) == pair.second) return
 *         ic?.deleteSurroundingText(wordLen, 0)
 *         ic?.commitText(pair.second, 1)
 *     }
 * }
 */
