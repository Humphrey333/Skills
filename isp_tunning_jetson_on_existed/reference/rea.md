# REA (rea:reverse-engineer-anything) with this skill

## What REA adds to a tune port
- **Archive inventory with identity:** `open_binary` + `inspect_artifact` on a Chromatix `.zip` list every member with its SHA-256, so the report can prove which files were used.
- **Binary tunes:** `libchromatix_*.so`, `.bin` blobs and other packed tuning files are opened with `open_binary` and analysed natively (strings, data tables, functions).
- **Not covered:** REA has no Chromatix XML table parser. The tables are always read by `scripts/argus_isp/` (`qcom.py`, `qcom480.py`).

## Why the tools can be missing although the plugin is installed
`bash scripts/rea_check.sh` reports each of these. All were seen on this host on 2026-11-12 (rea-agents 6.8.0):

| Blocker | Effect | Fix (developer runs it) |
|---|---|---|
| The plugin ships no `.mcp.json` | Invoking the skill loads only instructions. No REA MCP server starts, so `open_binary` and the rest do not exist. | `npx -y rea-agents@6.8.0 setup --client claude_code --dry-run --json`, review, run again with `--yes`, restart Claude Code |
| The plugin has no `node_modules` | The bundled package cannot run by itself | Same setup command (npx installs the package with its dependencies) |
| Node older than `^22.23.4 \|\| ^24.22.1 \|\| >=26.12.1` (v24.21.0 here) | REA refuses to start | Upgrade Node first, e.g. `nvm install 24` |

After the restart, run ToolSearch `open_binary inspect_artifact`. The tools should be listed.
