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
- Every change: raise the version under the app name and add a line to the README version history.
- `handouts.json` is generated: edit `make_handouts.py` and rerun it, never hand-edit the JSON.
- Handout PDFs live in `~/Documents/Taka Lako Class/Claude outputs` (not in this repo).
- Repo location moved on 13 Nov 2026 from `Documents/Taka Lako Class/Translator` to `~/Claude/Code/Translator`.
