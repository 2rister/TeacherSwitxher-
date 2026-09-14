# -*- coding: utf-8 -*-
"""Reading + practice for the collocations on the classroom poster
"Talk About Remarkable People" (columns 1 and 2, with column 3 used for output).

The reading is a NEW text written so that every target phrase appears in a true
sentence. Nothing here is invented to fit a collocation: where the poster's
example would have been false, the phrase keeps its shape and takes the real
fact ("to be born in 1920" -> "was born in 1533", "to die at the age of 80" ->
"died at the age of 69"). Facts checked 13-14.09.2026 against the pack's own
verified texts and, for the two new claims, against Wikipedia:

  * The Beatles were appointed MBE by Queen Elizabeth II in June 1965
    ("The Beatles"), which is the true instance of "to win an award".
  * Diana was born into the Spencer family, her father Viscount Althorp and
    later Earl Spencer ("Diana, Princess of Wales"), which is the true
    instance of "to come from a wealthy family".

Ages at death are arithmetic from dates already verified in the pack:
Elizabeth 69, Nelson 47, Lennon 40, Diana 36, Newton 84.

Four of the poster's phrases are VALUE JUDGEMENTS, not facts - "an influential
leader", "an inspiring leader", "a remarkable person", "to change the course of
history". The sheet marks them and the teacher's key says why: the intensive's
question is what makes a person great, and a student who writes "she was an
influential leader" without evidence has answered nothing.
"""

TITLE = "Talk About Remarkable People"
STRAP = "Five short lives &#183; the phrases you need to describe them"

# --------------------------------------------------------------- the reading
# (heading, paragraph)
READING = [
    ("Elizabeth I &#183; 1533&#8211;1603",
     "Elizabeth I <b>was born in 1533</b> and <b>came from a royal family</b>: her father "
     "was King Henry VIII. She <b>received a very good education</b> at Hatfield Palace, and "
     "by the age of thirteen she spoke several languages. She became queen in 1558 and never "
     "married, because she wanted to keep the power herself. Many people say that this "
     "<b>influential leader</b> <b>changed the course of English history</b>. She "
     "<b>died at the age of 69</b>."),
    ("Horatio Nelson &#183; 1758&#8211;1805",
     "Horatio Nelson <b>was born in 1758</b> and <b>grew up in a small village</b> in England. "
     "He joined the navy when he was twelve and <b>took part in many important battles</b> at "
     "sea. He lost the sight in one eye, and then he lost his right arm, but he went back to "
     "his ship. At Trafalgar in 1805 he <b>made history</b>: the British won, but Nelson "
     "<b>died at the age of 47</b>. For many people he is still <b>an inspiring leader</b>."),
    ("John Lennon &#183; 1940&#8211;1980",
     "John Lennon <b>was born in 1940</b> in Liverpool, and his aunt Mimi brought him up. In "
     "1956 he formed his first band, and later that band became the Beatles. The group "
     "<b>achieved great success</b> all over the world, and in 1965 they <b>won an award</b>: "
     "the Queen made all four of them Members of the Order of the British Empire. Lennon also "
     "<b>played an important role in the peace movement</b>, and he <b>is remembered for his "
     "songs</b>. He <b>died at the age of 40</b>."),
    ("Princess Diana &#183; 1961&#8211;1997",
     "Diana Spencer <b>was born in 1961</b> and <b>came from an old, rich family</b> &#8211; her "
     "father was an earl. She <b>did not study at university</b>. In 1981 she married Prince "
     "Charles and became <b>a prominent figure</b> all over the world. She visited hospitals, "
     "helped people with HIV/AIDS and worked to stop landmines, so she <b>had a strong "
     "influence on society</b>. She <b>died at the age of 36</b>, and people "
     "<b>remember her for her charity work</b>."),
    ("Isaac Newton &#183; 1642&#8211;1727",
     "Isaac Newton <b>was born in 1642</b> on a farm in England. He <b>studied at university</b> "
     "in Cambridge, and there he <b>made an important contribution to science</b>. He "
     "<b>made a discovery</b> about light: white light is a mixture of all the colours. Today "
     "he is <b>best known for his discovery</b> of gravity, and every school book calls him "
     "<b>an outstanding scientist</b>. He <b>died at the age of 84</b>."),
]

GLOSSARY = [
    ("a figure", "an important person that many people know about"),
    ("outstanding", "much better than the others"),
    ("influential", "able to change what other people think or do"),
    ("to achieve", "to get something after working for it"),
    ("a contribution", "something useful that you add to a piece of work"),
    ("an award", "a prize or an honour that somebody gives you"),
    ("a movement", "a group of people who work together for one idea"),
    ("society", "all the people of a country, taken together"),
]

