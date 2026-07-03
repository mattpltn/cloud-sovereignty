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

---

## D-005 — Phase 2a extraction retains verbatim source_text plus a page-level source_pointer on every record

**Date:** 2026-07-03
**Decision:** Unlike D-002's cautious default for *published catalog*
records (pointer-only unless verbatim reproduction is confirmed
permitted), the raw extraction working data in `/data/extracted/c3a.json`
populates **both** `source_text` (verbatim English, captured directly
from the C3A PDF) **and** `source_pointer` (document, section, page) on
every record. `source_pointer.page` is a new optional field added to
`control-record.schema.json` in this phase.
**Alternatives considered:** (a) pointer-only, matching D-002's
catalog-record default exactly; (b) verbatim text with no page number
(document + section only, as originally specified in Phase 1).
**Rationale:** This is explicit, logged project-owner direction for the
extraction working stage specifically, not a reversal of D-002: source
text is needed verbatim now to perform accurate Phase 2d generalization
later, and a page number makes every record locatable even if
`source_text` is stripped before the data is published (D-002's question
about public redistribution remains open and unresolved by this entry).
The practical effect: `/data/extracted/c3a.json` currently contains
verbatim CC-BY-ND-licensed text and should NOT be treated as
publication-ready without first resolving D-002.
**Framework anchor:** C3A v1.0 license terms (CC-BY-ND 4.0) — same open
question as D-002.
**Status:** Open, same as D-002.

---

## D-006 — No machine translation of framework-derived text; fr fields carry a literal placeholder

**Date:** 2026-07-03
**Decision:** In Phase 2a extraction records, the `fr` key of every
lang-string field (`source_text`, `generalized_text`) is not
machine-translated. It carries the literal placeholder string
`"FR-TRANSLATION-PENDING"` until a professional/reviewed French
translation exists.
**Alternatives considered:** Machine-translate the English C3A text into
French now, to satisfy the schema's requirement that every lang-string
field carry both `en` and `fr`.
**Rationale:** A machine translation of framework-derived criterion text
would itself constitute a derivative work of C3A's CC-BY-ND-licensed
content — the same "No Derivatives" concern already flagged in D-002,
just applied to translation rather than paraphrase/generalization.
Producing one now, before BSI/counsel confirms scope, risks compounding
an already-open license question. The placeholder satisfies the schema's
structural requirement (both language keys present) without generating
new derivative content.
**Framework anchor:** C3A v1.0 license terms (CC-BY-ND 4.0) — same open
question as D-002/D-005.
**Status:** Open — blocks on the same BSI/counsel confirmation as D-002,
plus a decision on who produces the eventual French translation
(professional translator vs. reviewed machine translation once license
scope is clear).

---

## D-007 — Supply-chain layer split (CR-2)

**Date:** 2026-07-03
**Decision:** `schema/control-record.schema.json`'s and
`schema/disposition-rule.schema.json`'s `layer` enum value
`hardware_supply_chain` is replaced with three values:
`supply_chain_hardware`, `supply_chain_software`, `supply_chain_services`.
The 7 affected `c3a.json` records (SOV-5-01 through SOV-5-04) are retagged
by subject matter: SOV-5-01 (SBOM/software suppliers) ->
`supply_chain_software`; SOV-5-02 (hardware inventory) ->
`supply_chain_hardware`; SOV-5-03 (external cloud-service dependencies)
-> `supply_chain_services`; SOV-5-04 (export restrictions, which
verbatim-spans software, hardware, and services at once) ->
`supply_chain_hardware` as primary, `needs_review: true` retained with an
updated note (export-control regimes are most classically applied to
physical hardware/technology export, but the criterion explicitly covers
all three).
**Alternatives considered:** (a) leave the single `hardware_supply_chain`
catch-all in place, as flagged for future review in the Phase 2a report;
(b) a four-way split adding a generic `supply_chain` value for
criteria that genuinely span multiple supply-chain types, instead of
forcing a primary-tag choice on SOV-5-04.
**Rationale:** This is CR-2 from the Phase 2a review. The single
`hardware_supply_chain` catch-all was already flagged as an open item in
`docs/phases/phase-2a-report.md` (7 of the original 15 needs_review flags
traced to it). Splitting resolves 4 of those 7 flags outright (SOV-5-01,
SOV-5-02, SOV-5-03 pairs now have an exact-fit layer) and leaves one
(SOV-5-04) genuinely multi-layer regardless of taxonomy granularity — a
generic fourth `supply_chain` value was rejected because it would let
every ambiguous case default to it rather than forcing an explicit
per-record judgment, defeating the purpose of the split.
**Framework anchor:** N/A — layer taxonomy is an editorial/architectural
construct (the responsibility-map layer model), not sourced from C3A/
ECSF/CADA directly.

