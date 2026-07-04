#!/usr/bin/env python3
"""Phase 2c: extracts CADA proposal Annex II (Union assurance level
criteria) into data/extracted/cada.json, as control-record.schema.json
records, derivation: verbatim, status: proposed_legislation.

Annex II defines four cumulative Union assurance levels (UA-1..UA-4).
UA-1 is self-assessed (Article 19) and has its own 7-letter criteria set
(a)-(g), substantively distinct from UA-2/UA-3/UA-4's shared 11-letter
scheme (a)-(k) (those three levels are audited, Article 20, and each
higher level's audited provider must also meet every lower level's
criteria per Article 20(1) — but the printed text of each letter still
repeats with level-specific deltas rather than being defined once, so
each level's own wording is captured verbatim and separately, per this
phase's explicit instruction: "do NOT dedupe across levels, that's Phase
3"). Numbered sub-criteria (e.g. 2.1(g) i-iv) are kept as part of the
same record's single verbatim text block (the source itself prints them
as a continuation of the lettered clause, not as separate top-level
provisions), rather than introducing a new nested schema field beyond
the one authorized addition (assurance_level) — a schema-fit choice,
documented in METHODOLOGY.md, analogous to Phase 2b's criterion_type="C"
choice for ECSF.

Verbatim-isolation regime (D-009/D-010) from the start:
data/local/cada-verbatim.json (git-ignored).

Run: .venv/bin/python3 scripts/extract_cada.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_PUBLIC = ROOT / "data" / "extracted" / "cada.json"
OUT_LOCAL = ROOT / "data" / "local" / "cada-verbatim.json"

DOCUMENT = "COM(2026) 502 final, 3.6.2026 — Annexes 1 to 3 (Cloud and AI Development Act proposal)"
FR_PENDING = "FR-TRANSLATION-PENDING"
LOCAL_VERBATIM_PLACEHOLDER = "SEE-LOCAL-VERBATIM"

ALL_EVIDENCE = ["self_attested", "contractual_commitment", "third_party_certified", "independently_audited"]

# Per-letter (sov_domain, layer, needs_review_note or None). UA-1's
# 7-letter scheme is substantively distinct from UA-2/3/4's shared
# 11-letter scheme (see module docstring), so each is mapped separately.
# Domain/layer choices follow the precedent set in Phase 2a's own C3A
# layer tagging (SOV-1/SOV-2 content -> legal_jurisdiction;
# SOV-5/SOV-6 -> supply_chain_*/platform, checked directly against
# data/extracted/c3a.json on this branch).
UA1_MAP = {
    "a": ("SOV-2", "legal_jurisdiction", None),
    "b": ("SOV-2", "facility", "Criterion covers infrastructure and assets location only (not personnel, unlike the UA-2/3/4 equivalent); tagged facility, but the location concern is fundamentally about jurisdictional reach, so SOV-2 vs. a facility-specific domain framing is a judgment call."),
    "c": ("SOV-3", "data", None),
    "d": ("SOV-4", "operations_personnel", "Could plausibly be tagged SOV-5/supply_chain_services instead (the criterion is about outsourcing arrangements to third-party providers); tagged SOV-4 since the substance is about preserving the provider's own operational autonomy."),
    "e": ("SOV-7", "platform", "SOV-7 is inheritance-only (CLAUDE.md) and the ten-value layer taxonomy has no SOV-7-specific option; 'platform' chosen as the closest generic fit. disposition_default set to inherit rather than assess, matching the project-wide SOV-7 treatment."),
    "f": ("SOV-5", "supply_chain_services", None),
    "g": ("SOV-2", "legal_jurisdiction", None),
}

UA_SHARED_MAP = {
    "a": ("SOV-2", "legal_jurisdiction", None),
    "b": ("SOV-2", "facility", "Criterion spans infrastructure/assets (facility) and personnel (operations_personnel) location in a single clause; tagged facility as the criterion's primary framing, but this is a genuine either/or."),
    "c": ("SOV-3", "data", None),
    "d": ("SOV-4", "operations_personnel", None),
    "e": ("SOV-7", "platform", "SOV-7 is inheritance-only (CLAUDE.md) and the ten-value layer taxonomy has no SOV-7-specific option; 'platform' chosen as the closest generic fit. disposition_default set to inherit rather than assess, matching the project-wide SOV-7 treatment."),
    "f": ("SOV-3", "data", None),
    "g": ("SOV-1", "legal_jurisdiction", "Third-country control/ownership test combines SOV-1 (strategic ownership/control, the defining concept — 'subject to the control of') and SOV-2 (jurisdictional exposure, the mechanism); tagged SOV-1 for consistency with ECSF's own 'Change of Control Risk' factor (csat-sov1-ecsf-02)."),
    "h": ("SOV-4", "operations_personnel", None),
    "i": ("SOV-5", "supply_chain_software", None),
    "j": ("SOV-6", "platform", None),
    "k": ("SOV-2", "legal_jurisdiction", None),
}

UA1_TEXT = {
    "a": "the cloud computing service provider is established in the Union.",
    "b": (
        "the infrastructure and assets of the cloud computing service provider, "
        "including those of its subcontractors which are involved in the "
        "provision of the service, are located in the Union unless the public "
        "sector body explicitly requires otherwise."
    ),
    "c": (
        "the customer data, including metadata and telemetry data, that is "
        "processed, stored and transferred by the cloud computing service "
        "provider, and by the subcontractors, which are involved in the "
        "provision of the service, remain exclusively within the Union, unless "
        "the public sector body explicitly requires otherwise and at any time, "
        "including before, during or after the configuration or use of the "
        "service."
    ),
    "d": (
        "where the cloud computing service provider outsources the technical "
        "and operational support or assistance, including any subsequent "
        "sub-outsourcing arrangements, to third-party service providers "
        "outside of the Union, the necessary legal, technical and "
        "organisational measures are implemented to ensure traceability, "
        "security and governance of those operations and those operations do "
        "not, in any way, compromise the operational autonomy of the cloud "
        "computing service provider."
    ),
    "e": "the cloud computing service provider demonstrates that the service complies with the state-of-the-art cybersecurity standards.",
    "f": (
        "the cloud computing service provider provides full transparency "
        "around the use of subcontractors. The cloud computing service "
        "provider subjects subcontractors to due diligence, contractual "
        "obligations and ongoing oversight to meet Union legal obligations."
    ),
    "g": (
        "Where the cloud computing service provider is subject to the control "
        "of a third country or a legal entity established in a third-country, "
        "the cloud computing service provider guarantees that there are no "
        "existing laws and practices in that third country, demonstrated by "
        "independent sources, that require the cloud computing service "
        "provider to report information on software vulnerabilities to "
        "authorities of that third country prior to those vulnerabilities "
        "being known to have been exploited."
    ),
}

UA2_TEXT = {
    "a": "the audited provider and the subcontractors which are involved in the provision of the audited service are established in the Union.",
    "b": (
        "the infrastructure, assets, and personnel of the audited provider, "
        "including those of its subcontractors which are involved in the "
        "provision of the service are located in the Union."
    ),
    "c": (
        "the customer data, including metadata and telemetry data, that is "
        "processed, stored and transferred by the audited provider and the "
        "subcontractors which are involved in the provision of the service, "
        "remain exclusively within the Union, unless the public sector body "
        "explicitly requires otherwise and at any time, including before, "
        "during or after the configuration or use of the service."
    ),
    "d": (
        "if the public sector body determines that imposing additional "
        "personnel screening and Union citizenship requirements are "
        "necessary, the audited provider should ensure that presonnel "
        "meeting those requirements are available."
    ),
    "e": (
        "the audited service obtains a European cybersecurity certificate of "
        "at least assurance level 'substantial' under a European "
        "cybersecurity certification scheme covering cloud computing "
        "services to be established under Regulation (EU) 2019/881, provided "
        "that such a scheme has been established under that Regulation and "
        "is available to cloud computing service providers. Until the "
        "establishment of such a scheme, national cybersecurity "
        "certification schemes shall apply, where they exist. Where no "
        "Union or national cybersecurity certification schemes exist, the "
        "audited provider is to demonstrate that the service complies with "
        "the highest cybersecurity standards under applicable Union law."
    ),
    "f": (
        "the data generated by using the audited service are not used to "
        "train or fine-tune any AI system operated by a third country or a "
        "legal entity established in a third-country, and are not "
        "transferred outside the Union in any case."
    ),
    "g": (
        "if the audited provider and the subcontractors which are involved "
        "in the provision of the audited service are subject to the control "
        "of a third country or a legal entity established in a third-country, "
        "they demonstrate that the necessary legal, technical and "
        "organisational measures have been implemented to ensure that the: "
        "i. control of the third country or the legal entity established in "
        "a third-country over the audited provider is not exercised in a "
        "manner that restrains or restricts the provider's ability to "
        "perform and deliver the service, imposes limitations on the "
        "infrastructure, assets, and personnel required for the service "
        "provision, or undermines the capabilities and standards necessary "
        "to perform the audited service; ii. access by a third country or by "
        "a legal entity established in a third-country to customer data is "
        "prevented; iii. possibility of disruption of the service continuity "
        "and/or the degradation of the service quality by a third country or "
        "a legal entity established in a third country is prevented; iv. "
        "control of the third country or the legal entity established in a "
        "third-country over the audited provider is not exercised in a "
        "manner that obliges the audited provider to implement, enforce, "
        "give effect to, or comply with restrictive measures such as "
        "sanction regimes, embargoes, or any equivalent legal or "
        "administrative measures adopted by a third country, unless such "
        "measures are legitimate under the national laws of Member States or "
        "Union law."
    ),
    "h": (
        "the technical and operational support or assistance related to the "
        "audited service, including subsequent sub-outsourcing arrangements, "
        "are initiated and performed exclusively within the Union."
    ),
    "i": (
        "the audited provider demonstrates that the following software "
        "supply chain measures are in place: i. a complete and up-to-date "
        "software bill of materials (SBOM), as defined in Article 3, point "
        "(39), of Regulation (EU) 2024/2847, and a list of identified "
        "dependencies relevant to the provision of the service are "
        "documented and made available to the auditing organisation; ii. "
        "where software components as defined in Regulation (EU) 2024/2847 "
        "Article 3, point 6 or products are provided, owned, and licensed by "
        "a legal entity established in a third country, controls are "
        "implemented and documented to block any remote features that could "
        "materially tamper with or disrupt a device, system, or software "
        "(including during updates) and to ensure that the security-relevant "
        "components from third-country software manufacturers, as defined in "
        "Regulation (EU) 2024/2847 Article 3, point 13, are subject to "
        "source code audits, and have a documented migration plan in the "
        "event that the vendor fails or a third country imposes "
        "restrictions; iii. where the cloud computing service provider is "
        "subject to the control of a third country or a legal entity "
        "established in a third-country, the cloud computing service "
        "provider guarantees that there are no existing laws and practices "
        "in that third country, demonstrated by independent sources, that "
        "require the cloud computing service provider to report information "
        "on software vulnerabilities to authorities of that third country "
        "prior to those vulnerabilities being known to have been exploited."
    ),
    "j": (
        "where software released under an open-source licence is used for "
        "the provision of the service, the audited provider demonstrates "
        "that it has implemented and documented the appropriate controls to "
        "prevent the use of any remote features or mechanisms that could be "
        "used to materially tamper with or disrupt a device, system, or "
        "software."
    ),
    "k": (
        "to the extent that the audited provider provides its services "
        "globally and maintains a subsidiary in a third country, the audited "
        "provider has implemented the necessary measures to ensure and "
        "enforce the effective legal, technical and organisational "
        "separation between the Union parent company and any such "
        "third-country subsidiary."
    ),
}

UA3_TEXT = {
    "a": "the audited provider and the subcontractors which are involved in the provision of the audited service are established in the Union.",
    "b": (
        "the infrastructure, assets, and personnel of the audited provider, "
        "including those of the subcontractors which are involved in the "
        "provision of the service, are located in the Union."
    ),
    "c": (
        "the customer data, including metadata and telemetry data, that is "
        "processed, stored and transferred by the audited provider and the "
        "subcontractors which are involved in the provision of the service, "
        "remain exclusively within the Union unless the public sector body "
        "explicitly requires otherwise and at any time, including before, "
        "during or after the configuration or use of the service."
    ),
    "d": (
        "the personnel, including the personnel of the subcontractors which "
        "are involved in the provision of the audited service are Union "
        "citizens and where appropriate, the personnel must also have the "
        "necessary national security clearance issued by a Member State when "
        "handling classified information, as defined in Article 2, point "
        "(21), of Regulation (EU) 2021/697."
    ),
    "e": UA2_TEXT["e"],
    "f": (
        "the data generated by using the audited service are not used to "
        "train or fine-tune any AI system operated by a third country or a "
        "legal entity established in a third-country and are not "
        "transferred outside the Union in any case."
    ),
    "g": (
        "the audited provider and the subcontractors which are involved in "
        "the provision of the audited service are not subject to the control "
        "of a third country or a legal entity established in a third-"
        "country. By way of derogation to this criterion, a cloud computing "
        "service provider and its subcontractors which are involved in the "
        "provision of the audited service that are subject to the control of "
        "a third country or a legal entity established in a third-country "
        "may be audited for Union assurance level 3 where the Commission has "
        "adopted an implementing act under Article 19. Where the Commission "
        "has adopted an implementing act under Article 19, the audited "
        "provider and the subcontractors which are involved in the provision "
        "of the audited service must also demonstrate that the necessary "
        "legal, technical and organisational measures have been implemented "
        "to ensure that the: i. control of the third country or the legal "
        "entity established in a third-country over the audited provider is "
        "not exercised in a manner that restrains or restricts the "
        "provider's ability to perform and deliver the service, imposes "
        "limitations on the infrastructure, assets, and personnel required "
        "for the service provision, or undermines the capabilities and "
        "standards necessary to perform the audited service. The audited "
        "provider should allow for reasonable access to the code; ii. access "
        "by a third country or by a legal entity established in a "
        "third-country to customer data is prevented; iii. possibility of "
        "disruption of the service continuity and/or the degradation of the "
        "service quality by a third country or a legal entity established in "
        "a third country is prevented; iv. control of the third country or "
        "the legal entity established in a third-country over the audited "
        "provider is not exercised in a manner that obliges the audited "
        "provider to implement, enforce, give effect to, or comply with "
        "restrictive measures such as sanction regimes, embargoes, or any "
        "equivalent legal or administrative measures adopted by a third "
        "country, unless such measures are legitimate under the national "
        "laws of Member States or Union law."
    ),
    "h": (
        "the technical and operational support or assistance related to the "
        "audited service, including subsequent sub-outsourcing arrangements, "
        "are initiated and performed exclusively within the Union, by "
        "personnel that are Union residents, and by third parties that are "
        "not subject to the control of a third country or a legal entity "
        "established in a third country."
    ),
    "i": (
        "the audited provider demonstrates that the following software "
        "supply chain measures are in place: i. a complete and up-to-date "
        "SBOM and a list of identified dependencies relevant to the "
        "provision of the service are documented and made available to the "
        "auditing organisation; ii. where software components or products "
        "are provided, owned, and licensed by a legal entity established in "
        "a third country, controls are implemented and documented to block "
        "any remote features that could materially tamper with or disrupt a "
        "device, system, or software (including during updates) and to "
        "ensure that the security-relevant components from third-country "
        "manufacturers are subject to source code audits, and have a "
        "documented migration plan in the event that the vendor fails or a "
        "third country imposes restrictions; iii. where the cloud computing "
        "service provider is subject to the control of a third country or a "
        "legal entity established in a third-country, the cloud computing "
        "service provider guarantees that there are no existing laws and "
        "practices in that third country, demonstrated by independent "
        "sources, that require the cloud computing service provider to "
        "report information on software vulnerabilities to authorities of "
        "that third country prior to those vulnerabilities being known to "
        "have been exploited."
    ),
    "j": UA2_TEXT["j"],
    "k": (
        "to the extent that the audited provider provides its services "
        "outside of the Union and maintains a subsidiary in a third country, "
        "the audited provider demonstrates that it has implemented the "
        "necessary measures to ensure and enforce the effective legal, "
        "technical and organisational separation between the Union parent "
        "company and any such third-country subsidiary."
    ),
}

UA4_TEXT = {
    "a": "the audited provider and the subcontractors which are involved in the provision of the audited service are established in the Union.",
    "b": (
        "the infrastructure, assets, and personnel of the audited provider, "
        "including the subcontractors, which are involved in the provision "
        "of the service, are located in the Union."
    ),
    "c": (
        "the customer data, including metadata and telemetry data, which, "
        "following a risk assessment, is identified as sensitive, that is "
        "processed, stored and transferred by the audited provider and the "
        "subcontractors which are involved in the provision of the service, "
        "remain exclusively within the Union and at any time, including "
        "before, during or after the configuration or use of the service."
    ),
    "d": (
        "the personnel, including the personnel of the subcontractors, "
        "which are involved in the provision of the audited service are "
        "Union citizens and, where appropriate, the personnel must also have "
        "the necessary national security clearance issued by a Member State "
        "when handling classified information."
    ),
    "e": (
        "the audited service obtains a European cybersecurity certificate "
        "of at least assurance level 'high' under a European cybersecurity "
        "certification scheme covering cloud computing services to be "
        "established under Regulation (EU) 2019/881, provided that such a "
        "scheme has been established under that Regulation and is available "
        "to cloud computing service providers. Until the establishment of "
        "such a scheme, national cybersecurity certification schemes shall "
        "apply, where they exist. Where no Union or national cybersecurity "
        "certification schemes exist, the audited provider is to "
        "demonstrate that the service complies with the highest "
        "cybersecurity standards under applicable Union law."
    ),
    "f": UA2_TEXT["f"],
    "g": "the audited provider and the subcontractors which are involved in the provision of the audited service are not subject to the control of a third country or a legal entity established in a third-country.",
    "h": UA3_TEXT["h"],
    "i": (
        "the audited provider demonstrates that the following software "
        "supply chain measures are in place: i. a complete and up-to-date "
        "SBOM and a list of identified dependencies relevant to the "
        "provision of the service are documented and made available to the "
        "auditing organisation; ii. measures in place to retain effective "
        "control over the software components or products by demonstrating "
        "that a third country or a legal entity established in a third "
        "country does not hold or exercise effective control over the "
        "design, development, maintenance, and evolution of those "
        "components or products. Effective control includes the ability to "
        "materially influence the technical evolution, maintenance "
        "priorities, security remediation, and long-term continuity of the "
        "component."
    ),
    "j": (
        "where software released under an open-source licence is used, the "
        "audited provider demonstrates that it has implemented and "
        "documented the appropriate controls to prevent the use of any "
        "remote features or mechanisms that could be used to materially "
        "tamper with or disrupt a device, system, or software."
    ),
    "k": UA3_TEXT["k"],
}

LEVELS = [
    (1, "UA-1", "1.1", UA1_TEXT, UA1_MAP, 5),
    (2, "UA-2", "2.1", UA2_TEXT, UA_SHARED_MAP, 6),
    (3, "UA-3", "3.1", UA3_TEXT, UA_SHARED_MAP, 7),
    (4, "UA-4", "4.1", UA4_TEXT, UA_SHARED_MAP, 9),
]

# UA-3(g) cites "Article 19" for the third-country implementing-act
# derogation, but the Act's own operative text (Article 18, "Associated
# third countries") — not Article 19 ("Conformity self-assessment") — is
# what substantively establishes that mechanism. Flagged rather than
# silently corrected; captured verbatim as printed regardless.
UA3_G_CITATION_NOTE = (
    "Annex II 3.1(g) cites 'an implementing act under Article 19', but "
    "Article 19 in the Act (COM(2026) 502 final part 1) is titled "
    "'Conformity self-assessment' (Union assurance level 1) — the "
    "substantively matching third-country adequacy mechanism is Article "
    "18, 'Associated third countries'. Possible cross-reference "
    "inconsistency in the source draft; captured verbatim as printed, "
    "not corrected. Flag for Phase 3/owner verification against a later "
    "consolidated version of the proposal."
)


def ls(en: str) -> dict:
    return {"en": en, "fr": FR_PENDING}


UA2_D_TYPO_NOTE = (
    "source typo 'presonnel' preserved verbatim per project convention — "
    "erratum candidate"
)


def load_existing():
    public = json.loads(OUT_PUBLIC.read_text()) if OUT_PUBLIC.exists() else []
    local = json.loads(OUT_LOCAL.read_text()) if OUT_LOCAL.exists() else {}
    return public, local


def extract_level(level_num: int, ua_label: str, para_prefix: str, text_map: dict, domain_map: dict, page: int):
    public, local = load_existing()
    existing_ids = {r["id"] for r in public}

    for letter, text in text_map.items():
        rid = f"csat-sov{domain_map[letter][0][-1]}-cada-ua{level_num}-{letter}"
        if rid in existing_ids:
            continue  # already extracted in a prior run of this script

        sov_domain, layer, note = domain_map[letter]
        record = {
            "id": rid,
            "sov_domain": sov_domain,
            "criterion_type": "C",
            "assurance_level": ua_label,
            "layer": layer,
            "derivation": "verbatim",
            "source_refs": [
                {
                    "framework": "CADA",
                    "section_id": f"CADA-Annex-II-{para_prefix}({letter})",
                    "status": "proposed_legislation",
                }
            ],
            "source_pointer": {
                "document": DOCUMENT,
                "section": f"Annex II, {ua_label}, paragraph {para_prefix}({letter})",
                "page": page,
            },
            "source_text": {"en": LOCAL_VERBATIM_PLACEHOLDER, "fr": FR_PENDING},
            "generalized_text": {"en": "GENERALIZATION-PENDING", "fr": FR_PENDING},
            "disposition_default": "inherit" if sov_domain == "SOV-7" else "assess",
            "evidence_quality_options": ALL_EVIDENCE,
            "weight": 1.0,
            "needs_review": False,
        }
        if letter == "g" and level_num == 3:
            note = (note + " " if note else "") + UA3_G_CITATION_NOTE
        if letter == "d" and level_num == 2:
            note = (note + " " if note else "") + UA2_D_TYPO_NOTE
        if note:
            record["needs_review"] = True
            record["needs_review_note"] = note

        public.append(record)
        local[rid] = ls(text)

    OUT_PUBLIC.parent.mkdir(parents=True, exist_ok=True)
    OUT_LOCAL.parent.mkdir(parents=True, exist_ok=True)
    OUT_PUBLIC.write_text(json.dumps(public, indent=2, ensure_ascii=False) + "\n")
    OUT_LOCAL.write_text(json.dumps(local, indent=2, ensure_ascii=False) + "\n")
    print(f"{ua_label}: {len(text_map)} criteria -> {OUT_PUBLIC} ({len(public)} total)")


def main():
    import sys
    if len(sys.argv) != 2 or sys.argv[1] not in ("1", "2", "3", "4"):
        print("Usage: extract_cada.py <level 1|2|3|4>")
        raise SystemExit(1)
    level_num = int(sys.argv[1])
    for ln, label, prefix, text_map, domain_map, page in LEVELS:
        if ln == level_num:
            extract_level(ln, label, prefix, text_map, domain_map, page)
            return
    raise SystemExit(f"no such level {level_num}")


if __name__ == "__main__":
    main()
