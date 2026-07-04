# Phase 2d review — Generalization (2d-i + 2d-ii)

**Reviewer:** External (Claude, project design advisor)
**Date:** 2026-07-04
**Branch reviewed:** `phase-2d-generalization` @ 3d94651
**Verdict:** APPROVED with one documentation change request (CR-1). Merge after CR-1 and the owner's read-through of cada-act.json (see N-1).

## Verified by reviewer (hands-on)
- Main history: phases 2a/2b/2c each merged as individually reviewed squash units; all review notes on main; both new process rules codified in CLAUDE.md; merged branches deleted.
- DECISIONS register coherent D-001..D-023; parallel-branch renumbering rule applied correctly twice (2c → D-017/D-018 at rebase; 2d-i's provisional D-017/D-018 → D-019/D-020 at the main merge, mapping documented in commit b09ecb3). Cosmetic only: the 2c squash message cites "D-012..D-018" where D-017..D-018 is accurate.
- **Mechanical reproduction:** with owner-supplied verbatim files (ecsf, cada, ecsf-guidance) placed in data/local/, the repo's own equality check reproduced generalized_text for all 70 ECSF+CADA control records and the guidance cells; residual-literal lint clean across all files; leak checks pass. C3A equality verified executor-side only (reviewer holds no c3a-verbatim.json); reviewer spot-checked 3 C3A records against PDF-anchored verbatim — correct, including the D-008 erratum override ("within {NATION}") and the R4 two-level construct.
- R7 instrument handling and the certification-scheme reframings (2.1(e)/3.1(e)/4.1(e)) reviewed — functionally sound, source citations retained.
- Rule table R1–R9 + amendments (D-021 R5d, D-022 R2b, D-023 R2-Europe) reviewed; each amendment has its own register entry as required.

## Change request (pre-merge)
- **CR-1 (documentation of class semantics):** the implementation deviates from the phase instructions by keeping override-based records classed `direct` (overrides live in the rules table, so f(verbatim, rules) includes them and the equality check covers 128/129 records). The reviewer ENDORSES this design — it strengthens verification coverage versus the specified scheme — but the semantic choice must be registered: (a) a DECISIONS entry codifying "direct = machine-reproducible including per-record overrides; the enumeration of human judgment = the public overrides table ∪ structural_adaptation records"; (b) a validator rule that every override entry carries a generalization_note (rationale) — currently true by inspection, make it enforced; (c) one METHODOLOGY line stating how to enumerate all judgment points.

## Noted
- **N-1 (owner action):** cada-act.json's 13 hand-generalized records are the only file with no mechanical check behind it; owner to read through once before merge (they describe obligations on the tool's own users).
- **N-2 (optional):** owner may supply c3a-verbatim.json for reviewer-side reproduction of the remaining 59 records; executor-side verification is otherwise accepted.
- **N-3:** with 2d merged, all Phase 2 extraction work is complete: 3 frameworks + 2 companion sources, 129 control records + 13 act records + 11 evidence criteria, 4 official-source errata caught and catalogued, zero unverified text in the public artifact, full judgment register. Phase 3 (master catalog + crosswalk + three-ladder mapping) is next; the persona-approval debt becomes the critical path immediately after.
