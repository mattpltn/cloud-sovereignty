# Cloud Sovereignty Assessment Tool (CSAT) — v2

## Purpose
A questionnaire-based assessment tool for **governments in emerging markets** to understand and incrementally improve their cloud sovereignty posture. The tool NEVER judges a deployment choice as right or wrong. Output = a **posture profile** (per-domain achieved score vs. structural ceiling) + **improvement paths** ranked by effort and impact, in three buckets:
- **Negotiate** — contract clauses to pursue with providers (CSP, colo, vendor, MSP)
- **Implement** — internal fixes within the government's own responsibility
- **Strategic options** — longer-horizon architectural choices, presented with tradeoffs (cost, capacity, continuity), never as prescriptions

## Source frameworks (in /sources — READ-ONLY, never edit)
1. **BSI C3A v1.0** (Apr 2026) — primary criteria source. Domains SOV-1..SOV-6 (strategic, legal & jurisdictional, data, operational, supply chain, technology). Criteria (C) + Additional Criteria (AC) + Supplementary Information. Localization levels C1 (EU) / C2 (Germany).
2. **EU Cloud Sovereignty Framework v1.2.1 (ECSF)** — SOV domain definitions, SEAL maturity levels (0–4), weighted scoring model.
3. **CADA proposal** (EU Commission, Jun 2026) — legislative obligations extracted as control statements, flagged `status: proposed_legislation`.

C3A translates ECSF factors into verifiable criteria and presupposes BSI C5 for security. SOV-7 (security) is **inheritance-only** here (satisfied by C5/ISO 27001/SOC 2 evidence; no questions). SOV-8 out of scope.

## Policy alignment (grounds all recommendation text — see References)
- **World Bank outcome-based approach to digital sovereignty**: define outcomes, assess tradeoffs, build capacity. Recommendations must speak this language.
- **WB caution on blanket data localization**: costs, security, portability, continuity tradeoffs. The tool NEVER recommends "move data in-country" as a default. Localization appears only as a strategic option with tradeoffs stated.
- **Risk-tiered estates** (Singapore pattern): different workload classifications legitimately live on different deployment models.
- **Regional trust frameworks** (AU Data Policy Framework, Malabo, AfCFTA digital trade protocol): the `{TRUSTED_REGION}` concept maps to real adequacy/reciprocity mechanisms.

## Transparency & provenance (non-negotiable)
This tool must be publicly defensible: anyone must be able to trace every question, rule and score to a globally recognized source, and see exactly where human judgment was applied.
1. **Public repository.** The repo is public from day one; all work happens in the open.
2. **Full traceability.** Every catalog record carries `source_refs` (framework + exact criterion/section ID, e.g., `C3A SOV-4-01-C2`). Every rendered question displays its source citation(s) in the UI. Every disposition rule and scoring formula cites its basis.
3. **Derivation tiers.** Every record and rule is tagged `derivation:` one of:
   - `verbatim` — framework text as-is
   - `generalized` — placeholder substitution only, applied via the documented substitution rules (no freehand rewording)
   - `derived` — restructured from a source (e.g., CADA obligation → control statement), with the source passage referenced alongside
   - `editorial` — a project judgment (default weights, disposition mappings, question phrasing choices). MUST have an entry in docs/DECISIONS.md.
4. **Decision register (docs/DECISIONS.md).** "Minimal editorial choice" cannot mean zero — so every unavoidable judgment is logged: ID, date, decision, alternatives considered, rationale, and framework anchor where partial. This register is the standing answer to any bias critique: nothing is hidden.
5. **Methodology document (docs/METHODOLOGY.md).** Written incrementally: each phase appends the section describing exactly what was done and how (extraction rules, substitution rules, disposition logic, scoring math, testing method). A phase cannot merge without its methodology section.
6. **Phase reports.** Each phase ends with `docs/phases/phase-N-report.md`: scope, outputs, statistics (records per derivation tier, needs_review count), CI status.
7. **License care.** C3A is CC-BY-ND 4.0 (no derivatives) — verify with BSI/counsel how far verbatim reproduction and generalization may go in a public repo. Cautious default: public records carry source IDs + `generalized_text`; verbatim `source_text` is included only where the license clearly permits, otherwise referenced by pointer (document + section) to the official PDF. ECSF and CADA follow EU Commission reuse policy. Record the resolution in DECISIONS.md.

