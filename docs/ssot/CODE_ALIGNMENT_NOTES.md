# CODE_ALIGNMENT_NOTES

## Purpose
Document mismatches between current lab SSOT and existing prototype code without broad refactors.

## Current mismatches
- Some code still uses A/B-labeled structures that can be misread as fixed cast canon.
- Pressure variables (rumor/public/hygiene) exist in baseline state and may look mandatory.
- Current placeholder text is uneven: some outputs are narrative-style legacy remnants rather than neutral diagnostics.

## Likely next minimal adjustments
- Keep A/B labels but annotate as non-canonical placeholders in dev-facing notes.
- Add/standardize reaction placeholder outputs linked to trigger reasons.
- Add small trace summaries for why no reaction fired under current context.

## Safe minimal follow-ups
- Improve debug trace visibility.
- Add neutral placeholder reaction lines where missing.
- Keep memory/hint output lightweight and reversible.

## Do NOT change yet
- Do not refactor into final cast architecture.
- Do not lock route/macro-story structure.
- Do not expand pressure stacks as default gameplay spine.
- Do not perform engine-migration work.
