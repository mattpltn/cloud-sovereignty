# Phase 2b report — ECSF extraction

**Branch:** `phase-2b-ecsf` (branched from `main` post Phase 2a squash-merge)
**Scope:** Extract the EU Cloud Sovereignty Framework v1.2.1 (ECSF) into
`/data/extracted/`. C3A and CADA are out of scope for this phase; no
crosswalk work beyond producing unverified hints; `c3a.json` was not
touched.

## Outputs

| File | Purpose |
|---|---|
| `schema/ecsf-scoring.schema.json` | New schema (phase's one authorized addition) for SEAL/domains/weights/formula |
| `data/extracted/ecsf-scoring.json` | SEAL-0..4, all 8 SOV domain definitions + weights + scope, scoring formula |
| `data/extracted/ecsf.json` | 30 control records: ECSF contributing factors, SOV-1..6 |
| `data/local/ecsf-verbatim.json` | 30 verbatim entries, git-ignored, local only (D-009/D-010 regime applied from the start per D-012) |
| `data/extracted/ecsf-c3a-hints.json` | 30 entries mapping ECSF factor id → candidate C3A ids or `"uncovered"` — unverified, Phase 3 input |
| `scripts/extract_ecsf_scoring.py` | Generates `ecsf-scoring.json` |
| `scripts/extract_ecsf.py` | Verbatim transcription + domain-batched writer for `ecsf.json`/`ecsf-verbatim.json` |
| `scripts/build_ecsf_c3a_hints.py` | Generates `ecsf-c3a-hints.json` |
| `scripts/validate.py` | +`check_ecsf_scoring()`, +`check_ecsf_c3a_hints()`; existing `check_local_verbatim()`/`check_verbatim_leak()` extended to the ECSF pair with no code change (both already generic over `data/local/*-verbatim.json`) |
| `docs/DECISIONS.md` | +D-012 (ECSF license basis, and why the D-009/D-010 regime is applied to `ecsf.json` anyway) |
| `docs/METHODOLOGY.md` | +Phase 2b section |

## Statistics

- **ECSF contributing factors extracted:** 30 (SOV-1: 6, SOV-2: 5, SOV-3: 4, SOV-4: 6, SOV-5: 5, SOV-6: 4)
- **Derivation:** 100% verbatim
- **needs_review:** 15/30 (50%) — see breakdown below
- **Coverage hints:** 23/30 (77%) have at least one candidate C3A match; 7/30 (23%) marked `uncovered`

This needs_review rate is markedly higher than Phase 2a's 19% (post
D-007). This is expected: ECSF's "contributing factors" are deliberately
higher-level narrative bullets (a procurement-assessment framework), not
C3A's fine-grained pass/fail criteria, so more of them straddle multiple
responsibility-map layers or address concerns (financing sources,
industrial investment, EU policy alignment, IP location, AI governance)
that C3A's narrower operational/technical scope doesn't cover at all.

## needs_review summary (15 records)

| Records | Reason |
|---|---|
| csat-sov1-ecsf-03, -04, -05 | Layer ambiguity (financing/investment/policy-alignment factors have no clean layer fit) **and** coverage: no C3A analogue |
| csat-sov1-ecsf-06 | Spans legal_jurisdiction (compulsion source) and operations_personnel (continuity); tagged operations_personnel |
| csat-sov2-ecsf-03 | Spans legal_jurisdiction and data/identity (technical access channels); tagged legal_jurisdiction |
| csat-sov2-ecsf-05 | Layer ambiguity (IP jurisdiction hybrid) **and** coverage: no C3A analogue |
| csat-sov3-ecsf-01 | Key-custody control could be identity (IAM) or data; tagged data |
| csat-sov3-ecsf-02 | Access/audit logging spans data vs. platform/operations_personnel, mirroring C3A's SOV-3-04 ambiguity |
| csat-sov3-ecsf-04 | Layer ambiguity (AI/platform vs. data) **and** coverage: C3A has no AI-specific criteria |
| csat-sov4-ecsf-04 | Spans operations_personnel and legal_jurisdiction (support location vs. applicable law) |
| csat-sov5-ecsf-02 | Firmware spans supply_chain_hardware and supply_chain_software; tagged hardware |
| csat-sov5-ecsf-04 | Spans all three post-D-007 supply-chain layers at once, mirroring C3A's SOV-5-04-C pattern |
| csat-sov6-ecsf-01 | Coverage only: no C3A criterion addresses API/protocol openness as such |
| csat-sov6-ecsf-02 | Coverage only: no C3A criterion requires open-license software |
| csat-sov6-ecsf-04 | Spans platform (software ecosystems) and supply_chain_hardware (processors/accelerators); tagged hardware |

