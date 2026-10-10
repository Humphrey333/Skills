#!/usr/bin/env bash
# Run the same checks CI runs, locally: configure, build, test, format check.
#
# Usage: tools/ci-local.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$ROOT/build/ci"

cmake -S "$ROOT" -B "$BUILD_DIR"
cmake --build "$BUILD_DIR" -j
ctest --test-dir "$BUILD_DIR" --output-on-failure || [[ $? -eq 8 ]]  # 8 = no tests registered
"$ROOT/tools/run-clang-format.sh" --check
