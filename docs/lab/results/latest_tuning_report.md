# TUNING VERDICT
Overall: **improved**
Confidence: **high**

## Baseline summary
- Score: `20.103`
- Unique reactions: `7`
- No-op frequency: `0.133`
- Readability score: `0.649`

## Best candidate summary
- Score: `22.6972`
- Unique reactions: `8`
- No-op frequency: `0.133`
- Readability score: `0.688`
- Score delta vs baseline: `2.5942`

## Main improvements
- `unique_reactions_triggered` changed by `1`
- `branch_differentiation_count` changed by `1`
- `action_context_sensitivity` changed by `1`
- `readability_score` changed by `0.039`
- `same_reaction_dominance` changed by `-0.033`
- `dead_path_ratio` changed by `-0.067`

## Main regressions
- none clear

## Parameters changed most
- `differentiation_weight`: `1.0` -> `1.1551`
- `hidden_state_weight`: `1.0` -> `0.8912`
- `delayed_threshold`: `0.55` -> `0.6335`
- `timing_weight`: `1.0` -> `0.9654`
- `repeated_state_penalty`: `1.0` -> `0.9685`
- `readability_weight`: `1.0` -> `0.969`
- `context_weight`: `1.0` -> `0.9794`
- `hint_weight`: `1.0` -> `0.9841`
- `no_op_penalty`: `1.0` -> `0.9891`
- `object_evidence_weight`: `1.0` -> `0.998`

- System still too repetitive? **no**
- Recommended next step: keep tuning if verdict is improved; expand scenarios only when stagnation warnings persist.

# SHOULD THE LAB SCOPE GROW?
- Verdict: **partly, add 2-3 more micro-scenarios**