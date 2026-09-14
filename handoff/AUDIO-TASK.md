# Задача: озвучить скрипт аудирования «The Queen Who Said No»

Вставь этот файл целиком в новый чат Claude Code, **запущенный на компьютере, где стоит
OmniVoice** (не в облаке — облачная сессия к локальным программам доступа не имеет).

---

## Что нужно сделать

Синтезировать **две аудиодорожки** из текста ниже с помощью локально установленного
OmniVoice и положить их в папку `materials/audio/` репозитория.

| Файл | Что это | Настройки |
|---|---|---|
| `elizabeth-01-normal.mp3` | первое прослушивание | британский голос, обычный темп, паузы между абзацами ~0,5 с |
| `elizabeth-02-slow.mp3` | второе прослушивание | тот же голос, темп ~0.9 от обычного, паузы между абзацами **~1,5 с** |

Если OmniVoice умеет — сделай третьим файлом `elizabeth-full-lesson.mp3`: дорожка 1,
пять секунд тишины, дорожка 2. Учителю удобно нажать play один раз.

**Формат:** MP3, моно, 64–96 kbps этого хватает. Целевая длительность дорожки 1 — около
3 минут (в тексте 330 слов, это ≈ 110 слов в минуту).

**Голос:** британский английский. Мужской или женский — на твоё усмотрение, но **один и
тот же** в обеих дорожках. Это радиопередача «Great Lives», нужен спокойный дикторский
тон, не эмоциональное чтение.

### Почему две дорожки, а не одна

Так устроено задание на листе `16-monday-listening`. Первое прослушивание — на общий
смысл, ученики отмечают только задание 2. Второе — медленнее и с паузами, под задания 3 и
4. Если сделать одну дорожку, урок не работает.

---

## Текст для синтеза

Числа и даты уже написаны словами — так и синтезируй, не превращай обратно в цифры.
Абзацы разделяй паузой (0,5 с в дорожке 1; 1,5 с в дорожке 2).

```
1
Hello, and welcome to Great Lives. Today: a queen who ruled England for forty-four years.

2
Elizabeth was born on the seventh of September, fifteen thirty-three, at Greenwich Palace,
near London. Her father was King Henry the Eighth. Her mother was Anne Boleyn. When
Elizabeth was two years old, her father had her mother killed. People said the little girl
was not a real princess.

3
But Elizabeth was clever. She studied with a famous teacher, Roger Ascham. She learned
Latin, French and Italian. She read and she read and she read.

4
Life was not safe. In March fifteen fifty-four her sister Mary sent her to the Tower of
London. Elizabeth stayed in the Tower for about two months. After that she lived in the
country for almost a year, and soldiers watched her door. She was not free.

5
Everything changed in fifteen fifty-eight. Mary died, and on the seventeenth of November
Elizabeth became queen. She was twenty-five years old. In January fifteen fifty-nine they
crowned her in Westminster Abbey.

6
Many men wanted to marry her. Kings and princes sent her letters and pictures. Elizabeth
said no. She said no to all of them, and she kept the power herself. Today people call her
the Virgin Queen.

7
In fifteen eighty-eight the King of Spain sent a great fleet of ships, the Armada, against
England. Elizabeth went to Tilbury and spoke to her soldiers. She said: I know I have the
body but of a weak, feeble woman; but I have the heart and stomach of a king. The Armada
lost.

8
Elizabeth loved the theatre. In her time William Shakespeare and Christopher Marlowe wrote
their plays, and people still watch them today.

9
Elizabeth died on the twenty-fourth of March, sixteen oh three, at Richmond Palace. She was
queen for forty-four years. King James of Scotland became the next king of England.

10
So, what makes a great person? Think about Elizabeth. She was clever. She was brave. And
she said no.
```

**Абзац 7 — самый трудный для учеников.** Цитату с Тилбери («I know I have the body but of
a weak, feeble woman…») прочитай чуть медленнее и с паузой перед ней в обеих дорожках.

**Ничего в тексте не меняй.** Каждая дата и цифра здесь сверена с источниками; «сделать
красивее» = сломать ключи к заданиям.

---

## Куда положить и что сделать после

