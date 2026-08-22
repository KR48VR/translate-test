#!/usr/bin/env python3
"""Structural gate for i18n files: key parity, number parity, markup parity vs en.json."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
EN = json.loads((ROOT / "i18n" / "en.json").read_text(encoding="utf-8"))

# CJK languages legitimately reformat some numerals (9,200万 / 3億 / 1.7억…)
NUM_FLEX = {"zh", "yue", "ja", "ko"}


def leaves(d, prefix=""):
    out = {}
    for k, v in d.items():
        p = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            out.update(leaves(v, p))
        else:
            out[p] = v
    return out


def nums(s):
    # normalize locale separators (60,000 / 60.000 / 60 000) to bare digit runs
    toks = re.findall(r"\d+(?:[.,   ]\d+)*", str(s))
    return sorted(re.sub(r"[.,   ]", "", t) for t in toks)


def tags(s):
    return sorted(re.findall(r"<span class=['\"]hl(?:New)?['\"]>|</span>|<br\s*/?>", str(s)))


def check(code):
    f = ROOT / "i18n" / f"{code}.json"
    if not f.exists():
        return [f"{code}: MISSING FILE"]
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"{code}: INVALID JSON — {e}"]
    errs = []
    en_l, tr_l = leaves(EN), leaves(data)
    for k in en_l:
        if k not in tr_l:
            errs.append(f"{code}: missing key {k}")
    for k in tr_l:
        if k not in en_l:
            errs.append(f"{code}: extra key {k}")
    meta = data.get("_meta", {})
    if meta.get("code") != code:
        errs.append(f"{code}: _meta.code is {meta.get('code')!r}")
    for k, v in en_l.items():
        if k.startswith("_meta") or k not in tr_l:
            continue
        t = tr_l[k]
        if not isinstance(t, str) or not t.strip():
            errs.append(f"{code}: empty value at {k}")
            continue
        if tags(v) != tags(t):
            errs.append(f"{code}: markup mismatch at {k}: {tags(v)} vs {tags(t)}")
        for ph in re.findall(r"\{[a-z]+\}", v, re.I):
            if ph not in t:
                errs.append(f"{code}: placeholder {ph} lost at {k}")
        if code not in NUM_FLEX and nums(v) != nums(t):
            # dates may be legitimately reformatted; only flag when digits are truly lost
            en_only = set(nums(v)) - set(nums(t))
            if en_only:
                errs.append(f"{code}: numbers {sorted(en_only)} lost at {k} (en={nums(v)} tr={nums(t)})")
    return errs


def main():
    codes = sys.argv[1:] or ["zh", "ms", "ta", "sg", "yue", "th", "vi", "ja", "ko", "hi", "ml", "si", "fr", "es", "de", "nl", "ru"]
    bad = False
    for c in codes:
        errs = check(c)
        if errs:
            bad = True
            print(f"--- {c}: {len(errs)} issue(s)")
            for e in errs[:20]:
                print("   ", e)
        else:
            print(f"OK  {c}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
