# Catalog C1/C2 over-merge fix — review

**Reviewer:** External (Claude, project design advisor)
**Date:** 2026-07-05
**Branch reviewed:** `fix/catalog-c1c2-overmerge`
**Verdict:** APPROVED — merge as its own reviewed unit.

## Verified by reviewer (hands-on)
- Validator PASS including the new permanent invariant (no catalog entry spans more than one localization_level); reviewer's independent sweep confirms ZERO mixing entries remain across all 98.
- cat-0024 correctly decomposed: SOV-3-01 C1–C5 now five separate entries; only the literal match (C3 ↔ ECSF strict-confinement factor ↔ CADA UA residency criteria) retained as equivalent.
- Retargeting of the 8 CADA UA residency links verified semantically correct (Annex II (c) "remain exclusively within the Union" = residency guarantee, csat-sov3-01-c3 — not the transparency criterion).
- Relation distribution consistent with the described downgrades (equivalent 37→29, partially_covers 29→37); catalog 90→98 entries; D-032 present, documenting both the fix (with Phase 3 precedent) and the intentionally retained assurance-level clustering pattern.
- Invariant was defect-tested (bug reintroduced, caught, removed) before being trusted — endorsed practice.

## Notes
- **N-1 (non-blocking):** UA-4's residency criterion is narrower (sensitive-data-only, post-risk-assessment) than UA-2/3's while sharing the equivalent link to C3; the assurance_level metadata preserves the distinction — add one clarifying line to cat-0028's justification if absent.
- **Process observation:** this defect escaped both the Phase 3 executor self-review and the external review (sampled crosswalk verification did not include these links). It was caught by Milestone 4a's test-first requirement to resolve assertions to concrete ids — recording this as evidence for the layered-defense design, and as a caution: sampling reviews bound but do not eliminate residual defect risk; permanent invariants remain the strongest control.

## Post-merge actions
1. Squash-merge to main as its own unit; delete branch.
2. Resume Phase 4 Milestone 4a on a fresh `phase-4-engine` branch off the updated main, per the original Phase 4 prompt (unchanged).
