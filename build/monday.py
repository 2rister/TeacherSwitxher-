# -*- coding: utf-8 -*-
"""Monday 14.09.2026 lesson kit for the Elizabeth I team.

Content only — the sheets themselves are laid out in build.py.

Every historical claim here was checked against the English Wikipedia articles
"Elizabeth I" and "Speech to the Troops at Tilbury" on 2026-09-13. Where the
record is disputed the sheet says so rather than flattening it, because the
lesson's whole question is how we judge a person:

  * The Tilbury speech is accepted as genuine by most historians (Neale,
    Mattingly, Collinson, Weir, Green); a minority (Christy, Barker, Frye)
    doubt it. The audio script quotes it and the teacher note flags the doubt.
  * The teacher's original text said Elizabeth died on 14 March 1603 and
    reigned 45 years. The record says 24 March 1603 and 44 years. The corrected
    figures are used throughout.
  * Two claims in circulation are NOT in the article and are not used anywhere:
    that her white make-up poisoned her, and that Shakespeare was her favourite
    writer. She is documented as loving the theatre; Shakespeare and Marlowe
    are documented as writing in her reign. Those are the claims used.
"""

TITLE = "Monday 14 September &#183; Elizabeth I"

# ---------------------------------------------------------------- the timetable
# left column exactly as the school sent it; right column is the staging
TIMETABLE = [
    ("11.00 &#8211; 11.45", "Revision: your hero + Past Simple", "45 min"),
    ("11.45 &#8211; 12.00", "Break", "15 min"),
    ("12.00 &#8211; 13.35", "Preparing the presentation", "95 min"),
    ("13.35 &#8211; 14.05", "Lunch", "30 min"),
    ("14.05 &#8211; 15.40", "Plenary &#183; presentations &#183; awards", "95 min"),
]

AIMS = [
    "recall the life of Elizabeth I and re-tell it in the Past Simple",
    "listen to a three-minute A2 talk and take the facts out of it",
    "build their own criteria for <b>WHAT MAKES A GREAT PERSON</b> and defend them",
    "find evidence for and against Elizabeth&#8217;s greatness in what she actually did",
    "give a ten-minute team presentation in English with a clear line of argument",
    "judge other teams against the same criteria and vote for the award winners",
]

MATERIALS = [
    ("Sheet [[#elizabeth-i]]", "Elizabeth I &#8211; reading, exercises, board call-backs", "1 per student"),
    ("Sheet [[#grammar-elizabeth-i]]", "Past Simple on Elizabeth I", "1 per student"),
    ("Listening sheet", "&#8220;The Queen Who Said No&#8221; &#8211; worksheet", "1 per student"),
    ("Audio script", "read aloud by the teacher &#8211; keys on the back", "teacher only"),
    ("Great Person sheet", "criteria, evidence grid, the greatness test", "1 per student"),
    ("Presentation kit", "roles, timing plan, sentence frames, checklist", "1 per student"),
    ("Feedback cards", "cut into four &#183; voting slips at the bottom", "1 per student"),
    ("Certificates", "cut in half &#183; fill the names in at lunch", "4 per group"),
    ("Answer keys", "reading key and grammar key from the pack", "teacher only"),
]

