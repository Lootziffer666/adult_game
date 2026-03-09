# LAB_RUNNER_README

## Purpose
`tools/lab_runner.py` is a standalone autonomous lab harness.
It runs repeated prototype scenarios and supports a bounded tuning loop over parameter candidates.

It is diagnostic infrastructure, not content production.

## Run commands
From repo root:

- Standard scenario run:
  - `python tools/lab_runner.py`
- Deterministic standard run:
  - `python tools/lab_runner.py --variation-mode deterministic --seed 7`
- Autonomous tuning run:
  - `python tools/lab_runner.py --tune`
- Tune with explicit bounds:
  - `python tools/lab_runner.py --tune --generations 8 --population 10 --mutation 0.1 --seed 17`

PowerShell-friendly examples:
- `python .\tools\lab_runner.py`
- `python .\tools\lab_runner.py --tune --generations 8 --population 10 --mutation 0.1 --seed 17`

## Tunable parameters (bounded)
Defined in `tools/lab_config.json` under `tuning.base_parameters`:
- `hint_weight`
- `context_weight`
- `timing_weight`
- `hidden_state_weight`
- `delayed_threshold`
- `no_op_penalty`
- `repeated_state_penalty`
- `differentiation_weight`
- `readability_weight`
- `object_evidence_weight`

## Scenario bundle
The config includes 10 generic micro-scenarios (non-canonical), including:
- wrong/right timing with and without fragments
- delayed reaction cases
- context privacy shifts
- repeated-action fatigue pattern
- bounded object/evidence tests
- return-later and memory-followup patterns

## Output locations
Standard run:
- `docs/lab/results/latest_run.json`
- `docs/lab/results/latest_run.md`
- `docs/lab/results/latest_run.csv`

Tuning run:
- `docs/lab/results/latest_tuning_report.json`
- `docs/lab/results/latest_tuning_report.md`
- `docs/lab/results/best_candidate.json`
- `docs/lab/results/baseline_vs_best.md`

Archive:
- optional `docs/lab/results/archive/run_YYYYMMDD_HHMMSS.json`

## What to compare
- unique reaction coverage
- no-op frequency
- delayed reaction usage quality
- action-context sensitivity
- repeated state collapse count
- readability score proxy
- stagnation warnings

## Suspicious results
- high no-op and high dominance by one reaction
- low unique reaction coverage
- repeated state collapse spikes
- many context/action pairs with no meaningful difference

## Promising results
- readable reaction differences across scenarios
- fragments/evidence affecting outcomes
- delayed reactions used meaningfully
- improved best-vs-baseline score without readability collapse
