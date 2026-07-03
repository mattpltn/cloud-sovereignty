# Phase 2b review — ECSF extraction

**Reviewer:** External (Claude, project design advisor)
**Date:** 2026-07-03
**Branch reviewed:** `phase-2b-ecsf` @ 01f9d42 (9 commits)
**Verdict:** CONDITIONALLY APPROVED — merge after CR-1 (hints restructure) and CR-2 (fidelity/weights verification).

## Verified by reviewer (hands-on)
- Process: one commit per domain/artifact; main squash-merge from Phase 2a clean; review notes landed in /reviews (Phase 2a CR-4 closed); CI green; validator green locally with correct graceful-skip behavior for local-file checks in CI.
- ecsf-scoring.json: SEAL 0–4 complete; 8 domain definitions; weights 15/10/10/15/20/15/10/5 (sum 100); scoring formula captured; SOV-7 `inheritance_only` with 5 factors as metadata; SOV-8 `out_of_scope` with weight retained (needed for Phase 5 renormalization). New schema was the phase's single authorized schema addition — respected.
- ecsf.json: 30 records (SOV-1:6, 2:5, 3:4, 4:6, 5:5, 6:4); D-009/D-010 regime applied from the start (placeholders verified in all text fields; data/local never staged); layer tags use D-007 taxonomy; needs_review 15/30 with substantive layer-ambiguity notes.
- Hints: 30 entries; all real C3A ids resolve (no dangling references besides the sentinel issue below); c3a.json untouched.
- D-012 present; the intentional asymmetry (verbatim isolation despite ECSF's permissive license, for uniform pipeline behavior) is endorsed.

## Change requests (pre-merge)
- **CR-1 (hints encoding):** `"uncovered"` is a magic string inside the candidate-id lists, silently special-cased by the validator; mixed entries would validate. Restructure each entry to `{"coverage": "covered"|"uncovered", "c3a_candidates": [...]}`; validator enforces candidates non-empty iff covered, empty iff uncovered, sentinel rejected. (Root cause traces to loose wording in the reviewer's Phase 2b prompt — noted for process honesty.)
- **CR-2 (fidelity/completeness/weights):** Owner supplies the ECSF v1.2.1 PDF and data/local/ecsf-verbatim.json to the reviewer. Reviewer verifies: 30-factor completeness against the source; text fidelity sample (≥8 records across domains); and — critical for this phase — exact verification of weights, SEAL level definitions, and the scoring formula, since scoring-model transcription errors would silently corrupt all downstream scores.

## Noted for Phase 3 (no action now)
- **N-1:** The 7 uncovered ECSF factors (financing sources, EU investment/jobs, policy alignment, IP location, AI governance, API openness, open-license software) require per-factor editorial decisions in Phase 3 (derived control vs. metadata signal vs. documented out-of-scope), each with a DECISIONS entry.
- **N-2:** 15/30 layer-ambiguity flags → Phase 3 must include an explicit layer-adjudication pass resolved under a consolidated DECISIONS entry.

## Status
Blocked on CR-1 + CR-2. All structural and process checks pass.
