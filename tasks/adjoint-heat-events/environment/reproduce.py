#!/usr/bin/env python3
"""Offline smoke check for the pinned upstream (forward only)."""

import sys

sys.path.insert(0, "/app/repo")
from heat1d import Experiment, Simulation, Step

exp = Experiment(
    steps=[
        Step(kind="duration", value=0.05),
        Step(kind="event", threshold=0.4),
    ]
)
out = Simulation(0.08, nx=0).solve(exp)
assert len(out["values"]["end_times"]) == 2
print("reproduce ok", out["values"]["end_times"])
