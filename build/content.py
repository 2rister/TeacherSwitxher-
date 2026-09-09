# -*- coding: utf-8 -*-
"""Reading texts and exercises for the 'Interesting People' A2 pack.

Reading texts are reproduced from the teacher's own materials, verbatim.
Every exercise item is anchored to a fact that appears on the Jeopardy board
(Jeopardy_Interesting_People_A2_interactive.pptx), so the handouts and the
game test exactly the same knowledge.
"""

# ---------------------------------------------------------------- Isaac Newton
NEWTON = dict(
    slug="isaac-newton", num="I", name="Isaac Newton", dates="1642 – 1727",
    tagline="The man who never stopped looking",
    strap="Scientist · Mathematician · Astronomer",
    portrait="newton.png",
    text=[
        "Isaac Newton was born on December 25, 1642, in England. His childhood was difficult. "
        "His father died shortly after he was born. His mother remarried and left him with his "
        "grandmother, Marjorie. Newton lived on a boring farm and spent most of his time alone.",

        "His grandmother wanted him to be a farmer and take care of pigs. But Newton was not "
        "interested in farming. He preferred to watch the rain, the wind, and the grass. His "
        "grandmother did not like his &#8220;observation.&#8221; When he was 12, his mother and "
        "grandmother sent him to school. He stayed at the house of a pharmacist, Mr. Clark. There "
        "he discovered a library with books on chemistry, mathematics, and astronomy. He read many "
        "of them and learned a lot.",

        "After a few years, his mother took him away from school to work on the farm again. One "
        "day, he had to guard the pigs, but he was not paying attention. He was thinking about "
        "nature and the books he had read. The pigs escaped and destroyed the crops. After this "
        "failure, his uncle William convinced his mother to send Newton to Cambridge University.",

        "At Cambridge, Newton had to work as a servant to pay for his studies. He cleaned rooms "
        "and swept stairs, but he did not care. He read all the important science books of that time.",

        "In 1665, something terrible happened. The plague arrived in London from ships. Thousands "
        "of people died every day. Newton left Cambridge and returned to his family&#8217;s farm. "
        "The village was safer and cleaner. There, he had time to think and observe nature again. "
        "During this time, he made his most important discoveries.",

        "First, he experimented with light and colors. He bought a glass pyramid called a prism. "
        "He let a single ray of sunlight pass through it. The white light became a rainbow of many "
        "colors. He proved that white light is a combination of all colors. He also built the best "
        "telescope of his time, and the King of England congratulated him.",

        "Then came his most famous idea. One day, in the garden, he saw an apple fall from a tree. "
        "He asked himself: &#8220;Why do objects fall to the ground? Is there a force that pulls "
        "them?&#8221; After many calculations and experiments, he discovered the force of gravity. "
        "He understood that the Earth attracts all objects. The apple falls because of gravity. But "
        "gravity does not work only on Earth. All bodies in the universe attract each other. The "
        "planets stay in orbit around the Sun because of gravity. The Moon attracts water in our "
        "oceans and creates tides. Gravity is like a string that holds the planets in their places.",

        "Newton created three important laws of motion. With these laws and the law of gravity, he "
        "could explain how any object moves. He became the most famous scientist in the world, "
        "admired by kings and queens. He continued to observe nature and kept a telescope on his roof.",

        "Today, his formulas help us build cars, bridges, and rockets for space travel. Newton said: "
        "&#8220;Remember me and my apple.&#8221; His story is the story of a man who never stopped "
        "looking and thinking.",
    ],
    pull="Remember me and my apple.",
    tf=[  # (statement, answer)
        ("Newton&#8217;s father died before Newton was born.", "F"),
        ("Newton&#8217;s grandmother wanted him to become a farmer.", "T"),
        ("Newton enjoyed taking care of the pigs.", "F"),
        ("At Mr. Clark&#8217;s house Newton found a library with science books.", "T"),
        ("Newton&#8217;s uncle William was a teacher at Cambridge University.", "NG"),
        ("Newton worked as a servant to pay for his studies.", "T"),
        ("Newton left Cambridge in 1665 because of the plague.", "T"),
        ("Newton proved that white light is made of only three colors.", "F"),
    ],
    bank=["apple", "gravity", "motion", "plague", "prism", "pigs", "servant", "telescope"],
    gaps=[
        ("Newton&#8217;s grandmother wanted him to take care of ____________ .", "pigs"),
        ("At Cambridge, Newton worked as a ____________ to pay for his studies.", "servant"),
        ("In 1665 the ____________ arrived in London from ships.", "plague"),
        ("He used a glass ____________ to turn white light into a rainbow.", "prism"),
        ("Newton built the best ____________ of his time.", "telescope"),
        ("In the garden he saw an ____________ fall from a tree.", "apple"),
        ("After many experiments he discovered the force of ____________ .", "gravity"),
        ("Newton created three important laws of ____________ .", "motion"),
    ],
    qs=[
        ("Where did Newton live when he was 12?",
         "At the house of a pharmacist, Mr. Clark."),
        ("What happened to the pigs when Newton was not paying attention?",
         "They escaped and destroyed the crops."),
        ("Who convinced Newton&#8217;s mother to send him to Cambridge?",
         "His uncle William."),
        ("What did Newton prove about white light?",
         "That it is a combination of all colors."),
        ("Why do the planets stay in orbit around the Sun?",
         "Because of gravity."),
        ("What did Newton keep on the roof of his house?",
         "A telescope."),
    ],
    match=[  # (first half, correct second half)
        ("Newton&#8217;s mother took him away from school", "to work on the family farm again."),
        ("Newton was thinking about nature instead of watching the pigs,", "so they escaped and destroyed the crops."),
        ("A single ray of sunlight passed through the prism", "and became a rainbow of many colors."),
        ("The Moon attracts the water in our oceans", "and creates the tides."),
        ("Today Newton&#8217;s formulas help engineers", "build cars, bridges and rockets."),
    ],
    jeopardy=[
        (400, "Who lived with his grandmother when he was a child?", "Isaac Newton."),
        (600, "What did Newton create to explain how objects move?", "Three laws of motion."),
        (700, "What did Newton do at Cambridge to pay for his studies?", "He worked as a servant."),
    ],
)

