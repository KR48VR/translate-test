# The AI Shift — a multilingual classroom companion

An original, single-page interactive website that retells — in **13 languages** — the facts and
findings of Lianhe Zaobao's interactive feature on how AI is reshaping Singapore's job market
([original feature, in Chinese](https://interactive.zaobao.com.sg/2026/artificial-intelligence-impact-on-singapore-jobs/)).

Built for classrooms with international student profiles: every language version has **identical
layout, structure, charts and link placement**, so students reading in different languages can
follow the same story side by side — no more matching words and paragraphs across a machine-translated
copy.

## Languages

English · 中文（简体）· Bahasa Melayu · தமிழ் · Singlish · 廣東話 (written Cantonese) ·
ไทย · Tiếng Việt · 日本語 · 한국어 · Français · Español · Deutsch

## Features

- **Language switcher** — one click, whole page switches; the choice is remembered and
  shareable via URL (`index.html#lang=ta` opens the Tamil version directly).
- **Compare mode** — pick a second language in the header, then tap any paragraph to see the
  same paragraph in that language inline. Made for vocabulary matching and bilingual reading.
- **Interactive charts** (no external libraries):
  - Top-5 industries for AI hiring demand in Singapore, 2024–2026 (rank bump chart; select an
    industry to see the AI skills its ads mention and its entry-level share)
  - AI job ads vs applications, indexed trend (the boom, the −74% freeze, the rebound)
  - Share of US jobs exposed to AI automation by occupation (Goldman Sachs)
  - WEF 2030 projection: 92M jobs displaced vs 170M created
- **Further reading** — every related article and video linked from the original feature,
  grouped as in the original, each with a one-line description in all 13 languages.
- **Accessible** — data tables behind every chart, keyboard-focusable chart points, screen-reader
  language tagging, light/dark theme, reduced-motion support, colour-blind-safe validated palette.

## What this is (and isn't)

The text is an **original summary written for teaching** — not a translation or copy of the
Zaobao article. Quotes are paraphrased; all data belongs to its cited sources (Zaobao × Jobstreet
by SEEK analysis, Goldman Sachs Research/Haver Analytics, World Economic Forum *Future of Jobs
Report 2025*, University of Oxford research). Full attribution is in the page footer. Please
support the original journalism. Not affiliated with, or endorsed by, SPH Media.

## Development

```
i18n/en.json      ← the English master (source of truth for content)
i18n/<code>.json  ← one file per language, identical key structure
src/template.html ← page template (all CSS/JS inline)
build.py          ← inlines all i18n files + pre-renders English, writes index.html
index.html        ← the deliverable: a single self-contained file
```

To change any text: edit the JSON file(s), then run `python3 build.py`.
To add a language: copy `i18n/en.json`, translate the values (keep every key and every
`<span class='hl'>` tag), add the code to `ORDER` in both `build.py` and `src/template.html`.

`index.html` is fully self-contained (fonts come from Google Fonts with system fallbacks) —
host it anywhere, e.g. GitHub Pages, or open the file directly.
