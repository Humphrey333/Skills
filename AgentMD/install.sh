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

# Answers come from the original stdin; the rules loop below redirects its own.
exec 3<&0

n_inst=0 n_same=0 n_skip=0 n_bak=0
seen=""
backup_root="$HOME/.agentmd-backup/$(date +%F-%H%M%S)"

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

# No answer (EOF, no terminal) means skip.
ask_overwrite() {
  local ans
  printf '%s differs. [o]verwrite (old one is backed up) / [s]kip? ' "$1" >&2
  read -r ans <&3 || ans=s
  [ "$ans" = o ]
}

place() { # place <src> <dst>
  local src=$1 dst=$2
  case $seen in *"|$dst|"*) return 0 ;; esac
  seen="$seen|$dst|"
  if [ -e "$dst" ] || [ -L "$dst" ]; then
    if is_same "$src" "$dst"; then
      n_same=$((n_same + 1))
      return 0
    fi
    if ! ask_overwrite "$dst"; then
      echo "skip     $dst"
      n_skip=$((n_skip + 1))
      return 0
    fi
    # Backups live outside the skills dirs so agents never load an old copy as a skill.
    mkdir -p "$backup_root/$(dirname "${dst#"$HOME"/}")"
    mv "$dst" "$backup_root/${dst#"$HOME"/}"
    echo "backup   $dst -> $backup_root/${dst#"$HOME"/}"
    n_bak=$((n_bak + 1))
  fi
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

skills=()
for d in "$SRC"/*/; do
  [ -f "${d}SKILL.md" ] && skills+=("${d%/}")
done
[ "${#skills[@]}" -gt 0 ] || { echo "no skills found in $SRC" >&2; exit 1; }

for agent in $agents; do
  echo "== $agent"
  while IFS='|' read -r file dst; do
    place "$RULES_SRC/$file" "$dst"
  done < <(rules_for "$agent")
  sdir=$(skills_dir_for "$agent")
  for s in "${skills[@]}"; do
    place "$s" "$sdir/$(basename "$s")"
  done
done

echo "installed=$n_inst same=$n_same skipped=$n_skip backed_up=$n_bak"
[ "$n_bak" -eq 0 ] || echo "backups are in $backup_root"
echo "Restart your agent sessions to load the changes."
