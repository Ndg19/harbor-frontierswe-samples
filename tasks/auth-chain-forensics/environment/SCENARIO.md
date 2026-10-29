# Synthetic lab scenario (agent-visible)

All evidence is fictional training material for `lab-gateway`.

## Timestamp rule

`auth.log` lines omit the year. **`access.log` uses year 2025** (`28/Oct/2025`). When building ISO-8601 UTC timestamps for the report timeline, use **2025-10-28** with the time-of-day taken from the relevant `auth.log` or `access.log` line (UTC).

## Expected milestone order

1. First failed brute-force attempt (earliest failed SSH password in `auth.log`)
2. Successful SSH compromise (`Accepted password`)
3. Privilege escalation (`sudo` copying key material)
4. Lateral web access (first suspicious HTTP GET in `access.log`)
5. Data staging (bulk PUT / exfil hostname in `access.log`)
