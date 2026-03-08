# CORE_PROGRESS_SYSTEM

## Central progression formula (minimal)
Progress is computed as a hidden interaction of:

`context (location + phase + recent events)`
`+ behavioral consistency`
`+ relationship vectors (A/B/R placeholders)`
`+ world reaction (rumor/public standing)`
`+ delayed consequence queue`

## Required state groups
- **Time:** day, minutes, phase, nightly tick hooks.
- **World:** per-location rumor heat, optional rumor global aggregate, public image axes.
- **Characters (prototype roles):** A/B/R with trust/attention/attraction/exclusivity-compatible fields.
- **Story control:** flags, pending story/event queue.
- **Behavior memory:** last_style + consistency drift.

## Progression rules
1. Choices update hidden state, not player-visible bars.
2. Event eligibility is condition + priority based.
3. Some effects apply immediately; some are delayed and resolved by later context.
4. Nightly/system ticks update long-horizon pressure (cleanliness, rumor cooling, etc.).
