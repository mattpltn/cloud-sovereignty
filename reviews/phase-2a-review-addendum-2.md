# Phase 2a review — Addendum 2: CR-2 execution verification

**Reviewer:** External (Claude, project design advisor)
**Date:** 2026-07-03
**Branch reviewed:** `phase-2a-c3a-extraction` @ 6d1c580 (commits 74dfe24, 1e8f931, f382499, 6d1c580)

## Verified hands-on
- **D-007 (CR-2):** layer enum split landed in control-record schema and engine/types.ts; retags confirmed (supply_chain_software: 2, supply_chain_hardware: 3, supply_chain_services: 2); needs_review reduced 15 → 11; SOV-5-04-C correctly kept flagged (spans all three supply chains).
- **D-008:** erratum confirmation logged; record untouched, verbatim as printed.
- **D-009:** source_text placeholders in all 59 public records; verbatim moved to data/local/ (git-ignored, zero tracked files).
- Executor self-reporting was accurate and appropriately candid (commit-boundary slip disclosed; residual gap disclosed; no unauthorized history rewrite). Endorsed.

## New merge blockers found
- **CR-3:** `generalized_text` still carries full verbatim C3A text in the public artifact for all 59 records (confirmed by reviewer), making D-009 ineffective as committed. Remediate: replace with "GENERALIZATION-PENDING" placeholders + add a validator leak check (no public text field may equal or contain a >15-word span of a local verbatim entry when the local file is present). Log as D-010 correction entry.
- **CR-4 (process):** /reviews is empty across all branches — including Phase 1, which was merged without its review note landing, contrary to the CLAUDE.md workflow. Owner to commit all review notes (phase-1 review, phase-2a review, CR-1 addendum, this addendum) before merging this branch.

## History exposure — reviewer recommendation
Pre-D-009 commits on this public branch contain the full verbatim text; the D-009/CR-3 fixes do not remove them. Recommended handling: after CR-3, **squash-merge** this branch to main (single commit, message summarizing the per-domain batches and D-007..D-010) and delete the remote branch; log the deviation from per-batch public history as a DECISIONS entry (license caution, granular history preserved locally). Note: unreachable commits may persist in GitHub caches for a time; complete purging would require a GitHub support request — proportionate to defer unless BSI's reuse guidance comes back negative. No force-push/history rewrite recommended at this time.

## Status
Phase 2a merge blocked on CR-3 + CR-4. All previously verified results (CR-1 fidelity, completeness 59/59) remain valid — the placeholder substitution does not alter record identity, pointers, or the locally retained verbatim chain.
