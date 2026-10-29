# Harbor FrontierSWE-style sample tasks

Three original Harbor task folders for long-horizon agent evaluation:

| Task | Kind | Path |
|------|------|------|
| Adjoint heat with event-terminated steps | Scientific SWE | [tasks/adjoint-heat-events](tasks/adjoint-heat-events) |
| Slotted CBOR framing codec | Systems SWE | [tasks/slotted-cbor-framing](tasks/slotted-cbor-framing) |
| Synthetic auth-chain forensics | Security IR | [tasks/auth-chain-forensics](tasks/auth-chain-forensics) |

## Validate locally

```bash
python3 frontierswe-check.py tasks/adjoint-heat-events
python3 frontierswe-check.py tasks/slotted-cbor-framing
python3 frontierswe-check.py tasks/auth-chain-forensics

harbor run -p tasks/adjoint-heat-events -a oracle -y
harbor run -p tasks/adjoint-heat-events -a nop -y
```

Repeat `harbor run` for the other two tasks. Oracle should report `Mean: 1.000`; nop should report `Mean: 0.000`.

Author: **Nigusie Dessalegn** (`kingniguse81@gmail.com`).
