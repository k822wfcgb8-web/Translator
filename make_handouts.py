"""Build handouts.json for Prevoditelj from the Claude outputs vocabulary handouts.
Row: (english, croatian, g)  g: m, ma (masc animate), f, n, mpl, fpl, npl, adj:a|b|c, or '' (other)
"""
import json, re, unicodedata

TS = 1793664000000  # 2026-11-02, fixed so re-running gives the same file
TS_LESSONS = 1793750400000  # 2026-11-04, when the lesson worksheet words were added

H = []  # (id, title, file, rows)

H.append(("family", "Obitelj (family)", "Croatian_Family.pdf", [
    ("family", "obitelj", "f"), ("parents", "roditelji", "mpl"), ("parent", "roditelj", "ma"),
    ("father", "otac", "ma"), ("dad", "tata", "ma"), ("mother", "majka", "f"), ("mum / mom", "mama", "f"),
    ("son", "sin", "ma"), ("sons", "sinovi", "mpl"), ("daughter", "kći", "f"), ("child", "dijete", "n"),
    ("children", "djeca", ""), ("brother", "brat", "ma"), ("brothers", "braća", ""),
    ("sister", "sestra", "f"), ("siblings", "braća i sestre", ""), ("twins", "blizanci", "mpl"),
    ("husband", "muž / suprug", "ma"), ("wife", "žena / supruga", "f"),
    ("grandfather", "djed", "ma"), ("grandmother", "baka", "f"), ("grandson", "unuk", "ma"),
    ("grandchildren", "unuci", "mpl"), ("granddaughter", "unuka", "f"),
    ("great-grandfather", "pradjed", "ma"), ("great-grandmother", "prabaka", "f"),
    ("great-grandson", "praunuk", "ma"), ("great-granddaughter", "praunuka", "f"),
    ("uncle (father's brother)", "stric", "ma"), ("aunt (wife of father's brother)", "strina", "f"),
    ("uncle (mother's brother)", "ujak", "ma"), ("aunt (wife of mother's brother)", "ujna", "f"),
    ("aunt", "tetka / teta", "f"), ("uncle (aunt's husband)", "tetak", "ma"),
    ("cousin (male)", "bratić / rođak", "ma"), ("cousin (female)", "sestrična / rođakinja", "f"),
    ("nephew", "nećak", "ma"), ("niece", "nećakinja", "f"),
    ("father-in-law (husband's father)", "svekar", "ma"), ("father-in-law (wife's father)", "punac", "ma"),
    ("mother-in-law (husband's mother)", "svekrva", "f"), ("mother-in-law (wife's mother)", "punica", "f"),
    ("son-in-law", "zet", "ma"), ("daughter-in-law", "snaha", "f"),
    ("brother-in-law", "šogor", "ma"), ("sister-in-law", "šogorica", "f"),
    ("brother-in-law (husband's brother)", "djever", "ma"), ("brother-in-law (wife's brother)", "šurjak", "ma"),
    ("sister-in-law (husband's sister)", "zaova", "f"), ("sister-in-law (wife's sister)", "svastika", "f"),
    ("stepfather", "očuh", "ma"), ("stepmother", "maćeha", "f"),
    ("stepson", "pastorak", "ma"), ("stepdaughter", "pastorka", "f"),
    ("half-brother", "polubrat", "ma"), ("half-sister", "polusestra", "f"),
    ("godfather / best man", "kum", "ma"), ("godmother / maid of honour", "kuma", "f"),
    ("boyfriend", "dečko", "ma"), ("girlfriend", "djevojka / cura", "f"),
    ("fiancé", "zaručnik", "ma"), ("fiancée", "zaručnica", "f"),
    ("relatives (all of them)", "rodbina", "f"),
    ("widower", "udovac", "ma"), ("widow", "udovica", "f"),
    ("former / ex-", "bivši", "adj:bivši|bivša|bivše"),
    ("married (of a man)", "oženjen", ""), ("married (of a woman)", "udana", ""),
]))

