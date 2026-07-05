# Phase 3 review — Master catalog, crosswalk, ladders

**Reviewer:** External (Claude, project design advisor)
**Date:** 2026-07-05
**Branch reviewed:** `phase-3-catalog` @ 20292bb
**Verdict:** APPROVED — no blocking change requests. Merge as-is.

## Verified by reviewer (hands-on)
- Validator PASS (9 schemas, 129 records, all Phase 3 checks); CI green.
- Crosswalk: 97 links, 100% justified; relation mix (37 equivalent / 29 partially_covers / 12 related / 3 subsumed_by / 16 no_counterpart) is plausible and the direction-fix commit (059d5c2) shows correct self-correction. Sampled links verified against sources (e.g., xw-0018 ECSF crypto-control ↔ C3A SOV-3-02: sound).
- Catalog: 90 entries from 127 in-scope records (2 documented out-of-scope in data/catalog/out_of_scope.json per D-028's per-factor decisions); member distribution sane (78 singletons, clusters up to 10); D-027 precedence rule well-argued, including why the rejected alternatives were rejected.
- Ladders: 30 cells; honestly sparse — 2 source_anchored, 13 inferred, 15 no_mapping, each no_mapping with a source-grounded justification. Endorsed: forcing density here would have been fabrication.
- Layer adjudication: 26 flags resolved under consolidated D-026.
- D-numbering: persona-merge collision resolved correctly (D-025..D-030 → D-026..D-031) with cross-references updated; register coherent through D-031.
- Calculator's 48 specific objectives correctly excluded from catalog membership with the required note.

## Endorsed deviations (no action)
- **N-1:** Self-directed controls implemented as `addressed_party: government_self` tags on three cada-act records rather than catalog.json entries — correct, since act records intentionally don't conform to the control-record schema (D-012) and forcing them into the catalog would break its member-resolution invariants. CONSEQUENCE for Phase 6: the self-obligations module sources from cada-act tagged records, not the catalog; revisit promotion to catalog entries when the questionnaire generator exists.
- **N-2:** Ladder sparsity has a Phase 5 design consequence: per-domain ceilings must derive primarily from the responsibility map plus the level semantics of C1/C2 and UA-1..4 directly, with ladders.json as supporting evidence rather than the backbone. The weak commensurability of the three official maturity ladders is itself a citable methodology finding.

## Status
Phase 3 complete. Remaining Phase 4 preconditions: owner-authored Layer-2 assertions (guided round with reviewer). Phase 4 (responsibility-map builder + disposition engine) is otherwise unblocked upon merge.