Nothing was guessed silently — every flag carries a substantive note, per
working rule 2.

## SOV-7 and SOV-8 handling

- **SOV-7 (Security & Compliance Sovereignty)** is inheritance-only per
  CLAUDE.md (satisfied by C5/ISO 27001/SOC 2 evidence; no questions). No
  control records were produced. Its domain definition, official weight
  (10%), and its 5-factor list are captured as metadata in
  `ecsf-scoring.json` (`scope: "inheritance_only"`) for traceability only.
- **SOV-8 (Environmental Sustainability)** is out of scope per CLAUDE.md.
  Its domain definition and official weight (5%) are captured in
  `ecsf-scoring.json` (`scope: "out_of_scope"`) so the weight table stays
  traceable to the source's full 100%, but its factor list was not
  extracted anywhere in this repo.

## License basis (D-012)

ECSF is an EU Commission (DG DIGIT) procurement document and, per
CLAUDE.md, follows the EU Commission's reuse policy — materially more
permissive than C3A's CC-BY-ND 4.0. On that basis `ecsf-scoring.json`
carries full verbatim text directly in the public repository. `ecsf.json`
was nonetheless put through the same D-009/D-010 verbatim-isolation
regime as C3A, per this phase's explicit instruction, for pipeline
consistency rather than because the license itself demands it — this
asymmetry within a single source framework is intentional and is logged
as D-012 specifically so it reads as a documented choice, not an
oversight. The underlying reuse-policy confirmation for this specific
document remains open, at lower urgency than the C3A question.

## Open items for the project owner

1. **7 candidate-uncovered ECSF factors** (see table above) — worth a
   look at whether any should become new `derived`/`editorial` records in
   Phase 3 (e.g., an EU-financing-source criterion has no C3A analogue at
   all, but might still be worth assessing) or genuinely left out of the
   catalogue's scope.
2. **`ecsf-c3a-hints.json` is unverified** — it is a first-pass thematic
   reading, not a checked equivalence. Phase 3's crosswalk should treat
   every entry as a hypothesis, not a fact.
3. **D-012's asymmetry** (verbatim-public `ecsf-scoring.json` vs.
   verbatim-isolated `ecsf.json`) is intentional per this phase's
   instruction, but is worth revisiting once ECSF's reuse-policy status is
   separately confirmed — it may turn out the isolation regime on
   `ecsf.json` is unnecessary caution, or that `ecsf-scoring.json` should
   have received it too.
4. **`criterion_type: "C"` uniformly on all ECSF records** is a
   schema-fit necessity (ECSF has no C/AC distinction), not a substantive
   claim that these are "baseline" vs. "additional" in ECSF's own terms.

## CI status

Confirmed locally: `scripts/validate.py` (with `data/local/` present, so
the leak check was active throughout extraction), `npm test`, and
`npm run typecheck` (`tsc --noEmit`) all pass — 89 combined control
records valid (59 C3A + 30 ECSF), `ecsf-scoring.json` valid against its
new schema, all 30 `ecsf-c3a-hints.json` references resolve, personas
unaffected, 2 real engine tests still passing, 7 invariants still `todo`.
`git log --name-only` on this branch confirms `data/local/` was never
staged in any commit. Pushed to `origin/phase-2b-ecsf`; GitHub Actions
run confirmed green.

---

Per phase-gate discipline (working rule 6), Phase 2b stops here. CADA
(Phase 2c) extraction and the Phase 3 crosswalk do not start in this
session.

## Addendum (CR-1)

`data/extracted/ecsf-c3a-hints.json` was re-encoded per external review
CR-1 (`reviews/phase-2b-review.md`): each entry is now
`{"coverage": "covered"|"uncovered", "c3a_candidates": [...]}` instead of
a bare list with an `"uncovered"` sentinel string. The candidate mappings
themselves are unchanged. See D-013.

## Phase 2b.1 — Implementation Guidance + official calculator

**Branch:** `phase-2b-ecsf` (same branch, continuation after CR-2 closed
and the reviewer's addendum recommended this small supplement before
merge — see `reviews/phase-2b-review-addendum.md`).

### CR-2 outcome (recap)

The external reviewer independently verified, against the ECSF v1.2.1
PDF and `data/local/ecsf-verbatim.json`: 30/30 factor completeness, text
fidelity on all 30 entries (one accepted deviation — terminal
punctuation normalization at bullet boundaries, now noted in
METHODOLOGY.md), and exact match of weights/SEAL definitions/scoring
formula against v1.2.1 §3/§5. CR-2 is closed; no changes to `ecsf.json`
or `ecsf-scoring.json` resulted.

### New outputs

