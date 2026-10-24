#!/usr/bin/env python3
"""Local pull-request review page for a branch made by embed_executing_plans.

    python3 review.py --base <branch> --plan <plan.md> [--pr Review/PR_<slug>.md]
                      [--round N] [--prev Review/export_r<N-1>.txt]

Writes Review/Review_<plan-slug>_r<N>.html: a self-contained, offline page that
shows the PR description, the commits and every changed file as a diff. The
reviewer accepts or rejects each file, comments on single lines or line ranges
(as on GitHub or GitLab), accepts or rejects the whole pull request, and
presses "Export review" to get a text block to paste back into the chat. The
page opens in the default browser unless --no-open is given. Nothing is sent
anywhere; drafts stay in the browser.
"""

import argparse
import html
import json
import re
import subprocess
import sys
import webbrowser
from pathlib import Path

MAX_LINES_PER_FILE = 5000   # beyond this a file shows only its first lines
EXPORT_HEAD = re.compile(r"^=== REVIEW (\S+) round (\d+) base (\w+) head (\w+) ===$")
EXPORT_PR = re.compile(r"^PULL REQUEST: (accept|reject|pending)$")
EXPORT_FILE = re.compile(r"^FILE (.+): (accept|reject|pending)$")
EXPORT_LINE = re.compile(r"^  L(\d+)(?:-L(\d+))? \(([+\- ])\): (.*)$")


def git(*args):
    """
    @brief  Run one git command in the current repository.
    @param  args  git arguments, e.g. ("log", "--oneline").
    @return The command's stdout as text.
    How it works: runs git with check=True, so a failing command stops the
    script with git's own error message instead of producing a half page.
    """
    out = subprocess.run(["git", *args], check=True, capture_output=True, text=True)
    return out.stdout


