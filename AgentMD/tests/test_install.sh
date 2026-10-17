#!/usr/bin/env bash
# Runs install.sh against throw-away HOME directories. Never touches the real home.
set -uo pipefail

HERE=$(cd "$(dirname "$0")" && pwd)
INSTALL="$HERE/../install.sh"
REPO=$(cd "$HERE/../.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

total=0
fails=0
check() { # check "<what>" <command...>
  local what=$1
  shift
  total=$((total + 1))
  if "$@" >/dev/null 2>&1; then
    echo "PASS $what"
  else
    echo "FAIL $what"
    fails=$((fails + 1))
  fi
}
absent_text() { ! grep -q "$1" "$2"; }
newhome() { mktemp -d -p "$TMP"; }
run() { # run <home> [install.sh args]; stdin and stderr pass through
  local h=$1
  shift
  HOME=$h bash "$INSTALL" "$@" 2>&1
}

# (a) fresh install, all agents
h=$(newhome)
out=$(run "$h" </dev/null)
check "a: claude rules" test -f "$h/.claude/CLAUDE.md" -a -f "$h/.claude/AGENTS.md"
check "a: claude skills" test -f "$h/.claude/skills/embed_debug/SKILL.md"
check "a: new forks installed" test -f "$h/.claude/skills/embed_executing_plans/SKILL.md" -a -f "$h/.claude/skills/embed_programming/SKILL.md"
check "a: handoff installed" test -f "$h/.claude/skills/handoff/SKILL.md"
check "a: codex rules" test -f "$h/.codex/AGENTS.md"
check "a: codex/gemini skills" test -f "$h/.agents/skills/embed_planning-embedded-topics/SKILL.md"
check "a: gemini/antigravity rules" test -f "$h/.gemini/GEMINI.md"
check "a: antigravity skills" test -f "$h/.gemini/config/skills/embed_debug/SKILL.md"
check "a: AgentMD not installed as a skill" test ! -e "$h/.claude/skills/AgentMD"
check "a: karpathy clone not installed" test ! -e "$h/.claude/skills/andrej-karpathy-skills"
check "a: no Requirements/Plans files copied" test -z "$(find "$h/.claude/skills" \( -name 'Requi*' -o -name 'Plans*' \))"
check "a: installed matches repo" diff -rq -x 'Requi*' -x 'Plans*' "$REPO/embed_debug" "$h/.claude/skills/embed_debug"
check "a: summary line" bash -c 'echo "$1" | grep -q "installed=[1-9]"' _ "$out"

# (b) second run changes nothing
out=$(run "$h" </dev/null)
check "b: rerun installs nothing" bash -c 'echo "$1" | grep -q "installed=0 .*skipped=0 .*backed_up=0"' _ "$out"

# (c) a differing file: no answer / s skips, o backs up and overwrites
echo tampered >>"$h/.claude/AGENTS.md"
out=$(run "$h" </dev/null)
check "c: no terminal skips" grep -q tampered "$h/.claude/AGENTS.md"
out=$(echo s | run "$h")
check "c: s keeps the edit" grep -q tampered "$h/.claude/AGENTS.md"
check "c: s counted" bash -c 'echo "$1" | grep -q "skipped=1"' _ "$out"
out=$(echo o | run "$h")
check "c: o restores the repo copy" absent_text tampered "$h/.claude/AGENTS.md"
check "c: o keeps a backup outside the skills dir" bash -c 'grep -q tampered "$1"/.agentmd-backup/*/.claude/AGENTS.md' _ "$h"

# (d) a differing skill directory
echo tampered >>"$h/.claude/skills/embed_debug/SKILL.md"
out=$(echo o | run "$h")
check "d: skill dir restored" diff -rq -x 'Requi*' -x 'Plans*' "$REPO/embed_debug" "$h/.claude/skills/embed_debug"
check "d: skill backup not left inside skills dir" test -z "$(find "$h/.claude/skills" -maxdepth 1 -name '*bak*')"
check "d: skill backup kept" test -d "$h"/.agentmd-backup/*/.claude/skills/embed_debug

# (e) --link
h=$(newhome)
run "$h" --link </dev/null >/dev/null
check "e: skill is a symlink into the clone" test "$(readlink "$h/.claude/skills/embed_debug")" = "$REPO/embed_debug"
check "e: rules are symlinks" test "$(readlink "$h/.claude/CLAUDE.md")" = "$REPO/AgentMD/CLAUDE.md"
out=$(run "$h" --link </dev/null)
check "e: link rerun installs nothing" bash -c 'echo "$1" | grep -q "installed=0 .*skipped=0"' _ "$out"

# (f) --agents limits the targets
h=$(newhome)
run "$h" --agents claude </dev/null >/dev/null
check "f: claude installed" test -f "$h/.claude/CLAUDE.md"
check "f: others untouched" test ! -e "$h/.codex" -a ! -e "$h/.gemini" -a ! -e "$h/.agents"

# (g) bad agent name fails and installs nothing
h=$(newhome)
check "g: unknown agent exits non-zero" bash -c '! HOME="$1" bash "$2" --agents nope </dev/null' _ "$h" "$INSTALL"
check "g: nothing installed" test -z "$(ls -A "$h")"

echo "$((total - fails))/$total passed"
[ "$fails" -eq 0 ]
