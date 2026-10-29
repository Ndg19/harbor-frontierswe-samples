#!/bin/bash
set -euo pipefail
cd /app/repo
git init -q 2>/dev/null || true
git add -A 2>/dev/null || true
git commit -q -m base --allow-empty 2>/dev/null || true
git apply /solution/feature.patch
cp -R slotted_cbor /app/submission/slotted_cbor
