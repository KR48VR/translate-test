#!/usr/bin/env python3
"""Build index.html: inline all i18n files into the template and pre-render English text."""
import json
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
ORDER = ["en", "zh", "ms", "ta", "sg", "yue", "th", "vi", "ja", "ko", "fr", "es", "de"]


def rich(s: str) -> str:
    """Escape, then restore the page's own allowed markup (hl spans, <br>)."""
    s = escape(str(s), quote=False)
    s = (
        s.replace("&lt;span class='hl'&gt;", "<span class='hl'>")
        .replace("&lt;span class='hlNew'&gt;", "<span class='hlNew'>")
        .replace('&lt;span class="hl"&gt;', "<span class='hl'>")
        .replace('&lt;span class="hlNew"&gt;', "<span class='hlNew'>")
        .replace("&lt;/span&gt;", "</span>")
        .replace("&lt;br&gt;", "<br>")
        .replace("&lt;br/&gt;", "<br>")
        .replace("&lt;br /&gt;", "<br>")
    )
    return s


def get(dct, path):
    cur = dct
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def main():
    bundle = {}
    missing = []
    for code in ORDER:
        f = ROOT / "i18n" / f"{code}.json"
        if not f.exists():
            missing.append(code)
            continue
        bundle[code] = json.loads(f.read_text(encoding="utf-8"))
    if "en" not in bundle:
        sys.exit("FATAL: i18n/en.json is required")
    if missing:
        print(f"WARN: missing languages skipped: {', '.join(missing)}")

    tpl = (ROOT / "src" / "template.html").read_text(encoding="utf-8")

    # inline the bundle (raw JSON replaces the quoted placeholder string)
    payload = json.dumps(bundle, ensure_ascii=False, separators=(",", ":"))
    payload = payload.replace("</", "<\\/")  # never close the script tag early
    out = tpl.replace('"__I18N_DATA__"', payload, 1)

    # pre-render English into empty data-i18n elements for the no-JS fallback
    en = bundle["en"]

    def fill(m):
        prefix, key = m.group(1), m.group(2)
        val = get(en, key)
        return f"{prefix}{rich(val)}<" if isinstance(val, str) else m.group(0)

    out = re.sub(r'((?:data-i18n)="([^"]+)"[^>]*>)<', fill, out)

    (ROOT / "index.html").write_text(out, encoding="utf-8")
    n = len(out.encode("utf-8"))
    print(f"OK: index.html written ({n/1024:.0f} KB, {len(bundle)} languages: {', '.join(bundle)})")


if __name__ == "__main__":
    main()
