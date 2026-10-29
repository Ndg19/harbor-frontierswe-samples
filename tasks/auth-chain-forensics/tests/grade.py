"""Verify synthetic IR deliverables."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

LOGS = Path("/logs/verifier")
SUBMISSION = Path("/app/submission")
HERE = Path(__file__).resolve().parent
GOLDEN_REPORT = json.loads((HERE / "golden_report.json").read_text())
GOLDEN_IOC = (HERE / "golden_ioc.txt").read_text()


def normalize_report(data: dict) -> bytes:
    timeline = [str(x) for x in data["timeline"]]
    if timeline != sorted(timeline):
        raise ValueError("timeline not ascending")
    if len(timeline) != 5:
        raise ValueError("timeline must contain five entries")
    lateral = [str(x) for x in data["lateral_steps"]]
    if len(lateral) < 2:
        raise ValueError("lateral_steps too short")
    controls = [str(x) for x in data["recommended_controls"]]
    if len(controls) < 3:
        raise ValueError("recommended_controls too short")
    normalized = {
        "timeline": timeline,
        "compromised_account": str(data["compromised_account"]),
        "initial_vector": str(data["initial_vector"]),
        "lateral_steps": lateral,
        "exfil_indicator": str(data["exfil_indicator"]),
        "recommended_controls": controls,
    }
    return json.dumps(normalized, sort_keys=True, separators=(",", ":")).encode()


def normalize_ioc(text: str) -> bytes:
    lines = sorted({ln.strip() for ln in text.splitlines() if ln.strip()})
    if len(lines) < 3:
        raise ValueError("ioc.txt needs at least three indicators")
    return ("\n".join(lines) + "\n").encode()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    report_path = SUBMISSION / "incident_report.json"
    ioc_path = SUBMISSION / "ioc.txt"
    if not report_path.is_file() or not ioc_path.is_file():
        (LOGS / "reward.txt").write_text("0")
        print(json.dumps({"error": "missing deliverables"}))
        return
    report = json.loads(report_path.read_text())
    rep_hash = sha256(normalize_report(report))
    ioc_hash = sha256(normalize_ioc(ioc_path.read_text()))
    expected = json.loads((HERE / "expected.json").read_text())
    ok = rep_hash == expected["report_sha256"] and ioc_hash == expected["ioc_sha256"]
    reward = 1 if ok else 0
    out = {
        "task_id": "auth-chain-forensics",
        "reward": reward,
        "report_sha256": rep_hash,
        "ioc_sha256": ioc_hash,
    }
    (LOGS / "criteria.json").write_text(json.dumps(out, indent=2))
    (LOGS / "reward.txt").write_text(str(reward))
    print(json.dumps(out))


if __name__ == "__main__":
    main()
