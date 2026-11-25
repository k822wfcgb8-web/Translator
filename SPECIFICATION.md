# Prevoditelj (Translator): specification.md

Status: **describes the app as built (v4.1).** Written after the fact. Treat the current behaviour as what was intended all along.
Revision 1 (24 Nov 2026).

This file is committed to a **public** GitHub repo. It must contain no personal information: no names, no home-folder paths, no account names, no keys.

Keeping it current: every change to the app updates the matching section here, as well as the version number and the README version history (Section 10.4).

---

## 1. Purpose

**Prevoditelj** ("translator") is a one-page Croatian ⇄ English web app for a family learning Croatian. It does two jobs:

1. **Translate:** you type or speak Croatian or English and it translates in either direction using Claude. When the input is Croatian it also corrects mistakes and explains cases, endings and gender, gives example phrases with audio, and offers pronunciation practice.
2. **Flash cards:** you quiz yourself on the class vocabulary (Tako lako, Croatian School of Boston, class reference sheets), typing or speaking your answers, with free on-device checking and Claude as the judge when your wording differs.

### How it differs from Učitelj
Prevoditelj is **user-driven**: you choose what to translate or which set to study. Učitelj (a separate, planned app) is the tutor-driven course. The two stay separate.

### Scope
- Croatian is **standard Croatian** (hrvatski standardni jezik): ijekavian, Croatian vocabulary, correct č ć đ š ž.
- No accounts, no server, no saved study history. Each device works on its own.
- No adding outside vocabulary (removed in v4.0, Section 9).

---

## 2. Users and Devices

- **Users:** family members, each on their own device. No profiles or logins inside the app.
- **Platform:** Safari on iPhone, iPad and Mac. It can be added to the Home Screen (iOS) or the Dock (Mac) with `icon-180.png`. Other modern browsers should work but aren't the target.
- **Hosting:** GitHub Pages, from the root of the `main` branch of a public repo.
- **API key:** each user types their own Claude API key into Settings on each device (Section 7.1).

---

## 3. Translate Tab

