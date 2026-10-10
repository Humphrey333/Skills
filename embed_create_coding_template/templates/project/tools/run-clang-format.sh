#!/usr/bin/env bash
# Format (or check) all C++ sources with the project's .clang-format.
#
# Usage: tools/run-clang-format.sh [--check]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MODE=(-i)
[[ "${1:-}" == "--check" ]] && MODE=(--dry-run --Werror)

find "$ROOT/src" "$ROOT/include" "$ROOT/test" -type f \
  \( -name '*.cpp' -o -name '*.hpp' -o -name '*.h' \) -print0 \
  | xargs -0 clang-format "${MODE[@]}"
