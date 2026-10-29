# Harbor FrontierSWE-style sample tasks

Three original Harbor task folders for long-horizon agent evaluation:

| Task | Kind | Path |
|------|------|------|
| Adjoint heat with event-terminated steps | Scientific SWE | [tasks/adjoint-heat-events](tasks/adjoint-heat-events) |
| Slotted CBOR framing codec | Systems SWE | [tasks/slotted-cbor-framing](tasks/slotted-cbor-framing) |
| Synthetic auth-chain forensics | Security IR | [tasks/auth-chain-forensics](tasks/auth-chain-forensics) |

Client submission brief (RustLabs): [docs/client/forms.md](docs/client/forms.md)

## Validate locally

```bash
python3 frontierswe-check.py tasks/adjoint-heat-events
python3 frontierswe-check.py tasks/slotted-cbor-framing
python3 frontierswe-check.py tasks/auth-chain-forensics
```

Harbor (use a **new** `--job-name` on every run so `jobs/` does not collide):

```bash
harbor run -p tasks/adjoint-heat-events -a oracle -y --job-name heat-oracle-final
harbor run -p tasks/adjoint-heat-events -a nop -y --job-name heat-nop-final
harbor run -p tasks/slotted-cbor-framing -a oracle -y --job-name cbor-oracle-final
harbor run -p tasks/slotted-cbor-framing -a nop -y --job-name cbor-nop-final
harbor run -p tasks/auth-chain-forensics -a oracle -y --job-name forensics-oracle-final
harbor run -p tasks/auth-chain-forensics -a nop -y --job-name forensics-nop-final
```

Oracle should report `Mean: 1.000`; nop should report `Mean: 0.000`.

Author: **Nigusie Dessalegn** (`kingniguse81@gmail.com`).