H.append(("groceries", "Namirnice (groceries)", "Croatian_Groceries.pdf", [
    ("fruit", "voće", "n"), ("vegetables", "povrće", "n"), ("spices / condiments", "začini", "mpl"),
    ("apple", "jabuka", "f"), ("pear", "kruška", "f"), ("banana", "banana", "f"), ("orange", "naranča", "f"),
    ("mandarin", "mandarina", "f"), ("lemon", "limun", "m"), ("grapes", "grožđe", "n"),
    ("strawberry", "jagoda", "f"), ("raspberry", "malina", "f"), ("cherry", "trešnja", "f"),
    ("plum", "šljiva", "f"), ("peach", "breskva", "f"), ("apricot", "marelica", "f"), ("fig", "smokva", "f"),
    ("watermelon", "lubenica", "f"), ("melon", "dinja", "f"),
    ("potato", "krumpir", "m"), ("tomato", "rajčica", "f"), ("cucumber", "krastavac", "m"),
    ("onion", "luk", "m"), ("garlic", "češnjak", "m"), ("carrot", "mrkva", "f"),
    ("pepper (vegetable)", "paprika", "f"), ("lettuce", "zelena salata", "f"), ("cabbage", "kupus", "m"),
    ("beans", "grah", "m"), ("peas", "grašak", "m"), ("mushroom", "gljiva", "f"), ("spinach", "špinat", "m"),
    ("corn", "kukuruz", "m"), ("zucchini", "tikvica", "f"), ("eggplant", "patlidžan", "m"),
    ("broccoli", "brokula", "f"),
    ("meat", "meso", "n"), ("chicken (meat)", "piletina", "f"), ("beef", "govedina", "f"),
    ("pork", "svinjetina", "f"), ("lamb", "janjetina", "f"), ("veal", "teletina", "f"),
    ("minced meat", "mljeveno meso", "n"), ("ham", "šunka", "f"), ("sausage", "kobasica", "f"),
    ("bacon", "slanina", "f"), ("fish", "riba", "f"), ("tuna", "tuna", "f"), ("prawns", "kozice", "fpl"),
    ("squid", "lignje", "fpl"),
    ("salt", "sol", "f"), ("pepper (spice)", "papar", "m"), ("oil", "ulje", "n"),
    ("olive oil", "maslinovo ulje", "n"), ("vinegar", "ocat", "m"), ("mustard", "senf", "m"),
    ("ketchup", "kečap", "m"), ("mayonnaise", "majoneza", "f"), ("sauce", "umak", "m"), ("honey", "med", "m"),
    ("jam", "pekmez / džem", "m"), ("pepper relish", "ajvar", "m"), ("parsley", "peršin", "m"),
    ("basil", "bosiljak", "m"),
    ("milk", "mlijeko", "n"), ("cheese", "sir", "m"), ("butter", "maslac", "m"), ("yogurt", "jogurt", "m"),
    ("sour cream", "vrhnje", "n"), ("egg", "jaje", "n"), ("eggs", "jaja", "npl"), ("bread", "kruh", "m"),
    ("bread roll", "pecivo", "n"), ("flour", "brašno", "n"), ("rice", "riža", "f"),
    ("pasta", "tjestenina", "f"), ("sugar", "šećer", "m"), ("coffee", "kava", "f"), ("tea", "čaj", "m"),
    ("water", "voda", "f"), ("juice", "sok", "m"), ("wine", "vino", "n"), ("beer", "pivo", "n"),
    ("kilo / kilogram", "kilogram / kila", ""), ("half a kilo", "pola kile", ""),
    ("100 grams", "deset deka", ""), ("litre / liter", "litra", "f"), ("bottle", "boca", "f"),
    ("piece", "komad", "m"), ("bag", "vrećica", "f"), ("box / carton", "kutija", "f"),
    ("jar", "staklenka", "f"), ("can / tin", "limenka", "f"), ("head (of lettuce, onion)", "glavica", "f"),
]))

H.append(("tools", "Kućni alat (household tools)", "Croatian_Household_Tools.pdf", [
    ("tools", "alat", "m"), ("hammer", "čekić", "m"), ("screwdriver", "odvijač", "m"), ("screw", "vijak", "m"),
    ("nail", "čavao", "m"), ("drill", "bušilica", "f"), ("saw", "pila", "f"), ("pliers", "kliješta", "npl"),
    ("key / wrench", "ključ", "m"), ("adjustable wrench", "francuski ključ", "m"),
    ("tape measure", "metar", "m"), ("glue", "ljepilo", "n"), ("tape", "ljepljiva traka", "f"),
    ("paint / colour", "boja", "f"), ("paintbrush", "kist", "m"), ("rope", "uže", "n"),
    ("scissors", "škare", "fpl"), ("toolbox", "kutija za alat", "f"),
    ("garden", "vrt", "m"), ("ladder", "ljestve", "fpl"), ("shovel", "lopata", "f"), ("rake", "grablje", "fpl"),
    ("axe", "sjekira", "f"), ("hose", "crijevo", "n"), ("watering can", "kanta za zalijevanje", "f"),
    ("gloves", "rukavice", "fpl"),
    ("kitchen", "kuhinja", "f"), ("pot", "lonac", "m"), ("frying pan", "tava", "f"), ("plate", "tanjur", "m"),
    ("bowl", "zdjela", "f"), ("cup", "šalica", "f"), ("glass", "čaša", "f"), ("fork", "vilica", "f"),
    ("spoon", "žlica", "f"), ("teaspoon", "žličica", "f"), ("knife", "nož", "m"),
    ("cutting board", "daska za rezanje", "f"), ("bottle opener", "otvarač", "m"),
    ("fridge", "hladnjak", "m"), ("stove", "štednjak", "m"), ("oven", "pećnica", "f"),
    ("cleaning", "čišćenje", "n"), ("broom", "metla", "f"), ("dustpan", "lopatica", "f"),
    ("vacuum cleaner", "usisavač", "m"), ("cloth / rag", "krpa", "f"), ("sponge", "spužva", "f"),
    ("bucket / bin", "kanta", "f"), ("detergent", "deterdžent", "m"), ("iron (for clothes)", "glačalo", "n"),
    ("washing machine", "perilica rublja", "f"),
    ("light bulb", "žarulja", "f"), ("battery", "baterija", "f"), ("flashlight / torch", "baterijska svjetiljka", "f"),
    ("extension cord", "produžni kabel", "m"), ("socket / outlet", "utičnica", "f"), ("plug", "utikač", "m"),
    ("switch", "prekidač", "m"), ("fuse", "osigurač", "m"), ("lock", "brava", "f"), ("tap / faucet", "slavina", "f"),
    ("to fix / to repair", "popraviti", ""), ("to hammer in", "zabiti", ""), ("to drill", "bušiti", ""),
    ("to cut", "rezati", ""), ("to measure", "mjeriti", ""), ("to paint", "bojiti", ""),
    ("to borrow / to lend", "posuditi", ""), ("to give back / to return", "vratiti", ""),
    ("to clean", "čistiti", ""), ("to wash", "prati", ""), ("to switch on", "uključiti", ""),
    ("to switch off", "isključiti", ""),
]))

