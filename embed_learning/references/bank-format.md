# Question Bank Format (path days)

Path days are examined by `learn.py` in the topic folder, not by pasting answers to Claude. Claude writes one bank and one note per day when the path is approved (F1 step 4). The script reads the files below; every field it reads is defined here once.

## Files in `<topic-dir>/.learn/`

| File | Written by | Read by | Contains |
|---|---|---|---|
| `bank_day<N>.json` | Claude | `learn.py` | the day's questions, answers and source locations |
| `notes/day<N>.md` | Claude | `learn.py` (copies it on a pass) | the day's lesson note, see `notes-format.md` |
| `exam.html` | copied from `templates/exam.html` | `learn.py` (serves it) | the page; questions arrive from the server, never answers |
| `attempts.jsonl` | `learn.py` | `learn.py` | one line per attempt |

`<N>` runs from 1 to the number of days in the path, with no gaps. The script finds the days by listing `bank_day*.json`.

## `bank_day<N>.json`

```json
{
  "day": 1,
  "title": "What UML is for, and reading a class box",
  "draw": { "basic": 4, "medium": 3, "traps": 3 },
  "questions": [
    {
      "id": "d1-b01",
      "section": "basic",
      "question": "Which statement best matches how the book defines the UML?",
      "options": {
        "A": "A programming language that compiles object-oriented models into code",
        "B": "A family of graphical notations backed by a single meta-model",
        "C": "A diagramming tool whose file format the OMG licenses to vendors",
        "D": "A notation defined only for class hierarchies in C++ and Java"
      },
      "answer": "B",
      "source": "UML Distilled, Ch. 1, p. 1 (What Is the UML?)",
      "why": "Right: the book calls it a family of notations with one meta-model. 'A programming language' is wrong because the UML only describes designs. 'A diagramming tool' is wrong because it is a standard, not a product. 'Only class hierarchies' is wrong because it also covers sequence and state diagrams."
    }
  ]
}
```

| Field | Rule |
|---|---|
| `day` | integer, equal to `<N>` in the file name |
| `title` | the day's purpose in a few words; shown on the page and used in the note's file name |
| `draw` | how many questions of each section one attempt shows. Default `4 / 3 / 3` (10 questions) |
| `questions[].id` | unique in the bank, form `d<N>-<b\|m\|t><NN>` (`d1-b01`, `d3-t06`). Fixing a question's wording or answer keeps its id; a different question gets a new id. Never delete an id that appears in `attempts.jsonl` |
| `section` | `basic`, `medium` or `traps` |
| `question` | plain text. Wrap code in backticks (`` `+ getName() : String` ``); the page shows it as code. No HTML |
| `code` | optional. A short multi-line snippet (C++ or PlantUML) the question is about. The page shows it in a code block under the question. Plain text, no HTML |
| `options` | exactly the keys `A`, `B`, `C`, `D`, each a non-empty plain-text string. One answer only. See "Writing the options" |
| `answer` | one of `A`–`D` |
| `source` | the exact location in a supplied source: book, chapter or section, **printed page** (or rule or section number). Never a `.md` line number, never from memory |
| `why` | why the answer is right and why **each** distractor is wrong, naming each option by its text. Never by letter: the page shuffles the letters. For Claude when re-teaching. The script never prints it |

Bank size: about 2.5 times `draw` per section. The default is **24 questions: 10 basic, 8 medium, 6 traps**. In a `traps` question, one distractor is the common misconception.

## Writing the options

The exam must not be passable by test-taking tricks.

- The four options of a question are about the same length (within about 25%) and the same grammatical form. Wrong options are full statements, not three-word throwaways.
- Each distractor is a real misconception or a near-miss from the source, something a learner who skimmed would believe.
- The right option is the strictly longest of its four in at most 40% of the bank's questions. `learn.py` refuses a bank above that.
- At least half of the `medium` and `traps` questions carry a `code` snippet: read a C++ declaration and pick the matching UML or PlantUML, or read a PlantUML block and pick the C++ ownership, dependency or defect it implies. "What does <author> say" questions are for `basic` only.
- Do not balance `answer` letters by hand. The page shuffles every question, so the bank may keep any letter.

