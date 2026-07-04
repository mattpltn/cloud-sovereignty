# Methodology

This document is written incrementally: each phase appends the section
describing exactly what was done and how (extraction rules, substitution
rules, disposition logic, scoring math, testing method). A phase does not
merge without its section here. See `CLAUDE.md` for the full project
charter, source frameworks, and phase plan.

**Extraction conventions (all phases):** terminal punctuation at
criterion/list boundaries is normalized to a period, and line-break
hyphenation artifacts introduced by PDF text extraction are reconstructed
into whole words. All other characters — including source typos — are
preserved exactly as printed, flagged `needs_review` with an explanatory
note rather than silently corrected (working rule 2). Confirmed source
errata caught by this discipline so far: BSI SOV-4-02-C2 (Phase 2a), the
Article 18/19 cross-reference in the CADA proposal (Phase 2c), the ECSF
Implementation Guidance's "ELA 3." (Phase 2b.1), and CADA Annex II
2.1(d)'s "presonnel" (Phase 2c, see D-018 on `phase-2c-cada`).

---

## Phase 0 — Repository setup

The repository was initialized as a public GitHub repo
(`mattpltn/cloud-sovereignty`) containing the project charter
(`CLAUDE.md`) and the four source framework PDFs. No project structure
existed beyond this. See `docs/DECISIONS.md` D-002 for the subsequent
decision to hold the source PDFs back from the public repo on license
grounds.

## Phase 1 — Schema, personas, test harness skeleton

### Schemas (`/schema`)

Four JSON Schemas, Draft 2020-12:

- **`lang-string.schema.json`** — the shared language-keyed string type
  (`{"en": ..., "fr": ...}`, extensible to further languages) used by every
  human-readable field elsewhere, per the i18n-from-day-one design
  principle.