# ----------------------------------------------------------------- John Lennon
LENNON = dict(
    slug="john-lennon", num="II", name="John Lennon", dates="1940 – 1980",
    tagline="A voice for peace",
    strap="Musician · Songwriter · Peace activist",
    portrait="lennon.png",
    text=[
        "John Lennon was born on October 9, 1940, in Liverpool, England. It happened during the war. "
        "He was named John Winston after his grandfather and Prime Minister Churchill. John&#8217;s "
        "parents separated, and his strict aunt Mimi raised him.",

        "When John was 15, his mother bought him his first guitar. Before that, he learned to play "
        "the banjo and harmonica. In 1956, he formed his first band, The Quarrymen. Later, this band "
        "became The Beatles. In 1957, John met Paul McCartney at a church party. They became great "
        "friends and wrote songs together.",

        "In the 1960s, The Beatles became very famous all over the world. John sang and played "
        "guitar. In 1962, he married Cynthia Powell. They had a son, Julian.",

        "In 1966, John said that The Beatles were more popular than Jesus. This caused a big scandal. "
        "In 1969, he returned his MBE medal to the Queen. He protested against the Vietnam War.",

        "In 1969, John married for the second time. His wife was artist Yoko Ono. Together, they did "
        "peace actions &#8211; &#8220;bed-ins&#8221; in Amsterdam and Montreal.",

        "In 1970, The Beatles broke up. John started a solo career. His first solo album came out in "
        "1970. In 1971, he recorded his famous song &#8220;Imagine&#8221; about peace.",

        "In the 1970s, John had problems with the American government. President Nixon wanted to send "
        "him out of the USA because of his anti-war views. From 1973 to 1975, John lived apart from "
        "Yoko. This period is called his &#8220;lost weekend.&#8221;",

        "On October 9, 1975, John and Yoko had a son, Sean. It was John&#8217;s birthday on the same "
        "day! After that, John did not work as a musician for five years. He stayed at home and "
        "raised his son.",

        "In 1980, John came back to music with a new album, Double Fantasy. Sadly, on December 8, "
        "1980, a crazy fan killed him outside his home in New York City. But John Lennon will always "
        "stay in people&#8217;s memory as a great musician and a fighter for peace.",
    ],
    pull="A great musician and a fighter for peace.",
    tf=[
        ("John Lennon was born in London.", "F"),
        ("John was raised by his strict aunt Mimi.", "T"),
        ("The guitar was the first instrument John learned to play.", "F"),
        ("John met Paul McCartney at school.", "F"),
        ("Cynthia Powell sang in The Quarrymen.", "NG"),
        ("John returned his MBE medal to the Queen in 1969.", "T"),
        ("John and Yoko did &#8220;bed-ins&#8221; in Amsterdam and Montreal.", "T"),
        ("Sean Lennon was born on his father&#8217;s birthday.", "T"),
    ],
    bank=["Beatles", "guitar", "Imagine", "Liverpool", "peace", "Quarrymen", "Sean", "solo"],
    gaps=[
        ("John Lennon was born in ____________ in 1940.", "Liverpool"),
        ("When John was 15, his mother bought him his first ____________ .", "guitar"),
        ("In 1956 he formed his first band, The ____________ .", "Quarrymen"),
        ("Later this band became The ____________ .", "Beatles"),
        ("After 1970 John started a ____________ career.", "solo"),
        ("In 1971 he recorded his famous song &#8220;____________&#8221; .", "Imagine"),
        ("John and Yoko did &#8220;bed-ins&#8221; for ____________ .", "peace"),
        ("In 1975 John and Yoko had a son, ____________ .", "Sean"),
    ],
    qs=[
        ("Why was John given the name &#8220;Winston&#8221;?",
         "He was named after Prime Minister Churchill."),
        ("Who raised John when his parents separated?",
         "His strict aunt Mimi."),
        ("Where and when did John meet Paul McCartney?",
         "At a church party, in 1957."),
        ("What did John say in 1966 that caused a big scandal?",
         "That The Beatles were more popular than Jesus."),
        ("Why did President Nixon want to send John out of the USA?",
         "Because of his anti-war views."),
        ("What was special about Sean&#8217;s date of birth?",
         "He was born on John&#8217;s birthday, 9 October."),
    ],
    match=[
        ("Before the guitar, John learned to play", "the banjo and the harmonica."),
        ("In 1969 John returned his MBE medal", "to the Queen."),
        ("From 1973 to 1975 John lived apart from Yoko &#8211;", "this period is called his &#8220;lost weekend.&#8221;"),
        ("After Sean was born, John stayed at home", "and did not work as a musician for five years."),
        ("In 1980 John came back to music", "with a new album, Double Fantasy."),
    ],
    jeopardy=[
        (100, "Who was born in Liverpool in 1940?", "John Lennon."),
        (200, "What band did John Lennon help create?", "The Beatles."),
        (500, "What did John Lennon do after The Beatles broke up?", "He started a solo career."),
    ],
)