# ------------------------------------------------------------------- the stages
# (clock, minutes, what, how, interaction)
STAGE1 = [
    ("11.00", 5, "Warmer &#183; three facts",
     "Books closed. In pairs, write down everything you remember about Elizabeth I in "
     "three minutes. Then count: the pair with the most <i>correct</i> facts wins.", "PAIRS"),
    ("11.05", 10, "Reading recall",
     "Sheet [[#elizabeth-i]], page 2, task 1 (True / False / Not Given). Students may re-read "
     "page 1 first for two minutes, then close it. Check as a class; ask &#8220;which paragraph?&#8221; "
     "every time.", "IND &#8594; CLASS"),
    ("11.15", 13, "Listening &#183; The Queen Who Said No",
     "Listening sheet. Task 1 (words) before you read anything aloud. Read the script once at "
     "normal speed &#8211; students do task 2 only. Read it a second time, slightly slower, pausing "
     "at the ||&nbsp;marks &#8211; students do tasks 3 and 4. Check in pairs, then as a class.", "IND &#8594; PAIRS"),
    ("11.28", 12, "Past Simple",
     "Sheet [[#grammar-elizabeth-i]]. Task 1 (choose a, b or c) against the clock &#8211; six minutes, "
     "then swap sheets and mark. Task 2 (verbs in brackets): items 1&#8211;5 now, 6&#8211;10 as "
     "homework if time is short. Board the three shapes: <b>was/were</b> &#183; <b>-ed / irregular</b> "
     "&#183; <b>did + infinitive</b>.", "IND &#8594; PAIRS"),
    ("11.40", 5, "Set the big question",
     "Write on the board: <b>WHAT MAKES A GREAT PERSON?</b> Each student writes one word that "
     "must be in the answer. Collect the words on the board &#8211; do not discuss them yet. "
     "Tell them these words come back after the break.", "CLASS"),
]

STAGE2 = [
    ("12.00", 12, "My criteria",
     "Great Person sheet, task 1. Alone: tick your five. In the team: agree on <b>three</b> and "
     "write them in the box. The team must be able to say why each one is in and why one "
     "popular word was left out.", "IND &#8594; TEAM"),
    ("12.12", 18, "Evidence hunt",
     "Great Person sheet, task 2. Go back to Sheet [[#elizabeth-i]] and the listening. For each "
     "criterion find something Elizabeth <i>did</i>, with a year. No year, no evidence.", "TEAM"),
    ("12.30", 10, "The greatness test",
     "Great Person sheet, task 3. Four things Elizabeth really did &#8211; two that look great and "
     "two that do not. Rate each one against your own criteria. This is where the presentation "
     "gets its honesty, and it is what separates a report from an argument.", "TEAM"),
    ("12.40", 10, "Roles and the clock",
     "Presentation kit, page 1. Fill in the timing plan with real names. Six roles, ten minutes. "
     "Everybody speaks. Nobody speaks for more than two and a half minutes.", "TEAM"),
    ("12.50", 25, "Write your part",
     "Presentation kit, page 2. Each student drafts their own part using the sentence frames. "
     "Teacher circulates and corrects Past Simple forms only &#8211; leave everything else.", "IND"),
    ("13.15", 15, "Rehearsal 1",
     "Full run with a stopwatch. One student holds the checklist and ticks. Stop at ten minutes "
     "even if they are not finished &#8211; that is the point of the exercise.", "TEAM"),
    ("13.30", 5, "Fix list",
     "Three things to change, written at the bottom of the kit. Not more than three.", "TEAM"),
]

STAGE3 = [
    ("14.05", 5, "Set up",
     "Hand out the feedback cards, one per student, already cut. Explain the three awards and "
     "that everyone votes at the end.", "CLASS"),
    ("14.10", 70, "Presentations",
     "About ten minutes per team plus two minutes of questions. The audience fills in one "
     "feedback card per team. Teacher keeps time visibly and does not interrupt.", "PLENARY"),
    ("15.20", 10, "Voting and counting",
     "Students tear off the three slips and post them. Two students count while the teacher "
     "gives whole-class feedback on the English &#8211; three things that worked, three to fix.", "CLASS"),
    ("15.30", 10, "Awards and close",
     "Read out the certificates. One or two &#8220;most active&#8221; per group, the debate winners and "
     "the winners of the game. Close by reading three of the morning&#8217;s words from the board "
     "and asking whether the day changed anybody&#8217;s answer.", "CLASS"),
]