---

## D-008 — SOV-4-02-C2 erratum confirmed against the published PDF, record left verbatim (CR-2)

**Date:** 2026-07-03
**Decision:** The reviewer verified `SOV-4-02-C2` against the published
C3A v1.0 PDF (page 11) directly. The criterion genuinely reads "within the
EU" in its first sentence and "outside Germany" in its second, exactly as
captured in `data/extracted/c3a.json` — this is not a transcription error
introduced during extraction. `csat-sov4-02-c2`'s `source_text` is left
unmodified. The likely-intended meaning ("within Germany" in the first
sentence, to match the C2/Germany-variant pattern used elsewhere in the
document) will be captured via a `generalization_note` referencing this
entry when Phase 2d performs placeholder substitution, not by editing the
verbatim record now.
**Alternatives considered:** (a) "correct" the verbatim text to what was
presumably intended; (b) drop the `needs_review` flag now that the text is
confirmed accurate-to-source (i.e., not an extraction error).
**Rationale:** Working rule 4 ("Verbatim first, transform second") and
working rule 2 ("never guess") both argue against silently correcting
apparent source-document errors — that is itself an editorial judgment
about BSI's intent, not extraction. The `needs_review` flag stays set:
confirming the text is accurately transcribed does not resolve the
underlying ambiguity about what the criterion should be understood to
require, which is exactly what Phase 2d's `generalization_note` exists to
carry forward transparently.
**Framework anchor:** C3A v1.0, SOV-4-02-C2, p. 11.

---

## D-009 — Verbatim C3A text moved out of the public git-tracked artifact (CR-2)

**Date:** 2026-07-03
**Decision:** `data/extracted/c3a.json` (public, git-tracked) no longer
contains real verbatim text: every record's `source_text.en` and
`source_text.fr` are replaced with the literal placeholder
`"SEE-LOCAL-VERBATIM"`. The real verbatim text moved to
`data/local/c3a-verbatim.json`, keyed by record `id`, which is
git-ignored (`data/local/` added to `.gitignore`). `scripts/validate.py`
now cross-checks, when `data/local/c3a-verbatim.json` is present, that
every public record has a matching local verbatim entry and vice versa;
when the directory is absent (always true in CI), the check is skipped
with a printed notice instead of failing.
**Alternatives considered:** (a) leave `source_text` verbatim in the
public file per D-005's original working-stage exception; (b) remove the
`source_text` field entirely rather than placeholder it (rejected: would
require a schema change beyond this decision's scope, and the
`if`/`then` constraint added in Phase 1 already requires either
`source_text` or `source_pointer` — an empty/placeholder string is
simpler and keeps every record's shape uniform).
**Rationale:** D-005 authorized verbatim text in the working extraction
data specifically so Phase 2d generalization would have accurate source
material; it did not resolve whether that verbatim text should sit in
the *public, git-tracked* repository in the meantime. On reflection this
is exactly the license exposure D-002 was cautious about — C3A is
CC-BY-ND 4.0, and a public GitHub repo is publication the moment it's
pushed. This decision closes that specific gap: the full provenance
chain (verbatim text, page numbers, section IDs) is retained and
restorable locally, but the git-tracked artifact no longer reproduces
CC-BY-ND text pending BSI/counsel confirmation.
**Scope note (known residual gap):** `generalized_text` was NOT scrubbed
by this decision — at this stage `generalized_text.en` is still set equal
to the original verbatim English (Phase 2d generalization hasn't run
yet), so it currently still contains verbatim CC-BY-ND text in the
public file. This was out of the explicit scope given for this fix; see
`docs/phases/phase-2a-report.md` for a flagged follow-up recommendation.
**Framework anchor:** C3A v1.0 license terms (CC-BY-ND 4.0) — same open
question as D-002/D-005.
**Status:** Open, same as D-002/D-005. Additionally: verbatim C3A text
already exists in this repository's git history (the original Phase 2a
extraction commits, before this fix). This decision does not rewrite
that history — see the phase report for the owner's decision on whether
history rewriting is warranted.