# ------------------------------------------------------------- Princess Diana
DIANA = dict(
    slug="princess-diana", num="III", name="Princess Diana", dates="1961 – 1997",
    tagline="The People&#8217;s Princess",
    strap="Princess of Wales · Charity worker",
    portrait="diana.png",
    text=[
        "Diana Frances Spencer was born on 1 July 1961 in England. She grew up in a large family "
        "with two older sisters and a younger brother. Her parents divorced when she was young.",

        "Diana was a quiet and shy child. She liked music, dancing and working with children. She "
        "studied in England and Switzerland but did not go to university. Before becoming a "
        "princess, she worked with children in London.",

        "In 1981, Diana married Prince Charles and became the Princess of Wales. They had two sons, "
        "William and Harry. Diana became very popular because she was kind, friendly and open with "
        "ordinary people.",

        "Diana did a lot of charity work. She visited hospitals and helped sick children, homeless "
        "people and people with HIV/AIDS. She also worked to stop the use of landmines. She used her "
        "fame to talk about important problems and help people in need.",

        "Diana died in a car accident in Paris on 31 August 1997. She was 36 years old. People still "
        "remember her for her kindness, courage and charity work. She was often called the "
        "&#8220;People&#8217;s Princess&#8221;. One of her famous quotes is: &#8220;Only do what "
        "your heart tells you.&#8221;",
    ],
    pull="Only do what your heart tells you.",
    tf=[
        ("Diana was born in 1961.", "T"),
        ("Diana was the youngest child in her family.", "F"),
        ("Diana studied at a university in Switzerland.", "F"),
        ("Diana&#8217;s favourite subject at school was history.", "NG"),
        ("Before she married, Diana worked with children in London.", "T"),
        ("Diana and Prince Charles had two sons.", "T"),
        ("Diana worked to stop the use of landmines.", "T"),
        ("Diana was 40 years old when she died.", "F"),
    ],
    bank=["charity", "children", "hospitals", "landmines", "Paris", "People&#8217;s", "shy", "Wales"],
    gaps=[
        ("Diana was a quiet and ____________ child.", "shy"),
        ("In 1981 she married Prince Charles and became the Princess of ____________ .", "Wales"),
        ("Before becoming a princess, she worked with ____________ in London.", "children"),
        ("Diana did a lot of ____________ work.", "charity"),
        ("She visited ____________ and helped sick children.", "hospitals"),
        ("She also worked to stop the use of ____________ .", "landmines"),
        ("Diana died in a car accident in ____________ in 1997.", "Paris"),
        ("People often called her the &#8220;____________ Princess&#8221;.", "People&#8217;s"),
    ],
    qs=[
        ("How many brothers and sisters did Diana have?",
         "Three &#8211; two older sisters and a younger brother."),
        ("What happened to Diana&#8217;s parents when she was young?",
         "They divorced."),
        ("What are the names of Diana&#8217;s two sons?",
         "William and Harry."),
        ("Name two groups of people that Diana helped.",
         "Sick children, homeless people, people with HIV/AIDS (any two)."),
        ("Why did Diana become very popular?",
         "Because she was kind, friendly and open with ordinary people."),
        ("How old was Diana when she died?",
         "She was 36."),
    ],
    match=[
        ("Diana grew up in a large family", "with two older sisters and a younger brother."),
        ("She studied in England and Switzerland,", "but she did not go to university."),
        ("Diana used her fame", "to talk about important problems and help people in need."),
        ("On 31 August 1997 Diana", "died in a car accident in Paris."),
        ("One of her famous quotes is:", "&#8220;Only do what your heart tells you.&#8221;"),
    ],
    jeopardy=[
        (300, "What did Diana do before becoming a princess?", "She worked with children."),
        (500, "Who was a quiet and shy child and liked dancing and music?", "Diana Spencer."),
        (700, "What important work did Diana do for people with serious problems?",
         "She did charity work and helped people in need."),
    ],
)

