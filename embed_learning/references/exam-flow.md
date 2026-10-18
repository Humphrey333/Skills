# Exam flow (F3) — detail

Moved word for word from `SKILL.md`. Read it before writing, running or grading any exam.

There are two kinds of exam:

| Exam | Taken with | Graded by | Format |
|---|---|---|---|
| A path day | `python3 learn.py` | `learn.py` | `references/bank-format.md` |
| A book chapter, or a review of a passed day | the HTML page, then paste the export | Claude | `references/exam-format.md` |

Read the format file before writing any exam.

**Content, for both.** Act as a university lecturer. Write three sections:
- **basic**: definitions and the core mechanism;
- **medium**: applying it to a situation in the learner's world;
- **traps**: points that are easy to misunderstand, written so that the common misconception is the tempting wrong answer.

Every question maps to an exact source location in supplied material. If that source isn't in the conversation, in `<topic-dir>` or in the ebook folder, ask for it before writing any questions.

### Path days (`learn.py`)

1. **Banks are written at F1 step 4**, all days at once. A path-day exam is multiple choice only. There are no `Exam_day<N>.html` files and no retake files: a retake draws the least-shown questions from the same bank.
2. **Re-teaching a failed attempt** (the developer asks after `learn.py` reports a fail). Read the day's last line in `.learn/attempts.jsonl`; `Qn` on the page is the n-th id in its `shown`, and the page shuffled the options, so `order[<id>]` maps the page's A–D to the bank's letters while `answers` already holds bank letters. Quote options by their text, not by letter. For each id in `wrong`, take `answer`, `source` and `why` from the bank. Then use the grading output in `references/exam-format.md`: the misconception, a quote of the source passage with its location, and the re-teach, context first. The re-teach reveals those answers, so append one new question per re-taught id to the bank, on the same target and section and under "Writing the options" (the 40% limit covers the whole bank), with the next free id numbers in that section (no separate yes needed). The re-taught questions have been shown, so `learn.py` draws them only after every unseen question in their section. Rerun `python3 learn.py status`, then end with: *"Retake with `python3 learn.py`."*
3. **More questions.** If the developer has seen most of a day's bank and wants fresh questions, append new ones to that bank with the next free id numbers (no separate yes needed), and rerun `python3 learn.py status`. Rerun it after every bank edit.
4. **Never write `Progress.md` or `attempts.jsonl` for a path day.** `learn.py` owns both.

### Chapter and review exams (paste flow)

1. **Files.** An exam request, or a failed chapter exam needing a retake, is itself the go-ahead for writing exam files — no separate yes. Write `Exam_<source>.html`: offline, self-contained, **no answers anywhere in the page**, with an export block the developer copies back. Also write `Exam_<source>_key.md` containing, per question, the answer, why the traps are wrong, and the exact source location. Both go to `<topic-dir>` as local files. Don't publish them online.
2. **Grading** (when the developer pastes the export). Grade against the key. For each wrong answer:
   - explain the misconception;
   - quote the source passage and give its exact location;
   - re-teach the point, context first.

   Grade short answers against the elements the key lists for them, not exact wording. Report the score.
3. **Review exams** on a day already passed are named `Exam_day<N>_review<k>.html`. Propose adding their weak points to `Progress.md` under a `## Review weak points` heading below the table, one bullet each: `- Day <N> review <k> (<YYYY-MM-DD>): <point> (<source location>)`. `learn.py` keeps text outside the table; never put numbered table rows there. Wait for a yes, then write them. A review never un-passes a day.
4. **Chapter retakes.** Below 100%, write `Exam_<book-slug>_ch<M>_retake<k>.html` plus its key, with **new** questions on the same targets.
