# Lesson Note Format (path days)

Claude writes one note per path day, `<topic-dir>/.learn/notes/day<N>.md`, together with the day's bank (F1 step 4). It stays hidden until the day is passed. Then `learn.py` copies it to `<topic-dir>/Notes/Day<N>_<title-slug>.md`, where `<title-slug>` is the bank's `title` in lower case, with every run of other characters replaced by `-`, cut to 40 characters.

The note is what the developer keeps: the knowledge of that day, short enough to re-read in ten minutes. Every point carries its source, and nothing is added that the day's sources do not support.

## Sections, in order

```markdown
# Day <N> — <title>

## Purpose
The one thing this day makes clear, in one or two sentences.

## When you'd use it
1–3 lines in the learner's world (Jetson, GStreamer, MAVLink, drivers).

## Key points
- <point>. (<book>, <chapter or section>, p. <printed page>)
- …

## In an embedded project
Where it shows up in real work, with a small example. A code or UML snippet is fine; cite where it comes from, or mark it as the note's own illustration of a cited point.

## Traps
- <the misconception> → <what is true>. (<source>)

## Where to re-read
- <book>, <chapter or section>, pp. <from>–<to>
```

## Rules

- Key points cover every question target in the day's bank; a question whose point is missing from the note means the note is incomplete.
- Citations use printed pages, rule numbers or section numbers, never `.md` line numbers.
- A point that needs a diagram cites the figure and its PDF page (`[FIG p.N]` marker) so the developer can open it. Take the number from the marker in the book's Markdown, never from memory. A day whose sources show figures must have at least one such citation in its note.
- The text goes through `embed_writing` before it is saved.
