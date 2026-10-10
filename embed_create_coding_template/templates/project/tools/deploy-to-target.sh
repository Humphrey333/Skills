#!/usr/bin/env bash
# Copy a built artefact to the target board for debugging.
#
# Usage: TARGET=user@board tools/deploy-to-target.sh <build-dir> [remote-dir]
#
# Installs into a staging directory first (DESTDIR) so only the files this
# project installs are sent, then rsyncs the staging tree to the board.
set -euo pipefail

BUILD_DIR="${1:?usage: TARGET=user@board $0 <build-dir> [remote-dir]}"
REMOTE_DIR="${2:-/opt/@PROJECT_SLUG@}"
: "${TARGET:?set TARGET=user@host}"

STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

DESTDIR="$STAGE" cmake --install "$BUILD_DIR" --prefix /usr

rsync -av "$STAGE"/ "$TARGET:$REMOTE_DIR/"
