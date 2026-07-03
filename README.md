# Cloud Sovereignty Assessment Tool (CSAT) — v2

A questionnaire-based assessment tool for **governments in emerging
markets** to understand and incrementally improve their cloud sovereignty
posture. The tool never judges a deployment choice as right or wrong. Its
output is a posture profile (per-domain achieved score vs. structural
ceiling) plus improvement paths ranked by effort and impact, in three
buckets: **negotiate** (contract clauses to pursue with providers),
**implement** (internal fixes within government control), and **strategic
options** (longer-horizon architectural choices, presented with
tradeoffs, never as prescriptions).

Every question, rule, and score in the tool traces to a globally
recognized source — BSI's C3A v1.0, the EU Cloud Sovereignty Framework,
and the CADA legislative proposal — with the exact citation and the
derivation tier (verbatim / generalized / derived / editorial) visible in
the rendered app. Nothing is hidden; every project judgment call is logged
in [`docs/DECISIONS.md`](docs/DECISIONS.md).

**Full project charter, design principles, scenario model, disposition
logic, scoring model, testing methodology, and phase plan:
[`CLAUDE.md`](CLAUDE.md).** That document is the source of truth for
anyone reviewing this repo — start there.

## Client-side only

This is a static web app. Assessment answers (posture, contract gaps, key
custody) are sensitive government information and never leave the user's
device — no backend, no accounts, no analytics, no external calls at
runtime. Deployable on GitHub Pages or downloadable as a zip for
offline/air-gapped use.

## Status

**Phase 1 complete** (schema, golden personas, test harness skeleton) on
branch [`phase-1-schema`](https://github.com/mattpltn/cloud-sovereignty/tree/phase-1-schema),
pending external review before merge to `main`. See
[`docs/phases/phase-1-report.md`](docs/phases/phase-1-report.md) for the
full report, open items, and CI status.

Phase progress:

| Phase | Scope | Status |
|---|---|---|
| 0 | Repo setup | Done |
| 1 | Schema, golden personas (drafted, awaiting owner approval), invariant test skeleton, validator, CI | Done — awaiting review |
| 2 | Extraction (C3A, ECSF, CADA) | Not started |
| 3 | Master catalog (crosswalk, dedup, layer tagging) | Not started |
| 4 | Responsibility-map builder + disposition engine | Not started |
| 5 | Scoring | Not started |
| 6 | Questionnaire rendering, recommendations, UI | Not started |
| 7 | Hardening | Not started |

## Repository layout

```
/sources       Framework source PDFs — held back from this public repo
               on license grounds (see docs/DECISIONS.md D-002); used
               locally for extraction.
/schema        JSON Schemas: control record, persona profile, disposition rule.
/data          Extracted + catalog control records (Phase 2+, not yet populated).
/engine        TypeScript engine (responsibility map, disposition, scoring).
               Same build runs in CI and in the browser — no ports, no
               parallel implementations.
/app           Static client-side web app (Phase 6, not yet started).
/tests
  /personas    Golden persona YAML fixtures — draft, awaiting approval.
  /invariants  Property tests (I1-I7) that must hold for any approved persona.
  /helpers     Test fixture loaders (persona-approval gate, Node side).
/docs
  METHODOLOGY.md   Written incrementally, one section per completed phase.
  DECISIONS.md     Append-only editorial decision register.
  /phases          Phase completion reports.
/scripts       validate.py (schema + persona-approval gate).
.github/workflows/ci.yml
```

## Running the validator and tests locally

The system Python on most dev machines is externally managed (PEP 668),
so validation runs inside a project-local venv:

```sh
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt
.venv/bin/python3 scripts/validate.py

npm install
npm run typecheck
npm test
```

## License

C3A is CC-BY-ND 4.0; ECSF and CADA follow EU Commission reuse policy. See
[`docs/DECISIONS.md`](docs/DECISIONS.md) D-002 for how this repo handles
source-material reproduction.