---

## D-010 — Verbatim scrub extended to `generalized_text`; validator leak check added (CR-3, correction to D-009)

**Date:** 2026-07-03
**Decision:** External review (`reviews/phase-2a-review-addendum-2.md`,
CR-3) found that D-009 scrubbed `source_text` but left `generalized_text`
equal to the full verbatim English for all 59 public records, since at
this stage in the pipeline `generalized_text` is simply a placeholder
copy of the verbatim source (Phase 2d generalization hasn't run yet).
This made D-009 ineffective as committed: verbatim CC-BY-ND text was
still present in the public, git-tracked `data/extracted/c3a.json` via
a different field. This decision corrects that gap:
1. `data/extracted/c3a.json`'s `generalized_text.en` and `.fr` are now
   the literal placeholder `"GENERALIZATION-PENDING"` for all 59
   records. Phase 2d owns filling this field with real generalized text
   (placeholder substitution per the documented rules), at which point
   the field will legitimately diverge from `source_text` again.
2. `scripts/validate.py` gained `check_verbatim_leak()`: when
   `data/local/c3a-verbatim.json` is present, it scans every text field
   in every public `/data/extracted/*.json` record for any contiguous
   span of more than 15 words that also appears in a local verbatim
   entry, and fails the build if one is found. This is a
   defense-in-depth check — not just a spot-fix of the one field the
   reviewer found — so a future field (or the same field, if Phase 2d
   generalization degenerates into near-verbatim copying) can't
   reintroduce the same leak silently. When `data/local/` is absent
   (always true in CI), the check is skipped with a printed notice,
   consistent with `check_local_verbatim()` (D-009).
**Alternatives considered:** (a) scrub only `generalized_text` and stop
there, matching the reviewer's literal finding — rejected because it
would leave the class of bug (any public field silently holding verbatim
text) undefended, and the next field to leak wouldn't be caught until
another manual review found it; (b) make the leak check exact-match only
(whole-field equality) rather than span-based — rejected because
paraphrased-but-still-substantially-copied text could still infringe and
a >15-word contiguous match is a reasonable, testable proxy for "this is
still verbatim reproduction," per CR-3's own phrasing.
**Verification:** ran the leak check with `data/local/c3a-verbatim.json`
present against the real (fixed) `c3a.json` — passes clean. Also
deliberately injected a verbatim 161-word span into a copy of
`generalized_text` and re-ran the validator to confirm the check fails
loudly on a genuine leak, then restored the real file and re-confirmed a
clean pass, before committing.
**Framework anchor:** C3A v1.0 license terms (CC-BY-ND 4.0) — same open
question as D-002/D-005/D-009. This is a correction entry (append-only
register — D-009 itself is not edited); see D-009 for the original
decision and its Scope note.
**Status:** Open, same as D-002/D-005/D-009 pending BSI/counsel
confirmation on how far verbatim reproduction and generalization may go
in this public repo. Same git-history caveat as D-009 applies (see
D-011 and the phase report for the owner's merge-time handling of this).

---

## D-011 — Squash-merge `phase-2a-c3a-extraction` into `main` (deviation from per-batch history convention)

**Date:** 2026-07-03
**Decision:** Merge `phase-2a-c3a-extraction` into `main` as a single
squashed commit, rather than preserving the branch's individual
per-domain-batch commit history (the convention working rule 5 normally
calls for: one commit per validated batch, e.g.
`phase-2a: extract SOV-4 (12 criteria, validator pass)`). The remote
branch is deleted after the squash-merge.
**Alternatives considered:** (a) merge with full history preserved
(the default convention) — rejected because the pre-D-009 commits on
this branch contain the full verbatim C3A text (CC-BY-ND 4.0), and a
regular merge would carry that history onto `main`, which up to now has
never been exposed to verbatim text; (b) rewrite the branch's history in
place (interactive rebase or `git filter-repo`) to strip verbatim text
from the old commits, then fast-forward merge — rejected as unnecessarily
risky (rewriting already-pushed history) for the same end result a
squash-merge achieves non-destructively; (c) do nothing and merge as-is,
deferring the license question — rejected, since `main` is the
branch most likely to be cloned/mirrored/reviewed externally, and the
squash-merge is a low-cost way to keep it clean while the BSI/counsel
question (D-002/D-005/D-009/D-010) remains open.
**Rationale:** endorsed in `reviews/phase-2a-review-addendum-2.md`
("History exposure — reviewer recommendation"): squash-merge with a
summary commit message, log the deviation as a DECISIONS entry, and
note that the granular per-batch history remains available locally to
the project owner (the local branch/reflog is untouched by this — only
the pushed remote branch is deleted after the squash-merge lands on
`main`). The reviewer also notes unreachable commits may persist
transiently in GitHub's caches/forks and that full purging would need a
GitHub support request — judged disproportionate unless BSI's guidance
comes back negative.
**Verification:** after the squash-merge, `main`'s full git history is
checked to confirm no commit ever introduced `data/local/` content, and
the CR-3 leak check (D-010) is run against `main`'s `c3a.json` to
confirm no verbatim text is present in the squashed commit itself.
**Framework anchor:** N/A — this is a repository/process decision, not a
framework-sourced one. License caution per C3A's CC-BY-ND 4.0 terms
(same open question as D-002/D-005/D-009/D-010).
**Status:** Applied. The granular batch-by-batch commits remain
reachable via `origin`'s branch history until the remote branch is
deleted per this decision; the project owner retains the full history
locally (local branch ref / reflog) independent of the remote deletion.

---

## D-012 — ECSF text license basis, and why the D-009/D-010 verbatim-isolation regime is applied anyway

**Date:** 2026-07-03
**Decision:** The EU Cloud Sovereignty Framework (ECSF) v1.2.1 is a
European Commission (DG DIGIT) procurement document. Per CLAUDE.md's
license-care section, "ECSF and CADA follow EU Commission reuse policy,"
which is materially more permissive than C3A's CC-BY-ND 4.0 — EU
Commission documents are, by default, reusable under the EU's standard
reuse policy (Decision 2011/833/EU), typically equivalent to CC-BY,
unless a document states otherwise. No CC-BY-ND-style "No Derivatives"
restriction applies. On this basis:
- `data/extracted/ecsf-scoring.json` (SEAL levels, domain definitions,
  official weights, scoring formula) carries full verbatim ECSF text
  directly in the public, git-tracked file — no local/public split is
  applied to this artifact, since the license basis does not require it.
- `data/extracted/ecsf.json` (SOV-1..6 contributing factors, extracted as
  control records) **is** put through the same D-009/D-010
  verbatim-isolation regime as C3A anyway (public `source_text`/
  `generalized_text` placeholdered; real text in git-ignored
  `data/local/ecsf-verbatim.json`), per explicit instruction for this
  phase, even though ECSF's license does not strictly require it.
**Alternatives considered:** (a) treat all ECSF artifacts uniformly as
license-permissive and skip the local/public split entirely, including
for `ecsf.json` — rejected for this phase per explicit instruction, to
keep the extraction pipeline's provenance mechanics uniform across
frameworks rather than branching behavior on a license determination
that, while more confident than the open C3A question, has not itself
been separately confirmed by counsel; (b) apply the split to
`ecsf-scoring.json` too, for total consistency — rejected because that
file's content (SEAL scale, domain weights, formula) is short, factual,
and structurally different from prose criteria text, and the explicit
instruction only asked for the split on the contributing-factor control
records.
**Rationale:** This produces an intentional, documented asymmetry within
the same source framework: `ecsf-scoring.json` is verbatim-in-public,
`ecsf.json` is verbatim-isolated-to-local. This is not an oversight — it
is recorded here specifically so the asymmetry is traceable rather than
looking like an inconsistency, per the transparency principle that every
editorial choice must be visible and explained (CLAUDE.md, Transparency
& provenance, item 4).
**Framework anchor:** ECSF v1.2.1; EU Commission document reuse policy
(Decision 2011/833/EU) as generally understood, not yet separately
confirmed by counsel for this specific document.
**Status:** Open (lower urgency than C3A's D-002/D-005/D-009/D-010,
since the reuse policy is inherently more permissive) pending explicit
confirmation of ECSF's specific reuse terms.

## D-013 — ecsf-c3a-hints.json re-encoded as a coverage object (correction, CR-1)

**Date:** 2026-07-03
**Decision:** `data/extracted/ecsf-c3a-hints.json` (Phase 2b) originally
encoded each entry as a bare list of C3A candidate ids, with the literal
string `"uncovered"` used as a magic sentinel value inside that list for
the 7 factors with no plausible C3A match. The external Phase 2b review
(`reviews/phase-2b-review.md`, CR-1) correctly flagged this: a bare list
lets the sentinel sit silently inside what is otherwise an id list, and a
malformed mixed entry (real ids alongside the sentinel) would validate
without error. Each entry is now re-encoded as an object:
`{"coverage": "covered"|"uncovered", "c3a_candidates": [...]}`, with
`c3a_candidates` required non-empty when `coverage` is `"covered"` and
required empty when `"uncovered"`. The existing candidate-id lists
themselves are unchanged — this is a re-encoding of the same mappings,
not a re-assessment of them. `scripts/build_ecsf_c3a_hints.py` was
updated to emit the new shape, and `scripts/validate.py`'s
`check_ecsf_c3a_hints()` was tightened to reject bare lists, reject the
sentinel string anywhere, require `coverage` to be one of the two
allowed values, and enforce the non-empty/empty pairing with `coverage`.
**Alternatives considered:** leave the sentinel in place and just
document the convention more clearly in the docstring — rejected per the
reviewer's point that documentation cannot substitute for a check when
the format itself permits an invalid state.
**Rationale:** This is a correction to the Phase 2b hints design
introduced when `ecsf-c3a-hints.json` was first built (see
`docs/phases/phase-2b-report.md`); as the reviewer noted, the root cause
traces to loose wording in the original Phase 2b task description, not a
data-entry error — logged here for process honesty per the append-only
register rules (correction, not an edit to the original design).
**Framework anchor:** Editorial — internal data-shape decision, no
framework criterion involved.
**Status:** Resolved.

## D-014 — Dual ECSF weight sets stored; CSAT's outcome-derived weighting remains the tool's approach

**Date:** 2026-07-03
**Decision:** The Phase 2b.1 second source, the EU Commission's "Cloud
Sovereignty Framework — Implementation guidance" PDF, contains an
alternative domain weight matrix (SOV-1 20%, SOV-2 10%, SOV-3 10%,
SOV-4 15%, SOV-5 10%, SOV-6 15%, SOV-7 15%, SOV-8 5%; sum 100) that
differs from v1.2.1's own default weights (SOV-1 15%, SOV-5 20%, SOV-7
10%; `data/extracted/ecsf-scoring.json`) in exactly those three domains.
The guidance text itself states contracting authorities may adapt these
values, so no single canonical ECSF weight set exists. Both are now
recorded as named, traceable reference profiles: v1.2.1's weights stay
in `ecsf-scoring.json` as before; the guidance's alternative is stored as
`ecsf_guidance_matrix` in the new `data/extracted/ecsf-guidance.json`.
Neither is treated as authoritative for CSAT's own scoring: per
CLAUDE.md's core design principle 5, CSAT derives domain weights from
each assessment's elicited sovereignty-outcome priorities, not from
either ECSF procurement weight set. Storing both here is for
traceability and Phase 5 reference only (e.g. as a sanity check or an
optional "compare to ECSF procurement weighting" view), not because
CSAT will default to one of them.
**Alternatives considered:** (a) discard the guidance's alternative
weights as a one-off procurement artifact not worth capturing — rejected
because it is officially published Commission guidance and materially
informs Phase 5 design (it also happens to be the weight set the
official calculator XLSX itself actually uses, per Phase 2b.1's own
cross-check); (b) treat the guidance weights as an update superseding
v1.2.1's — rejected, since v1.2.1 remains the primary source framework
per CLAUDE.md and nothing indicates v1.2.1's weights were withdrawn.
**Rationale:** Recording both, explicitly labeled and source-pointed,
keeps the project's stated non-adoption of either procurement weighting
scheme (design principle 5) visible and defensible rather than requiring
a reader to reconcile two documents themselves.
**Framework anchor:** ECSF v1.2.1 §5 (default weights, already in
`ecsf-scoring.json`); Implementation Guidance, "The Sovereign Cloud
Framework Matrix" (page 6-7) for the alternative matrix.
**Status:** Resolved.

## D-015 — SEAL minimum-aggregation rule adopted as a Phase 5 ceiling-semantics anchor

**Date:** 2026-07-03
**Decision:** The Implementation Guidance states a SEAL aggregation rule
absent from v1.2.1 itself: "The overall SEAL level is the lowest SEAL
level achieved in any of the objectives" (page 9), captured verbatim in
`data/extracted/ecsf-guidance.json`'s `seal_aggregation_rule`. This
weakest-link rule is logged now, in Phase 2b.1, as an explicit anchor for
Phase 5's ceiling/ceiling-vs-achieved design: CSAT's own "ceiling" concept
(the maximum attainable score given structural constraints, CLAUDE.md
"Scoring") is conceptually the same weakest-link idea ECSF uses for
SEAL, and Phase 5 should either adopt a minimum-across-domains rule for
an analogous overall-ceiling figure or explicitly document why CSAT
diverges from ECSF's own precedent here.
**Alternatives considered:** wait until Phase 5 to record this — rejected
because the rule was found now (Phase 2b.1) and CLAUDE.md's provenance
discipline (working rule 9) calls for logging judgments/anchors in the
commit where they're identified, not deferring documentation to a later
phase that may not re-derive them from the source.
**Rationale:** Makes the source basis for a likely Phase 5 design choice
traceable back to this phase rather than appearing to be invented in
Phase 5 without a framework anchor.
**Framework anchor:** Implementation Guidance, "Assessment of Sovereignty
Objectives" (page 9).
**Status:** Open — Phase 5 must decide whether/how to adopt; this entry
only establishes the source basis, not the Phase 5 design itself.

## D-016 — Official calculator kept as a separate operationalization layer, not merged into the 30 normative v1.2.1 factors

**Date:** 2026-07-03
**Decision:** The official Cloud III DPS tender calculator XLSX (`Annex -
Sovereignty assessment calculator.xlsx`) breaks the 30 v1.2.1
contributing factors (`data/extracted/ecsf.json`) into 48 finer-grained
"specific objectives," each with multiple-choice answer options carrying
a point value and a SEAL level. These are extracted into a new, separate
file, `data/extracted/ecsf-calculator.json` (schema:
`schema/ecsf-calculator.schema.json`), rather than merged into or
replacing the existing 30 `ecsf.json` factor records. Each calculator
objective carries a provisional, unverified `ecsf_factor_hints` mapping
back to the `ecsf.json` factor(s) it operationalizes (coverage-object
encoding per D-013/CR-1), built by reading the calculator's objective
titles against the Implementation Guidance's own "Criteria" bullets
(near-identical wording to the `ecsf.json` factor text). SOV-7 and SOV-8
objectives have no `ecsf.json` records to map to at all (inheritance-only
/ out of scope, Phase 2b) and are therefore marked `"uncovered"` by
construction, not because no analogue was found.
**Alternatives considered:** (a) treat the 48 specific objectives as
replacing the 30 factors as CSAT's normative catalogue — rejected: the
factors are v1.2.1's own primary-source text (verbatim, CC-BY-ND-style
caution already applied via D-012); the calculator is a downstream
operational artifact from a specific tender, with example scoring values
its own sheet calls fictitious, and conflating the two would blur which
data is the source-of-truth criteria versus a worked implementation
example; (b) silently drop the calculator's malformed/blank answer rows
during extraction — rejected per this phase's explicit instruction and
working rule 2 ("never guess silently"); every blank/malformed row is
captured as-is with `needs_review`.
**Rationale:** Keeps the calculator as what it is — an operationalization
reference for Phases 4-6 question/answer design — without letting a
single tender's implementation choices (e.g. its own fictitious example
scores, or rows that are blank/malformed in the source spreadsheet)
contaminate the catalogue of normative criteria.
**Framework anchor:** `Annex - Sovereignty assessment calculator.xlsx`,
sheet "Sov Assessment Levels (COL)".
**Status:** Resolved.
