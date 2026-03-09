# RESULTS_FORMAT

## Standard outputs

### `latest_run.json`
Contains:
- run metadata (`run_name`, `seed`, `scenario_repeats`)
- candidate parameters
- metrics
- full trace

### `latest_run.csv`
Flat trace table with:
- iteration/step/scenario
- context
- action
- selected reaction
- immediate/delayed
- fragments
- hidden-state snapshot
- readable notes

### `latest_run.md`
Human summary for quick comparison.

## Tuning outputs

### `latest_tuning_report.json`
Contains:
- tuning metadata (generations, population, seed)
- verdict (`overall`, `confidence`, scope-growth verdict)
- baseline summary + score
- best candidate summary + score
- score delta
- generation history

### `latest_tuning_report.md`
Human-facing verdict format:
- `# TUNING VERDICT`
- Overall: improved / worsened / unclear
- Confidence: high / medium / low
- baseline and best summaries
- main improvements/regressions
- parameter changes
- scope-growth recommendation

### `best_candidate.json`
Contains:
- best candidate parameters
- best score and metrics
- full best trace

### `baseline_vs_best.md`
Quick side-by-side metric delta view.

## Trace schema (used in standard and best candidate traces)
Each step includes:
- `iteration_id`
- `step_index`
- `scenario_id`
- `time_context`
- `known_fragments`
- `hidden_state`
- `chosen_action`
- `eligible_reactions`
- `selected_reaction`
- `source` (immediate/delayed)
- `immediate_or_delayed`
- `newly_unlocked_information`
- `notes`
- `next_hidden_state`
- `repeated_state_collapse`

## Metrics emphasis
Evaluation is multi-signal.
Variable movement alone is not sufficient; readability proxies and differentiation metrics are included in tuning score.
