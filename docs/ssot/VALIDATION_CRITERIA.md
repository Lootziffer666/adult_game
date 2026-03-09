# VALIDATION_CRITERIA

## Success criteria
- Hidden-state logic is coherent and inspectable.
- Placeholder reactions are readable and tied to state/context changes.
- At least one repeated action path yields meaningfully different outcomes under changed conditions.
- Players can identify "why this changed" with lightweight support output.

## Failure criteria
- Variables change but reactions feel arbitrary or invisible.
- Loop requires brute-force guessing without interpretable signals.
- Repeated attempts feel like chores with no perceived learning.
- Output depends on fixed narrative context not available in current lab scope.

## Ambiguous / partial results
- Logic appears correct in debug traces but reactions remain unclear to humans.
- Reactions are readable only with debug on.
- Improvements depend on over-specific placeholder cast/story assumptions.

## Observations to gather from runs
- Which cues players used for interpretation.
- Where timing/context influence was noticed or missed.
- Which hint/memory outputs were useful vs noisy.
- Where players expected reaction changes but saw none.

## Expansion vs redesign trigger
- **Expand** when core loop is readable, repeatable, and non-chore in multiple runs.
- **Redesign** when readability depends on heavy explanation, brute force, or fixed-canon scaffolding.

> CONFLICT NOTE:
> Previous docs assumed: variable change itself was near-sufficient proof of progress.
> Current lab-oriented reading is: variable coherence + human-readable reaction coherence are both required.
> Action needed: treat variable-only success as partial validation.
> Status: generalized
