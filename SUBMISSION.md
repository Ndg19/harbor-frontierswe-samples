# Form submission (one form, three task rows)

Use **one** RustLabs form submission. Fill **Task 1**, **Task 2**, and **Task 3** on the same page. Same repo; different folder links below.

Repo: https://github.com/Ndg19/harbor-frontierswe-samples

---

## Task 1 — adjoint-heat-events

- **Kind:** Long-horizon SWE (scientific computing)
- **Description (form):** Fix 1D heat-equation parameter sensitivities when steps end on a center temperature event; deliver `heat1d` under `/app/submission` per TASK_CONTRACT. Verifier runs numeric fixtures (analytic, grid, multi-step, repeat-run idempotence, legacy flag behavior).
- **Engineer time:** 8–16 hours
- **Link:** https://github.com/Ndg19/harbor-frontierswe-samples/tree/main/tasks/adjoint-heat-events
- **Checker:** `FSWE-CHECK v1 PASS ndg19/adjoint-heat-events ab232a66fa53`
- **Oracle:** 1.0 — **Nop:** 0.0

---

## Task 2 — slotted-cbor-framing

- **Kind:** Long-horizon SWE (systems / serialization)
- **Description (form):** Add CRC32C slotted framing and encode/decode/stream-decode CLI on a restricted CBOR subset. Verifier checks golden bytes, round-trip, stream output, and spec error codes on corrupt vectors.
- **Engineer time:** 6–12 hours
- **Link:** https://github.com/Ndg19/harbor-frontierswe-samples/tree/main/tasks/slotted-cbor-framing
- **Checker:** `FSWE-CHECK v1 PASS ndg19/slotted-cbor-framing 7dead72cc443`
- **Oracle:** 1.0 — **Nop:** 0.0

---

## Task 3 — auth-chain-forensics

- **Kind:** Security (incident response / forensics)
- **Description (form):** Reconstruct a synthetic SSH-to-exfil timeline from offline logs; write `incident_report.json` and `ioc.txt`. Verifier uses a field rubric (times, account, vector, exfil host, IOC set).
- **Engineer time:** 3–6 hours
- **Link:** https://github.com/Ndg19/harbor-frontierswe-samples/tree/main/tasks/auth-chain-forensics
- **Checker:** `FSWE-CHECK v1 PASS ndg19/auth-chain-forensics c86b557ffd5d`
- **Oracle:** 1.0 — **Nop:** 0.0

---

Harbor was last verified at oracle 1.0 / nop 0.0 before this copy edit; re-run if you change Docker or verifiers.

```bash
harbor run -p tasks/<name> -a oracle -y --job-name my-oracle-run
harbor run -p tasks/<name> -a nop -y --job-name my-nop-run
```
