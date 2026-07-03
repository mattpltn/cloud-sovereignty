# Phase 2b review — Addendum: CR-2 verification + second-source finding

**Reviewer:** External (Claude, project design advisor)
**Date:** 2026-07-03
**Materials:** ECSF v1.2.1 PDF + ECSF Implementation Guidance PDF + data/local/ecsf-verbatim.json (all supplied by owner)

## CR-2 results — PASS
- **Completeness:** ECSF v1.2.1 section 4 contains exactly 30 contributing factors (SOV-1:6, SOV-2:5, SOV-3:4, SOV-4:6, SOV-5:5, SOV-6:4); extraction matches exactly.
- **Fidelity:** all 30 verbatim entries compared against the source — faithful. Minor accepted deviation: terminal punctuation normalized at bullet boundaries; add one line to METHODOLOGY extraction rules if absent.
- **Scoring model:** weights (15/10/10/15/20/15/10/5, sum 100), SEAL 0–4 definitions, and the Sovereignty Score formula verified exact against v1.2.1 sections 3 and 5.

## New finding — the Implementation Guidance is a material second source
The Commission's post-tender Implementation Guidance diverges from v1.2.1:
1. **Alternative weight set** in its worked matrix (SOV-1 20%, SOV-5 10%, SOV-7 15%; others unchanged; sum 100), with explicit statement that authorities may adapt values. Consequence: no single canonical weight set exists; both official sets should be stored as named reference profiles, reinforcing the project's outcome-based weighting decision (log in DECISIONS).
2. **SEAL aggregation rule** absent from v1.2.1: overall SEAL = MINIMUM SEAL across objectives. Directly relevant to Phase 5 ceiling semantics; must be captured with source pointer.
3. **Per-domain SEAL-2/3/4 requirement descriptions** (table mapping each level's concrete meaning per SOV domain) — key input for Phase 5 per-domain ceiling definitions.
4. **SEAL-3 relabeled** "Technological Sovereignty" (v1.2.1: "Digital Resilience") — capture both labels with provenance.
5. **Answer-option scoring pattern** (per-answer points + per-answer SEAL) and the technical-layers diagram — design reference for Phases 4–6.
6. **Lessons learnt:** Commission states SEAL-4 is presently unattainable given chip/hardware dependencies — official support for the tool's achieved-vs-ceiling philosophy; citable in methodology.

## Disposition
- CR-2 closed. Phase 2b merge remains gated only on CR-1 (hints re-encoding) plus the small Phase 2b.1 supplement below (recommended before merge so the ECSF extraction is complete as a unit).
- **Phase 2b.1 (recommended):** add the Implementation Guidance PDF to /sources; extract deltas 1–4 above into data/extracted/ecsf-guidance.json (verbatim-isolation regime; new small schema authorized); log DECISIONS entries for the dual weight sets (v1.2.1 remains the default reference profile) and the SEAL min-rule.
