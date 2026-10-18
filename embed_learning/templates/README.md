# Templates for a learning topic

This directory holds the files `embed_learning` copies (from the installed skill, `~/.claude/skills/embed_learning/templates/`) into a topic folder when a path is approved (F1 step 4). It is skill documentation plus source files; the directory itself is not copied.

| Template | Copied to | Then |
|---|---|---|
| `learn.py` | `<topic-dir>/learn.py` | substitute the placeholders below |
| `exam.html` | `<topic-dir>/.learn/exam.html` | copied as it is; it has no placeholders |
| `topic-README.md` | `<topic-dir>/README.md` | the learner's guide to every file in the folder; substitute the placeholders below |

Claude also writes, from the formats in `../references/`:
- `<topic-dir>/.learn/bank_day<N>.json` for every day (`bank-format.md`);
- `<topic-dir>/.learn/notes/day<N>.md` for every day (`notes-format.md`).

`learn.py` creates `attempts.jsonl` and `Notes/`, and rewrites the `Progress.md` table after each attempt.

## Placeholders

| Placeholder | Meaning |
|---|---|
| `@TOPIC_SLUG@` | the topic slug from `~/.agents/Learning/INDEX.md`, e.g. `uml-oop-design-cpp` |
| `@TOPIC_TITLE@` | the topic in words, as the path's title gives it, e.g. `UML design for OOP in C++` |
| `@PATH_FILE@` | the path's file name, e.g. `Path_2026-10-11.md` (`topic-README.md` only) |
| `@EBOOK_DIR@` | the `ebooks:` folder on the topic's `INDEX.md` line (`topic-README.md` only) |
| `@DAY_TABLE@` | a Markdown table, one row per day of the path: `\| Day \| Title \| Read \|`. Title is the bank's `title`, or for a day with no bank yet the day's Purpose from the path in a few words; Read is the day's Source from the path, or exactly `not ready: source not supplied yet` for a day with no supplied source (`topic-README.md` only) |

After substitution this must print nothing:

```bash
grep -rn '@[A-Z_]*@' <topic-dir>/README.md <topic-dir>/learn.py <topic-dir>/.learn
```

## Checks before telling the developer it is ready

```bash
cd <topic-dir>
python3 learn.py status        # validates every bank; prints the table, Day 1 "not passed"
```

A bank that breaks `bank-format.md` makes `status` exit with the file and question at fault. Fix it before handing over.

## Tests

`../tests/test_learn.py` runs the template against a temporary topic:

```bash
python3 -m unittest discover -s embed_learning/tests
```
