# AI-writing signs

The word and phrase lists `embed_writing` checks a draft against. Two sources: the Wikipedia page "Signs of AI writing" (read 2026-10-17) and the pattern dictionary of `humanize-writing-skill` (MIT, Luis Guzman). A sign is a reason to look at a sentence, not proof. If a listed word is the exact technical term (for example "dynamic" in "dynamic linking"), keep it.

## Words: replace with the plain one

| Sign | Write instead |
|---|---|
| delve, embark, spearhead, garner, bolster | look at, start, lead, get, support |
| tapestry, landscape, realm, interplay, symphony | name the thing itself, or drop |
| pivotal, crucial, key role, vital | important, or state the consequence |
| underscore, highlight, showcase, illuminate | show, say, or drop |
| testament, stands as, serves as, features, boasts | is, has |
| intricate, meticulous, nuanced, multifaceted | detailed, careful, or say what the detail is |
| leverage, utilize, facilitate | use |
| robust, seamless, comprehensive, holistic, cutting-edge, innovative, groundbreaking | say what it does, with a number or a name |
| vibrant, rich, profound, renowned, nestled, diverse array, commitment to | drop; these are promotion |
| foster, enhance, navigate, resonate | improve, handle, or drop |
| evolving landscape, setting the stage for, indelible mark, valuable insights | drop the sentence |

## Transitions

Furthermore, Moreover, Additionally, Consequently, Nevertheless, Subsequently, Notably, Indeed, Hence, Thus: use "also", "so", "but", "then", or nothing. More than two in one document is a sign.

Announcing phrases: "In conclusion", "In summary", "It's worth noting that", "It's important to understand that", "Let's dive in", "Let's break this down", "Here's the thing": delete and state the point.

## Sentence shapes: say the positive fact once

- Negative parallelism: "not just X but Y", "It's not X, it's Y", "Y rather than X", "no X, no Y, just Z". Write what is true.
- Negation as filler: "does not move any lens", "without any optics". State what it does.
- Groups of three used to sound complete. Keep the items that matter.
- Trailing "-ing" analysis: ", highlighting…", ", ensuring…", ", reflecting…", ", contributing to…". Drop the clause or make it its own sentence with a fact in it.
- Question then answer: "What does this mean? It means…". Give the answer.
- Mirror sentences: two neighbours with the same shape and different nouns.
- Copula avoidance: "serves as", "stands as", "refers to" where "is" works. A lead sentence of the form "X refers to…" becomes "X is…".
- Vague attribution: "experts argue", "industry reports", "some critics". Name the source or delete the claim.
- Significance inflation: "marks a pivotal moment", "plays a crucial role". State the fact.
- Hedging disclaimers: "not widely documented", "it could be argued". Say what is known and what is unknown (`TODO:` for the unknown).
- Em dashes: use none. A comma, colon, parentheses or a second sentence does the job.
- A neat closing sentence on every paragraph that repeats the paragraph.
- A section that ends with "Future outlook" or "Despite these challenges…" when no source says so.

## Padding and invented content (found in the baseline test)

- Restating the intro under a heading such as "What it is".
- A sentence under every required heading even when no fact exists. Write the fact or `TODO:`; do not fill.
- Benefits, audiences, "easy to use", "fits into existing pipelines": claims no source gave.
- A friendly opener ("Hi, here is…") or a closing line that repeats the point.
- Instructions nobody gave ("Ask the maintainers before…").

## Formatting

- Title Case headings: write sentence case ("Getting started").
- Bold on key phrases in running text. Bold only a term at its definition, or a warning.
- Bullets that start with a bold label and a colon (`**Label:** text`) where plain sentences or a table fit better.
- Emoji used as bullets or heading marks.
- Skipped heading levels, a second level-1 heading, a heading that holds only other headings.
- A table with one row, or a table for prose.
- Curly quotes in code, commands or file names (plain ASCII quotes there).

## Leftovers: always remove

- Chatbot lines: "Here's a template…", "Below is a detailed overview…", "Great question".
- Tool markers: `contentReference`, `oaicite`, `[cite: 1]`, `utm_source=`.
- Unfilled placeholders: `[Describe…]`, `INSERT_…`, `2025-XX-XX`. A real unknown is `TODO: <what is missing>`, never a bracket placeholder.
- A sudden shift from plain to promotional tone.
