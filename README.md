# Prevoditelj: Croatian ⇄ English translator

A one-page web app for the family. Type or speak Croatian or English and it translates both ways using Claude. It also corrects Croatian mistakes, explains cases, endings and gender, gives example phrases with audio, and offers pronunciation practice with 3 tries.

Files:
- `index.html`: the whole app
- `icon-180.png`: home-screen icon
- `README.md`: this guide
- `handouts.json`: flash cards for the word lists in the *Claude outputs* handouts (loaded by the app automatically)
- `make_handouts.py`: the script that builds `handouts.json` from those word lists

**Your API key is NOT in these files, and must never be added to them.** Each person types the key into the app's Settings on their own device. It is saved only in that browser.

---

## 1. Put it online with GitHub Desktop (one time)

1. Open **GitHub Desktop** → **File → Add Local Repository…** → choose this `Translator` folder.
   If it says the folder isn't a repository, click **create a repository** and keep the defaults.
2. Write a summary such as "First version" and click **Commit to main**.
3. Click **Publish repository**. You can leave **"Keep this code private"** ticked only if your GitHub plan allows Pages on private repositories; otherwise untick it. The code contains no secrets, so a public repository is fine.
4. On github.com, open the repository → **Settings → Pages**.
   Under **Build and deployment**, set Source = *Deploy from a branch*, Branch = `main`, folder = `/ (root)`, then **Save**.
5. After a minute or two the page shows your address, something like
   `https://YOUR-USERNAME.github.io/Translator/`. That's the link for the family.

**Updating later:** replace the files in this folder, then in GitHub Desktop **Commit** → **Push origin**. The site updates within a few minutes. On devices, a refresh may be needed.

> GitHub's menus change from time to time. If a step above doesn't match what you see, look for "Pages" in the repository's Settings.

---

## 2. First use on each device

1. Open the GitHub Pages link in **Safari** (iPhone, iPad or Mac).
2. Tap ⚙︎ **Settings** → paste the Claude API key → **Save**.
3. Tap 🎤 **Speak** once and allow the microphone when Safari asks.
4. Optional: add it to the home screen. On iPhone or iPad, use Share → **Add to Home Screen**. On a Mac, use Safari's File → **Add to Dock**.
   *If voice input misbehaves in the home-screen version, use it in regular Safari instead. Apple's speech recognition has been less reliable in home-screen apps on some iOS versions.*

### Keeping the API key safe from cleared data
The key is saved in the browser on each device. Closing Safari or restarting doesn't remove it, but these do: **Clear History and Website Data**, deleting *github.io* under Safari's Website Data, and Safari's automatic clean-up of sites not opened for about 7 days (the home-screen version is exempt from that). The flash-card word lists aren't affected: they come with the app and reload by themselves.

To have a backup of the key:
- When you tap **Save** in Settings, Safari may ask whether to save the password. Tap **Save Password**. It goes into your Passwords app (iCloud Keychain) and syncs to your other Apple devices.
- If the key is ever lost, open ⚙︎ Settings, tap the key box, and pick **Prevoditelj Claude API key** from the suggestions above the keyboard.
- If Safari doesn't offer to save it, add it yourself in the **Passwords** app: tap **+**, set Website to your github.io address, User to `Prevoditelj Claude API key`, and Password to the key.
- Don't put the key anywhere in this folder. The folder is published on GitHub.

### If voice input doesn't work
- The **microphone bar** at the top always shows the state: green = ready, red pulsing = listening, amber = starting or a hint, red = problem, grey = unavailable.
- Tap **↺ Reset voice**. This fully restarts the microphone, the recogniser, playback and the practice counter. Your typed text is kept.
- The app also resets itself if the microphone hasn't started within 6 seconds, or is still listening after 20 seconds.
- If permission was denied: on iPhone or iPad, go to Settings → Apps → Safari → Microphone (or the **aA** menu in the address bar → Website Settings). On a Mac, go to Safari → Settings → Websites → Microphone.
- Apple's speech recognition may need **Dictation** (and/or Siri) turned on in device settings.

