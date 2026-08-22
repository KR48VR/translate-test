#!/usr/bin/env python3
"""Structural gate for i18n translation files: key parity, number parity,
markup parity, and placeholder survival against the master file.

Usage:
    python3 check_i18n.py --dir i18n --master en [--numflex zh,yue,ja,ko] [codes...]

With no codes given, every *.json in --dir except the master is checked.
Exit code 1 if any file fails. Run this after EVERY translation or edit pass —
it has caught real defects (lost placeholders, dropped numbers) on every
project it has been used on.
"""
import argparse
import json
import re
import sys
from pathlib import Path


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
    toks = re.findall(r"\d+(?:[.,   ]\d+)*", str(s))
    return sorted(re.sub(r"[.,   ]", "", t) for t in toks)


def tags(s):
    return sorted(re.findall(r"<span class=['\"][^'\"]+['\"]>|</span>|<br\s*/?>", str(s)))


def check(code, i18n_dir, master, numflex):
    f = i18n_dir / f"{code}.json"
    if not f.exists():
        return [f"{code}: MISSING FILE"]
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"{code}: INVALID JSON — {e}"]
    errs = []
    en_l, tr_l = leaves(master), leaves(data)
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
        if code not in numflex and nums(v) != nums(t):
            en_only = set(nums(v)) - set(nums(t))
            if en_only:
                errs.append(f"{code}: numbers {sorted(en_only)} lost at {k}")
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="i18n")
    ap.add_argument("--master", default="en")
    ap.add_argument("--numflex", default="zh,yue,ja,ko",
                    help="codes allowed to reformat large numbers natively (万/億/억…)")
    ap.add_argument("codes", nargs="*")
    args = ap.parse_args()

    i18n_dir = Path(args.dir)
    master = json.loads((i18n_dir / f"{args.master}.json").read_text(encoding="utf-8"))
    numflex = set(args.numflex.split(","))
    codes = args.codes or sorted(
        p.stem for p in i18n_dir.glob("*.json") if p.stem != args.master
    )
    bad = False
    for c in codes:
        errs = check(c, i18n_dir, master, numflex)
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
