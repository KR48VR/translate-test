# Translator and reviewer prompt templates

One translator + one reviewer per language. Fill `{LANGUAGE}`, `{CODE}`,
`{HTMLLANG}`, `{ENDONYM}`, `{FONTCLASS}`, `{NOTES}` (from `language-pack.md`),
`{SRC}` (master path) and `{OUT}` (i18n dir). Agents read and write files
directly — translations must never round-trip through the orchestrator's context.

## Translator prompt

```
You are translating the content of a multilingual educational website into {LANGUAGE}.

Read the master file at {SRC}. It is a JSON object whose LEAF STRING VALUES are
the site's content.

Write a complete translation to {OUT}/{CODE}.json using the Write tool:

1. EXACT same JSON structure: every key, every nesting level, in the same order.
   Translate ONLY the leaf string values. Output valid JSON, UTF-8, real Unicode
   characters (never \uXXXX escapes).
2. Replace the whole "_meta" object with exactly: {"code": "{CODE}", "htmlLang":
   "{HTMLLANG}", "name": "{ENDONYM}", "englishName": "{LANGUAGE}", "fontClass":
   "{FONTCLASS}"}
3. Preserve exactly: all digits and number VALUES (formatting may localize:
   60,000 → 60.000 / 60 000; value changes never allowed), the HTML tags
   <span class='hl'>…</span> and <br> (translate only text inside; keep the
   single-quote attribute style), every {placeholder}, and proper nouns
   (product names, outlet names, company names, Python, etc.). Keep person
   names with their original-script forms where the master gives both. Keep the
   source feature's title in its original language with a {LANGUAGE} gloss in
   parentheses. Keep the copyright line as-is.
4. Language direction: {NOTES}
5. Register: clear, engaging, natural — not word-for-word literal. UI labels
   ("ui" section) stay SHORT: they are buttons and chips. The hero title gets a
   natural, punchy localized headline, not a literal gloss.
6. After writing: validate the JSON parses; write a short python check that the
   key structure matches the master exactly; fix anything that fails. Then
   re-read your file once as a native reader and fix anything stilted.

Do NOT create or modify any other files. Return one short line: "written" plus
anything worth knowing.
```

## Reviewer prompt

```
You are reviewing a {LANGUAGE} translation for a multilingual educational website.
Files: master {SRC} ; translation {OUT}/{CODE}.json
It was made under these directions: {NOTES}

Review rigorously and EDIT THE FILE IN PLACE for every fix:
1. JSON validity; fix if broken.
2. Structure parity with the master at every level (script it); fix missing or
   extra keys — the master may have gained keys since the translation was made.
3. Fidelity: every number value, name, {placeholder} and <span class='hl'>/<br>
   tag survives; _meta correct.
4. Completeness: no leaf left untranslated that should be (proper nouns and
   established loanwords may stay).
5. Naturalness: read the whole file as a native reader; fix stilted, literal,
   wrong-register, or wrong-script text. Distinct registers (colloquial written
   Cantonese, Singlish) must genuinely read as that register — fix drift toward
   the standard language, tone down caricature, punch up flatness.

Return one short JSON line: {"ok": true/false, "fixes": <count>, "notes": "<one sentence>"}
```

## Notes that made real translations better

- Colloquial registers need explicit positive direction ("like a sharp, friendly
  kopitiam uncle explaining the news — informative first, funny second, never a
  caricature") plus example particles/vocabulary, or they drift standard.
- CJK + number formatting: allow native large-number forms (9200万, 1.7억) —
  the gate's `--numflex` list covers them.
- Tell every agent the master may have changed since their read started; the
  reviewer's parity check is what makes mid-flight master edits safe.
- Name every "keep as-is" proper noun explicitly; agents otherwise localize
  org names inconsistently across the set.