H.append(("house", "Kuća i namještaj (house and furniture)", "Croatian_House_and_Furniture.pdf", [
    ("house", "kuća", "f"), ("flat / apartment", "stan", "m"), ("room", "soba", "f"),
    ("living room", "dnevni boravak", "m"), ("kitchen", "kuhinja", "f"), ("dining room", "blagovaonica", "f"),
    ("bedroom", "spavaća soba", "f"), ("children's room", "dječja soba", "f"),
    ("study / home office", "radna soba", "f"), ("bathroom", "kupaonica", "f"), ("toilet (room)", "zahod / WC", "m"),
    ("hallway", "hodnik", "m"), ("entrance hall", "predsoblje", "n"), ("pantry", "ostava", "f"),
    ("laundry room", "praonica rublja", "f"), ("basement / cellar", "podrum", "m"), ("attic", "tavan", "m"),
    ("garage", "garaža", "f"), ("balcony", "balkon", "m"), ("terrace", "terasa", "f"), ("garden", "vrt", "m"),
    ("floor (storey)", "kat", "m"), ("ground floor", "prizemlje", "n"), ("stairs", "stube / stepenice", "fpl"),
    ("floor (surface)", "pod", "m"), ("wall", "zid", "m"), ("ceiling", "strop", "m"), ("roof", "krov", "m"),
    ("window", "prozor", "m"), ("door", "vrata", "npl"), ("lift / elevator", "dizalo", "n"),
    ("kitchen sink", "sudoper", "m"), ("cupboard", "kuhinjski ormarić", "m"),
    ("dishwasher", "perilica posuđa", "f"), ("microwave", "mikrovalna pećnica", "f"),
    ("furniture", "namještaj", "m"), ("table", "stol", "m"), ("chair", "stolica", "f"),
    ("armchair", "fotelja", "f"), ("sofa", "kauč / trosjed", "m"), ("coffee table", "stolić", "m"),
    ("shelf / bookcase", "polica", "f"), ("television", "televizor", "m"), ("rug / carpet", "tepih", "m"),
    ("curtain", "zavjesa", "f"), ("lamp", "svjetiljka / lampa", "f"), ("picture / painting", "slika", "f"),
    ("clock / watch", "sat", "m"), ("radiator", "radijator", "m"), ("air conditioner", "klima-uređaj", "m"),
    ("bed", "krevet", "m"), ("wardrobe", "ormar", "m"), ("chest of drawers", "komoda", "f"),
    ("drawer", "ladica", "f"), ("bedside table", "noćni ormarić", "m"), ("mirror", "ogledalo", "n"),
    ("pillow", "jastuk", "m"), ("blanket", "pokrivač / deka", ""), ("duvet", "poplun", "m"),
    ("sheet", "plahta", "f"), ("washbasin", "umivaonik", "m"), ("bathtub", "kada", "f"), ("shower", "tuš", "m"),
    ("toilet bowl", "zahodska školjka", "f"), ("towel", "ručnik", "m"), ("soap", "sapun", "m"),
    ("toothbrush", "četkica za zube", "f"),
]))

H.append(("questions", "Upitne riječi (question words)", "Croatian_Question_Words-1.pdf", [
    ("who", "tko", ""), ("whom", "koga", ""), ("from whom", "od koga", ""), ("to whom / for whom", "komu / kome", ""),
    ("about whom", "o kome / o komu", ""), ("with whom", "s kim", ""),
    ("whose", "čiji", "adj:čiji|čija|čije"),
    ("what", "što", ""), ("of what / from what", "čega", ""), ("to what / what for", "čemu", ""),
    ("about what", "o čemu", ""), ("with what (tool)", "čime / čim", ""),
    ("which", "koji", "adj:koji|koja|koje"), ("what kind of / what … like", "kakav", "adj:kakav|kakva|kakvo"),
    ("where", "gdje", ""), ("where to", "kamo", ""), ("where from", "odakle / otkud", ""),
    ("which way", "kuda", ""), ("how far / up to where", "dokle", ""),
    ("when", "kada / kad", ""), ("at what time", "u koliko sati", ""), ("what time is it", "koliko je sati", ""),
    ("since when", "otkad / otkada", ""), ("until when", "dokad / dokada", ""),
    ("why", "zašto", ""), ("because of what", "zbog čega", ""), ("what is it for", "čemu služi", ""),
    ("how", "kako", ""), ("how much / how many", "koliko", ""), ("how much does it cost", "koliko košta", ""),
    ("how long", "koliko dugo", ""), ("how often", "koliko često", ""), ("how old", "koliko godina", ""),
    ("is it …? / whether", "je li", ""), ("really? / surely not?", "zar", ""), ("isn't it? / right?", "zar ne", ""),
]))

H.append(("kwords", "K-words anchor phrases", "K_Words_Anchor_Phrases.pdf", [
    ("How are you?", "Kako si?", ""), ("What's your name?", "Kako se zoveš?", ""),
    ("When is the concert?", "Kada je koncert?", ""), ("Where are you going?", "Kamo ideš?", ""),
    ("Which way are we going?", "Kuda idemo?", ""), ("How much does it cost?", "Koliko košta?", ""),
    ("Which is your house?", "Koja je tvoja kuća?", ""), ("What is the weather like?", "Kakvo je vrijeme?", ""),
    ("Whom are you waiting for?", "Koga čekaš?", ""),
]))

H.append(("conj", "Veznici (conjunctions)", "Croatian_Conjunctions.pdf", [
    ("and", "i", ""), ("and (contrast) / while / whereas", "a", ""), ("and so / and then", "pa", ""),
    ("but", "ali", ""), ("but (formal)", "no", ""), ("but rather / than", "nego", ""),
    ("but rather (after a negative)", "već", ""), ("or", "ili", ""), ("nor", "niti", ""),
    ("because", "jer", ""), ("that", "da", ""), ("because", "zato što", ""), ("since (reason)", "budući da", ""),
    ("since / after", "pošto", ""), ("if", "ako", ""), ("unless", "osim ako", ""),
    ("although", "iako / premda / mada", ""), ("even if", "čak i ako", ""), ("even if / at least", "makar", ""),
    ("when", "kada / kad", ""), ("while", "dok", ""), ("until", "dok ne", ""),
    ("before", "prije nego što", ""), ("after", "nakon što", ""), ("since (time)", "otkad / otkada", ""),
    ("as soon as", "čim", ""), ("as long as", "dok god", ""), ("so that / in order to", "kako bi", ""),
    ("so … that", "tako … da", ""), ("as if", "kao da", ""), ("as (the way) / how", "kako", ""),
    ("in case", "u slučaju da", ""), ("whether", "je li", ""),
    ("both … and", "i … i", ""), ("either … or", "ili … ili", ""), ("neither … nor", "ni … ni", ""),
    ("not only … but also", "ne samo … nego i", ""), ("whether … or", "bilo … bilo", ""),
]))