| File | Purpose |
|---|---|
| `schema/ecsf-guidance.schema.json` | New schema: guidance deltas (weight profile, SEAL aggregation rule, per-domain SEAL-2/3/4 table, SEAL-3 label variant) |
| `data/extracted/ecsf-guidance.json` | The four deltas above, verbatim-isolated |
| `data/local/ecsf-guidance-verbatim.json` | Git-ignored, 25 verbatim entries |
| `schema/ecsf-calculator.schema.json` | New schema: 48 calculator "specific objectives" |
| `data/extracted/ecsf-calculator.json` | 48 records: description, answer options (label/point value/SEAL), coverage hints back to `ecsf.json` |
| `data/local/ecsf-calculator-verbatim.json` | Git-ignored, 285 verbatim entries |
| `scripts/extract_ecsf_guidance.py` | Generates the guidance file pair |
| `scripts/extract_ecsf_calculator.py` | Parses the XLSX algorithmically; generates the calculator file pair |
| `scripts/validate.py` | +`check_ecsf_guidance()`, +`check_ecsf_calculator()`, +`check_verbatim_placeholder_count()`; `check_verbatim_leak()` generalized to cover non-array public files; new `ID_KEYED_VERBATIM_EXCLUSIONS` constant |
| `docs/DECISIONS.md` | +D-014 (dual weight sets), +D-015 (SEAL min-rule, Phase 5 anchor), +D-016 (calculator kept separate from the 30 normative factors) |
| `docs/METHODOLOGY.md` | +Phase 2b.1 section; +punctuation-normalization note added to Phase 2b's extraction rules (CR-2 finding) |

### Key findings (from the reviewer's addendum, now extracted)

- **Dual weight sets** (D-014): the guidance's alternative matrix (SOV-1
  20%, SOV-5 10%, SOV-7 15%; others unchanged from v1.2.1) is also the
  exact weight set the official calculator XLSX itself uses — confirmed
  in this phase by reading the XLSX's own per-domain weight column.
  Neither displaces CSAT's own outcome-derived weighting (design
  principle 5).
- **SEAL minimum-aggregation rule** (D-015): "overall SEAL = lowest
  across objectives" — absent from v1.2.1, logged as a Phase 5
  ceiling-semantics anchor.
- **SEAL-3 relabeled** "Technological Sovereignty" in the guidance vs.
  v1.2.1's "Digital Resilience" — both captured with provenance.
- **Per-domain SEAL-2/3/4 requirements table** — captured, but every row
  flagged `needs_review`: the PDF's table geometry does not survive text
  extraction, so column boundaries are inferred from prose breaks, not
  read from actual cells.
- **Calculator = operationalization layer** (D-016): kept as a separate
  file from the 30 normative `ecsf.json` factors, not merged in. Parsed
  programmatically (openpyxl) rather than transcribed by hand, so the
  sheet's several blank/malformed answer rows (merged-cell artifacts)
  are flagged `needs_review` mechanically rather than repaired or
  guessed. The sheet's own "Score" column (fictitious example values per
  its own disclaimer) was never extracted.

### Statistics

- Guidance: 1 weight profile, 1 SEAL aggregation rule, 8/8 domain rows
  (all flagged `needs_review` for column-boundary inference), 1 label
  variant.
- Calculator: 48 specific objectives (SOV-1: 8, SOV-2: 6, SOV-3: 5,
  SOV-4: 6, SOV-5: 7, SOV-6: 5, SOV-7: 7, SOV-8: 4). 16/48 (33%) flagged
  `needs_review` (malformed source rows and/or SOV-7/SOV-8's
  no-coverage-by-construction). Coverage hints: 37/48 (77%) matched to a
  candidate `ecsf.json` factor; 11/48 (23%) uncovered — all 11 are the
  SOV-7/SOV-8 objectives, which have no `ecsf.json` records to map to at
  all (not a thematic-match failure).

### Validation

Validator green locally (`data/local/{c3a,ecsf,ecsf-guidance,
ecsf-calculator}-verbatim.json` all present, leak check active
throughout); both new schemas validate their files with 0 errors;
`ecsf-calculator.json`'s coverage-hint ids and id-uniqueness confirmed;
the leak check and the new placeholder-count check were both manually
verified to fail on a deliberately injected leak/mismatch, then
reconfirmed clean. `npm test` (2 passing, 7 todo) and `npm run
typecheck` pass. Pushed to `origin/phase-2b-ecsf`; CI green.

### Not done in this phase (explicitly out of scope)

No merge to `main` (owner/reviewer close CR-2's disposition externally;
this phase only adds the recommended 2b.1 supplement). No CADA work. No
crosswalk beyond the coverage hints already described. `c3a.json` and
`ecsf.json` untouched.
