# Methodology

This document is written incrementally: each phase appends the section
describing exactly what was done and how (extraction rules, substitution
rules, disposition logic, scoring math, testing method). A phase does not
merge without its section here. See `CLAUDE.md` for the full project
charter, source frameworks, and phase plan.

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
