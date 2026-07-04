# Phase 2c report — CADA extraction

**Branch:** `phase-2c-cada` (branched from `main` post Phase 2a
squash-merge; Phase 2b, unmerged, was not a dependency for this phase)
**Scope:** Extract the CADA proposal (COM(2026) 502 final, 3.6.2026) —
Annex II criteria, Annex III audit evidence, and a hand-picked subset of
the Act itself — into `/data/extracted/`. No crosswalk work; `c3a.json`
untouched.

## Outputs

| File | Purpose |
|---|---|
| `data/extracted/cada.json` | 40 control records: Annex II Union assurance level criteria (UA-1: 7, UA-2/3/4: 11 each), `derivation: verbatim`, `status: proposed_legislation` |
| `data/extracted/cada-scope.json` | Annex II's introductory scope statement (software in/hardware out), file-level metadata |
| `data/extracted/cada-evidence.json` | 11 Annex III audit criteria (A-K), each with the Annex II paragraph it assesses and its evidence items, verbatim |
| `data/extracted/cada-act.json` | 13 hand-picked Act extracts (definitions, risk assessment, third-country mechanism, procurement, open-source preference), `derivation: derived` |
| `data/local/cada-verbatim.json` | Git-ignored, 40 verbatim entries (Annex II) |
| `data/local/cada-scope-verbatim.json` | Git-ignored, 1 verbatim entry (scope statement) |
| `data/local/cada-evidence-verbatim.json` | Git-ignored, 73 verbatim entries (Annex III) |
| `schema/control-record.schema.json` | +1 optional field: `assurance_level` (enum `UA-1`..`UA-4`) — the phase's one authorized addition to this schema |
| `schema/cada-evidence.schema.json` | New schema (the phase's one authorized new schema) |
| `scripts/extract_cada.py` | Domain-batched (per UA level) writer for `cada.json`/`cada-verbatim.json` |
| `scripts/extract_cada_evidence.py` | Writer for `cada-evidence.json`/`cada-evidence-verbatim.json` |
| `scripts/extract_cada_act.py` | Writer for `cada-act.json` (no verbatim isolation — see below) |
| `scripts/validate.py` | +`check_cada_scope()`, +`check_cada_evidence()`, +`check_cada_act()`, +`check_verbatim_placeholder_count()`; `check_verbatim_leak()`/`check_local_verbatim()` extended with `NON_CONTROL_RECORD_FILES`/`ID_KEYED_VERBATIM_EXCLUSIONS` (merged with Phase 2b's equivalent infrastructure at the post-merge rebase) |
| `docs/DECISIONS.md` | +D-017 (`cada-act.json`'s data shape doesn't conform to `control-record.schema.json`, and why — originally logged as D-012, renumbered at rebase per CR-2) |
| `docs/METHODOLOGY.md` | +Phase 2c section |

## Scope note: Annex I excluded

Annex I ("Grand Challenges") defines eight EU R&D funding priority areas
(data centre efficiency, cloud stacks, frontier/physical/industrial AI,
AI agents platform, public sector AI). It contains no assessable
criteria, no obligations on a government cloud customer, and no
definitions used elsewhere in this catalog — it is a research-funding
policy annex, out of scope for CSAT entirely, per this phase's explicit
instruction. Not extracted anywhere in this repo.

## UA-1 vs. UA-2/3/4: two distinct criteria schemes

Annex II's four levels are not one 11-letter scheme repeated four times
with wording deltas. UA-1 (self-assessed, Article 19) has its own
7-criterion scheme (a)-(g); UA-2/UA-3/UA-4 (independently audited,
Article 20, cumulative among themselves) share an 11-criterion scheme
(a)-(k). Every level's own wording was extracted verbatim and separately
— including where UA-2/3/4 repeat a criterion almost unchanged — per
this phase's explicit "do NOT dedupe across levels" instruction; that
consolidation is Phase 3's job.

## SOV domain / layer mapping (Annex II)

Each lettered criterion was mapped to a SOV domain and layer by
substance, cross-checked against Phase 2a's own C3A layer-tagging
precedent for consistency. Full reasoning in METHODOLOGY.md. Notably:
criterion (e) (cybersecurity certification) maps to SOV-7, which is
inheritance-only project-wide — its `disposition_default` is set to
`inherit` rather than `assess`, and its `layer` is flagged `needs_review`
since the ten-value layer taxonomy has no SOV-7-specific option.
Criterion (g) (third-country control) was tagged SOV-1, matching ECSF's
own "Change of Control Risk" factor, and flagged as a genuine SOV-1/SOV-2
boundary case.

## Source cross-reference discrepancy (captured, not corrected)

Annex II 3.1(g) and Annex III criterion G both cite "an implementing act
under Article 19" for the third-country adequacy mechanism, but Article
19 in the extracted Act text is "Conformity self-assessment" (UA-1) —
Article 18, "Associated third countries", is what substantively matches.
Likely a cross-reference error in this draft. Captured verbatim as
printed (citing Article 19) and flagged `needs_review` on both
`csat-sov1-cada-ua3-g` (`cada.json`) and
`cada-act-art18-associated-third-countries` (`cada-act.json`), rather
than silently "corrected" — a later consolidated text may resolve this
differently than assumed here. **Recommend the project owner verify
against an official consolidated version before Phase 3 relies on
either article number.**

## `cada-act.json`'s data shape (D-017, originally D-012)

Does not conform to `control-record.schema.json` and no new schema was
created for it. Reasoning: most of what the extracted articles describe
(risk assessment, procurement, open-source preference) are obligations
on the **assessing government itself**, not a cloud provider's posture —
the schema's `layer`/`disposition_default` shape is built for the
latter. `derivation: "derived"` throughout (plain-language restatements
with a short, sub-16-word `source_quote` anchor, not verbatim block
quotes), so no verbatim-isolation regime applies to this file.

## UA ↔ SEAL ↔ C1/C2 ladder — a Phase 3 input, not resolved here

CADA (UA-1..4), ECSF (SEAL-0..4), and C3A (localization levels C1/C2)
each define their own maturity/assurance scale, and Phase 3's crosswalk
will need to relate them. A few observations to seed that work, offered
as hypotheses, not conclusions:

- **UA-1** is self-assessed and its criteria (EU establishment, EU data
  residency "unless the public sector body explicitly requires
  otherwise," state-of-the-art cybersecurity, subcontractor transparency)
  are structurally closer to a baseline/entry tier than to any single
  ECSF SEAL level — it has no independent-audit backing, which ECSF's
  SEAL-2+ generally presupposes via its evidence-quality framing.
- **UA-2/UA-3/UA-4** are cumulative and independently audited, echoing
  ECSF's own weakest-link SEAL aggregation rule (Implementation
  Guidance, "overall SEAL = lowest across objectives" — captured on the
  `phase-2b-ecsf` branch, not yet merged). UA-4's strictest criteria
  (Union-citizen-only personnel with security clearance, no third-country
  control at all, "high" cybersecurity certification, customer data
  restricted following a sensitivity risk assessment) look substantively
  closest to ECSF's SEAL-4 ("Full Digital Sovereignty") and to C3A's C2
  (Germany-level, the stricter of C3A's two localization tiers) — but
  this is a structural resemblance, not a verified equivalence.
- **UA-3's derogation** (control by an adequacy-listed third country's
  entity is tolerated via the Article 18/19 mechanism) has no obvious
  ECSF or C3A analogue captured so far — worth an explicit Phase 3
  question rather than an assumed gap.
- **No numeric or formulaic mapping is asserted here.** Phase 3 should
  treat any UA<->SEAL<->C1/C2 correspondence as requiring its own
  evidence and DECISIONS entry, exactly like the `ecsf-c3a-hints.json`
  coverage hints — a hypothesis for verification, not a finding.

## Statistics

- Annex II: 40 criteria (UA-1: 7, UA-2: 11, UA-3: 11, UA-4: 11), 100%
  verbatim, 4/40 (10%) needs_review (criterion e x4 levels — SOV-7 layer
  gap; criterion g x4 levels — SOV-1/SOV-2 boundary; UA-1 b/d — framing;
  UA-3 g — Article 18/19 citation).
- Annex III: 11 audit criteria (A-K), 100% verbatim, 0 needs_review
  (extraction-only, no interpretation asked or performed).
- Act extracts: 13 records, 100% derived, 2/13 needs_review (Union
  entities vs. public-sector-body persona-model gap; Article 18/19
  citation, echoed from Annex II).

## Open items for the project owner

1. **Article 18/19 citation discrepancy** — verify against an official
   consolidated text before Phase 3 treats either article number as
   authoritative for the third-country adequacy mechanism.
2. **"Union entities" vs. "public sector body"** — CADA names both as
   distinct addressees of its risk-assessment/procurement obligations
   (Articles 29-30); CSAT's persona model currently targets national/
   subnational governments only. Whether EU-institution-level personas
   are ever in scope is an open product question, not resolved here.
3. **Cross-branch DECISIONS.md numbering — resolved.** This phase
   originally logged its `cada-act.json` shape decision as D-012 in
   parallel with `phase-2b-ecsf`'s own independent D-012..D-016. Per the
   Phase 2c review's CR-2, `phase-2b-ecsf` merged first (keeping
   D-012..D-016); this branch's entry was renumbered to **D-017** at
   rebase onto the post-merge `main`. See `docs/DECISIONS.md` D-017 and
   the new CLAUDE.md working rule on provisional parallel-branch
   numbering.
4. **UA↔SEAL↔C1/C2 ladder** (above) is offered as Phase 3 input only;
   none of it is asserted as a verified crosswalk.

## CR-1 addendum (external fidelity check)

The reviewer's CR-1 fidelity check (`reviews/phase-2c-review.md`)
diffed `data/local/cada-verbatim.json` against the Annexes text directly
and found one transcription deviation: `csat-sov4-cada-ua2-d` (Annex II
2.1(d)) had silently corrected the source PDF's typo "presonnel" to
"personnel." Restored to read "presonnel" verbatim and flagged
`needs_review`; logged as D-018 (correction). No other deviations found
across the ≥10-record verbatim sample spanning all four UA levels and
Annex III; completeness re-confirmed; `source_pointer.document` pinning
to "COM(2026) 502 final, 3.6.2026" confirmed on all records. CR-1 is
closed.

## CI status

Confirmed locally: `scripts/validate.py` (with `data/local/` present,
leak check active throughout extraction), `npm test` (2 passing, 7
todo), `npm run typecheck` all pass. The leak check and the new
placeholder-count/structural checks were each manually verified to fail
on a deliberately injected defect (a leaked verbatim span, a
placeholder/local-entry count mismatch, a missing required field), then
reconfirmed clean after restoring the generated files. `git log
--name-only` confirms `data/local/` was never staged on this branch.
Pushed to `origin/phase-2c-cada`; GitHub Actions run confirmed green.

---

Per phase-gate discipline (working rule 6), Phase 2c stops here. No
merge to `main`, no crosswalk work beyond the UA↔SEAL↔C1/C2 observations
above (explicitly not a crosswalk), `c3a.json` untouched.