PLAN_NOTES = [
    ("If you are running late",
     "Cut &#8220;The greatness test&#8221; to five minutes and set task 2 of the grammar sheet as "
     "homework. Do not cut Rehearsal 1 &#8211; an unrehearsed ten minutes always becomes fourteen."),
    ("The difficult sentence in the audio",
     "The script says that Elizabeth&#8217;s father had her mother killed. That is what happened: "
     "Anne Boleyn was beheaded on 19 May 1536, when Elizabeth was two years and eight months old. "
     "Say it plainly, do not dwell on it, and move on to what the child did next &#8211; she studied."),
    ("The Tilbury quotation",
     "&#8220;I know I have the body but of a weak, feeble woman; but I have the heart and stomach "
     "of a king&#8221; &#8211; Tilbury, 9 August 1588. Most historians accept the speech as genuine; "
     "a minority doubt the text. If a student asks whether she really said it, the honest answer "
     "is &#8220;probably, and that is a good question&#8221;."),
    ("Two facts the original class text had wrong",
     "Elizabeth died on <b>24</b> March 1603, not the 14th, and she was queen for <b>44</b> years, "
     "not 45 (17 November 1558 to 24 March 1603). Both are corrected on every sheet in this pack."),
]

# ------------------------------------------------------------- the audio script
# ~310 words; read at about 100 words a minute this runs a little over three
# minutes. || marks a pause for the second, slower reading.
SCRIPT_TITLE = "The Queen Who Said No"
SCRIPT_META = ("A2 &#183; about 310 words &#183; 3 minutes at reading speed &#183; "
               "read twice: once at normal speed, once pausing at ||")

SCRIPT = [
    ("Hello, and welcome to <i>Great Lives</i>. Today: a queen who ruled England for "
     "forty-four years.", True),
    ("Elizabeth was born on the seventh of September, fifteen thirty-three, at Greenwich "
     "Palace, near London. Her father was King Henry the Eighth. Her mother was Anne Boleyn. "
     "When Elizabeth was two years old, her father had her mother killed. People said the "
     "little girl was not a real princess.", True),
    ("But Elizabeth was clever. She studied with a famous teacher, Roger Ascham. She learned "
     "Latin, French and Italian. She read and she read and she read.", True),
    ("Life was not safe. In March fifteen fifty-four her sister Mary sent her to the Tower of "
     "London. Elizabeth stayed in the Tower for about two months. After that she lived in the "
     "country for almost a year, and soldiers watched her door. She was not free.", True),
    ("Everything changed in fifteen fifty-eight. Mary died, and on the seventeenth of November "
     "Elizabeth became queen. She was twenty-five years old. In January fifteen fifty-nine they "
     "crowned her in Westminster Abbey.", True),
    ("Many men wanted to marry her. Kings and princes sent her letters and pictures. Elizabeth "
     "said no. She said no to all of them, and she kept the power herself. Today people call "
     "her the Virgin Queen.", True),
    ("In fifteen eighty-eight the King of Spain sent a great fleet of ships &#8211; the Armada &#8211; "
     "against England. Elizabeth went to Tilbury and spoke to her soldiers. She said: &#8220;I "
     "know I have the body but of a weak, feeble woman; but I have the heart and stomach of a "
     "king.&#8221; The Armada lost.", True),
    ("Elizabeth loved the theatre. In her time William Shakespeare and Christopher Marlowe "
     "wrote their plays, and people still watch them today.", True),
    ("Elizabeth died on the twenty-fourth of March, sixteen oh three, at Richmond Palace. She "
     "was queen for forty-four years. King James of Scotland became the next king of England.", True),
    ("So &#8211; what makes a great person? Think about Elizabeth. She was clever. She was brave. "
     "And she said no.", False),
]

# ------------------------------------------------------- the listening worksheet
L_WORDS = [
    ("a palace", "a very big house where a king or a queen lives"),
    ("a tower", "a tall building &#8211; this one was a prison"),
    ("to crown somebody", "to put a crown on a new king or queen"),
    ("a fleet", "a large group of ships"),
    ("brave", "not afraid of danger"),
    ("power", "when you can decide things and other people must do them"),
    ("free", "when you can go where you want"),
    ("a play", "a story that actors show in a theatre"),
]

