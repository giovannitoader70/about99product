#!/usr/bin/env python3
"""Create a new script from the template and add it to data/videos.json.

Example:
  python tools/new_script.py "Ketchup" --skip 8 --safe 3 --category food
"""
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("product", help="The product (e.g. Ketchup)")
    p.add_argument("--skip", type=int, default=7)
    p.add_argument("--safe", type=int, default=3)
    p.add_argument("--category", default="food")
    a = p.parse_args()

    data_file = ROOT / "data" / "videos.json"
    videos = json.loads(data_file.read_text(encoding="utf-8"))
    n = max(v["n"] for v in videos) + 1
    slug = slugify(a.product)
    title = f"{a.skip} {a.product} Brands to Skip (And {a.safe} That Are Actually Safe)"

    if any(v["slug"] == slug for v in videos):
        sys.exit(f"A video with the slug '{slug}' already exists.")

    videos.append({"n": n, "slug": slug, "title": title, "category": a.category,
                   "skip": [], "safe": [], "angles": []})
    data_file.write_text(json.dumps(videos, indent=2, ensure_ascii=False), encoding="utf-8")

    tpl = (ROOT / "templates" / "video-template.md").read_text(encoding="utf-8")
    tpl = tpl.replace("# [NUMBER] [Category] Brands to Skip (And [NUMBER] That Are Actually Safe)", f"# {title}")
    tpl = tpl.replace("- Video nr: ", f"- Video nr: {n}", 1).replace("- Category: ", f"- Category: {a.category}", 1)
    out = ROOT / "scripts" / f"{n:02d}-{slug}.md"
    out.write_text(tpl, encoding="utf-8")
    print(f"Created: {out.relative_to(ROOT)}")
    print("Then run: python tools/build_site.py")


if __name__ == "__main__":
    main()