def parse_diff(text):
    """
    @brief  Turn `git diff` output into a list of files with typed lines.
    @param  text  unified diff text from `git diff --no-color`.
    @return list of dicts: {path, old_path, binary, lines:[{kind, old, new, text}]},
            kind is "hunk", "add", "del", "ctx" or "note".
    How it works: walks the diff line by line. A "diff --git" header starts a
    new file; "@@ -a,b +c,d @@" resets the old/new counters; then each body
    line advances the counter of its side ("+" new only, "-" old only, " " both).
    """
    files, cur, old_no, new_no = [], None, 0, 0
    hunk = re.compile(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@(.*)$")
    for line in text.splitlines():
        if line.startswith("diff --git "):
            m = re.match(r"^diff --git a/(.*) b/(.*)$", line)
            cur = {"path": m.group(2) if m else line[11:], "old_path": m.group(1) if m else "",
                   "binary": False, "lines": []}
            files.append(cur)
        elif cur is None:
            continue
        elif line.startswith("Binary files "):
            cur["binary"] = True
        elif line.startswith(("index ", "--- ", "+++ ", "new file", "deleted file",
                              "similarity", "rename ", "old mode", "new mode")):
            continue
        elif hunk.match(line):
            m = hunk.match(line)
            old_no, new_no = int(m.group(1)), int(m.group(2))
            cur["lines"].append({"kind": "hunk", "old": "", "new": "", "text": line})
        elif line.startswith("+"):
            cur["lines"].append({"kind": "add", "old": "", "new": new_no, "text": line[1:]})
            new_no += 1
        elif line.startswith("-"):
            cur["lines"].append({"kind": "del", "old": old_no, "new": "", "text": line[1:]})
            old_no += 1
        elif line.startswith("\\"):
            cur["lines"].append({"kind": "note", "old": "", "new": "", "text": line})
        else:
            cur["lines"].append({"kind": "ctx", "old": old_no, "new": new_no, "text": line[1:]})
            old_no += 1
            new_no += 1
    return files


def parse_export(text):
    """
    @brief  Read a pasted review export back into structured form.
    @param  text  the block between "=== REVIEW" and "=== END ===".
    @return dict {branch, round, base, head, pr, files:{path:{decision, comment, lines:[...]}},
            overall} or None when the header line is missing; pr is "pending" when the
            export has no PULL REQUEST line (older pages).
    How it works: matches the header and the PULL REQUEST line, then each FILE line opens a file; the
    "  comment:" and "  L<n> (side):" lines that follow belong to it; lines
    indented by four spaces continue the previous comment.
    """
    lines = text.strip().splitlines()
    start = next((i for i, l in enumerate(lines) if EXPORT_HEAD.match(l.strip())), None)
    if start is None:
        return None
    m = EXPORT_HEAD.match(lines[start].strip())
    res = {"branch": m.group(1), "round": int(m.group(2)), "base": m.group(3),
           "head": m.group(4), "pr": "pending", "files": {}, "overall": ""}
    cur, last = None, None
    for line in lines[start + 1:]:
        if line.strip() == "=== END ===":
            break
        fm, lm, pm = EXPORT_FILE.match(line), EXPORT_LINE.match(line), EXPORT_PR.match(line)
        if pm:
            res["pr"] = pm.group(1)
            last = None
        elif fm:
            cur = res["files"].setdefault(fm.group(1), {"decision": fm.group(2), "comment": "", "lines": []})
            last = None
        elif line.startswith("  comment: ") and cur is not None:
            cur["comment"] = line[len("  comment: "):]
            last = (cur, "comment")
        elif lm and cur is not None:
            c = {"start": int(lm.group(1)), "end": int(lm.group(2) or lm.group(1)),
                 "side": lm.group(3), "text": lm.group(4)}
            cur["lines"].append(c)
            last = (c, "text")
        elif line.startswith("OVERALL: "):
            res["overall"] = line[len("OVERALL: "):]
            last = (res, "overall")
        elif line.startswith("    ") and last is not None:
            obj, key = last
            obj[key] += "\n" + line[4:]
    return res


def earlier_status(prev, path):
    """
    @brief  Mark each earlier-round line comment on a file as addressed or open.
    @param  prev  parsed previous export (parse_export), or None.
    @param  path  file path in this round.
    @return list of {label, text, status} for that file, empty when none.
    How it works: diffs the previous round's head against HEAD for this file;
    a comment whose old-side line range overlaps a changed hunk counts as
    addressed by the commits that touched the file since then.
    """
    if not prev or path not in prev["files"]:
        return []
    try:
        d = git("diff", "--no-color", "-U0", prev["head"], "HEAD", "--", path)
        shas = git("log", "--format=%h", f"{prev['head']}..HEAD", "--", path).split()
    except subprocess.CalledProcessError:
        d, shas = "", []
    changed = [(int(a), int(a) + max(int(b or 1), 1) - 1)
               for a, b in re.findall(r"^@@ -(\d+)(?:,(\d+))? ", d, re.M)]
    out = []
    for c in prev["files"][path]["lines"]:
        hit = any(not (c["end"] < lo or c["start"] > hi) for lo, hi in changed)
        label = f"L{c['start']}" + (f"-L{c['end']}" if c["end"] != c["start"] else "") + f" ({c['side']})"
        status = f"addressed in {', '.join(shas)}" if hit and shas else "still open"
        out.append({"label": label, "text": c["text"], "status": status})
    if prev["files"][path]["comment"]:
        out.append({"label": "file", "text": prev["files"][path]["comment"],
                    "status": f"file changed in {', '.join(shas)}" if shas else "still open"})
    return out


def md_to_html(md):
    """
    @brief  Render the small Markdown subset used by the PR description.
    @param  md  Markdown text: headings, paragraphs, "-" lists, "- [ ]"/"- [x]"
                checkboxes, fenced code, `code` and **bold**.
    @return HTML string; every input character is escaped first.
    How it works: escapes the whole line, then applies inline rules, so no raw
    HTML from the description can reach the page.
    """
    def inline(s):
        s = html.escape(s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)

    out, in_list, in_code = [], False, False
    for line in md.splitlines():
        if line.startswith("```"):
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append("</code></pre>" if in_code else "<pre><code>")
            in_code = not in_code
            continue
        if in_code:
            out.append(html.escape(line))
            continue
        m = re.match(r"^\s*- \[( |x|X)\] (.*)$", line)
        if m or re.match(r"^\s*- ", line):
            if not in_list:
                out.append("<ul>")
                in_list = True
            if m:
                mark = "checked" if m.group(1) != " " else ""
                out.append(f'<li class="task"><input type="checkbox" disabled {mark}> {inline(m.group(2))}</li>')
            else:
                out.append(f"<li>{inline(line.split('- ', 1)[1])}</li>")
            continue
        if in_list:
            out.append("</ul>")
            in_list = False
        h = re.match(r"^(#{1,4}) (.*)$", line)
        if h:
            n = len(h.group(1)) + 1
            out.append(f"<h{n}>{inline(h.group(2))}</h{n}>")
        elif line.strip():
            out.append(f"<p>{inline(line)}</p>")
    if in_list:
        out.append("</ul>")
    if in_code:
        out.append("</code></pre>")
    return "\n".join(out)


def render_file(idx, f, earlier):
    """
    @brief  Build the HTML panel of one changed file.
    @param  idx      file index, used in element ids.
    @param  f        one entry of parse_diff().
    @param  earlier  earlier_status() result for this file.
    @return HTML string for the panel.
    How it works: one table row per diff line with old/new numbers and a "+"
    gutter button carrying data-side/data-line, so the page script can open a
    comment box under any line.
    """
    p = html.escape(f["path"])
    rename = (f' <span class="muted">(renamed from {html.escape(f["old_path"])})</span>'
              if f["old_path"] and f["old_path"] != f["path"] else "")
    rows = []
    if f["binary"]:
        rows.append('<tr class="note"><td colspan="4">binary file, not shown</td></tr>')
    shown = f["lines"][:MAX_LINES_PER_FILE]
    for i, ln in enumerate(shown):
        k = ln["kind"]
        if k in ("hunk", "note"):
            rows.append(f'<tr class="{k}"><td colspan="4">{html.escape(ln["text"])}</td></tr>')
            continue
        side, num = ("-", ln["old"]) if k == "del" else (("+", ln["new"]) if k == "add" else (" ", ln["new"]))
        sign = {"add": "+", "del": "-", "ctx": " "}[k]
        rows.append(
            f'<tr class="ln {k}" data-row="{i}" data-side="{side}" data-line="{num}">'
            f'<td class="num">{ln["old"]}</td><td class="num">{ln["new"]}'
            f'<button class="addc" title="Comment (shift-click a second line for a range)">+</button></td>'
            f'<td class="sign">{sign}</td><td class="code">{html.escape(ln["text"])}</td></tr>')
    if len(f["lines"]) > MAX_LINES_PER_FILE:
        rows.append(f'<tr class="note"><td colspan="4">large diff: first {MAX_LINES_PER_FILE} lines shown</td></tr>')
    prev = ""
    if earlier:
        items = "".join(f'<li><code>{html.escape(e["label"])}</code> {html.escape(e["text"])} '
                        f'<span class="status">{html.escape(e["status"])}</span></li>' for e in earlier)
        prev = f'<div class="earlier"><strong>Earlier round comments</strong><ul>{items}</ul></div>'
    return f'''
<section class="file" id="f{idx}" data-idx="{idx}" data-path="{p}">
  <header>
    <span class="path">{p}</span>{rename}
    <span class="count" data-count="{idx}">0 comments</span>
    <label><input type="radio" name="d{idx}" value="accept"> Accept</label>
    <label><input type="radio" name="d{idx}" value="reject"> Reject</label>
    <label><input type="radio" name="d{idx}" value="pending" checked> Pending</label>
  </header>
  {prev}
  <table class="diff"><tbody>{"".join(rows)}</tbody></table>
  <textarea class="fcomment" placeholder="Comment on the whole file"></textarea>
</section>'''


def build_page(meta, files, commits, pr_html, earlier_by_path):
    """
    @brief  Assemble the full self-contained review page.
    @param  meta     dict: branch, base, base_sha, head_sha, round, slug.
    @param  files    parse_diff() result.
    @param  commits  list of (sha7, subject).
    @param  pr_html  rendered PR description, or "".
    @param  earlier_by_path  {path: earlier_status()}.
    @return the HTML document as a string.
    How it works: static HTML for the diffs, plus one inline script that keeps
    decisions and comments in localStorage and writes the export block.
    """
    commit_rows = "".join(f"<li><code>{html.escape(s)}</code> {html.escape(t)}</li>" for s, t in commits)
    panels = "".join(render_file(i, f, earlier_by_path.get(f["path"], [])) for i, f in enumerate(files))
    meta_json = json.dumps(meta).replace("</", "<\\/")
    title = html.escape(f"Review {meta['branch']} r{meta['round']}")
    pr = f'<section class="pr">{pr_html}</section>' if pr_html else ""
    header = html.escape(f"{meta['branch']} into {meta['base']} · round {meta['round']} · "
                         f"base {meta['base_sha']} · head {meta['head_sha']}")
    fill = {"TITLE": title, "META": meta_json, "HEADER": header, "PR": pr,
            "COMMITS": commit_rows, "FILES": panels}
    # One pass, so text inside a diff that looks like a placeholder is never replaced.
    return re.sub(r"@(TITLE|META|HEADER|PR|COMMITS|FILES)@", lambda m: fill[m.group(1)], PAGE)


def main():
    """
    @brief  Command-line entry: collect git data and write the review page.
    @return process exit code (0 on success).
    How it works: reads base/HEAD shas, the diff and log since the merge base,
    picks the next free round number, optionally loads the PR description and
    the previous round's export, writes Review/Review_<slug>_r<N>.html and opens
    it in the default browser unless --no-open is given.
    """
    ap = argparse.ArgumentParser(description="Build a local review page for the current branch.")
    ap.add_argument("--base", required=True, help="branch the work started from")
    ap.add_argument("--plan", required=True, help="plan file; its name gives the slug")
    ap.add_argument("--pr", help="PR description in Markdown (Review/PR_<slug>.md)")
    ap.add_argument("--round", type=int, help="round number (default: next free)")
    ap.add_argument("--prev", help="previous round's pasted export, saved as a text file")
    ap.add_argument("--out-dir", default="Review")
    ap.add_argument("--no-open", action="store_true", help="do not open the page in a browser")
    a = ap.parse_args()

    slug = re.sub(r"^Plan_|_\d{4}-\d{2}-\d{2}$", "", Path(a.plan).stem)
    out_dir = Path(a.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rnd = a.round or 1 + max([int(m.group(1)) for p in out_dir.glob(f"Review_{slug}_r*.html")
                              if (m := re.search(r"_r(\d+)\.html$", p.name))] or [0])
    branch = git("rev-parse", "--abbrev-ref", "HEAD").strip()
    base_sha = git("merge-base", a.base, "HEAD").strip()[:7]
    head_sha = git("rev-parse", "--short=7", "HEAD").strip()
    files = parse_diff(git("diff", "--no-color", "-M", f"{a.base}...HEAD"))
    commits = [tuple(l.split(" ", 1)) for l in
               git("log", "--reverse", "--format=%h %s", f"{a.base}..HEAD").splitlines() if l]
    if not files:
        print(f"no changes between {a.base} and HEAD", file=sys.stderr)
        return 1
    pr_html = md_to_html(Path(a.pr).read_text()) if a.pr else ""
    prev = parse_export(Path(a.prev).read_text()) if a.prev else None
    earlier = {f["path"]: earlier_status(prev, f["path"]) for f in files}
    meta = {"branch": branch, "base": a.base, "base_sha": base_sha, "head_sha": head_sha,
            "round": rnd, "slug": slug}
    out = out_dir / f"Review_{slug}_r{rnd}.html"
    out.write_text(build_page(meta, files, commits, pr_html, earlier))
    print(f"{out}  ({len(files)} files, {len(commits)} commits, round {rnd})")
    if not a.no_open and not open_page(out):
        print(f"open it manually: {out.resolve()}")
    return 0


def open_page(path):
    """
    @brief  Open the review page in the default browser.
    @param  path  the written HTML file.
    @return True when a browser was started, False when none is available.
    How it works: hands a file:// URI to the webbrowser module, which picks the
    desktop's default browser (xdg-open on Linux); any error counts as False so
    the caller can print the path instead.
    """
    try:
        return webbrowser.open(path.resolve().as_uri())
    except Exception:
        return False


PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@TITLE@</title>
<style>
:root { --bg:#fff; --fg:#1f2328; --muted:#59636e; --line:#d1d9e0; --panel:#f6f8fa;
  --add:#dafbe1; --del:#ffebe9; --hunk:#ddf4ff; --accent:#0969da; --note:#fff8c5; }
@media (prefers-color-scheme: dark) { :root { --bg:#0d1117; --fg:#e6edf3; --muted:#9198a1;
  --line:#3d444d; --panel:#151b23; --add:#12261e; --del:#25171c; --hunk:#121d2f;
  --accent:#4493f8; --note:#2b2a1a; } }
* { box-sizing:border-box; }
body { margin:0; padding:16px; background:var(--bg); color:var(--fg);
  font:14px/1.5 -apple-system, "Segoe UI", Roboto, sans-serif; }
code, .code, textarea { font-family: ui-monospace, "SFMono-Regular", Menlo, monospace; }
.top { position:sticky; top:0; z-index:2; background:var(--bg); border-bottom:1px solid var(--line);
  padding:8px 0; display:flex; flex-wrap:wrap; gap:12px; align-items:center; }
.top .meta { font-weight:600; } .muted, .count, .status { color:var(--muted); font-size:12px; }
button { background:var(--panel); color:var(--fg); border:1px solid var(--line); border-radius:6px;
  padding:4px 10px; cursor:pointer; } button.primary { background:var(--accent); color:#fff; border-color:var(--accent); }
.pr, .commits, .file, .export { border:1px solid var(--line); border-radius:6px; margin:16px 0; padding:8px 16px; }
.file { padding:0; overflow:hidden; } .file header { display:flex; flex-wrap:wrap; gap:12px; align-items:center;
  background:var(--panel); padding:8px 16px; border-bottom:1px solid var(--line); }
.path { font-weight:600; font-family:ui-monospace, monospace; word-break:break-all; }
.diff { width:100%; border-collapse:collapse; table-layout:fixed; }
.diff td { padding:0 8px; vertical-align:top; } .num { width:56px; text-align:right; color:var(--muted);
  font-family:ui-monospace, monospace; font-size:12px; position:relative; user-select:none; }
.sign { width:16px; color:var(--muted); } .code { white-space:pre-wrap; word-break:break-all; font-size:12px; }
tr.add { background:var(--add); } tr.del { background:var(--del); } tr.hunk td, tr.note td { background:var(--hunk);
  color:var(--muted); font-family:ui-monospace, monospace; font-size:12px; padding:4px 8px; }
tr.note td { background:var(--note); } tr.sel td { outline:1px solid var(--accent); }
.addc { display:none; position:absolute; left:2px; top:0; padding:0 5px; line-height:16px; font-size:12px;
  background:var(--accent); color:#fff; border:0; } tr.ln:hover .addc { display:inline-block; }
tr.crow td { background:var(--panel); padding:8px 16px; border-top:1px solid var(--line); border-bottom:1px solid var(--line); }
.cbox { border:1px solid var(--line); border-radius:6px; padding:6px 10px; margin:4px 0; background:var(--bg); }
.cbox .who { font-size:12px; color:var(--muted); } .cbox p { margin:4px 0; white-space:pre-wrap; }
textarea { width:100%; min-height:64px; background:var(--bg); color:var(--fg); border:1px solid var(--line);
  border-radius:6px; padding:6px; font-size:13px; }
.fcomment { border:0; border-top:1px solid var(--line); border-radius:0; }
.earlier { padding:8px 16px; background:var(--note); border-bottom:1px solid var(--line); font-size:13px; }
.earlier ul { margin:4px 0; } li.task { list-style:none; margin-left:-20px; }
#out { min-height:200px; }
.prbar { display:flex; flex-wrap:wrap; gap:8px; align-items:center; }
.prstate { font-weight:600; padding:2px 8px; border-radius:12px; border:1px solid var(--line); font-size:12px; }
.prstate.accept { background:var(--add); } .prstate.reject { background:var(--del); }
button.ok { background:#1f883d; color:#fff; border-color:#1f883d; } button.bad { background:#cf222e; color:#fff; border-color:#cf222e; }
button.on { outline:2px solid var(--fg); }
#banner { display:none; margin:8px 0; padding:8px 16px; border:1px solid #cf222e; border-radius:6px; background:var(--del); }
#banner a { color:var(--accent); margin-right:8px; }
@media (max-width:600px) { body { padding:8px 16px; } .num { width:40px; } }
</style></head><body>
<div class="top"><span class="meta">@HEADER@</span>
  <span id="summary" class="muted"></span>
  <span class="prbar">Pull request: <span class="prstate" data-prstate>pending</span>
    <button class="ok" data-pr="accept">Accept pull request</button>
    <button class="bad" data-pr="reject">Reject (request changes)</button></span>
  <button class="primary" id="exportBtn">Export review</button></div>
<div id="banner"></div>
@PR@
<section class="commits"><h3>Commits</h3><ul>@COMMITS@</ul></section>
@FILES@
<section class="export"><h3>Pull request decision</h3>
  <p class="prbar"><span class="prstate" data-prstate>pending</span>
    <button class="ok" data-pr="accept">Accept pull request</button>
    <button class="bad" data-pr="reject">Reject (request changes)</button>
    <span class="muted">Merge happens only when the pull request and every file are accepted.</span></p>
  <h3>Overall comment</h3>
  <textarea id="overall" placeholder="Comment on the whole pull request"></textarea>
  <h3>Export</h3><p class="muted">Press "Export review", then paste the block into the chat.</p>
  <textarea id="out" readonly></textarea> <button id="copyBtn">Copy</button></section>
<script>
const META = @META@;
const KEY = "review:" + META.branch + ":r" + META.round;
let S;
try { S = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { S = {}; }
S.files = S.files || {}; S.overall = S.overall || ""; S.pr = S.pr || "pending";
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} };
const fileState = p => (S.files[p] = S.files[p] || { decision: "pending", comment: "", lines: [] });
let anchor = null;   // first line of a shift-click range: {sec, row}

function label(c) { return "L" + c.start + (c.end !== c.start ? "-L" + c.end : "") + " (" + c.side + ")"; }

function rowsOf(sec) { return Array.from(sec.querySelectorAll("tr.ln")); }

function drawComments(sec) {
  const st = fileState(sec.dataset.path);
  sec.querySelectorAll("tr.crow.saved").forEach(r => r.remove());
  st.lines.forEach((c, i) => {
    const row = sec.querySelector('tr.ln[data-row="' + c.row + '"]');
    if (!row) return;
    const tr = document.createElement("tr"); tr.className = "crow saved";
    const td = document.createElement("td"); td.colSpan = 4;
    const box = document.createElement("div"); box.className = "cbox";
    const who = document.createElement("div"); who.className = "who"; who.textContent = label(c);
    const p = document.createElement("p"); p.textContent = c.text;
    const ed = document.createElement("button"); ed.textContent = "Edit";
    const del = document.createElement("button"); del.textContent = "Delete";
    ed.onclick = () => openEditor(sec, row, c, i);
    del.onclick = () => { st.lines.splice(i, 1); save(); drawComments(sec); refresh(); };
    box.append(who, p, ed, " ", del); td.append(box); tr.append(td);
    row.after(tr);
  });
  sec.querySelector("[data-count]").textContent = st.lines.length + (st.lines.length === 1 ? " comment" : " comments");
}

function openEditor(sec, row, existing, index, range) {
  sec.querySelectorAll("tr.crow.edit").forEach(r => r.remove());
  const tr = document.createElement("tr"); tr.className = "crow edit";
  const td = document.createElement("td"); td.colSpan = 4;
  const lab = document.createElement("div"); lab.className = "muted";
  const c = existing || { row: Number(row.dataset.row), side: row.dataset.side,
    start: Number(range ? range[0] : row.dataset.line), end: Number(range ? range[1] : row.dataset.line), text: "" };
  lab.textContent = "Comment on " + label(c);
  const ta = document.createElement("textarea"); ta.value = c.text;
  const ok = document.createElement("button"); ok.className = "primary"; ok.textContent = existing ? "Update" : "Add comment";
  const cancel = document.createElement("button"); cancel.textContent = "Cancel";
  ok.onclick = () => {
    if (!ta.value.trim()) return;
    c.text = ta.value.trim();
    const st = fileState(sec.dataset.path);
    if (existing) st.lines[index] = c; else st.lines.push(c);
    save(); tr.remove(); drawComments(sec); refresh();
  };
  cancel.onclick = () => tr.remove();
  td.append(lab, ta, ok, " ", cancel); tr.append(td); row.after(tr); ta.focus();
}

function refresh() {
  let total = 0, acc = 0, rej = 0, pen = 0;
  document.querySelectorAll("section.file").forEach(sec => {
    const st = fileState(sec.dataset.path); total += st.lines.length;
    if (st.decision === "accept") acc++; else if (st.decision === "reject") rej++; else pen++;
  });
  document.getElementById("summary").textContent =
    total + " line comments · files: " + acc + " accepted · " + rej + " rejected · " + pen + " pending";
  const names = { accept: "accepted", reject: "changes requested", pending: "pending" };
  document.querySelectorAll("[data-prstate]").forEach(el => {
    el.textContent = names[S.pr]; el.className = "prstate " + S.pr;
  });
  document.querySelectorAll("button[data-pr]").forEach(b => b.classList.toggle("on", b.dataset.pr === S.pr));
  // Accepting the PR while a file is not accepted cannot merge: say which files block it.
  const banner = document.getElementById("banner");
  const blocking = Array.from(document.querySelectorAll("section.file"))
    .filter(sec => fileState(sec.dataset.path).decision !== "accept");
  banner.textContent = "";
  if (S.pr === "accept" && blocking.length) {
    banner.append("Cannot merge yet: " + blocking.length + " file" + (blocking.length === 1 ? "" : "s") + " not accepted. ");
    blocking.forEach(sec => {
      const a = document.createElement("a"); a.href = "#f" + sec.dataset.idx; a.textContent = sec.dataset.path;
      banner.append(a);
    });
    banner.style.display = "block";
  } else banner.style.display = "none";
}

function indent(t) { return t.split("\n").join("\n    "); }

function exportText() {
  const out = ["=== REVIEW " + META.branch + " round " + META.round + " base " + META.base_sha + " head " + META.head_sha + " ===",
               "PULL REQUEST: " + S.pr];
  document.querySelectorAll("section.file").forEach(sec => {
    const st = fileState(sec.dataset.path);
    out.push("FILE " + sec.dataset.path + ": " + st.decision);
    if (st.comment.trim()) out.push("  comment: " + indent(st.comment.trim()));
    st.lines.slice().sort((a, b) => a.start - b.start).forEach(c => out.push("  " + label(c) + ": " + indent(c.text)));
  });
  out.push("OVERALL: " + indent(S.overall.trim()));
  out.push("=== END ===");
  return out.join("\n");
}

document.querySelectorAll("section.file").forEach(sec => {
  const st = fileState(sec.dataset.path);
  sec.querySelectorAll('input[type="radio"]').forEach(r => {
    r.checked = r.value === st.decision;
    r.onchange = () => { st.decision = r.value; save(); refresh(); };
  });
  const fc = sec.querySelector(".fcomment"); fc.value = st.comment;
  fc.oninput = () => { st.comment = fc.value; save(); };
  sec.querySelectorAll("button.addc").forEach(b => b.onclick = ev => {
    const row = b.closest("tr");
    if (ev.shiftKey && anchor && anchor.sec === sec) {
      const rows = rowsOf(sec), i = rows.indexOf(anchor.row), j = rows.indexOf(row);
      const [a, z] = i <= j ? [rows[i], rows[j]] : [rows[j], rows[i]];
      sec.querySelectorAll("tr.sel").forEach(r => r.classList.remove("sel"));
      rows.slice(Math.min(i, j), Math.max(i, j) + 1).forEach(r => r.classList.add("sel"));
      const nums = [a, z].map(r => Number(r.dataset.line));
      openEditor(sec, z, null, null, [Math.min(...nums), Math.max(...nums)]);
      anchor = null;
    } else {
      sec.querySelectorAll("tr.sel").forEach(r => r.classList.remove("sel"));
      anchor = { sec, row }; row.classList.add("sel");
      openEditor(sec, row);
    }
  });
  drawComments(sec);
});
document.querySelectorAll("button[data-pr]").forEach(b => b.onclick = () => {
  S.pr = S.pr === b.dataset.pr ? "pending" : b.dataset.pr;   // a second click undoes the choice
  save(); refresh();
});
const ov = document.getElementById("overall"); ov.value = S.overall;
ov.oninput = () => { S.overall = ov.value; save(); };
document.getElementById("exportBtn").onclick = () => {
  const box = document.getElementById("out"); box.value = exportText();
  box.scrollIntoView({ behavior: "smooth" });
  try { navigator.clipboard.writeText(box.value); } catch (e) {}
};
document.getElementById("copyBtn").onclick = () => {
  const box = document.getElementById("out"); box.select();
  try { navigator.clipboard.writeText(box.value); } catch (e) { document.execCommand("copy"); }
};
refresh();
</script></body></html>
"""

if __name__ == "__main__":
    sys.exit(main())
