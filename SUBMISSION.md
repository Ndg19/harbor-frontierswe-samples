# Form submission record

**Repo:** https://github.com/Ndg19/harbor-frontierswe-samples  
**Author:** Nigusie Dessalegn (`kingniguse81@gmail.com`)

---

## Task 1: adjoint-heat-events

- **Kind:** Long-horizon SWE — scientific / numerical computing
- **Summary:** Extend a pinned 1D heat-equation experiment driver so scalar diffusivity sensitivities remain correct when steps end on a center temperature threshold event. The verifier runs isolated numeric probes (analytic, grid, multi-step, idempotent resume, legacy compat) via subprocess; binary reward requires every probe group to pass.
- **Engineer time (form):** 8–16 hours
- **Link:** https://github.com/Ndg19/harbor-frontierswe-samples/tree/main/tasks/adjoint-heat-events
- **Checker:** `FSWE-CHECK v1 PASS ndg19/adjoint-heat-events a77ac2ff320e`
- **Oracle Mean:** 1.000
- **Nop Mean:** 0.000

---

## Task 2: slotted-cbor-framing

- **Kind:** Long-horizon SWE — systems / serialization (codec-adjacent)
- **Summary:** Implement CRC32C slotted framing and a CLI (`encode`, `decode`, `stream-decode`) on top of a restricted CBOR subset. The verifier compares canonical encoded bytes, round-trip files, stream JSON lines, and error codes for bad CRC, truncation, duplicate slots, and oversized length fields.
- **Engineer time (form):** 6–12 hours
- **Link:** https://github.com/Ndg19/harbor-frontierswe-samples/tree/main/tasks/slotted-cbor-framing
- **Checker:** `FSWE-CHECK v1 PASS ndg19/slotted-cbor-framing 130d75e9286c`
- **Oracle Mean:** 1.000
- **Nop Mean:** 0.000

---

## Task 3: auth-chain-forensics

- **Kind:** Security — incident response / forensics (synthetic lab)
- **Summary:** Reconstruct a fictional SSH spray → compromise → sudo staging → HTTP exfil chain from offline logs; deliver `incident_report.json` and `ioc.txt`. The verifier applies a hidden rubric (timeline, account, vector, exfil host, IOC set; free-form narrative fields need only meet length/non-empty rules).
- **Engineer time (form):** 3–6 hours
- **Link:** https://github.com/Ndg19/harbor-frontierswe-samples/tree/main/tasks/auth-chain-forensics
- **Checker:** `FSWE-CHECK v1 PASS ndg19/auth-chain-forensics 61e09e7e1f47`
- **Oracle Mean:** 1.000
- **Nop Mean:** 0.000

---

## Local re-check

```bash
python3 frontierswe-check.py tasks/<name>
harbor run -p tasks/<name> -a oracle -y --job-name my-oracle-run
harbor run -p tasks/<name> -a nop -y --job-name my-nop-run
```

Use a fresh `--job-name` each Harbor run (do not type angle brackets).