# first listening — tick the five the talk really mentions
L_TICK = [
    ("her mother", True),
    ("her horses", False),
    ("the Tower of London", True),
    ("her school in Spain", False),
    ("the ships from Spain", True),
    ("the theatre", True),
    ("her children", False),
    ("the next king", True),
]

L_TF = [
    ("Elizabeth was born in London.", "F"),
    ("Her father was King Henry VIII.", "T"),
    ("She learned three foreign languages.", "T"),
    ("Her sister Mary sent her to the Tower of London.", "T"),
    ("She was twenty-five years old when she became queen.", "T"),
    ("She married a prince from Spain.", "F"),
    ("She wrote a play with Shakespeare.", "NG"),
    ("A king from Scotland became king after her.", "T"),
]

L_NUMBERS = [
    ("1533", "the year Elizabeth was born"),
    ("1554", "the year her sister sent her to the Tower"),
    ("1558", "the year she became queen"),
    ("1588", "the year of the Armada"),
    ("1603", "the year she died"),
    ("44", "the number of years she was queen"),
    ("25", "her age when she became queen"),
]

L_AFTER = [
    "The talk ends with three words about Elizabeth: <i>clever</i>, <i>brave</i>, and "
    "<i>she said no</i>. Which of the three is the most important? Why?",
    "Elizabeth said no to every man who wanted to marry her. Was that a brave choice or a "
    "cold one? Give one reason.",
    "The programme does not say anything bad about Elizabeth. Is that honest? What would you "
    "add to the talk?",
    "Write one sentence: <i>A person is great when &#8230;</i>",
]

# ------------------------------------------- WHAT MAKES A GREAT PERSON? sheet
CRITERIA = [
    "courage &#8211; doing the right thing when it is dangerous",
    "intelligence &#8211; seeing what other people do not see",
    "hard work &#8211; years of it, not one good day",
    "kindness &#8211; caring about people with no power",
    "never giving up",
    "changing other people&#8217;s lives for the better",
    "being honest, also when it costs something",
    "being famous &#8211; everybody knows your name",
    "having power &#8211; you can decide things",
    "being remembered a long time after you die",
]

# task 3 — four things Elizabeth really did. Two read well, two read badly.
GREATNESS_TEST = [
    ("She said no to every marriage and kept the power herself (1558&#8211;1603).",
     "Nobody ruled England through her. But she had no child, and after her death the "
     "crown went to Scotland."),
    ("She sent her ships against the Spanish Armada and spoke to the soldiers herself "
     "at Tilbury (1588).",
     "England won. But the war was expensive, and she was careful with money for her "
     "soldiers afterwards."),
    ("After the rising in the north of England in 1569, more than 750 people were "
     "executed on her orders.",
     "She kept the country quiet. Think about the price."),
    ("From 1581, to make an English person a Catholic was treason, and treason meant death.",
     "She said it was about the state, not about God. Her enemies said it was about God."),
]

DEBATE_MOTION = "Elizabeth I was a great person."

TEACHER_EVIDENCE = (
    "Where the hard numbers in task 3 come from: the 750+ executions after the 1569 Rising "
    "of the North and the 1581 treason law are both stated in the Wikipedia article "
    "&#8220;Elizabeth I&#8221;, which also records that she at first resisted calls for the "
    "execution of Mary, Queen of Scots, signed the warrant in 1586, and afterwards blamed her "
    "secretary for sending it &#8211; and that historians have questioned how sincere that was. "
    "The article also notes that economic and military problems weakened her popularity late "
    "in the reign, and that some historians read her as short-tempered and sometimes "
    "indecisive. None of this is on the reading sheet; it is here so that a team that wants "
    "to argue the hard side can be given something real."
)

