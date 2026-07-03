#!/usr/bin/env python3
"""Phase 2b: extracts ECSF's SOV-1..6 contributing factors (section 4 of
the source PDF) as control-record.schema.json records into
data/extracted/ecsf.json.

Source: sources/Cloud-Sovereignty-Framework.pdf (EU Cloud Sovereignty
Framework v1.2.1, Oct. 2025), read locally per D-002 (not committed).

SOV-7 (inheritance-only) and SOV-8 (out of scope) factors are captured
as metadata in ecsf-scoring.json instead (see extract_ecsf_scoring.py),
not as control records here — per CLAUDE.md and this phase's scope.

Per D-012: even though ECSF's license basis (EU Commission reuse policy)
is more permissive than C3A's, these control records go through the
same D-009/D-010 verbatim-isolation regime from the start, for pipeline
consistency: public source_text/generalized_text carry placeholders;
real verbatim text lives only in the git-ignored
data/local/ecsf-verbatim.json, keyed by record id.

criterion_type is set to "C" uniformly: ECSF's contributing factors have
no baseline/additional distinction (unlike C3A's C/AC), so "C" is used
as the schema-required value closest to "this is a baseline factor,"
documented here rather than treated as a substantive judgment call.

Run: .venv/bin/python3 scripts/extract_ecsf.py <SOV-N>
(writes every domain up to and including SOV-N, same batching pattern
as extract_c3a.py)
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "extracted" / "ecsf.json"
VERBATIM_OUT = ROOT / "data" / "local" / "ecsf-verbatim.json"

DOCUMENT = "EU Cloud Sovereignty Framework v1.2.1 (Oct. 2025)"
FR_PENDING = "FR-TRANSLATION-PENDING"
LOCAL_VERBATIM_PLACEHOLDER = "SEE-LOCAL-VERBATIM"
GENERALIZATION_PENDING_PLACEHOLDER = "GENERALIZATION-PENDING"
ALL_EVIDENCE = ["self_attested", "contractual_commitment", "third_party_certified", "independently_audited"]


def rec(id_suffix, sov_domain, factor_no, layer, page, text_en,
        needs_review=False, needs_review_note=None):
    r = {
        "id": f"csat-{id_suffix}",
        "sov_domain": sov_domain,
        "criterion_type": "C",
        "layer": layer,
        "derivation": "verbatim",
        "source_refs": [{"framework": "ECSF", "section_id": f"ECSF-§4-{sov_domain}-F{factor_no:02d}"}],
        "source_pointer": {"document": DOCUMENT, "section": f"§4 {sov_domain} factor {factor_no}", "page": page},
        "source_text": {"en": text_en, "fr": FR_PENDING},
        "generalized_text": {"en": text_en, "fr": FR_PENDING},
        "disposition_default": "assess",
        "evidence_quality_options": ALL_EVIDENCE,
        "weight": 1.0,
        "needs_review": needs_review,
    }
    if needs_review_note:
        r["needs_review_note"] = needs_review_note
    return r


SOV1 = [
    rec("sov1-ecsf-01", "SOV-1", 1, "legal_jurisdiction", 4,
        "Ensuring that bodies having decisive authority over your services are located within EU jurisdiction."),
    rec("sov1-ecsf-02", "SOV-1", 2, "legal_jurisdiction", 4,
        "Evaluating the assurances against change of control."),
    rec("sov1-ecsf-03", "SOV-1", 3, "legal_jurisdiction", 4,
        "Degree to which the provider relies on financing coming from EU sources.",
        needs_review=True,
        needs_review_note="Financing-source dependency is an ownership/economic factor, not cleanly any single "
                           "responsibility-map layer (all ten layer values describe technical-operational "
                           "responsibility, not capital structure). Tagged legal_jurisdiction as the closest fit, "
                           "consistent with how C3A's own SOV-1 criteria (effective control, ownership transparency) "
                           "were tagged in Phase 2a. Coverage: candidate uncovered factor — verify in Phase 3 "
                           "(no C3A criterion addresses financing source)."),
    rec("sov1-ecsf-04", "SOV-1", 4, "legal_jurisdiction", 4,
        "Extent of investment, jobs, and value creation within EU.",
        needs_review=True,
        needs_review_note="Same ambiguity as csat-sov1-ecsf-03: an industrial/economic factor without a clean "
                           "layer fit. Tagged legal_jurisdiction for consistency with the domain's other factors. "
                           "Coverage: candidate uncovered factor — verify in Phase 3 (no C3A criterion addresses "
                           "EU investment/jobs/value creation)."),
    rec("sov1-ecsf-05", "SOV-1", 5, "legal_jurisdiction", 4,
        "Involvement in EU initiatives, Consistency with digital, green, and industrial sovereignty objectives "
        "defined at EU level.",
        needs_review=True,
        needs_review_note="A policy-alignment factor rather than a technical responsibility-layer concern. Tagged "
                           "legal_jurisdiction as the closest available fit; no layer value captures "
                           "policy-alignment specifically. Coverage: candidate uncovered factor — verify in Phase 3 "
                           "(no C3A criterion addresses EU policy-initiative alignment)."),
    rec("sov1-ecsf-06", "SOV-1", 6, "operations_personnel", 4,
        "Ability to sustain secure operations against requests to cease or suspend the service, or if vendor "
        "support is withdrawn or disrupted.",
        needs_review=True,
        needs_review_note="Spans legal_jurisdiction (the request to cease/suspend typically originates from a "
                           "jurisdictional authority or the vendor's home-country obligations) and "
                           "operations_personnel (sustaining operations despite the disruption is an operational "
                           "continuity concern). Tagged operations_personnel as primary since the factor asks about "
                           "the government's/operator's ability to continue running the service, not about the "
                           "legal basis of the request itself."),
]

SOV2 = [
    rec("sov2-ecsf-01", "SOV-2", 1, "legal_jurisdiction", 4,
        "The national legal system governing the provider's operations and contracts."),
    rec("sov2-ecsf-02", "SOV-2", 2, "legal_jurisdiction", 4,
        "Degree of exposure to non-EU laws with cross-border reach (e.g., US CLOUD Act, Chinese Cybersecurity "
        "Law)."),
    rec("sov2-ecsf-03", "SOV-2", 3, "legal_jurisdiction", 4,
        "Existence of legal, contractual, or technical channels through which non-EU authorities could compel "
        "access to data or systems.",
        needs_review=True,
        needs_review_note="Explicitly spans legal_jurisdiction (the compulsion mechanism itself) and data/identity "
                           "(the 'technical channels' through which access would actually occur). Tagged "
                           "legal_jurisdiction as primary since the factor is framed around the existence of a "
                           "compulsion pathway, not the technical access-control mechanics."),
    rec("sov2-ecsf-04", "SOV-2", 4, "legal_jurisdiction", 4,
        "Applicability of international regimes, which may restrict usage or transfer."),
    rec("sov2-ecsf-05", "SOV-2", 5, "legal_jurisdiction", 4,
        "Location of intellectual property creation, registration, and development (EU vs. third countries), "
        "legal jurisdiction where IP is created and developed.",
        needs_review=True,
        needs_review_note="IP jurisdiction is a hybrid of legal_jurisdiction and platform/technology ownership; "
                           "tagged legal_jurisdiction since the factor's own text frames it primarily in "
                           "jurisdictional terms ('legal jurisdiction where IP is created and developed'). "
                           "Coverage: candidate uncovered factor — verify in Phase 3 (no C3A criterion addresses "
                           "IP creation/registration location)."),
]

SOV3 = [
    rec("sov3-ecsf-01", "SOV-3", 1, "data", 4,
        "Ensuring that only the customer, not the provider, has effective control over cryptographic access to "
        "their data.",
        needs_review=True,
        needs_review_note="Cryptographic key-custody control could be tagged identity (access-management layer, "
                           "per C3A's SOV-3-03 IAM convention) or data (data-protection layer, per C3A's SOV-3-01/02 "
                           "convention). Tagged data as primary since the factor centers on protecting data "
                           "confidentiality outcomes, not on IAM integration mechanics."),
    rec("sov3-ecsf-02", "SOV-3", 2, "data", 4,
        "Visibility into when, where, and by whom data is accessed, including auditability of AI model usage, "
        "mechanisms guaranteeing irreversible removal of data, with verifiable evidence.",
        needs_review=True,
        needs_review_note="Access/audit logging spans data vs. platform/operations_personnel (who operates the "
                           "logging system), mirroring the same ambiguity flagged for C3A's SOV-3-04 in Phase 2a. "
                           "Tagged data as primary since the factor's subject is data-access visibility."),
    rec("sov3-ecsf-03", "SOV-3", 3, "data", 4,
        "Strict confinement of storage and processing to European jurisdictions, with no fallback to third "
        "countries."),
    rec("sov3-ecsf-04", "SOV-3", 4, "platform", 4,
        "Extent to which AI models and data pipelines are developed, trained, hosted, and governed under EU "
        "control, minimizing dependency on non-EU technology stacks.",
        needs_review=True,
        needs_review_note="Spans platform (hosting/training infrastructure) and data (training-data provenance) "
                           "simultaneously. Tagged platform as primary since the factor centers on where/how the "
                           "AI system itself is built and run, not on the data assets it consumes. Coverage: "
                           "candidate uncovered factor — verify in Phase 3 (C3A has no AI-specific criteria)."),
]

SOV4 = [
    rec("sov4-ecsf-01", "SOV-4", 1, "platform", 5,
        "Ease of migrating workloads or integrating with alternative EU-controlled solutions without vendor "
        "lock-in."),
    rec("sov4-ecsf-02", "SOV-4", 2, "operations_personnel", 5,
        "Capacity for EU operators to manage, maintain, and support the technology without requiring non-EU "
        "vendor involvement."),
    rec("sov4-ecsf-03", "SOV-4", 3, "operations_personnel", 5,
        "Existence of an EU-based talent pool with the expertise to operate and sustain the service."),
    rec("sov4-ecsf-04", "SOV-4", 4, "operations_personnel", 5,
        "Assurance that operational support is delivered from within the EU and subject exclusively to EU legal "
        "frameworks.",
        needs_review=True,
        needs_review_note="Spans operations_personnel (support delivered from within the EU) and legal_jurisdiction "
                           "(subject exclusively to EU legal frameworks). Tagged operations_personnel as primary "
                           "since the factor is fundamentally about where support work is performed."),
    rec("sov4-ecsf-05", "SOV-4", 5, "platform", 5,
        "Availability of full technical documentation, source code, and operational know-how enabling long-term "
        "autonomy."),
    rec("sov4-ecsf-06", "SOV-4", 6, "supply_chain_services", 5,
        "Location and legal control of critical suppliers or subcontractors involved in service delivery."),
]

SOV5 = [
    rec("sov5-ecsf-01", "SOV-5", 1, "supply_chain_hardware", 5,
        "Geographic source of key physical parts, manufacturing location - countries where hardware is "
        "manufactured or assembled."),
    rec("sov5-ecsf-02", "SOV-5", 2, "supply_chain_hardware", 5,
        "Jurisdiction and provenance of embedded code controlling hardware, firmware.",
        needs_review=True,
        needs_review_note="Firmware is embedded code (software-like) but tightly bound to specific hardware. "
                           "Tagged supply_chain_hardware as primary, consistent with C3A's SOV-5-04 precedent "
                           "(D-007) of tagging hardware-adjacent embedded technology under the hardware layer; "
                           "could also be argued as supply_chain_software."),
    rec("sov5-ecsf-03", "SOV-5", 3, "supply_chain_software", 5,
        "Origin of Software: where and by whom software is architected and programmed, location and jurisdiction "
        "governing software packaging, distribution, and updates."),
    rec("sov5-ecsf-04", "SOV-5", 4, "supply_chain_services", 5,
        "Degree of reliance on non-EU vendors, facilities, or proprietary technologies.",
        needs_review=True,
        needs_review_note="Spans all three post-D-007 supply-chain layers at once: vendors/facilities (services), "
                           "facilities (hardware-adjacent), and proprietary technologies (software) — the same "
                           "multi-layer pattern flagged for C3A's SOV-5-04-C. Tagged supply_chain_services as "
                           "primary since 'reliance on vendors' is the dominant framing."),
    rec("sov5-ecsf-05", "SOV-5", 5, "supply_chain_services", 5,
        "Visibility into the entire supplier and sub-supplier chain, including audit rights."),
]

SOV6 = [
    rec("sov6-ecsf-01", "SOV-6", 1, "platform", 5,
        "Ability to integrate with other technologies through well-documented and non-proprietary APIs or "
        "protocols, extent to which the solution adheres to publicly governed and widely adopted standards, "
        "reducing dependency on single vendors.",
        needs_review=True,
        needs_review_note="Coverage: candidate uncovered factor — verify in Phase 3 (C3A's SOV-6 criteria address "
                           "source-code backup and vendor-disruption contingency, not API/protocol openness as "
                           "such; C3A's SOV-3-03-AC1 requires open standards for identity-provider integration "
                           "specifically, not a general API-openness requirement)."),
    rec("sov6-ecsf-02", "SOV-6", 2, "platform", 5,
        "Whether software is accessible under open licenses, with rights to audit, modify, and redistribute, "
        "ensuring transparency and adaptability.",
        needs_review=True,
        needs_review_note="Coverage: candidate uncovered factor — verify in Phase 3 (C3A has no criterion "
                           "requiring open-license software or audit/modify/redistribute rights)."),
    rec("sov6-ecsf-03", "SOV-6", 3, "platform", 5,
        "Visibility into the design and functioning of the service, including architectural documentation, data "
        "flows, and dependencies."),
    rec("sov6-ecsf-04", "SOV-6", 4, "supply_chain_hardware", 5,
        "Degree of EU independence in high-performance computing capabilities, including processors, "
        "accelerators, and software ecosystems.",
        needs_review=True,
        needs_review_note="Spans platform (software ecosystems) and supply_chain_hardware (processors, "
                           "accelerators). Tagged supply_chain_hardware as primary since the factor centers on "
                           "hardware/compute independence, with software ecosystems as a secondary aspect."),
]

DOMAINS = {
    "SOV-1": SOV1,
    "SOV-2": SOV2,
    "SOV-3": SOV3,
    "SOV-4": SOV4,
    "SOV-5": SOV5,
    "SOV-6": SOV6,
}


def write_through(domain_key: str) -> None:
    """Writes /data/extracted/ecsf.json (public) containing every domain up
    to and including domain_key, in DOMAINS order, plus
    data/local/ecsf-verbatim.json (git-ignored, D-009/D-010 regime applied
    from the start per D-012). Used to produce one commit's worth of
    records per Phase 2b batch.
    """
    order = list(DOMAINS.keys())
    public_records = []
    verbatim = {}
    for d in order[: order.index(domain_key) + 1]:
        for r in DOMAINS[d]:
            verbatim[r["id"]] = dict(r["source_text"])
            public = json.loads(json.dumps(r))  # deep copy
            public["source_text"] = {"en": LOCAL_VERBATIM_PLACEHOLDER, "fr": LOCAL_VERBATIM_PLACEHOLDER}
            public["generalized_text"] = {"en": GENERALIZATION_PENDING_PLACEHOLDER, "fr": GENERALIZATION_PENDING_PLACEHOLDER}
            public_records.append(public)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(public_records, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(public_records)} public records (source_text/generalized_text scrubbed) through {domain_key} -> {OUT}")

    VERBATIM_OUT.parent.mkdir(parents=True, exist_ok=True)
    VERBATIM_OUT.write_text(json.dumps(verbatim, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(verbatim)} verbatim entries -> {VERBATIM_OUT} (git-ignored, local only)")


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "SOV-6"
    write_through(target)
