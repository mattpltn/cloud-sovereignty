#!/usr/bin/env python3
"""Phase 2c: extracts data/extracted/cada-act.json — a hand-picked
subset of articles from the CADA proposal act itself (COM(2026) 502
final, part 1), NOT the whole regulation. Scope, per this phase's
explicit instruction: definitions; the sovereignty risk-assessment
obligations on public sector bodies; the third-country implementing-act
mechanism referenced by Annex II level 3; procurement obligations; the
open-source preference provision. Annex I (Grand Challenges) is out of
scope entirely (noted in the phase report, not extracted here).

Modeling choice (D-017, logged in docs/DECISIONS.md): these records do
NOT conform to control-record.schema.json. That schema models a
provider-facing criterion with a layer/disposition (assess/auto_answer/
inherit/suppress) — a shape built for assessing a CSP's posture. Most of
what this file captures is not that: a definition, or an obligation on
the ASSESSING GOVERNMENT itself (conduct a risk assessment; procure
only recognised UA levels; prefer open source), not on a cloud provider.
Forcing sov_domain/layer/disposition_default onto these would either be
meaningless (a definition has no disposition) or a stretch (a
government's own procedural obligation isn't "assessed" the way a
provider criterion is). No new schema is authorized for this part
either, so cada-act.json uses a small ad-hoc shape, checked structurally
by scripts/validate.py rather than against a JSON Schema file.

Each record's derivation is "derived" (CLAUDE.md tier: "restructured
from a source ... with the source passage referenced alongside") — the
obligation_text is a plain-language restatement, not a verbatim block
quote, and source_quote (where present) is a short (<16-word) anchor
phrase rather than a full reproduction, so no verbatim-isolation regime
is required for this file (unlike cada.json/cada-evidence.json).

Run: .venv/bin/python3 scripts/extract_cada_act.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "extracted" / "cada-act.json"

DOCUMENT = "COM(2026) 502 final, 3.6.2026 — Regulation part 1 (Cloud and AI Development Act proposal)"
FR_PENDING = "FR-TRANSLATION-PENDING"


def ls(en: str) -> dict:
    return {"en": en, "fr": FR_PENDING}


RECORDS = [
    {
        "id": "cada-act-def-cloud-computing-service",
        "article": "Article 2",
        "paragraph": "point (1)",
        "page": 39,
        "title": "Definition: cloud computing service",
        "obligation_text": (
            "'Cloud computing service' takes the definition already used "
            "elsewhere in EU law (Directive (EU) 2022/2555, Article 6, "
            "point (30)) rather than defining it afresh — CADA layers its "
            "assurance-level framework on top of an existing legal "
            "definition, not a new one."
        ),
        "source_quote": "'cloud computing service' means cloud computing service as defined in Article 6",
    },
    {
        "id": "cada-act-def-cloud-computing-service-provider",
        "article": "Article 2",
        "paragraph": "point (2)",
        "page": 39,
        "title": "Definition: cloud computing service provider",
        "obligation_text": "'Cloud computing service provider' means a legal entity which provides a cloud computing service — the party whose posture CADA's UA levels (Annex II) assess.",
        "source_quote": "means a legal entity which provides a cloud computing service",
    },
    {
        "id": "cada-act-def-public-sector-body",
        "article": "Article 2",
        "paragraph": "point (6)",
        "page": 40,
        "title": "Definition: public sector body",
        "obligation_text": (
            "'Public sector body' takes the definition from Directive (EU) "
            "2019/1024, Article 2, point (1) — the governments CSAT "
            "assesses are 'public sector bodies' in CADA's own terms, "
            "which is the hook for CADA's obligations on them (risk "
            "assessment, procurement) to apply."
        ),
        "source_quote": "means public sector body as defined in Article 2, point (1)",
    },
    {
        "id": "cada-act-def-union-entities",
        "article": "Article 2",
        "paragraph": "point (7)",
        "page": 39,
        "title": "Definition: Union entities",
        "obligation_text": "'Union entities' means the Union institutions, bodies, offices and agencies established under the EU treaties — distinct from 'public sector bodies' (Member State level); CADA's obligations on risk assessment and procurement (Articles 29-30) name both categories separately.",
        "needs_review": True,
        "needs_review_note": "CSAT's persona model targets national/subnational governments ('public sector bodies'); 'Union entities' (EU institutions themselves) is a distinct addressee CSAT does not currently model as a persona type. Flagged for Phase 3/owner consideration, not resolved here.",
    },
    {
        "id": "cada-act-def-control",
        "article": "Article 2",
        "paragraph": "point (21)",
        "page": 39,
        "title": "Definition: control",
        "obligation_text": (
            "'Control' takes the definition from Regulation (EU) 2021/697, "
            "Article 2, point (6) — this is the legal term of art that "
            "Annex II's 'subject to the control of a third country or a "
            "legal entity established in a third-country' criteria "
            "(assessed via Annex III criterion G) turn on."
        ),
        "source_quote": "means control as defined in Article 2, point (6)",
    },
    {
        "id": "cada-act-def-contracting-authorities",
        "article": "Article 2",
        "paragraph": "point (22)",
        "page": 39,
        "title": "Definition: contracting authorities",
        "obligation_text": "'Contracting authorities' takes the definition from Directive 2014/24/EU, Article 2(1), point (1) — the addressee of Article 30's procurement obligations.",
        "source_quote": "means contracting authorities as defined in Article 2(1), point (1)",
    },
    {
        "id": "cada-act-def-open-source-licence",
        "article": "Article 2",
        "paragraph": "point (25)",
        "page": 40,
        "title": "Definition: open source licence",
        "obligation_text": "'Open source licence' takes the definition from Regulation (EU) 2024/903, Article 2, point (12) — the term used throughout Annex II (j), Annex III criterion J, and Article 41's open-source-first obligation.",
        "source_quote": "means open source licence as defined in Article 2, point (12)",
    },
    {
        "id": "cada-act-def-audit-criteria-evidence",
        "article": "Article 2",
        "paragraph": "points (19)-(20)",
        "page": 39,
        "title": "Definitions: audit criteria, audit evidence",
        "obligation_text": (
            "'Audit criteria' means the Annex II cumulative criteria an "
            "auditing organisation assesses a provider against for UA-2/3/4 "
            "recognition; 'audit evidence' means any information an "
            "auditing organisation uses to support its findings and issue "
            "an audit opinion — the Annex III items extracted in "
            "cada-evidence.json. Directly relevant to CSAT's own "
            "evidence-quality tiering (control-record.schema.json's "
            "evidence_quality_options: self_attested < contractual_"
            "commitment < third_party_certified < independently_audited) — "
            "an 'independently_audited' evidence tier for a CADA-derived "
            "control corresponds to a positive UA-2/3/4 audit opinion under "
            "this mechanism."
        ),
    },
    {
        "id": "cada-act-art18-associated-third-countries",
        "article": "Article 18",
        "paragraph": None,
        "page": 54,
        "title": "Associated third countries (the operative third-country adequacy mechanism)",
        "obligation_text": (
            "The Commission may, by implementing act, designate third "
            "countries whose control over a cloud computing service "
            "provider does not disqualify that provider from UA-3 audit, "
            "provided the third country meets six cumulative conditions "
            "(GDPR adequacy decision; no measures conflicting with lawful-"
            "access safeguards in Regulation (EU) 2023/2854 Article 32(2)-"
            "(3); no power to compel service disruption or sanctions "
            "compliance; no impediment to state-of-the-art technology "
            "provision; an open market to EU cloud services; reciprocal "
            "procurement access for EU providers). This is the article "
            "that substantively implements what Annex II 3.1(g) calls 'an "
            "implementing act under Article 19' — see the citation "
            "discrepancy noted below and in csat-sov1-cada-ua3-g's "
            "needs_review_note (data/extracted/cada.json)."
        ),
        "needs_review": True,
        "needs_review_note": (
            "Annex II 3.1(g) and Annex III criterion G's 7.2(c) both cite "
            "'an implementing act under Article 19' for this third-country "
            "adequacy mechanism, but Article 19 in this draft is titled "
            "'Conformity self-assessment' (the UA-1 self-assessment "
            "procedure) and does not describe implementing acts on "
            "third countries at all — Article 18 ('Associated third "
            "countries') is what substantively matches. Likely a "
            "cross-reference/numbering error in this draft (COM(2026) 502 "
            "final part 1 as extracted); captured as a discrepancy, not "
            "silently corrected. Verify against a later consolidated text."
        ),
    },
    {
        "id": "cada-act-art19-conformity-self-assessment",
        "article": "Article 19",
        "paragraph": None,
        "page": 55,
        "title": "Conformity self-assessment (UA-1)",
        "obligation_text": (
            "Every cloud computing service provider seeking UA-1 "
            "recognition self-assesses against Annex II's UA-1 criteria "
            "and issues a public EU statement of conformity, assuming "
            "responsibility for its accuracy. Unlike UA-2/3/4 (independent "
            "third-party audit, Article 20), UA-1 relies entirely on "
            "provider self-attestation — directly relevant to CSAT's "
            "evidence-quality tiering: a UA-1 statement of conformity is "
            "'self_attested' evidence, structurally weaker than a UA-2/3/4 "
            "audit opinion ('independently_audited')."
        ),
    },
    {
        "id": "cada-act-art29-risk-assessments",
        "article": "Article 29",
        "paragraph": None,
        "page": 61,
        "title": "Risk assessment obligation on Member States and Union entities",
        "obligation_text": (
            "Member States and Union entities must periodically (at least "
            "every two years) identify which public sector activities use "
            "or will use cloud computing services in public-order-sensitive "
            "sectors (per Directive (EU) 2022/2555 Annexes I/II, plus "
            "national security, internal security, border management, "
            "defence, justice, law enforcement), and determine which UA "
            "level (2, 3, or 4) is appropriate for each. The risk "
            "assessment must weigh data sensitivity/criticality, the risk "
            "of unlawful third-country access, and the risk of service "
            "disruption, and must consider whether a multi-vendor/"
            "multi-cloud strategy is appropriate. Results go to the "
            "Commission; a Commission-specified methodology governs how "
            "the highest assurance level is applied to the most critical "
            "activities (defence named explicitly). Where a risk "
            "assessment requires migrating to a different cloud service, "
            "migration must complete within 12 months. This is the direct "
            "analogue of CSAT's own workload-classification-tiering design "
            "principle (CLAUDE.md: 'Classification tiering' — one "
            "government, several per-tier assessments)."
        ),
        "source_quote": "Member States and Union entities shall carry out risk assessments",
    },
    {
        "id": "cada-act-art30-public-procurement",
        "article": "Article 30",
        "paragraph": None,
        "page": 63,
        "title": "Public procurement obligations",
        "obligation_text": (
            "Contracting authorities (and Union entities procuring for "
            "their own exclusive use) whose activities were NOT identified "
            "under Article 29's risk assessment as public-order-sensitive "
            "must use only cloud computing services recognised at UA-1 or "
            "above. Contracting authorities whose activities WERE so "
            "identified must use only services recognised at UA-2, UA-3, "
            "or UA-4. A narrow derogation permits procuring an unrecognised "
            "service on an exceptional, justified basis: no recognised "
            "service can meet the tender's subject matter and no reasonable "
            "alternative exists (and this absence isn't the result of an "
            "artificially narrow tender); or a prior similar tender drew no "
            "suitable bids; or compliance would require disproportionate "
            "cost."
        ),
        "source_quote": "shall use cloud computing services that have been recognised",
    },
    {
        "id": "cada-act-art41-open-source-first",
        "article": "Article 41",
        "paragraph": None,
        "page": 70,
        "title": "Open-source-first preference",
        "obligation_text": (
            "The Union and Member States must take necessary measures to "
            "encourage Union entities and public sector bodies to use and "
            "facilitate reuse of open standards and open-source-licensed "
            "components when building their cloud/AI ecosystem or stack, "
            "weighing functionality (including security), total cost, and "
            "other duly justified objective criteria — a preference, not a "
            "mandate, and explicitly balanced against functional/cost "
            "criteria rather than absolute. Directly grounds CSAT's SOV-6 "
            "(Technology Sovereignty) domain and the World Bank "
            "outcome-based framing CLAUDE.md requires recommendation text "
            "to speak (lock-in avoidance as one weighable outcome among "
            "several, not an automatic 'move to open source' directive)."
        ),
        "source_quote": "shall take the necessary measures to encourage Union entities",
    },
]


def main() -> None:
    records = []
    for r in RECORDS:
        rec = {
            "id": r["id"],
            "derivation": "derived",
            "source_refs": [
                {
                    "framework": "CADA",
                    "section_id": f"CADA-{r['article'].replace(' ', '-')}"
                    + (f"-{r['paragraph']}" if r.get("paragraph") else ""),
                    "status": "proposed_legislation",
                }
            ],
            "title": ls(r["title"]),
            "obligation_text": ls(r["obligation_text"]),
            "source_pointer": {
                "document": DOCUMENT,
                "section": f"{r['article']}" + (f", {r['paragraph']}" if r.get("paragraph") else ""),
                "page": r["page"],
            },
            "needs_review": r.get("needs_review", False),
        }
        if "source_quote" in r:
            rec["source_quote"] = ls(r["source_quote"])
        if r.get("needs_review"):
            rec["needs_review_note"] = r["needs_review_note"]
        records.append(rec)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(records)} act records -> {OUT}")


if __name__ == "__main__":
    main()
