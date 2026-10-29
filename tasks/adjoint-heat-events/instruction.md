Extend the pinned heat-equation codebase in `/app/repo` so scalar-parameter sensitivities stay consistent when experiment steps terminate on a **temperature threshold event** at the domain center.

The starter implementation integrates a 1D heat model with fixed-duration steps and can optionally report sensitivities of the center temperature at step ends. It does **not** move derivatives through event-triggered step boundaries: end times depend on the thermal diffusivity parameter, so comparisons across discharge-style step sequences are wrong even when the forward temperature trace looks fine.

Implement the opt-in API and derivative conventions in `/app/TASK_CONTRACT.md`. With `Simulation.solve(calculate_sensitivities=True, calculate_event_sensitivities=True)`, processed outputs must use sensitivities at fixed absolute time (including effects of earlier moving transitions). Provide `end_time_sensitivities` for step-ending times and keep center-temperature sensitivities aligned with the contract. Preserve semantics across multi-step experiments, resumed solves, and concatenated results. Without the event flag, legacy behavior must remain unchanged.

Supported scope: single scalar diffusivity parameter `alpha`, sine-mode analytic model and uniform-grid explicit integrator shipped in-repo, constant Dirichlet boundaries, steps that are either fixed duration or center threshold crossings (`>=`), monotonic forward integration. Drive cycles, multiple simultaneous events, and vector parameters are out of scope.

Deliver the complete importable package at `/app/submission/heat1d` (mirror the in-repo layout). Keep native public entry points and forward trajectories. Upstream sources, contract, and an offline reproduction script are available in the environment; no network access is required at solve time.

Verification runs isolated numeric probes (analytic and grid cases, multi-step and resume flows, compatibility without the event flag) with tolerances defined in the contract. Each probe has a five-minute CPU budget on two cores. A full pass requires every probe group to succeed.
