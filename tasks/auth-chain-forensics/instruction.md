Offline exercise only: the logs under `/app/evidence` describe a made-up incident on `lab-gateway`, not a live customer environment.

You are triaging that lab host. Read `/app/SCENARIO.md` for how to align timestamps across `auth.log` and `access.log`.

## Artifacts

- `/app/evidence/auth.log` — SSH auth
- `/app/evidence/access.log` — HTTP proxy-style lines
- `/app/evidence/cron/deployment` — cron snippet for the deploy user
- `/app/evidence/notes.txt` — partial analyst notes

## Deliverables

Write under `/app/submission/`:

**`incident_report.json`**

```json
{
  "timeline": ["<five ISO-8601 UTC times, ascending>"],
  "compromised_account": "<username>",
  "initial_vector": "<short label, e.g. ssh_password_spray>",
  "lateral_steps": ["...", "..."],
  "exfil_indicator": "<host or URI from the logs>",
  "recommended_controls": ["...", "...", "..."]
}
```

The five timeline entries are: first failed password spray, successful login, sudo/key staging, first suspicious HTTP GET, then the bulk upload/staging seen in access logs (see SCENARIO.md).

`lateral_steps` needs at least two short steps you can justify from the evidence. `recommended_controls` needs at least three concrete hardening ideas.

**`ioc.txt`** — one indicator per line (IP, username, or path that appears in the evidence), sorted, no duplicates. Include the source IP, the compromised account, the staged key path, and the private key path referenced in sudo.

## Constraints

Stay on the provided files. Do not run external scans or threat-intel lookups. Do not rename the output files.
