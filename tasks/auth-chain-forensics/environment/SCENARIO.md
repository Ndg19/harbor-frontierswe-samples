# lab-gateway runbook (training data)

Everything in `/app/evidence` is fictional.

## Timestamps

`auth.log` lines do not include a year. `access.log` does (`28/Oct/2025`). When you emit UTC ISO times for the report, use **2025-10-28** and take the clock time from whichever log line you are anchoring.

## Timeline milestones (in order)

1. Earliest failed SSH password attempt in `auth.log`
2. First `Accepted password` for the compromised user
3. The `sudo` line that copies key material under `/tmp/stage/`
4. First relevant HTTP GET in `access.log`
5. The PUT to the staging host in `access.log`
