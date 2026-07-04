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

## D-017 — `cada-act.json` records do not conform to `control-record.schema.json`

**Note (renumbering, CR-2 sequencing):** originally logged as D-012 on
the `phase-2c-cada` branch, allocated independently and in parallel with
`phase-2b-ecsf`'s own D-012..D-016. Per the reviewer's CR-2 and the new
CLAUDE.md working rule ("DECISIONS numbers on parallel phase branches
are provisional; the later-merging branch renumbers at rebase"),
renumbered to D-017 at rebase onto the post-2b-merge `main`, since 2b
merged first and already holds D-012..D-016. No content below this note
was changed — see the phase-2c-cada rebase/renumbering commit for the
full old->new mapping.

**Date:** 2026-07-03
**Decision:** Phase 2c's Act-derived extracts (`data/extracted/cada-act.json`
— a hand-picked subset of CADA proposal articles: definitions, the
Article 29 risk-assessment obligation, the Article 18/19 third-country
mechanism, the Article 30 procurement obligation, and the Article 41
open-source-first preference) use a small ad-hoc record shape, checked
structurally by `scripts/validate.py`'s `check_cada_act()`, rather than
validating against `control-record.schema.json` and rather than
introducing a new JSON Schema file.
**Alternatives considered:** (a) force these records into
`control-record.schema.json` by picking a plausible `sov_domain`/`layer`/
`disposition_default` for each — rejected: that schema models a
provider-facing criterion assessed via one of assess/auto_answer/
inherit/suppress, but most of what this file captures is either a plain
definition (no disposition makes sense) or an obligation on the
**assessing government itself** (conduct a risk assessment; procure only
recognised UA levels; prefer open source) — not a cloud provider's
posture, so the schema's central concept doesn't fit; (b) introduce a
new schema (`cada-act.schema.json`) for this shape — rejected because
this phase's instructions authorized exactly one new schema for Annex
III (`cada-evidence.schema.json`) and none for the Act extracts; adding
one anyway would exceed that authorization for a 13-record file where a
plain structural check is sufficient.
**Rationale:** Keeps the distinction CLAUDE.md's scenario model already
draws — between controls that assess a *provider's* posture (what
`control-record.schema.json` is for) and obligations that fall on the
*government* running the assessment — visible in the data shape itself,
rather than papering over it by stretching a provider-criterion schema
onto government-obligation content.
**Framework anchor:** N/A — internal data-modeling decision, not
dictated by C3A/ECSF/CADA.
**Status:** Resolved.

## D-018 — CADA Annex II 2.1(d) verbatim typo ("presonnel") restored (correction, CR-1)

**Date:** 2026-07-04
**Decision:** `data/local/cada-verbatim.json`'s entry for
`csat-sov4-cada-ua2-d` (Annex II, Union assurance level 2, paragraph
2.1(d), personnel screening/citizenship criterion) originally
transcribed "...the audited provider should ensure that **personnel**
meeting those requirements are available," silently correcting a typo
present in the source PDF, which actually reads "...ensure that
**presonnel** meeting those requirements are available" (COM(2026) 502
final, 3.6.2026). The external Phase 2c review's CR-1 fidelity check
caught this deviation from strict verbatim transcription. The verbatim
entry is corrected to read "presonnel," exactly as printed, and the
corresponding public record (`csat-sov4-cada-ua2-d` in
`data/extracted/cada.json`) is flagged `needs_review: true` with the
note "source typo 'presonnel' preserved verbatim per project convention
— erratum candidate."
**Alternatives considered:** leave the silent correction in place, on
the reasoning that "presonnel" is obviously a typo for "personnel" and
faithful transcription of an obvious typo serves no purpose — rejected:
per the METHODOLOGY.md extraction-conventions rule (working rule 2),
only terminal punctuation and PDF line-break hyphenation artifacts are
normalized; every other character, including source typos, is preserved
and flagged rather than silently corrected, precisely so this class of
transcription drift is always caught and logged rather than invisibly
"fixed" during extraction.
**Rationale:** Restores strict verbatim discipline for this record and
catalogues the typo as a confirmed source erratum, alongside BSI
SOV-4-02-C2 (Phase 2a, D-008) and the Article 18/19 cross-reference
discrepancy (Phase 2c) — all three are candidates for submission via
the respective source organizations' feedback/erratum mechanisms, per
the external reviewer's recommendation.
**Framework anchor:** COM(2026) 502 final, 3.6.2026, Annex II, 2.1(d).
**Status:** Resolved (verbatim corrected); the underlying source typo
itself remains open pending any official erratum from the European
Commission.