## Core design principles
1. **Controls are data, not code.** All criteria live in JSON under /data validating against /schema. Engine and app read them; logic never hardcodes individual controls.
2. **Jurisdiction parameterization.** Placeholders `{NATION}` (assessing country; generalizes C2/Germany) and `{TRUSTED_REGION}` (its trusted bloc; generalizes C1/EU). `source_text` is always preserved verbatim; generalized text in `generalized_text`.
3. **Two-axis scenario model** (see below). Dispositions are COMPUTED from a layer-responsibility map — never hand-tagged per scenario.
4. **Non-judgmental language.** Generated text never uses pass/fail, compliant/non-compliant, or imperative relocation advice. Use: "met / not yet met / structurally constrained in this posture", "opportunity to strengthen via…".
5. **Outcome weighting.** The assessment opens by eliciting the government's sovereignty priorities (continuity under disconnection/sanctions; protection from foreign legal access; lock-in avoidance; local capacity building; cost efficiency). Domain weights derive from this ranking, not fixed ECSF procurement weights.
6. **Classification tiering.** Assessments run per workload tier (per national data classification, or a default 4-tier scheme: public / internal / restricted / secret). One government = several assessments = a tiered posture map.

## Scenario model
**Axis A — Deployment** (who provides what):
- A1: Government-owned datacenter, government cloud
- A2: Government cloud in a commercial colocation facility (in-country)
- A3: IaaS/PaaS/SaaS from a local (in-country) cloud provider
- A4: IaaS/PaaS/SaaS from an international provider (hyperscaler)
- A5: Partner-operated "sovereign region" of an international provider

**Axis B — Platform stack** (A1/A2 mainly): vanilla open source | open source + commercial support | closed proprietary ecosystem (e.g., Huawei/VMware/Nutanix)

**Modifiers:** ops outsourced (to whom, which jurisdiction) | service model (IaaS/PaaS/SaaS) | provider & facility jurisdiction and extraterritorial-law exposure | key custody (provider-held / HYOK / external HSM) | existing contract terms (audit rights, exit/reversibility, residency, escrow) | workload classification tier.

**Layer-responsibility map:** from Axis A + B + modifiers, the engine derives, for each layer (legal/jurisdiction, facility, hardware/supply chain, virtualization, platform, data, identity, operations/personnel), WHICH party owns it, operates it, and has legal reach over it. All dispositions and wording variants derive from this map. Example: A2 → facility layer = colo provider (assess facility-dependency controls, adapted wording), platform layer = government (assess normally), CSP-upper-stack controls = suppress (no such party exists).

## Dispositions (resolved per control, per assessment, BEFORE any question is shown)
- `assess` — ask; wording variant selected by the responsibility map (`adapt_wording` is a text-variant mechanism inside assess, not a separate disposition)
- `auto_answer` — the engine answers on the government's behalf: VISIBLE prefilled answer + plain-language rationale + citation of the rule that fired + user override allowed. Used when posture determines the answer (e.g., A4 foreign hyperscaler → "{NATION} law applies to the provider environment" = not met, with rationale). Replaces v1's silent `auto_fail` — nothing is scored invisibly.
- `inherit` — satisfied by provider certification evidence (C5, ISO 27001, SOC 2, C3A audit); asks only for the evidence artifact.
- `suppress` — truly N/A: the control's addressed party/layer does not exist in this posture. Excluded from scoring (weights renormalized) — never counted as failure.

**Cross-cutting flag `negotiation_opportunity`:** attachable to any control (usually auto_answer=not-met or assess=not-met) carrying model contract clause language. This is a core value-add: every structural gap should, where realistic, surface a clause suggestion.

## Scoring
Per SOV domain and per workload tier: **achieved** score, **ceiling** (max attainable in this posture given structural constraints), and gap decomposition → negotiate / implement / strategic-options buckets. Evidence quality weighting: self-attested < contractual commitment < third-party certified < independently audited. Overall score uses the outcome-derived weights.