The script refuses to run a bank that breaks a rule above (missing field, duplicate `id`, `answer` not in `options`, empty `source`, a `why` that cites an option by letter, a `code` that is not a string, the right option longest in over 40% of questions, fewer questions in a section than `draw` asks for) and says which question is wrong.

## What reaches the page

The server sends only `day`, `title`, the attempt number, and per drawn question: its position `Q1`…`Qn`, `section`, `question` and `options`. It never sends `id`, `answer`, `source` or `why`. The page posts back `{"Q1": "B", …}`; the server maps positions back to ids. In `attempts.jsonl`, `Qn` is the n-th id in `shown`, and `order[<id>]` lists the bank letters in the order the page showed them as A, B, C, D.

## Draw rule

For each section, in the order `basic`, `medium`, `traps`:

1. Count how often each question of the section has been shown, from `attempts.jsonl`.
2. Take the `draw[section]` questions with the lowest count; break ties at random.
3. Shuffle them within the section.

Questions are numbered `Q1`…`Qn` across sections. The options of each question are shuffled for every attempt, so the page's letters differ from the bank's, and the right option doesn't sit at the same letter every time. The bank may therefore keep its answers at any letter; `why` refers to the bank's letters.

## Grading and the day gate

- A question is right only when the posted letter equals `answer`. Unanswered is wrong.
- **Passed means every drawn question right.** Anything below 100% is not passed.
- The terminal shows the score `x / n`, then for each wrong question: its number, its text, the text of the option picked, and its `source`. It never shows `answer` or `why`.
- The script opens only the first day that is not passed. Later days are locked, and asking for one is refused.

## `attempts.jsonl`

One JSON object per line, appended after each submission:

```json
{"time": "2026-10-18T21:04:11", "day": 1, "attempt": 1, "shown": ["d1-b03", "d1-b07", "…"], "order": {"d1-b03": "CADB", "d1-b07": "BDAC"}, "answers": {"d1-b03": "B", "d1-b07": "—"}, "wrong": ["d1-b07"], "score": 9, "total": 10, "passed": false}
```

`attempt` counts from 1 per day. `answers` holds the **bank's** letter of the option picked (already mapped back from the page), or `—` for an unanswered question. This file is the record; `Progress.md` is rebuilt from it.

## `Progress.md`

Claude writes the first version at path approval:

```markdown
# Progress — <topic-slug>

Path: Path_<YYYY-MM-DD>.md · Level: base→medium | base→advanced

| Day | Status | Attempts | Last score | Weak points (source location) |
|---|---|---|---|---|
| 1 | not passed | 0 | — | — |
| 2 | locked | 0 | — | — |
```

with one row for every day of the path, including days whose bank is not written yet. After that, the script keeps everything above and below the table as it is and rewrites the table from `attempts.jsonl`:

```markdown
| Day | Status | Attempts | Last score | Weak points (source location) |
|---|---|---|---|---|
| 1 | passed | 2 | 10/10 | — |
| 2 | not passed | 1 | 8/10 | UML Distilled, Ch. 3, p. 41; Ambler, rule 121, p. 64 |
| 3 | locked | 0 | — | — |
```

- `passed`: some attempt scored 100%.
- `not passed`: the first day that is not passed.
- `locked`: every day after it.
- `not ready`: the open day has no bank yet (its source hasn't been supplied). The script says so and opens nothing.

The days are the larger of: the banks found, and the highest day number in the existing table.
- Weak points: the `source` of each wrong question in the day's last attempt, or `—`.

If `Progress.md` does not exist, the script writes `# Progress — <topic-slug>` above the table.