# ------------------------------------------------------- task 1: find and scan
# (phrase in the infinitive, paragraph number where it appears)
FIND = [
    ("to grow up in a small village", 2),
    ("to come from an old, rich family", 4),
    ("to receive a very good education", 1),
    ("to study at university in Cambridge", 5),
    ("to achieve great success", 3),
    ("to win an award", 3),
    ("to take part in many important battles", 2),
    ("to make an important contribution to science", 5),
    ("to have a strong influence on society", 4),
    ("to change the course of English history", 1),
]

# ----------------------------------------------------------- task 2: who is it
# E = Elizabeth I · N = Nelson · L = Lennon · D = Diana · I = Isaac Newton
WHO = [
    ("This person was an influential leader who never married.", "E"),
    ("This person was an inspiring leader at sea.", "N"),
    ("This person was a talented musician who formed a band in 1956.", "L"),
    ("This person was an outstanding scientist.", "I"),
    ("This person was a prominent figure and did a lot of charity work.", "D"),
    ("This person was a historical figure who died at the age of 47.", "N"),
    ("This person is best known for a discovery about gravity.", "I"),
    ("This person played an important role in the peace movement.", "L"),
]
WHO_LEGEND = ("E = Elizabeth I &#183; N = Nelson &#183; L = Lennon &#183; "
              "D = Diana &#183; I = Isaac Newton")

# ------------------------------------------------- task 3: build the phrase
# adjective half -> noun half; the right column is shuffled by the build
NOUN_PAIRS = [
    ("an influential &#8230;", "leader"),
    ("an outstanding &#8230;", "scientist"),
    ("a prominent &#8230;", "figure"),
    ("a talented &#8230;", "musician"),
    ("a well-known &#8230;", "writer"),
    ("a successful &#8230;", "explorer"),
    ("a respected &#8230;", "politician"),
    ("a remarkable &#8230;", "person"),
]

# --------------------------------------------------- task 4: the missing verb
VERB_BANK = ["achieved", "died", "had", "made", "played", "received", "took", "won"]
VERB_GAPS = [
    ("Nelson grew up in a small village and ____________ part in many important battles.",
     "took"),
    ("Elizabeth ____________ a very good education at Hatfield Palace.", "received"),
    ("The Beatles ____________ great success all over the world.", "achieved"),
    ("In 1965 the group ____________ an award from the Queen.", "won"),
    ("Newton ____________ an important contribution to science.", "made"),
    ("Diana ____________ a strong influence on society.", "had"),
    ("Lennon ____________ an important role in the peace movement.", "played"),
    ("Nelson ____________ at the age of 47.", "died"),
]

# ----------------------------------------------------- task 5: fact or opinion
FACT_OPINION = [
    ("Newton died at the age of 84.", "FACT"),
    ("Newton was an outstanding scientist.", "OPINION"),
    ("Elizabeth was queen for 44 years.", "FACT"),
    ("Elizabeth changed the course of English history.", "OPINION"),
    ("Nelson lost his right arm.", "FACT"),
    ("Nelson was an inspiring leader.", "OPINION"),
]

# ------------------------------------------------------- task 6: your own hero
STARTERS = [
    "He / She was a prominent figure in &#8230;",
    "He / She was born in &#8230; and grew up &#8230;",
    "He / She became famous for &#8230;",
    "He / She made an important contribution to &#8230;",
    "One of his / her greatest achievements was &#8230;",
    "He / She is remembered for &#8230;",
]
WRITE_RULE = ("Write six sentences about <b>your</b> person. Use a different phrase from "
              "tasks 3 and 4 in each one. After every opinion write <i>because</i> and "
              "one fact.")

TEACHER_NOTE = (
    "Four of the poster&#8217;s phrases are not facts at all. <i>An influential leader</i>, "
    "<i>an inspiring leader</i>, <i>a remarkable person</i> and <i>to change the course of "
    "history</i> are judgements: somebody decided them. A student who writes &#8220;she was "
    "an influential leader&#8221; and stops has said nothing that can be argued with &#8211; and "
    "argued with is exactly what the intensive asks of them. Task 5 puts this in front of "
    "them; task 6 makes them pay for every opinion with a fact. If you cut anything on this "
    "sheet, do not cut those two."
)

SOURCE_NOTE = (
    "The text is new, but no fact in it is. Dates, places and events come from the reading "
    "sheets in this pack, which were checked before they were printed. Two facts are used "
    "here for the first time and were checked against Wikipedia on 14.09.2026: the Queen "
    "appointed all four Beatles MBE in June 1965 (&#8220;The Beatles&#8221;), and Diana was born "
    "into the Spencer family, her father Viscount Althorp and later Earl Spencer "
    "(&#8220;Diana, Princess of Wales&#8221;). The ages at death are arithmetic from dates "
    "already in the pack: 69, 47, 40, 36 and 84."
)
