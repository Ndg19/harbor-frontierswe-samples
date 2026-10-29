#!/usr/bin/env python3
"""Run one heat1d probe configuration."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from heat1d import Experiment, Simulation, Step


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    config = json.loads(Path(args.input).read_text())
    steps = []
    for raw in config["steps"]:
        if raw["kind"] == "duration":
            steps.append(Step(kind="duration", value=raw["value"]))
        else:
            steps.append(Step(kind="event", threshold=raw["threshold"]))
    flags = config.get("flags", {})
    sim = Simulation(
        config["alpha"],
        L=config.get("L", 1.0),
        amplitude=config.get("amplitude", 1.0),
        nx=config.get("nx", 0),
    )
    out = sim.solve(
        Experiment(steps=steps),
        calculate_sensitivities=flags.get("calculate_sensitivities", False),
        calculate_event_sensitivities=flags.get("calculate_event_sensitivities", False),
    )
    Path(args.output).write_text(json.dumps(out))


if __name__ == "__main__":
    main()
