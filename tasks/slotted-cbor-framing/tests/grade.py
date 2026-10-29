"""Grade slotted_cbor submission via CLI probes."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LOGS = Path("/logs/verifier")
SUBMISSION = Path("/app/submission")
HERE = Path(__file__).resolve().parent
VECTORS = HERE / "vectors"


def run_cli(args: list[str], *, expect_code: int = 0) -> subprocess.CompletedProcess:
    env = {"PYTHONPATH": str(SUBMISSION), "PYTHONDONTWRITEBYTECODE": "1"}
    proc = subprocess.run(
        [sys.executable, "-m", "slotted_cbor", *args],
        capture_output=True,
        text=True,
        env=env,
    )
    if proc.returncode != expect_code:
        raise ValueError(f"CLI {args} expected {expect_code} got {proc.returncode}: {proc.stderr}")
    return proc


def main() -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    pkg = SUBMISSION / "slotted_cbor"
    if not (pkg / "frame.py").is_file():
        (LOGS / "reward.txt").write_text("0")
        print(json.dumps({"error": "missing submission"}))
        return

    work = Path(tempfile.mkdtemp(prefix="slcb-"))
    out_stream = work / "out.bin"
    out_dir = work / "decoded"
    manifest = Path("/app/data/demo/manifest.json")

    run_cli(["encode", "--manifest", str(manifest), "--output", str(out_stream)])
    golden = VECTORS / "golden.bin"
    if out_stream.read_bytes() != golden.read_bytes():
        raise ValueError("encoded bytes mismatch golden")

    run_cli(["decode", "--input", str(out_stream), "--output-dir", str(out_dir)])
    if (out_dir / "alpha.txt").read_text() != "alpha payload\n":
        raise ValueError("alpha decode mismatch")
    if (out_dir / "beta.bin").read_bytes() != bytes(range(16)):
        raise ValueError("beta decode mismatch")

    proc = run_cli(["stream-decode", "--input", str(out_stream)])
    lines = [json.loads(x) for x in proc.stdout.splitlines() if x.strip()]
    if len(lines) != 2 or lines[0]["slot"] != 1:
        raise ValueError("stream-decode output wrong")

    run_cli(["decode", "--input", str(VECTORS / "bad_crc.bin"), "--output-dir", str(work / "x")], expect_code=3)
    run_cli(["decode", "--input", str(VECTORS / "truncated.bin"), "--output-dir", str(work / "y")], expect_code=2)

    reward = 1
    report = {"task_id": "slotted-cbor-framing", "reward": reward, "full_pass": True}
    (LOGS / "criteria.json").write_text(json.dumps(report, indent=2))
    (LOGS / "reward.txt").write_text(str(reward))
    print(json.dumps(report))


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        LOGS.mkdir(parents=True, exist_ok=True)
        (LOGS / "reward.txt").write_text("0")
        print(json.dumps({"error": str(exc)}))
