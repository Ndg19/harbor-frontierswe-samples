# Synthetic incident reconstruction (offline lab)

You are investigating a **fabricated** training incident on the host `lab-gateway`. All artifacts under `/app/evidence` are synthetic teaching data — not real customer systems, live addresses, or undisclosed vulnerabilities.

Read `/app/SCENARIO.md` for timestamp rules and milestone ordering.

## Artifacts

- `/app/evidence/auth.log` — OpenSSH authentication events
- `/app/evidence/access.log` — HTTP reverse-proxy style access lines
- `/app/evidence/cron/deployment` — user crontab snippet
- `/app/evidence/notes.txt` — analyst scratch pad (may be incomplete)

## Deliverables

Write the following under `/app/submission/`:

1. **`incident_report.json`** with keys:
   - `timeline`: array of five ISO-8601 UTC timestamps (`YYYY-MM-DDTHH:MM:SSZ`) in ascending order: first failed brute force, successful compromise, privilege escalation, lateral web access, data staging (see SCENARIO.md).
   - `compromised_account`: Unix username taken over on `lab-gateway`
   - `initial_vector`: use `ssh_password_spray` when evidence shows repeated SSH password failures followed by acceptance
   - `lateral_steps`: array of ≥ 2 short human-readable steps (wording is free-form)
   - `exfil_indicator`: hostname or URI from access logs for bulk transfer (must include the staging host used in the PUT line)
   - `recommended_controls`: array of ≥ 3 concrete hardening actions (wording is free-form)

2. **`ioc.txt`**: one indicator per line (IPv4, username, or file path that appears in the evidence), sorted lexicographically, no duplicates. Include the attacker IP, compromised username, staged key path, and source private-key path from the logs.

Scoring checks structured fields and IOC set equality; free-form sentences in `lateral_steps` and `recommended_controls` are not compared verbatim.

## Constraints

- Do not scan external networks or download threat intel feeds.
- Do not invent credentials beyond what logs support.
- Keep filenames exactly as listed above.
