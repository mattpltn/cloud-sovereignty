# Phase 2c review — CADA extraction

**Reviewer:** External (Claude, project design advisor)
**Date:** 2026-07-03
**Branch reviewed:** `phase-2c-cada` @ a9fcafc (8 commits)
**Verdict:** CONDITIONALLY APPROVED — merge after CR-1 (fidelity check) and CR-2 (merge sequencing/renumbering), and after the 2b line has merged.

## Verified by reviewer (hands-on)
- Validator executed independently: PASS (99 extracted records across all files).
- cada.json: 40 records; UA-1: 7, UA-2/3/4: 11 each — matches Annex II exactly, including UA-1's distinct 7-criterion scheme (correctly not forced into the (a)–(k) template). `status: proposed_legislation` present in source_refs on all 40 (per the Phase 1 schema design). Placeholders correct; verbatim isolated from the start. 12 needs_review flags with substantive notes.
- cada-evidence.json: 11 audit criteria A–K, extraction-only. cada-act.json: 13 derived records. Annex II scope statement (software in scope per CRA; hardware excluded) captured as metadata. Annex I correctly excluded.
- **Article 18/19 cross-reference error CONFIRMED by reviewer against the Act PDF**: Art. 18 = "Associated third countries", Art. 19 = "Conformity self-assessment"; Annex II 3.1(g) and Annex III criterion G cite Art. 19 where Art. 18 substantively matches. Second official-source erratum caught by the pipeline (after BSI SOV-4-02-C2). Recommend submitting via the Commission's feedback mechanism on COM(2026) 502 final and logging the submission as a DECISIONS entry.
- D-012 (act records intentionally nonconforming to the provider-centric control schema) endorsed.

## Change requests (pre-merge)
- **CR-1 (fidelity):** owner supplies data/local/cada-verbatim.json to reviewer; reviewer diffs against the Annexes text (already in hand): completeness re-verification plus ≥10-record verbatim sample across all four UA levels and Annex III, and confirmation that source_pointer.document pins "COM(2026) 502 final, 3.6.2026".
- **CR-2 (sequencing):** merge order: 2b CR-1 (hints re-encoding) + Phase 2b.1 → merge phase-2b-ecsf → rebase phase-2c-cada onto main, renumbering its DECISIONS entries (both branches independently allocated D-012+). Add CLAUDE.md working rule: DECISIONS numbers on parallel phase branches are provisional; the later-merging branch renumbers at rebase.

## Noted for later phases
- **N-1 (Phase 3):** cada-act obligations (Arts. 29/30/41) are candidates for a new addressed-party class — self-directed controls on the assessing government. Genuine differentiator; requires a schema/design decision + DECISIONS entry in Phase 3.
- **N-2 (Phase 2d):** "public sector body"/"Union entities" in CADA text generalizes to the {NATION} government-as-customer; encode in the substitution rules. Resolves the persona-model gap flagged by the executor.
- **N-3 (Phase 3/5):** the UA↔SEAL↔C1/C2 ladder note in the phase report is accepted as unverified input; the three-ladder mapping becomes a first-class Phase 3 deliverable.

## Status
Blocked on CR-1, CR-2, and 2b-line merge. Extraction quality and process discipline: excellent. With 2c, all three source frameworks are extracted; Phase 2d (generalization) then Phase 3 (master catalog + crosswalk) follow.
