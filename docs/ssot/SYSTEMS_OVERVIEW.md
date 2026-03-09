# SYSTEMS_OVERVIEW

This is the current **lab systems** list, not a final game architecture.

## 1) Context / Timing Layer (current)
- Tracks when and where interpretation/action is attempted.
- Gates what can react now vs later.

## 2) Hidden Relational / World-State Layer (current)
- Stores internal state that influences reaction selection.
- Uses generic structures; named cast schemas are optional placeholders.

## 3) World-Reaction Trigger Layer (current)
- Selects meaningful response based on context and hidden state.
- Supports at least one immediate and one deferred reaction pathway (if needed by test).

## 4) Hint / Memory / Objective Output Layer (current)
- Provides lightweight player-facing support.
- Must communicate change/readability without heavy quest-marker design.

## 5) Small Object / Evidence Interaction Layer (optional)
- Allowed when bounded and logically local.
- Must avoid brute-force try-everywhere patterns.

## 6) Optional Pressure Modifiers (deferred-by-default)
- Rumor/hygiene/public-standing and related stacks.
- Included only if required to answer current validation questions.

> CONFLICT NOTE:
> Previous docs assumed: pressure systems were close to baseline pillars.
> Current lab-oriented reading is: pressure systems are optional modifiers unless needed for proof quality.
> Action needed: keep them opt-in and evidence-driven.
> Status: generalized