H.append(("short", "Kratke riječi (short words)", "Croatian_Short_Words.pdf", [
    ("in / at / on (a day)", "u", ""), ("on / at", "na", ""), ("at someone's place", "kod", ""),
    ("from (a place)", "iz", ""), ("from (a person) / since", "od", ""), ("to / as far as / until", "do", ""),
    ("toward", "prema", ""), ("across / over / via", "preko", ""), ("through", "kroz", ""),
    ("around / about (approximately)", "oko", ""), ("under", "pod", ""), ("below / underneath", "ispod", ""),
    ("above / over", "iznad", ""), ("in front of", "ispred", ""), ("behind", "iza", ""),
    ("next to / beside", "pokraj / kraj", ""), ("between", "između", ""), ("along / alongside", "uz", ""),
    ("near", "blizu", ""), ("around (all over) / to fetch", "po", ""), ("before / ago", "prije", ""),
    ("after", "poslije", ""), ("after", "nakon", ""), ("during", "tijekom", ""),
    ("for / in (time from now)", "za", ""), ("with", "s / sa", ""), ("without", "bez", ""),
    ("about (a topic)", "o", ""), ("because of", "zbog", ""), ("except / besides", "osim", ""),
    ("instead of", "umjesto", ""), ("against", "protiv", ""),
    ("yes", "da", ""), ("no / not", "ne", ""), ("isn't / is not", "nije", ""), ("not even / nor", "ni", ""),
    ("maybe", "možda", ""), ("of course", "naravno", ""), ("OK / sure", "može", ""), ("good / OK", "dobro", ""),
    ("here", "tu", ""), ("here", "ovdje", ""), ("there", "tamo", ""), ("(to) here", "ovamo", ""),
    ("here is / here you go", "evo", ""), ("home (going home)", "kući", ""), ("at home", "doma", ""),
    ("now", "sada / sad", ""), ("then", "onda", ""), ("then / at that time", "tada", ""),
    ("already", "već", ""), ("still / yet", "još", ""), ("today", "danas", ""), ("tomorrow", "sutra", ""),
    ("yesterday", "jučer", ""), ("always", "uvijek", ""), ("never", "nikada / nikad", ""),
    ("often", "često", ""), ("sometimes", "ponekad", ""), ("again", "opet", ""), ("right away", "odmah", ""),
    ("very", "vrlo", ""), ("very / a lot", "jako", ""), ("a little", "malo", ""), ("a lot", "puno", ""),
    ("much / many", "mnogo", ""), ("too much", "previše", ""), ("enough / quite", "dosta", ""),
    ("only / just", "samo", ""), ("even", "čak", ""), ("almost", "skoro", ""), ("also / too", "također", ""),
    ("also / the same", "isto", ""), ("everyone", "svi", ""), ("everything", "sve", ""),
    ("someone", "netko", ""), ("no one / nobody", "nitko", ""), ("something", "nešto", ""),
    ("nothing", "ništa", ""), ("like / as", "kao", ""), ("please / you're welcome / pardon?", "molim", ""),
    ("thanks / thank you", "hvala", ""), ("come on", "hajde", ""), ("let's go", "hajdemo", ""),
    # Page 5 (added Nov 7, 2026): little grammar words se and li
    ("oneself / each other (goes with some verbs)", "se", ""), ("(question word for yes/no questions)", "li", ""),
    ("is it …? / whether", "je li", ""), ("do you have …?", "imaš li", ""),
    ("my name is …", "zovem se", ""), ("my name isn't …", "ne zovem se", ""), ("What's your name?", "Kako se zoveš?", ""),
    ("see you / see each other", "vidimo se", ""), ("I like it", "sviđa mi se", ""),
    ("How do you say …?", "Kako se kaže …?", ""),
]))


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[.!?,;:…]+$", "", s.strip().lower()))


def slug(s):
    s = unicodedata.normalize("NFKD", s.replace("đ", "d").replace("Đ", "D"))
    return re.sub(r"[^a-z0-9]+", "-", s.encode("ascii", "ignore").decode().lower()).strip("-")[:40]


def gram(g):
    if not g:
        return {"pos": "other", "by": "book", "at": TS}
    if g.startswith("adj:"):
        return {"pos": "adj", "forms": g[4:].split("|"), "by": "book", "at": TS}
    o = {"pos": "noun", "gender": g[0], "by": "book", "at": TS}
    if g == "ma":
        o["animate"] = True
    if g.endswith("pl"):
        o["plural"] = True
    return o


GLABEL = {"m": "masculine", "f": "feminine", "n": "neuter"}

cards, by_hr = [], {}
for hid, title, _f, rows in H:
    for en, hr, g in rows:
        k = norm(hr)
        if k in by_hr:  # same Croatian in several places: one card, both meanings, all handouts
            c = by_hr[k]
            ens = c["en"].split(" / ")
            for e in en.split(" / "):
                if norm(e) not in [norm(x) for x in ens]:
                    ens.append(e)
            c["en"] = " / ".join(ens)
            if hid not in c["ho"]:
                c["ho"].append(hid)
            if c["gram"]["pos"] == "other" and g:
                c["gram"] = gram(g)
            continue
        c = {"id": f"ho-{hid}-{slug(hr)}", "hr": hr, "en": en, "ho": [hid], "gram": gram(g), "_g": g}
        by_hr[k] = c
        cards.append(c)