```bash
git checkout claude/educational-materials-newton-lennon-diana-97qb1p
git pull origin claude/educational-materials-newton-lennon-diana-97qb1p
mkdir -p materials/audio
# ...положить сюда mp3...
python3 build/verify.py          # должно быть 242/242
git add materials/audio
git commit -m "Add the recorded listening track for the Monday lesson"
git push -u origin claude/educational-materials-newton-lennon-diana-97qb1p
```

Репозиторий: **`2rister/TeacherSwitxher-`**
Ветка: **`claude/educational-materials-newton-lennon-diana-97qb1p`** — работать и пушить
только в неё, в другие ветки не пушить.

После того как файлы лягут в `materials/audio/`, обнови два места, где сейчас написано,
что записи нет:

1. `build/monday.py` — блок заметки «If you would rather not read it yourself» в
   `build/build.py`, функция `audio_script()`. Сейчас там: *«There is no recording in this
   pack.»* Заменить на то, как называются файлы и где лежат.
2. `README.md` — раздел про понедельник, абзац «**Записи звука нет**».

Затем пересобрать и проверить:

```bash
python3 build/build.py           # HTML + PDF, цветной и ч/б, с контролем переполнения A4
python3 build/make_docx.py       # редактируемые версии для Word
python3 build/verify.py          # 242 проверки содержания
python3 build/check_with_libreoffice.py
```

---

## Контекст проекта (коротко)

Печатный комплект A2 к игре Jeopardy для языкового интенсива. Главный вопрос интенсива —
**WHAT MAKES A GREAT PERSON?** Группа, для которой делается это аудирование, готовит
выступление про **Елизавету I**.

В `materials/` лежат: `pdf/` (цветная версия), `pdf-bw/` (ч/б для класса), `docx/`
(редактируемая), `jeopardy/` (колода PowerPoint), `img/`, `html/` (исходники вёрстки).
Контент правится **только** в `build/content.py`, `build/grammar.py`, `build/monday.py`,
`build/phrases.py` — PDF и DOCX генерируются из них, руками их не редактировать.

Аудирование — это листы `16-monday-listening` (ученикам) и `17-monday-audio-script`
(учителю: скрипт + ключи ко всем заданиям).

### Что нельзя ломать

- **Даты Елизаветы.** Умерла **24 марта 1603** (в исходном тексте учителя было 14 марта),
  была королевой **44 года** (было 45). Исправлено во всём комплекте.
- **Два неподтверждённых сюжета** — что её убил свинцовый грим и что Шекспир был её
  любимым писателем — остались в тексте для чтения на листе VI, потому что это текст
  учителя и он воспроизводится как написан. Но **ни в одном упражнении, ключе или в
  аудио их нет**, и добавлять нельзя. В аудио сказано только то, что задокументировано:
  она любила театр, Шекспир и Марло писали в её правление.
- **Цитата с Тилбери** (9 августа 1588) большинством историков считается подлинной,
  меньшинством оспаривается. На листе учителя это написано прямо — не убирать.
- `python3 build/verify.py` должен проходить **242/242**. Если после правки упало —
  чинить содержание, а не проверку.
- В коммиты, PR и комментарии кода **не вставлять названия моделей**.

### Хвост коммитов

```
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_012xu6R3py9QfGiRnZ4SZmDj
```

---

## Если OmniVoice не заведётся

Запасной путь, проверенный в облачной сессии: Piper TTS, оффлайн, без ключей и без
интернета после скачивания голоса.

```bash
pip install piper-tts lameenc
# британские голоса из rhasspy/piper-voices на HuggingFace:
#   en/en_GB/alan/medium/en_GB-alan-medium.onnx           (мужской, нейтральный)
#   en/en_GB/cori/high/en_GB-cori-high.onnx               (женский, выше качеством)
# к каждому .onnx нужен файл .onnx.json рядом

# дорожка 1 — обычный темп
python3 -m piper -m en_GB-alan-medium.onnx -f normal.wav \
        --length-scale 1.00 --sentence-silence 0.35 < script.txt
# дорожка 2 — медленнее
python3 -m piper -m en_GB-alan-medium.onnx -f slow.wav \
        --length-scale 1.20 --sentence-silence 0.55 < script.txt
```

`--length-scale` — длительность фонемы: больше значение = медленнее речь. Паузы между
абзацами Piper сам не ставит: синтезируй абзацы по отдельности и склей WAV-ы, вставляя
тишину нужной длины (модуль `wave` из стандартной библиотеки), потом сожми в MP3
(`lameenc`).
