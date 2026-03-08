# CORE_PROGRESS_SYSTEM

## Core progression formula (current baseline)

`observation / hint -> interpretation -> timing + context -> action -> world reaction -> new information`

This loop is the main thing being validated.

## Required distinction: internal vs player-facing

### 1) Hidden internal state (system side)
Examples:
- Context/timing flags.
- Relationship/reaction variables (placeholder-role compatible).
- Event eligibility and delayed consequence state.

These values can be hidden from normal player UI.

### 2) Player-facing evidence (experience side)
The player still needs lightweight evidence that state changed, such as:
- Changed dialogue tone or availability.
- New hint/reminder line.
- Updated event log/journal entry.
- Altered world reaction cue.

The prototype is **not** memory-only by design.

## Mandatory baseline systems (for proof)
1. Context + timing-sensitive event triggering.
2. World reaction hooks that can change future information.
3. Lightweight hint/goal/completion output so inference remains playable.
4. Minimal delayed consequence behavior.

## Optional/deferred modifiers (not mandatory for shortest proof)
- Rumor/public/hygiene pressure stacks.
- Larger social reputation simulations.
- Expanded multi-layer modifier systems.

These are valid if they help the proof, but they are not required equally at baseline.

## Non-goals for current progression proof
- "Raise affection until scene unlock" as dominant loop.
- Pure inventory-combination chain gameplay.
- Explicit route picker as primary progression UX.
