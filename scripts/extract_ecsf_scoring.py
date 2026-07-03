#!/usr/bin/env python3
"""Phase 2b: extracts the ECSF SEAL scale, domain definitions, official
weights, and scoring formula into data/extracted/ecsf-scoring.json,
conforming to schema/ecsf-scoring.schema.json.

Source: sources/Cloud-Sovereignty-Framework.pdf (EU Cloud Sovereignty
Framework v1.2.1, Oct. 2025), read locally per D-002 (not committed).

Unlike C3A, ECSF text is not scrubbed to a placeholder here: ECSF follows
EU Commission reuse policy, not CC-BY-ND (see D-012). Only the SOV-1..6
contributing factors extracted as control records (ecsf.json) go through
the D-009/D-010 verbatim-isolation regime, per explicit instruction, for
consistency with the established provenance pipeline pending any future
divergence in how the two frameworks' licenses are actually treated.

Run: .venv/bin/python3 scripts/extract_ecsf_scoring.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "extracted" / "ecsf-scoring.json"

DOCUMENT = "EU Cloud Sovereignty Framework v1.2.1 (Oct. 2025)"
FR_PENDING = "FR-TRANSLATION-PENDING"


def ls(en: str) -> dict:
    """lang-string helper: fr always FR-TRANSLATION-PENDING (D-006)."""
    return {"en": en, "fr": FR_PENDING}


def sp(section: str, page: int) -> dict:
    return {"document": DOCUMENT, "section": section, "page": page}


SEAL_LEVELS = [
    {
        "level": 0,
        "label": ls("No Sovereignty"),
        "description": ls(
            "Service, technology or operations under exclusive control of "
            "non-EU third parties, governed entirely in non-EU jurisdictions."
        ),
        "source_pointer": sp("ECSF §3 SEAL-0", 3),
    },
    {
        "level": 1,
        "label": ls("Jurisdictional Sovereignty"),
        "description": ls(
            "EU law formally applies with limited practical enforceability; "
            "service, technology or operations under exclusive control of "
            "non-EU third parties."
        ),
        "source_pointer": sp("ECSF §3 SEAL-1", 3),
    },
    {
        "level": 2,
        "label": ls("Data Sovereignty"),
        "description": ls(
            "EU law applicable and enforceable, with material non-EU "
            "dependencies remaining; service, technology or operations "
            "under indirect control of non-EU third parties."
        ),
        "source_pointer": sp("ECSF §3 SEAL-2", 3),
    },
    {
        "level": 3,
        "label": ls("Digital Resilience"),
        "description": ls(
            "EU law applicable and enforceable, EU actors exercising "
            "meaningful but not full influence; service, technology or "
            "operations under marginal control of non-EU third parties."
        ),
        "source_pointer": sp("ECSF §3 SEAL-3", 3),
    },
    {
        "level": 4,
        "label": ls("Full Digital Sovereignty"),
        "description": ls(
            "Technology and operations under complete EU control, subject "
            "only to EU law, with no critical non-EU dependencies."
        ),
        "source_pointer": sp("ECSF §3 SEAL-4", 3),
    },
]

DOMAINS = [
    {
        "id": "SOV-1",
        "label": ls("Strategic Sovereignty"),
        "description": ls(
            "Strategic sovereignty captures the degree to which the services "
            "of a cloud provider (or technology actor) are anchored within "
            "the European Union legal, financial, and industrial ecosystem. "
            "It assesses ownership stability, governance influence, and "
            "alignment with EU strategic priorities."
        ),
        "weight_percent": 15,
        "scope": "assessed",
        "factors": [
            ls("Ensuring that bodies having decisive authority over your services are located within EU jurisdiction."),
            ls("Evaluating the assurances against change of control."),
            ls("Degree to which the provider relies on financing coming from EU sources."),
            ls("Extent of investment, jobs, and value creation within EU."),
            ls("Involvement in EU initiatives, Consistency with digital, green, and industrial sovereignty objectives defined at EU level."),
            ls("Ability to sustain secure operations against requests to cease or suspend the service, or if vendor support is withdrawn or disrupted."),
        ],
        "source_pointer": sp("ECSF §2/§4 SOV-1", 2),
    },
    {
        "id": "SOV-2",
        "label": ls("Legal & Jurisdictional Sovereignty"),
        "description": ls(
            "Legal & Jurisdictional sovereignty evaluates the legal "
            "environment, exposure to foreign authority, and enforceability "
            "of rights that govern the services of a technology provider. It "
            "determines the extent to which the services are anchored in "
            "European jurisdiction and insulated from external legal claims."
        ),
        "weight_percent": 10,
        "scope": "assessed",
        "factors": [
            ls("The national legal system governing the provider's operations and contracts."),
            ls("Degree of exposure to non-EU laws with cross-border reach (e.g., US CLOUD Act, Chinese Cybersecurity Law)."),
            ls("Existence of legal, contractual, or technical channels through which non-EU authorities could compel access to data or systems."),
            ls("Applicability of international regimes, which may restrict usage or transfer."),
            ls("Location of intellectual property creation, registration, and development (EU vs. third countries), legal jurisdiction where IP is created and developed."),
        ],
        "source_pointer": sp("ECSF §2/§4 SOV-2", 2),
    },
    {
        "id": "SOV-3",
        "label": ls("Data & AI Sovereignty"),
        "description": ls(
            "Data & AI sovereignty focuses on the protection, control, and "
            "independence of data assets and AI services within the EU. It "
            "addresses how data is secured, where it is processed, and the "
            "degree of autonomy customers retain over AI capabilities."
        ),
        "weight_percent": 10,
        "scope": "assessed",
        "factors": [
            ls("Ensuring that only the customer, not the provider, has effective control over cryptographic access to their data."),
            ls("Visibility into when, where, and by whom data is accessed, including auditability of AI model usage, mechanisms guaranteeing irreversible removal of data, with verifiable evidence."),
            ls("Strict confinement of storage and processing to European jurisdictions, with no fallback to third countries."),
            ls("Extent to which AI models and data pipelines are developed, trained, hosted, and governed under EU control, minimizing dependency on non-EU technology stacks."),
        ],
        "source_pointer": sp("ECSF §2/§4 SOV-3", 2),
    },
    {
        "id": "SOV-4",
        "label": ls("Operational Sovereignty"),
        "description": ls(
            "Operational sovereignty measures the practical ability of EU "
            "actors to run, support, and evolve a technology independently "
            "of foreign control. It focuses on continuity of operations, "
            "skill availability, and resilience against external "
            "dependencies."
        ),
        "weight_percent": 15,
        "scope": "assessed",
        "factors": [
            ls("Ease of migrating workloads or integrating with alternative EU-controlled solutions without vendor lock-in."),
            ls("Capacity for EU operators to manage, maintain, and support the technology without requiring non-EU vendor involvement."),
            ls("Existence of an EU-based talent pool with the expertise to operate and sustain the service."),
            ls("Assurance that operational support is delivered from within the EU and subject exclusively to EU legal frameworks."),
            ls("Availability of full technical documentation, source code, and operational know-how enabling long-term autonomy."),
            ls("Location and legal control of critical suppliers or subcontractors involved in service delivery."),
        ],
        "source_pointer": sp("ECSF §2/§4 SOV-4", 3),
    },
    {
        "id": "SOV-5",
        "label": ls("Supply Chain Sovereignty"),
        "description": ls(
            "Supply chain sovereignty evaluates the geographic origin, "
            "transparency, and resilience of the technology supply chain, "
            "focusing on the extent to which critical components and "
            "processes remain under EU control or exposed to non-EU "
            "dependencies."
        ),
        "weight_percent": 20,
        "scope": "assessed",
        "factors": [
            ls("Geographic source of key physical parts, manufacturing location - countries where hardware is manufactured or assembled."),
            ls("Jurisdiction and provenance of embedded code controlling hardware, firmware."),
            ls("Origin of Software: where and by whom software is architected and programmed, location and jurisdiction governing software packaging, distribution, and updates."),
            ls("Degree of reliance on non-EU vendors, facilities, or proprietary technologies."),
            ls("Visibility into the entire supplier and sub-supplier chain, including audit rights."),
        ],
        "source_pointer": sp("ECSF §2/§4 SOV-5", 3),
    },
    {
        "id": "SOV-6",
        "label": ls("Technology Sovereignty"),
        "description": ls(
            "Technology sovereignty evaluates the degree of openness, "
            "transparency, and independence in the underlying technological "
            "stack, ensuring EU actors can interoperate, audit, and evolve "
            "solutions without lock-in to foreign proprietary systems."
        ),
        "weight_percent": 15,
        "scope": "assessed",
        "factors": [
            ls("Ability to integrate with other technologies through well-documented and non-proprietary APIs or protocols, extent to which the solution adheres to publicly governed and widely adopted standards, reducing dependency on single vendors."),
            ls("Whether software is accessible under open licenses, with rights to audit, modify, and redistribute, ensuring transparency and adaptability."),
            ls("Visibility into the design and functioning of the service, including architectural documentation, data flows, and dependencies."),
            ls("Degree of EU independence in high-performance computing capabilities, including processors, accelerators, and software ecosystems."),
        ],
        "source_pointer": sp("ECSF §2/§4 SOV-6", 3),
    },
    {
        "id": "SOV-7",
        "label": ls("Security & Compliance Sovereignty"),
        "description": ls(
            "Security & Compliance sovereignty measures the extent to "
            "which security operations, compliance obligations, and "
            "resilience measures are controlled within the EU, ensuring "
            "independence from foreign jurisdictions and long-term "
            "operational assurance."
        ),
        "weight_percent": 10,
        "scope": "inheritance_only",
        "factors": [
            ls("Attainment of EU and internationally recognized certifications (e.g., ISO, ENISA schemes)."),
            ls("Adherence to GDPR, NIS2, DORA, and other EU frameworks."),
            ls("Security Operations Centres and response teams operating exclusively under EU jurisdiction, control over security monitoring/logging - customer or EU authority ability to oversee logs, alerts, and monitoring functions directly."),
            ls("Transparent, timely, and EU-compliant reporting of breaches or vulnerabilities, maintenance Autonomy - ability to develop, test, and apply security patches independently of non-EU vendors."),
            ls("Capacity for EU entities to perform independent security and compliance audits with full access."),
        ],
        "source_pointer": sp("ECSF §2/§4 SOV-7", 3),
    },
    {
        "id": "SOV-8",
        "label": ls("Environmental Sustainability"),
        "description": ls(
            "Environmental sustainability assesses autonomy and resilience "
            "of cloud services over the long term in relation to energy "
            "usage, dependency and raw material scarcity."
        ),
        "weight_percent": 5,
        "scope": "out_of_scope",
        "source_pointer": sp("ECSF §2/§4 SOV-8", 3),
    },
]

SCORING_FORMULA = {
    "description": ls(
        "The Sovereignty Score is the weighted sum, across all 8 "
        "Sovereignty Objectives (SOV-1..SOV-8), of each objective's "
        "achieved score divided by its maximum possible score, multiplied "
        "by that objective's official weight (see domains[].weight_percent, "
        "which sum to 100%)."
    ),
    "source_text": ls(
        "Sovereignty Score = sum over n=1..8 of "
        "[Score(SOVn) / Max. Score(SOVn)] x Weight(SOVn) %"
    ),
    "source_pointer": sp("ECSF §5", 6),
}


def main() -> None:
    data = {
        "document": DOCUMENT,
        "version": "1.2.1",
        "seal_levels": SEAL_LEVELS,
        "domains": DOMAINS,
        "scoring_formula": SCORING_FORMULA,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote ecsf-scoring.json -> {OUT}")


if __name__ == "__main__":
    main()
