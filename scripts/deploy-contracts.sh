#!/usr/bin/env bash
set -euo pipefail

if command -v initia >/dev/null 2>&1; then
  initia move publish --package-dir contracts --profile local
else
  echo "Initia CLI not found. Install initia and rerun:"
  echo "  initia move publish --package-dir contracts --profile local"
fi