titles = {h[0]: h[1] for h in H}
out_cards = []
for c in cards:
    g = c.pop("_g")
    kind = ("noun, " + GLABEL[g[0]] + (", plural only" if g.endswith("pl") else "")) if g and not g.startswith("adj") else ("adjective" if g else "")
    note = "Handout: " + " · ".join(titles[h] for h in c["ho"]) + (("\n" + kind) if kind else "")
    out_cards.append({"id": c["id"], "hr": c["hr"], "en": c["en"], "note": note, "ho": c["ho"],
                      "level": 1, "due": 0, "createdAt": TS, "updatedAt": TS, "lastReviewed": 0,
                      "deleted": False, "gram": c["gram"]})

# Book-lesson words from class worksheets (not handouts: no "ho", tagged with a lesson instead).
# Row: (english, croatian, g, acc_sg, acc_pl, example)
LESSONS = [
    ("Tako lako U1 · M1 · Lesson 6: Roditelji", "U pekari", "u1m1l6", [
        ("bread", "kruh", "m", "kruh", "kruhove", "Kupujem ove kruhove."),
        ("pastry / roll", "pecivo", "n", "pecivo", "peciva", "Molim svježa peciva."),
        ("croissant", "kroasan", "m", "kroasan", "kroasane", "Želim čokoladne kroasane."),
        ("doughnut", "krafna", "f", "krafnu", "krafne", "Molim sve ove krafne."),
        ("burek", "burek", "m", "burek", "bureke", "Trebam tople bureke."),
        ("pie / strudel", "pita", "f", "pitu", "pite", "Volim slatke pite."),
        ("crispy pastry", "kroštula", "f", "kroštulu", "kroštule", "Uzmite ove kroštule!"),
        ("sandwich", "sendvič", "m", "sendvič", "sendviče", "Pripremite sendviče."),
        ("yogurt", "jogurt", "m", "jogurt", "jogurte", "Kupujem voćne jogurte."),
        ("coffee", "kava", "f", "kavu", "kave", "Nosite li ove kave?"),
    ]),
]
for tag, sheet, lid, rows in LESSONS:
    for en, hr, g, asg, apl, ex in rows:
        kind = "noun, " + GLABEL[g] + (" (inanimate)" if g == "m" else "")
        note = f"{tag}\nWorksheet: {sheet}\n{kind}\nAcc. sg. {asg} · Acc. pl. {apl}\n{ex}"
        out_cards.append({"id": f"tl-{lid}-{slug(hr)}", "hr": hr, "en": en, "note": note,
                          "level": 1, "due": 0, "createdAt": TS_LESSONS, "updatedAt": TS_LESSONS,
                          "lastReviewed": 0, "deleted": False,
                          "gram": {"pos": "noun", "gender": g, "by": "book", "at": TS_LESSONS}})

# Professions from Lesson 6, Zadatak 1 (Profesija / zanimanje). Row: (english, croatian, g)
# English matches the wording of cards already in the book deck where the word exists.
PROFESSIONS = ("Tako lako U1 · M1 · Lesson 6: Roditelji", "Zadatak 1: Profesija / zanimanje", "u1m1l6", [
    ("professor (man)", "profesor", "ma"), ("professor (woman)", "profesorica", "f"),
    ("actor", "glumac", "ma"), ("actress", "glumica", "f"),
    ("singer (man)", "pjevač", "ma"), ("singer (woman)", "pjevačica", "f"),
    ("artist (man)", "umjetnik", "ma"), ("artist (woman)", "umjetnica", "f"),
    ("programmer (man)", "programer", "ma"), ("programmer (woman)", "programerka", "f"),
    ("manager (man)", "menadžer", "ma"), ("manager (woman)", "menadžerica", "f"),
    ("journalist (man)", "novinar", "ma"), ("journalist (woman)", "novinarka", "f"),
    ("driver (man)", "vozač", "ma"), ("driver (woman)", "vozačica", "f"),
    ("economist (man)", "ekonomist", "ma"), ("economist (woman)", "ekonomistica", "f"),
    ("police officer (man)", "policajac", "ma"), ("police officer (woman)", "policajka", "f"),
    ("politician (man)", "političar", "ma"), ("politician (woman)", "političarka", "f"),
    ("cook / chef (man)", "kuhar", "ma"), ("cook (woman)", "kuharica", "f"),
    ("vendor / salesman", "prodavač", "ma"), ("vendor / saleswoman", "prodavačica", "f"),
    ("lawyer (man)", "odvjetnik", "ma"), ("lawyer (woman)", "odvjetnica", "f"),
    ("musician (man)", "glazbenik", "ma"), ("musician (woman)", "glazbenica", "f"),
    ("firefighter", "vatrogasac", "ma"), ("firefighter (woman)", "žena vatrogasac", ""),
    ("doctor", "liječnik", "ma"), ("female doctor", "liječnica", "f"),
    ("engineer (man)", "inženjer", "ma"), ("engineer (woman)", "inženjerka", "f"),
    ("designer (man)", "dizajner", "ma"), ("designer (woman)", "dizajnerica", "f"),
    ("retiree", "umirovljenik", "ma"), ("retiree (woman)", "umirovljenica", "f"),
    ("boxer (man)", "boksač", "ma"), ("boxer (woman)", "boksačica", "f"),
    ("architect (man)", "arhitekt", "ma"), ("architect (woman)", "arhitektica", "f"),
    ("car mechanic (man)", "automehaničar", "ma"), ("car mechanic (woman)", "automehaničarka", "f"),
    ("hairdresser (man)", "frizer", "ma"), ("hairdresser (woman)", "frizerka", "f"),
])
tag, sheet, lid, rows = PROFESSIONS
for en, hr, g in rows:
    kind = ("noun, " + GLABEL[g[0]] + (", animate" if g == "ma" else "")) if g else "phrase (vatrogasac stays masculine)"
    gr = gram(g); gr["at"] = TS_LESSONS
    out_cards.append({"id": f"tl-{lid}-{slug(hr)}", "hr": hr, "en": en,
                      "note": f"{tag}\nBook: {sheet}\n{kind}",
                      "level": 1, "due": 0, "createdAt": TS_LESSONS, "updatedAt": TS_LESSONS,
                      "lastReviewed": 0, "deleted": False, "gram": gr})

