#!/usr/bin/env bash
# Install every skill in this repo plus the AgentMD rules for each agent.
# Usage: bash install.sh [--link] [--agents claude,codex,gemini,antigravity] [-h]
set -euo pipefail

SRC=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
RULES_SRC="$SRC/AgentMD"
ALL_AGENTS="claude codex gemini antigravity"

# --- Targets. One place to edit if an agent moves a path. ---
# rules_for: "<file in AgentMD>|<destination>" per line.
# Gemini CLI and Antigravity both read ~/.gemini/GEMINI.md, so they share one copy.
rules_for() {
  case $1 in
    claude)             echo "AGENTS.md|$HOME/.claude/AGENTS.md"
                        echo "CLAUDE.md|$HOME/.claude/CLAUDE.md" ;;
    codex)              echo "AGENTS.md|$HOME/.codex/AGENTS.md" ;;
    gemini|antigravity) echo "AGENTS.md|$HOME/.gemini/GEMINI.md" ;;
  esac
}
# Codex and Gemini CLI share ~/.agents/skills.
skills_dir_for() {
  case $1 in
    claude)      echo "$HOME/.claude/skills" ;;
    codex|gemini) echo "$HOME/.agents/skills" ;;
    antigravity) echo "$HOME/.gemini/config/skills" ;;
  esac
}

usage() {
  echo "Usage: bash install.sh [--link] [--agents a,b,...] [-h]"
  echo "  --link     symlink to this clone instead of copying"
  echo "  --agents   comma list of: ${ALL_AGENTS// /, } (default: all)"
}

link=0
agents=$ALL_AGENTS
while [ $# -gt 0 ]; do
  case $1 in
    --link) link=1 ;;
    --agents)
      [ $# -ge 2 ] || { usage >&2; exit 2; }
      agents=${2//,/ }
      shift ;;
    -h|--help) usage; exit 0 ;;
    *) usage >&2; exit 2 ;;
  esac
  shift
done
for a in $agents; do
  case " $ALL_AGENTS " in
    *" $a "*) ;;
    *) echo "unknown agent: $a" >&2; exit 2 ;;
  esac
done
[ -f "$RULES_SRC/AGENTS.md" ] || { echo "missing $RULES_SRC/AGENTS.md" >&2; exit 1; }

n_inst=0 n_same=0 n_skip=0 n_over=0
seen=""
mode=scan      # scan: only collect what would be overwritten; apply: install
overwrite=0    # set by the single question between the two passes
conflicts=()

# Skills are directories with a SKILL.md at the top. Dev-only files stay out of the copy.
copy_dir() {
  mkdir -p "$2"
  (cd "$1" && tar cf - --exclude='Requi*' --exclude='Plans*' .) | tar xf - -C "$2"
}

is_same() { # is_same <src> <dst>
  if [ "$link" -eq 1 ]; then
    [ -L "$2" ] && [ "$(readlink "$2")" = "$1" ]
  elif [ -L "$2" ]; then
    return 1
  elif [ -d "$1" ]; then
    diff -rq -x 'Requi*' -x 'Plans*' "$1" "$2" >/dev/null 2>&1
  else
    cmp -s "$1" "$2"
  fi
}

# One question for everything that differs. No answer (EOF, no terminal) means skip.
ask_overwrite_all() {
  local ans
  echo "These ${#conflicts[@]} items already exist and differ:" >&2
  printf '  %s\n' "${conflicts[@]}" >&2
  printf '[o]verwrite all (no backup) / [s]kip all? ' >&2
  read -r ans || ans=s
  [ "$ans" = o ]
}

place() { # place <src> <dst>
  local src=$1 dst=$2
  case $seen in *"|$dst|"*) return 0 ;; esac
  seen="$seen|$dst|"
  if [ -e "$dst" ] || [ -L "$dst" ]; then
    if is_same "$src" "$dst"; then
      [ "$mode" = apply ] && n_same=$((n_same + 1))
      return 0
    fi
    if [ "$mode" = scan ]; then
      conflicts+=("$dst")
      return 0
    fi
    if [ "$overwrite" -ne 1 ]; then
      echo "skip     $dst"
      n_skip=$((n_skip + 1))
      return 0
    fi
    # No backup: the developer keeps their own copy if they want one.
    rm -rf "$dst"
    n_over=$((n_over + 1))
  fi
  [ "$mode" = apply ] || return 0
  mkdir -p "$(dirname "$dst")"
  if [ "$link" -eq 1 ]; then
    ln -s "$src" "$dst"
  elif [ -d "$src" ]; then
    copy_dir "$src" "$dst"
  else
    cp "$src" "$dst"
  fi
  echo "install  $dst"
  n_inst=$((n_inst + 1))
}

# Shared memory for every agent. Created once, never overwritten: agents write it.
seed_index() { # seed_index <file> <heading>
  [ -e "$1" ] && return 0
  mkdir -p "$(dirname "$1")"
  printf '# %s\n' "$2" >"$1"
  echo "create   $1"
  n_inst=$((n_inst + 1))
}

skills=()
for d in "$SRC"/*/; do
  [ -f "${d}SKILL.md" ] && skills+=("${d%/}")
done
[ "${#skills[@]}" -gt 0 ] || { echo "no skills found in $SRC" >&2; exit 1; }

walk() {
  seen=""
  for agent in $agents; do
    [ "$mode" = apply ] && echo "== $agent"
    while IFS='|' read -r file dst; do
      place "$RULES_SRC/$file" "$dst"
    done < <(rules_for "$agent")
    sdir=$(skills_dir_for "$agent")
    for s in "${skills[@]}"; do
      place "$s" "$sdir/$(basename "$s")"
    done
  done
}

mode=scan
walk
if [ "${#conflicts[@]}" -gt 0 ] && ask_overwrite_all; then
  overwrite=1
fi
mode=apply
walk

seed_index "$HOME/.agents/Knowledge/INDEX.md" "Embedded Knowledge Index"
seed_index "$HOME/.agents/Learning/INDEX.md" "Learning Topics"

# Gitea review flow (embed_programming_discussion): warn only, never change Gitea or git config.
check_gitea() {
  if ! command -v tea >/dev/null 2>&1; then
    echo "warning: tea not found; install it for the Gitea review flow (README: Gitea setup (once))" >&2
    return 0
  fi
  if ! tea login list -o csv 2>/dev/null | grep -q '^Agent,http://localhost:3000,[^,]*,Agent,'; then
    echo "warning: no tea login 'Agent' (user Agent) on http://localhost:3000 (README: Gitea setup (once))" >&2
  fi
}
check_gitea

echo "installed=$n_inst same=$n_same skipped=$n_skip overwritten=$n_over"
echo "Restart your agent sessions to load the changes."
