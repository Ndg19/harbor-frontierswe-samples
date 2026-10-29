Tasks you built: FrontierSWE-style and security
Hey Nigussie,

A client wants to see samples of two kinds of evaluation task before a new project starts. If you've already built one yourself, we'd like to see it.

Long-horizon software engineering tasks in the FrontierSWE format. FrontierSWE is a public benchmark where an agent gets up to 20 hours on one hard problem: reimplementing a compiler or a database, optimising a codec, scientific computing. Read frontierswe.com and a few tasks in its GitHub repo.
Cybersecurity and red-team tasks in the same format. Isolated security labs, incident-response or forensics scenarios, web, IAM and cloud security, prompt injection, rogue-agent behavior, unauthorized tool use, or an agent breaking out of its system boundaries.
Each task is a Harbor task folder like the FrontierSWE ones: instruction.md, task.toml, a Docker environment, a verifier that writes a score, and a reference solution in solution/solve.sh.

Before you send, three checks for every task:

Run our checker on the folder and fix every FAIL: frontierswe-check.py (Python 3.11+, no installs). It catches the small things that get tasks rejected: missing files, the solution or hidden tests visible to the agent, a short agent budget, leaked keys, paths from your machine.
harbor run -p path/to/task -a oracle: the reference solution should score full marks (Harbor prints Mean: 1.000).
harbor run -p path/to/task -a nop: an agent that does nothing should score 0 (Mean: 0.000).
The form asks for the checker's PASS line and both scores, with a link to the folder. Send up to three by Friday 30 October, 12:00 ET. We review them as they arrive, so earlier is better.

Please note: there is no payment for samples and no guarantee of paid work. The client wants to see examples first. If they like yours, you'll be first in line when the project starts.

Only send work you own. No client or employer material, and no real credentials, live targets or undisclosed vulnerabilities.

Open the form ↗
