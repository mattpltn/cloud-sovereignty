#!/usr/bin/env python3
"""Phase 2b.1: extracts data/extracted/ecsf-guidance.json — deltas found
in the EU Commission's "Cloud Sovereignty Framework — Implementation
guidance" PDF relative to v1.2.1 (see reviews/phase-2b-review-addendum.md
and docs/DECISIONS.md D-014/D-015). Does NOT modify ecsf-scoring.json.

Captures, per the phase instruction:
1. The guidance's alternative weight matrix as a named reference profile
   "ecsf_guidance_matrix" (page 6-7 matrix; also the weight set actually
   used by the official calculator XLSX, cross-checked in Phase 2b.1).
2. The SEAL aggregation rule (page 9): overall SEAL = lowest across
   objectives.
3. The per-domain SEAL-2/3/4 requirement descriptions table (page 10).
   The PDF's table structure does not survive text extraction as
   distinct cells — column boundaries below are inferred from sentence/
   punctuation breaks in the reflowed text, not from the source table's
   actual cell geometry. Every row is therefore marked needs_review so
   this inference is never silently treated as certain (working rule 2).
   SOV-8's SEAL-3 cell has no distinguishable text in the reflowed
   source at all (the PDF text runs directly from the SEAL-2 sentence to
   the SEAL-4 sentence) and is left absent rather than guessed.
4. The SEAL-3 label variant: v1.2.1 calls it "Digital Resilience"
   (data/extracted/ecsf-scoring.json); the guidance calls the same level
   "Technological Sovereignty" (page 3 and page 9-10).

Verbatim-isolation regime (D-009/D-010) applied from the start: public
lang-string fields carrying guidance prose are scrubbed to
SEE-LOCAL-VERBATIM; real text lives only in
data/local/ecsf-guidance-verbatim.json (git-ignored).

Run: .venv/bin/python3 scripts/extract_ecsf_guidance.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_PUBLIC = ROOT / "data" / "extracted" / "ecsf-guidance.json"
OUT_LOCAL = ROOT / "data" / "local" / "ecsf-guidance-verbatim.json"

DOCUMENT = "Cloud Sovereignty Framework - Implementation guidance (EU Commission, post-tender, undated)"
FR_PENDING = "FR-TRANSLATION-PENDING"
LOCAL_VERBATIM_PLACEHOLDER = "SEE-LOCAL-VERBATIM"


def ls(en: str) -> dict:
    return {"en": en, "fr": FR_PENDING}


def sp(section: str, page: int) -> dict:
    return {"document": DOCUMENT, "section": section, "page": page}


# id -> verbatim English text, for every lang-string field this file
# isolates. Written to data/local/ecsf-guidance-verbatim.json; the
# matching public field carries LOCAL_VERBATIM_PLACEHOLDER.
VERBATIM = {
    "seal-agg-rule": (
        "The overall SEAL level is the lowest SEAL level achieved in "
        "any of the objectives."
    ),
    "label-variant-seal3-guidance": "Technological Sovereignty",
    "dsr-SOV-1-seal2": (
        "An autonomous entity in its organization, but not in its "
        "technical choices. The service continues but no longer has "
        "access to updates and security patches in the event of a "
        "break in access to the underlying technology."
    ),
    "dsr-SOV-1-seal3": "Access to the roadmap. Complete guarantee of operations continuity.",
    "dsr-SOV-1-seal4": (
        "Decision-making centres exclusively in the EU. Priority "
        "European customers in roadmap arbitrations."
    ),
    "dsr-SOV-2-seal2": "Isolation by creating separate entities. Limited exposure to export control-type measures.",
    "dsr-SOV-2-seal3": (
        "Complete insulation guaranteeing the inapplicability of "
        "non-EU legislation. No exposure of Member States to export "
        "control measures."
    ),
    "dsr-SOV-2-seal4": (
        "Operations are designed and carried out exclusively in the "
        "EU. Protection of international institutions against export "
        "control measures."
    ),
    "dsr-SOV-3-seal2": "Full control of the data, including encryption control, data localization and deletion guarantee. Logs available.",
    "dsr-SOV-3-seal3": "EU design AI. Logs recorded in real time in the EU.",
    "dsr-SOV-3-seal4": "Immutability of logs, audits carried out by European teams.",
    "dsr-SOV-4-seal2": (
        "Operations carried out and documented locally. Expertise "
        "from outside the EU may be necessary. Open and documented "
        "alternatives exist."
    ),
    "dsr-SOV-4-seal3": (
        "Availability of expertise in Europe, including "
        "subcontractors. Processes are designed and documented locally."
    ),
    "dsr-SOV-4-seal4": (
        "Complete European autonomy, including security clearances "
        "and the integration of key skills of subcontractors."
    ),
    "dsr-SOV-5-seal2": (
        "Majority of the supply chains are documented. Deployments "
        "are carried out locally, according to procedures that can be "
        "external. Critical suppliers and subcontractors can be audited."
    ),
    "dsr-SOV-5-seal3": (
        "The majority of services are designed in the EU. They are "
        "deployed and orchestrated locally. No subcontractors involved "
        "in critical services."
    ),
    "dsr-SOV-5-seal4": (
        "EU-certified components origin. EU design, build and "
        "compliance check. No dependence on non-EU suppliers. Complete "
        "auditability of suppliers and subcontractors."
    ),
    "dsr-SOV-6-seal2": "The services are partially interoperable. HPC is hosted on-premises.",
    "dsr-SOV-6-seal3": (
        "European and public standards for core services. Open-source "
        "majority and predominance of European contributors."
    ),
    "dsr-SOV-6-seal4": "Auditability of the architecture. Full compliance: EU Open AI, public standard, open source.",
    "dsr-SOV-7-seal2": (
        "EAL2 level security. Local operations, transparent and "
        "immediate feedback of information, audits allowed."
    ),
    "dsr-SOV-7-seal3": "ELA 3.",
    "dsr-SOV-7-seal4": "EAL 4-5, ENISA integration, immutable logs.",
    "dsr-SOV-8-seal2": "Documented and transparent approach.",
    "dsr-SOV-8-seal4": "EU-certified lifecycle, EU-audited reporting.",
}


def pub(key: str) -> dict:
    assert key in VERBATIM, key
    return {"en": LOCAL_VERBATIM_PLACEHOLDER, "fr": FR_PENDING}


DOMAIN_ROW_NOTE = (
    "SEAL-2/3/4 column boundaries in this row are inferred from "
    "sentence/punctuation breaks in the guidance PDF's reflowed text "
    "(source page 10); the original table's cell geometry was not "
    "preserved by text extraction. Verify against the source PDF table "
    "layout before treating this split as authoritative."
)
SOV8_SEAL3_NOTE = DOMAIN_ROW_NOTE + " SOV-8's SEAL-3 cell has no text distinguishable from SEAL-2/SEAL-4 in the source reflow and is omitted rather than guessed."


def main() -> None:
    weight_profiles = [
        {
            "id": "ecsf_guidance_matrix",
            "label": ls("ECSF Implementation Guidance alternative weight matrix"),
            "weights_percent": {
                "SOV-1": 20, "SOV-2": 10, "SOV-3": 10, "SOV-4": 15,
                "SOV-5": 10, "SOV-6": 15, "SOV-7": 15, "SOV-8": 5,
            },
            "note": ls(
                "Differs from v1.2.1's default weights (SOV-1 15, SOV-5 20, "
                "SOV-7 10; see ecsf-scoring.json) only in SOV-1 (+5), SOV-5 "
                "(-10) and SOV-7 (+5); sum is 100 in both sets. The guidance "
                "text states authorities may adapt these values. This is "
                "also the exact weight set used by the official calculator "
                "XLSX's own D-column (cross-checked in Phase 2b.1) — the "
                "calculator does not use the v1.2.1 default weights."
            ),
            "source_pointer": sp("The Sovereign Cloud Framework Matrix", 6),
        }
    ]

    seal_aggregation_rule = {
        "description": ls(
            "The government's overall SEAL level for an assessment is the "
            "minimum (lowest) SEAL level achieved across all assessed "
            "objectives, not an average or weighted score."
        ),
        "source_text": pub("seal-agg-rule"),
        "source_pointer": sp("Assessment of Sovereignty Objectives", 9),
    }

    domains = ["SOV-1", "SOV-2", "SOV-3", "SOV-4", "SOV-5", "SOV-6", "SOV-7", "SOV-8"]
    domain_seal_requirements = []
    for dom in domains:
        entry = {
            "domain": dom,
            "seal_2": pub(f"dsr-{dom}-seal2"),
            "seal_4": pub(f"dsr-{dom}-seal4"),
            "source_pointer": sp("The Sovereign Cloud Framework Matrix — SEAL-2/3/4 requirements table", 10),
            "needs_review": True,
        }
        seal3_key = f"dsr-{dom}-seal3"
        if seal3_key in VERBATIM:
            entry["seal_3"] = pub(seal3_key)
            entry["needs_review_note"] = DOMAIN_ROW_NOTE
        else:
            entry["needs_review_note"] = SOV8_SEAL3_NOTE
        domain_seal_requirements.append(entry)

    seal_level_label_variants = [
        {
            "level": 3,
            "v1_2_1_label": ls("Digital Resilience"),
            "guidance_label": pub("label-variant-seal3-guidance"),
            "source_pointer_v1_2_1": {
                "document": "EU Cloud Sovereignty Framework v1.2.1 (Oct. 2025)",
                "section": "SEAL levels",
                "page": 3,
            },
            "source_pointer_guidance": sp("Sovereignty Effective Assurance Levels", 3),
        }
    ]

    public_doc = {
        "document": DOCUMENT,
        "version": "undated (post-tender publication, referenced 2026-07-03)",
        "weight_profiles": weight_profiles,
        "seal_aggregation_rule": seal_aggregation_rule,
        "domain_seal_requirements": domain_seal_requirements,
        "seal_level_label_variants": seal_level_label_variants,
    }

    local_verbatim = {k: ls(v) for k, v in VERBATIM.items()}

    OUT_PUBLIC.parent.mkdir(parents=True, exist_ok=True)
    OUT_LOCAL.parent.mkdir(parents=True, exist_ok=True)
    OUT_PUBLIC.write_text(json.dumps(public_doc, indent=2, ensure_ascii=False) + "\n")
    OUT_LOCAL.write_text(json.dumps(local_verbatim, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote guidance deltas -> {OUT_PUBLIC}")
    print(f"Wrote {len(local_verbatim)} verbatim entries -> {OUT_LOCAL}")


if __name__ == "__main__":
    main()
