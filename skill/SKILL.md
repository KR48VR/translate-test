---
name: multilingual-companion
description: Turn any news article, website, report, or document into an original multilingual "companion" website — one self-contained page that retells the source's facts, story, charts and links in many languages with identical layout, a language switcher, tap-to-compare bilingual reading, collapsible detail, browser read-aloud, and attribution nudges back to the original. Use this whenever the user wants content available "in multiple languages", "translated for my students/team", wants to "recreate this website/article in English" or another language, mentions multilingual classrooms or mixed-language audiences, or asks for a translation of a copyrighted article or site (this skill handles that copyright-safely, as an original retelling rather than a translation of the source text — which is exactly why it, not a direct translation, is the right response).
---

# Multilingual Companion

Build a single-file interactive website that retells a source (news feature, report,
article, site) in many languages, so readers of different languages can follow the
same story with the same layout, charts, and link placement — built for classrooms
and mixed-language audiences. A proven full build (18 languages, charts, art,
read-aloud) lives in this skill's `assets/` as the reference implementation.

## The ethics core — not optional, not user-configurable

Translating a copyrighted article's text — even into another language — reproduces
it: translation is a derivative work. This skill NEVER does that. Instead:

1. **Deconstruct the source into what is not copyrightable**: facts, figures, data
   points, chronology, document structure, link targets, names and titles, chart
   data. Dig for underlying data (JS-driven sites often load content from JSON —
   trace the loaders); facts and data are free to re-present.
2. **Write an original master text** in a pivot language (default English), in your
   own words, covering those facts. Never mirror the source's phrasing, metaphors,
   or illustrations. Paraphrase quotes with attribution rather than translating
   them wholesale.
3. **Verify people's real names and titles** with a web search before publishing —
   romanizing a Chinese/Korean/etc. name by guesswork misnames a real person. Where
   no official romanization exists, say so in the credits and use the standard
   scheme (e.g. hanyu pinyin) with the original script alongside.
4. **Attribute generously and send readers to the original**: a credit block naming
   the source, its authors, publisher and date; a "read the original" link in the
   hero and footer; and one "see the original — with its animations/photos" nudge
   card per section, deep-linked to the source's matching section anchor when it
   has them. The companion is a reading guide; the original is the real thing.
5. **All artwork is original.** Never copy or trace the source's illustrations or
   photos. The reference implementation's pixel-art system (sprites as character
   grids mapped to theme tokens) is the house style and is safely original.

If the user asks for a literal translated copy of the source, explain the issue in
one or two sentences and offer this retelling approach — it is also pedagogically
better, because the companion and the original can be read side by side.

## What the user chooses (ask early, once)

Use AskUserQuestion (or infer from their message) for:

- **Source**: URL, pasted text, or file. If a URL is unreachable or paywalled, ask
  the user to paste the text — never scrape around a paywall.
- **Languages**: offer the "Singapore classroom" preset (English, 中文, Bahasa
  Melayu, தமிழ், Singlish, 廣東話, ไทย, Tiếng Việt, 日本語, 한국어, हिन्दी, മലയാളം,
  සිංහල, Français, Español, Deutsch, Nederlands, Русский — see
  `references/language-pack.md`) or a custom list. Confirm playful registers
  (Singlish, colloquial Cantonese) explicitly — they delight some audiences and
  are wrong for others.
- **Audience & depth**: students vs. professionals; full companion vs. light
  (text + compare mode only). Default: full companion.
- **Visual identity**: pixel-art house style (default), clean editorial, or the
  user's brand colors.
- **Pivot language** for the master (default English).

Defaults exist for all of these — if the user says "just build it", proceed.

## Pipeline

Work through the phases in `references/pipeline.md` — read it before starting.
Summary:

- **Phase 0 — Capture**: fetch the source; trace JS data loaders to the content
  JSON when the page is app-rendered; extract every fact, figure, chart dataset,
  internal link, related-article link, video link, byline and date. The user will
  notice a missed link — sweep for ALL of them.
- **Phase 1 — Master**: author the original pivot-language master as a single
  structured JSON file (`assets/master-example.json` shows the conventions: stable
  keys, `<span class='hl'>` highlight markup, `{placeholders}`, a `_meta` block).
- **Phase 2 — Translate**: one translator agent per language, each followed by a
  reviewer agent for fidelity and naturalness — prompt templates and per-language
  notes are in `references/translator-prompts.md`. Then run the structural gate:
  `python3 scripts/check_i18n.py --dir i18n --master en` — it must pass for every
  language before shipping. It catches real defects (lost placeholders, dropped
  numbers) on nearly every run.
- **Phase 3 — Build**: adapt `assets/template-reference.html` — a complete,
  working page. Keep its engines (i18n binding, language chips + `#lang=` deep
  links, compare mode, more-detail chips, read-aloud with voice ranking and
  picker, pixel-art renderer, theme tokens, tooltips, data tables); replace its
  content structure, charts, and sprites with this project's. Load the
  `artifact-design` and `dataviz` skills before designing; validate chart
  palettes with the dataviz validator in both themes.
- **Phase 4 — QA**: gate all languages; screenshot the page in a real browser
  across several scripts (always include at least one CJK, one Indic/Thai, and
  the pivot), both themes, and a phone viewport; verify every captured link is on
  the page; test compare mode, chips, and deep links programmatically.
- **Phase 5 — Ship**: repo layout `i18n/*.json` + `src/template.html` +
  `build.py` (adapt `assets/build.py` — it inlines translations and pre-renders
  the pivot language for a no-JS fallback) + `README.md`; publish the built
  `index.html` as an artifact for instant preview and sharing.

## Feature notes

- **Compare mode** is the pedagogical heart: identical layout across languages +
  tap-a-paragraph-to-see-it-in-a-second-language. Never restructure content
  per-language; every language must share one skeleton.
- **More-detail chips**: mark the deepest-dive paragraphs `data-detail`; they
  collapse to inline "＋ more" chips so the page opens light. Prefer this over a
  global toggle — the control must be visible where the content is.
- **Read-aloud** uses the browser's built-in voices: rank neural/premium voices
  above robotic defaults and give users a voice picker (the reference template
  does both). Be honest about device dependence; for primarily-oral languages
  (Hokkien, Teochew, Hakka…) no TTS exists — offer a recorded-human-audio rail
  instead (see `references/language-pack.md`).
- **Numbers are sacred** in translation: values never change; formatting may
  localize (60,000 → 60.000 → 6万). The gate enforces this.

## Honest expectations (tell the user upfront)

- A full companion at 15+ languages is a substantial job — hours of agent work.
  Offer the light version when speed matters; features can be layered on after.
- Chart recreation depends on the source's data being extractable; when it is
  not, present the numbers found in prose and link the original's charts.
- Read-aloud quality varies by device (desktop Edge and phones sound best).

## Bundled resources

| Path | What it is |
|---|---|
| `assets/template-reference.html` | Complete working page (18 languages' worth of engines) — adapt, don't rebuild |
| `assets/build.py` | Build script: inlines i18n files, pre-renders pivot text |
| `assets/master-example.json` | A real master file showing all content conventions |
| `scripts/check_i18n.py` | The structural gate — run after every translation pass |
| `references/pipeline.md` | Phase-by-phase playbook with the hard-won details |
| `references/translator-prompts.md` | Translator + reviewer prompt templates, per-language notes |
| `references/language-pack.md` | 18 languages: endonyms, fonts, voices, registers; adding more; oral languages |