# --------------------------------------------------------- the presentation kit
ROLES = [
    ("1", "The Opener", "0:00 &#8211; 0:40",
     "Name the person and ask the big question. No biography yet."),
    ("2", "The Story-teller", "0:40 &#8211; 2:40",
     "Five or six moments of the life, in order, all in the Past Simple, all with years."),
    ("3", "The Evidence-giver", "2:40 &#8211; 5:00",
     "Your three criteria, and one thing Elizabeth did for each one. Year every time."),
    ("4", "The Other Side", "5:00 &#8211; 6:30",
     "What was <i>not</i> great. One or two real examples from the greatness test."),
    ("5", "The Closer", "6:30 &#8211; 8:00",
     "Your team&#8217;s answer to WHAT MAKES A GREAT PERSON, and where Elizabeth lands on it."),
    ("6", "The Question-taker", "8:00 &#8211; 10:00",
     "Take questions from the room. You may ask the rest of the team to help."),
]

FRAMES = [
    ("Opening", [
        "Our person is Elizabeth the First, Queen of England from 1558 to 1603.",
        "Before we begin, one question: what makes a person great?",
        "Today we will give you our answer, and three pieces of evidence.",
    ]),
    ("Telling the story (Past Simple)", [
        "She was born in 1533 at Greenwich Palace.",
        "In 1554 her sister sent her to the Tower of London.",
        "She became queen in 1558, when she was twenty-five.",
        "She did not marry, and she kept the power herself.",
    ]),
    ("Giving evidence", [
        "Our first criterion is courage. In 1588 she &#8230;",
        "This shows that &#8230;",
        "We chose this criterion because &#8230;",
    ]),
    ("The other side", [
        "But not everything was great. In 1569 &#8230;",
        "We have to say honestly that &#8230;",
        "A great person is not a perfect person, and here is why that matters.",
    ]),
    ("Closing", [
        "So our answer is: a person is great when &#8230;",
        "Elizabeth meets two of our three criteria. The third one is harder.",
        "Thank you. We are ready for your questions.",
    ]),
    ("Taking questions", [
        "That is a good question. Can I check &#8211; do you mean &#8230;?",
        "I am not sure about the year. Maria, do you remember?",
        "We did not find that in our text, so I cannot answer it today.",
    ]),
]

CHECKLIST = [
    "Every member of the team speaks.",
    "Nobody speaks for longer than two and a half minutes.",
    "The big question is asked in the first minute.",
    "Every date is said out loud, not only shown.",
    "Every fact about the past is in the Past Simple.",
    "Three criteria, three pieces of evidence, in that order.",
    "At least one honest point against your own person.",
    "The last sentence answers the big question directly.",
    "You finish inside ten minutes.",
    "You look at the room, not at the paper.",
]

# ---------------------------------------------------------------- feedback card
FB_SCORES = [
    "Clear English &#8211; I understood them",
    "Evidence &#8211; facts and years, not opinions",
    "Teamwork &#8211; everybody had a real part",
    "It made me think",
]

FB_OPEN = [
    ("Their answer to the big question was &#8230;", 2),
    ("The best sentence I heard from them", 2),
    ("One thing I would change", 1),
]

VOTES = [
    ("MOST ACTIVE", "the person in my group who worked hardest today"),
    ("DEBATE", "the best arguer of the intensive"),
    ("THE GAME", "the winner of the Jeopardy board"),
]

# ------------------------------------------------------------------ certificates
CERTS = [
    ("MOST ACTIVE PARTICIPANT",
     "for working, speaking and asking more than anybody else",
     "Elizabeth I team"),
    ("MOST ACTIVE PARTICIPANT",
     "for working, speaking and asking more than anybody else",
     "Elizabeth I team"),
    ("CHAMPION OF THE DEBATE",
     "for the best argument of the intensive &#8211; clear, evidenced and fair",
     "Speak &#183; Reason &#183; Persuade &#183; Respect"),
    ("CHAMPION OF THE GAME",
     "for winning the Great Britons Jeopardy board",
     "Interesting People &#183; A2"),
]

CERT_FOOT = "Monday 14 September 2026 &#183; English intensive &#183; WHAT MAKES A GREAT PERSON?"
