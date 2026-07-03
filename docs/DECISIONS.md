# Decision Register

Append-only. Every `editorial`-derivation record or rule, and every
project judgment call not fully dictated by a source framework, gets an
entry here — this is the standing answer to any bias critique (CLAUDE.md,
Transparency & provenance, item 4). **Never edit an existing entry.**
Corrections are new entries that reference the old ID.

Format: ID, date, decision, alternatives considered, rationale, framework
anchor (where partial).

---

## D-001 — Engine implemented in TypeScript only

**Date:** 2026-07-02
**Decision:** The CSAT engine (`/engine`) is written in TypeScript. The
same build passes the golden-persona test suites in CI (via a Node test
runner) and runs unmodified in the browser. Python is used exclusively for
extraction tooling and data/schema validation (`scripts/validate.py`) —
never for engine logic.
**Alternatives considered:** Python engine with a separate JS/TS port for
the browser; Python engine compiled to WASM (e.g. via Pyodide).
**Rationale:** The client-side-only architecture (design principle:
"Client-side only — no backend, ever") requires the engine to run in a
browser. Maintaining two engine implementations (Python for
tooling/tests, TS/JS for the browser) risks silent behavioral drift
between what's tested and what's shipped. A single TypeScript
implementation removes that risk entirely; Pyodide/WASM was rejected as
unnecessary complexity for a project of this size.
**Framework anchor:** N/A — pure engineering/architecture decision, not
derived from C3A/ECSF/CADA.

---

## D-002 — Source framework PDFs held back from the public repository

**Date:** 2026-07-02
**Decision:** The `/sources` PDFs (C3A, ECSF, ECSF implementation
guidance, CADA proposal + annex) are kept on the maintainer's local
machine and used for extraction, but are **not committed** to the public
repository (`sources/` is gitignored). Public catalog records carry
`source_refs` (framework + exact section/criterion ID) and
`generalized_text`; verbatim `source_text` is only included in a catalog
record where the applicable license has been separately confirmed to
permit it, otherwise records carry `source_pointer` (document name +
section) referencing the official PDF held externally.
**Alternatives considered:** (a) commit all source PDFs to the public repo
outright; (b) commit only ECSF/CADA (EU Commission reuse policy is
permissive) and hold back only C3A.
**Rationale:** C3A v1.0 is licensed CC-BY-ND 4.0 — "No Derivatives."
Redistributing the verbatim PDF, and potentially even verbatim extracted
passages, in a public repository is not clearly permitted without
confirming scope with BSI/counsel first (CLAUDE.md, Transparency &
provenance, item 7: "License care"). The cautious default — pointer-only
by default, verbatim only where confirmed — was chosen over committing
outright to avoid an unrecoverable public-distribution mistake; it can be
loosened later once the license question is resolved, but not reversed
if reproduction turns out to be non-permitted.
**Framework anchor:** C3A v1.0 license terms (CC-BY-ND 4.0).
**Status:** Open — BSI/counsel confirmation on scope of permissible
verbatim reproduction and generalization is still outstanding. This entry
records the interim cautious default, not a final resolution.

---

## D-003 — Persona modifier interpretation for self-operated (A1) and licensed-partner (A5) scenarios

**Date:** 2026-07-02
**Decision:** In the golden persona fixtures (`tests/personas/*.yaml`),
two modifier fields are given interpretations not explicitly specified by
the two-axis scenario model in CLAUDE.md, because the model's
`key_custody` and `provider_jurisdiction` concepts presuppose a
third-party provider distinct from the government:
- **A1 (fully self-hosted) personas** (P1 `gov-dc-oss-inhouse`, and the
  restricted tier of P8 `mixed-tier-estate`): `key_custody` is set to
  `external_hsm` to represent government-operated dedicated key-management
  hardware, since `provider_held`/`hyok` don't map cleanly when there is no
  third party. See inline comment in each affected YAML file.
- **A5 (partner-operated sovereign region) persona** (P7
  `sovereign-region-partner`): `provider_jurisdiction` is set to `{NATION}`
  (the domestic licensed operating entity), with the dependency on the
  foreign parent hyperscaler's technology/support chain captured instead
  via `extraterritorial_law_exposure: true`, rather than by changing
  `provider_jurisdiction` itself.
**Alternatives considered:** Adding a new `key_custody` enum value (e.g.
`self_managed`) to `persona-profile.schema.json` distinct from
`external_hsm`; adding a separate `underlying_technology_jurisdiction`
modifier field to capture the A5 nuance explicitly instead of overloading
`extraterritorial_law_exposure`.
**Rationale:** Both alternatives would expand the schema before Phase 4's
responsibility-map/disposition engine exists to consume the distinction,
which risks guessing at a shape the engine doesn't actually need
(Simplicity principle — no speculative schema fields). The interim
interpretations are lower-cost and flagged inline for project-owner
review; schema changes remain open if review concludes the engine
genuinely needs a sharper distinction.
**Framework anchor:** N/A — persona design fixtures, not source-framework
derived content. Personas are project-owned test scaffolding per the
persona ownership workflow, not catalog records.
**Status:** Open — pending project-owner review during persona approval.

---

## D-004 — vitest pinned to 4.x rather than 2.x at project start

**Date:** 2026-07-02
**Decision:** `package.json` pins `vitest` to `^4.1.9` rather than the
initially-installed `^2.1.4`.
**Alternatives considered:** Leave at `^2.1.4` and accept the advisory
since it only affects the vite dev server, not `vitest run` in CI.
**Rationale:** `vitest@2.1.4`'s dependency chain (`vite` -> `esbuild`)
carries GHSA-67mh-4wv8-2f99 (esbuild dev-server CORS, moderate/high/
critical per npm audit's transitive scoring). Not a real exposure for
`vitest run` in a CI job with no exposed dev server, but pinning to the
patched major version costs nothing at project start and removes the
finding entirely (`npm audit` -> 0 vulnerabilities).
**Framework anchor:** N/A — tooling hygiene decision.
