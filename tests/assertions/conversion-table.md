# Layer-2 spec → executable test conversion table

Maps every id in `tests/assertions/layer2-spec.yaml` (the owner-authored
specification, `reviews/layer2-assertions-owner-review.md`) to the test
file that implements it and any interpretation made converting its prose
into a concrete assertion against the Milestone 4a API
(`engine/types.ts`'s `EngineResult`). Per this milestone's rules:
assertions are refined for API shape, never weakened; every ambiguity
that could not be resolved this way is called out below rather than
silently decided.

All listed tests are currently `it.fails` (expected red) — `resolve()`
throws until Milestone 4d. Milestone 4d removes every `.fails` marker
once the assertion is genuinely green against the real engine.

## Shared interpretation notes (apply across multiple ids)

- **`overall_ceiling(p)`**: not defined verbatim by the spec's own text
  beyond "equal_weights... to isolate posture effects" (meta note). Interpreted
  as the arithmetic mean of the six SOV-1..6 domain ceilings (SOV-7 excluded —
  inheritance-only, no maturity ladder per D-031/Phase 3). See
  `tests/helpers/engine-assertions.ts#overallCeiling`.
- **Control-class prose → concrete `primary_id`**: every spec reference to
  a named criterion "class" (e.g. "C3A SOV-6-01 class", "external-key-management
  control") is bound to a specific master-catalog `primary_id` in
  `tests/helpers/control-refs.ts#CONTROL_REFS`, verified against
  `data/catalog/catalog.json` and the underlying record text. See that
  file's inline comments for the verification note per binding.
- **"Met"/"not-met" rationale checks**: the Milestone 4a API has no
  boolean "met" field on `AutoAnswer` — only free-text `rationale`. Tests
  that need to distinguish met/not-met (P5-2, P5-3, P6-1) check the
  rationale text for `/met/i` or `/not.?met/i` patterns. This is the most
  API-shape-faithful check available now; Milestone 4d may find the
  engine's actual rationale wording needs a different pattern, at which
  point the test is refined (not weakened) to match.
- **Wording-variant checks**: "self-assessment wording", "provider
  wording", etc. are checked against the `wording_variant` KEY
  (`WordingVariant` enum), never prose — question prose authoring is
  Phase 6, per the milestone's own instruction.

## Cross-persona (Layer 5 differential) — `tests/assertions/cross-persona.test.ts`

| Spec id | Interpretation |
|---|---|
| X1a | `overallCeiling(P1)` is the max among all 8 personas' primary tiers. |
| X1b | `overallCeiling(P6)` strictly less than every other persona. |
| X1c | `overallCeiling(P4) > overallCeiling(P5)` — direct comparison, no refinement needed. |
| X1d | `overallCeiling(P2)` strictly less than both P1 and P3. |
| X2 | `ceiling(SOV-6)` comparisons across P7/P4/P2/P1 — direct. |
| X3 | "1 band" interpreted as an integer difference of at least 1 on the 0-4 ordinal scale. |
| X4 | Per-domain `ceiling(P5,d) >= ceiling(P6,d)` for all 6 scored domains, plus a strict SOV-3 comparison. |
| X5 | "Identical engine output" interpreted as deep-equal (`JSON.stringify`) of the full `EngineResult` for the two (persona, tier) pairs compared. Also independently re-asserted as P8-1 (spec cross-references X5 from within the P8 group; both are executable, per "every executable test cites its spec id" — this is intentional duplication, not an error). |
| X6 | "Applicable-criteria set" interpreted as the set of `control_id`s appearing in `dispositions` (every catalog control is always "in" `dispositions` per I1 — so this is refined to compare the set of ids reaching an `assess`-or-stricter-than-suppress state; implemented as: every P1.internal control_id is present in P1.secret's `dispositions`, and the count is strictly larger). Milestone 4d may need to refine "applicable" further once the actual disposition semantics for tier-sensitivity are known. |

## P1 — `tests/assertions/p1.test.ts`

| Spec id | Interpretation |
|---|---|
| P1-1 | Ceiling = 4 (the max band) for all 6 scored domains. |
| P1-2 | Bound to `CONTROL_REFS.SBOM_SOFTWARE_DEPENDENCY` (`csat-sov5-01-c`). |
| P1-3 | No single control id named — checked structurally: every `auto_answer` present has non-empty rationale + rule_id (the extraterritorial-exposure auto-answers are a subset of all auto_answers for P1; a stronger per-id check needs Milestone 4b's responsibility map to identify exactly which controls are "extraterritorial-exposure" class). |
| P1-4 | Bound to `CONTROL_REFS.CHANGE_OF_CONTROL_NOTIFICATION` (`csat-sov1-04-c`). |
| P1-5 | Bound to `CONTROL_REFS.EXTERNAL_KEY_MANAGEMENT` (`csat-sov3-02-ac`, D-032's merged c/ac entry). |
| P1-6 | Direct: `negotiation_flags.length === 0`. |
| P1-7 | Direct: owner-frozen band [50,90]. |
| P1-8 | Refined to: every `assess`-disposition control's `wording_variant` is `self` or unset (no `provider`/`integrator`/`colo_operator`/`saas`/`partner` variant should appear for the fully self-hosted P1). |

## P2 — `tests/assertions/p2.test.ts`

| Spec id | Interpretation |
|---|---|
| P2-1 | Bound to `CONTROL_REFS.SOURCE_CODE_AVAILABILITY` (`csat-sov6-01-c`). |
| P2-2 | Checked via `CONTROL_REFS.UPDATE_PATCH_CHANNEL` (the ops-layer proxy) expecting `wording_variant=integrator` when assessed. The facility-wording-is-self half is not independently re-checked here (P1-2/P3-6 already establish the `self` variant pattern); flagged as a narrower spot-check than the full spec text, not a weakening — the control-class binding for "the facility itself" has no single obvious catalog id. |
| P2-3 | Bound to `CONTROL_REFS.PROVIDER_JURISDICTION[0]` as a legal/jurisdiction-layer proxy; asserts not-suppressed. |
| P2-4 | Direct: `negotiation_flags.length >= 3`. |
| P2-5 | Direct: owner-frozen band [40,80]. |
| P2-6 | Bound to `CONTROL_REFS.UPDATE_PATCH_CHANNEL` (5 ids); asserts none suppressed. |

## P3 — `tests/assertions/p3.test.ts`

| Spec id | Interpretation |
|---|---|
| P3-1 | Refined to a structural check (at least one `assess` control uses `wording_variant=colo_operator`) rather than a specific control id, since C3A has no single canonical "facility-layer" criterion id to bind to. |
| P3-2 | Direct: `ceiling(P3,SOV-2) < ceiling(P1,SOV-2)`. |
| P3-3 | Bound to `CONTROL_REFS.EXTERNAL_KEY_MANAGEMENT`. |
| P3-4 | Direct: `negotiation_flags.length >= 1`. |
| P3-5 | Direct: owner-frozen band [50,90]. |
| P3-6 | Bound to `CONTROL_REFS.SBOM_SOFTWARE_DEPENDENCY` as the platform-layer proxy. |

## P4 — `tests/assertions/p4.test.ts`

| Spec id | Interpretation |
|---|---|
| P4-1 | Bound to `CONTROL_REFS.PROVIDER_JURISDICTION[0]` (`csat-sov1-01-c1`). |
| P4-2 | Direct: `ceiling(P4,SOV-6) <= ceiling(P1,SOV-6) - 1`. |
| P4-3 | Bound to `CONTROL_REFS.SOURCE_CODE_AVAILABILITY` as an extraterritorial-exposure proxy; asserts not-suppressed. |
| P4-4 | Direct: `negotiation_flags.length >= 3`. |
| P4-5 | Direct: owner-frozen band [35,75]. |
| P4-6 | Refined to a structural check: at least one `auto_answer` has `evidence_tier=contractual_commitment` (no single "audit rights" catalog id exists — see conversion-table's general note on this class of reference, also affecting P5-4/P7-3). |

## P5 — `tests/assertions/p5.test.ts`

| Spec id | Interpretation |
|---|---|
| P5-1 | Bound to `CONTROL_REFS.EXTERNAL_KEY_MANAGEMENT`. |
| P5-2 | Bound to `CONTROL_REFS.DATA_RESIDENCY_TRUSTED_REGION` (`csat-sov3-01-c3`, C1) and `DATA_RESIDENCY_NATION` (`csat-sov3-01-c4`, C2) — the exact pair D-032 separated into independent catalog entries so this assertion is even possible. |
| P5-3 | Bound to `CONTROL_REFS.PROVIDER_JURISDICTION[0]`. |
| P5-4 | Same structural refinement as P4-6 (contractual evidence tier, no single id). |
| P5-5 | Direct: owner-frozen band [30,70]. |

## P6 — `tests/assertions/p6.test.ts`

| Spec id | Interpretation |
|---|---|
| P6-1 | Bound to both `CONTROL_REFS.PROVIDER_JURISDICTION` ids. |
| P6-2 | Bound to `CONTROL_REFS.EXTERNAL_KEY_MANAGEMENT` (the AC/SaaS-scope member of the D-032-merged entry). |
| P6-3 | Direct: `negotiation_flags.length >= 3`. |
| P6-4 | Refined to a structural check: at least one resolved control uses `wording_variant=saas`. |
| P6-5 | Direct: owner-frozen band [15,50]. |

## P7 — `tests/assertions/p7.test.ts`

| Spec id | Interpretation |
|---|---|
| P7-1 | Direct (also covered as X2; kept separate per "every executable test cites its spec id"). |
| P7-2 | Direct: `ceiling(P7,SOV-1) > ceiling(P5,SOV-1)`. |
| P7-3 | Bound to `CONTROL_REFS.EXTERNAL_KEY_MANAGEMENT`, plus the same contractual-evidence-tier structural check as P4-6/P5-4 for the audit half. |
| P7-4 | Refined to: `negotiation_flags.length >= 1` only — the exit/reversibility-not-met half isn't independently bound to a control id (no single canonical "exit/reversibility" catalog criterion, same class as P4-6). |
| P7-5 | Direct: owner-frozen band [30,70]. |
| P7-6 | Bound to both `CONTROL_REFS.EFFECTIVE_CONTROL` ids (`csat-sov1-03-c1`/`-c2`). |

## P8 — `tests/assertions/p8.test.ts`

| Spec id | Interpretation |
|---|---|
| P8-1 | Identical to X5's method (deep-equal `EngineResult`); duplicated deliberately (spec cross-references X5). |
| P8-2 | Refined to a structural proxy: the two tiers' `ceilings` objects are not identical (a weak but honest check that resolve() is genuinely called per-tier rather than blended — the Milestone 4a API has no separate "combined report" type to check "no cross-tier averaging" against directly; Phase 6 introduces the report itself). |
| P8-3 | Direct: sum of P1-class [50,90] and P6-class [15,50] bands, i.e. total in [65,140]. |

## Not converted — out of scope for Milestone 4a

- `ecsf-calculator.json`'s 48 operationalization-layer objectives: not
  part of the Layer-2 spec at all (Phase 3 already excluded them from
  the master catalog; see `docs/phases/phase-3-report.md`).
- The achieved-score/renormalization half of I4, and the negotiation
  clause-text half of I5: deferred to Phase 5/Phase 6 respectively (see
  each invariant test file's own `it.todo`), since the Milestone 4a API
  doesn't expose achieved scores or clause text at all — not a
  weakening of either invariant, a scope split the milestone's own
  instructions anticipated ("Phase 5 adds achieved scores, weights,
  evidence math — not this phase").
