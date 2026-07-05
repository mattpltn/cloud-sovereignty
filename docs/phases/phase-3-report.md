# Phase 3 report — Master catalog, crosswalk, ladder mapping

**Branch:** `phase-3-catalog`
**Scope:** Crosswalk verification, master catalog construction, three-ladder
mapping, layer adjudication, and a set of bounded editorial decisions
(uncovered ECSF factors, self-directed controls, SOV-7 confirmation).
Structure only — no `source_text`/`generalized_text` in
`c3a.json`/`ecsf.json`/`cada.json` was read, rewritten, or duplicated.

## Outputs

| File | Change |
|---|---|
| `schema/crosswalk.schema.json` | New (the one schema authorized this phase) |
| `data/catalog/crosswalk.json` | New — 97 links |
| `scripts/build_crosswalk.py` | New |
| `data/catalog/catalog.json` | New — 90 entries |
| `scripts/build_catalog.py` | New |
| `data/catalog/out_of_scope.json` | New — 2 entries (D-028) |
| `data/catalog/ladders.json` | New — 30 cells across 6 domains |
| `scripts/build_ladders.py` | New |
| `schema/control-record.schema.json` | +`addressed_party` (D-030) |
| `data/extracted/cada-act.json` | +`addressed_party: government_self` on Articles 29/30/41 |
| `data/extracted/{c3a,ecsf,cada}.json` | Layer adjudication (D-026): 26 `needs_review` flags cleared, 6 trimmed |
| `scripts/validate.py` | +`check_crosswalk`, +`check_catalog`, +`check_ladders`; `check_catalog` extended for `government_self` ids |
| `docs/DECISIONS.md` | +D-026 through D-031 |
| `docs/METHODOLOGY.md` | +Phase 3 section |

## Layer adjudication (D-026)

One consolidated decision resolving every open layer-related
`needs_review` flag across all three frameworks: 26 cleared (10 c3a, 8
ecsf, 8 cada), 6 kept open with their layer-only note trimmed (5 ecsf,
1 cada) because a separate, non-layer concern remains — coverage
ambiguity or `sov_domain` choice. Flags about the D-008 erratum, the
CADA 2.1(d) typo, and pure coverage/sov_domain ambiguity were left
completely untouched, as instructed.

## Crosswalk (97 links)

Verified/corrected all 30 ECSF→C3A hints from the unverified Phase 2b
`ecsf-c3a-hints.json`; mapped all 40 CADA Annex II criteria to C3A via
`UA1_MAP`/`UA_SHARED_MAP`; added 5 direct ECSF↔CADA links where no C3A
intermediary exists.

**`ecsf-calculator.json`'s 48 specific objectives are deliberately NOT
crosswalk/catalog members.** They were already established in Phase
2b.1 as a separate operationalization layer (the official tender
calculator, one level more granular than the 30 normative v1.2.1
factors, with its own coverage-hint mechanism back to `ecsf.json` —
D-016), not a peer set of criteria to reconcile against C3A/CADA.
Phase 6 (question design) is the intended consumer of that
operationalization detail, not Phase 3's catalog. No crosswalk link
references a calculator id; `build_crosswalk.py`/`build_catalog.py`
never read `ecsf-calculator.json`.

Relation counts: 37 `equivalent`, 29 `partially_covers`, 16
`no_counterpart`, 12 `related`, 3 `subsumed_by`.

**Two bugs found and fixed before commit** (both self-caught during
manual cluster review, not flagged by any external reviewer):

1. A backwards `subsumed_by` direction on the ECSF↔CADA AI-training
   link (source/target were swapped relative to the relation's own
   definition). Fixed, plus the missing UA-3/UA-4 instances added, in a
   dedicated follow-up commit (`059d5c2`).
2. `csat-sov4-ecsf-04` tagged `equivalent` to two mutually-distinct C3A
   criteria (`csat-sov4-01-c1` personnel citizenship,
   `csat-sov4-02-c1` admin-access location), which union-find then
   merged into one incorrect 9-member cluster. Fixed by downgrading
   both relations to `partially_covers` before the catalog commit.

## Master catalog (90 entries)

Union-find over `equivalent`/`subsumed_by` links across 127 in-scope
records (129 total, minus 2 documented out-of-scope). 87 entries from
c3a/ecsf/cada clustering (12 multi-member, 75 single-member; cluster
sizes 2-10), plus 3 more singleton entries from D-030's self-directed
cada-act.json obligations, for 90 total. `primary_id` chosen by fixed
precedence C3A > ECSF > CADA (D-027).

## Three-ladder mapping (30 cells)

SEAL 0-4 ↔ C3A C1/C2 ↔ CADA UA-1..4, per SOV-1..6 (SOV-7 inheritance-
only, SOV-8 out of scope — both excluded). Confidence: 2
`source_anchored`, 13 `inferred`, 15 `no_mapping`. SEAL-0/1 rows and all
of SOV-6 are `no_mapping` in every domain — no per-domain source text
supports a claim there. Surfaced a structural finding (D-029): C3A's
C1/C2 is a localization-*scope* axis, not a strictness ladder like
SEAL/UA, so every `c3a_localization` cell is `inferred` with an
explicit caveat even where its paired SEAL↔UA correspondence is
`source_anchored`.

## Bounded editorial decisions

- **D-027** — `primary_id` precedence rule (C3A > ECSF > CADA), citing
  CLAUDE.md's own source-framework ordering.
- **D-028** — the 7 uncovered ECSF factors, decided individually: 5
  included, 2 excluded as documented out-of-scope (provider investment/
  job-creation; regional-strategic-initiative involvement — both
  procurement-economics rather than posture-assessment criteria).
- **D-030** — new `addressed_party` field (`provider` |
  `government_self`); 3 cada-act.json obligations (Articles 29, 30, 41)
  tagged self-directed and given singleton catalog entries.
- **D-031** — confirms (no data change) SOV-7's end-to-end
  inheritance-only treatment: 4 CADA-only `inherit` entries mapping to
  Annex III criterion E, no C3A/ECSF SOV-7 records to reconcile.

## Validator extensions

`check_crosswalk()` (schema + id-resolution + justification),
`check_catalog()` (structural — no schema authorized; member/primary
resolution, no-orphan-records, extended for `government_self` ids),
`check_ladders()` (structural — SEAL 0-4 coverage, confidence-tag
validity, `no_mapping` cells assert no rung, non-empty justification).

## Statistics

| Metric | Count |
|---|---|
| Crosswalk links | 97 (37/29/16/12/3 by relation) |
| Catalog entries | 90 (78 single-member, 12 multi-member) |
| In-scope records clustered | 127 of 129 |
| Out-of-scope records | 2 (D-028) |
| Self-directed catalog entries added | 3 (D-030) |
| Ladder cells | 30 (2/13/15 by confidence) |
| `needs_review` remaining (pre-existing, non-layer) | 13 (1 c3a, 7 ecsf, 5 cada) |
| New DECISIONS entries | 6 (D-026 through D-031) |

## Validation

Full validator green (9 schemas, 8 draft personas, 129 extracted
control records, plus the three new Phase 3 checks). `npm test` (2
passing, 7 todo) and `npm run typecheck` pass — no engine/TypeScript
changes this phase.

## Not done in this phase (explicitly out of scope)

No Phase 4 work, no disposition-rule engine, no persona status changes,
no merge to `main`. `placeholders_used` remains unpopulated (deferred
since Phase 2d-i). The 13 remaining `needs_review` flags stay open for
a future phase.
