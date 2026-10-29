"""Verify synthetic IR deliverables against a hidden rubric."""

from __future__ import annotations

import json
from pathlib import Path

LOGS = Path("/logs/verifier")
SUBMISSION = Path("/app/submission")
HERE = Path(__file__).resolve().parent


def main() -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    rubric = json.loads((HERE / "rubric.json").read_text())
    report_path = SUBMISSION / "incident_report.json"
    ioc_path = SUBMISSION / "ioc.txt"
    errors: list[str] = []

    if not report_path.is_file():
        errors.append("missing incident_report.json")
    if not ioc_path.is_file():
        errors.append("missing ioc.txt")
    if errors:
        (LOGS / "reward.txt").write_text("0")
        print(json.dumps({"errors": errors}))
        return

    report = json.loads(report_path.read_text())
    timeline = [str(x) for x in report.get("timeline", [])]
    if timeline != rubric["timeline"]:
        errors.append("timeline mismatch")
    if str(report.get("compromised_account", "")) != rubric["compromised_account"]:
        errors.append("compromised_account mismatch")
    if str(report.get("initial_vector", "")) != rubric["initial_vector"]:
        errors.append("initial_vector mismatch")
    exfil = str(report.get("exfil_indicator", ""))
    if rubric["exfil_indicator_substr"] not in exfil:
        errors.append("exfil_indicator mismatch")
    lateral = report.get("lateral_steps", [])
    if not isinstance(lateral, list) or len(lateral) < 2 or not all(str(x).strip() for x in lateral):
        errors.append("lateral_steps invalid")
    controls = report.get("recommended_controls", [])
    if not isinstance(controls, list) or len(controls) < 3 or not all(str(x).strip() for x in controls):
        errors.append("recommended_controls invalid")

    ioc_lines = sorted({ln.strip() for ln in ioc_path.read_text().splitlines() if ln.strip()})
    expected_ioc = sorted(rubric["ioc_lines"])
    if ioc_lines != expected_ioc:
        errors.append("ioc.txt mismatch")

    reward = 0 if errors else 1
    out = {"task_id": "auth-chain-forensics", "reward": reward, "errors": errors}
    (LOGS / "criteria.json").write_text(json.dumps(out, indent=2))
    (LOGS / "reward.txt").write_text(str(reward))
    print(json.dumps(out))


if __name__ == "__main__":
    main()
