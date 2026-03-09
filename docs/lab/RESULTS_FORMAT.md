# RESULTS_FORMAT

## `latest_run.json`
Contains:
- `run_metadata`
  - run name
  - seed
  - iterations
  - max steps
  - variation mode
  - timestamp
- `metrics`
  - total_iterations
  - total_steps
  - unique_reactions_triggered
  - unique_reaction_ids
  - reactions_never_triggered
  - branch_differentiation_count
  - empty_noop_reaction_frequency
  - delayed_reaction_frequency
  - immediate_reaction_count
  - delayed_reaction_count
  - hint_usefulness_score
  - action_context_sensitivity
  - repeated_state_collapse_count
  - loop_stagnation_warnings
  - contexts_actions_with_no_meaningful_difference
- `trace`
  - per-step causality records

## Trace entry schema
Each step includes:
- `iteration_id`
- `step_index`
- `time_context`
- `known_fragments`
- `hidden_state`
- `chosen_action`
- `eligible_reactions`
- `selected_reaction`
- `source` (immediate/delayed)
- `immediate_or_delayed`
- `newly_unlocked_information`
- `notes` (placeholder-readable)
- `next_hidden_state`

## `latest_run.csv`
Flat table for quick filtering/sorting:
- iteration/step
- context
- action
- selected reaction
- immediate/delayed
- fragments
- hidden state snapshot
- notes

## `latest_run.md`
Short comparison summary for humans:
- metadata
- key metrics
- untriggered reactions
- no-difference context/action pairs
- stagnation warnings
