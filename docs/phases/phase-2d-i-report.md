# Phase 2d-i report — Generalization infrastructure + C3A

**Branch:** `phase-2d-generalization` (branched from `main` post Phase
2a/2b merge)
**Scope:** Build the generalization infrastructure (placeholder
registry, substitution rule table, engine, validator extensions) and
apply it to `data/extracted/c3a.json` only. ECSF and CADA files
untouched (Phase 2d-ii, same branch).

## Outputs

| File | Purpose |
|---|---|
| `data/rules/placeholders.yaml` | Permanent placeholder registry: `{NATION}`, `{TRUSTED_REGION}`, `{NATION_CYBERSECURITY_AUTHORITY}`, `{NATION_ADMINISTRATION}`, `{GOVERNMENT_CUSTOMER}`, `{PROVIDER}` |
| `data/rules/generalization-rules.yaml` | R1-R9 substitution rules (pattern/replacement/rationale/examples) + per-record overrides section |
| `schema/control-record.schema.json` | +2 optional fields: `generalization_class` (enum), `generalization_note` (lang-string); +1 conditional requiring the note when class is `structural_adaptation` |
| `scripts/generalize.py` | The generalization engine: `generalize(text, rules)` pure function + CLI (`generalize.py <framework> [SOV-domain]`) |
| `scripts/validate.py` | +`check_generalization()` (equality check + residual-literal lint); `check_verbatim_leak()` adjusted to exclude `generalized_text` |
| `data/extracted/c3a.json` | All 59 records: `generalized_text` populated (previously `"GENERALIZATION-PENDING"`), `generalization_class: "direct"` set on all, 1 `generalization_note` (D-008 override) |
| `docs/DECISIONS.md` | +D-019 (consolidated rule-table decision), +D-020 (public generalized C3A text remains subject to D-002's pending posture) — originally logged as D-017/D-018 on this branch, renumbered after `phase-2c-cada` merged first (see docs/DECISIONS.md renumbering notes) |
| `docs/METHODOLOGY.md` | +Phase 2d-i section |

## Rule table summary

Nine rules, R1-R9 (full text and rationale in
`data/rules/generalization-rules.yaml`, consolidated decision D-019):

- **R1a/R1b** — Germany/German → `{NATION}` (R1a: "German federal
  administration" → `{NATION_ADMINISTRATION}` specifically, must run
  first).
- **R2** — EU/European Union/the Union/EU-EEA/European jurisdictions/bare
  European → `{TRUSTED_REGION}`.
- **R3/R3b** — "EU member state"/"Member State", as the acting
  government → `{NATION}` (must run before R2).
- **R4** — two-level constructs (documentation only; falls out of R1+R2
  running independently, per-token).
- **R5a/R5b/R5c/R5d** — non-EU/third-country forms → "outside
  `{TRUSTED_REGION}`" (must run before R2, since "EU" sits at a regex
  word boundary inside "non-EU").
- **R6** — public sector body/Union entities → `{GOVERNMENT_CUSTOMER}`
  (seeded for CADA, zero C3A matches).
- **R7** — named legal instruments not substituted, reframed generically
  with a `"(source cites: ...)"` parenthetical (seeded for CADA, zero
  C3A matches requiring rewrite).
- **R8** — EU-institutional mechanisms with no national analog →
  `generalization_class: structural_adaptation` (seeded for CADA, zero
  C3A matches).
- **R9** — the "responsible authority is the one in the country where
  the data center is located" sentence (documentation only; already
  region-agnostic, no substitution needed).

## The D-008 erratum override

`csat-sov4-02-c2`'s verbatim source text has an internal inconsistency
(confirmed against the published PDF, D-008): sentence 1 says "within
the EU" but sentence 2 says "outside Germany." Per this phase's
instruction, the override lives in `generalization-rules.yaml`'s
`overrides` section (not code): `generalized_text` reads "within
`{NATION}`... outside `{NATION}`..." (the intended meaning), with a
`generalization_note` citing D-008. `source_text` and the original
Phase 2a `needs_review`/`needs_review_note` are untouched.
`generalization_class` stays `"direct"` since the override is itself
part of "the rules" the equality check runs against.

## Statistics

- **Records generalized:** 59/59 (100%), 0 remaining
  `"GENERALIZATION-PENDING"`.
- **`generalization_class: direct`:** 59/59. No `structural_adaptation`
  or `eu_institutional` records needed for C3A.
- **Records with a `generalization_note`:** 1 (the D-008 override).
- **Records with ≥1 rule fired:** 27/59; **pure pass-through (no
  jurisdiction-specific literal at all):** 32/59.
- **Rule fire counts:** R1a: 2, R1b: 10, R2: 19, R3: 1, R5a: 2, R5b: 1;
  R3b/R5c/R5d/R6: 0 (no matching constructions in C3A — seeded for
  Phase 2d-ii).
- **Residual-literal lint hits (final state):** 0/59.
- **Per-record overrides:** 1 (`csat-sov4-02-c2`, D-008).

## Validation

`.venv/bin/python3 scripts/validate.py` (with
`data/local/c3a-verbatim.json` present, so the equality check and leak
check are both active) passes clean: 89 combined control records valid
(59 C3A + 30 ECSF), the new equality check confirms all 59
`generalization_class: direct` C3A records match
`generalize(verbatim, rules)` exactly, and the residual-literal lint
finds 0 hits. Both new checks (equality, lint) and the adjusted leak
check were manually verified to fail correctly on deliberately injected
defects, then reconfirmed clean after restoring the generated files.
`npm test` (2 passing, 7 todo) and `npm run typecheck` unaffected (no
engine/TypeScript changes this phase). `git log --name-only` confirms
`data/local/` was never staged on this branch.

## Not done in this phase (explicitly out of scope)

`ecsf.json`, `ecsf-guidance.json`, `ecsf-scoring.json`, and all CADA
files are untouched — Phase 2d-ii, same branch, applies the same
(unchanged) rule table to those files. No merge to `main`. No Phase 3
crosswalk work.
