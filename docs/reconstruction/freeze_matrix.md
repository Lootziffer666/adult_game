# Freeze Matrix

| Topic | Current best reading | Supporting files | Contradicting files | Status (green/yellow/red) | Merge now? | Notes |
|---|---|---|---|---|---|---|
| Engine target | Ren'Py remains implementation baseline | Analyse_ Adult-Game_Startplan, Design-Sheet Erotica, GAME DESIGN DOCUMENT | none explicit | green | yes | No migration commitment found |
| Hidden-state philosophy | Player should feel systems, not read bars | FINALES GESAMTDOKUMENT, UI-PHILOSOPHIE, GAME DESIGN DOCUMENT | none major | green | yes | Core identity anchor |
| Visible stat UI | Numeric debug/state should not be player-facing by default | UI-PHILOSOPHIE, FINALES GESAMTDOKUMENT | prototype screens exposing debug values | yellow | bounded | Keep optional dev toggle only |
| Time phases + nightly decay | Day/phase cycle and nightly hygiene/rumor decay | Analyse_ Startplan, VERSION 2, RENPY-PROJEKTGERÜST | none major | green | yes | Already partially in code |
| Rumor model | Per-location rumor with optional global coupling | Analyse_ Startplan, VERSION 2, EVENT docs | docs with simpler scalar rumor | yellow | bounded | Preserve hook; avoid overfitting |
| A/B structure | A/B as hidden relational vectors, not explicit route menu | GAME DESIGN DOCUMENT, Startplan | early route-like slice framing | green | yes | Keep as internal state names for now |
| Canon story/lore specifics | Lore remains provisional; avoid invented canon | FINALES GESAMTDOKUMENT (open contradictions), Startplan (missing lore) | steampunk-strong docs asserting specificity | yellow | no | Needs human decision |
| Figure identities | A/B/R functional roles are usable as prototypes | AAA GDD, OVERVIEW 2ND STAGE | files with deeper but unstable characterization | yellow | bounded | Keep placeholders, no hard canon bios |
| Intimacy baseline | Build intimacy systems before explicit content expansion | FINALES GESAMTDOKUMENT, smart-porn manifesto, VERSION 2 | scene drafts treating explicit beats as fixed | green | yes | Mechanics-first accepted |
| Event architecture | Priority/condition event checker + delayed consequences | EVENT-TABELLE, EVENT-KETTEN, E_PUBLIC_FRICTION, PROJEKTGERÜST | none major | green | yes | Implement minimal robust scheduler |
| UI visual motif | Brass/glass/smoke warm low-noise style is useful pattern library | UI-PHILOSOPHIE, VISUELLE DNA, PROMPT docs | none major | yellow | no | Treat as art pattern, not strict canon |
| Production timeline promises | 14-day schedule is planning artifact only | DAILY PLAN, Dev Task Breakdown | n/a | red | no | Do not encode as SSOT requirement |
| Brand/logo docs as canon | Brand/logo chats are non-game canon | Logo docs, Brand sheet | n/a | red | no | Archive only |
| Empty/fragment files | Peer_review_beta and Untitled are non-authoritative | Peer_review_beta, Unbenanntes Dokument | n/a | red | no | Keep but ignore for SSOT |
