The pinned code under `/app/repo` integrates a 1D heat equation with fixed-length steps and optional sensitivities of center temperature at step ends. That works for plain duration steps, but it never moves derivatives across step boundaries that stop on a center temperature threshold. Event end times depend on thermal diffusivity, so sensitivity comparisons across multi-step runs are misleading even when the forward profile looks fine.

Extend the model following `/app/TASK_CONTRACT.md`.

## Deliverables

1. **Event-aligned sensitivities.** With `Simulation.solve(calculate_sensitivities=True, calculate_event_sensitivities=True)`, return step results whose `derivatives.end_times` and `derivatives.end_centers` follow the contract: event steps include time sensitivities when the flag pair is on; legacy callers that omit `calculate_event_sensitivities` keep the old behavior.

2. **Package layout.** Ship the full importable tree at `/app/submission/heat1d`, matching the in-repo package layout and public entry points. Forward trajectories without the new flags should match today's behavior.

3. **Multi-step and repeat runs.** Concatenate steps in order. Running the same experiment twice with the same inputs should give identical per-step values and derivatives.

## Scope

In scope: scalar diffusivity `alpha`, the bundled sine-mode analytic solver and explicit grid integrator, Dirichlet boundaries, duration steps and center threshold events (`>=`). Out of scope: vector parameters, simultaneous events, drive cycles, network I/O.

Offline sources, the contract, and `/app/reproduce.py` are in the environment.