## Frontend architecture
1. **Client-side only — no backend, ever.** Assessment answers (posture, contract gaps, key custody) are sensitive government information and MUST never leave the user's device. Static web app: catalog JSON bundled, engine runs in the browser, state saved/resumed via local JSON file export. No accounts, no analytics, no trackers, no external calls at runtime. Deployable on GitHub Pages AND downloadable as a zip for offline/intranet/air-gapped use. The public repo is the running app — auditable end to end.
2. **One engine, one language.** The engine (/engine) is **TypeScript**: the exact same build passes the golden-persona test suites in CI and runs in the browser. No parallel implementations, no ports. Python is used only for extraction tooling and data validation (validate.py). Log this as a DECISIONS.md entry in Phase 1.
   - This machine's system Python is externally managed (PEP 668); use the project venv: `python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt`, then run tools via `.venv/bin/python3 ...` (`.venv/` is gitignored).
3. **Flow (5 screens):**
   1. *Methodology landing* — sources, derivation tiers, license, decision-register link, and the privacy statement ("your answers never leave your device").
   2. *Priorities* — rank sovereignty outcomes → domain weights.
   3. *Posture wizard* — Axis A/B + modifiers in plain language, one per screen with help text; workload tier selection.
   4. *Auto-resolution review* — BEFORE the questionnaire, show what the engine resolved: counts of auto-answered / suppressed / inherited controls; each auto_answer with rationale, rule citation, override toggle, and negotiation flag. Irrelevance-prevention made visible.
   5. *Questionnaire → results* — questions grouped by SOV domain, each with a framework citation chip and evidence-quality selector. Results: per-domain bars with three segments — achieved (solid), gap-to-ceiling split into negotiate/implement (hatched), above-ceiling greyed and labeled "structural in this posture → strategic options".
4. **Report-first.** The exportable report is the primary product (ministers and negotiators circulate documents, not dashboards): executive summary, posture profile, three recommendation buckets with model clause language and framework citations on every item, per-tier breakdown. Generated client-side (print stylesheet / PDF).
5. **i18n from day one.** Every UI string externalized; every human-readable field in catalog/schema is a language-keyed object (`{"en": …, "fr": …}`). English + French minimum.
6. **Design tone:** sober, institutional, accessible (WCAG AA); something a ministry can put in front of an oversight committee.

## Repository layout
```
/sources       Framework PDFs/texts (read-only)
/schema        JSON Schemas (control record, persona/assessment profile, disposition rules)
/data
  /extracted   Raw per-framework extractions (c3a.json, ecsf.json, cada.json)
  /catalog     Master catalog + crosswalk
/engine        TypeScript: responsibility-map builder, disposition resolver, scoring, recommendations — the SAME build runs in CI tests and in the browser
/app           Static client-side web app (no backend); consumes /engine + catalog JSON
/tests
  /personas    Golden persona YAML files (design fixtures — written in Phase 1)
  /invariants  Property tests that must hold for ANY persona
  /assertions  Curated per-persona spot-check assertions
  /snapshots   Full committed output snapshots per persona (diff-reviewed)
  /relevance   LLM-judge rubric + relevance review outputs
/docs
  METHODOLOGY.md   Incrementally written public methodology
  DECISIONS.md     Editorial decision register (append-only)
  /phases          phase-N-report.md per completed phase
/scripts       validate.py, run_tests.py
/reviews       Phase review notes from external reviewer
.github/workflows/ci.yml   Runs validator + all test layers on every push
```

## Testing methodology (MANDATORY — the previous project failed on question relevance)
Definition: a question is **relevant** for a persona iff (a) its addressed party/layer exists in the persona's responsibility map, (b) the government can act on the answer (implement, negotiate, or it is auto-answered/inherited with rationale), and (c) its wording matches who actually holds the responsibility. Every test layer defends this definition.

Runners: Layers 1, 2, 3 and 5 execute against the TypeScript engine via a Node test runner (e.g., vitest) in CI; validate.py (Python) covers data/schema validation and the persona-approval gate.