### If there's no Croatian voice for playback
On iPhone or iPad: Settings → Accessibility → Spoken Content → Voices → Croatian → download a voice.
On a Mac: System Settings → Accessibility → Spoken Content → System voice → Manage Voices → Croatian.
Then reload the page, and pick the voice in the app's Settings if you like.

---

## 3. About the API key and cost

- The app calls Claude directly from the browser, using the key saved on that device. That's fine for family use. Don't share the link and key outside the family, because anyone with the key can spend on your account.
- Strongly suggested: in the **Claude Console** (console.anthropic.com), set a **monthly spend limit** for this key. Consider creating a separate key just for this app, so you can revoke it on its own.
- The default model is **Claude Sonnet 5.5**. Anthropic's docs list it at $2 per million input tokens and $10 per million output tokens, as of October 2026; prices change, so check the pricing page. A single translation with grammar notes is a small request. I haven't measured an exact cost per translation, so watch the Console's usage page for the first few days.
- You can switch to Opus 5.5 (more careful, costs more) or Haiku 5.5 (cheaper, faster) in Settings.
- If you host other pages under the same `github.io` address, note that browser storage is shared per site address. Don't host untrusted pages there.

---

## 4. How the features work

- **Translate:** the box you typed or spoke in last is the "From" box. ⇅ swaps direction and starts fresh: it clears the text, the results and the practice panel. ⌘/Ctrl + Enter also translates.
- **Flash cards first:** if the whole text matches one of your flash cards (the Croatian side, or any English alternative on the card), the card is shown straight away and Claude isn't asked, so it costs nothing. Capitals and end punctuation are ignored, and "to", "a" or "the" at the start of the English is too. Tap **Ask Claude** for corrections, grammar and examples. Anything that isn't an exact card match goes to Claude as before.
- **Corrections:** if Croatian input has mistakes (endings, č ć š ž đ, agreement), the answer shows the corrected sentence, what changed and why. **Use this** puts the correction into the Croatian box.
- **Cases, endings & gender** (tick box): for each word that changes form, it shows the root, the case or verb form, gender, the ending, and why. It also shows what you originally typed if it was wrong, and how the ending would look for masculine, feminine and neuter words.
- **Example phrases** (tick box): 2 or 3 phrases, each with 🔊 play and 🗣 practise buttons.
- **Practise saying it:** say the Croatian sentence up to 3 times. Each try is scored word by word: ✓ matched, ≈ nearly (often a č/ć or š/s difference), ✗ not heard. Silent tries aren't counted. The score reflects what the speech recogniser heard, so treat it as a guide.
- **Studying flash cards:** pick a **Section**, then the set inside it, then tap **Study this set**. Every session goes through the whole chosen set in random order; tap ✕ to stop at any time.
  - **1 · Tako lako:** pick a Unit, Module and Lesson (or a unit's **Phrase Book**). Tick **Add everything before this…** to include all earlier vocabulary.
  - **2 · Croatian School of Boston:** pick a week (*Tjedan 1* … *Tjedan 18*) or **All weeks**. Each week holds the words from that date's main lesson and T1 page on croatianschoolofboston.org/uci.
  - **3 · Categories:** every word in the app (Tako lako, CSOB and the W00 reference sheets) sorted into 19 broad topics: greetings, phrases & sayings, people & family, body & health, food & drink, home, clothes & shopping, town & directions, travel, countries & languages, school & work, free time, nature & weather, holidays, time, numbers, describing words, verbs, and small words (question words, pronouns, prepositions, conjunctions). Each word is in exactly one category, or **All categories**.
  - Nothing about right or wrong answers is saved. There are no due dates or levels; each session starts fresh.
  - A card you miss comes back at a random later spot (at least 3 other cards in between) until you've answered it right 3 times in that session. In a set of more than 10 cards, one right answer is enough: the card drops off the list.
- **Where the words come from:** all cards are built into the app in `handouts.json`. It loads from the website each time the app opens and adds any words the device doesn't have yet; a small copy is kept so the menus work offline. There is no saving of your own cards and no iCloud file any more (both removed in v4.0).
  - `handouts.json` is generated: run `python3 make_handouts.py`, never edit it by hand. That script combines `tako-lako-all.json` (the whole Tako lako book list), the CSOB weeks, the class-worksheet lesson words (`LESSONS`) and the W00 reference sheets.
  - The categories are decided in `vocab_categories.py`: rules by word type and English keywords, the theme of the lesson or week, and a list of hand-checked words (`OVERRIDE`). To move a word, add it to `OVERRIDE` and rerun the script.
  - Adding new vocabulary: ask Claude to add it to `make_handouts.py`, rerun it, then Commit and Push in GitHub Desktop.
- **Direction:** *Croatian → English*, *English → Croatian*, or **Mixed**. In Mixed, each card picks its direction at random and the card says which language to answer in. A card you miss comes back later the other way round, and switches again on each repeat.
- **Every card is a quiz:** below the word, an answer box laid out like the Translate tab shows the direction (e.g. *English → Hrvatski*). Type your answer, or for Croatian answers tap 🎤 and say it, then tap **Check** (or press Enter/Done). Croatian answers get č ć đ š ž keys; English answers are typed only (no 🎤). **✕ Clear** empties the box. (The old *Flip & self-grade* mode was removed in v3.0.)
  - **Explain more (cases & gender):** tick this to get, after a wrong or nearly-right answer, a word-by-word breakdown of the Croatian (root, case, gender, ending and why), like Translate's *Explain cases & gender*. Unticked, you get a sentence or two. The tick is remembered; the longer explanation costs a little more per check.
  - The app checks your answer on the device first, which is free and instant. It accepts any wording listed on the card ("table / desk"), with or without bracketed hints ("American (woman)" or "American"), and ignores capitals, punctuation, and *a / the / to*.
  - If your answer isn't word-for-word the card, Claude (Haiku 5.5, the cheapest model) judges it. It accepts synonyms and explains wrong endings, cases or genders in a sentence. Each of these checks is a very small request.
  - The result is ✓ Correct, ≈ Nearly or ✗ Not quite, and the matching button (*Knew it* or *Still learning*) is outlined as the suggestion. Press Enter or tap it to accept, or tap the other button if you disagree, for example when speech recognition misheard you.
  - A typed Croatian answer with a missing or wrong č ć đ š ž counts as *Nearly*. A spoken one counts as correct, because the recogniser often can't tell those letters apart.
  - **I don't know** shows the answer straight away and suggests *Still learning*.
  - **Say it** (pronunciation practice) appears only after a ✓ Correct answer, for that card only. It's optional: say the Croatian up to 3 times and each try is scored word by word, or just tap *Knew it* to move on. It doesn't change the grade. (It replaces the old *Say it* study mode.)
- **Grammar on flash cards:** under the Croatian, each card shows the gender of every noun (masculine / feminine / neuter, plus animate or plural), its case in that sentence (with the preposition that decides it), and which words agree with it. Adjective cards show all three forms (dobar · dobra · dobro · dobri). A ⚠ line appears if a card's Croatian looks wrong. Cards that haven't been checked yet can be done with **Check now** on the Flash cards tab (needs the key). You can correct a single noun's gender with the Gender menu once the answer is shown.

## 5. Version history

The version number is shown under the app's name. It goes up with every update pushed to GitHub: the first number for big changes, the second for smaller ones, and a third (like v3.10.1) for very small additions. If your device still shows the old number after an update, reload the page (or close and reopen the home-screen app).

- **v4.1** (Nov 25, 2026): Flash cards: in a set of **more than 10 cards**, a missed card now drops off the list after **one** right answer instead of three. Sets of 10 or fewer still need 3 right.
- **v4.0** (Nov 25, 2026): **New flash-card menus.** Pick one of three sections: **1 · Tako lako** (Unit / Module / Lesson, Phrase Book and *Add everything before* as before), **2 · Croatian School of Boston** (by week, Tjedan 1–18) and **3 · Categories**, where every word in the app is sorted into 19 broad topics such as Food & drink, Verbs or Time, days & dates. The whole Tako lako book list is now built into the app, so a new device gets every word without loading a file. **Removed** to keep things simple: ☆ *Save as flash card* on the Translate tab, *My saved cards*, *Book topic lists*, the old Handout menu (the W00 reference words are in Categories) and the iCloud *Load / Save* box. Cards you saved yourself before stay on the device but no longer appear in any set.
- **v3.15** (Nov 24, 2026): 18 new handouts in the Handout picker, one per **Croatian School of Boston** class date (*CSOB Tjedan 1* … *CSOB Tjedan 18*, Sept 13 to May 16). Each holds the vocabulary from that date's main lesson and its T1 (Words) page on croatianschoolofboston.org/uci, with the site's English and its example sentence on the card (Bok, ja sam Luka! (Hi, I am Luka!)). Nouns show their gender and adjectives all three forms. 176 are new cards; the rest you already have and simply count in that week's handout as well. The matching worksheets are in the class folder as W##_CSOB-…_handout.pdf.
- **v3.14** (Nov 23, 2026): New 🎨 **Style** button next to ⚙︎ Settings. Pick how the app looks: **Classic** (the usual blue and red, light or dark with the device), **Šahovnica** (Croatian red and white), **Jadran** (Adriatic blue), **Lavanda** (lavender), **Maslina** (olive green) or **Noć** (always dark, night blue and gold). Tapping a style changes the app straight away, and it is remembered on that device only, so each person can choose their own.
- **v3.13** (Nov 21, 2026): New handout **Vrijeme (time)** in the Handout picker, from the new time study guide *W00_U0_Vrijeme_study*. 170 words and phrases: units of time from second to millennium (with 2 sata · 5 sati style counting), prekjučer … prekosutra, this / last / next week and year, ago and in (prije dva dana, za pet minuta), parts of the day (ujutro, jutros, navečer, sinoć …), telling the time (pola četiri = 3:30, četvrt do četiri, u sedam sati), days with u + accusative and the -om forms (u srijedu, subotom), months, seasons (u proljeće, ljeti, zimi), how often (obično, rijetko, jednom tjedno, s vremena na vrijeme) and everyday phrases (Samo malo!, Čekaj malo!, Kasnim, Nema žurbe, Nemam vremena …). Each card carries a usage line from the guide. About 85 are new cards; the rest (days, months, units of time, danas / sutra, question words …) you already have and simply count in this handout. The words are also in the W00 · U0 Reference set. The *sat* card also gets the meaning "hour" on new devices.
- **v3.12** (Nov 17, 2026): New handout **Prijedlozi (prepositions)** in the Handout picker, from the new prepositions sheet. It has the 34 prepositions, each card noting the case it takes (bez = without, + genitive), and 30 short phrases that practise the endings (u gradu / u grad / iz grada, kod bake / k baki / od bake, bez šećera, kod mene, sa mnom …). The prepositions moved out of the *Kratke riječi* handout, which now holds only the little everyday words and se / li, matching the shorter sheet. Your existing preposition cards keep their ids and simply count under Prijedlozi now; 30 new cards (k / ka, niz and the phrases; sa mnom and s tobom you already had, so they just count in it). The W00 · U0 Reference set still includes the prepositions. Also new: handout **Pridjevi (adjectives)**, the 138 adjectives on the new adjectives sheet (masculine form; each card shows all three forms). Nearly all are cards you already have from the book and just count in this handout; 5 are new: sladak (sweet), kiseo (sour), svjež (fresh), vruć (hot), hladan (cold).
- **v3.11** (Nov 15, 2026): New handout **W00 · U0 Reference (short words & verbs)** in the Handout picker, for reference material not tied to a class week or a Tako lako lesson. It holds all the *Kratke riječi* short words (they also stay in their own handout) and the 21 verbs from the W00_U0 Glagol sheets: each infinitive plus its 6 present-tense forms (imati = to have, imam = I have … imaju = they have), and sviđati se with its dative forms (sviđa mi se, sviđa joj se …). 143 new cards; forms you already had from the book just count in the handout. For he/she/it forms the card says "he has (also: she, it)", so type "he has" or let Claude judge "she has".
- **v3.10.1** (Nov 12, 2026): Two more flash cards for the *Lupi petama* words in Tako lako U1 · M2 · Lesson 1 (delivered in `handouts.json`): **zagrljaj** (a hug, the noun beside the verb *zagrliti*) and **golubica** (female dove; *golubica mira* = dove of peace).
- **v3.10** (Nov 12, 2026): Translate tab: Claude no longer points out capital letters or punctuation as mistakes, and the ✏️ *Corrected Croatian* box doesn't appear when those are the only differences. New 📋 **Copy** button on the translation, next to 🔊 Listen.
- **v3.9** (Nov 11, 2026): The *Short words* handout has a new page 5, *Little grammar words*: **se**, **li** and the second-place rule. Its words are now flash cards under Handout → Kratke riječi (delivered in `handouts.json`): 8 new cards (se, li, imaš li, zovem se, ne zovem se, vidimo se, sviđa mi se, Kako se kaže …?), and your existing *je li* and *Kako se zoveš?* cards now also count in that handout. (Made on Nov 7 but not pushed until now.)
- **v3.8** (Nov 11, 2026): Filled the seven beginner lessons that had no cards: Unit 1 Module 0 (Brojevi 1–21, Dani u tjednu, Mjeseci, Jedinice vremena, Boje), U2 · M1 · Lesson 1 *Odakle si?* and U2 · M3 · Lesson 4 *Moji interesi*. 73 new cards (numbers, units of time, masculine colour forms, continents and countries, phrases); 60 words you already had (days, months, feminine colours, places) just get the lesson tag. The book pages for these lessons are pictures, so the lists are standard beginner vocabulary chosen by Claude and marked "Beginner list (Claude)" on each card.
- **v3.7** (Nov 11, 2026): Added the 9 learning-objective words from the Veterans Day worksheet *Domovinski rat i glazba: Lupi petama* to Tako lako U1 · M2 · Lesson 1 (delivered in `handouts.json`): rat, prijatelji, zagrliti, zastava, suza, golub, nebo, noć, nedjelja. Words you already had (rat, nedjelja) just get the Lesson 1 tag.
- **v3.6** (Nov 7, 2026): Flash cards: after a wrong or nearly-right answer, the result shows the card's **original phrase**, what you typed and the **correct answer** together, and Claude's explanation quotes the original phrase. **Say it** dots now fill in green when you say the Croatian right (all three once it's done), and a missed card being repeated shows three dots that fill in green with each right answer.
- **v3.5** (Nov 5, 2026): Added the adjectives from Lesson 6, part 1.1.6 (Zadaci 2–4) to Tako lako U1 · M1 · Lesson 6, masculine and feminine: dobar/dobra, drag/draga, vrijedan/vrijedna, strog/stroga, simpatičan/simpatična, visok/visoka, smiješan/smiješna, ozbiljan/ozbiljna, lijep/lijepa, zanimljiv/zanimljiva. Words you already had just get the Lesson 6 tag.
- **v3.4** (Nov 4, 2026): Added the 10 bakery words from the *U pekari* worksheet to Tako lako U1 · M1 · Lesson 6 (delivered in `handouts.json`). Words you already had, such as kruh and kava, get the Lesson 6 tag added instead of a duplicate card. Also added the 48 professions from Lesson 6, Zadatak 1 (profesor / profesorica, glumac / glumica, …). When a word you already have gets a new meaning in the lesson, the meaning is added to your card (kuharica: cookbook / cook (woman)).
- **v3.3** (Nov 2, 2026): New **Handout** picker on the Flash cards tab, with 460 words from the eight vocabulary handouts in *Claude outputs*. They load automatically from `handouts.json`.
- **v3.2** (Nov 1, 2026): Fixed "Claude didn't return a usable check": Claude must now always answer in the app's check format, gets more room for its reply, and the app retries once automatically.
- **v3.1** (Nov 1, 2026): Flash cards: 🔊 Listen only appears for Croatian; no Listen button on English words, on either the question or the answer side.
- **v3.0** (Nov 1, 2026): Flash cards redesigned as a quiz: every card has an answer box like the Translate tab, with **Check**, **I don't know**, **✕ Clear**, and an **Explain more (cases & gender)** tick box. *Flip & self-grade* removed.
- **v2.9** (Nov 1, 2026): Flash cards: **Mixed** direction; English answers are typed only (🎤 only for Croatian answers); missed cards come back in the opposite direction in Mixed mode; new **I don't know** button.
- **v2.8**: Version before this history was started.
