#!/usr/bin/env bash
# Run clang-tidy over src/ using the build directory's compile_commands.json.
#
# Usage: tools/run-clang-tidy.sh [build-dir]    (default: build)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="${1:-$ROOT/build}"

if [[ ! -f "$BUILD_DIR/compile_commands.json" ]]; then
  echo "error: $BUILD_DIR/compile_commands.json missing - configure first:" >&2
  echo "       cmake -S $ROOT -B $BUILD_DIR" >&2
  exit 1
fi

find "$ROOT/src" -type f -name '*.cpp' -print0 \
  | xargs -0 clang-tidy -p "$BUILD_DIR"
