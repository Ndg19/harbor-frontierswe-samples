# Heat1D event sensitivity contract

## Parameters

- `alpha`: scalar thermal diffusivity (> 0).
- Optional grid size `nx` (integer ≥ 11). When `nx` is 0, use the single sine-mode analytic forward model with `L = 1` and amplitude `1`.
- Initial condition: `u(x,0) = sin(π x / L)` with Dirichlet `u(0)=u(L)=0`.

## Experiment steps

Each step is either:

- `{"kind": "duration", "value": <seconds>}` — integrate from the current absolute time for exactly `value` seconds.
- `{"kind": "event", "threshold": <temperature>}` — integrate until the center sample `u(L/2)` is **≥ threshold** (first crossing).

Steps run sequentially; step *k* starts from the end state of step *k−1* at the same absolute time baseline (state resets to the analytic IC at time zero only for the first step — subsequent steps continue from the field reached at the prior step end in grid mode; analytic mode treats each step as advancing absolute time with the same decaying sine mode).

## API

```python
Simulation(alpha, L=1.0, amplitude=1.0, nx=0).solve(
    Experiment(steps=[...]),
    calculate_sensitivities=False,
    calculate_event_sensitivities=False,
)
```

Returns:

```python
{
  "values": {"end_times": [float, ...], "end_centers": [float, ...]},
  "derivatives": {"end_times": [float, ...], "end_centers": [float, ...]},
}
```

When `calculate_sensitivities` is false, all derivative entries must be `0.0`.

When `calculate_sensitivities` is true and `calculate_event_sensitivities` is false (legacy):

- For **duration** steps: populate `derivatives/end_centers`; `derivatives/end_times` entry is `0`.
- For **event** steps: populate `derivatives/end_centers` only; **do not** move `derivatives/end_times` (must be `0`).

When both flags are true:

- Duration steps behave as above.
- Event steps must populate **both** `derivatives/end_times` (sensitivity of the event absolute time w.r.t. `alpha`) and set `derivatives/end_centers` to `0` for that step (center is locked to the threshold).

## Tolerances used by verification

| Field | Analytic model | Grid (`nx ≥ 21`) |
|-------|----------------|------------------|
| `values/end_times` | 1e-4 | 2e-2 |
| `values/end_centers` | 1e-5 | 5e-4 |
| `derivatives/end_times` | 2e-4 relative + 1e-5 abs | 5e-2 |
| `derivatives/end_centers` | 3e-4 | 5e-3 |

## Resume / multi-step

Multi-step experiments concatenate step results in order. A resumed experiment repeats the same step list; implementations must return identical step-wise values and derivatives for identical inputs (idempotent).
