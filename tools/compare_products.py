#!/usr/bin/env python3
"""Compare the ingredients of several products from data/products.csv.

Fill in the `ingredients` column (separated by `;`) in the CSV, then:
  python tools/compare_products.py "Dawn" "Joy" "Dr. Bronner's"
  python tools/compare_products.py --flags          # look for problematic ingredients across the whole CSV
"""
import argparse, csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_rows():
    with open(ROOT / "data" / "products.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def split_ing(text):
    return {i.strip().lower() for i in text.split(";") if i.strip()}


def compare(names, rows):
    found = {}
    for n in names:
        match = [r for r in rows if r["brand"].lower() == n.lower()]
        if not match:
            sys.exit(f"Brand '{n}' is not in products.csv")
        found[n] = split_ing(match[0]["ingredients"])
        if not found[n]:
            print(f"Warning: '{n}' has no ingredients filled in.")
    common = set.intersection(*found.values()) if found else set()
    print(f"\nCommon to all ({len(common)}): {', '.join(sorted(common)) or '-'}")
    for n, ing in found.items():
        unique = ing - set.union(*(v for k, v in found.items() if k != n)) if len(found) > 1 else ing
        print(f"Only in {n} ({len(unique)}): {', '.join(sorted(unique)) or '-'}")


def flags(rows):
    watch = json.loads((ROOT / "data" / "flags.json").read_text(encoding="utf-8"))
    hits = 0
    for r in rows:
        ing = split_ing(r["ingredients"])
        for flag, info in watch.items():
            if any(flag in i for i in ing):
                hits += 1
                print(f"[{r['verdict'].upper():4}] {r['brand']} ({r['video_slug']}): {flag} -> {info}")
    if not hits:
        print("No matches (or ingredients are not filled in yet).")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("brands", nargs="*")
    p.add_argument("--flags", action="store_true")
    a = p.parse_args()
    rows = load_rows()
    if a.flags:
        flags(rows)
    elif len(a.brands) >= 2:
        compare(a.brands, rows)
    else:
        p.error("Give at least two brands or use --flags")
