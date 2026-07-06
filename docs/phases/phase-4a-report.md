# Phase 4, Milestone 4a report — tests exist before the engine

**Branch:** `phase-4-engine`
**Scope:** Convert the 54-assertion owner-authored Layer-2 specification
into executable tests, make invariants I1-I7 executable, implement the
X-series as Layer-5 differential tests, build the Layer-3 snapshot
harness (no baselines), and define the engine's public API as
TypeScript types only. `resolve()` itself is not implemented — that is
Milestone 4d.

## Outputs

| File | Change |
|---|---|
| `engine/types.ts` | +Phase 4 public API (`WordingVariant`, `EvidenceQuality`, `SovDomain`, `DispositionEntry`, `AutoAnswer`, `Ceilings`, `EngineResult`); `KeyCustody`/`Modifiers` synced with the persona schema's `government_held`/`provider_stack` (D-025) |
| `engine/index.ts` | `resolve(persona, tierId): EngineResult`, throws "not implemented until Milestone 4d" |
| `tests/helpers/catalog.ts` | New — loads/joins `data/catalog/catalog.json` with c3a/ecsf/cada/cada-act metadata |
| `tests/helpers/control-refs.ts` | New — spec-prose → catalog `primary_id` bindings (the interpretation record) |
| `tests/helpers/engine-assertions.ts` | New — shared `EngineResult` query helpers |
| `tests/helpers/personas.ts` | +`loadPersonaByShorthand("P1".."P8")` |
| `tests/invariants/i1..i7-*.test.ts` | Rewritten from `it.todo` stubs to executable `it.fails` assertions (I4/I5 each keep one `it.todo` sub-case, scope-split to Phase 5/6) |
| `tests/assertions/cross-persona.test.ts` | New — X1a-X6 (9 assertions), Layer 5 |
| `tests/assertions/p1..p8.test.ts` | New — 45 per-persona assertions, Layer 2 |
| `tests/assertions/conversion-table.md` | New — spec id → test file → interpretation, required by this milestone's rules |
| `tests/snapshots/harness.ts` | New — `buildSnapshot`/`serializeSnapshot`, no baselines committed |
| `tests/snapshots/harness.test.ts` | New — harness smoke test + `it.todo` for the real baseline-diff test |
| `docs/METHODOLOGY.md` | +Phase 4/Milestone 4a section |

## Blocking discovery, resolved before this milestone could complete (D-032)

Binding the spec's prose control-class references to concrete catalog
ids (the step that makes an assertion genuinely executable) surfaced a
catalog defect: 4 master-catalog entries incorrectly bridged C1/C2
localization tiers of the same C3A criterion into one entry. Per this
milestone's own "if anything conflicts with the catalog... STOP and
report" rule, Milestone 4a paused; the catalog was fixed on
`fix/catalog-c1c2-overmerge` (D-032), reviewed
(`reviews/catalog-fix-review.md`), and merged to `main` before this
branch (`phase-4-engine`) was created off the updated `main`. Full
detail in `docs/DECISIONS.md`'s D-032 and
`docs/phases/phase-3-report.md`'s addendum — not repeated here.
Concretely, P5-2 (the data-residency assertion distinguishing
`{TRUSTED_REGION}` vs. `{NATION}` satisfaction) would not have been
convertible into a real test without this fix.

## Success state confirmed

`npm test`: 18 test files, 149 tests — 3 passing (pre-existing persona
helper tests, untouched), **143 expected-fail** (81 invariant checks +
54 Layer-2/5 assertions + 8 snapshot-harness smoke checks — all
deliberately red via `it.fails`, confirming every test compiles and
genuinely exercises `resolve()`'s not-implemented path), 3 `it.todo`
(the Phase-5/6-deferred sub-cases). `npm run typecheck` passes. The
suite itself is green in CI throughout — `it.fails` inverts pass/fail,
so an assertion that stops failing *before* it's genuinely satisfied
would itself break CI, which is the intended tripwire for Milestone 4d.

## Scope splits, not weakenings

Three invariants (I4, I5, I6) and one (I2) needed explicit,
documented adaptation to the Milestone 4a API shape:
- **I2**: checked via the `wording_variant` KEY against
  `axis_a`/`service_model` structural constraints (necessary, not yet
  sufficient, condition — the full responsibility map is Milestone 4b).
- **I4**: `0 <= ceiling <= 4` checked now; achieved/renormalization
  (`0-100` scale) deferred to Phase 5 as `it.todo`.
- **I5**: rationale+`rule_id` checked now; negotiation clause TEXT
  deferred to Phase 6 as `it.todo` (the API has no clause-text field
  yet, only a list of flagged `control_id`s).
- **I6**: ceiling-monotonicity checked now; achieved-score
  monotonicity deferred to Phase 5.

Each split is fully documented in `docs/METHODOLOGY.md`'s Phase 4
section and in-line in the affected test file, per this milestone's
own explicit statement that Phase 5 owns achieved
scores/weights/evidence math and Phase 6 owns clause text/question
prose.

## Interpretation record

`tests/helpers/control-refs.ts` (9 named bindings) and
`tests/assertions/conversion-table.md` (every spec id → test file →
interpretation) together are the complete record of every non-obvious
judgment call made converting prose into code. No assertion was
weakened; every binding is justified against the underlying catalog
record text.

## Statistics

| Metric | Count |
|---|---|
| Layer-2 spec assertions converted | 54 (9 cross-persona/Layer-5, 45 per-persona/Layer-2) |
| Invariants made executable | 7 (I1-I7) |
| New test files | 18 |
| Total vitest tests (this repo, post-milestone) | 149 (3 pass, 143 expected-fail, 3 todo) |
| `CONTROL_REFS` interpretation bindings | 9 |
| Catalog fix required as a precondition | D-032 (4 entries corrected, 90→98) |

## Validation

Full validator green (9 schemas, 8 approved personas, 129 extracted
control records). `npm test` and `npm run typecheck` green (per the
expected-fail semantics above). CI green on the pushed branch.

## Not done in this milestone (explicitly out of scope)

No responsibility-map builder (Milestone 4b). No disposition rules
(Milestone 4c). No `resolve()` implementation (Milestone 4d). No
Layer-3 baselines committed. No Layer-4 relevance review (Milestone
4d). No Phase 5/6 work. No merge to `main`.
