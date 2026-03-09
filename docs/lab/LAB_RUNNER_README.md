# LAB_RUNNER_README

## Purpose
`tools/lab_runner.py` is a standalone autonomous lab harness.
It runs repeated prototype scenarios and writes comparison-friendly results.

It is diagnostic infrastructure, not game content production.

## Run commands
From repo root:

- Default run:
  - `python tools/lab_runner.py`
- Deterministic comparison run:
  - `python tools/lab_runner.py --variation-mode deterministic --seed 7 --iterations 20`
- Bounded variation run without archive:
  - `python tools/lab_runner.py --variation-mode bounded --seed 123 --iterations 40 --no-archive`

PowerShell-friendly examples:
- `python .\tools\lab_runner.py`
- `python .\tools\lab_runner.py --variation-mode deterministic --seed 7 --iterations 20`

## Config
Edit `tools/lab_config.json` to change:
- contexts
- fragments
- actions
- state presets
- iteration count
- seed
- delayed reaction toggle
- placeholder text toggle

## Output locations
- `docs/lab/results/latest_run.json`
- `docs/lab/results/latest_run.md`
- `docs/lab/results/latest_run.csv`
- optional archive: `docs/lab/results/archive/run_YYYYMMDD_HHMMSS.json`

## What to compare between runs
- unique reaction coverage
- no-op frequency
- delayed reaction frequency
- action-context sensitivity
- repeated state collapse count
- stagnation warnings

## Suspicious results
- very high no-op rate
- very low unique reaction coverage
- repeated state collapse spikes
- no observable difference across context/action pairs

## Promising results
- readable reaction differences across contexts/actions
- hints/fragments affecting outcomes
- delayed and immediate responses both showing useful behavior
- low stagnation warnings across repeated runs
