# About99Product

Working library for the About99Product channel: scripts, series template, product database, website and small automations.

## Structure

- `scripts/` one file per video (metadata + a place for the voiceover script)
- `templates/video-template.md` template for the "X brands to skip / Y that are safe" series
- `data/videos.json` main source of truth for all videos
- `data/products.csv` one row per brand (fill in ingredients, concerns and sources)
- `data/flags.json` problematic ingredients that are searched for automatically
- `tools/` Python scripts
- `docs/index.html` website for GitHub Pages

## Commands (Python 3, no external packages)

```
python tools/new_script.py "Ketchup" --skip 8 --safe 3   # new video from the template
python tools/compare_products.py "Dawn" "Joy"            # compare ingredients
python tools/compare_products.py --flags                 # flag problematic ingredients
python tools/build_site.py                               # regenerate the website
```

## Publishing the site on GitHub Pages

1. On GitHub: Settings → Pages
2. Source: "Deploy from a branch", branch `main`, folder `/docs`
3. The site appears at `https://<username>.github.io/<repo-name>/`

## Note

The files in `scripts/` currently contain only each video's metadata. Paste the full voiceover text into the "Voiceover script" section.
