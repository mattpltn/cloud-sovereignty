# Phase 2d-ii report — Generalization applied to ECSF, CADA, and the ECSF second-source files

**Branch:** `phase-2d-generalization` (same branch as Phase 2d-i)
**Scope:** Apply the Phase 2d-i rule table (largely unchanged; 3 amendments
made and logged) to every remaining extracted file: `ecsf.json`,
`cada.json`, `cada-act.json`, `cada-evidence.json`, `ecsf-guidance.json`'s
domain SEAL-2/3/4 cells, and `ecsf-scoring.json`'s domain definitions.

## Outputs

| File | Change |
|---|---|
| `data/extracted/ecsf.json` | `generalized_text` + `generalization_class: "direct"` on all 30 records |
| `data/extracted/cada.json` | Same on all 40 records; 1 `structural_adaptation` (Article 18/19), 7 records with `generalization_note` |
| `data/extracted/cada-act.json` | `generalized_text`/`generalization_class`/`generalization_note` added (ad-hoc keys, no schema — hand-generalized, all 13 records) |
| `data/extracted/cada-evidence.json` | `title`/`evidence_items`/`notes` generalized in place (no parallel field — no schema authorized) |
| `schema/ecsf-guidance.schema.json` | +`generalized_seal_2/3/4`, +`generalization_note` on `domainSealRequirement` |
| `data/extracted/ecsf-guidance.json` | 23/24 possible cells generalized (SOV-8 SEAL-3 has no verbatim cell); 1 erratum note (SOV-7 SEAL-3) |
| `schema/ecsf-scoring.schema.json` | +`generalized_description` on `domain` |
| `data/extracted/ecsf-scoring.json` | All 8 domain descriptions generalized |
| `data/rules/generalization-rules.yaml` | 3 rule amendments (R5d, R2b new, R2); 8 new per-record overrides |
| `scripts/validate.py` | Dedicated lint passes for `cada-evidence.json`/`ecsf-scoring.json`/`ecsf-guidance.json` (no `generalization_class` marker); generalized `check_verbatim_leak()` field-exclusion (any `generalized_*`/`generalization_note` key, any depth); new `GENERALIZED_IN_PLACE_FILES` exclusion set |
| `docs/DECISIONS.md` | +D-021, D-022, D-023 (rule amendments) |
| `docs/METHODOLOGY.md` | +Phase 2d-ii section |

## Two file shapes needed different treatment

- **`ecsf.json`/`cada.json`** fit the established control-record pattern
  exactly — mechanical `generalize(verbatim, rules)`, batched via
  `scripts/generalize.py`.
- **`cada-act.json`** is analytical commentary (`derivation: derived`,
  written during Phase 2c), not verbatim CADA text, with no matching
  verbatim file. Several records are self-referential *definitions* of
  the terms ("Union entities" vs. "public sector body") the mechanical
  rules would otherwise collapse into the same placeholder, destroying
  the very distinction being defined. Hand-generalized instead, all 13
  records, each with a `generalization_note` explaining why.
- **`cada-evidence.json`** is verbatim but nested (not a flat array);
  generalized in place (no parallel field — no schema change was
  authorized for this file).
- **`ecsf-guidance.json`/`ecsf-scoring.json`** *did* have schema changes
  authorized this phase, so both keep the source/generalized-field split
  used everywhere else in the project.

## The Article 18/19 erratum, generalized functionally (R8)

`cada.json`'s `csat-sov1-cada-ua3-g` and `cada-evidence.json`'s
criterion G both reference "an implementing act under Article 19."
Both are hand-overridden to describe the functional mechanism
generically ("a formal adequacy/allowlist decision by {NATION}'s
competent authority") rather than substituting a placeholder into
"Article 19" itself, which has no {NATION}-level analog.
`csat-sov1-cada-ua3-g` is the only record this phase tagged
`generalization_class: "structural_adaptation"` (R8); both records'
notes cite the existing Phase 2c `needs_review_note` rather than
re-explaining the discrepancy.

## The 2.1(d) typo, corrected in generalized text only

`cada.json`'s `csat-sov4-cada-ua2-d` preserves "presonnel" verbatim
(D-018, unchanged). Its `generalized_text` override corrects this to
"personnel," with a `generalization_note` citing D-018; `needs_review`
stays set.

## Named-instrument citations (R7), exercised for real

Seven `cada.json`/`cada-act.json`/`cada-evidence.json` records cite
Regulations/Directives by number (2019/881, 2024/2847, 2021/697,
2022/2555, 2019/1024, 2014/24/EU, 2024/903, 2016/679). Each is
hand-overridden to reframe the requirement generically with the
instrument kept as a `(source cites: ...)` parenthetical — mechanical
substitution would otherwise produce "Regulation ({TRUSTED_REGION})
2019/881," which is nonsense.

## Three rule amendments

1. **D-021 — R5d widened to match plural "third countries."** Found in
   `ecsf.json` (2 records); CADA only uses the singular.
2. **D-022 — new rule R2b for bare "Union."** CADA uses "Union
   citizens"/"Union citizenship"/"Union law" as bare adjectives R2 never
   matched. A narrow lookahead avoids touching CADA's own proper term
   "Union assurance level" and R6's "Union entities" mapping.
3. **D-023 — R2 widened to match bare "Europe."** Found in
   `ecsf-guidance.json`'s SOV-4 SEAL-3 cell ("expertise in Europe").

All three were verified not to change any already-committed `c3a.json`
record before being committed.

## Statistics

| File | Records | `direct` | `structural_adaptation` | With note |
|---|---|---|---|---|
| `ecsf.json` | 30 | 30 | 0 | 0 |
| `cada.json` | 40 | 39 | 1 | 7 |
| `cada-act.json` | 13 | 13 (hand) | 0 | 13 |
| `cada-evidence.json` | 11 criteria (in place) | — | — | — |
| `ecsf-guidance.json` | 8 rows, 23/24 cells | — | — | 1 |
| `ecsf-scoring.json` | 8 domains, 8 descriptions | — | — | 0 |

Rule amendments: 3. New overrides: 8 in `cada.json`/`cada-act.json`'s
rules-file mechanism, plus 3 hand-written substitutions applied directly
in `cada-evidence.json` (no formal overrides table for that file).

## Validation

Full validator green with `data/local/{c3a,ecsf,cada,cada-evidence,
ecsf-guidance}-verbatim.json` all present (leak check + equality check
active). 129 combined control records validate; both newly authorized
schema field additions (`ecsf-guidance.schema.json`,
`ecsf-scoring.schema.json`) validate against Draft 2020-12; 0
residual-literal lint hits across every file touched. Every new/adjusted
check (equality, lint, leak-check exclusion) was manually verified to
fail on a deliberately injected defect in each file type, then
reconfirmed clean. `npm test` (2 passing, 7 todo) and `npm run
typecheck` pass (no engine/TypeScript changes this phase). `git log
--name-only` confirms `data/local/` was never staged.

## Not done in this phase (explicitly out of scope)

No merge to `main`. No Phase 3 crosswalk work. `placeholders_used`
remains unpopulated/unextended (deferred, per Phase 2d-i's own note).