PEOPLE = [NEWTON, LENNON, DIANA]

# ------------------------------------------------------- Sheet IV: mixed round
# "Who is it?" items are taken straight from the Jeopardy board.
WHO = [
    ("Who was born in Liverpool in 1940?",                         "Lennon"),
    ("Who lived with his grandmother when he was a child?",        "Newton"),
    ("Who was a quiet and shy child and liked dancing and music?", "Diana"),
    ("Who discovered the force of gravity?",                       "Newton"),
    ("Who wrote and recorded the song &#8220;Imagine&#8221;?",     "Lennon"),
    ("Who worked with children before becoming famous?",           "Diana"),
    ("Who worked as a servant at Cambridge University?",           "Newton"),
    ("Who was born on the same day as his son?",                   "Lennon"),
    ("Who became famous for helping people through charity work?", "Diana"),
    ("Who kept a telescope on the roof of the house?",             "Newton"),
]

# Birth years verified against the reading texts; the pack uses the CORRECTED
# order (the game slide 78 lists Elizabeth I in the wrong place).
TIMELINE = [
    ("Princess Diana", 1961), ("Isaac Newton", 1642), ("John Lennon", 1940),
    ("Horatio Nelson", 1758), ("Elizabeth I", 1533),
]
TIMELINE_KEY = ["Elizabeth I", "Isaac Newton", "Horatio Nelson", "John Lennon", "Princess Diana"]

NUMBERS = [
    ("1642", "Isaac Newton was born."),
    ("1665", "The plague came to London and Newton went back to the farm."),
    ("1940", "John Lennon was born in Liverpool."),
    ("1961", "Diana Frances Spencer was born."),
    ("1971", "John Lennon recorded &#8220;Imagine&#8221;."),
    ("1997", "Diana died in a car accident in Paris."),
    ("3",    "The number of Newton&#8217;s laws of motion."),
    ("36",   "Diana&#8217;s age when she died."),
]

