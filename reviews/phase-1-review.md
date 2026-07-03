# Phase 1 review — schemas, personas, test harness

**Reviewer:** External (Claude, project design advisor)
**Date:** 2026-07-02
**Branch reviewed:** `phase-1-schema` @ 45d7fc8
**Verdict:** APPROVED with two minor change requests (below). Merge after fixes.

## Findings

### Conformant
- All Phase 1 deliverables present; CI green on both jobs (validate-python, test-engine incl. typecheck).
- Provenance model correctly enforced in schemas: `derivation` tiers, required `source_refs`, lang-strings requiring en+fr, `proposed_legislation` status for CADA-derived records, and disposition rules requiring `decision_ref` — every editorial judgment is structurally traceable.
- `wording_variant` correctly modeled as a variant selector within `assess` (not a separate disposition), with a schema conditional requiring it when used.
- 8 personas as separate draft YAML files with design-intent commentary. P2 correctly encodes the "facility-sovereign but tech/ops-constrained" trap case, including the explicit bug condition (P2 scoring near P1 = engine defect).
- Persona-approval gate implemented twice: validate.py (approval metadata) and `loadApprovedPersonas()` in the test helper (runner refuses drafts).
- Invariant stubs I1–I7 all present with definitional docstrings; I2 restates the relevance rule verbatim and names its phase dependencies.
- DECISIONS.md: 4 entries (D-001..D-004), well-formed, append-only style. D-002 (source PDFs held out of public repo pending license clarification) endorsed — record the eventual BSI/counsel resolution as a new entry.
- Phase report is accurate and appropriately candid about what is deferred.

### Change requests (pre-merge)
- **CR-1:** Add `# OWNER-REVIEW:` markers in all 8 persona files at every plausible-but-unconfirmed modeling choice (contract terms, tier selections, partner-model assumptions, etc.), per the Phase 1 instructions. These markers are the owner's amendment roadmap.
- **CR-2:** Update CLAUDE.md title/version header — content is v4 (includes Transparency & provenance, Frontend architecture) but header says v2.

### Noted for later (non-blocking)
- **N-1:** Consider an optional `help_text` lang-string on the control record at Phase 6 (plain-language explanation under each rendered question). Non-breaking addition; do not add now.
- **N-2:** `sov_domain` is single-valued — accepted as source-faithful to C3A's structure (minimal editorial choice). If Phase 3 crosswalk reveals genuinely multi-domain controls, revisit via a DECISIONS.md entry.

## Owner actions after merge
1. Amend all 8 personas (focus: P2 modifiers, P5 contract terms, P7 partner model), then set `status: approved` + `approved_by` + `approved_date`.
2. Author Layer-2 spot-check assertions against approved personas (15–30 per persona) before any Phase 4 engine work; Phase 2 extraction may proceed in parallel.