- **`control-record.schema.json`** — a single catalog criterion. Encodes:
  the SOV domain and layer it addresses (used later by the disposition
  engine and by invariant I2); its `derivation` tier
  (verbatim/generalized/derived/editorial); `source_refs` (framework +
  exact section ID); either `source_text` (verbatim, language-keyed) or
  `source_pointer` (document + section, used when verbatim reproduction
  isn't confirmed permitted — see D-002) — exactly one of the two is
  required; `generalized_text` with the placeholders it uses; a
  `disposition_default`; evidence-quality options; a weight; and the
  `needs_review` flag with a required note when set.
- **`persona-profile.schema.json`** — a persona or real assessment
  profile: a 5-item sovereignty-outcome priority ranking, a classification
  scheme, and one `tier_scenario` per workload tier assessed (Axis A/B,
  modifiers). Supports multiple tiers per persona to exercise
  classification tiering (e.g. P8).
- **`disposition-rule.schema.json`** — a declarative rule for the Phase 4
  responsibility-map/disposition engine: a condition matched against a
  control's layer/domain and a persona tier's axis/modifiers, mapping to a
  disposition. Every rule is `derivation: editorial` by construction (rules
  encode a project judgment about who holds responsibility for a layer
  under a given scenario) and must carry a `decision_ref` pointing to a
  `docs/DECISIONS.md` entry.

**Validation approach:** each schema was checked against the Draft
2020-12 meta-schema, and each was exercised against a hand-written example
instance (see git history for the exact test script). This caught one real
bug: an `if`/`then` conditional using
`"if": {"properties": {"negotiation_opportunity": {"const": true}}}`
vacuously matched when the property was *absent* (JSON Schema's
`properties` keyword only constrains properties that are present), wrongly
requiring `negotiation_clause` on every record. Fixed by adding
`"required": ["negotiation_opportunity"]` to the `if` clause. The same
pattern was checked and found *not* to be a problem in the other
conditionals in these schemas, because their `if` keys (`status`,
`disposition`, `derivation`) are always-required fields and therefore
never absent.

### Golden personas (`/tests/personas`)

All 8 golden personas from the charter (P1-P8) were drafted as separate
YAML files, each with `status: draft` and inline comments explaining every
field, per the persona ownership workflow. Each validates against
`persona-profile.schema.json`. Two modeling choices needed for fields that
presuppose a third-party provider (which A1 self-hosted and A5
licensed-partner scenarios don't cleanly have) are logged in
`docs/DECISIONS.md` D-003 and flagged inline for project-owner review.

Claude Code does not set `status: approved` on any persona file — only the
project owner does, per the ownership workflow.

### Test harness (`/engine`, `/tests`)

A minimal Node/TypeScript project (`package.json`, `tsconfig.json`) hosts
the engine and its tests, run via `vitest`:

- **`/engine`** — `types.ts` mirrors the JSON Schemas as TypeScript types
  (hand-kept in sync; no schema-to-type generation at this scale).
  `index.ts` exports a single `resolveDispositions()` stub that throws
  "not implemented until Phase 4" — this gives the test harness and its
  imports something real to compile against without pretending Phase 4
  logic exists yet.
- **`/tests/helpers/personas.ts`** — loads persona YAML fixtures and
  exposes `loadApprovedPersonas()`, which filters to `status: approved`.
  This is the Node-side half of the persona-approval gate ("the test
  runner MUST refuse to execute engine tests against any persona not
  marked approved"); `scripts/validate.py` is the Python-side half (below).
  A real, passing test (`personas.test.ts`) confirms the loader finds all
  8 fixtures and that zero are currently approved.
- **`/tests/invariants/i1-*.test.ts` through `i7-*.test.ts`** — one file
  per invariant defined in `CLAUDE.md`'s Testing methodology section, each
  carrying the invariant's definition as a docstring and a single
  `it.todo(...)` describing the assertion to be implemented once the
  catalog (Phase 3) and disposition engine (Phase 4) exist. `it.todo` was
  chosen over `it.skip` with a runtime condition: the invariants cannot be
  implemented at all yet (no engine), so marking them structurally
  unimplemented is more honest than a condition that happens to currently
  evaluate false.

`npm run typecheck` (`tsc --noEmit`) and `npm test` (`vitest run`) both
pass clean as of this phase: 2 real tests passing, 7 invariants correctly
reported as `todo`, 0 TypeScript errors.

### Validator (`scripts/validate.py`)

Python, run inside a project-local venv (`python3 -m venv .venv && .venv/bin/pip
install -r scripts/requirements.txt` — the system Python on the reference
development machine is externally managed per PEP 668 and rejects global
installs). Responsibilities:

1. Every file in `/schema` is itself a valid Draft 2020-12 JSON Schema.
2. Every persona fixture in `/tests/personas` validates against
   `persona-profile.schema.json`.
3. Persona-approval gate: any persona with `status: approved` must carry
   `approved_by` and `approved_date` (already enforced structurally by the
   schema's own conditional; re-checked here with a clearer error message
   since this is the field most likely to be hand-edited incorrectly).
4. Prints a summary (schemas checked, personas checked, draft vs. approved
   counts) and exits non-zero on any failure.

`/data/catalog` validation against `control-record.schema.json` is
deferred to Phase 2+, once extraction produces records to validate — no
speculative validation code was written for a data shape that doesn't
exist yet.

Both the schema/example-instance checks and the persona-fixture checks
were exercised against deliberately broken inputs (a schema conditional
bug, and a persona missing required fields / falsely marked approved) to
confirm the validators actually fail when they should, not just pass
trivially.

### CI (`.github/workflows/ci.yml`)

Two jobs on every push and pull request: `validate-python` (installs
`scripts/requirements.txt`, runs `scripts/validate.py`) and `test-engine`
(installs npm deps, runs `npm run typecheck` and `npm test`). No job
depends on `/data` or `/sources` yet.

### Testing methodology — status at end of Phase 1

Of the five test layers defined in `CLAUDE.md`:

- **Layer 1 (Invariants)** — I1-I7 stubbed with definitional docstrings,
  not yet implemented (depends on Phases 3-5).
- **Layer 2 (Persona spot-checks)** — not started; written by the project
  owner against *approved* personas, which don't exist yet.
- **Layer 3 (Snapshot diffs)** — not started; depends on the engine
  existing.
- **Layer 4 (Relevance review / LLM-as-judge)** — not started; scheduled
  for the ends of Phases 4, 5 and 6.
- **Layer 5 (Differential pairs)** — not started; depends on the engine.

No layer is expected to be substantively implemented until its
prerequisite phase (catalog, engine, scoring) exists — Phase 1's job was
to make sure the *shape* everything else plugs into is correct and
tested, which it is.

## Phase 2a — BSI C3A extraction

### Source and tooling

`sources/C3A_Cloud_Computing_Autonomy.pdf` (BSI C3A v1.0, 27.04.2026), 16
pages, held locally per D-002/D-005 (git-ignored, not published). Text was
extracted with `pypdf` (`poppler-utils`/`pdftotext` were not installable
in this environment — no passwordless sudo — so the Read tool's PDF
renderer, which depends on `pdftoppm`, could not be used; `pypdf`'s text
extraction proved clean and complete for this document, verified against
the table of contents' section list and page count). The raw extracted
text was read in full and hand-transcribed, criterion by criterion, into
`scripts/extract_c3a.py`, then cross-checked against the raw extraction
before each domain batch was written out.

### Extraction rules applied

- **Unit of extraction:** one control record per criterion (C) or
  additional criterion (AC), per CLAUDE.md's Phase 2a instruction to
  capture "every criterion (C) and additional criterion (AC)... nothing
  skipped, nothing merged, nothing invented."
- **Criterion type from the explicit label, not the ID suffix.**
  `SOV-4-01-C3` is printed with a "C3"-style ID but is explicitly labelled
  "Additional criterion" in the source text — it is extracted as
  `criterion_type: AC`. This is the only such mismatch found in the
  document; every other ID suffix and label agree.
- **Supplementary Information (SI) blocks are out of scope for this
  phase.** The schema's `criterion_type` enum has no SI value, and the
  Phase 2a instruction named only C and AC. SI text is neither extracted
  as a record nor folded into another record's `source_text` (which would
  corrupt verbatim accuracy). It remains available in the source PDF for
  a later phase if the app's UI wants to surface it as contextual help.
- **`derivation: verbatim` for all 59 records** — no generalization, no
  placeholder substitution. That is Phase 2d.
- **`localization_level` (C1=EU / C2=Germany) is set only for genuine
  paired variants** of the identical requirement (same subject/scope,
  differing only in EU-vs-Germany jurisdiction) — 20 of 59 records
  qualify. Criteria that merely mention "EU" or "Germany" without a
  paired counterpart of the *same* requirement are left untagged, even
  where the source's own ID suffix might suggest otherwise. The clearest
  example is `SOV-3-01`: five criteria share the ID stem, but only C3
  (EU, customer data) and C4 (Germany, customer data) are a true pair —
  C1 (a generic customer-visibility requirement), C2 (EU-only, derived +
  account data) and C5 (EU-only, provider data) have no jurisdictional
  counterpart in the document, so none of the three are tagged.
- **`fr` fields carry the literal placeholder `"FR-TRANSLATION-PENDING"`**
  in both `source_text` and `generalized_text`, per D-006 — framework text
  is not machine-translated, since that would itself be a derivative work
  under C3A's CC-BY-ND license.
- **`layer` is a best-effort mapping** to the responsibility-map layer
  enum from Phase 1, revised in Phase 2a's CR-2 response (D-007): the
  original eight-value enum's single `hardware_supply_chain` catch-all was
  split into `supply_chain_hardware`, `supply_chain_software`,
  `supply_chain_services`, and the 7 affected SOV-5 records were retagged
  by subject matter. This cleared 4 of the original 15 `needs_review`
  flags outright; 11 of 59 records (~19%) still carry `needs_review: true`
  — the remainder are either genuine multi-layer criteria (e.g. `SOV-2-03`
  State of Defense Takeover touches legal, facility, and personnel at
  once; `SOV-5-04` export restrictions still spans all three post-split
  supply-chain layers) or, for one record family (`SOV-4-02-C2`), a
  verbatim source-text inconsistency (see D-008: reviewer-confirmed
  against the published PDF, kept verbatim as printed per working rule 4,
  intended meaning to be handled via a generalization_note in Phase 2d).
- **`disposition_default: assess`, `weight: 1.0`, and the full four-tier
  `evidence_quality_options`** are uniform placeholders across all 59
  records — scenario-dependent disposition is Phase 4 rule work; weighting
  and evidence-tier applicability are Phase 5 scoring work.
- **`source_pointer` (document, section, page) is populated on every
  record**, alongside verbatim `source_text` — an extension of D-002
  logged as D-005, specific to this extraction working stage (see
  DECISIONS.md; the public-catalog-record default from D-002 is
  unchanged and still open).

### Statistics

| | |
|---|---|
| Total records | 59 |
| By domain | SOV-1: 7, SOV-2: 5, SOV-3: 15, SOV-4: 19, SOV-5: 9, SOV-6: 4 |
| By criterion_type | C: 43, AC: 16 |
| By derivation | verbatim: 59 (100%) |
| By layer | data: 14, platform: 13, legal_jurisdiction: 12, operations_personnel: 7, supply_chain_hardware: 3, supply_chain_software: 2, supply_chain_services: 2, identity: 4, facility: 2, virtualization: 0 |
| needs_review | 11 (19%), down from 15 after D-007's supply-chain layer split |
| localization_level set | 20 (34%) |

### Validation

`scripts/validate.py` was extended this phase to validate every record in
`/data/extracted/*.json` against `control-record.schema.json` (previously
deferred from Phase 1, since no extracted data existed yet) and to check
`id` uniqueness within each file — the schema itself can't express
array-level uniqueness. All 59 records validate clean; extraction
proceeded in six batches (one per SOV domain), each run through the
validator before committing, per working rule 1.

### Response to review (CR-2)

Three follow-ups were made to the initial extraction in response to a
project-owner review, before Phase 2b started:

1. **D-007 — supply-chain layer split**, described above.
2. **D-008 — SOV-4-02-C2 erratum confirmed, not corrected.** The reviewer
   checked the published PDF directly (p. 11) and confirmed the record's
   verbatim text is printed exactly as extracted (sentence 1: "within the
   EU"; sentence 2: "outside Germany"). The record is left untouched; the
   likely-intended meaning ("within Germany") will be captured via a
   `generalization_note` referencing D-008 when Phase 2d performs
   placeholder substitution — not by silently editing the verbatim
   capture now.
3. **D-009 — verbatim text moved out of the public artifact.**
   `data/extracted/c3a.json` (public, git-tracked) had every record's
   `source_text` language values replaced with the literal placeholder
   `"SEE-LOCAL-VERBATIM"`. The real verbatim text moved to
   `data/local/c3a-verbatim.json`, keyed by record `id`, which is
   git-ignored. `scripts/validate.py` now checks, when
   `data/local/c3a-verbatim.json` is present, that every record has a
   matching verbatim entry and vice versa; when the file is absent (e.g.
   in CI, which never has it), that check is skipped with a printed
   notice rather than failing. This directly implements D-002/D-005's
   still-open license caution rather than resolving it — the underlying
   BSI/counsel question is unchanged.

A follow-up review (`reviews/phase-2a-review-addendum-2.md`) found D-009
incomplete — `generalized_text` still carried the full verbatim text —
and recommended a squash-merge to keep that residual exposure out of
`main`'s history. Both were addressed (D-010, D-011) and the branch was
merged; see `docs/phases/phase-2a-report.md` for the full response.

## Phase 2b — ECSF extraction

### Source and scope

`sources/Cloud-Sovereignty-Framework.pdf` (EU Cloud Sovereignty Framework
v1.2.1, Oct. 2025 — the European Commission's DG DIGIT procurement
document), read locally per D-002, extracted with `pypdf` (the same
approach used in Phase 2a; `poppler-utils` remains unavailable on this
machine without passwordless sudo). The document is only 6 pages and is
structurally different from C3A: it defines a maturity scale and a
scoring model, not a criteria catalogue. Three shapes were extracted, per
phase scope:

1. **SEAL scale, domain definitions, weights, scoring formula** →
   `data/extracted/ecsf-scoring.json`, conforming to a new schema,
   `schema/ecsf-scoring.schema.json` (the phase's one authorized new
   schema — no existing schema was modified).
2. **Contributing factors, SOV-1..6** → `data/extracted/ecsf.json`, as
   `control-record.schema.json` records (the existing schema is generic
   enough across frameworks — its `source_refs.framework` enum already
   included `"ECSF"` from Phase 1).
3. **ECSF-to-C3A coverage hints** → `data/extracted/ecsf-c3a-hints.json`,
   an unverified candidate crosswalk for Phase 3 to check, not to trust.

SOV-7 (SOV-7 in ECSF, "Security & Compliance Sovereignty") is
inheritance-only per CLAUDE.md — it produces no control records. Its
domain definition, weight, and factor list are captured as metadata in
`ecsf-scoring.json` (`scope: "inheritance_only"`) purely for traceability.
SOV-8 ("Environmental Sustainability") is out of scope per CLAUDE.md; its
domain definition and weight are captured (`scope: "out_of_scope"`) but
its factor list is not extracted.

### License basis and the D-012 asymmetry

CLAUDE.md states ECSF (like CADA) "follows EU Commission reuse policy" —
materially more permissive than C3A's CC-BY-ND 4.0 (see D-012). On that
basis, `ecsf-scoring.json` carries full verbatim ECSF text directly in
the public file; no local/public split was applied to it. `ecsf.json`,
however, **is** put through the same D-009/D-010 verbatim-isolation
regime as C3A from the start (public `source_text`/`generalized_text`
placeholdered as `"SEE-LOCAL-VERBATIM"` / `"GENERALIZATION-PENDING"`;
real text in git-ignored `data/local/ecsf-verbatim.json`), per this
phase's explicit instruction, for pipeline consistency rather than a
license determination. D-012 records this intentional asymmetry so it
reads as a documented choice, not an inconsistency.

Because `scripts/validate.py`'s `check_local_verbatim()` and
`check_verbatim_leak()` (D-009/D-010) both iterate generically over every
`data/local/*-verbatim.json` file and match it to a same-named public
file, no code change was needed to extend either check to the ECSF pair
— adding `data/local/ecsf-verbatim.json` was sufficient. Two new checks
were added instead: `check_ecsf_scoring()` (validates `ecsf-scoring.json`
against the new schema, when present) and `check_ecsf_c3a_hints()`
(confirms every id referenced in the hints file exists in `ecsf.json` or
`c3a.json` — a typo/dangling-reference guard, not a correctness check on
the mapping itself).

### Extraction rules applied

- **`criterion_type` set to `"C"` uniformly.** ECSF's contributing
  factors have no baseline/additional distinction (unlike C3A's C/AC);
  `"C"` is the schema-required value that best fits "this is a baseline
  factor." Documented here as a schema-fit mapping, not logged as a
  separate DECISIONS entry since `derivation` remains `verbatim` and no
  substantive judgment about the factor's content is involved.
- **One record per bullet.** Each contributing-factor bullet under ECSF
  §4 becomes one control record; `id`s follow `csat-sov{n}-ecsf-{k:02d}`
  to avoid colliding with C3A's `csat-sov{n}-{criterion}-{c1/c2}` pattern
  in the same id-space.
- **Layer tagging** followed the same D-007 ten-value enum and, where
  possible, the precedent set by how C3A's own criteria in the same SOV
  domain were tagged in Phase 2a (e.g. SOV-1 → `legal_jurisdiction`,
  SOV-3 key-custody → `data`, matching C3A's SOV-3-01/02 convention over
  SOV-3-03's `identity`/IAM convention).
- **Coverage hints are separate from layer-tagging ambiguity.** A
  `needs_review` flag can fire for either reason (or both, noted
  together in `needs_review_note`): the layer taxonomy doesn't cleanly
  fit the factor, or no C3A criterion appears to address it at all. The
  latter carries the literal phrase `"Coverage: candidate uncovered
  factor — verify in Phase 3"` so it's greppable independent of the
  layer-ambiguity prose around it.
- **`ecsf-c3a-hints.json` does not modify `c3a.json` or `ecsf.json`.** It
  is a separate, additive lookup table; Phase 3 owns turning any of these
  candidate mappings into an authoritative crosswalk (or rejecting them).
- **Terminal punctuation normalized at bullet boundaries.** Where the
  source PDF's bullet text runs on without a final period (or with
  inconsistent trailing punctuation across otherwise-parallel bullets),
  a terminal period was added/normalized for readability. This is the
  only accepted deviation from strict verbatim transcription, confirmed
  in the external Phase 2b review (`reviews/phase-2b-review-addendum.md`,
  CR-2 fidelity check) as not affecting substance.

### Statistics

| Metric | Value |
|---|---|
| ECSF factors extracted (SOV-1..6) | 30 |
| Per domain | SOV-1: 6, SOV-2: 5, SOV-3: 4, SOV-4: 6, SOV-5: 5, SOV-6: 4 |
| Derivation | 100% verbatim |
| By layer | legal_jurisdiction: 10, platform: 6, operations_personnel: 4, data: 3, supply_chain_services: 3, supply_chain_hardware: 3, supply_chain_software: 1 |
| needs_review | 15/30 (50%) — 8 layer-ambiguity only, 7 also/only flagged as candidate-uncovered coverage |
| Coverage hints: candidate C3A match found | 23/30 (77%) |
| Coverage hints: uncovered | 7/30 (23%) — csat-sov1-ecsf-03/04/05 (financing, investment/jobs, EU-initiative alignment), csat-sov2-ecsf-05 (IP location), csat-sov3-ecsf-04 (AI governance), csat-sov6-ecsf-01/02 (API openness, open-license software) |
| SOV-7 factors (metadata only, no records) | 5 |
| SOV-8 | out of scope, domain definition + weight only |

The higher needs_review rate versus Phase 2a's 19% is expected, not a
quality regression: ECSF's "contributing factors" are deliberately
higher-level and more abstract than C3A's fine-grained pass/fail
criteria, so more of them either straddle multiple responsibility layers
or fall outside the narrower, more operational scope of C3A entirely
(financing, industrial policy, IP location, and AI governance have no
C3A analogue at all).

### Validation

All 89 combined control records (59 C3A + 30 ECSF) validate against
`control-record.schema.json`; `ecsf-scoring.json` validates against the
new `ecsf-scoring.schema.json`; `ecsf-c3a-hints.json`'s 30 keys and every
referenced C3A id were confirmed to resolve. The validator was run
locally with `data/local/{c3a,ecsf}-verbatim.json` present throughout
extraction so the leak check stayed active (it is always skipped in CI,
which never has `data/local/`).

## Phase 2b.1 — ECSF Implementation Guidance and official calculator

### Source and scope

Two further Commission documents, placed in `/sources` after the
external Phase 2b review: `Cloud Sovereignty Framework - Implementation
guidance.pdf` (a post-tender guidance document, extracted with `pypdf`)
and `Annex - Sovereignty assessment calculator.xlsx` (the official
Cloud III DPS tender calculator, a single sheet, parsed with
`openpyxl`). The review's addendum (`reviews/phase-2b-review-addendum.md`)
found these are a material second source, diverging from v1.2.1 in ways
relevant to later phases. Two shapes were extracted:

1. **Guidance deltas** → `data/extracted/ecsf-guidance.json`, a new
   schema `schema/ecsf-guidance.schema.json`: the alternative weight
   matrix (named profile `ecsf_guidance_matrix`, D-014), the SEAL
   minimum-aggregation rule (D-015), the per-domain SEAL-2/3/4
   requirement descriptions, and the SEAL-3 label variant
   ("Technological Sovereignty" vs. v1.2.1's "Digital Resilience").
   `ecsf-scoring.json` (Phase 2b) was **not** modified.
2. **Calculator specific objectives** → `data/extracted/ecsf-calculator.json`,
   a second new schema `schema/ecsf-calculator.schema.json` (documented
   choice, D-016): all 48 "specific objectives" across SOV-1..8, each
   with its description, answer options (label, point value, SEAL
   level), and a provisional coverage hint back to the relevant
   `ecsf.json` factor(s).

Both extraction scripts (`scripts/extract_ecsf_guidance.py`,
`scripts/extract_ecsf_calculator.py`) apply the D-009/D-010
verbatim-isolation regime from the start: public lang-string fields are
scrubbed to `"SEE-LOCAL-VERBATIM"`; real text lives only in
`data/local/ecsf-guidance-verbatim.json` and
`data/local/ecsf-calculator-verbatim.json` (both git-ignored).

### Why the calculator was parsed programmatically, not hand-transcribed

`extract_ecsf_calculator.py` reads the XLSX directly with `openpyxl`
rather than hand-transcribing rows, specifically so that blank/malformed
rows (several exist — apparent merged-cell artifacts in the source
workbook that leave some rows with only a SEAL value and no label/point
value, or a stray numeric value where a text label is expected) are
detected mechanically and flagged `needs_review`, rather than silently
repaired or guessed by a human transcriber. The sheet's own "Score"
column (a worked example the sheet's own header note calls fictitious)
is never read.

### Why the guidance's SEAL-2/3/4 table is marked needs_review throughout

The Implementation Guidance PDF's per-domain SEAL-2/3/4 requirements
table (page 10) does not survive `pypdf` text extraction as distinct
cells — the reflowed text runs each domain's three columns together as
one paragraph. Column boundaries in `ecsf-guidance.json`'s
`domain_seal_requirements` were inferred from sentence/punctuation
breaks in that reflow, not read from the source table's actual
geometry. Every one of the 8 domain rows is therefore marked
`needs_review` with an explanatory note, rather than presenting an
inferred split as certain (working rule 2). SOV-8's SEAL-3 cell has no
text distinguishable from its SEAL-2/SEAL-4 neighbors in the reflow at
all and was left absent rather than guessed.

**CR-1 refinements (external fidelity check):** SOV-7's SEAL-3 cell
reads "ELA 3." in the source PDF — almost certainly a typo for "EAL 3"
(Evaluation Assurance Level, matching the "EAL2"/"EAL 4-5" phrasing in
the same row's SEAL-2/SEAL-4 cells). Preserved verbatim per the
extraction-conventions rule above rather than silently corrected; its
`needs_review_note` now names this explicitly as an erratum candidate.
SOV-8's row prints only two visually distinct source cells across the
three SEAL columns; this extraction's seal_2/seal_4 assignment is an
interpretation based on sentence content, not a confirmed reading of the
table's actual cell boundaries for this specific row — its
`needs_review_note` now says so explicitly, pending visual confirmation
of the source table layout.

### Coverage hints (calculator → v1.2.1 factors)

Built the same way as the Phase 2b `ecsf-c3a-hints.json` (CR-1 coverage-
object encoding, D-013): by reading the calculator's 48 objective titles
against the Implementation Guidance's own "Criteria" bullets (pages 3-5),
which are near-identical wording to the `ecsf.json` factor text already
extracted in Phase 2b. Several v1.2.1 factors are split across two
calculator objectives (e.g. `csat-sov1-ecsf-02` covers both "Change of
Control Risk" and "Control Over Roadmap"). SOV-7 and SOV-8 objectives
(11 of 48) are marked `"uncovered"` by construction, since Phase 2b
produced no `ecsf.json` records for those two domains at all — not
because no thematic analogue could be found.

### Validator extensions

`ecsf-guidance.json` (a single nested object, not a record array) and
`ecsf-calculator.json` (a record array whose ids don't match the
verbatim file's finer per-field keys) don't fit the existing generic
`check_local_verbatim()` id-set cross-check, so both are added to a new
`ID_KEYED_VERBATIM_EXCLUSIONS` set and skipped by that specific check.
`check_verbatim_leak()`'s outer loop was generalized (it already
recursed through dicts via `walk_strings`; only the top-level "is this a
list of records" assumption needed relaxing) so both files remain
covered by the leak check itself. A new, shape-agnostic
`check_verbatim_placeholder_count()` replaces the id-set check for these
two files: it asserts the count of `SEE-LOCAL-VERBATIM` placeholders in
the public file equals the number of entries in the matching local
verbatim file — a weaker signal than exact id matching, but one that
still catches a field scrubbed-but-never-isolated (or the reverse) for
either file shape. Two ordinary schema-validation checks,
`check_ecsf_guidance()` and `check_ecsf_calculator()`, were added
following the existing `check_ecsf_scoring()` pattern;
`check_ecsf_calculator()` additionally checks `ecsf_factor_hints`
candidate ids resolve against `ecsf.json` and that calculator ids are
unique, mirroring `check_ecsf_c3a_hints()`.

### Statistics

| Metric | Value |
|---|---|
| Guidance deltas captured | 1 weight profile, 1 SEAL aggregation rule, 8 domain SEAL-2/3/4 rows, 1 SEAL label variant |
| Domain SEAL-2/3/4 rows needing review | 8/8 (100%) — column-boundary inference, see above |
| Calculator specific objectives extracted | 48 (SOV-1: 8, SOV-2: 6, SOV-3: 5, SOV-4: 6, SOV-5: 7, SOV-6: 5, SOV-7: 7, SOV-8: 4) |
| Calculator objectives needing review | 16/48 (33%) — malformed/blank source rows and/or SOV-7/SOV-8 no-coverage-by-construction |
| Calculator coverage hints: candidate match found | 37/48 (77%) |
| Calculator coverage hints: uncovered | 11/48 (23%) — all 11 are the SOV-7 (7) and SOV-8 (4) objectives |

### Validation

`ecsf-guidance.json` validates against the new `ecsf-guidance.schema.json`;
`ecsf-calculator.json` validates against the new
`ecsf-calculator.schema.json`, with all `ecsf_factor_hints` candidate ids
resolving against `ecsf.json` and all 48 ids unique. The leak check and
placeholder-count check were both manually verified to fail correctly
when a leak/mismatch was deliberately injected, then confirmed clean
after restoring the generated files. Validator run locally throughout
with `data/local/{c3a,ecsf,ecsf-guidance,ecsf-calculator}-verbatim.json`
present.
