# Synthetic incident reconstruction (offline lab)

You are investigating a **fabricated** training incident on the host `lab-gateway`. All artifacts under `/app/evidence` are synthetic teaching data — not real customer systems, live addresses, or undisclosed vulnerabilities.

## Artifacts

- `/app/evidence/auth.log` — OpenSSH authentication events
- `/app/evidence/access.log` — HTTP reverse-proxy style access lines
- `/app/evidence/cron/deployment` — user crontab snippet
- `/app/evidence/notes.txt` — analyst scratch pad (may be incomplete)

## Deliverables

Write the following under `/app/submission/`:

1. **`incident_report.json`** with keys:
   - `timeline`: array of ISO-8601 UTC timestamps (`YYYY-MM-DDTHH:MM:SSZ`) in ascending order describing five milestones: first failed brute force, successful compromise, privilege escalation, lateral web access, data staging.
   - `compromised_account`: Unix username taken over on `lab-gateway`
   - `initial_vector`: short string (`ssh_password_spray`, `web_exploit`, etc.)
   - `lateral_steps`: array of short human-readable steps (≥ 2 entries)
   - `exfil_indicator`: hostname or URI observed in access logs for bulk transfer
   - `recommended_controls`: array of ≥ 3 concrete hardening actions

2. **`ioc.txt`**: one indicator per line (IPv4, username, or file path mentioned in evidence), sorted lexicographically, no duplicates.

Ground truth is **derivable only from the provided evidence**. Verification compares normalized content to expected answers; every required field must match for a pass.

## Constraints

- Do not scan external networks or download threat intel feeds.
- Do not invent credentials beyond what logs support.
- Keep filenames exactly as listed above.