### 3.1 Input
- **One input box with a direction toggle** (Croatian → English or English → Croatian). The box you last typed or spoke in sets the "From" language. **⇅** swaps direction and starts fresh: it clears the text, the results and the practice panel.
- **Diacritic keys** under the box: ⇧ (capitalises the next letter only), č ć đ š ž.
- **Buttons:** 🎤 Speak, 🔊 Listen (Croatian only; there's no Listen for English input), 🗣 Practise saying it, ✕ Clear (text and results).
- **Options:** *Explain cases & gender* (on by default) and *Example phrases* (off by default). Both are remembered.
- **Translate** button; ⌘/Ctrl + Enter also translates. A setting can make it translate automatically after speaking (on by default).
- If there's no API key, a banner at the top asks for one and links to Settings.

### 3.2 Flash cards first (free)
Before calling Claude, the app checks whether the whole input matches a flash card: the Croatian side, or any English alternative on the card. Capitals and end punctuation are ignored, and so is a leading "to", "a" or "the" in English. On a match the card is shown straight away and Claude is not called. An **Ask Claude: corrections, grammar & examples** button sends it to Claude anyway.

### 3.3 Claude's answer
Claude replies through a tool (structured output) with:
- `detected_language`: trusted over the box the text was typed in. Croatian typed in the English box is still treated as Croatian.
- `corrected_input` and `corrections` (original, corrected, explanation). **Capitalisation and punctuation are never treated as mistakes.**
- `translation`.
- `croatian_text`: the correct Croatian that the grammar notes describe.
- `grammar` (only when asked for): one entry for each inflecting word (nouns, adjectives, pronouns, numerals, verbs). Each entry has the word, root or dictionary form, part of speech, form (case + number, or tense + person + number), gender, ending, why that form is used (naming the preposition or verb that decides the case), `user_wrote` if the user got that word wrong, and `gender_compare` (the same case for masculine, feminine and neuter).
- `examples` (only when asked for): 2 or 3 Croatian/English phrases.
- `notes`.

### 3.4 Results display
- **✏️ Corrected Croatian** card: shown only when the Croatian input had a real correction. A difference only in capitals or punctuation doesn't count. It shows the corrected sentence, then each change as *was → now* with its explanation. **Use this** puts the correction into the input box. It also has 🔊.
- **Translation** card with 🔊 Listen and 📋 **Copy**.
- **Cases, endings & gender** card: one box per word. If the user wrote a word wrongly, it says "You wrote X. The correct form is Y."
- **Example phrases**, each with 🔊 play and 🗣 practise.
- All text from Claude is shown with `textContent` (Section 10.2).

---

## 4. Pronunciation Practice

- Opened with 🗣 on the input or on an example phrase. If the input was corrected, the corrected Croatian is the target, and a note says so.
- **Listen first** plays the target. **Say it** records one try. **Start over** resets.
- **Up to 3 tries.** Each try is scored word by word against the target: ✓ matched, ≈ nearly (often a č/ć or š/s difference), ✗ not heard. Silent tries aren't counted.
- The score shows what the speech recogniser heard, so it's a guide, not a judgement on accent.

---

## 5. Flash Cards Tab

### 5.1 Choosing a set
- **Direction:** Croatian → English, English → Croatian, or **Mixed**. In Mixed each card picks a direction at random, and the card says which language to answer in.
- **Section** (one of three), then the set inside it:
  1. **Tako lako:** Unit, Module and Lesson, or a unit's **Phrase Book**. A tick box, **Add everything before this…**, adds all earlier vocabulary.
  2. **Croatian School of Boston:** a week (*Tjedan 1* … *Tjedan 18*) or **All weeks**.
  3. **Categories:** one of 19 broad topics, or **All categories**. Every card is in exactly one category.
- Each menu shows how many cards it holds. The same Croatian on two cards is studied only once.
- The last choices are remembered on the device.
- **Study this set** starts a session.

### 5.2 Study session
- The session goes through **the whole chosen set in random order**. ✕ ends it at any time. At the end, a message shows how many cards were done and how many were known first time.
- The progress line reads *N done · M to go*.
- **A missed card** ("Still learning") comes back at a random later spot, with at least **3** other cards in between. If too few cards are left, random cards from the same session are added as fillers. A filler that comes up is extra review and doesn't count as done.
  - **Set of 10 cards or fewer:** the card stays until it has been answered right **3 times in total**. The progress line shows *this one: k of 3 right*, with dots. Missing it again keeps the count.
  - **Set of more than 10 cards:** **one** right answer drops the card off the list. The progress line shows *missed earlier*.
  - In Mixed mode a repeated card comes back the other way round, and switches again on each repeat.
- **Nothing about right or wrong answers is saved.** There are no due dates, levels or streaks. Every session starts fresh.

### 5.3 Answering (every card is a quiz)
- Under the prompt is an answer box laid out like the Translate tab, labelled with the direction (e.g. *English → Hrvatski*).
- **Croatian answers:** typed with the č ć đ š ž keys, or spoken with 🎤. **English answers:** typed only, with no 🎤.
- **Check** (or Enter/Done) checks the answer. **✕ Clear** empties the box. **I don't know** shows the answer and suggests *Still learning*.
- **On-device check first** (free and instant):
  - Accepts any alternative on the card ("table / desk"), with or without bracketed hints ("American (woman)" or "American").
  - Ignores capitals, punctuation and *a / the / to*.
  - If only č ć đ š ž differ, a **typed** Croatian answer is ≈ *Nearly*, but a **spoken** one counts as ✓ correct, because the recogniser often can't tell those letters apart.
- **Claude as judge:** if the answer isn't an on-device match, Claude Haiku 5.5 judges it. It returns a verdict of `correct`, `nearly` or `wrong` and one or two sentences of feedback. It accepts synonyms, either formal or informal "you", and small English slips. With **Explain more (cases & gender)** ticked (remembered), a wrong or nearly-right answer also gets a word-by-word grammar breakdown like the one on the Translate tab.
- **Result:** ✓ Correct, ≈ Nearly, ✗ Not quite (or *Compare your answer* if no verdict was possible). It shows your answer and, when it wasn't right, the correct answer.
- **Grading:** the user always decides. The suggested button (*Knew it ✓* or *Still learning*) is outlined, and Enter accepts it. Tapping the other button overrides the suggestion, for example when the recogniser misheard.
- **Say it:** after a ✓ Correct only, optional pronunciation practice of the card's Croatian, with up to 3 tries scored as in Section 4. It doesn't affect the grade.

### 5.4 Grammar on cards
- Under the Croatian, each card shows the gender of every noun (masculine, feminine or neuter, plus animate or plural), its case in that phrase (with the preposition that decides it), and which words agree with it.
- Adjective cards show all three forms (dobar · dobra · dobro).
- A ⚠ line appears if a card's Croatian looks wrong (with the suggested fix).
- Most cards come with this information from the word lists. Cards without it can be filled in by Claude with **Classify now** (needs the key; uses the chosen model).
- Once the answer is shown, a single noun's gender can be corrected with the **Gender** menu. A user's own choice always wins over Claude's.

### 5.5 Deleting a card
🗑 on a card deletes it **on this device only**. It takes two taps: the first arms the button.

---

## 6. Voice

### 6.1 Listening (speech recognition)
- Safari's built-in speech recognition: hr-HR for Croatian and en-US for English. It needs a secure (https) address.
- A **microphone bar** at the top always shows the state: green = ready, red pulsing = listening, amber = starting or a hint, red = problem, grey = unavailable. Errors get plain-language hints (e.g. turn on Dictation or Siri, how to allow the microphone).
- **↺ Reset voice** fully restarts the microphone, the recogniser, playback and the practice counter, and keeps the typed text.
- **Watchdogs:** the app resets itself if the microphone hasn't started within 6 seconds, or is still listening after 20 seconds.

### 6.2 Speaking (speech synthesis)
- Safari's speech synthesis, with a Croatian (hr-HR) and an English voice chosen in Settings. Croatian speed: Slow, Relaxed (default) or Normal.
- If no Croatian voice is installed, the app says how to add one on iOS and on the Mac.

---

## 7. Settings and Style

### 7.1 Settings (⚙︎)
- **Claude API key** with *Show key*. Stored only in that browser. Saving can trigger Safari's *Save Password*, so the key can be recovered from iCloud Keychain. **Remove API key from this device** clears it.
- **Claude model** for translation and *Classify now*: Sonnet 5.5 (default), Opus 5.5 or Haiku 5.5.
- **Croatian voice** and **English voice**, with test buttons.
- **Croatian speaking speed.**
- **Translate automatically after speaking.**

### 7.2 Style (🎨)
Six looks, applied straight away and remembered on that device only:

| Style | Look |
|---|---|
| **Classic** (default) | Blue and red; follows the device's light or dark mode |
| **Šahovnica** | Croatian red and white, with flag blue |
| **Jadran** | Adriatic sea blue with a sunset orange |
| **Lavanda** | Soft Hvar lavender purple |
| **Maslina** | Olive green on warm cream |
| **Noć** | Always dark: night blue with gold |

The style is applied before the page draws, so there's no flash of the wrong colours.

---

## 8. Claude Models and Cost

| Use | Model |
|---|---|
| Translation, corrections, grammar, examples | User's choice in Settings (default Sonnet 5.5) |
| *Classify now* (grammar on cards) | User's choice in Settings |
| Flash-card answer judging | **Haiku 5.5**, fixed (cheap, fast) |

- Calls go straight from the browser to the Claude Messages API, using the device's key (`anthropic-dangerous-direct-browser-access`). Structured answers come back through tools.
- Free paths come first: exact flash-card matches on Translate (3.2) and on-device answer checks (5.3) never call Claude.
- There's no spend meter in the app. The README recommends a monthly spend limit and a separate key in the Claude Console.

---

## 9. Data and Storage

### 9.1 On each device (browser storage)
Everything is kept under keys starting with `prev.`, and read and written defensively, so blocked or private-mode storage can't break the app. It holds the settings, the style, the last tab, the Translate options, the flash-card choices and options, the card list with any grammar and gender edits and deletions, and a small offline copy of the set index. **No study results are saved.**

### 9.2 The word lists: `handouts.json`
- **Generated, never edited by hand.** Built by `python3 make_handouts.py`, which combines:
  - `tako-lako-all.json`: the whole Tako lako book list
  - the Croatian School of Boston weeks (Tjedan 1–18)
  - the class-worksheet lesson words
  - the W00 reference sheets (short words, prepositions, adjectives, verbs, time, …)
- **Categories** are decided in `vocab_categories.py`: rules by word type and English keywords, the theme of the lesson or week, and a hand-checked `OVERRIDE` list. To move a word, add it to `OVERRIDE` and rerun the build.
- **Card fields:** `id`, `hr`, `en` (alternatives separated by " / "), `note` (source line, word type, usage), `gram` (part of speech, gender, animate, forms, who set it), `cat`, `ho` (handout or lesson tags), plus timestamps and flags.
- **Loading:** the app fetches `handouts.json` (no cache) each time it opens and adds any cards the device doesn't have yet. If it's offline, the saved index keeps the menus working.
- **Rule:** every new word or phrase added to the app must also be a flash card.

### 9.3 Removed in v4.0
☆ *Save as flash card* on Translate, *My saved cards*, *Book topic lists*, the old Handout menu, and the iCloud *Load / Save* file. Cards a user saved before stay on that device but appear in no set.

---

## 10. Technical Conventions

### 10.1 Layout
- `index.html` is the whole app: HTML, CSS and plain JavaScript in one file. **No build tools, no external scripts, no CDN libraries.**
- Other repo files: `icon-180.png`, `README.md`, `CLAUDE.md`, this file, `handouts.json`, `make_handouts.py`, `vocab_categories.py`, `tako-lako-all.json`.

### 10.2 Safety
- **Rule one, no keys in files.** Before every commit, `git diff --cached | grep -n 'sk-ant'` must find only the placeholder in the Settings key box.
- Claude's replies and all data-file text are shown with `textContent`, never `innerHTML`. `innerHTML` is used only for fixed button icons.
- No Google or Meta services, fonts, analytics or speech APIs.

### 10.3 Language rules for Claude
- Standard Croatian (ijekavian, Croatian vocabulary, correct diacritics).
- Never correct capitalisation or punctuation.

### 10.4 Housekeeping
- **Every change** raises the version under the app name and adds a line to the README version history. The first number is for big changes, the second for smaller ones, and a third (like v3.10.1) for very small additions.
- Update this specification in the same change.

---

## How to work on it (for a new session)
Tell Claude: "Change the Translator: …". Claude reads `CLAUDE.md` and this file, makes the change in `index.html` (or the word-list scripts, then reruns `make_handouts.py`), raises the version, adds a README version line, updates this file, and runs the key check. The user commits and pushes with GitHub Desktop.