## D-019 — Generalization rule table (R1-R9), placeholder registry, and generalization_class schema fields

**Note (renumbering, parallel-branch collision):** originally logged as
D-017 on the `phase-2d-generalization` branch, allocated independently
and in parallel with `phase-2c-cada`'s own D-017/D-018 (both branches
were unmerged siblings of `main` at the time). Per the working rule
"DECISIONS numbers on parallel phase branches are provisional; the
later-merging branch renumbers at rebase," `phase-2c-cada` merged to
`main` first (bringing D-017/D-018), so `phase-2d-generalization`'s
entries are renumbered here to D-019/D-020. No content below this note
was changed.

**Date:** 2026-07-04
**Decision:** Phase 2d-i introduces the project's generalization
infrastructure, the central editorial artifact of this phase (this is
the single consolidated entry the project owner reviews in place of a
per-rule log):
- **`data/rules/placeholders.yaml`** — the permanent placeholder
  registry: `{NATION}`, `{TRUSTED_REGION}`, `{NATION_CYBERSECURITY_AUTHORITY}`,
  `{NATION_ADMINISTRATION}`, `{GOVERNMENT_CUSTOMER}`, `{PROVIDER}`. These
  remain in the public catalog permanently — the client-side app
  resolves them per-assessment from the government's own profile
  (CLAUDE.md, "Jurisdiction parameterization"); no placeholder may be
  added without its own DECISIONS entry.