**Layer 1 — Invariants** (run against every persona, current and future):
- I1: every catalog control resolves to exactly one disposition; zero unresolved, zero rule conflicts (two rules firing with different dispositions = build failure, not silent precedence).
- I2: **no rendered question references a party or layer absent from the persona's responsibility map.** (The #1 defense against irrelevant questions.)
- I3: no unresolved placeholders ({NATION}, {TRUSTED_REGION}, {PROVIDER}) in any rendered text.
- I4: achieved ≤ ceiling ≤ 100 in every domain/tier; suppressed controls contribute zero weight and weights renormalize.
- I5: every auto_answer carries a rationale and a rule citation; every negotiation_opportunity carries clause text.
- I6: monotonicity — adding a strengthening modifier (e.g., HYOK, audit-rights clause) never lowers any score or ceiling; removing one never raises them.
- I7: questionnaire size sanity — asked (assess) question count per persona within a declared band (e.g., 25–90); >90 means suppression/auto_answer logic is leaking.

**Layer 2 — Persona spot-checks:** per golden persona, 15–30 hand-written assertions on high-value controls (exact disposition, wording variant chosen, ceiling for a named domain, presence of a specific clause suggestion). Written by the project owner BEFORE the engine exists (test-first) and treated as the specification.

**Layer 3 — Snapshot diffs:** the full engine output per persona (all dispositions, scores, recommendations) is committed under /tests/snapshots. CI fails on any diff. Re-baselining requires: (1) human review of the diff, (2) a note in /reviews explaining why the change is correct, (3) explicit commit message `rebaseline: <persona> — <reason>`. Claude Code MUST NEVER re-baseline a snapshot on its own initiative.
- **L3-safety net:** an unexplained diff in a persona untouched by the change being made is always a bug. Stop and report.

**Layer 4 — Relevance review (LLM-as-judge):** for each persona, render the complete questionnaire and have Claude role-play that persona's CISO answering it, scoring each question 1–5 on a fixed rubric (applicable? answerable? wording matches my responsibilities? actionable?). Any question scoring ≤2 opens an issue. Run at the end of Phases 4, 5 and 6. Judge outputs are advisory inputs to human review, never auto-fixes.

**Layer 5 — Differential pairs:** persona pairs differing in exactly ONE axis/modifier, with asserted deltas (e.g., A4±HYOK → data-domain ceiling rises; A3 local vs A4 foreign provider → jurisdiction controls flip auto_answer→assess; A1 vanilla-OSS vs A1 closed-stack → technology-domain ceiling drops). Catches rule-interaction bugs that single-persona tests miss.

**Persona ownership workflow:** Claude Code DRAFTS each golden persona as a SEPARATE YAML file in /tests/personas, with `status: draft` and inline comments explaining every field. The project owner amends the file and sets `status: approved` (+ `approved_by`, `approved_date`). validate.py and the test runner MUST refuse to execute engine tests against any persona not marked approved. Claude Code never sets `approved` itself.

**Golden persona set (draft in Phase 1 as separate YAML design fixtures):**
- P1 `gov-dc-oss-inhouse` — A1, vanilla OpenStack, in-house ops (high-sovereignty baseline)
- P2 `gov-dc-closed-outsourced` — A1, closed ecosystem stack, ops outsourced to foreign vendor (facility-sovereign but tech/ops-constrained — must NOT score as sovereign across the board)
- P3 `colo-oss-supported` — A2, foreign-owned in-country colo, OSS + commercial support
- P4 `local-csp-iaas` — A3, IaaS, restricted-tier workload
- P5 `hyperscaler-iaas-strong-contract` — A4, IaaS, HYOK + audit + residency clauses
- P6 `hyperscaler-saas-standard` — A4, SaaS, standard terms (lowest-ceiling case)
- P7 `sovereign-region-partner` — A5
- P8 `mixed-tier-estate` — one government, public tier on A4 + restricted tier on A1 (exercises classification tiering)

