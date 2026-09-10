# -*- coding: utf-8 -*-
"""Past Simple exercises built on the same three people.

These do NOT follow the reading texts — they are free-standing grammar practice.
Every fact was checked against the subject's Wikipedia article before use
(2026-09-10). Two widely repeated Diana stories could not be confirmed there —
the ungloved handshake with an AIDS patient in 1987, and the walk through the
Angolan minefield in 1997 — so neither appears here; only the general facts
("she helped people with HIV/AIDS", "she spoke about landmines") are used.

Newton's father is deliberately never mentioned: the teacher's reading text says
he died shortly AFTER Isaac was born, the historical record says three months
BEFORE, and a grammar item resting on that would quietly contradict Sheet I.

Item format
  mc      (sentence with ____ , [option a, option b, option c], index of the key)
  bracket (sentence with __________ (verb) , answer or [answers] left to right)
"""

NEWTON = dict(
    slug="newton", num="VII", name="Isaac Newton", dates="1642 – 1727",
    portrait="newton-thumb.jpg",
    mc=[
        ("Isaac Newton ____ born in England in 1642.", ["is", "was", "were"], 1),
        ("He ____ mathematics at Trinity College, Cambridge.", ["studied", "studyed", "study"], 0),
        ("Newton ____ like farming.", ["wasn&#8217;t", "didn&#8217;t", "doesn&#8217;t"], 1),
        ("In 1668 he ____ the first reflecting telescope.", ["build", "builded", "built"], 2),
        ("____ Newton write the Principia in Latin?", ["Did", "Was", "Does"], 0),
        ("He ____ the Principia in 1687.", ["writed", "wrote", "written"], 1),
        ("Newton ____ President of the Royal Society in 1703.", ["become", "becomed", "became"], 2),
        ("Queen Anne ____ him a knight in 1705.", ["made", "maked", "make"], 0),
        ("____ he interested in light and colours?", ["Did", "Was", "Were"], 1),
        ("Where ____ Newton study?", ["was", "did", "does"], 1),
        ("Newton ____ in London in 1727.", ["die", "died", "was died"], 1),
        ("People ____ him in Westminster Abbey.", ["buried", "buryed", "bury"], 0),
    ],
    bracket=[
        ("Isaac Newton __________ (be) born in Lincolnshire, England.", "was"),
        ("He __________ (study) at Trinity College, Cambridge.", "studied"),
        ("Newton __________ (not / like) farming.", "did not like / didn&#8217;t like"),
        ("In 1668 he __________ (build) the first reflecting telescope.", "built"),
        ("He __________ (write) the Principia in Latin.", "wrote"),
        ("__________ (he / become) President of the Royal Society in 1703?", "Did he become"),
        ("Queen Anne __________ (make) him a knight in 1705.", "made"),
        ("Newton __________ (not / publish) the Principia in English.",
         "did not publish / didn&#8217;t publish"),
        ("When __________ (Newton / die)?", "did Newton die"),
        ("People __________ (bury) him in Westminster Abbey.", "buried"),
    ],
)

