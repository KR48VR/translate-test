# Language pack

The 18 languages from the reference build, with everything a new build needs.
`fontClass` maps to a CSS class that swaps the font stack and line-height;
`voices` are Web Speech API match prefixes, best first.

| code | endonym | htmlLang | fontClass | Google Fonts family | voices | register notes |
|---|---|---|---|---|---|---|
| en | English | en | latin | Noto Sans | en-sg, en-gb, en-us, en | clear journalistic explainer |
| zh | 中文（简体） | zh-Hans | sc | Noto Sans SC | zh-cn, zh-sg, cmn, zh | standard written Chinese; 人工智能（AI）first mention; Chinese punctuation; write fresh from the master, never reconstruct any existing Chinese article's wording |
| ms | Bahasa Melayu | ms | latin | Noto Sans | ms | Singapore/Malaysia standard, NOT Indonesian; kecerdasan buatan (AI) first |
| ta | தமிழ் | ta | tamil | Noto Sans Tamil | ta | formal but accessible Singapore written Tamil; Western digits |
| sg | Singlish | en-SG | latin | Noto Sans | en-sg, en-gb, en | particles (lah, leh, lor, sia) and local expressions used naturally, in moderation; informative first, funny second, never mocking; facts and names stay exact |
| yue | 廣東話 | yue | tc | Noto Sans TC | yue, zh-hk | written colloquial Cantonese in TRADITIONAL characters (嘅咗唔係喺畀啲) — HK online-media register, not standard written Chinese |
| th | ไทย | th | thai | Noto Sans Thai | th | news-explainer register; ปัญญาประดิษฐ์ (AI) first; Western digits |
| vi | Tiếng Việt | vi | latin | Noto Sans | vi | trí tuệ nhân tạo (AI) first |
| ja | 日本語 | ja | jp | Noto Sans JP | ja | です・ます polite explainer; 人工知能（AI）first; katakana names with originals in parens |
| ko | 한국어 | ko | kr | Noto Sans KR | ko | 합니다체; 인공지능(AI) first |
| hi | हिन्दी | hi | deva | Noto Sans Devanagari | hi | Hindi tech-media register; कृत्रिम बुद्धिमत्ता (AI) first, then Latin AI; Western digits |
| ml | മലയാളം | ml | mlym | Noto Sans Malayalam | ml | Malayalam news-explainer register; നിർമിത ബുദ്ധി (AI) first |
| si | සිංහල | si | sinh | Noto Sans Sinhala | si | standard written Sinhala; කෘත්‍රිම බුද්ධිය (AI) first |
| fr | Français | fr | latin | Noto Sans | fr-fr, fr | intelligence artificielle (IA) first; French typography (60 000, « ») |
| es | Español | es | latin | Noto Sans | es-es, es-us, es | neutral international Spanish; inteligencia artificial (IA) first |
| de | Deutsch | de | latin | Noto Sans | de-de, de | Künstliche Intelligenz (KI) first |
| nl | Nederlands | nl | latin | Noto Sans | nl-nl, nl | kunstmatige intelligentie (AI) first |
| ru | Русский | ru | latin* | Noto Sans | ru | искусственный интеллект (ИИ) first, then ИИ; standard Russian transcription for names |

\* Noto Sans covers Cyrillic; no separate family needed. The display face
(Archivo in the reference) does not — Cyrillic headlines fall back to Noto Sans
bold, which is fine.

**Keep "AI"/domain keywords in Latin** wherever they name the literal keyword the
source measured (e.g. terms employers search in job ads) — translating those
changes the claim.

## Adding a language

1. Add its row: code, endonym, htmlLang, fontClass (+ Google Fonts family and a
   CSS font class if it needs a new script), voice prefixes, register notes.
2. Add the code to the ORDER lists (template + build script) and the fonts link.
3. Run the translator + reviewer chain, then the gate.
4. Update the language count anywhere the content states it (hero, about,
   README) — in every existing language file (usually a digit swap).

## Primarily-oral languages (Hokkien, Teochew, Hakka, …)

No mainstream platform ships TTS voices for these — do not pretend otherwise.
Options that actually work:

- **Cantonese is the exception**: zh-HK voices are widely available, so 廣東話
  gets real read-aloud.
- **Recorded human audio** is the honest path: speakers (students, family,
  community) record a short spoken summary per section; the page gets an audio
  rail playing per-section recordings with a "recording not yet available"
  state. In a classroom this doubles as a heritage-language activity. Build the
  rail only once at least one real recording exists.
- Never render a Mandarin voice over Hokkien/Teochew/Hakka text and call it
  read-aloud — it is neither language done right.

## Read-aloud device guidance (tell users honestly)

- Desktop **Microsoft Edge**: neural "Natural" voices for most languages, no
  setup, needs internet.
- **Android**: good Google voices pre-installed; widest coverage for Tamil,
  Malayalam, Sinhala, Malay, Thai, Vietnamese.
- **iPhone/iPad**: download Enhanced/Premium voices under Settings →
  Accessibility → Spoken Content → Voices (renamed **Read & Speak** in newer
  iOS 26 builds) — one voice at a time, a few hundred MB each; fully restart the
  browser afterwards. Websites see downloaded Enhanced voices but never the Siri
  voices themselves.
- Voice choice is remembered per language per device by the reference engine.
