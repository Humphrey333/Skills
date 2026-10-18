# Exam Format (F3, paste flow)

This format is for exams that `learn.py` does not run: a **book chapter** (`<book-slug>_ch<M>`) or a **review of a passed path day** (`day<N>_review<k>`). Path-day exams and their retakes use the question bank and `learn.py` instead: see `bank-format.md`.

A paste-flow exam is two local files in `<topic-dir>`:

| File | Who reads it | Contains |
|---|---|---|
| `Exam_<source>.html` | the developer, in a browser | questions and the answer form only |
| `Exam_<source>_key.md` | Claude, when grading | answers, why each trap is wrong, exact source locations |

`<source>` is `<book-slug>_ch<M>` for a book chapter (`<book-slug>_ch<M>_retake<k>` for its retakes), or `day<N>_review<k>` for a review of a passed day.

## The HTML page

The page is **one self-contained file**: inline `<style>` and `<script>` only, with no CDN, font or image links. It must work offline when opened with `file://`.

Layout, top to bottom:

1. **Header**: topic, source (e.g. "Day 2 — Caps negotiation; source: *<book>*, ch. 8"), attempt number, and the line *"Pass mark: 100%. Answer every question, then press Export and paste the result back to Claude."*
2. **Three sections**, in order: `Basic`, `Medium`, `Traps`. Number the questions continuously: `Q1`…`Qn`.
3. Question types:
   - **Multiple choice** (one answer): radio buttons labelled `A`–`D`. In a trap question, one distractor is the common misconception.
   - **Short answer**: a `<textarea>` with a hint about the expected length ("1–2 sentences").
4. **Export button**: fills a read-only `<textarea>` with the export block (below) and selects its text so it is ready to copy. Unanswered questions export as `—`.

Never put in the page (grading with quoted evidence is where the re-teaching happens, and answers in the page would leak into retakes):
- answers or answer hashes;
- "correct!" feedback or a score;
- explanations;
- source locations per question. These go in the key, so the page can't give away which passage holds the answer.

Styling: readable, light and dark (`prefers-color-scheme`), and usable at phone width.

Size: 8–12 questions for a 1-hour day, about 40% basic, 35% medium and 25% traps. A retake has a similar count, and all of its questions are new, worded differently from earlier attempts.

### Export block format

```
EXAM <topic-slug> <source> attempt <k>
Q1: B
Q2: C
Q3: <short answer text, newlines replaced by spaces>
...
END
```

The first line lets the grader find the right key file without asking.

## The key file

```markdown
# Key — <topic-slug> <source> attempt <k>

| Q | Section | Answer | Source location | Why the traps are wrong / what a full short answer must contain |
|---|---|---|---|---|
| Q1 | basic | B | *<book>*, ch. 8.2, p. 143 | A confuses caps with buffers; C … |
| Q7 | traps | D | *<book>*, ch. 8.4, p. 151 | B is the common misconception "…" |
```

Every row needs a source location from the supplied material, or the URL of an approved search. A question that can't be located gets rewritten or dropped. Never leave the location blank and never fill it from memory.

## Grading output

Start with the score `x / n` and the verdict `passed` or `not passed`; anything under 100% is not passed. Then, for each wrong or incomplete answer:

1. `Qn`, what was answered, and the correct answer.
2. The misconception behind the wrong answer, in one line.
3. A quote of the source passage, with its exact location.
4. A re-teach: context first, then the point itself.

Then, for a chapter exam that was not passed, offer the retake. For a review exam, propose adding the weak points to `Progress.md` under `## Review weak points`, below the table (a review never un-passes a day), and wait for a yes.

The same output is used when the developer asks Claude to re-teach a failed `learn.py` attempt: read the wrong ids from `.learn/attempts.jsonl` and their `answer`, `source` and `why` from the bank.

## Progress.md

The `Progress.md` format is defined in `bank-format.md`. `learn.py` writes the table; Claude edits it only to add review-exam weak points, after a yes.