LENNON = dict(
    slug="lennon", num="VIII", name="John Lennon", dates="1940 – 1980",
    portrait="lennon-thumb.jpg",
    mc=[
        ("John Lennon ____ born in Liverpool in 1940.", ["were", "was", "is"], 1),
        ("He ____ his first band, The Quarrymen, in 1956.", ["formed", "formd", "form"], 0),
        ("John ____ Paul McCartney in 1957.", ["meeted", "met", "meet"], 1),
        ("____ the Beatles come from Liverpool?", ["Was", "Did", "Do"], 1),
        ("The Beatles ____ to the United States in 1964.", ["go", "goed", "went"], 2),
        ("John ____ Yoko Ono in 1969.", ["marryed", "married", "marry"], 1),
        ("He ____ to New York in 1971.", ["moved", "moven", "move"], 0),
        ("The Beatles ____ stay together after 1970.", ["weren&#8217;t", "didn&#8217;t", "don&#8217;t"], 1),
        ("When ____ John write &#8220;Imagine&#8221;?", ["did", "was", "does"], 0),
        ("He ____ a lot of songs about peace.", ["singed", "sang", "sung"], 1),
        ("____ John and Yoko famous?", ["Did", "Was", "Were"], 2),
        ("John Lennon ____ in New York in 1980.", ["die", "died", "was died"], 1),
    ],
    bracket=[
        ("John Lennon __________ (be) born in Liverpool.", "was"),
        ("In 1956 he __________ (form) a band called The Quarrymen.", "formed"),
        ("He __________ (meet) Paul McCartney in 1957.", "met"),
        ("John __________ (study) at Liverpool College of Art.", "studied"),
        ("The Beatles __________ (go) to the United States in 1964.", "went"),
        ("__________ (John / marry) Yoko Ono in 1969?", "Did John marry"),
        ("He __________ (move) to New York in 1971.", "moved"),
        ("The Beatles __________ (not / stay) together after 1970.",
         "did not stay / didn&#8217;t stay"),
        ("Where __________ (John / live) after 1971?", "did John live"),
        ("John and Yoko __________ (be) famous all over the world.", "were"),
    ],
)

DIANA = dict(
    slug="diana", num="IX", name="Princess Diana", dates="1961 – 1997",
    portrait="diana-thumb.jpg",
    mc=[
        ("Diana ____ born on 1 July 1961.", ["were", "was", "is"], 1),
        ("Before her marriage she ____ in a nursery school in London.",
         ["worked", "workd", "work"], 0),
        ("She ____ Prince Charles in 1981.", ["marry", "marryed", "married"], 2),
        ("She ____ two sons, William and Harry.", ["haved", "has", "had"], 2),
        ("Diana ____ go to university.", ["wasn&#8217;t", "didn&#8217;t", "doesn&#8217;t"], 1),
        ("____ Diana marry Prince Charles in 1981?", ["Was", "Does", "Did"], 2),
        ("She ____ many hospitals and helped sick children.", ["visited", "visitted", "visit"], 0),
        ("Diana and Charles ____ in 1996.", ["divorce", "divorcd", "divorced"], 2),
        ("Where ____ Diana work before her marriage?", ["was", "did", "does"], 1),
        ("She ____ about important problems on television.", ["spoke", "speaked", "speak"], 0),
        ("____ William and Harry her sons?", ["Was", "Were", "Did"], 1),
        ("Diana ____ in Paris in 1997.", ["die", "died", "was died"], 1),
    ],
    bracket=[
        ("Diana Frances Spencer __________ (be) born in 1961.", "was"),
        ("She __________ (work) with young children in London.", "worked"),
        ("Diana __________ (marry) Prince Charles in 1981.", "married"),
        ("Many people around the world __________ (watch) her wedding on television.", "watched"),
        ("William and Harry __________ (be) her two sons.", "were"),
        ("Diana __________ (not / go) to university.", "did not go / didn&#8217;t go"),
        ("__________ (she / help) people with HIV/AIDS?", "Did she help"),
        ("She __________ (speak) about landmines.", "spoke"),
        ("Where __________ (Diana / work) before her marriage?", "did Diana work"),
        ("Diana __________ (not / work) in a hospital, but she __________ (visit) many.",
         ["did not work / didn&#8217;t work", "visited"]),
    ],
)

GRAMMAR_PEOPLE = [NEWTON, LENNON, DIANA]

