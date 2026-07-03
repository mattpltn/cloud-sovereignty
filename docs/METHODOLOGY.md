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
