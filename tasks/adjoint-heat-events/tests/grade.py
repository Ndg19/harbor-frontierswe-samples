"""Grade heat1d submission against hidden fixtures."""

from __future__ import annotations

import json
import os
import signal
import stat
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
LOGS = Path("/logs/verifier")
SUBMISSION = Path("/app/submission")
WEIGHTS = {"1": 15, "2": 20, "3": 20, "4": 20, "5": 10, "6": 15}


def read_json(path: Path) -> dict:
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd) as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > 4_000_000:
            raise ValueError("fixture too large")
        return json.loads(stream.read())


def compare(actual, expected, absolute, relative=0.0):
    a = np.asarray(actual, dtype=float)
    b = np.asarray(expected, dtype=float)
    if a.shape != b.shape:
        raise ValueError(f"shape mismatch {a.shape} vs {b.shape}")
    delta = np.abs(a - b)
    if np.any(delta > absolute + relative * np.abs(b)):
        raise ValueError(f"error {float(delta.max())} > tol")
    return float(delta.max()) if delta.size else 0.0


def main() -> None:
    LOGS.mkdir(exist_ok=True, parents=True)
    if not (SUBMISSION / "heat1d" / "__init__.py").is_file():
        (LOGS / "reward.txt").write_text("0")
        print(json.dumps({"error": "missing submission package"}))
        return

    base = Path(tempfile.mkdtemp(prefix="heat-eval-"))
    os.chmod(base, 0o755)
    probe = base / "probe.py"
    probe.write_text((HERE / "probe.py").read_text())
    os.chmod(probe, 0o644)
    counter = 0

    def invoke(name: str, config: dict) -> dict:
        nonlocal counter
        counter += 1
        src = base / f"in-{counter}.json"
        src.write_text(json.dumps(config))
        outdir = base / f"out-{counter}"
        outdir.mkdir(mode=0o700)
        os.chown(outdir, 65534, 65534)
        output = outdir / "result.json"
        env = {
            "PATH": "/usr/local/bin:/usr/bin:/bin",
            "HOME": str(outdir),
            "PYTHONPATH": str(SUBMISSION),
            "PYTHONNOUSERSITE": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        proc = subprocess.Popen(
            [sys.executable, str(probe), "--input", str(src), "--output", str(output)],
            cwd=outdir,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            user=65534,
            group=65534,
            extra_groups=[],
            start_new_session=True,
        )
        try:
            code = proc.wait(timeout=300)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
            raise ValueError(f"{name}: timeout") from None
        if code:
            raise ValueError(f"{name}: exit {code}")
        return read_json(output)

    def check(name: str) -> dict:
        fixture = read_json(HERE / "fixtures" / f"{name}.json")
        cfg = fixture["input"]
        expected = fixture["expected"]
        if name == "resume":
            first = invoke(name, cfg)
            second = invoke(name, cfg)
            for label, actual in (("run1", first), ("run2", second)):
                for key in ("values", "derivatives"):
                    for field in expected[key]:
                        compare(
                            actual[key][field],
                            expected[key][field],
                            1e-4 if field == "end_times" else 3e-4,
                            2e-4 if field == "end_times" else 0.0,
                        )
            for key in ("values", "derivatives"):
                for field in expected[key]:
                    compare(first[key][field], second[key][field], 1e-8)
            return {"idempotent": True}
        actual = invoke(name, cfg)
        nx = int(cfg.get("nx", 0))
        analytic = nx <= 0
        v_t = 1e-4 if analytic else 2e-2
        v_c = 1e-5 if analytic else 5e-4
        d_t = (1e-5, 2e-4) if analytic else (5e-2, 0.0)
        d_c = 3e-4 if analytic else 5e-3
        detail = {}
        detail["end_times"] = compare(
            actual["values"]["end_times"], expected["values"]["end_times"], v_t
        )
        detail["end_centers"] = compare(
            actual["values"]["end_centers"], expected["values"]["end_centers"], v_c
        )
        detail["d_end_times"] = compare(
            actual["derivatives"]["end_times"],
            expected["derivatives"]["end_times"],
            d_t[0],
            d_t[1],
        )
        detail["d_end_centers"] = compare(
            actual["derivatives"]["end_centers"],
            expected["derivatives"]["end_centers"],
            d_c,
        )
        return detail

    groups = {
        "1": ["analytic-duration"],
        "2": ["analytic-event"],
        "3": ["multi-step"],
        "4": ["grid-event"],
        "5": ["compat"],
        "6": ["resume"],
    }
    outcomes = {}
    diagnostics = {}
    for gid, cases in groups.items():
        try:
            diagnostics[gid] = {n: check(n) for n in cases}
            outcomes[gid] = 1
        except (ValueError, KeyError, TypeError, OSError) as exc:
            outcomes[gid] = 0
            diagnostics[gid] = {"error": str(exc)}

    reward = int(all(outcomes.values()))
    report = {
        "task_id": "adjoint-heat-events",
        "reward": reward,
        "weighted_score": sum(WEIGHTS[k] * outcomes[k] for k in outcomes) / 100,
        "per_criterion": outcomes,
        "diagnostics": diagnostics,
    }
    (LOGS / "criteria.json").write_text(json.dumps(report, indent=2))
    (LOGS / "reward.txt").write_text(str(reward))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
