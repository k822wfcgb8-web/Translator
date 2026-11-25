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

H.append(("short", "Kratke riječi (short words)", "W00_U0_Kratke-rijeci_ref.pdf", [
    # Prepositions moved to their own handout (Prijedlozi) on Nov 17, 2026.
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


# Prijedlozi (added Nov 17, 2026): the prepositions sheet W00_U0_Prijedlozi_ref.pdf.
# Prepositions first (their case is in PREP_NOTE, shown under the card), then short phrases that practise the case endings.
G, D, A, L, I = "genitive", "dative", "accusative", "locative", "instrumental"
PREPS = [  # (english, croatian, case note)
    ("in / at / on (a day)", "u", f"preposition + {L} (where) or {A} (where to; on a day)"),
    ("on / at", "na", f"preposition + {L} (where) or {A} (where to)"),
    ("at someone's place", "kod", f"preposition + {G}"),
    ("from (a place) / out of", "iz", f"preposition + {G}"),
    ("from (a person) / since", "od", f"preposition + {G}"),
    ("to / as far as / until", "do", f"preposition + {G}"),
    ("toward", "prema", f"preposition + {D}"),
    ("to (a person's place)", "k / ka", f"preposition + {D}; ka before k and g"),
    ("across / over / via", "preko", f"preposition + {G}"),
    ("through", "kroz", f"preposition + {A}"),
    ("down", "niz", f"preposition + {A}"),
    ("around / about (approximately)", "oko", f"preposition + {G}"),
    ("under", "pod", f"preposition + {I} (where) or {A} (where to)"),
    ("below / underneath", "ispod", f"preposition + {G}"),
    ("above / over", "iznad", f"preposition + {G}"),
    ("in front of", "ispred", f"preposition + {G}"),
    ("behind", "iza", f"preposition + {G}"),
    ("next to / beside", "pokraj / kraj", f"preposition + {G}"),
    ("between", "između", f"preposition + {G}"),
    ("along / alongside", "uz", f"preposition + {A}"),
    ("near", "blizu", f"preposition + {G}"),
    ("around (all over) / to fetch", "po", f"preposition + {L} (all over) or {A} (to fetch)"),
    ("before / ago", "prije", f"preposition + {G}"),
    ("after", "poslije", f"preposition + {G}"),
    ("after", "nakon", f"preposition + {G}"),
    ("during", "tijekom", f"preposition + {G}"),
    ("for / in (time from now)", "za", f"preposition + {A} (for; in + time) or {I} (behind, at)"),
    ("with / off (a surface)", "s / sa", f"preposition + {I} (with) or {G} (off, from); sa before s, z, š, ž and mnom"),
    ("without", "bez", f"preposition + {G}"),
    ("about (a topic)", "o", f"preposition + {L}"),
    ("because of", "zbog", f"preposition + {G}"),
    ("except / besides", "osim", f"preposition + {G}"),
    ("instead of", "umjesto", f"preposition + {G}"),
    ("against", "protiv", f"preposition + {G}"),
]
PREP_PHRASES = [  # (english, croatian, case note)
    ("in town / in the city", "u gradu", f"u + {L}: where"),
    ("into town / to town", "u grad", f"u + {A}: where to"),
    ("from town", "iz grada", f"iz + {G}: where from"),
    ("at the seaside", "na moru", f"na + {L}: where"),
    ("to the seaside", "na more", f"na + {A}: where to"),
    ("from the seaside", "s mora", f"s + {G}: where from"),
    ("at work", "na poslu", f"na + {L}: where"),
    ("from work", "s posla", f"s + {G}: where from"),
    ("at Grandma's", "kod bake", f"kod + {G}: where"),
    ("to Grandma's", "k baki", f"k + {D}: where to"),
    ("from Grandma", "od bake", f"od + {G}: where from"),
    ("under the table", "pod stolom", f"pod + {I}: where"),
    ("from America", "iz Amerike", f"iz + {G}"),
    ("with Mom", "s mamom", f"s + {I}"),
    ("coffee with milk", "kava s mlijekom", f"s + {I}"),
    ("without sugar", "bez šećera", f"bez + {G}"),
    ("for you (informal)", "za tebe", f"za + {A}"),
    ("about the family", "o obitelji", f"o + {L}"),
    ("after work", "poslije posla", f"poslije + {G}"),
    ("before lunch", "prije ručka", f"prije + {G}"),
    ("two days ago", "prije dva dana", f"prije + {G}"),
    ("in a week", "za tjedan dana", f"za + {A}: in + time"),
    ("from nine to five", "od devet do pet", f"od … do + {G}"),
    ("because of the rain", "zbog kiše", f"zbog + {G}"),
    ("at my place", "kod mene", f"kod + {G}"),
    ("at your place (informal)", "kod tebe", f"kod + {G}"),
    ("with me", "sa mnom", f"s + {I}; sa before mnom"),
    ("with you (informal)", "s tobom", f"s + {I}"),
    ("for me", "za mene", f"za + {A}"),
    ("about me", "o meni", f"o + {L}"),
]
# These were on the Kratke riječi handout until Nov 17, 2026; their cards keep the old ho-short-… ids.
LEGACY_SHORT = {"u", "na", "kod", "iz", "od", "do", "prema", "preko", "kroz", "oko", "ispod", "iznad", "ispred", "iza",
                "pokraj / kraj", "između", "uz", "blizu", "po", "prije", "poslije", "nakon", "tijekom", "za", "s / sa",
                "bez", "o", "zbog", "osim", "umjesto", "protiv"}
PREP_NOTE = {hr: note for _e, hr, note in PREPS + PREP_PHRASES}
prep_rows = [(e, hr, "") for e, hr, _n in PREPS + PREP_PHRASES]
H.append(("prep", "Prijedlozi (prepositions)", "W00_U0_Prijedlozi_ref.pdf", prep_rows))


# Pridjevi (added Nov 17, 2026): the adjectives sheet W00_U0_Pridjevi_ref.pdf, masculine form with all three forms.
# Most are already book cards and just count in this handout; sladak, kiseo, svjež, vruć and hladan are new.
ADJ_ROWS = [  # (english, masculine, adj:m|f|n), same words and order as W00_U0_Pridjevi_ref.pdf
    ('active', 'aktivan', "adj:aktivan|aktivna|aktivno"),
    ('ambitious', 'ambiciozan', "adj:ambiciozan|ambiciozna|ambiciozno"),
    ('approachable', 'pristupačan', "adj:pristupačan|pristupačna|pristupačno"),
    ('arrogant', 'arogantan', "adj:arogantan|arogantna|arogantno"),
    ('cheerful', 'veseo', "adj:veseo|vesela|veselo"),
    ('communicative', 'komunikativan', "adj:komunikativan|komunikativna|komunikativno"),
    ('compassionate', 'suosjećajan', "adj:suosjećajan|suosjećajna|suosjećajno"),
    ('creative', 'kreativan', "adj:kreativan|kreativna|kreativno"),
    ('dear / kind', 'drag', "adj:drag|draga|drago"),
    ('decisive', 'odlučan', "adj:odlučan|odlučna|odlučno"),
    ('dominant', 'dominantan', "adj:dominantan|dominantna|dominantno"),
    ('dynamic', 'dinamičan', "adj:dinamičan|dinamična|dinamično"),
    ('emotional', 'emotivan', "adj:emotivan|emotivna|emotivno"),
    ('energetic', 'energičan', "adj:energičan|energična|energično"),
    ('fun', 'zabavan', "adj:zabavan|zabavna|zabavno"),
    ('funny', 'smiješan', "adj:smiješan|smiješna|smiješno"),
    ('hard-working', 'marljiv', "adj:marljiv|marljiva|marljivo"),
    ('hard-working / diligent', 'vrijedan', "adj:vrijedan|vrijedna|vrijedno"),
    ('hysterical', 'histeričan', "adj:histeričan|histerična|histerično"),
    ('independent', 'samostalan', "adj:samostalan|samostalna|samostalno"),
    ('intelligent', 'inteligentan', "adj:inteligentan|inteligentna|inteligentno"),
    ('irresponsible', 'neodgovoran', "adj:neodgovoran|neodgovorna|neodgovorno"),
    ('irritating', 'iritantan', "adj:iritantan|iritantna|iritantno"),
    ('jealous', 'ljubomoran', "adj:ljubomoran|ljubomorna|ljubomorno"),
    ('kind / friendly', 'ljubazan', "adj:ljubazan|ljubazna|ljubazno"),
    ('likeable / nice', 'simpatičan', "adj:simpatičan|simpatična|simpatično"),
    ('loud', 'glasan', "adj:glasan|glasna|glasno"),
    ('optimistic', 'optimističan', "adj:optimističan|optimistična|optimistično"),
    ('organized', 'organiziran', "adj:organiziran|organizirana|organizirano"),
    ('patient', 'strpljiv', "adj:strpljiv|strpljiva|strpljivo"),
    ('polite', 'pristojan', "adj:pristojan|pristojna|pristojno"),
    ('possessive', 'posesivan', "adj:posesivan|posesivna|posesivno"),
    ('productive', 'produktivan', "adj:produktivan|produktivna|produktivno"),
    ('quiet', 'tih', "adj:tih|tiha|tiho"),
    ('refined', 'profinjen', "adj:profinjen|profinjena|profinjeno"),
    ('responsible', 'odgovoran', "adj:odgovoran|odgovorna|odgovorno"),
    ('romantic', 'romantičan', "adj:romantičan|romantična|romantično"),
    ('rude', 'bezobrazan', "adj:bezobrazan|bezobrazna|bezobrazno"),
    ('self-confident', 'samopouzdan', "adj:samopouzdan|samopouzdana|samopouzdano"),
    ('selfish', 'sebičan', "adj:sebičan|sebična|sebično"),
    ('serious', 'ozbiljan', "adj:ozbiljan|ozbiljna|ozbiljno"),
    ('smart', 'pametan', "adj:pametan|pametna|pametno"),
    ('sociable', 'druželjubiv', "adj:druželjubiv|druželjubiva|druželjubivo"),
    ('strict', 'strog', "adj:strog|stroga|strogo"),
    ('stupid', 'glup', "adj:glup|glupa|glupo"),
    ('witty / funny', 'duhovit', "adj:duhovit|duhovita|duhovito"),
    ('bald', 'ćelav', "adj:ćelav|ćelava|ćelavo"),
    ('beautiful / nice', 'lijep', "adj:lijep|lijepa|lijepo"),
    ('curly', 'kovrčav', "adj:kovrčav|kovrčava|kovrčavo"),
    ('good-looking', 'zgodan', "adj:zgodan|zgodna|zgodno"),
    ('old', 'star', "adj:star|stara|staro"),
    ('short (height) / low', 'nizak', "adj:nizak|niska|nisko"),
    ('slim / thin', 'mršav', "adj:mršav|mršava|mršavo"),
    ('tall / high', 'visok', "adj:visok|visoka|visoko"),
    ('ugly', 'ružan', "adj:ružan|ružna|ružno"),
    ('busy / hectic', 'užurban', "adj:užurban|užurbana|užurbano"),
    ('busy / taken', 'zauzet', "adj:zauzet|zauzeta|zauzeto"),
    ('dressed', 'odjeven', "adj:odjeven|odjevena|odjeveno"),
    ('free', 'slobodan', "adj:slobodan|slobodna|slobodno"),
    ('healthy', 'zdrav', "adj:zdrav|zdrava|zdravo"),
    ('hungry', 'gladan', "adj:gladan|gladna|gladno"),
    ('ill / sick', 'bolestan', "adj:bolestan|bolesna|bolesno"),
    ('invited', 'pozvan', "adj:pozvan|pozvana|pozvano"),
    ('ready', 'spreman', "adj:spreman|spremna|spremno"),
    ('relaxed', 'opušten', "adj:opušten|opuštena|opušteno"),
    ('strong', 'jak', "adj:jak|jaka|jako"),
    ('sure / safe', 'siguran', "adj:siguran|sigurna|sigurno"),
    ('tired', 'umoran', "adj:umoran|umorna|umorno"),
    ('big / large', 'velik', "adj:velik|velika|veliko"),
    ('empty', 'prazan', "adj:prazan|prazna|prazno"),
    ('heavy / difficult', 'težak', "adj:težak|teška|teško"),
    ('light / easy', 'lagan', "adj:lagan|lagana|lagano"),
    ('short', 'kratak', "adj:kratak|kratka|kratko"),
    ('small / little (also malen)', 'mali', "adj:mali|mala|malo"),
    ('wide / broad', 'širok', "adj:širok|široka|široko"),
    ('appropriate', 'prikladan', "adj:prikladan|prikladna|prikladno"),
    ('attractive', 'atraktivan', "adj:atraktivan|atraktivna|atraktivno"),
    ('bad', 'loš', "adj:loš|loša|loše"),
    ('boring', 'dosadan', "adj:dosadan|dosadna|dosadno"),
    ('different', 'drugačiji', "adj:drugačiji|drugačija|drugačije"),
    ('easy', 'lak', "adj:lak|laka|lako"),
    ('excellent', 'odličan', "adj:odličan|odlična|odlično"),
    ('favourite', 'omiljen', "adj:omiljen|omiljena|omiljeno"),
    ('forbidden', 'zabranjen', "adj:zabranjen|zabranjena|zabranjeno"),
    ('good', 'dobar', "adj:dobar|dobra|dobro"),
    ('gorgeous / wonderful', 'predivan', "adj:predivan|predivna|predivno"),
    ('high-quality', 'kvalitetan', "adj:kvalitetan|kvalitetna|kvalitetno"),
    ('interesting', 'interesantan', "adj:interesantan|interesantna|interesantno"),
    ('interesting', 'zanimljiv', "adj:zanimljiv|zanimljiva|zanimljivo"),
    ('necessary', 'potreban', "adj:potreban|potrebna|potrebno"),
    ('popular', 'popularan', "adj:popularan|popularna|popularno"),
    ('similar', 'sličan', "adj:sličan|slična|slično"),
    ('well-known / famous', 'poznat', "adj:poznat|poznata|poznato"),
    ('bright / light', 'svijetao', "adj:svijetao|svijetla|svijetlo"),
    ('built', 'izgrađen', "adj:izgrađen|izgrađena|izgrađeno"),
    ('clean', 'čist', "adj:čist|čista|čisto"),
    ('colourful', 'šaren', "adj:šaren|šarena|šareno"),
    ('comfortable', 'udoban', "adj:udoban|udobna|udobno"),
    ('distant / far away', 'udaljen', "adj:udaljen|udaljena|udaljeno"),
    ('former / ex-', 'bivši', "adj:bivši|bivša|bivše"),
    ('founded', 'osnovan', "adj:osnovan|osnovana|osnovano"),
    ('furnished', 'namješten', "adj:namješten|namještena|namješteno"),
    ('messy / untidy', 'neuredan', "adj:neuredan|neuredna|neuredno"),
    ('modern', 'moderan', "adj:moderan|moderna|moderno"),
    ('neat / tidy', 'uredan', "adj:uredan|uredna|uredno"),
    ('new', 'nov', "adj:nov|nova|novo"),
    ('next', 'sljedeći', "adj:sljedeći|sljedeća|sljedeće"),
    ('old-fashioned', 'staromodan', "adj:staromodan|staromodna|staromodno"),
    ('open / outdoor', 'otvoren', "adj:otvoren|otvorena|otvoreno"),
    ('planned / scheduled', 'predviđen', "adj:predviđen|predviđena|predviđeno"),
    ('private', 'privatan', "adj:privatan|privatna|privatno"),
    ('rich', 'bogat', "adj:bogat|bogata|bogato"),
    ('traditional', 'tradicionalan', "adj:tradicionalan|tradicionalna|tradicionalno"),
    ('unfurnished', 'nenamješten', "adj:nenamješten|nenamještena|nenamješteno"),
    ('unhealthy', 'nezdrav', "adj:nezdrav|nezdrava|nezdravo"),
    ('warm', 'topao', "adj:topao|topla|toplo"),
    ('well-kept / decorated', 'uređen', "adj:uređen|uređena|uređeno"),
    ('affordable / good value', 'povoljan', "adj:povoljan|povoljna|povoljno"),
    ('cheap', 'jeftin', "adj:jeftin|jeftina|jeftino"),
    ('expensive', 'skup', "adj:skup|skupa|skupo"),
    ('reliable', 'pouzdan', "adj:pouzdan|pouzdana|pouzdano"),
    ('slow', 'spor', "adj:spor|spora|sporo"),
    ('cold', 'hladan', "adj:hladan|hladna|hladno"),
    ('fresh', 'svjež', "adj:svjež|svježa|svježe"),
    ('hot', 'vruć', "adj:vruć|vruća|vruće"),
    ('sour', 'kiseo', "adj:kiseo|kisela|kiselo"),
    ('sweet', 'sladak', "adj:sladak|slatka|slatko"),
    ('black', 'crn', "adj:crn|crna|crno"),
    ('blue / blond', 'plav', "adj:plav|plava|plavo"),
    ('brown', 'smeđ', "adj:smeđ|smeđa|smeđe"),
    ('green', 'zelen', "adj:zelen|zelena|zeleno"),
    ('grey', 'siv', "adj:siv|siva|sivo"),
    ('orange', 'narančast', "adj:narančast|narančasta|narančasto"),
    ('pink', 'ružičast', "adj:ružičast|ružičasta|ružičasto"),
    ('purple', 'ljubičast', "adj:ljubičast|ljubičasta|ljubičasto"),
    ('red', 'crven', "adj:crven|crvena|crveno"),
    ('white', 'bijel', "adj:bijel|bijela|bijelo"),
    ('yellow', 'žut', "adj:žut|žuta|žuto"),
]
H.append(("adj", "Pridjevi (adjectives)", "W00_U0_Pridjevi_ref.pdf", ADJ_ROWS))


# Vrijeme (added Nov 21, 2026): the time study guide W00_U0_Vrijeme_study.pdf (units of time, yesterday/today/tomorrow,
# parts of the day, telling the time, days, months, seasons, how often, everyday time phrases). Words already in the
# deck (book lessons U1 · M0, short words, prepositions, question words) just count in this handout.
# Row: (english, croatian, g, note line)
VR = [
 # 1 Units of time
 ("second", "sekunda", "f", "2 sekunde · 5 sekundi"),
 ("minute", "minuta", "f", "2 minute · 5 minuta"),
 ("hour", "sat", "m", "2 sata · 5 sati; sat = hour and also clock / watch"),
 ("day", "dan", "m", "2 dana · 5 dana"),
 ("week", "tjedan", "m", "2 tjedna · 5 tjedana"),
 ("month", "mjesec", "m", "2 mjeseca · 5 mjeseci; also means moon"),
 ("year", "godina", "f", "2 godine · 5 godina"),
 ("decade", "desetljeće", "n", "2 desetljeća · 5 desetljeća"),
 ("century", "stoljeće", "n", "u 21. stoljeću = in the 21st century"),
 ("millennium", "tisućljeće", "n", ""),
 ("time / weather", "vrijeme", "n", "Nemam vremena = I don't have time; Kakvo je vrijeme? = What's the weather like?"),
 ("moment", "trenutak", "m", ""),
 ("half an hour", "pola sata", "", ""),
 ("quarter of an hour", "četvrt sata", "", ""),
 ("an hour (length of time)", "sat vremena", "", "Čekam sat vremena = I've been waiting for an hour"),
 ("calendar", "kalendar", "m", ""),
 ("date", "datum", "m", ""),
 ("two minutes", "dvije minute", "", "2–4: dvije with feminine nouns, then the small-number form"),
 ("five minutes", "pet minuta", "", "5 and up: genitive plural"),
 # 2 Yesterday, today, tomorrow
 ("the day before yesterday", "prekjučer", "", ""),
 ("yesterday", "jučer", "", ""),
 ("today", "danas", "", ""),
 ("tomorrow", "sutra", "", ""),
 ("the day after tomorrow", "prekosutra", "", ""),
 ("now", "sada / sad", "", ""),
 ("right away", "odmah", "", ""),
 ("soon", "uskoro", "", ""),
 ("later", "kasnije", "", ""),
 ("before / ago", "prije", "", "prije + genitive = ago: prije dva dana"),
 ("after", "poslije", "", ""),
 ("already", "već", "", ""),
 ("still / yet", "još", "", ""),
 ("not yet", "još ne", "", ""),
 ("then / at that time", "tada", "", ""),
 ("then", "onda", "", ""),
 ("early", "rano", "", ""),
 ("late", "kasno", "", ""),
 ("next", "sljedeći", "adj:sljedeći|sljedeća|sljedeće", "synonym: idući"),
 ("last / previous", "prošli", "adj:prošli|prošla|prošlo", ""),
 ("this week", "ovaj tjedan", "", ""),
 ("last week", "prošli tjedan", "", ""),
 ("next week", "sljedeći tjedan", "", "also: idući tjedan"),
 ("this month", "ovaj mjesec", "", ""),
 ("next month", "sljedeći mjesec", "", ""),
 ("this year", "ove godine", "", "godina is feminine, so the genitive: ove godine"),
 ("last year", "prošle godine", "", "genitive"),
 ("next year", "sljedeće godine", "", "genitive"),
 ("two days ago", "prije dva dana", "", "prije + genitive = ago"),
 ("an hour ago", "prije sat vremena", "", "prije + genitive = ago"),
 ("in five minutes", "za pet minuta", "", "za + accusative = in (from now)"),
 ("in a week", "za tjedan dana", "", "za + accusative = in (from now)"),
 # 3 Parts of the day
 ("morning", "jutro", "n", "in the morning = ujutro; this morning = jutros"),
 ("in the morning", "ujutro", "", "no preposition"),
 ("this morning", "jutros", "", ""),
 ("late morning (before noon)", "prijepodne", "n", ""),
 ("noon", "podne", "n", "at noon = u podne"),
 ("at noon", "u podne", "", ""),
 ("afternoon", "poslijepodne", "n", "also: popodne"),
 ("afternoon / in the afternoon", "popodne", "n", ""),
 ("evening", "večer", "f", "in the evening = navečer; this evening = večeras"),
 ("in the evening", "navečer", "", "no preposition"),
 ("this evening", "večeras", "", ""),
 ("night", "noć", "f", "at night = noću; tonight = noćas"),
 ("at night", "noću", "", "no preposition"),
 ("tonight", "noćas", "", ""),
 ("last night", "sinoć", "", ""),
 ("midnight", "ponoć", "f", "at midnight = u ponoć"),
 ("at midnight", "u ponoć", "", ""),
 ("Good morning!", "Dobro jutro!", "", "greeting"),
 ("Good day! / Hello", "Dobar dan!", "", "greeting (daytime)"),
 ("Good evening!", "Dobra večer!", "", "greeting; večer is feminine"),
 ("Good night!", "Laku noć!", "", "greeting"),
 # 4 Telling the time
 ("What time is it?", "Koliko je sati?", "", "phrase"),
 ("one o'clock", "jedan sat", "", ""),
 ("two o'clock / two hours", "dva sata", "", "2–4: sata (tri sata, četiri sata)"),
 ("five o'clock / five hours", "pet sati", "", "5 and up: sati (pet … dvanaest sati)"),
 ("ten past three (3:10)", "tri i deset", "", "long form: tri sata i deset minuta"),
 ("quarter past three (3:15)", "tri i četvrt", "", "also: tri i petnaest"),
 ("half past three (3:30)", "pola četiri", "", "pola counts toward the NEXT hour: pola četiri = 3:30"),
 ("quarter to four (3:45)", "četvrt do četiri", "", ""),
 ("five to four (3:55)", "pet do četiri", "", ""),
 ("At what time?", "U koliko sati?", "", "phrase"),
 ("at seven o'clock", "u sedam sati", "", "u + time"),
 ("at half past seven (7:30)", "u pola osam", "", "pola osam = 7:30"),
 ("from nine to five", "od devet do pet", "", ""),
 ("at seven in the morning", "u sedam ujutro", "", ""),
 ("at eight in the evening", "u osam navečer", "", ""),
 # 5 Days of the week
 ("Monday", "ponedjeljak", "m", "on Monday = u ponedjeljak; on Mondays = ponedjeljkom"),
 ("Tuesday", "utorak", "m", "on Tuesday = u utorak; on Tuesdays = utorkom"),
 ("Wednesday", "srijeda", "f", "on Wednesday = u srijedu; on Wednesdays = srijedom"),
 ("Thursday", "četvrtak", "m", "on Thursday = u četvrtak; on Thursdays = četvrtkom"),
 ("Friday", "petak", "m", "on Friday = u petak; on Fridays = petkom"),
 ("Saturday", "subota", "f", "on Saturday = u subotu; on Saturdays = subotom"),
 ("Sunday", "nedjelja", "f", "on Sunday = u nedjelju; on Sundays = nedjeljom"),
 ("on Monday", "u ponedjeljak", "", "u + accusative"),
 ("on Wednesday", "u srijedu", "", "u + accusative: srijeda → srijedu"),
 ("on Friday", "u petak", "", "u + accusative"),
 ("on Saturday", "u subotu", "", "u + accusative: subota → subotu"),
 ("on Sunday", "u nedjelju", "", "u + accusative: nedjelja → nedjelju"),
 ("on Mondays / every Monday", "ponedjeljkom", "", "instrumental, no u"),
 ("on Fridays / every Friday", "petkom", "", "instrumental, no u"),
 ("on Saturdays / every Saturday", "subotom", "", "instrumental, no u"),
 ("on Sundays / every Sunday", "nedjeljom", "", "instrumental, no u"),
 ("weekend", "vikend", "m", "on the weekend = za vikend"),
 ("on the weekend", "za vikend", "", "also: preko vikenda"),
 ("workday", "radni dan", "", ""),
 ("holiday (day off)", "praznik", "m", ""),
 # 6 Months and seasons
 ("January", "siječanj", "m", "in January = u siječnju · 1. siječnja"),
 ("February", "veljača", "f", "in February = u veljači · 1. veljače"),
 ("March", "ožujak", "m", "in March = u ožujku · 1. ožujka"),
 ("April", "travanj", "m", "in April = u travnju · 1. travnja"),
 ("May", "svibanj", "m", "in May = u svibnju · 1. svibnja"),
 ("June", "lipanj", "m", "in June = u lipnju · 1. lipnja"),
 ("July", "srpanj", "m", "in July = u srpnju · 1. srpnja"),
 ("August", "kolovoz", "m", "in August = u kolovozu · 1. kolovoza"),
 ("September", "rujan", "m", "in September = u rujnu · 1. rujna"),
 ("October", "listopad", "m", "in October = u listopadu · 1. listopada"),
 ("November", "studeni", "m", "in November = u studenom · 1. studenoga"),
 ("December", "prosinac", "m", "in December = u prosincu · 1. prosinca"),
 ("in January", "u siječnju", "", "u + locative"),
 ("in May", "u svibnju", "", "u + locative"),
 ("in August", "u kolovozu", "", "u + locative"),
 ("birthday", "rođendan", "m", "Rođendan mi je u svibnju = My birthday is in May"),
 ("season (of the year)", "godišnje doba", "n", ""),
 ("spring", "proljeće", "n", "in spring = u proljeće"),
 ("summer", "ljeto", "n", "in summer = ljeti"),
 ("autumn / fall", "jesen", "f", "in autumn = u jesen"),
 ("winter", "zima", "f", "in winter = zimi"),
 ("in spring", "u proljeće", "", ""),
 ("in summer", "ljeti", "", "no preposition"),
 ("in autumn / in the fall", "u jesen", "", ""),
 ("in winter", "zimi", "", "no preposition"),
 # 7 How often
 ("How often?", "Koliko često?", "", "phrase"),
 ("always", "uvijek", "", ""),
 ("usually", "obično", "", ""),
 ("often", "često", "", ""),
 ("sometimes", "ponekad", "", ""),
 ("rarely", "rijetko", "", ""),
 ("never", "nikada / nikad", "", "takes ne: Nikad ne pijem kavu."),
 ("every day", "svaki dan", "", ""),
 ("every week", "svaki tjedan", "", ""),
 ("every month", "svaki mjesec", "", ""),
 ("every year", "svake godine", "", "genitive"),
 ("daily", "dnevno", "", ""),
 ("weekly", "tjedno", "", ""),
 ("monthly", "mjesečno", "", ""),
 ("yearly", "godišnje", "", ""),
 ("once a week", "jednom tjedno", "", ""),
 ("twice a day", "dvaput dnevno", "", "also: dva puta dnevno"),
 ("from time to time", "s vremena na vrijeme", "", ""),
 ("all the time / constantly", "stalno", "", ""),
 # 8 Everyday phrases
 ("Just a minute!", "Samo malo!", "", "phrase"),
 ("Just a moment!", "Samo trenutak!", "", "phrase"),
 ("Wait a second! (informal)", "Čekaj malo!", "", "formal / plural: Čekajte malo!"),
 ("Wait a second! (formal / plural)", "Čekajte malo!", "", ""),
 ("I'm coming right away.", "Odmah dolazim.", "", ""),
 ("I'm in a hurry.", "Žurim se.", "", ""),
 ("I'm late. / I'm running late.", "Kasnim.", "", ""),
 ("No hurry.", "Nema žurbe.", "", ""),
 ("Take it easy. / Slowly.", "Polako.", "", ""),
 ("on time", "na vrijeme", "", ""),
 ("Do you have time? (informal)", "Imaš li vremena?", "", "vremena = genitive of vrijeme"),
 ("I don't have time.", "Nemam vremena.", "", "vremena = genitive of vrijeme"),
 ("It's time for lunch.", "Vrijeme je za ručak.", "", ""),
 ("How long does it last?", "Koliko traje?", "", ""),
 ("How long?", "Koliko dugo?", "", ""),
 ("Sooner or later.", "Prije ili kasnije.", "", ""),
 ("See you soon!", "Vidimo se uskoro!", "", ""),
 ("See you tomorrow!", "Do sutra!", "", "literally: until tomorrow"),
 ("The early bird catches the worm.", "Tko rano rani, dvije sreće grabi.", "", "proverb"),
]
VR_NOTE = {hr: n for _e, hr, _g, n in VR if n}
vr_rows = [(e, hr, g) for e, hr, g, _n in VR]
H.append(("time", "Vrijeme (time)", "W00_U0_Vrijeme_study.pdf", vr_rows))


# W00 · U0 (added Nov 15, 2026): reference set not tied to a class week or a Tako lako lesson.
# Holds every short word (above) plus the 21 verbs from the W00_U0_Glagol sheets: infinitive + the 6 present forms.
# English "he has (also: she, it)": the app strips brackets, so "he has" is the typed answer it accepts.
VERBS = [  # (infinitive, english, pattern, [ja, ti, on, mi, vi, oni], [english base forms])
    ("biti", "to be", "irregular; short forms (long: jesam, jesi, jest…)", ["sam", "si", "je", "smo", "ste", "su"], ["am", "are", "is", "are", "are", "are"]),
    ("dati", "to give", "-am verb", ["dam", "daš", "da", "damo", "date", "daju"], ["give", "give", "gives", "give", "give", "give"]),
    ("govoriti", "to speak", "-im verb", ["govorim", "govoriš", "govori", "govorimo", "govorite", "govore"], ["speak", "speak", "speaks", "speak", "speak", "speak"]),
    ("htjeti", "to want", "irregular; short forms ću, ćeš… make the future", ["hoću", "hoćeš", "hoće", "hoćemo", "hoćete", "hoće"], ["want", "want", "wants", "want", "want", "want"]),
    ("ići", "to go", "-em verb (stem id-)", ["idem", "ideš", "ide", "idemo", "idete", "idu"], ["go", "go", "goes", "go", "go", "go"]),
    ("imati", "to have", "-am verb; negative nemam", ["imam", "imaš", "ima", "imamo", "imate", "imaju"], ["have", "have", "has", "have", "have", "have"]),
    ("jesti", "to eat", "-em verb (stem jed-)", ["jedem", "jedeš", "jede", "jedemo", "jedete", "jedu"], ["eat", "eat", "eats", "eat", "eat", "eat"]),
    ("misliti", "to think", "-im verb", ["mislim", "misliš", "misli", "mislimo", "mislite", "misle"], ["think", "think", "thinks", "think", "think", "think"]),
    ("moći", "can / to be able to", "irregular (mog- / mož-)", ["mogu", "možeš", "može", "možemo", "možete", "mogu"], ["can", "can", "can", "can", "can", "can"]),
    ("morati", "must / to have to", "-am verb", ["moram", "moraš", "mora", "moramo", "morate", "moraju"], ["must", "must", "must", "must", "must", "must"]),
    ("piti", "to drink", "-em verb", ["pijem", "piješ", "pije", "pijemo", "pijete", "piju"], ["drink", "drink", "drinks", "drink", "drink", "drink"]),
    ("raditi", "to work / to do", "-im verb", ["radim", "radiš", "radi", "radimo", "radite", "rade"], ["work", "work", "works", "work", "work", "work"]),
    ("razumjeti", "to understand", "-em verb", ["razumijem", "razumiješ", "razumije", "razumijemo", "razumijete", "razumiju"], ["understand", "understand", "understands", "understand", "understand", "understand"]),
    ("spavati", "to sleep", "-am verb", ["spavam", "spavaš", "spava", "spavamo", "spavate", "spavaju"], ["sleep", "sleep", "sleeps", "sleep", "sleep", "sleep"]),
    ("trebati", "to need", "-am verb", ["trebam", "trebaš", "treba", "trebamo", "trebate", "trebaju"], ["need", "need", "needs", "need", "need", "need"]),
    ("vidjeti", "to see", "-im verb", ["vidim", "vidiš", "vidi", "vidimo", "vidite", "vide"], ["see", "see", "sees", "see", "see", "see"]),
    ("voljeti", "to like / to love", "-im verb", ["volim", "voliš", "voli", "volimo", "volite", "vole"], ["like", "like", "likes", "like", "like", "like"]),
    ("željeti", "to wish / would like", "-im verb", ["želim", "želiš", "želi", "želimo", "želite", "žele"], ["wish", "wish", "wishes", "wish", "wish", "wish"]),
    ("živjeti", "to live", "-im verb", ["živim", "živiš", "živi", "živimo", "živite", "žive"], ["live", "live", "lives", "live", "live", "live"]),
    ("znati", "to know", "-am verb", ["znam", "znaš", "zna", "znamo", "znate", "znaju"], ["know", "know", "knows", "know", "know", "know"]),
]
WHO = ["I {}", "you {} (informal)", "he {} (also: she, it)", "we {}", "you {} (plural or polite)", "they {}"]
SECOND = {"raditi": "do", "voljeti": "love", "željeti": "want"}   # second meaning on the sheet: "I work / I do"
SECOND3 = {"do": "does", "love": "loves", "want": "wants"}
VERB_NOTE = {}
w00 = []
for inf, en, pat, forms, ens in VERBS:
    w00.append((en, inf, ""))
    VERB_NOTE[inf] = f"verb, infinitive · {pat}"
    for i, (hr, e) in enumerate(zip(forms, ens)):
        s = SECOND.get(inf)
        if s:  # "I work / I do", "he works / he does (also: she, it)"
            who, tail = WHO[i].split(" {}")
            txt = f"{who} {e} / {who} {SECOND3[s] if i == 2 else s}{tail}"
        else:
            txt = WHO[i].format(e)
        w00.append((txt, hr, ""))
        VERB_NOTE.setdefault(hr, f"verb {inf} ({en}) · present tense")
# sviđati se: the person is in the dative ("it pleases me")
w00.append(("to like (to be pleasing)", "sviđati se", ""))
VERB_NOTE["sviđati se"] = "verb, infinitive · -am verb, “backwards”: the person who likes is in the dative"
for en, hr in [("I like it", "sviđa mi se"), ("you like it (informal)", "sviđa ti se"), ("he likes it", "sviđa mu se"),
               ("she likes it", "sviđa joj se"), ("we like it", "sviđa nam se"), ("you like it (plural or polite)", "sviđa vam se"),
               ("they like it", "sviđa im se")]:
    w00.append((en, hr, ""))
    VERB_NOTE.setdefault(hr, "verb sviđati se (to like) · present tense, person in the dative")
short_rows = [r for h in H if h[0] == "short" for r in h[3]]
# Nov 17, 2026: the prepositions (now their own handout) stay in the W00 · U0 set too.
# Nov 21, 2026: the Vrijeme (time) words are in the W00 · U0 set too.
H.append(("w00u0", "W00 · U0 Reference (short words, prepositions, verbs & time)", "W00_U0_Kratke-rijeci_ref.pdf + W00_U0_Prijedlozi_ref.pdf + W00_U0_Glagol sheets + W00_U0_Vrijeme_study.pdf", short_rows + prep_rows + w00 + vr_rows))


# >>> CSOB (generated by Taka Lako Class/_tools/csob_vocab_block.py; edit that script, not this block)
# Croatian School of Boston: one handout per class date, words from the date's main lesson and its
# T1 (Words) page on croatianschoolofboston.org/uci. English and example sentences are the site's.
# Worksheets: W##_CSOB-T1-T3_…_handout.pdf and W##_CSOB-T1_…_handout.pdf in the class folder's pdf/Homework.
# Row: (english, croatian, g, example, example_en)
CSOB = [  # (week, date, title, files, rows)
    (1, '2026-09-13', 'CSOB Tjedan 1 · Moj grad u Hrvatskoj + Tin ide u školu', 'W01_CSOB-T1-T3_Moj-grad-u-Hrvatskoj_handout.pdf + W01_CSOB-T1_Tin-ide-u-skolu_handout.pdf', [
        ('hi / bye (to friends)', 'bok', '', 'Bok, ja sam Luka!', 'Hi, I am Luka!'),
        ('Good day! / Hello', 'dobar dan', '', 'Dobar dan, učiteljice!', 'Good day, teacher!'),
        ('thank you', 'hvala', '', 'Hvala na pomoći!', 'Thanks for the help!'),
        ('goodbye', 'doviđenja', '', 'Doviđenja, vidimo se u nedjelju!', 'Goodbye, see you on Sunday!'),
        ('ten', 'deset', '', 'Brojim od jedan do deset.', 'I count from one to ten.'),
        ('city / town', 'grad', 'm', 'Moj grad je na moru.', 'My town is by the sea.'),
        ('sea', 'more', 'n', 'Ljeti plivam u moru svaki dan.', 'In the summer I swim in the sea every day.'),
        ('island', 'otok', 'm', 'Baka živi na otoku, a otok se zove Brač.', 'Grandma lives on an island, and the island is called Brač.'),
        ('family', 'obitelj', 'f', 'Moja obitelj je iz Hrvatske.', 'My family is from Croatia.'),
        ('beach', 'plaža', 'f', 'Naša plaža ima bijele kamenčiće.', 'Our beach has little white pebbles.'),
        ('ice cream', 'sladoled', 'm', 'Najbolji sladoled je od čokolade.', 'The best ice cream is chocolate.'),
        ('summer', 'ljeto', 'n', 'Svako ljeto putujemo u Hrvatsku.', 'Every summer we travel to Croatia.'),
        ('I like / I love', 'volim', '', 'Ja volim svoj grad.', 'I love my town.'),
        ('school', 'škola', 'f', 'Škola je velika i lijepa.', 'The school is big and beautiful.'),
        ('teacher (female)', 'učiteljica', 'f', 'Učiteljica se zove Ana.', "The teacher's name is Ana."),
        ('bag', 'torba', 'f', 'Moja torba je plava.', 'My bag is blue.'),
        ('year', 'godina', 'f', 'Imam šest godina, a Luka ima deset godina.', 'I am six, and Luka is ten.'),
    ]),
    (2, '2026-09-27', 'CSOB Tjedan 2 · Tko sam ja? Putovnica + Tko si ti?', 'W02_CSOB-T1-T3_Tko-sam-ja-Putovnica_handout.pdf + W02_CSOB-T1_Tko-si-ti_handout.pdf', [
        ('passport', 'putovnica', 'f', 'Moja putovnica je plava.', 'My passport is blue.'),
        ('name', 'ime', 'n', 'Moje ime je na prvoj stranici.', 'My name is on the first page.'),
        ('year', 'godina', 'f', 'Jedna godina ima dvanaest mjeseci.', 'One year has twelve months.'),
        ('friend', 'prijatelj', 'ma', 'Marko je moj najbolji prijatelj.', 'Marko is my best friend.'),
        ('question', 'pitanje', 'n', 'Imam jedno pitanje za tebe.', 'I have one question for you.'),
        ('from where', 'odakle', '', 'Odakle si ti?', 'Where are you from?'),
        ('nice to meet you', 'drago mi je', '', 'Bok, drago mi je!', 'Hi, nice to meet you!'),
        ('class / grade', 'razred', 'm', 'Naš razred je veseo.', 'Our class is cheerful.'),
        ('my name is …', 'zovem se', '', 'Zovem se Tin.', 'My name is Tin.'),
        ('friend (girl)', 'prijateljica', 'f', 'Lana je moja nova prijateljica.', 'Lana is my new friend.'),
        ('park', 'park', 'm', 'Park je pun djece.', 'The park is full of children.'),
        ('ball', 'lopta', 'f', 'Moja lopta je crvena.', 'My ball is red.'),
        ('the same / too', 'isto', '', 'I ja imam šest godina, isto!', 'I am six too, the same!'),
    ]),
    (3, '2026-10-04', 'CSOB Tjedan 3 · Obiteljsko stablo + Obiteljska fotografija', 'W03_CSOB-T1-T3_Obiteljsko-stablo_handout.pdf + W03_CSOB-T1_Obiteljska-fotografija_handout.pdf', [
        ('mom', 'mama', 'f', 'Moja mama ima dugu kosu.', 'My mom has long hair.'),
        ('dad', 'tata', 'ma', 'Moj tata je jako visok.', 'My dad is very tall.'),
        ('brother', 'brat', 'ma', 'Moj brat voli nogomet.', 'My brother loves soccer.'),
        ('sister', 'sestra', 'f', 'Moja sestra ide u peti razred.', 'My sister is in fifth grade.'),
        ('grandma', 'baka', 'f', 'Naša baka peče najbolje palačinke.', 'Our grandma makes the best palačinke.'),
        ('grandpa', 'djed', 'ma', 'Moj djed ima sijedu bradu.', 'My grandpa has a gray beard.'),
        ('tall', 'visok', 'adj:visok|visoka|visoko', 'Košarkaš je visok čovjek.', 'A basketball player is a tall person.'),
        ('short (height) / low', 'nizak', 'adj:nizak|niska|nisko', 'Stol za bebe je nizak.', 'A baby table is low.'),
        ('hair', 'kosa', 'f', 'Marina kosa je crna i kovrčava.', "Mara's hair is black and curly."),
        ('family', 'obitelj', 'f', 'Moja obitelj je velika.', 'My family is big.'),
        ('cat', 'mačka', 'f', 'Naša mačka se zove Lena.', 'Our cat is called Lena.'),
        ('photograph', 'fotografija', 'f', 'Ova fotografija je za školu.', 'This photograph is for school.'),
        ('everyone / all', 'svi', '', 'Svi smo zajedno.', 'We are all together.'),
    ]),
    (4, '2026-10-18', 'CSOB Tjedan 4 · Izgled i osobine', 'W04_CSOB-T1-T3_Izgled-i-osobine_handout.pdf', [
        ('tall', 'visok', 'adj:visok|visoka|visoko', 'Moj tata je jako visok.', 'My dad is very tall.'),
        ('short (height) / low', 'nizak', 'adj:nizak|niska|nisko', 'Tin je još malen i nizak.', 'Tin is still little and short.'),
        ('thin / slim', 'mršav', 'adj:mršav|mršava|mršavo', 'Naš susjed je visok i mršav.', 'Our neighbor is tall and thin.'),
        ('strong', 'snažan', 'adj:snažan|snažna|snažno', 'Tata je snažan kao medvjed.', 'Dad is as strong as a bear.'),
        ('young', 'mlad', 'adj:mlad|mlada|mlado', 'Naš novi učitelj je mlad.', 'Our new teacher is young.'),
        ('old', 'star', 'adj:star|stara|staro', 'Djedov auto je jako star.', "Grandpa's car is very old."),
        ('good-looking / handsome / attractive', 'zgodan', 'adj:zgodan|zgodna|zgodno', 'Djed misli da je jako zgodan.', 'Grandpa thinks he is very handsome.'),
        ('beautiful / pretty', 'lijep', 'adj:lijep|lijepa|lijepo', 'Danas je lijep sunčan dan.', 'Today is a beautiful sunny day.'),
        ('cute', 'sladak', 'adj:sladak|slatka|slatko', 'Susjedov mali pas je sladak.', "The neighbor's little dog is cute."),
        ('has long hair', 'ima dugu kosu', '', 'Moja mama ima dugu kosu.', 'My mom has long hair.'),
        ('has short hair', 'ima kratku kosu', '', 'Moj brat ima kratku kosu.', 'My brother has short hair.'),
        ('has straight hair', 'ima ravnu kosu', '', 'Moja sestra ima ravnu kosu.', 'My sister has straight hair.'),
        ('has curly hair', 'ima kovrčavu kosu', '', 'Tin ima kovrčavu kosu kao janje.', 'Tin has curly hair like a lamb.'),
        ('has blonde hair', 'ima plavu kosu', '', 'Moja prijateljica ima plavu kosu.', 'My friend has blonde hair.'),
        ('has brown hair', 'ima smeđu kosu', '', 'Moj tata ima smeđu kosu.', 'My dad has brown hair.'),
        ('has black hair', 'ima crnu kosu', '', 'Naša mama ima crnu kosu.', 'Our mom has black hair.'),
        ('has red hair', 'ima crvenu kosu', '', 'Moja teta ima crvenu kosu.', 'My aunt has red hair.'),
        ('has blue eyes', 'ima plave oči', '', 'Moj djed ima plave oči.', 'My grandpa has blue eyes.'),
        ('has green eyes', 'ima zelene oči', '', 'Bakino mače ima zelene oči.', "Grandma's kitten has green eyes."),
        ('has brown eyes', 'ima smeđe oči', '', 'Moj tata ima smeđe oči.', 'My dad has brown eyes.'),
        ('wears glasses', 'nosi naočale', '', 'Djed nosi naočale za čitanje.', 'Grandpa wears reading glasses.'),
        ('has a beard', 'ima bradu', '', 'Djed ima bradu i brkove.', 'Grandpa has a beard and a mustache.'),
        ('has a mustache', 'ima brkove', '', 'Moj ujak ima brkove.', 'My uncle has a mustache.'),
        ('kind', 'ljubazan', 'adj:ljubazan|ljubazna|ljubazno', 'Naš susjed je jako ljubazan.', 'Our neighbor is very kind.'),
        ('friendly', 'prijateljski', 'adj:prijateljski|prijateljska|prijateljsko', 'Bobi je prijateljski pas.', 'Bobi is a friendly dog.'),
        ('cheerful', 'veseo', 'adj:veseo|vesela|veselo', 'Tin je uvijek veseo ujutro.', 'Tin is always cheerful in the morning.'),
        ('happy', 'sretan', 'adj:sretan|sretna|sretno', 'Danas sam jako sretan!', 'Today I am very happy!'),
        ('sad', 'tužan', 'adj:tužan|tužna|tužno', 'Bobi je tužan kad ostane sam.', 'Bobi is sad when he is left alone.'),
        ('funny', 'smiješan', 'adj:smiješan|smiješna|smiješno', 'Ovaj crtić je jako smiješan.', 'This cartoon is very funny.'),
        ('serious', 'ozbiljan', 'adj:ozbiljan|ozbiljna|ozbiljno', 'Ravnatelj je danas vrlo ozbiljan.', 'The principal is very serious today.'),
        ('calm', 'miran', 'adj:miran|mirna|mirno', 'Navečer je naš pas miran.', 'In the evening our dog is calm.'),
        ('active', 'aktivan', 'adj:aktivan|aktivna|aktivno', 'Djed je star, ali aktivan.', 'Grandpa is old, but active.'),
        ('hard-working / diligent', 'vrijedan', 'adj:vrijedan|vrijedna|vrijedno', 'Tata je vrijedan i puno radi.', 'Dad is hardworking and works a lot.'),
        ('lazy', 'lijen', 'adj:lijen|lijena|lijeno', 'Nedjeljom je tata malo lijen.', 'On Sundays dad is a little lazy.'),
        ('smart', 'pametan', 'adj:pametan|pametna|pametno', 'Moj brat je jako pametan.', 'My brother is very smart.'),
        ('creative', 'kreativan', 'adj:kreativan|kreativna|kreativno', 'Tin je kreativan i voli crtati.', 'Tin is creative and loves to draw.'),
        ('brave', 'hrabar', 'adj:hrabar|hrabra|hrabro', 'Vatrogasac mora biti hrabar.', 'A firefighter has to be brave.'),
        ('shy', 'sramežljiv', 'adj:sramežljiv|sramežljiva|sramežljivo', 'Tin je sramežljiv pred gostima.', 'Tin is shy in front of guests.'),
        ('sociable', 'društven', 'adj:društven|društvena|društveno', 'Moj tata je vrlo društven.', 'My dad is very sociable.'),
        ('talkative', 'pričljiv', 'adj:pričljiv|pričljiva|pričljivo', 'Moj prijatelj je jako pričljiv.', 'My friend is very talkative.'),
        ('quiet', 'tih', 'adj:tih|tiha|tiho', 'U knjižnici moraš biti tih.', 'In the library you have to be quiet.'),
        ('patient', 'strpljiv', 'adj:strpljiv|strpljiva|strpljivo', 'Dobar učitelj je uvijek strpljiv.', 'A good teacher is always patient.'),
        ('impatient', 'nestrpljiv', 'adj:nestrpljiv|nestrpljiva|nestrpljivo', 'Tin je nestrpljiv prije rođendana.', 'Tin is impatient before his birthday.'),
        ('generous', 'velikodušan', 'adj:velikodušan|velikodušna|velikodušno', 'Djed je velikodušan prema svima.', 'Grandpa is generous to everyone.'),
        ('selfish', 'sebičan', 'adj:sebičan|sebična|sebično', 'Nemoj biti sebičan, podijeli igračke.', "Don't be selfish, share your toys."),
        ('honest', 'pošten', 'adj:pošten|poštena|pošteno', 'Moj prijatelj je uvijek pošten.', 'My friend is always honest.'),
        ('curious', 'znatiželjan', 'adj:znatiželjan|znatiželjna|znatiželjno', 'Tin je znatiželjan i sve pita.', 'Tin is curious and asks about everything.'),
        ('jealous', 'ljubomoran', 'adj:ljubomoran|ljubomorna|ljubomorno', 'Bobi je ljubomoran na mače.', 'Bobi is jealous of the kitten.'),
    ]),
    (5, '2026-10-25', 'CSOB Tjedan 5 · Tržnica Dolac + Jesen u parku', 'W05_CSOB-T1-T3_Trznica-Dolac_handout.pdf + W05_CSOB-T1_Jesen-u-parku_handout.pdf', [
        ('market', 'tržnica', 'f', 'Subotom idemo na tržnicu.', 'On Saturdays we go to the market.'),
        ('apple', 'jabuka', 'f', 'Ova jabuka je crvena i slatka.', 'This apple is red and sweet.'),
        ('bread', 'kruh', 'm', 'Kupujem topli kruh iz pekare.', "I'm buying warm bread from the bakery."),
        ('cheese', 'sir', 'm', 'Domaći sir najbolji je na svijetu.', 'Homemade cheese is the best in the world.'),
        ('grapes', 'grožđe', 'n', 'Djed u vrtu ima grožđe.', 'Grandpa has grapes in his garden.'),
        ('orange', 'naranča', 'f', 'Jedna naranča stoji na stolu.', 'One orange is sitting on the table.'),
        ('to buy', 'kupiti', '', 'Želim kupiti dar za baku.', 'I want to buy a gift for grandma.'),
        ('to cost', 'koštati', '', 'Koliko može koštati jedan sladoled?', 'How much can one ice cream cost?'),
        ('money', 'novac', 'm', 'Novac je u mom džepu.', 'The money is in my pocket.'),
        ('autumn / fall', 'jesen', 'f', 'Jesen je moje najdraže godišnje doba.', 'Autumn is my favorite season.'),
        ('leaves', 'lišće', 'n', 'Lišće je žuto, crveno i smeđe.', 'The leaves are yellow, red and brown.'),
        ('wind', 'vjetar', 'm', 'Vjetar danas jako puše.', 'The wind is blowing hard today.'),
        ('chestnut', 'kesten', 'm', 'Kesten je pao s drveta.', 'A chestnut fell from the tree.'),
        ('to jump', 'skakati', '', 'Volim skakati po lišću.', 'I love jumping in the leaves.'),
        ('cold', 'hladno', '', 'Danas je hladno.', "It's cold today."),
        ('jacket', 'jakna', 'f', 'Gdje je moja topla jakna?', 'Where is my warm jacket?'),
        ('hat / beanie', 'kapa', 'f', 'Tatina kapa je smiješna.', "Dad's hat is funny."),
    ]),
    (6, '2026-11-08', 'CSOB Tjedan 6 · U pekari i kafiću + Prva palačinka', 'W06_CSOB-T1-T3_U-pekari-i-kaficu_handout.pdf + W06_CSOB-T1_Prva-palacinka_handout.pdf', [
        ('bakery', 'pekara', 'f', 'Naša se pekara otvara u sedam sati.', 'Our bakery opens at seven.'),
        ('café', 'kafić', 'm', 'Tata subotom sjedi u kafiću.', 'Dad sits in the café on Saturdays.'),
        ('burek (savory pastry)', 'burek', 'm', 'Topli burek sa sirom je najbolji doručak.', 'Warm burek with cheese is the best breakfast.'),
        ('juice', 'sok', 'm', 'Želim sok od naranče.', 'I want orange juice.'),
        ('water', 'voda', 'f', 'Hladna voda je na stolu.', 'Cold water is on the table.'),
        ('waiter', 'konobar', 'ma', 'Konobar nosi četiri kave odjednom.', 'The waiter is carrying four coffees at once.'),
        ('bill / receipt', 'račun', 'm', 'Račun je deset eura.', 'The bill is ten euros.'),
        ('to order', 'naručiti', '', 'Smijem li naručiti tortu?', 'May I order the cake?'),
        ('I want', 'želim', '', 'Ja želim palačinke s čokoladom.', 'I want palačinke with chocolate.'),
        ('breakfast', 'doručak', 'm', 'Za doručak jedemo palačinke.', 'For breakfast we eat pancakes.'),
        ('egg', 'jaje', 'n', 'Jedno jaje pada na pod.', 'One egg falls on the floor.'),
        ('milk', 'mlijeko', 'n', 'Mlijeko je u hladnjaku.', 'The milk is in the fridge.'),
        ('flour', 'brašno', 'n', 'Brašno je bijelo kao snijeg.', 'Flour is white like snow.'),
        ('spoon', 'žlica', 'f', 'Gdje je žlica za tijesto?', 'Where is the spoon for the batter?'),
        ('pancake', 'palačinka', 'f', 'Prva palačinka nikad ne uspije.', 'The first pancake never turns out right.'),
        ('dog', 'pas', 'ma', 'Naš pas voli palačinke.', 'Our dog loves pancakes.'),
        ('honey', 'med', 'm', 'Med je jako sladak.', 'Honey is very sweet.'),
    ]),
    (7, '2026-11-22', 'CSOB Tjedan 7 · Izbirljivi gost + Čaj bez šećera', 'W07_CSOB-T1-T3_Izbirljivi-gost_handout.pdf + W07_CSOB-T1_Caj-bez-secera_handout.pdf', [
        ('menu', 'jelovnik', 'm', 'Jelovnik ima četiri stranice.', 'The menu has four pages.'),
        ('milk', 'mlijeko', 'n', 'Pijem kakao bez mlijeka.', 'I drink cocoa without milk.'),
        ('sugar', 'šećer', 'm', 'Baka u čaj ne stavlja šećer.', "Grandma doesn't put sugar in her tea."),
        ('gluten', 'gluten', 'm', 'Ovaj kruh nema gluten.', 'This bread has no gluten.'),
        ('allergy', 'alergija', 'f', 'Markova alergija je na orahe.', "Marko's allergy is to walnuts."),
        ("I'm not allowed", 'ne smijem', '', 'Ja ne smijem jesti jagode.', "I'm not allowed to eat strawberries."),
        ('soup', 'juha', 'f', 'Topla juha je dobra zimi.', 'Warm soup is good in winter.'),
        ('salad', 'salata', 'f', 'Zelena salata je zdrava.', 'Green salad is healthy.'),
        ('to recommend', 'preporučiti', '', 'Mogu li vam preporučiti rižoto?', 'May I recommend the risotto?'),
        ('tea', 'čaj', 'm', 'Baka pije topli čaj.', 'Grandma drinks warm tea.'),
        ('without', 'bez', '', 'Čaj bez šećera je zdrav.', 'Tea without sugar is healthy.'),
        ('honey', 'med', 'm', 'Med je sladak i žut.', 'Honey is sweet and yellow.'),
        ('spoon', 'žlica', 'f', 'Jedna žlica meda, molim.', 'One spoon of honey, please.'),
        ('sweet', 'sladak', 'adj:sladak|slatka|slatko', 'Ovaj čaj je sladak!', 'This tea is sweet!'),
    ]),
    (8, '2026-12-06', 'CSOB Tjedan 8 · Gdje je muzej? + Gdje je Miško?', 'W08_CSOB-T1-T3_Gdje-je-muzej_handout.pdf + W08_CSOB-T1_Gdje-je-Misko_handout.pdf', [
        ('left', 'lijevo', '', 'Skreni lijevo kod pekare.', 'Turn left at the bakery.'),
        ('right', 'desno', '', 'Pošta je desno od banke.', 'The post office is to the right of the bank.'),
        ('straight ahead', 'ravno', '', 'Idi ravno do velikog trga.', 'Go straight to the big square.'),
        ('stop!', 'stani', '', 'Stani, semafor je crven!', 'Stop, the light is red!'),
        ('museum', 'muzej', 'm', 'Ovaj muzej ima staru putovnicu iz 1935.', 'This museum has an old passport from 1935.'),
        ('square', 'trg', 'm', 'Na trgu je spomenik banu Jelačiću.', 'On the square is the monument to Ban Jelačić.'),
        ('street', 'ulica', 'f', 'Naša ulica je duga i mirna.', 'Our street is long and quiet.'),
        ('intersection', 'križanje', 'n', 'Na križanju čekamo zeleno svjetlo.', 'At the intersection we wait for the green light.'),
        ('step', 'korak', 'm', 'Naprijed još jedan korak!', 'One more step forward!'),
        ('hamster', 'hrčak', 'ma', 'Naš hrčak se zove Miško.', 'Our hamster is called Miško.'),
        ('cage', 'kavez', 'm', 'Kavez je otvoren i prazan!', 'The cage is open and empty!'),
        ('to look for', 'tražiti', '', 'Idemo tražiti Miška.', "Let's go look for Miško."),
        ('slipper', 'papuča', 'f', 'Tatina papuča je velika i topla.', "Dad's slipper is big and warm."),
        ('to sleep', 'spavati', '', 'Miško voli spavati cijeli dan.', 'Miško loves to sleep all day.'),
        ('hungry', 'gladan', 'adj:gladan|gladna|gladno', 'Miško je uvijek gladan.', 'Miško is always hungry.'),
        ('cheese', 'sir', 'm', 'Sir je Miškova najdraža hrana.', "Cheese is Miško's favorite food."),
        ('room', 'soba', 'f', 'Moja soba je mala.', 'My room is small.'),
    ]),
    (9, '2026-12-13', 'CSOB Tjedan 9 · Putujemo vlakom + Tin i vlak', 'W09_CSOB-T1-T3_Putujemo-vlakom_handout.pdf + W09_CSOB-T1_Tin-i-vlak_handout.pdf', [
        ('train', 'vlak', 'm', 'Plavi vlak polazi u osam sati.', 'The blue train leaves at eight.'),
        ('ticket', 'karta', 'f', 'Jedna karta za Split, molim.', 'One ticket to Split, please.'),
        ('train station', 'kolodvor', 'm', 'Glavni kolodvor je pun ljudi.', 'The main station is full of people.'),
        ('departure', 'polazak', 'm', 'Polazak je s drugog perona.', 'The departure is from platform two.'),
        ('platform', 'peron', 'm', 'Naš peron je broj četiri.', 'Our platform is number four.'),
        ('to be late', 'kasniti', '', 'Vlak danas može kasniti pola sata.', 'The train may be half an hour late today.'),
        ('passenger', 'putnik', 'ma', 'Svaki putnik ima svoje mjesto.', 'Every passenger has their own seat.'),
        ('when', 'kada', '', 'Kada polazi autobus za Zadar?', 'When does the bus to Zadar leave?'),
        ('window', 'prozor', 'm', 'Tin sjedi kod prozora.', 'Tin sits by the window.'),
        ('to travel', 'putovati', '', 'Volim putovati vlakom.', 'I love traveling by train.'),
        ('station / stop', 'stanica', 'f', 'Zadnja stanica je Split.', 'The last stop is Split.'),
    ]),
    (10, '2027-01-24', 'CSOB Tjedan 10 · Moj tjedni raspored + Tinov dan', 'W10_CSOB-T1-T3_Moj-tjedni-raspored_handout.pdf + W10_CSOB-T1_Tinov-dan_handout.pdf', [
        ('hour / clock', 'sat', 'm', 'Jedan sat ima šezdeset minuta.', 'One hour has sixty minutes.'),
        ('in the morning', 'ujutro', '', 'Ustajem rano ujutro.', 'I get up early in the morning.'),
        ('in the afternoon', 'popodne', '', 'Popodne imam trening.', 'In the afternoon I have practice.'),
        ('in the evening', 'navečer', '', 'Navečer čitam knjigu.', 'In the evening I read a book.'),
        ('schedule', 'raspored', 'm', 'Moj raspored je pun cijeli tjedan.', 'My schedule is full all week.'),
        ('weekend', 'vikend', 'm', 'Za vikend idemo baki.', "On the weekend we're going to grandma's."),
        ('practice / training', 'trening', 'm', 'Trening počinje u četiri sata.', 'Practice starts at four.'),
        ('free', 'slobodan', 'adj:slobodan|slobodna|slobodno', 'Jesi li slobodan u subotu?', 'Are you free on Saturday?'),
        ('to wake up', 'buditi se', '', 'Ne volim se buditi rano.', "I don't like waking up early."),
        ('seven', 'sedam', '', 'Budim se u sedam sati.', 'I wake up at seven.'),
        ('breakfast', 'doručak', 'm', 'Doručak je na stolu.', 'Breakfast is on the table.'),
        ('lunch', 'ručak', 'm', 'Ručak je u jedan sat.', "Lunch is at one o'clock."),
        ('dinner', 'večera', 'f', 'Večera je u sedam navečer.', 'Dinner is at seven in the evening.'),
        ('to sleep', 'spavati', '', 'Tin ide spavati u osam.', 'Tin goes to sleep at eight.'),
    ]),
    (11, '2027-02-07', 'CSOB Tjedan 11 · Tko posprema sobu? + Tin pomaže', 'W11_CSOB-T1-T3_Tko-posprema-sobu_handout.pdf + W11_CSOB-T1_Tin-pomaze_handout.pdf', [
        ('room', 'soba', 'f', 'Moja soba je danas uredna.', 'My room is tidy today.'),
        ('to tidy up', 'pospremiti', '', 'Moram pospremiti igračke.', 'I have to tidy up the toys.'),
        ('cooking', 'kuhanje', 'n', 'Kuhanje s bakom je zabavno.', 'Cooking with grandma is fun.'),
        ('cleaning', 'čišćenje', 'n', 'Čišćenje prozora nije moj posao.', 'Cleaning the windows is not my job.'),
        ('trash', 'smeće', 'n', 'Tko će iznijeti smeće?', 'Who will take out the trash?'),
        ('dishes', 'suđe', 'n', 'Poslije ručka perem suđe.', 'After lunch I wash the dishes.'),
        ('vacuum cleaner', 'usisavač', 'm', 'Naš usisavač je glasan kao avion.', 'Our vacuum cleaner is as loud as an airplane.'),
        ('I must / I have to', 'moram', '', 'Ja moram prvo napisati zadaću.', 'I have to do my homework first.'),
        ('to help', 'pomoći', '', 'Mogu li ti pomoći?', 'Can I help you?'),
        ('to help', 'pomagati', '', 'Tin voli pomagati mami.', 'Tin likes helping mom.'),
        ('to cook', 'kuhati', '', 'Tata zna kuhati juhu.', 'Dad knows how to cook soup.'),
        ('to clean', 'čistiti', '', 'Mama voli čistiti prozore.', 'Mom likes cleaning windows.'),
        ('table', 'stol', 'm', 'Tin briše stol.', 'Tin wipes the table.'),
        ('toys', 'igračke', 'fpl', 'Igračke idu u kutiju.', 'The toys go in the box.'),
        ('well done', 'bravo', '', 'Bravo, Tine!', 'Well done, Tin!'),
    ]),
    (12, '2027-02-28', 'CSOB Tjedan 12 · Kod liječnika + Tin je bolestan', 'W12_CSOB-T1-T3_Kod-lijecnika_handout.pdf + W12_CSOB-T1_Tin-je-bolestan_handout.pdf', [
        ('head', 'glava', 'f', 'Boli me glava od sunca.', 'My head hurts from the sun.'),
        ('stomach / belly', 'trbuh', 'm', 'Poslije pet palačinki boli me trbuh.', 'After five palačinke my stomach hurts.'),
        ('knee', 'koljeno', 'n', 'Moje koljeno je plavo od nogometa.', 'My knee is bruised from soccer.'),
        ('tooth', 'zub', 'm', 'Klimavi zub napokon je ispao.', 'The wobbly tooth finally fell out.'),
        ('doctor', 'liječnik', 'ma', 'Liječnik nosi bijelu kutu.', 'The doctor wears a white coat.'),
        ('sick', 'bolestan', 'adj:bolestan|bolesna|bolesno', 'Marko je danas bolestan i nije u školi.', 'Marko is sick today and not in school.'),
        ('medicine', 'lijek', 'm', 'Ovaj lijek se pije poslije jela.', 'This medicine is taken after meals.'),
        ('to lie down', 'ležati', '', 'Kad si bolestan, moraš ležati.', "When you're sick, you have to lie down."),
        ('sad', 'tužan', 'adj:tužan|tužna|tužno', 'Pas je tužan kad smo u školi.', "The dog is sad when we're at school."),
        ('bed', 'krevet', 'm', 'Tin je u krevetu.', 'Tin is in bed.'),
        ('thermometer', 'toplomjer', 'm', 'Mama ima toplomjer.', 'Mom has a thermometer.'),
        ('healthy', 'zdrav', 'adj:zdrav|zdrava|zdravo', 'Sutra je Tin opet zdrav.', 'Tomorrow Tin is healthy again.'),
    ]),
    (13, '2027-03-14', 'CSOB Tjedan 13 · Izgubljene stvari + Gdje je kapa?', 'W13_CSOB-T1-T3_Izgubljene-stvari_handout.pdf + W13_CSOB-T1_Gdje-je-kapa_handout.pdf', [
        ('bag', 'torba', 'f', 'Moja torba je crvena i velika.', 'My bag is red and big.'),
        ('mobile phone', 'mobitel', 'm', 'Tatin mobitel uvijek zvoni.', "Dad's phone is always ringing."),
        ('key', 'ključ', 'm', 'Ključ od stana je u torbi.', 'The apartment key is in the bag.'),
        ('wallet', 'novčanik', 'm', 'U novčaniku su dva eura.', 'There are two euros in the wallet.'),
        ('umbrella', 'kišobran', 'm', 'Žuti kišobran stoji kod vrata.', 'The yellow umbrella is by the door.'),
        ('to lose', 'izgubiti', '', 'Ne želim izgubiti novu kapu.', "I don't want to lose my new cap."),
        ('to find', 'naći', '', 'Tko će prvi naći ključ?', 'Who will find the key first?'),
        ('yesterday', 'jučer', '', 'Jučer smo igrali nogomet.', 'Yesterday we played soccer.'),
        ('cap / hat', 'kapa', 'f', 'Tinova kapa je crvena.', "Tin's cap is red."),
        ('to look for', 'tražiti', '', 'Svi moraju tražiti kapu.', 'Everyone has to look for the cap.'),
        ('under', 'ispod', '', 'Kapa nije ispod kreveta.', "The cap isn't under the bed."),
        ('red', 'crven', 'adj:crven|crvena|crveno', 'Auto je crven kao jabuka.', 'The car is red like an apple.'),
    ]),
    (14, '2027-03-21', 'CSOB Tjedan 14 · Vremenska prognoza + Pada kiša', 'W14_CSOB-T1-T3_Vremenska-prognoza_handout.pdf + W14_CSOB-T1_Pada-kisa_handout.pdf', [
        ('rain', 'kiša', 'f', 'Pada kiša cijeli dan.', "It's been raining all day."),
        ('snow', 'snijeg', 'm', 'Bijeli snijeg pokriva grad.', 'White snow covers the city.'),
        ('wind', 'vjetar', 'm', 'Jaki vjetar nosi listove.', 'A strong wind carries the leaves.'),
        ('sunny', 'sunčano', '', 'Na moru je uvijek sunčano.', "It's always sunny at the seaside."),
        ('cloudy', 'oblačno', '', 'Nebo je danas oblačno i sivo.', 'The sky is cloudy and gray today.'),
        ('cold', 'hladno', '', 'Zimi je u Bostonu jako hladno.', "In winter it's very cold in Boston."),
        ('jacket', 'jakna', 'f', 'Moja jakna je topla i plava.', 'My jacket is warm and blue.'),
        ('umbrella', 'kišobran', 'm', 'Uzmi kišobran, past će pljusak!', "Take an umbrella, there's going to be a downpour!"),
        ('forecast', 'prognoza', 'f', 'Prognoza kaže da će sutra biti toplo.', 'The forecast says it will be warm tomorrow.'),
        ('sun', 'sunce', 'n', 'Sunce je žuto i toplo.', 'The sun is yellow and warm.'),
        ('boots', 'čizme', 'fpl', 'Tin ima žute čizme.', 'Tin has yellow boots.'),
        ('puddle', 'lokva', 'f', 'Tin skače u lokvu!', 'Tin jumps in the puddle!'),
    ]),
    (15, '2027-04-04', 'CSOB Tjedan 15 · Moja najdraža priča: Šegrt Hlapić + Zlatna ptica', 'W15_CSOB-T1-T3_Moja-najdraza-prica-Segrt-Hlapic_handout.pdf + W15_CSOB-T1_Zlatna-ptica_handout.pdf', [
        ('apprentice', 'šegrt', 'ma', 'Mali šegrt uči zanat kod majstora.', 'The little apprentice learns the trade from a master.'),
        ('master craftsman', 'majstor', 'ma', 'Majstor Mrkonja bio je često ljut.', 'Master Mrkonja was often angry.'),
        ('shoemaker', 'postolar', 'ma', 'Postolar popravlja stare cipele.', 'The shoemaker repairs old shoes.'),
        ('little boots', 'čizmice', 'fpl', 'Male čizmice bile su Hlapiću taman.', 'The little boots fit Hlapić just right.'),
        ('journey', 'putovanje', 'n', 'Njihovo putovanje trajalo je sedam dana.', 'Their journey lasted seven days.'),
        ('brave', 'hrabar', 'adj:hrabar|hrabra|hrabro', 'Hlapić je bio malen, ali hrabar.', 'Hlapić was small, but brave.'),
        ('star', 'zvijezda', 'f', 'Noću je svaka zvijezda pokazivala put.', 'At night every star showed the way.'),
        ('parrot', 'papiga', 'f', 'Gitina papiga zna govoriti.', "Gita's parrot can talk."),
        ('happy', 'sretan', 'adj:sretan|sretna|sretno', 'Na kraju priče svatko je sretan.', 'At the end of the story everyone is happy.'),
        ('king', 'kralj', 'ma', 'Kralj ima veliku krunu.', 'The king has a big crown.'),
        ('bird', 'ptica', 'f', 'Ptica pjeva u vrtu.', 'The bird sings in the garden.'),
        ('golden', 'zlatan', 'adj:zlatan|zlatna|zlatno', 'Ptica je zlatan dar.', 'The bird is a golden gift.'),
        ('son', 'sin', 'ma', 'Kralj ima tri sina.', 'The king has three sons.'),
        ('to sing', 'pjevati', '', 'Ptica ne želi pjevati.', "The bird doesn't want to sing."),
        ('good / kind', 'dobar', 'adj:dobar|dobra|dobro', 'Najmlađi sin ima dobar glas i dobro srce.', 'The youngest son has a good voice and a good heart.'),
    ]),
    (16, '2027-04-11', 'CSOB Tjedan 16 · Mali kritičari + Volim, ne volim', 'W16_CSOB-T1-T3_Mali-kriticari_handout.pdf + W16_CSOB-T1_Volim-ne-volim_handout.pdf', [
        ('movie', 'film', 'm', 'Gledali smo film o gusarima.', 'We watched a movie about pirates.'),
        ('cartoon', 'crtić', 'm', 'Nedjeljom ujutro gledam crtić.', 'On Sunday mornings I watch a cartoon.'),
        ('book', 'knjiga', 'f', 'Ova knjiga ima tristo stranica.', 'This book has three hundred pages.'),
        ('song', 'pjesma', 'f', 'Bakina najdraža pjesma je stara.', "Grandma's favorite song is old."),
        ('interesting', 'zanimljivo', '', 'Predavanje o morskim psima bilo je zanimljivo.', 'The talk about sharks was interesting.'),
        ('boring', 'dosadno', '', 'Čekanje u redu je dosadno.', 'Waiting in line is boring.'),
        ('funny', 'smiješno', '', 'Bobijevo hrkanje je jako smiješno.', "Bobi's snoring is very funny."),
        ('opinion', 'mišljenje', 'n', 'Svatko ima svoje mišljenje.', 'Everyone has their own opinion.'),
        ('I like it', 'sviđa mi se', '', 'Ova priča sviđa mi se od početka.', "I've liked this story from the start."),
        ('funny', 'smiješan', 'adj:smiješan|smiješna|smiješno', 'Ovaj crtić je smiješan!', 'This cartoon is funny!'),
        ('boring', 'dosadan', 'adj:dosadan|dosadna|dosadno', 'Film o povijesti je dosadan.', 'The history movie is boring.'),
        ('favorite', 'najdraži', 'adj:najdraži|najdraža|najdraže', 'Moj najdraži crtić je o zmaju.', 'My favorite cartoon is about a dragon.'),
    ]),
    (17, '2027-04-25', 'CSOB Tjedan 17 · Naši običaji + Tin boji pisanice', 'W17_CSOB-T1-T3_Nasi-obicaji_handout.pdf + W17_CSOB-T1_Tin-boji-pisanice_handout.pdf', [
        ('custom / tradition', 'običaj', 'm', 'Svaki kraj ima svoj običaj.', 'Every region has its own custom.'),
        ('holiday', 'blagdan', 'm', 'Božić je najveseliji blagdan.', 'Christmas is the merriest holiday.'),
        ('decorated Easter egg', 'pisanica', 'f', 'Ova pisanica je crvena sa zlatnim cvijetom.', 'This Easter egg is red with a golden flower.'),
        ('licitar (decorated gingerbread)', 'licitar', 'm', 'Licitar u obliku srca visi na boru.', 'A heart-shaped licitar hangs on the tree.'),
        ('folk costume', 'nošnja', 'f', 'Bakina nošnja ima bijelu bluzu i crvenu suknju.', "Grandma's folk costume has a white blouse and a red skirt."),
        ('cake / pastry', 'kolač', 'm', 'Najbolji kolač je bakina orehnjača.', "The best cake is grandma's walnut roll."),
        ('klapa (a cappella group)', 'klapa', 'f', 'Klapa pjeva bez instrumenata.', 'A klapa sings without instruments.'),
        ('booth / stand', 'štand', 'm', 'Naš štand je kod prozora.', 'Our booth is by the window.'),
        ('Easter', 'Uskrs', 'm', 'Uskrs je u nedjelju.', 'Easter is on Sunday.'),
        ('colour', 'boja', 'f', 'Žuta boja je moja najdraža.', 'Yellow is my favorite color.'),
        ('onion', 'luk', 'm', 'Baka boji jaja lukom.', 'Grandma dyes eggs with onion.'),
        ('basket', 'košara', 'f', 'Pisanice idu u košaru.', 'The eggs go in the basket.'),
    ]),
    (18, '2027-05-16', 'CSOB Tjedan 18 · Velika utrka + Tin u utrci', 'W18_CSOB-T1-T3_Velika-utrka_handout.pdf + W18_CSOB-T1_Tin-u-utrci_handout.pdf', [
        ('race', 'utrka', 'f', 'Naša utrka ima pet postaja.', 'Our race has five stations.'),
        ('task', 'zadatak', 'm', 'Svaki zadatak nosi deset bodova.', 'Each task is worth ten points.'),
        ('entrance ticket', 'ulaznica', 'f', 'Ulaznica za muzej stoji dva eura.', 'A museum ticket costs two euros.'),
        ('finish line / goal', 'cilj', 'm', 'Cilj je ispred školske ploče.', 'The finish line is in front of the blackboard.'),
        ('winner', 'pobjednik', 'ma', 'Pobjednik dobiva zlatni licitar.', 'The winner gets a golden licitar.'),
        ('help', 'pomoć', 'f', 'Smijem li zvati prijatelja u pomoć?', 'May I call a friend for help?'),
        ('together', 'zajedno', '', 'Lakše je kad radimo zajedno.', "It's easier when we work together."),
        ('fast / quickly', 'brzo', '', 'Trči brzo, vrijeme istječe!', 'Run fast, time is running out!'),
        ('please', 'molim', '', 'Jedan sok, molim.', 'One juice, please.'),
        ('where', 'gdje', '', 'Gdje je muzej?', 'Where is the museum?'),
    ]),
]
CSOB_EX = {}
for wk, _date, title, files, rows in CSOB:
    H.append((f"csob{wk:02d}", title, files, [(e, hr, g) for e, hr, g, _x, _xe in rows]))
    for e, hr, g, ex, exe in rows:
        if ex:
            CSOB_EX.setdefault(hr, f"{ex} ({exe})" if exe else ex)
# <<< CSOB


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
        cid = f"ho-{hid}-{slug(hr)}"
        if hid == "prep" and hr in LEGACY_SHORT:  # moved from Kratke riječi: keep the card id devices already have
            cid = f"ho-short-{slug(hr)}"
        c = {"id": cid, "hr": hr, "en": en, "ho": [hid], "gram": gram(g), "_g": g}
        by_hr[k] = c
        cards.append(c)

titles = {h[0]: h[1] for h in H}
out_cards = []
for c in cards:
    g = c.pop("_g")
    kind = ("noun, " + GLABEL[g[0]] + (", plural only" if g.endswith("pl") else "")) if g and not g.startswith("adj") else ("adjective" if g else "")
    kind = kind or VERB_NOTE.get(c["hr"], "") or PREP_NOTE.get(c["hr"], "")
    note = "Handout: " + " · ".join(titles[h] for h in c["ho"]) + (("\n" + kind) if kind else "")
    if "time" in c["ho"] and VR_NOTE.get(c["hr"]):   # usage line from the Vrijeme guide
        note += "\n" + VR_NOTE[c["hr"]]
    if any(h.startswith("csob") for h in c["ho"]) and CSOB_EX.get(c["hr"]):   # example sentence from the CSOB site
        note += "\n" + CSOB_EX[c["hr"]]
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

# Two more Lupi petama words (2026-11-12): the noun "a hug" next to the verb, and the female dove of peace.
TS_L8 = 1794528000000  # 2026-11-12
for en, hr, g, kind, forms, ex in [
    ("a hug / an embrace", "zagrljaj", "m", "noun, masculine (inanimate)", "Acc. sg. zagrljaj · Pl. zagrljaji · Verb: zagrliti", "Daj mi zagrljaj!"),
    ("dove (female) / dove of peace", "golubica", "f", "noun, feminine, animate", "Acc. sg. golubicu · Pl. golubice · golubica mira = dove of peace", "Golubica mira je bijela."),
]:
    gr = gram(g); gr["at"] = TS_L8
    out_cards.append({"id": f"tl-{lid}-{slug(hr)}", "hr": hr, "en": en,
                      "note": f"{tag}\nWorksheet: {sheet}\n{kind}\n{forms}\n{ex}",
                      "level": 1, "due": 0, "createdAt": TS_L8, "updatedAt": TS_L8,
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

# v4: the whole Tako lako book list (tako-lako-all.json, the old iCloud export) is built in too,
# so every device gets every word without loading a file. Ids are kept, so progress on a device carries on.
import vocab_categories as VC
book = []
for c in json.load(open("tako-lako-all.json"))["cards"]:
    if c.get("deleted") or not c.get("hr"):
        continue
    b = {"id": c["id"], "hr": c["hr"], "en": c["en"], "note": c.get("note", ""),
         "level": 1, "due": 0, "createdAt": c.get("createdAt", TS), "updatedAt": c.get("updatedAt", TS),
         "lastReviewed": 0, "deleted": False}
    if c.get("gram"):
        b["gram"] = c["gram"]
    book.append(b)
have = {c["id"] for c in book}
out_cards = book + [c for c in out_cards if c["id"] not in have]   # book first: on a new device it wins a tie

# One category per Croatian word, decided from everything known about it (all cards with that word).
LT = re.compile(r"U(\d+)\s*·\s*M(\d+)\s*·\s*Lesson\s*(\d+)"); PBT = re.compile(r"U(\d+)\s*·\s*Phrases")
TPT = re.compile(r"topic:\s*([^\n]+)")
info = {}
for c in out_cards:
    i = info.setdefault(norm(c["hr"]), {"hr": c["hr"], "en": [], "pos": set(), "ho": set(), "les": set(), "top": set()})
    i["en"] += [e for e in c["en"].split(" / ") if e not in i["en"]]
    i["pos"].add((c.get("gram") or {}).get("pos")); i["ho"] |= set(c.get("ho", []))
    i["les"] |= {f"{a}.{b}.{d}" for a, b, d in LT.findall(c["note"])} | {f"{a}.PB" for a in PBT.findall(c["note"])}
    i["top"] |= {t.strip() for t in TPT.findall(c["note"])}
cat_of = {k: VC.categorize(i["hr"], " / ".join(i["en"]), sorted(p for p in i["pos"] if p), sorted(i["ho"]), sorted(i["les"]), sorted(i["top"]))
          for k, i in info.items()}
for c in out_cards:
    c["cat"] = cat_of[norm(c["hr"])]

ids = [c["id"] for c in out_cards]
assert len(ids) == len(set(ids)), "duplicate ids"
data = {"app": "prevoditelj", "kind": "vocabulary", "version": 2, "savedAt": TS,
        "source": "Tako lako book lists + CSOB weeks + Claude-made reference handouts (Taka Lako Class)",
        "handouts": [{"id": h[0], "title": h[1], "file": h[2]} for h in H],
        "categories": [{"id": c, "title": t} for c, t in VC.CATS],
        "cards": out_cards}
json.dump(data, open("handouts.json", "w"), ensure_ascii=False, separators=(",", ":"))
for h in H:
    print(h[0], sum(h[0] in c.get("ho", []) for c in out_cards))
print("lesson cards", sum("ho" not in c for c in out_cards))
print("total cards", len(out_cards))
import collections
print("categories", collections.Counter(cat_of.values()).most_common())
print([ (c["hr"], c["en"]) for c in out_cards if len(c.get("ho", [])) > 1])
