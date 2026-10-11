# Exam Format (F3)

An exam is two local files in `<topic-dir>`:

| File | Who reads it | Contains |
|---|---|---|
| `Exam_<source>.html` | the developer, in a browser | questions and the answer form only |
| `Exam_<source>_key.md` | Claude, when grading | answers, why each trap is wrong, exact source locations |

`<source>` is `day<N>` for a path day (`day6`, `day6_retake1`, `day6_retake2`; `day2_review1` for a review of a passed day), or `<book-slug>_ch<M>` for a book chapter.

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

Then propose the `Progress.md` update and, if the exam was not passed, the retake.

## Progress.md

```markdown
# Progress — <topic-slug>

Path: Path_<YYYY-MM-DD>.md · Level: base→medium | base→advanced

| Day | Status | Attempts | Last score | Weak points (source location) |
|---|---|---|---|---|
| 1 | passed | 1 | 10/10 | — |
| 2 | not passed | 2 | 9/10 | fixation vs negotiation (ch. 8.4, p. 151) |
| 3 | locked | 0 | — | — |
```

`passed` only at 100%. The day after the first day that isn't passed stays `locked`.