# -------------------------------------------------- Sheet X: all three together
MIXED = dict(
    slug="mixed", num="X", name="All Three Together", dates="Newton · Lennon · Diana",
    mc=[
        ("Isaac Newton ____ born in 1642, and John Lennon ____ born in 1940.",
         ["was / was", "were / was", "was / were"], 0),
        ("Diana ____ Prince Charles in 1981.", ["marry", "married", "marryed"], 1),
        ("____ Newton study at Cambridge?", ["Was", "Does", "Did"], 2),
        ("The Beatles ____ to the United States in 1964.", ["went", "goed", "go"], 0),
        ("Newton ____ the Principia in English.",
         ["wasn&#8217;t write", "didn&#8217;t write", "didn&#8217;t wrote"], 1),
        ("Where ____ Diana work before her marriage?", ["did", "was", "does"], 0),
        ("John Lennon ____ to New York in 1971.", ["move", "moven", "moved"], 2),
        ("Queen Anne ____ Newton a knight in 1705.", ["make", "maked", "made"], 2),
        ("____ William and Harry Diana&#8217;s sons?", ["Was", "Were", "Did"], 1),
        ("Diana ____ go to university.", ["didn&#8217;t", "wasn&#8217;t", "doesn&#8217;t"], 0),
        ("John Lennon ____ Paul McCartney in 1957.", ["meeted", "met", "meet"], 1),
        ("Newton ____ President of the Royal Society in 1703.", ["became", "becomed", "become"], 0),
        ("When ____ John Lennon die?", ["was", "does", "did"], 2),
        ("Diana and Charles ____ in 1996.", ["divorce", "divorced", "divorcd"], 1),
        ("All three people ____ famous in Britain.", ["was", "were", "did"], 1),
    ],
    bracket=[
        ("Isaac Newton __________ (be) born in England in 1642.", "was"),
        ("John Lennon and Paul McCartney __________ (meet) in 1957.", "met"),
        ("Diana __________ (work) with children before she __________ (marry) Prince Charles.",
         ["worked", "married"]),
        ("Newton __________ (not / write) the Principia in English.",
         "did not write / didn&#8217;t write"),
        ("__________ (the Beatles / go) to the United States in 1964?", "Did the Beatles go"),
        ("Queen Anne __________ (make) Newton a knight in 1705.", "made"),
        ("William and Harry __________ (be) Diana&#8217;s two sons.", "were"),
        ("John Lennon __________ (move) to New York in 1971.", "moved"),
        ("When __________ (Diana / die)?", "did Diana die"),
        ("Diana __________ (not / go) to university.", "did not go / didn&#8217;t go"),
        ("Newton __________ (build) the first reflecting telescope in 1668.", "built"),
        ("All three people __________ (become) famous around the world.", "became"),
    ],
)

# Word order in Past Simple questions. The scrambled set always contains exactly
# one grammatical arrangement, so each item has a single correct answer.
WORD_ORDER = [
    ("born / when / Newton / was / ?", "When was Newton born?"),
    ("did / where / Diana / work / ?", "Where did Diana work?"),
    ("Lennon / did / meet / who / in 1957 / ?", "Who did Lennon meet in 1957?"),
    ("the Beatles / did / go / to the United States / when / ?",
     "When did the Beatles go to the United States?"),
    ("Diana&#8217;s / were / who / sons / ?", "Who were Diana&#8217;s sons?"),
    ("Newton / did / write / what / in 1687 / ?", "What did Newton write in 1687?"),
]

# Every irregular verb that the four grammar sheets actually use.
IRREGULAR = [
    ("be", "was / were"), ("become", "became"), ("build", "built"), ("go", "went"),
    ("have", "had"), ("make", "made"), ("meet", "met"), ("sing", "sang"),
    ("speak", "spoke"), ("write", "wrote"),
]

GRAMMAR_NOTE = (
    "These sheets do not follow the reading texts &#8211; they are free-standing Past Simple "
    "practice about the same three people, so they can be used before, after or without "
    "Sheets I&#8211;V. Every fact was checked against the subject&#8217;s Wikipedia article. "
    "Where a well-known story could not be confirmed there &#8211; Diana&#8217;s ungloved handshake "
    "with an AIDS patient, her walk through the Angolan minefield &#8211; it was left out, and only "
    "the general facts are used. Newton&#8217;s father is never mentioned: the reading text and the "
    "historical record disagree about when he died, and a grammar item resting on that would "
    "quietly contradict Sheet I."
)
