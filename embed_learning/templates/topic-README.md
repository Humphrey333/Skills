# @TOPIC_TITLE@

Your 7-day learning path for `@TOPIC_SLUG@`: one hour a day, one exam a day. A day counts as done only when you pass its exam at 100%.

## Quick start

```bash
cd <this folder>
python3 learn.py
```

Your browser opens today's exam. Pick one option for every question and press Submit. Your result appears in the terminal.

## Daily routine

1. Look up today's reading in the table under "Your week". The books are in `@EBOOK_DIR@`.
2. Read those pages. They fit in the hour, with time left for the exam.
3. Run `python3 learn.py` and take the exam.
4. Read the result in the terminal:
   - **Passed:** your lesson note for the day is now in `Notes/`. Re-read it whenever you need the day's points again. The next day is open.
   - **Not passed:** the terminal lists each question you missed, with the page to re-read. Re-read them, or ask Claude to re-teach (see "Getting help"). Then run `python3 learn.py` again. The retake shows questions you haven't seen first.

## Your week

@DAY_TABLE@

The full plan for each day (purpose, key points, sources) is in `@PATH_FILE@`.

## Files

| File | What it is | You |
|---|---|---|
| `learn.py` | Runs your exams and records the results | run it |
| `@PATH_FILE@` | The 7-day plan | read it |
| `Progress.md` | Your score for each day | read it; never edit the table |
| `Notes/` | One lesson note per day you have passed | read and keep them |
| `.learn/` | Question banks, the hidden notes, the attempt log and the exam page | leave it alone; opening a bank shows you the answers |
| `Exam_*.html`, `Exam_*_key.md` | Only for book-chapter exams and reviews of passed days | open the `.html` in a browser; don't open the `_key.md` |
| `Book_*.md` | A summary of one book, if you asked for one | read it |
| `README.md` | This file | read it |

## Rules

- The pass mark is 100%. Below that, the next day stays locked. Retakes are unlimited.
- Only `learn.py` writes `Progress.md` and the attempt log. A hand edit is overwritten on the next run.
- A day with no book source yet shows as `not ready`. Ask Claude to write its exam once you have the book.

| Command | What it does |
|---|---|
| `python3 learn.py` | Open the next exam: the first day you haven't passed |
| `python3 learn.py status` | Print your progress and the next day |
| `python3 learn.py <day>` | Open that day's exam, if it isn't locked or already passed |

## Getting help

Ask Claude in a session started in this folder:

| You want | Say |
|---|---|
| Your misses explained | "re-teach my last learn.py attempt for Day N" |
| To test a day you already passed | "give me a review exam for Day N" |
| An exam on one book chapter | "make me an exam on <book>, chapter M" |
| Fresh questions for a day | "add more questions to the Day N bank" |
| A question you think is wrong | "Day N, the question about <topic> looks wrong" (Claude checks it against the book and fixes the bank; your recorded attempt stands) |
