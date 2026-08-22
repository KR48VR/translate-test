#!/usr/bin/env python3
"""Verbatim-overlap gate: verify the master text is an original retelling, not a
copy. Finds runs of N+ consecutive words shared between the source text and the
master's leaf strings.

Usage:
    python3 check_overlap.py --source source.txt --master i18n/en.json [--n 8]

Testing showed even a well-intentioned "original retelling" can leak copied
sentence fragments — run this on every third-party-source project and rewrite
any flagged run (proper nouns, figures and titles that must repeat are fine;
whole copied clauses are not). Exit 1 when overlaps are found.
"""
import argparse
import json
import re
import sys
from pathlib import Path


def words(text):
    return re.findall(r"[a-z0-9']+", text.lower())


def leaves(d):
    out = []
    for v in d.values():
        if isinstance(v, dict):
            out.extend(leaves(v))
        elif isinstance(v, str):
            out.append(v)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="captured source text (plain text)")
    ap.add_argument("--master", required=True, help="master i18n JSON")
    ap.add_argument("--n", type=int, default=8, help="minimum run length in words")
    args = ap.parse_args()

    src_words = words(Path(args.source).read_text(encoding="utf-8"))
    shingles = {}
    for i in range(len(src_words) - args.n + 1):
        shingles.setdefault(tuple(src_words[i : i + args.n]), i)

    master = json.loads(Path(args.master).read_text(encoding="utf-8"))
    hits = []
    for leaf in leaves(master):
        w = words(re.sub(r"<[^>]+>", " ", leaf))
        i = 0
        while i <= len(w) - args.n:
            key = tuple(w[i : i + args.n])
            if key in shingles:
                j = i + args.n
                s = shingles[key] + args.n
                while j < len(w) and s < len(src_words) and w[j] == src_words[s]:
                    j += 1
                    s += 1
                hits.append(" ".join(w[i:j]))
                i = j
            else:
                i += 1

    if hits:
        print(f"OVERLAP: {len(hits)} verbatim run(s) of {args.n}+ words shared with the source:")
        for h in sorted(set(hits), key=len, reverse=True)[:20]:
            print(f"  [{len(h.split())} words] {h[:120]}")
        print("Rewrite these in your own words (repeated names/figures/titles are fine; copied clauses are not).")
        sys.exit(1)
    print(f"OK: no verbatim runs of {args.n}+ words shared with the source.")


if __name__ == "__main__":
    main()
