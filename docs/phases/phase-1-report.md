# Phase 1 report — Schema, personas, test harness skeleton

**Branch:** `phase-1-schema`
**CI:** green — [run 28632682535](https://github.com/mattpltn/cloud-sovereignty/actions/runs/28632682535), both jobs (`test-engine`, `validate-python`) passed.

## Scope

Per `CLAUDE.md`'s Phase plan: schemas, all 8 golden personas drafted for
owner approval, invariant test skeleton (I1-I7 stubs), `validate.py`
(schema validation + persona-approval gate), CI workflow,
`docs/METHODOLOGY.md` Phase 0+1 sections, `docs/DECISIONS.md` with first
entries including the TypeScript-engine decision.

## Outputs

| Area | Files |
|---|---|
| Schemas | `schema/lang-string.schema.json`, `control-record.schema.json`, `persona-profile.schema.json`, `disposition-rule.schema.json` |
| Personas | `tests/personas/p1-*.yaml` … `p8-*.yaml` (8 files) |
| Engine skeleton | `engine/types.ts`, `engine/index.ts` |
| Test harness | `tests/helpers/personas.ts` (+ test), `tests/invariants/i1-*.test.ts` … `i7-*.test.ts` |
| Validator | `scripts/validate.py`, `scripts/requirements.txt` |
| CI | `.github/workflows/ci.yml` |
| Docs | `docs/METHODOLOGY.md`, `docs/DECISIONS.md` (D-001 … D-004) |

## Statistics

- **Catalog control records:** 0 (extraction is Phase 2 — nothing to
  report per-derivation-tier yet).
- **Personas:** 8 drafted, 0 approved, 0 `needs_review` (persona schema
  has no `needs_review` field — that's a control-record concept; two
  personas carry inline-commented editorial modeling choices instead,
  logged in D-003).
- **DECISIONS.md entries:** 4 (D-001 TS-only engine, D-002 sources held
  back, D-003 persona modifier interpretation, D-004 vitest version pin).
- **Invariant stubs:** 7/7 (I1-I7), all `it.todo`, 0 implemented (expected
  — depends on Phases 3-4).
- **Real (non-stub) tests passing:** 2 (`personas.test.ts`).
- **npm audit:** 0 vulnerabilities.

## Open items for the project owner

1. **Persona approval** — all 8 personas need review/amendment and
   `status: approved` + `approved_by` + `approved_date`. Claude Code will
   not set these itself (persona ownership workflow).
2. **D-002 (license)** — BSI/counsel confirmation on how far verbatim C3A
   reproduction/generalization may go in the public repo is still open;
   current default is pointer-only, sources held back locally.
3. **D-003 (persona modeling)** — review the `key_custody`
   interpretation for A1 self-hosted personas (P1, P8-restricted-tier) and
   the `provider_jurisdiction`/`extraterritorial_law_exposure` split for
   the A5 persona (P7). May prompt a schema addition in Phase 2+ if you
   want the distinction modeled more explicitly.
4. **Minor housekeeping (non-blocking):** CI logs an informational
   deprecation annotation about `actions/checkout@v4`/`actions/setup-node@v4`
   being forced onto a newer Node.js runtime by GitHub's infrastructure.
   Not a failure, no action required now; worth bumping action versions
   in a future housekeeping pass.

## CI status

Confirmed green on the actual pushed branch (not just local), via
`gh run watch` — both jobs completed successfully.

---

Per phase-gate discipline (working rule 6), Phase 1 stops here. Phase 2
(extraction) does not start in this session.
