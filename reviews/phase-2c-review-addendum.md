# Phase 2c review — Addendum: CR-1 fidelity results (CADA + ECSF guidance)

**Reviewer:** External (Claude, project design advisor)
**Date:** 2026-07-03
**Materials:** data/local/cada-verbatim.json and data/local/ecsf-guidance-verbatim.json (owner-supplied); COM(2026) 502 final Annexes and ECSF Implementation Guidance (in reviewer's possession).

## CADA (Annex II) — 12-record sample across all four UA levels
- **Source pin verified:** source_pointer.document = "COM(2026) 502 final, 3.6.2026 — Annexes 1 to 3" with page on 40/40 records.
- **11/12 records verbatim-exact** under the documented convention (terminal `;` at criterion boundaries normalized to `.`, applied consistently — accepted).
- **1 violation — CR-1a:** UA-2 criterion 2.1(d) silently corrected the source's printed typo "presonnel" → "personnel". Verbatim discipline requires the typo preserved as printed + needs_review flag. Fix specified in the consolidation-session instructions. Incidentally the pipeline's THIRD official-source erratum catch (after BSI SOV-4-02-C2 and the CADA Art. 18/19 cross-reference).

## ECSF Implementation Guidance — full verification (25 entries)
- SEAL aggregation rule, SEAL-3 label variant, and all per-domain SEAL-2/3/4 requirement cells: verbatim-exact.
- **CR-1b (flags to confirm/add):** (i) SOV-7 SEAL-3 cell "ELA 3." is a probable source typo for "EAL 3" — preserved correctly; must carry needs_review (erratum candidate #4). (ii) SOV-8 row: two source cells across three SEAL columns; the seal2+seal4 assignment is an interpretation the linear text cannot settle — needs_review with the ambiguity noted, pending visual confirmation of the PDF table.
- Accepted convention extension: line-break hyphenation artifacts reconstructed (SOV-6 SEAL-2 "on-premises"); to be recorded in METHODOLOGY alongside the punctuation rule.

## Status
CR-1 conditionally satisfied: closes upon execution of corrections (i)–(iii) as folded into the consolidation session (item 3b). Calculator extraction (ecsf-calculator.json) not yet available for verification — reviewer will verify its answer-point values and per-answer SEALs against the official XLSX (in hand) once Phase 2b.1 lands; that check is REQUIRED before Phase 5 uses those values.