- **`data/rules/generalization-rules.yaml`** — nine substitution rules
  (R1-R9), each with a machine-readable `pattern`/`replacement` (Python
  `re.sub`, applied in list order — order is load-bearing: more specific
  patterns, e.g. R3's "EU member state" and R5's "non-EU" forms, must
  fire before R2's blanket "EU"->{TRUSTED_REGION} substitution or that
  blanket rule would pre-empt them, since "EU" sits at a regex word
  boundary even inside "non-EU"). R4 and R9 are documentation-only
  entries (no pattern): R4's two-level constructs (e.g. "EU citizens
  with Germany as main residency") fall out automatically from R1/R2
  substituting independently per-token, and R9's "responsible authority
  is the one in the country where the data center is located" sentence
  is already region-agnostic and needs no substitution. R6/R7/R8 seed
  the table for Phase 2d-ii (ECSF/CADA) but fire zero times on
  `c3a.json` (verified — no "public sector body"/"Union entities", named
  EU regulation citations, or EU-institutional-only mechanisms appear in
  C3A's 59 criteria).
- **`scripts/generalize.py`** — `generalize(text, rules)` is a pure
  function (ordered regex substitutions, no external state), making the
  engine deterministic and idempotent by construction: re-running it
  over already-generalized records reproduces the same output.
  Per-record overrides (currently one: `csat-sov4-02-c2`, the D-008
  erratum) live in the rules file's own `overrides` section, checked by
  id before the regex pipeline — this keeps the override
  "part of the rules" rather than a code-level special case, so the
  overridden record still validates as `generalization_class: direct`
  (the override IS what `generalize(verbatim, rules)` returns for that
  id; there is no equality-check divergence to reconcile).
- **Schema:** two new optional fields on `control-record.schema.json` —
  `generalization_class` (enum `direct`/`structural_adaptation`/
  `eu_institutional`) and `generalization_note` (lang-string, required
  by a new `if`/`then` when `generalization_class` is
  `structural_adaptation`). No other schema changes, per this phase's
  explicit scope.
- **Validator:** `scripts/validate.py` gained an equality check
  (`generalized_text.en == generalize(verbatim.en, rules)` for every
  `generalization_class: direct` record, when local verbatim files are
  present) and a residual-literal lint (no `generalized_text` may
  contain "Germany"/"German"/"EU"/"European Union"/"the Union"/"Member
  State(s)" outside an R7 `"(source cites: ...)"` exemption zone).
- **Existing `check_verbatim_leak()` adjusted:** `generalized_text` is
  now excluded from that check's scan. This is not a weakening of the
  D-009/D-010 leak protection — it is a necessary consequence of
  generalization being light-touch placeholder substitution rather than
  paraphrase (large verbatim spans legitimately persist in
  `generalized_text` by design; CLAUDE.md's License care section already
  establishes `generalized_text` as the intended *public*, non-isolated
  artifact, unlike `source_text`). `source_text` and every other field
  remain fully covered by the leak check, verified by deliberately
  injecting a leak into `needs_review_note` and confirming the check
  still fails correctly.
**Alternatives considered:** (a) a single monolithic "translate EU ->
TRUSTED_REGION" find-and-replace with no rule table — rejected: several
constructions (non-EU forms, EU-member-state-as-actor, named
instruments, EU-institutional-only mechanisms) need different treatment
than a blanket substitution, and an auditable table is what CLAUDE.md's
transparency principle requires; (b) hardcode the D-008 erratum
override in `scripts/generalize.py` Python code — rejected per this
phase's explicit instruction ("implement as a documented per-record
override in the rules file, not code"), so the override stays data,
reviewable by the project owner alongside the rest of the rule table,
not buried in script logic.
**Rationale:** A machine-readable, ordered, documented rule table is
citable per-rule (id, pattern, rationale, examples) exactly as
CLAUDE.md's transparency principle requires for every disposition rule
and scoring formula — generalization rules are no different. Keeping
`generalize()` a pure function of (text, rules) is what makes the
validator's equality check meaningful: it proves every `direct` record's
`generalized_text` is fully re-derivable from `source_text` plus the
rule table, not hand-edited out of sync.
**Framework anchor:** N/A — internal tooling/data-shape decision. The
underlying placeholder concept (`{NATION}`/`{TRUSTED_REGION}`) is
CLAUDE.md's own design principle 2, not framework-derived.
**Status:** Resolved.

## D-020 — Public `generalized_text` for C3A remains subject to D-002's pending BSI/counsel posture

**Note (renumbering, parallel-branch collision):** originally logged as
D-018 on the `phase-2d-generalization` branch; renumbered to D-020 for
the same reason as D-019 above (see that entry's renumbering note).

**Date:** 2026-07-04
**Decision:** Phase 2d-i populates `generalized_text` for all 59
`c3a.json` records with real text (light-touch placeholder substitution
of the verbatim source), replacing the `"GENERALIZATION-PENDING"`
placeholder used since Phase 2a/D-010. This text is committed to the
public, git-tracked `data/extracted/c3a.json`. Per CLAUDE.md's License
care section, `generalized_text` (unlike `source_text`) is the artifact
this project's design already designates as the intended *public*
output — but D-002 (BSI/counsel confirmation of permissible verbatim
reproduction *and generalization*) remains open. This entry records
that populating `generalized_text` now, ahead of D-002's resolution, is
a deliberate continuation of the project's existing cautious-default
posture, not a new determination that generalization is confirmed safe.
**Alternatives considered:** wait for D-002 to resolve before
populating any public `generalized_text` — rejected: D-005 already
established that extraction work proceeds ahead of D-002's resolution
(with source_text isolated per D-009/D-010), and CLAUDE.md's own charter
identifies `generalized_text` as the intended public-safe artifact
specifically because placeholder substitution is a real transformation
of the source (unlike verbatim `source_text`); waiting would block the
entire generalization phase pending a legal determination the project
has, from Phase 1 onward, structured its whole publication model
around already resolving in `generalized_text`'s favor.
**Rationale:** Keeps the open question visible rather than letting the
act of populating real `generalized_text` be read as an implicit "this
is settled" signal. D-002's status line is unchanged by this entry.
**Framework anchor:** C3A v1.0 license terms (CC-BY-ND 4.0), same
open question as D-002/D-005/D-009/D-010.
**Status:** Open — tracks D-002; not a new license determination.

## D-021 — R5d amended to match plural "third countries" (Phase 2d-ii, ecsf.json)

**Date:** 2026-07-04
**Decision:** `data/rules/generalization-rules.yaml`'s R5d rule
originally matched only the singular "third country"/"third-country"
(pattern `\bthird[- ]country\b`), sufficient for every occurrence in
`c3a.json` (none) and `cada.json` (singular only, throughout). Applying
the unchanged rule table to `ecsf.json` (Phase 2d-ii) surfaced two
records using the plural "third countries"
(`csat-sov2-ecsf-05`, `csat-sov3-ecsf-03`), which the original pattern
did not match, leaving the literal untouched in `generalized_text`. R5d
is amended to `\bthird[- ]countr(?:y|ies)\b`, matching both forms.
**Alternatives considered:** (a) leave R5d singular-only and add a
separate R5e rule for the plural — rejected as an unnecessary
duplicate rule for what is the same construction; a single regex
alternation is simpler and equally auditable; (b) tag the two affected
`ecsf.json` records `needs_review` instead of amending the rule —
rejected: this is a straightforward, unambiguous grammatical-number
gap in a mechanical pattern, not a genuine interpretive ambiguity, so
fixing the rule (and re-verifying zero residual-literal-adjacent gaps
across all three already-generalized files) is more honest than
flagging it as an open question.
**Rationale:** Keeps the rule table's coverage complete across all
three frameworks rather than leaving a known, mechanical gap; the fix
was verified not to change any of the 59 already-generalized
`c3a.json` records (no plural "third countries" appears there), so no
re-generalization of Phase 2d-i's output was needed.
**Framework anchor:** N/A — internal rule-table maintenance, surfaced
by ECSF's text, not dictated by any framework requirement.
**Status:** Resolved.

## D-022 — New rule R2b: narrow bare-"Union" generalization (Phase 2d-ii, cada.json)

**Date:** 2026-07-04
**Decision:** CADA frequently uses bare "Union" (no preceding "the" or
"European") as an adjective: "Union citizens," "Union citizenship,"
"Where no Union or national cybersecurity certification schemes
exist," "national laws of Member States or Union law." R2's existing
pattern only matches "the Union"/"European Union," so these were left
ungeneralized. A new rule, R2b, adds a narrow lookahead-restricted
pattern
(`\bUnion(?=\s+citizens?\b|\s+citizenship\b|\s+or national\b|\s+law\b)`
-> `{TRUSTED_REGION}`) matching only these confirmed constructions.
**Alternatives considered:** (a) a blanket `\bUnion\b` ->
`{TRUSTED_REGION}` rule — rejected: this would also rewrite CADA's own
proper term "Union assurance level" (its UA-1..4 certification scheme
name — a defined term of art, not a jurisdictional reference, and
correctly left untouched, exactly as ECSF's "SEAL" is never
generalized) and would double-fire against R6's "Union entities" ->
`{GOVERNMENT_CUSTOMER}` mapping; (b) tag the affected records
`needs_review` instead of extending the rule table — rejected for the
same reason as D-021: this is an unambiguous mechanical coverage gap
(a missing sentence construction), not an interpretive judgment call.
**Rationale:** Keeps generalization coverage complete for CADA without
touching the framework's own defined terminology or overlapping with
an existing rule (R6); the narrow lookahead is deliberately
conservative — it fires on 6 confirmed occurrences across
`cada.json`'s 40 records and nowhere else, verified by re-running the
full validator (0 regressions on `c3a.json`/`ecsf.json`, both of which
use "EU citizens" rather than "Union citizens" and never trigger this
pattern).
**Framework anchor:** N/A — internal rule-table maintenance, surfaced
by CADA's text, not dictated by any framework requirement.
**Status:** Resolved.

## D-023 — R2 amended to match bare "Europe" (Phase 2d-ii, ecsf-guidance.json); schema fields for generalized dsr cells and ecsf-scoring domains

**Date:** 2026-07-04
**Decision:** Two related additions while generalizing the ECSF guidance
and scoring files:
1. R2's pattern originally matched "European" (adjective) but not bare
   "Europe" (place-name noun). Applying the rule table to
   `ecsf-guidance.json`'s domain SEAL-2/3/4 cells surfaced one instance
   ("Availability of expertise in Europe, including subcontractors,"
   SOV-4 SEAL-3) that the original pattern left ungeneralized. R2 is
   amended to also match bare "Europe" (ordered after "European" in the
   alternation so "European" is still matched whole, not truncated to
   "Europe" + dangling "an").
2. Schema additions (authorized for these two files only, per this
   phase's explicit instruction): `ecsf-guidance.schema.json`'s
   `domainSealRequirement` gains three optional fields,
   `generalized_seal_2`/`generalized_seal_3`/`generalized_seal_4`
   (lang-string), plus `generalization_note` (lang-string, populated
   only where a cell's generalized text diverges from a mechanical rule
   application — currently just the SOV-7 SEAL-3 "ELA 3." -> "EAL 3."
   erratum correction). These sit *alongside* the existing verbatim
   `seal_2`/`seal_3`/`seal_4` fields (still isolated per D-009/D-010),
   mirroring the `source_text`/`generalized_text` split
   `control-record.schema.json` already uses, rather than replacing the
   verbatim fields in place.
3. `scripts/validate.py`'s leak-check field-exclusion (previously
   hardcoded to skip only the literal key `"generalized_text"`) is
   generalized to skip any key matching `generalized_*` or
   `generalization_note`, at any nesting depth — needed because
   `ecsf-guidance.json`'s new fields sit inside a nested
   `domain_seal_requirements` array, not at a record's top level like
   `control-record.schema.json`'s `generalized_text`.
**Alternatives considered:** (a) leave "Europe" unmatched since it's not
one of the residual-literal lint's banned tokens (the lint only checks
"Germany"/"German"/"EU"/"European Union"/"the Union"/"Member State(s)",
not bare "Europe") — rejected: passing the lint isn't the same as being
correctly generalized, and leaving a known, findable gap uncorrected
once discovered would be inconsistent with D-021/D-022's own reasoning;
(b) replace `seal_2`/`seal_3`/`seal_4` in place with generalized text
(as done for `cada-evidence.json`, which has no schema authorization for
new fields) — rejected here specifically because this phase's
instruction *does* authorize new fields on `ecsf-guidance.schema.json`,
so the source_text/generalized_text-style split (preferred throughout
the rest of the project) is used instead of the in-place fallback.
**Rationale:** Keeps ECSF guidance's verbatim/generalized distinction
structurally explicit (matching every other framework's pattern) rather
than collapsing it, now that a schema change is authorized; fixes a
real, if narrow, rule-table gap found in the process.
**Framework anchor:** N/A — internal rule-table/schema maintenance,
surfaced by the ECSF Implementation Guidance's text, not dictated by any
framework requirement.
**Status:** Resolved.

## D-024 — generalization_class semantics codified (CR-1, Phase 2d review)

**Date:** 2026-07-04
**Decision:** Phase 2d-i/2d-ii kept every per-record override (the D-008
C3A erratum, the CADA 2.1(d) typo correction, the R7 named-instrument
reframings, and every other hand-written override in
`data/rules/generalization-rules.yaml`'s `overrides` table) classified
`generalization_class: "direct"`, rather than introducing a distinct
class for "overridden." This was an implementation choice made without
its own DECISIONS entry at the time; the external Phase 2d review
(`reviews/phase-2d-review.md`, CR-1) endorsed the choice — it means the
validator's equality check (`scripts/validate.py`,
`check_generalization()`) covers 128 of 129 control records rather than
only the mechanically-substituted subset — but required the semantics
be registered explicitly rather than left implicit. This entry is that
registration:
- **`direct`** means `generalized_text` is machine-reproducible as
  `f(verbatim, rules)`, where `rules` includes both the ordered R1-R9
  substitution pipeline *and* the `overrides` table's per-record
  entries (checked by id before the pipeline runs). A record being
  `direct` does **not** imply no human judgment was involved — it means
  whatever judgment was applied is captured as *data* (an entry in the
  public `overrides` table), not as an undocumented one-off edit, and
  is therefore still subject to the equality check every time the
  validator runs.
- **`structural_adaptation`** means the divergence from a mechanical
  substitution is not expressible as replacement text at all — it is a
  narrative functional restatement of a mechanism with no
  `{NATION}`/`{TRUSTED_REGION}`-level analog (rule R8; currently one
  record, `csat-sov1-cada-ua3-g`). These records are exempt from the
  equality check (there is no `f(verbatim, rules)` to compare against
  in the same sense) but the schema requires a `generalization_note` on
  every one.
- **The complete enumeration of every point of human judgment in
  generalization**, for any reader auditing this project, is: the
  public `overrides` table in `data/rules/generalization-rules.yaml`
  **union** every record where `generalization_class != "direct"` (i.e.
  `"structural_adaptation"` or `"eu_institutional"`). Nothing else in
  the generalization pipeline involves judgment — every other record's
  `generalized_text` is reproducible from `source_text`/verbatim plus
  the ordered rule list alone.
**Alternatives considered:** (a) introduce a fourth
`generalization_class` value (e.g. `"overridden"`) distinct from
`"direct"`, reserved for override-table entries — rejected per the
reviewer's own recommendation: it would *shrink* equality-check
coverage (overridden records would become exempt, like
`structural_adaptation`) for no verification benefit, since the
override text is already fully data-driven and checkable; (b) leave the
semantics implicit, relying on code-reading to discover them — rejected
per this CR: a project built on the transparency principle (CLAUDE.md,
Transparency & provenance) needs this class distinction registered
somewhere a reader can find without reading `scripts/generalize.py`.
**Rationale:** Registers, rather than silently accepts, a deviation
between what the Phase 2d-i/2d-ii task instructions originally
specified (an implicit assumption that overrides would need their own
class) and what was actually built and is being kept (overrides stay
`direct`) — per the reviewer's endorsement that the built behavior is
strictly stronger for verification purposes.
**Framework anchor:** N/A — internal data-modeling/verification-design
decision, not dictated by any source framework.
**Status:** Resolved.
