# Phase 2a report — BSI C3A extraction

**Branch:** `phase-2a-c3a-extraction` (branched from a clean, merged `main`)
**Scope:** Extract all BSI C3A v1.0 criteria and additional criteria into
`/data/extracted/c3a.json` as records conforming to
`schema/control-record.schema.json`. ECSF and CADA are explicitly out of
scope for this phase.

## Outputs

| File | Purpose |
|---|---|
| `scripts/extract_c3a.py` | Verbatim transcription + domain-batched writer, now splits public/local (D-009) |
| `data/extracted/c3a.json` | 59 control records, public, `source_text` scrubbed (D-009) |
| `data/local/c3a-verbatim.json` | 59 verbatim entries, git-ignored, local only (D-009) |
| `schema/control-record.schema.json` | +`source_pointer.page`; `layer` enum split (D-007) |
| `schema/disposition-rule.schema.json` | `layer` enum kept in sync with control-record (D-007) |
| `engine/types.ts` | `Layer` union kept in sync (D-007) |
| `scripts/validate.py` | +validates `/data/extracted/*.json`, +id-uniqueness, +local-verbatim cross-check (D-009) |
| `docs/DECISIONS.md` | +D-005..D-009 (see below) |
| `docs/METHODOLOGY.md` | +Phase 2a section, +Response to review (CR-2) subsection |

## Response to review (CR-2)

This branch was reviewed before merge; three follow-ups were made in
response (all after the original 6-domain extraction, before Phase 2b
started):

- **D-007 — supply-chain layer split.** `hardware_supply_chain` replaced
  with `supply_chain_hardware` / `supply_chain_software` /
  `supply_chain_services` in both schemas + `engine/types.ts`. The 7
  affected records retagged by subject matter; 4 of the original 15
  `needs_review` flags cleared outright, 1 (SOV-5-04) kept with an
  updated note since it genuinely spans all three.
- **D-008 — SOV-4-02-C2 erratum confirmed, not corrected.** Verified
  against the published PDF (p. 11): the text really does read "within
  the EU" / "outside Germany" as extracted. Left verbatim; intended
  meaning to be handled via a `generalization_note` in Phase 2d.
- **D-009 — verbatim text moved out of the public artifact.**
  `data/extracted/c3a.json`'s `source_text` values are now the literal
  placeholder `SEE-LOCAL-VERBATIM`; real text lives only in
  `data/local/c3a-verbatim.json` (git-ignored). `scripts/validate.py`
  cross-checks the two when the local file is present, skips the check
  in CI. **Two things this did NOT fix, both logged in D-009's "Scope
  note" / "Status":**
  1. `generalized_text` still equals the original verbatim English
     (Phase 2d hasn't run) — verbatim CC-BY-ND text is still present in
     the public file via that field, just not via `source_text` anymore.
  2. **Verbatim C3A text already exists in this repository's git
     history** — the original Phase 2a extraction commits (before
     D-009) contain it, and were pushed to `origin/phase-2a-c3a-extraction`
     before this review. D-009 does not rewrite that history. **This is
     a decision for the project owner**: whether to rewrite the branch's
     history (e.g. `git filter-repo`/interactive rebase + force-push)
     before merge to `main`, given the branch is not yet merged and
     `main` itself was never exposed to the verbatim text. Claude Code
     did not perform any history rewrite, per standing instruction never
     to take destructive git actions without explicit authorization.

Note: this session's instructions referenced a `reviews/phase-2a-review.md`
file as the source of CR-2; that file does not exist anywhere in this
repository (checked working tree and all branches). The CR-2 items were
executed from the instruction text given directly in the session, not
from a file — flagging this discrepancy for the record.

## Statistics

- **Total criteria extracted:** 59 (43 criteria, 16 additional criteria)
- **Per domain:** SOV-1: 7, SOV-2: 5, SOV-3: 15, SOV-4: 19, SOV-5: 9, SOV-6: 4
- **Derivation:** 100% verbatim (generalization is Phase 2d)
- **needs_review:** 11 records (19%), down from 15 after D-007 — see below
- **localization_level tagged:** 20 records (34%), only where a genuine EU/DE paired variant exists

Full breakdown in `docs/METHODOLOGY.md` Phase 2a section.

## needs_review summary (11 records, post-D-007)

| Records | Reason |
|---|---|
| SOV-2-03-C1, C2 | Criterion spans legal_jurisdiction/facility/operations_personnel at once |
| SOV-3-04-C, AC1, AC2 | Logging spans data vs. platform/operations_personnel |
| SOV-4-02-C2 | Verbatim text internally inconsistent ("within the EU" vs. "outside Germany") — confirmed against published PDF p. 11 (D-008), captured as printed, not corrected |
| SOV-4-03-C, AC | Connectivity redundancy spans facility vs. supply_chain_services |
| SOV-5-04-C | Spans supply_chain_hardware/software/services simultaneously (tagged hardware as primary) |
| SOV-5-05-C1, C2 | Filed under SOV-5 (Supply Chain) domain but content is capacity-management/platform, not supply-chain |

Cleared by D-007 (previously flagged, now resolved): SOV-5-01-C/AC
(-> `supply_chain_software`), SOV-5-03-C/AC (-> `supply_chain_services`).

Nothing was guessed silently — every ambiguous layer assignment carries a
one-line note explaining the ambiguity, per working rule 2.

## Open items for the project owner

1. **Layer taxonomy: mostly resolved (D-007).** SOV-5-04 remains
   genuinely multi-layer regardless of taxonomy granularity — no schema
   change can fully resolve a criterion that verbatim-spans three layers.
2. **D-002/D-005/D-006/D-009 license question remains open**, now
   narrower: `source_text` is scrubbed from the public
   `data/extracted/c3a.json` (D-009), but `generalized_text` still
   equals the verbatim English pending Phase 2d, and **verbatim text
   already exists in this branch's pushed git history** from before
   D-009. Two decisions needed from the project owner: (a) whether
   `generalized_text` needs scrubbing/placeholder treatment too before
   Phase 2d runs, and (b) whether to rewrite this branch's git history
   before merge (Claude Code did not do this — see CR-2 response above).
3. **SOV-4-02-C2 apparent source inconsistency** — confirmed against the
   published PDF (D-008), not corrected. Worth a sanity check against
   any official C3A errata/next revision if one appears.
4. **SI (Supplementary Information) content** was read but not extracted
   or stored anywhere in this repo, per phase scope. If the app should
   surface SI as contextual help text later, that's unextracted work.

## CI status

Confirmed locally: `scripts/validate.py`, `npm test`, and
`npm run typecheck` all pass (59/59 extracted records valid, personas
unaffected, 2 real tests still passing, 7 invariants still `todo`).
Pushed to `origin/phase-2a-c3a-extraction`; GitHub Actions run confirmed
green — see commit history on the branch for the run link.

---

**Addendum (CR-3):** `generalized_text` has since been scrubbed to the
placeholder `GENERALIZATION-PENDING` and a validator leak check added —
see D-010.

Per phase-gate discipline (working rule 6), Phase 2a stops here. ECSF
(Phase 2b) and CADA (Phase 2c) extraction do not start in this session.
