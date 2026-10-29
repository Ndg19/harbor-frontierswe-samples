#!/bin/bash
set -euo pipefail
mkdir -p /logs/verifier
chmod 700 /logs/verifier /tests
python3 /tests/grade.py
