# Phase 2a review — C3A extraction

**Reviewer:** External (Claude, project design advisor)
**Date:** 2026-07-02
**Branch reviewed:** `phase-2a-c3a-extraction` @ ff81c1d
**Verdict:** CONDITIONALLY APPROVED — merge after CR-1 (fidelity spot-check) and CR-2 (supply-chain layer split).

## Verified by reviewer (hands-on)
- validate.py executed independently: PASS (59 records, schema-conformant, unique IDs).
- Counts reconcile with phase report: 59 total = 43 C + 16 AC; SOV-1:7, SOV-2:5, SOV-3:15, SOV-4:19, SOV-5:9, SOV-6:4; derivation uniformly `verbatim`.
- All 10 C1/C2 localization pairs contain genuinely differentiated text — no transcription-duplication artifacts.
- needs_review discipline: 15/59 flagged with substantive analytical notes, correctly clustered on the supply-chain taxonomy gap and multi-layer criteria. Conforms to working rule 2 (never guess silently).
- Extraction judgment calls endorsed: criterion_type derived from source labels rather than ID suffixes; localization_level applied only to true paired variants; disposition/weight deliberately deferred to Phases 4–5.
- D-005, D-006 present and well-formed. `source_pointer.page` schema addition was within the Phase 2a instructions and disclosed.
- SOV-4-02-C2 anomaly: reviewer diffed the pair; the record is internally mixed (sentence 1 "within the EU", sentence 2 "outside Germany") — pattern consistent with a source misprint rather than a transcription slip. Owner to confirm against PDF p.11; if confirmed, consider reporting the erratum to BSI and logging the confirmation as a DECISIONS entry.

## Not verified (reviewer limitation)
- **Verbatim fidelity against the source PDF.** The PDF is (correctly, per D-002) not in the repo, and BSI's site serves an HTML wrapper to the reviewer's fetcher. Hand-transcription is the highest-risk step in the provenance chain, so a fidelity check is a merge condition, not optional.

## Change requests (pre-merge)
- **CR-1 (fidelity spot-check):** Owner provides the C3A PDF to the reviewer (or performs the check locally): verify ≥10 records spanning all six domains, both criterion types, and ≥2 C1/C2 pairs, character-for-character against the source. Record the outcome in this file or a follow-up note.
- **CR-2 (supply-chain layer split — do NOW, before Phases 2b/2c):** Split layer enum value `hardware_supply_chain` into `supply_chain_hardware`, `supply_chain_software`, `supply_chain_services` (distinct responsible parties, which is what the layer field exists to capture). Retag the affected records, clear the corresponding needs_review flags where the new taxonomy resolves them, log as D-007. Migration is trivial at 59 records and painful after ECSF/CADA extraction.

## Noted for later (non-blocking)
- **N-1:** Supplementary Information (SI) blocks excluded — acceptable for Phase 2a scope. When `help_text` is added (Phase 6, see phase-1 review N-1), extract SI *pointers* (section/page references, not text) to ground help content without license exposure.
- **N-2:** csat-sov5-05-c1/c2 domain-vs-layer tension: keep flagged; resolve during Phase 3 layer-tagging review.

## Owner actions
1. CR-1 fidelity check (with reviewer or locally, documented).
2. CR-2 layer split on this branch.
3. Confirm SOV-4-02-C2 against PDF p.11; report erratum to BSI if confirmed.
4. Merge; then Phase 2b (ECSF) may start. Persona approval + Layer-2 assertions remain due before Phase 4.
