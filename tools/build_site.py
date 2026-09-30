#!/usr/bin/env python3
"""Generate docs/index.html (static site for GitHub Pages) from data/videos.json."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
videos = json.loads((ROOT / "data" / "videos.json").read_text(encoding="utf-8"))

LABELS = {"food": "Food", "personal-care": "Personal care", "household": "Household"}

cards = []
for v in reversed(videos):
    angles = "".join(f"<li>{escape(a)}</li>" for a in v["angles"][:5])
    angles_html = f"<ul>{angles}</ul>" if angles else ""
    counts = []
    if v["skip"]:
        counts.append(f"{len(v['skip'])} to avoid")
    if v["safe"]:
        counts.append(f"{len(v['safe'])} safe")
    meta = " · ".join(filter(None, [LABELS.get(v["category"], v["category"]), v.get("runtime"), ", ".join(counts)]))
    cards.append(
        f'<article data-cat="{escape(v["category"])}"><h2>{escape(v["title"])}</h2>'
        f'<p class="meta">{escape(meta)}</p>{angles_html}</article>'
    )

cats = sorted({v["category"] for v in videos})
buttons = '<button class="on" data-f="all">All</button>' + "".join(
    f'<button data-f="{escape(c)}">{escape(LABELS.get(c, c))}</button>' for c in cats
)

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>About99Product</title>
<meta name="description" content="Investigations into everyday products: what to avoid and what is actually safe.">
<style>
:root {{ --bg:#fafaf7; --fg:#1c1c1a; --muted:#6b6b66; --card:#fff; --line:#e4e4de; --accent:#c8321e; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#141412; --fg:#f2f2ee; --muted:#a2a29a; --card:#1e1e1b; --line:#333330; --accent:#ff6b52; }} }}
* {{ box-sizing:border-box }}
body {{ margin:0; background:var(--bg); color:var(--fg); font:16px/1.55 system-ui,sans-serif }}
main {{ max-width:760px; margin:0 auto; padding:32px 16px 64px }}
h1 {{ font-size:2rem; margin:0 0 4px }}
.sub {{ color:var(--muted); margin:0 0 24px }}
.filters {{ display:flex; gap:8px; flex-wrap:wrap; margin-bottom:20px }}
button {{ font:inherit; padding:6px 14px; border:1px solid var(--line); border-radius:999px; background:var(--card); color:var(--fg); cursor:pointer }}
button.on {{ background:var(--accent); border-color:var(--accent); color:#fff }}
article {{ background:var(--card); border:1px solid var(--line); border-radius:12px; padding:16px 18px; margin-bottom:12px }}
article h2 {{ font-size:1.05rem; margin:0 0 4px }}
.meta {{ color:var(--muted); font-size:.85rem; margin:0 0 6px }}
ul {{ margin:6px 0 0; padding-left:1.1rem; color:var(--muted); font-size:.9rem }}
footer {{ margin-top:32px; color:var(--muted); font-size:.85rem }}
[hidden] {{ display:none }}
</style>
</head>
<body>
<main>
<h1>About99Product</h1>
<p class="sub">Investigations into everyday products: what to avoid and what is actually safe.</p>
<div class="filters">{buttons}</div>
{"".join(cards)}
<footer>Informational content based on public sources. Not a substitute for professional advice.</footer>
</main>
<script>
document.querySelectorAll('.filters button').forEach(b => b.addEventListener('click', () => {{
  document.querySelectorAll('.filters button').forEach(x => x.classList.toggle('on', x === b));
  document.querySelectorAll('article').forEach(a => a.hidden = b.dataset.f !== 'all' && a.dataset.cat !== b.dataset.f);
}}));
</script>
</body>
</html>
"""
(ROOT / "docs" / "index.html").write_text(html, encoding="utf-8")
print(f"Site generated: docs/index.html ({len(videos)} videos)")