# Adjectives from Lesson 6 (1.1.6 Zadatak 2-4: dialogues and the Laura / Lorena / Ivana profiles).
# Row: (english, croatian, form m|f, example from the lesson)
# English on words already in the book deck matches that card, so only the Lesson 6 tag is added there.
ADJ_L6 = ("Tako lako U1 · M1 · Lesson 6: Roditelji", "1.1.6 Zadaci 2-4", "u1m1l6", [
    ("good", "dobar", "m", "Tata Hrvoje: profesor, dobar, drag."),
    ("good (feminine)", "dobra", "f", "Jako je dobra i draga."),
    ("dear / kind (masculine)", "drag", "m", "On je simpatičan i drag."),
    ("dear / kind (feminine)", "draga", "f", "Jako je vrijedna, dobra i draga."),
    ("hard-working (masculine)", "vrijedan", "m", "Jako je vrijedan i dobar."),
    ("hard-working (feminine)", "vrijedna", "f", "Mama Ljubica: ekonomistica, vrijedna."),
    ("strict", "strog", "m", "On je vrijedan i strog."),
    ("strict (feminine)", "stroga", "f", "Moja profesorica je stroga."),
    ("likeable", "simpatičan", "m", "On je simpatičan i drag."),
    ("likeable / nice (feminine)", "simpatična", "f", "Moja prijateljica je simpatična."),
    ("tall", "visok", "m", "Tata John: Amerikanac, visok, odvjetnik."),
    ("tall (feminine)", "visoka", "f", "Prijateljica Silvija: studentica, dobra, visoka."),
    ("funny (masculine)", "smiješan", "m", "Moj brat je smiješan."),
    ("funny (feminine)", "smiješna", "f", "Prijateljica Suzana: studentica, smiješna, vrijedna."),
    ("serious", "ozbiljan", "m", "Moj tata je ozbiljan."),
    ("serious (feminine)", "ozbiljna", "f", "Mama Josipa: odvjetnica, vrijedna, ozbiljna."),
    ("beautiful / nice (masculine)", "lijep", "m", "Tamara je baš lijepo ime."),
    ("beautiful / nice (feminine)", "lijepa", "f", "Sestra je lijepa."),
    ("interesting (masculine)", "zanimljiv", "m", "Baš zanimljivo."),
    ("interesting (feminine)", "zanimljiva", "f", "Moja mama je zanimljiva."),
])
ADJ_FORMS = {"dobar": ["dobar", "dobra", "dobro"], "drag": ["drag", "draga", "drago"],
             "vrijedan": ["vrijedan", "vrijedna", "vrijedno"], "strog": ["strog", "stroga", "strogo"],
             "simpatičan": ["simpatičan", "simpatična", "simpatično"], "visok": ["visok", "visoka", "visoko"],
             "smiješan": ["smiješan", "smiješna", "smiješno"], "ozbiljan": ["ozbiljan", "ozbiljna", "ozbiljno"],
             "lijep": ["lijep", "lijepa", "lijepo"], "zanimljiv": ["zanimljiv", "zanimljiva", "zanimljivo"]}
tag, sheet, lid, rows = ADJ_L6
for en, hr, form, ex in rows:
    forms = next(v for v in ADJ_FORMS.values() if hr in v)
    gr = {"pos": "adj", "forms": forms, "def": forms[0] if forms[0].endswith("i") else (forms[1][:-1] + "i"),
          "form": form, "by": "book", "at": TS_LESSONS}
    note = f"{tag}\nBook: {sheet}\nadjective, {GLABEL[form]} (m {forms[0]} · f {forms[1]} · n {forms[2]})\n{ex}"
    out_cards.append({"id": f"tl-{lid}-adj-{slug(hr)}", "hr": hr, "en": en, "note": note,
                      "level": 1, "due": 0, "createdAt": TS_LESSONS, "updatedAt": TS_LESSONS,
                      "lastReviewed": 0, "deleted": False, "gram": gr})

# Learning-objective words from the Veterans Day worksheet "Domovinski rat i glazba: Lupi petama"
# (Prljavo Kazalište), filed under U1 · M2 · Lesson 1. Examples are simple sentences, not song lyrics.
# Row: (english, croatian, g, kind, forms, example)   g as in gram(); kind/forms go in the note.
TS_L7 = 1794441600000  # 2026-11-11
WAR_SONG = ("Tako lako U1 · M2 · Lesson 1: Ljudi i stvari", "Domovinski rat i glazba: Lupi petama", "u1m2l1", [
    ("war", "rat", "m", "noun, masculine (inanimate)", "Acc. sg. rat · Acc. pl. ratove", "Rat je završio."),
    ("friends", "prijatelji", "mpl", "noun, masculine plural (animate)", "Sg. prijatelj · Acc. pl. prijatelje", "Moji prijatelji su ovdje."),
    ("to hug / to embrace", "zagrliti", "", "verb, perfective (ja zagrlim)", "Imperfective: grliti", "Želim te zagrliti."),
    ("flag", "zastava", "f", "noun, feminine", "Acc. sg. zastavu · Acc. pl. zastave", "Hrvatska zastava je crvena, bijela i plava."),
    ("tear (crying)", "suza", "f", "noun, feminine", "Acc. sg. suzu · Acc. pl. suze", "Imam suzu u oku."),
    ("dove / pigeon", "golub", "ma", "noun, masculine, animate", "Acc. sg. goluba · Acc. pl. golubove", "Golub je bijel."),
    ("sky", "nebo", "n", "noun, neuter", "Acc. sg. nebo · Pl. nebesa", "Nebo je plavo."),
    ("night", "noć", "f", "noun, feminine (ends in a consonant)", "Acc. sg. noć · Acc. pl. noći", "Laku noć!"),
    ("Sunday", "nedjelja", "f", "noun, feminine", "Acc. sg. nedjelju · on Sundays: nedjeljom", "U nedjelju gledam utakmicu."),
])
tag, sheet, lid, rows = WAR_SONG
for en, hr, g, kind, forms, ex in rows:
    gr = gram(g); gr["at"] = TS_L7
    out_cards.append({"id": f"tl-{lid}-{slug(hr)}", "hr": hr, "en": en,
                      "note": f"{tag}\nWorksheet: {sheet}\n{kind}\n{forms}\n{ex}",
                      "level": 1, "due": 0, "createdAt": TS_L7, "updatedAt": TS_L7,
                      "lastReviewed": 0, "deleted": False, "gram": gr})

