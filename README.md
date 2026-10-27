# Prevoditelj: Croatian ⇄ English translator

A one-page web app for the family. Type or speak Croatian or English and it translates both ways using Claude. It also corrects Croatian mistakes, explains cases, endings and gender, gives example phrases with audio, and offers pronunciation practice with 3 tries.

Files:
- `index.html`: the whole app
- `icon-180.png`: home-screen icon
- `README.md`: this guide

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
The key is saved in the browser on each device. Closing Safari or restarting doesn't remove it, but these do: **Clear History and Website Data**, deleting *github.io* under Safari's Website Data, and Safari's automatic clean-up of sites not opened for about 7 days (the home-screen version is exempt from that). Your flash-card progress on that device goes with it, so use **Save to iCloud** regularly.

To have a backup of the key:
- When you tap **Save** in Settings, Safari may ask whether to save the password. Tap **Save Password**. It goes into your Passwords app (iCloud Keychain) and syncs to your other Apple devices.
- If the key is ever lost, open ⚙︎ Settings, tap the key box, and pick **Prevoditelj Claude API key** from the suggestions above the keyboard.
- If Safari doesn't offer to save it, add it yourself in the **Passwords** app: tap **+**, set Website to your github.io address, User to `Prevoditelj Claude API key`, and Password to the key.
- Don't put the key in the iCloud cards file or anywhere in this folder. The folder is published on GitHub.

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

- **Translate:** the box you typed or spoke in last is the "From" box. ⇅ swaps direction. ⌘/Ctrl + Enter also translates.
- **Flash cards first:** if the whole text matches one of your flash cards (the Croatian side, or any English alternative on the card), the card is shown straight away and Claude isn't asked, so it costs nothing. Capitals and end punctuation are ignored, and "to", "a" or "the" at the start of the English is too. Tap **Ask Claude** for corrections, grammar and examples. Anything that isn't an exact card match goes to Claude as before.
- **Corrections:** if Croatian input has mistakes (endings, č ć š ž đ, agreement), the answer shows the corrected sentence, what changed and why. **Use this** puts the correction into the Croatian box.
- **Cases, endings & gender** (tick box): for each word that changes form, it shows the root, the case or verb form, gender, the ending, and why. It also shows what you originally typed if it was wrong, and how the ending would look for masculine, feminine and neuter words.
- **Example phrases** (tick box): 2 or 3 phrases, each with 🔊 play and 🗣 practise buttons.
- **Practise saying it:** say the Croatian sentence up to 3 times. Each try is scored word by word: ✓ matched, ≈ nearly (often a č/ć or š/s difference), ✗ not heard. Silent tries aren't counted. The score reflects what the speech recogniser heard, so treat it as a guide.
- **Answer by typing or speaking** (Flash cards tab → *Answer by: Type or speak*): instead of flipping the card and grading yourself, type your answer or tap 🎤 and say it, then tap **Check** (or press Enter/Done). Works in both directions; Croatian answers get č ć đ š ž keys.
  - The app checks your answer on the device first, which is free and instant. It accepts any wording listed on the card ("table / desk"), with or without bracketed hints ("American (woman)" or "American"), and ignores capitals, punctuation, and *a / the / to*.
  - If your answer isn't word-for-word the card, Claude (Haiku 5.5, the cheapest model) judges it. It accepts synonyms and explains wrong endings, cases or genders in a sentence. Each of these checks is a very small request.
  - The result is ✓ Correct, ≈ Nearly or ✗ Not quite, and the matching button (*Knew it* or *Still learning*) is outlined as the suggestion. Press Enter or tap it to accept, or tap the other button if you disagree, for example when speech recognition misheard you.
  - A typed Croatian answer with a missing or wrong č ć đ š ž counts as *Nearly*. A spoken one counts as correct, because the recogniser often can't tell those letters apart.
  - **Don't know** shows the answer and suggests *Still learning*. *Flip & self-grade* works exactly as before.
  - **Say it** (pronunciation practice) appears only after a ✓ Correct answer, for that card only. It's optional: say the Croatian up to 3 times and each try is scored word by word, or just tap *Knew it* to move on. It doesn't change the grade. (It replaces the old *Say it* study mode.)
- **Grammar on flash cards:** under the Croatian, each card shows the gender of every noun (masculine / feminine / neuter, plus animate or plural), its case in that sentence (with the preposition that decides it), and which words agree with it. Adjective cards show all three forms (dobar · dobra · dobro · dobri). A ⚠ line appears if a card's Croatian looks wrong. New cards are checked by Claude when you save them; cards that couldn't be checked yet (no key, offline) can be done with **Check now** on the Flash cards tab. You can correct a single noun's gender with the Gender menu after **Show answer**.
