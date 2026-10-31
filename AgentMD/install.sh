#!/usr/bin/env bash
# Install every skill in this repo plus the AgentMD rules for each agent.
# Usage: bash install.sh [--link] [--agents claude,codex,gemini,antigravity] [--gitea] [-h]
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
  echo "Usage: bash install.sh [--link] [--agents a,b,...] [--gitea] [-h]"
  echo "  --link     symlink to this clone instead of copying"
  echo "  --agents   comma list of: ${ALL_AGENTS// /, } (default: all)"
  echo "  --gitea    also set up the local Gitea review workspace (tea, Docker, Agent login)"
}

link=0
gitea=0
agents=$ALL_AGENTS
while [ $# -gt 0 ]; do
  case $1 in
    --link) link=1 ;;
    --agents)
      [ $# -ge 2 ] || { usage >&2; exit 2; }
      agents=${2//,/ }
      shift ;;
    --gitea) gitea=1 ;;
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

GITEA_URL=http://localhost:3000
GITEA_DEV_USER=Humphrey333   # the developer: reviewer, maintainer, owner of every repo

# True when tea has a login named Agent for user Agent on <url>.
has_agent_login() { # has_agent_login <url>
  tea login list -o csv 2>/dev/null | grep -q "^Agent,$1,[^,]*,Agent,"
}

# Gitea review flow (embed_programming_discussion): warn only, never change Gitea or git config.
check_gitea() {
  if ! command -v tea >/dev/null 2>&1; then
    echo "warning: tea not found; install it for the Gitea review flow (README: Gitea setup (once))" >&2
    return 0
  fi
  if ! has_agent_login "$GITEA_URL"; then
    echo "warning: no tea login 'Agent' (user Agent) on $GITEA_URL (README: Gitea setup (once))" >&2
  fi
}

wait_enter() { # wait_enter <prompt>
  printf '%s [Enter] ' "$1"
  read -r _ || true
}

# --gitea: set up the review workspace. Automatic where possible; the developer
# does only what needs a browser (accounts, token, collaborators). Each step
# skips itself when already done. Agent writes the code, the developer reviews
# and owns every repo; the developer's token is never asked for.
setup_gitea() {
  echo "== gitea"
  if [ ! -t 0 ]; then
    echo "skip gitea setup: needs a terminal (run: bash install.sh --gitea)" >&2
    return 0
  fi

  # 1. tea, the Gitea CLI
  if command -v tea >/dev/null 2>&1; then
    echo "ok       tea already installed"
  elif command -v brew >/dev/null 2>&1; then
    brew install tea
  else
    echo "error: brew not found; install tea by hand (README: Gitea setup (once))" >&2
    return 1
  fi

  # 2. Gitea server in Docker, data kept in the gitea-data volume
  if ! command -v docker >/dev/null 2>&1; then
    echo "error: docker not found; install Docker and run again" >&2
    return 1
  fi
  case $(docker inspect -f '{{.State.Running}}' gitea 2>/dev/null || echo absent) in
    true)  echo "ok       container gitea already running" ;;
    false) docker start gitea >/dev/null || return 1
           echo "start    container gitea" ;;
    *)     docker run -d --name=gitea --restart unless-stopped \
             -p 3000:3000 -p 222:22 -v gitea-data:/data gitea/gitea:latest >/dev/null || return 1
           echo "create   container gitea" ;;
  esac

  # 3. URL, typed by the developer
  local url
  read -r -p "Gitea URL [$GITEA_URL]: " url || true
  url=${url:-$GITEA_URL}
  url=${url%/}
  [ "$url" = "$GITEA_URL" ] ||
    echo "warning: the skills use $GITEA_URL; with $url they will not find Gitea" >&2
  local i
  for i in $(seq 60); do
    curl -fsS "$url/api/v1/version" >/dev/null 2>&1 && break
    [ "$i" -eq 60 ] && { echo "error: Gitea does not answer at $url" >&2; return 1; }
    sleep 1
  done
  echo "ok       Gitea answers at $url"

  # 4. Developer's own account (reviewer, maintainer, owner of every repo)
  echo
  echo "Your account ($GITEA_DEV_USER, reviewer and maintainer):"
  echo "  1. Open $url in a browser."
  echo "  2. First start only: finish the install page (defaults are fine), then"
  echo "     register your own account. The first account becomes the admin."
  wait_enter "Done?"
  local user
  while :; do
    read -r -p "Your Gitea username [$GITEA_DEV_USER]: " user || return 1
    user=${user:-$GITEA_DEV_USER}
    [ -n "$user" ] && curl -fsS "$url/api/v1/users/$user" >/dev/null 2>&1 && break
    echo "no user '$user' at $url, try again" >&2
  done
  echo "ok       user $user"

  # 5. Agent account and its token (Agent writes the code)
  if has_agent_login "$url"; then
    echo "ok       tea login Agent already set"
  else
    echo
    echo "Agent account (the agent's own user; it writes the code, you review):"
    echo "  1. As $user: Site Administration -> User Accounts -> Create User Account,"
    echo "     username Agent."
    echo "  2. Log out, log in as Agent once and set its password."
    echo "  3. As Agent: Settings -> Applications -> Generate New Token, scopes:"
    echo "     repository read/write, user read, issue read/write. Copy the token."
    wait_enter "Done?"
    local token
    while :; do
      read -r -s -p "Paste Agent's token (hidden): " token || return 1
      echo
      [ -n "$token" ] || continue
      tea login delete Agent >/dev/null 2>&1 || true
      if tea login add --name Agent --url "$url" --token "$token" >/dev/null &&
         has_agent_login "$url"; then
        break
      fi
      echo "tea login failed (token for user Agent?), try again" >&2
    done
    token=
    echo "ok       tea login Agent"
  fi

  # 6. Agent as Write collaborator on repos the developer already owns.
  # New repos need nothing here: Agent creates them at the project's first
  # init and transfers them to the developer (embed_programming_discussion).
  echo
  local repos r
  read -r -p "Your existing repos for Agent to work on (space separated, blank = none): " repos || true
  [ -n "$repos" ] || return 0
  echo "For each repo: Repo -> Settings -> Collaborators -> add Agent, permission Write."
  wait_enter "Done?"
  for r in $repos; do
    if tea api --login Agent "repos/$user/$r" 2>/dev/null | grep -q '"push": *true'; then
      echo "ok       Agent can push to $user/$r"
    else
      echo "warning: Agent cannot push to $user/$r; add it as Write collaborator" >&2
    fi
  done
}

if [ "$gitea" -eq 1 ]; then
  setup_gitea || echo "gitea setup stopped; fix the error above and run: bash install.sh --gitea" >&2
else
  check_gitea
fi

echo "installed=$n_inst same=$n_same skipped=$n_skip overwritten=$n_over"
echo "Restart your agent sessions to load the changes."
