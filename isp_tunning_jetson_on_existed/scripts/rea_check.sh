#!/usr/bin/env bash
# Read-only check of why REA (rea:reverse-engineer-anything) can or cannot run.
# Changes nothing and downloads nothing. Prints one line per check and a verdict.
# Usage: bash rea_check.sh
set -u
fail=0
say() { printf '%-5s %s\n' "$1" "$2"; }

# 1. Node.js version against the rea-agents engines field
plugin=$(ls -d "$HOME"/.claude/plugins/cache/rea/rea/* 2>/dev/null | head -1)
need=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['engines']['node'])" "$plugin/package.json" 2>/dev/null)
have=$(node --version 2>/dev/null | sed 's/^v//')
ok=$(python3 - "$have" <<'E'
import sys
v=tuple(int(x) for x in sys.argv[1].split('.')) if sys.argv[1] else (0,)
print("yes" if (v[0]==22 and v>=(22,23,4)) or (v[0]==24 and v>=(24,22,1)) or v>=(26,12,1) else "no")
E
)
if [ "$ok" = yes ]; then say OK "node $have meets $need"; else say FAIL "node ${have:-missing} does not meet ${need:-^22.23.4 || ^24.22.1 || >=26.12.1} -> upgrade Node"; fail=1; fi

# 2. Plugin present and whether it registers an MCP server
if [ -n "$plugin" ]; then say OK "REA plugin at $plugin ($(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['version'])" "$plugin/package.json" 2>/dev/null))"
else say FAIL "REA plugin not installed"; fail=1; fi
if [ -n "$plugin" ] && [ ! -f "$plugin/.mcp.json" ]; then
  say INFO "plugin ships no .mcp.json: it gives the skill text only, not the REA tools"
fi
if [ -n "$plugin" ] && [ ! -d "$plugin/node_modules" ]; then
  say INFO "plugin has no node_modules: the bundled package cannot run as is"
fi

# 3. MCP server registered with Claude Code
if claude mcp list 2>/dev/null | grep -qi 'rea'; then say OK "an MCP server named rea is registered"
else say FAIL "no REA MCP server registered -> npx -y rea-agents@6.8.0 setup --client claude_code --dry-run --json, review, then --yes, restart Claude Code"; fail=1; fi

# 4. CLI on PATH
if command -v rea >/dev/null 2>&1; then say OK "rea CLI: $(command -v rea)"; else say INFO "no rea CLI on PATH"; fi

[ $fail -eq 0 ] && echo "REA READY (tools appear after a Claude Code restart if just registered)" || echo "REA NOT READY"
exit $fail
