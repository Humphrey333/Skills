# AI-writing signs

The word and phrase lists `embed_writing` checks a draft against. Two sources: the Wikipedia page "Signs of AI writing" (read 2026-10-17) and the pattern dictionary of `humanize-writing-skill` (MIT, Luis Guzman). A sign is a reason to look at a sentence, not proof. If a listed word is the exact technical term (for example "dynamic" in "dynamic linking"), keep it.

Every fix below rewords. None of them removes a fact, a reason, a hedge, a warning or a list item. If a fix would change the meaning, keep the original wording and flag it.

## Words: replace with the plain one

| Sign | Write instead |
|---|---|
| delve, embark, spearhead, garner, bolster | look at, start, lead, get, support |
| tapestry, landscape, realm, interplay, symphony | name the thing itself |
| pivotal, crucial, key role, vital | important, or state the consequence |
| underscore, highlight, showcase, illuminate | show, say |
| testament, stands as, serves as, features, boasts | is, has |
| intricate, meticulous, nuanced, multifaceted | detailed, careful, or say what the detail is |
| leverage, utilize, facilitate | use |
| robust, seamless, comprehensive, holistic, cutting-edge, innovative, groundbreaking | say what it does, with the number or name the draft gives |
| vibrant, rich, profound, renowned, nestled, diverse array, commitment to | the plain adjective, or the plain noun ("many kinds of") |
| foster, enhance, navigate, resonate | improve, handle, work with |
| evolving landscape, setting the stage for, indelible mark, valuable insights | say the plain fact the phrase points at; if it points at none, keep it and flag it |

## Transitions

Furthermore, Moreover, Additionally, Consequently, Nevertheless, Subsequently, Notably, Indeed, Hence, Thus: use "also", "so", "but", "then". Keep the logic: "Consequently" becomes "so", never nothing. More than two in one document is a sign.

Announcing phrases: "In conclusion", "In summary", "It's worth noting that", "It's important to understand that", "Let's dive in", "Let's break this down", "Here's the thing": remove the phrase and keep the point that follows it.

## Sentence shapes: say the same fact directly

- Negative parallelism used as filler: "not just X but Y", "It's not X, it's Y". Write both facts plainly. A real contrast ("active low instead of active high", "Y rather than X" when both are real options) stays a contrast.
- Negation used as filler: "without any optics" in a sentence about software. A real negation ("the driver does not release reset") is a fact and stays.
- Groups of three used to sound complete. Keep every item; reword the list so it reads as a plain list.
- Trailing "-ing" analysis: ", highlighting…", ", ensuring…", ", reflecting…", ", contributing to…". Make it its own sentence with the same fact ("This ensures X" becomes "So X holds").
- Question then answer: "What does this mean? It means…". Give the answer as a statement.
- Mirror sentences: two neighbours with the same shape and different nouns. Join them or vary the shape; keep both facts.
- Copula avoidance: "serves as", "stands as", "refers to" where "is" works. A lead sentence of the form "X refers to…" becomes "X is…".
- Vague attribution: "experts argue", "industry reports", "some critics". Keep the claim and flag it so the caller names the source.
- Significance inflation: "marks a pivotal moment", "plays a crucial role". State the fact or the consequence.
- Hedging: a real hedge ("likely", "possible", "not checked yet", "not widely documented") is a fact about certainty and stays. Only stacked hedges ("it could perhaps be argued that") are reworded to one plain hedge.
- Em dashes in prose: use none. A comma, colon, parentheses or a second sentence does the job. The calling skill's fixed template keeps its own.
- A neat closing sentence on a paragraph that repeats the paragraph: keep it and flag it.
- A section that ends with "Future outlook" or "Despite these challenges…": keep it and flag it.

## Padding and invented content: flag, do not delete

These are signs the draft may hold content no source gave. Reword them if they have AI signs, keep them, and list each one under `flagged:` for the calling skill. The caller and the developer decide whether it goes.

- Restating the intro under a heading such as "What it is".
- A sentence under every required heading that seems to fill space.
- Benefits, audiences, "easy to use", "fits into existing pipelines".
- Instructions nobody gave ("Ask the maintainers before…").

## Formatting

- Title Case headings: write sentence case ("Getting started"). The calling skill's fixed headings stay as given.
- Bold on key phrases in running text. Bold only a term at its definition, or a warning. The calling skill's template keeps its own bold.
- Bullets that start with a bold label and a colon (`**Label:** text`) where plain sentences or a table fit better. Template labels stay.
- Emoji used as bullets or heading marks.
- Skipped heading levels, a second level-1 heading, a heading that holds only other headings.
- A table with one row, or a table for prose.
- Curly quotes in code, commands or file names (plain ASCII quotes there).

## Leftovers: the only things to strip

These carry no information. Strip them and name them in the `stripped:` part of the return line.

- Chatbot lines: "Here's a template…", "Below is a detailed overview…", "Great question", "Hope this helps", "Let me know if…". A next-step question the calling skill requires is not a leftover.
- Tool markers: `contentReference`, `oaicite`, `[cite: 1]`, `utm_source=`.
- Unfilled placeholders: `[Describe…]`, `INSERT_…`, `2025-XX-XX`. Do not strip these silently: flag each one so the caller turns it into `TODO: <what is missing>`.
- A sudden shift from plain to promotional tone: reword it plainly, keep the facts.
