# Prevoditelj (Translator): brief for Claude Code

Single-page Croatian ⇄ English app for the family. `index.html` is the whole app, published
from this repo with GitHub Pages. **The repo is public.**

## Rule one: no keys in files
- Never put an API key, or anything key-like, in any file here. Keys are typed into the app's
  Settings on each device and live only in that browser's storage.
- Before every commit, check: `git diff --cached | grep -n 'sk-ant'` must find only the
  placeholder in the Settings key box.

## Conventions that keep the key safe
- Render Claude's replies and any data-file text with `textContent`, never `innerHTML`.
  `innerHTML` is used only for fixed button icons.
- Add no external scripts or CDN libraries.

## Housekeeping
- `SPECIFICATION.md` describes the app as built. Read it first; update the matching section with every change.
- Every change: raise the version under the app name and add a line to the README version history.
- `handouts.json` is generated: edit `make_handouts.py` (words) or `vocab_categories.py` (Categories section) and rerun `make_handouts.py`, never hand-edit the JSON. It holds every flash card (Tako lako from `tako-lako-all.json`, CSOB weeks, W00 sheets); since v4.0 there is no adding of outside vocabulary and no iCloud file.
- Handout PDFs live in `~/Documents/Taka Lako Class/Claude outputs` (not in this repo).
- Repo location moved on 13 Nov 2026 from `Documents/Taka Lako Class/Translator` to `~/Claude/Code/Translator`.
