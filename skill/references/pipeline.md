# Pipeline playbook

The hard-won details from the reference build. Work the phases in order; each one
feeds the next.

## Phase 0 — Capture the source completely

**Fetching.** Try WebFetch first; if the host is blocked, `curl -sSL` (with the
environment's CA bundle if behind a proxy). If both fail or the page is paywalled,
ask the user to paste the text — never work around a paywall.

**App-rendered pages** (small HTML, lots of `<script src>`): the content usually
lives in a JSON file or API the page loads. Trace it: list the script URLs, fetch
the main module, follow imports to the data loader, fetch the content JSON. Chart
data is often inlined in chart modules as constants — fetch those too. This turns
"unscrapeable" interactives into a complete, structured capture.

**Sweep for every link.** Grep the captured HTML/JSON for all URLs: related
articles, videos, data sources, bylines. Users notice a missed link. Record each
with enough context to write an original one-line description later. Note the
source page's own section anchor ids — the per-section nudges deep-link to them.

**Record for attribution**: outlet, feature title, publication date, every
credited person and role, copyright line.

## Phase 1 — Author the master

Write the pivot-language master as one JSON file (see `assets/master-example.json`):

- Nested objects; leaf strings are the translatable content. Keys are stable ids —
  never renamed after translation starts.
- `_meta`: `{code, htmlLang, name (endonym), englishName, fontClass}`.
- Highlight markup: `<span class='hl'>…</span>` (and a second accent class if
  needed) with single-quote attributes, `<br>` only. Nothing else — translators
  preserve these exactly and the gate checks them.
- Templates with `{placeholders}` for strings that compose with data at runtime —
  word order varies across languages, so never build sentences by concatenation.
- Keep UI strings (`ui.*`) short: they are buttons and chips.
- Facts and figures exactly as captured; quotes paraphrased with attribution
  ("Lee says the industries that adopted AI fastest are seeing…" — reported
  speech, your words).
- Verify every person's name/romanization with a web search before writing it.

**If the master changes after translation starts** (added keys, changed
placeholders), the reviewer agents and the gate will catch stragglers — but
minimize churn: land new keys as early as possible.

## Phase 2 — Translate with a two-agent chain per language

For each language, run a translator agent then a reviewer agent (templates in
`translator-prompts.md`). Use the Workflow tool when the session permits it
(pipeline pattern, no barrier); otherwise the Agent tool in parallel batches.
Agents read the master from disk and write `i18n/<code>.json` directly — never
pass translations through your own context.

Then run the gate:

```
python3 <skill>/scripts/check_i18n.py --dir i18n --master en
```

Fix failures directly (a lost `{pct}` placeholder, a dropped number) and re-run
until every language is OK. Small late additions (a new button label) you may
translate yourself — 2–3 word UI strings only; anything longer goes to an agent.

## Phase 3 — Build by adapting the reference template

`assets/template-reference.html` is a complete working page. Keep its engines:

- i18n renderer (`data-i18n` binding, per-language font classes, `lang`/`dir`),
  language chips, `#lang=` deep links, localStorage persistence
- Compare mode (tap a paragraph → same paragraph in a second language, inline)
- More-detail chips (`data-detail` paragraphs collapse to inline "＋" chips)
- Read-aloud engine (voice ranking: natural > neural > premium > enhanced >
  google > default > espeak; per-language voice picker; sentence chunking —
  utterances under ~200 chars avoid Chrome's long-utterance stall; paragraph
  highlight + scroll)
- Pixel-art renderer (`px()` — sprites as string grids, chars mapped to CSS
  variables so art adapts to light/dark), tooltip layer, reveal observers,
  theme-token CSS structure (bare `:root` light, `prefers-color-scheme` guarded
  dark, `[data-theme]` overrides both ways)

Replace per project: the content skeleton (sections mirroring the source's
structure), the charts, the sprites, the further-reading data, colors if the user
chose a different identity.

**Design**: load the `artifact-design` skill before writing the page and the
`dataviz` skill before any chart. Validate every categorical palette with the
dataviz validator, light AND dark surfaces, in the chart's actual stacking order.
Give every chart a `<details>` data-table fallback and hover/focus tooltips.

**Watch for** (bugs found in the reference build): CSS specificity collisions
between component art sizes (scope section-art rules with `>`); scroll-step
observers overriding manual chart selection (a manual pick must lock out scroll
steps until deselected); SVG text too small on phones (charts get their own
`overflow-x: auto` with a min-width); sticky headers eating mobile viewports
(make the header static under ~760px).

## Phase 4 — QA gates before shipping

1. `check_i18n.py` passes for every language.
2. Palette validator passes both themes.
3. Real-browser screenshots (Playwright): pivot + one CJK + one Indic or Thai
   language; light and dark; desktop and ~390px mobile; every chart's section.
   Look at them — label collisions and overflow only show up visually.
4. Programmatic checks: language chip count, deep links set `documentElement.lang`
   and font class, compare mode injects, chips expand, every captured link is in
   the DOM.
5. Read the pivot page top to bottom once as an editor.

## Phase 5 — Ship

Repo layout:

```
i18n/<code>.json      one file per language; the pivot is the master
src/template.html     the page (all CSS/JS inline, "__I18N_DATA__" placeholder)
build.py              inlines i18n + pre-renders pivot text; writes index.html
scripts/check_i18n.py the gate
README.md             languages, features, how to edit text / add a language
index.html            the deliverable — a single self-contained file
```

`index.html` must be fully self-contained (Google Fonts links allowed, real
fallback stacks required — it is the one external host artifact pages permit).
Publish it as an artifact for instant preview; commit and push everything.
