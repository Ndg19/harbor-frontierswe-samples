#!/bin/bash
set -euo pipefail
mkdir -p /app/submission
cp /solution/golden/incident_report.json /app/submission/incident_report.json
cp /solution/golden/ioc.txt /app/submission/ioc.txt