# Beginner gap-fill (2026-11-11): lessons that had no cards. Unit 1 Module 0 and the two empty Unit 2 lessons.
# The book's pages for these are images or don't load, so the lists are standard beginner vocabulary chosen by Claude.
# English on words already in the deck matches that card, so those only get the lesson tag.
# Row: (english, croatian, g, extra note line)   g as in gram()
BEGINNER = [
    ("U1 · M0 · Lesson 1: Brojevi 1–21", "u1m0l1", [
        ("zero (0)", "nula", "f", "number"),
        ("one (1)", "jedan", "adj:jedan|jedna|jedno", "number; agrees like an adjective: jedan sat, jedna kava, jedno pivo"),
        ("two (2)", "dva", "", "number; dva for masculine/neuter, dvije for feminine (dvije kave)"),
        ("two (2, feminine)", "dvije", "", "number; with feminine nouns: dvije sestre"),
        ("three (3)", "tri", "", "number"), ("four (4)", "četiri", "", "number"),
        ("five (5)", "pet", "", "number; from 5 on, the noun goes in genitive plural: pet kava"),
        ("six (6)", "šest", "", "number"), ("seven (7)", "sedam", "", "number"), ("eight (8)", "osam", "", "number"),
        ("nine (9)", "devet", "", "number"), ("ten (10)", "deset", "", "number"),
        ("eleven (11)", "jedanaest", "", "number"), ("twelve (12)", "dvanaest", "", "number"),
        ("thirteen (13)", "trinaest", "", "number"), ("fourteen (14)", "četrnaest", "", "number"),
        ("fifteen (15)", "petnaest", "", "number"), ("sixteen (16)", "šesnaest", "", "number"),
        ("seventeen (17)", "sedamnaest", "", "number"), ("eighteen (18)", "osamnaest", "", "number"),
        ("nineteen (19)", "devetnaest", "", "number"), ("twenty (20)", "dvadeset", "", "number"),
        ("twenty-one (21)", "dvadeset jedan", "", "number; written as two words"),
        ("How many? / How much?", "Koliko?", "", "question word"),
    ]),
    ("U1 · M0 · Lesson 2: Dani u tjednu", "u1m0l2", [
        ("Monday", "ponedjeljak", "m", "day; on Monday = u ponedjeljak"), ("Tuesday", "utorak", "m", "day"),
        ("Wednesday", "srijeda", "f", "day; on Wednesday = u srijedu"), ("Thursday", "četvrtak", "m", "day"),
        ("Friday", "petak", "m", "day"), ("Saturday", "subota", "f", "day; on Saturday = u subotu"),
        ("Sunday", "nedjelja", "f", "day; on Sundays = nedjeljom"),
        ("day", "dan", "m", ""), ("week", "tjedan", "m", ""), ("weekend", "vikend", "m", ""),
        ("today", "danas", "", ""), ("tomorrow", "sutra", "", ""), ("yesterday", "jučer", "", ""),
        ("What day is it today?", "Koji je danas dan?", "", "phrase"),
        ("Today is Monday.", "Danas je ponedjeljak.", "", "phrase"),
        ("on Monday", "u ponedjeljak", "", "u + accusative for days"),
    ]),
    ("U1 · M0 · Lesson 3: Mjeseci", "u1m0l3", [
        ("January", "siječanj", "m", "month; in January = u siječnju"), ("February", "veljača", "f", "month"),
        ("March", "ožujak", "m", "month"), ("April", "travanj", "m", "month"), ("May", "svibanj", "m", "month"),
        ("June", "lipanj", "m", "month"), ("July", "srpanj", "m", "month"), ("August", "kolovoz", "m", "month"),
        ("September", "rujan", "m", "month"), ("October", "listopad", "m", "month"),
        ("November", "studeni", "m", "month; adjective-like form"), ("December", "prosinac", "m", "month"),
        ("month", "mjesec", "m", "also means moon"), ("year", "godina", "f", ""),
        ("in January", "u siječnju", "", "u + locative for months"),
    ]),
    ("U1 · M0 · Lesson 4: Jedinice vremena", "u1m0l4", [
        ("second", "sekunda", "f", ""), ("minute", "minuta", "f", ""),
        ("hour", "sat", "m", "sat = hour and also clock / watch"), ("day", "dan", "m", ""),
        ("week", "tjedan", "m", ""), ("month", "mjesec", "m", ""), ("year", "godina", "f", ""),
        ("decade", "desetljeće", "n", ""), ("century", "stoljeće", "n", ""),
        ("morning", "jutro", "n", ""), ("noon", "podne", "n", ""), ("afternoon", "popodne", "n", ""),
        ("evening", "večer", "f", ""), ("night", "noć", "f", ""), ("midnight", "ponoć", "f", ""),
        ("what time is it", "koliko je sati", "", "phrase"), ("half an hour", "pola sata", "", "phrase"),
    ]),
    ("U1 · M0 · Lesson 5: Boje", "u1m0l5", [
        ("color", "boja", "f", ""), ("What color is it?", "Koje je boje?", "", "phrase"),
        ("red (masculine)", "crven", "adj:crven|crvena|crveno", "adjective"), ("red", "crvena", "adj:crven|crvena|crveno", "adjective, feminine"),
        ("blue (masculine)", "plav", "adj:plav|plava|plavo", "adjective"), ("blue", "plava", "adj:plav|plava|plavo", "adjective, feminine"),
        ("green (masculine)", "zelen", "adj:zelen|zelena|zeleno", "adjective"), ("green", "zelena", "adj:zelen|zelena|zeleno", "adjective, feminine"),
        ("yellow", "žut", "adj:žut|žuta|žuto", "adjective"), ("yellow", "žuta", "adj:žut|žuta|žuto", "adjective, feminine"),
        ("black (masculine)", "crn", "adj:crn|crna|crno", "adjective"), ("black", "crna", "adj:crn|crna|crno", "adjective, feminine"),
        ("white (masculine)", "bijel", "adj:bijel|bijela|bijelo", "adjective"), ("white", "bijela", "adj:bijel|bijela|bijelo", "adjective, feminine"),
        ("brown (masculine)", "smeđ", "adj:smeđ|smeđa|smeđe", "adjective"), ("brown", "smeđa", "adj:smeđ|smeđa|smeđe", "adjective, feminine"),
        ("grey (masculine)", "siv", "adj:siv|siva|sivo", "adjective"), ("grey (feminine)", "siva", "adj:siv|siva|sivo", "adjective, feminine"),
        ("orange (masculine)", "narančast", "adj:narančast|narančasta|narančasto", "adjective"), ("orange", "narančasta", "adj:narančast|narančasta|narančasto", "adjective, feminine"),
        ("purple (masculine)", "ljubičast", "adj:ljubičast|ljubičasta|ljubičasto", "adjective"), ("purple", "ljubičasta", "adj:ljubičast|ljubičasta|ljubičasto", "adjective, feminine"),
        ("pink (masculine)", "ružičast", "adj:ružičast|ružičasta|ružičasto", "adjective"), ("pink (feminine)", "ružičasta", "adj:ružičast|ružičasta|ružičasto", "adjective, feminine"),
    ]),
    ("U2 · M1 · Lesson 1: Odakle si?", "u2m1l1", [
        ("continent", "kontinent", "m", ""), ("Europe", "Europa", "f", "from Europe = iz Europe"),
        ("Asia", "Azija", "f", ""), ("Africa", "Afrika", "f", ""),
        ("North America", "Sjeverna Amerika", "f", ""), ("South America", "Južna Amerika", "f", ""),
        ("Australia", "Australija", "f", ""), ("Antarctica", "Antarktika", "f", ""),
        ("Croatia", "Hrvatska", "f", "from Croatia = iz Hrvatske"), ("America / USA", "Amerika", "f", "from America = iz Amerike"),
        ("Germany", "Njemačka", "f", ""), ("Italy", "Italija", "f", ""), ("France", "Francuska", "f", ""),
        ("England", "Engleska", "f", ""), ("Canada", "Kanada", "f", ""), ("Mexico", "Meksiko", "m", ""),
        ("Where are you from? (formal / plural)", "Odakle ste?", "", "phrase"),
        ("I am from America.", "Ja sam iz Amerike.", "", "iz + genitive"),
        ("My parents are from Zagreb.", "Moji roditelji su iz Zagreba.", "", "iz + genitive"),
        ("for example", "na primjer", "", "phrase"),
    ]),
    ("U2 · M3 · Lesson 4: Moji interesi", "u2m3l4", [
        ("fortress", "tvrđava", "f", ""), ("waterfalls", "slapovi", "mpl", "sg. slap"),
        ("cathedral", "katedrala", "f", ""), ("beach", "plaža", "f", ""), ("sea", "more", "n", ""),
        ("lake", "jezero", "n", ""), ("river", "rijeka", "f", ""), ("forest", "šuma", "f", ""),
        ("museum", "muzej", "m", ""), ("trip / excursion", "izlet", "m", ""), ("to swim", "plivati", "", "verb"),
        ("Enjoy! (to a group)", "Uživajte!", "", "phrase; to one person: Uživaj!"),
        ("greeting / regards", "pozdrav", "m", "Pozdrav iz Splita = Greetings from Split"),
        ("It's a pity.", "Šteta je.", "", "phrase"), ("True. / That's right.", "Istina.", "", "phrase"),
        ("Can we go together?", "Možemo zajedno?", "", "phrase"), ("Do you have plans?", "Imaš li plan?", "", "phrase"),
    ]),
]
for tag, lid, rows in BEGINNER:
    for en, hr, g, extra in rows:
        gr = gram(g); gr["at"] = TS_L7
        note = f"Tako lako {tag}\nBeginner list (Claude)" + (f"\n{extra}" if extra else "")
        out_cards.append({"id": f"tl-{lid}-{slug(hr)}", "hr": hr, "en": en, "note": note,
                          "level": 1, "due": 0, "createdAt": TS_L7, "updatedAt": TS_L7,
                          "lastReviewed": 0, "deleted": False, "gram": gr})

ids = [c["id"] for c in out_cards]
assert len(ids) == len(set(ids)), "duplicate ids"
data = {"app": "prevoditelj", "kind": "handouts", "version": 1, "savedAt": TS,
        "source": "Claude-made reference handouts in Taka Lako Class/Claude outputs",
        "handouts": [{"id": h[0], "title": h[1], "file": h[2]} for h in H],
        "cards": out_cards}
json.dump(data, open("handouts.json", "w"), ensure_ascii=False, indent=1)
for h in H:
    print(h[0], sum(h[0] in c.get("ho", []) for c in out_cards))
print("lesson cards", sum("ho" not in c for c in out_cards))
print("total cards", len(out_cards))
print([ (c["hr"], c["en"]) for c in out_cards if len(c.get("ho", [])) > 1])
