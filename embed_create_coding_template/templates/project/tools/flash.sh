#!/usr/bin/env bash
# Flash the target board with this project's image.
#
# Usage: tools/flash.sh <image-or-artifact>
#
# Placeholder: the flashing command is board-specific (e.g. a vendor flash
# script, fastboot, dd to SD). Replace the marked line with the one your board
# needs and document the prerequisites (recovery mode, cables) below.
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <image-or-artifact>" >&2
  exit 2
fi

IMAGE="$1"
[[ -f "$IMAGE" ]] || { echo "error: $IMAGE not found" >&2; exit 1; }

echo "TODO: replace with the board's flash command for $IMAGE" >&2
exit 1