## Working rules for Claude Code
1. **Small batches.** Max ONE SOV domain (~15 controls) per extraction task. After each batch: `python scripts/validate.py`, fix, commit.
2. **Never invent criteria.** Every record cites its exact source ID (e.g., SOV-4-01-C2, ECSF section, CADA article). Ambiguity → `"needs_review": true` + note; never guess.
3. **Never modify /sources.** Never modify /schema, /tests/personas, /tests/assertions or /tests/snapshots without explicit instruction (snapshots: see L3 re-baseline rule).
4. **Verbatim first, transform second.** Extraction captures `source_text` verbatim; generalization is a separate pass with separate commits.
5. **Git discipline.** One branch per phase (`phase-1-schema`, `phase-2a-c3a-extraction`, …). Commit per validated batch: `phase-2a: extract SOV-4 (12 criteria, validator pass)`. Push every session. Merge to `main` only after external review notes land in /reviews. Review notes for phase N are always committed on phase N's branch before it merges; a phase merges to main only as its own reviewed unit, never as a side-effect of another branch's merge.
6. **Phase gates.** Complete only the current phase's scope. When done: summarize, list open `needs_review` items, confirm CI green, push, STOP. Never start the next phase in the same session.
7. **Tests are law.** No commit with failing validator or tests. If a test seems wrong, flag it in the session summary — do not weaken tests, skip tests, or re-baseline to make CI pass.
8. **Tone rules apply to generated content** (question text, rationales, recommendations): non-judgmental vocabulary per design principle 4; recommendations reference the World Bank outcome-based framing where relevant.
9. **Provenance discipline.** Never create a record or rule without `derivation` + `source_refs` (or, for `editorial`, a DECISIONS.md entry written in the same commit). Never edit existing DECISIONS.md entries — the register is append-only; corrections are new entries referencing the old ID.
10. **Documentation duty.** A phase is not complete until its METHODOLOGY.md section and phase report exist. Documentation is a deliverable, not an afterthought.
11. **DECISIONS numbers on parallel phase branches are provisional; the later-merging branch renumbers at rebase.**

## Current phase
> Update this line as phases complete.
Phase 2 extraction complete and merged to main: C3A, ECSF, and CADA all extracted (Phases 2a-2c) and generalized (Phase 2d) — see docs/phases/phase-2a-report.md through phase-2d-ii-report.md. **Next: Phase 3 (master catalog + crosswalk), in progress on `phase-3-catalog`.**

## Phase plan
- **P1** Schema (control record, persona profile, disposition rules; **all human-readable text fields are language-keyed objects, en + fr**) + **all 8 golden personas DRAFTED as separate YAML files (`status: draft`) for owner amendment and approval** + invariant test skeleton (I1–I7 stubs with definitional docstrings) + validate.py (schemas + persona-approval gate) + CI workflow + docs/METHODOLOGY.md skeleton + docs/DECISIONS.md with first entries (incl. the TypeScript-engine decision). Layer-2 assertions are authored by the project owner against approved personas before any engine code.
- **P2a–c** Extraction: C3A per SOV domain; ECSF (SEAL, factors, weights); CADA obligations.
- **P2d** Generalization pass ({NATION}/{TRUSTED_REGION}); Layer-1 I3 becomes enforceable here.
- **P3** Master catalog: crosswalk, dedup, layer tagging. Layer tagging enables I2.
- **P4** Responsibility-map builder + disposition engine (declarative YAML rules). Full Layer 1+2+3+5 suites must pass; first Layer-4 relevance review.
- **P5** Scoring (achieved/ceiling, outcome weights, evidence quality) + Layer-4 review.
- **P6** Questionnaire rendering + recommendations (clause library) + UI + Layer-4 review.
- **P7** Hardening: expand persona set from pilot feedback; every bug found in the field becomes a new assertion or differential pair before it is fixed.

## References (for recommendation grounding — cite in generated advice where apt)
- World Bank, *Government Migration to Cloud Ecosystems* (2022)
- World Bank/IFC, *Advancing Cloud and Data Infrastructure Markets: Strategic Directions for LMICs* (2024)
- World Bank blog, *Moving toward an outcome-based approach for digital sovereignty* (2026) — forthcoming WB toolkit
- African Union Data Policy Framework; Malabo Convention; AfCFTA Digital Trade Protocol
- BSI C3A v1.0 (2026); EU Cloud Sovereignty Framework v1.2.1; CADA proposal (2026)