# Final Jeopardy (slide 83) + phrase bank from the Debate Toolkit poster.
DEBATE = dict(
    question="Which person showed the most courage &#8211; Newton, Lennon or Diana? "
             "Give one reason and one example from the texts.",
    steps=[("OPINION", "I think that&#8230;"), ("REASON", "This is because&#8230;"),
           ("EXAMPLE", "For example,&#8230;"), ("RESULT", "So,&#8230; / That&#8217;s why&#8230;")],
    phrases=[
        ("SAY YOUR OPINION", ["I think that&#8230;", "In my opinion,&#8230;", "From my point of view,&#8230;"]),
        ("GIVE A REASON",    ["The main reason is&#8230;", "This is because&#8230;", "Another reason is&#8230;"]),
        ("GIVE AN EXAMPLE",  ["For example,&#8230;", "For instance,&#8230;", "A good example is&#8230;"]),
        ("AGREE / DISAGREE", ["I agree because&#8230;", "I see your point, but&#8230;", "That&#8217;s true, but&#8230;"]),
    ],
)

# Discrepancies found while checking the game against the texts and the record.
TEACHER_NOTES = [
    ("Wild Card 600 &#8211; wrong answer on the game slide",
     "The board answers &#8220;Newton &#8594; Nelson &#8594; Elizabeth &#8594; Lennon &#8594; Diana&#8221;. "
     "By year of birth the correct order is Elizabeth I (1533) &#8594; Newton (1642) &#8594; "
     "Nelson (1758) &#8594; Lennon (1940) &#8594; Diana (1961). Task 2 on Sheet IV uses the corrected order."),
    ("Childhood &amp; Early Life 300 &#8211; pronoun mismatch",
     "The slide asks &#8220;Who was raised by <i>her</i> strict aunt Mimi?&#8221; but the answer is John Lennon. "
     "It should read <i>his</i>. Corrected in this pack."),
    ("Newton&#8217;s text &#8211; three points that differ from the historical record",
     "(1) In the text the grandmother wants him to farm; historically it was his mother Hannah who took him "
     "out of school to run the farm. (2) A prism is a triangular <i>prism</i>, not a &#8220;pyramid&#8221;. "
     "(3) Newton&#8217;s reflecting telescope (1671) impressed the <i>Royal Society</i>, which led to his "
     "election as a Fellow; there is no reliable source for the king congratulating him. "
     "The exercises test the text as written, so students are never marked wrong for these."),
    ("Spelling",
     "The Newton text uses American spellings (&#8220;colors&#8221;) while the rest of the pack and the game "
     "use British ones (&#8220;colours&#8221;). Left as in the original. Change it in "
     "<i>build/content.py</i> if you want one convention throughout."),
]

# --------------------------------------------- A2 glossary printed under each text
GLOSSARY = {
    "isaac-newton": [
        ("observation", "watching something very carefully"),
        ("servant", "a person who works in someone else&#8217;s house"),
        ("plague", "a very dangerous illness that spreads quickly"),
        ("prism", "a piece of glass that breaks light into colours"),
        ("gravity", "the force that pulls objects down to the ground"),
        ("orbit", "the path of a planet around the Sun"),
        ("tide", "the rise and fall of the sea"),
        ("crops", "plants that farmers grow for food"),
    ],
    "john-lennon": [
        ("band", "a group of musicians who play together"),
        ("solo career", "working alone, not in a group"),
        ("to protest", "to say publicly that something is wrong"),
        ("scandal", "something that shocks a lot of people"),
        ("album", "a collection of songs"),
        ("to break up", "to stop working together"),
        ("views", "the things a person believes"),
        ("memory", "something that people remember"),
    ],
    "princess-diana": [
        ("shy", "not comfortable with new people"),
        ("charity work", "helping people without being paid"),
        ("homeless", "having nowhere to live"),
        ("landmine", "a bomb hidden under the ground"),
        ("fame", "being known by very many people"),
        ("kindness", "being good and friendly to other people"),
        ("courage", "being brave when something is difficult"),
        ("ordinary people", "normal people, not rich or famous"),
    ],
}
