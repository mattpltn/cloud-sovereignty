#!/usr/bin/env python3
"""Phase 3: builds data/catalog/ladders.json — the SEAL <-> C3A C1/C2 <->
CADA UA-1..4 three-ladder mapping, per SOV domain, for Phase 5's scoring
ceiling.

Source basis, per domain: the ECSF Implementation Guidance's per-domain
SEAL-2/3/4 requirement text (data/extracted/ecsf-guidance.json), C3A's
localization_level (C1/C2) usage per domain (data/extracted/c3a.json),
and CADA's UA-1..4 criteria per domain (data/extracted/cada.json).

A structural finding this build surfaces (recorded in DECISIONS): C1/C2
and SEAL/UA are not the same kind of axis. SEAL (0-4) and UA (1-4) are
both STRICTNESS/maturity ladders; C3A's C1/C2 is a LOCALIZATION-SCOPE
axis (does a requirement apply at the trusted-region level, or does it
require nation-specific instantiation) orthogonal to strictness. Cells
mapping SEAL to CADA UA are the primary, more defensible axis;
cells noting C1/C2's position are marked "inferred" and flagged with
this caveat rather than claimed as directly source-anchored, since no
source text directly equates a C1/C2 tier to a specific SEAL/UA number.

SEAL-0 and SEAL-1 have no per-domain guidance text at all (only the
generic, non-domain-specific SEAL-0/1 definitions exist) — every domain
marks these two rows no_mapping.

Does not modify c3a.json/ecsf.json/cada.json/ecsf-guidance.json.

Run: .venv/bin/python3 scripts/build_ladders.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "catalog" / "ladders.json"

NO_SEAL01_NOTE = (
    "The ECSF Implementation Guidance provides no per-domain text for "
    "SEAL-0/SEAL-1 (only the generic, cross-domain SEAL level "
    "definitions exist) — no domain-specific source to anchor a mapping "
    "against."
)

C12_CAVEAT = (
    "C3A's C1/C2 is a localization-SCOPE axis (trusted-region vs. "
    "nation-specific), not a strictness ladder like SEAL/UA — this cell "
    "is offered as a plausible correspondence, not a source-anchored "
    "equivalence; no source text directly equates a C1/C2 tier to a "
    "specific SEAL number."
)

# Per domain: {seal_level: (cada_ua_or_None, c3a_localization_or_None, confidence, justification)}
DOMAINS = {
    "SOV-1": {
        2: ("UA-1", "C1", "inferred",
            "SEAL-2 ('autonomous in organization, not technical choices; loses updates/patches on disconnect') describes a weak baseline closest to UA-1's self-assessed establishment/control bar, not yet UA-2's audited non-control test. " + C12_CAVEAT),
        3: ("UA-2", "C1", "inferred",
            "SEAL-3 ('access to roadmap, complete continuity guarantee') is stronger than SEAL-2 but short of full independence — closest to UA-2's audited (but not yet fully independent) control posture. " + C12_CAVEAT),
        4: ("UA-4", "C1", "inferred",
            "SEAL-4 ('decision-making centres exclusively in the trusted region') matches CADA's strictest 'not subject to third-country control' bar (UA-3/UA-4's (g)); UA-4 chosen as ECSF's own ceiling framing is at the trusted-region level, not a further nation-specific tightening C3A's C2 would represent. " + C12_CAVEAT),
    },
    "SOV-2": {
        2: ("UA-1", "C1", "inferred",
            "SEAL-2 ('isolation via separate entities, limited export-control exposure') is a partial-mitigation posture, closest to UA-1's baseline establishment/traceability bar. " + C12_CAVEAT),
        3: ("UA-2", "C1", "inferred",
            "SEAL-3 ('complete insulation from outside-region legislation') aligns with UA-2's audited non-EU-law-exposure criteria, a step beyond UA-1's self-assessment. " + C12_CAVEAT),
        4: ("UA-3", "C2", "inferred",
            "SEAL-4 ('operations designed and carried out exclusively in the trusted region, protection of international institutions') matches UA-3's stricter operational-exclusivity bar (personnel citizenship + Union residency) more than UA-2's. " + C12_CAVEAT),
    },
    "SOV-3": {
        2: ("UA-1", None, "inferred",
            "SEAL-2 ('full control of data, encryption control, localization, deletion guarantee, logs available') matches C3A's baseline customer-key-control/data-residency criteria, closest to UA-1's self-assessed data-residency bar (CADA (c))."),
        3: ("UA-3", None, "source_anchored",
            "SEAL-3 explicitly names 'real time in the {TRUSTED_REGION}' logging, matching CADA UA-3(c)'s stricter customer-data residency (extended to metadata/telemetry, no exceptions) and the real-time-logging emphasis in ECSF's own SOV-3 factors (csat-sov3-ecsf-02)."),
        4: ("UA-4", None, "source_anchored",
            "SEAL-4's 'immutability of logs, audits carried out by {TRUSTED_REGION} teams' matches CADA UA-4(c)'s sensitivity-classified data residency (the strictest tier, following a risk assessment) and C3A's real-time/immutable logging aspirations in the SOV-3-04 family."),
    },
    "SOV-4": {
        2: ("UA-1", "C1", "inferred",
            "SEAL-2 ('operations carried out locally, expertise from outside the region may be necessary') is a partial-localization posture, matching UA-1's baseline outsourcing-governance bar (CADA (d)) rather than UA-2's stricter personnel-citizenship requirement. " + C12_CAVEAT),
        3: ("UA-2", "C1", "inferred",
            "SEAL-3 ('availability of expertise in the trusted region including subcontractors, processes documented locally') aligns with UA-2's personnel-screening/citizenship bar (CADA (d)), a step beyond UA-1's outsourcing-governance-only requirement. " + C12_CAVEAT),
        4: ("UA-4", "C2", "inferred",
            "SEAL-4 ('complete regional autonomy including security clearances, integration of subcontractor skills') matches UA-4's strictest personnel-citizenship-plus-security-clearance bar (CADA (d)), the same criterion family C3A's own C2/nation-specific SOV-4-01/02 tier targets. " + C12_CAVEAT),
    },
    "SOV-5": {
        2: ("UA-1", "C1", "inferred",
            "SEAL-2 ('majority of supply chains documented, deployments local, critical suppliers auditable') matches a baseline supply-chain-documentation posture; CADA has no UA-1-level supply-chain criterion, so this is inferred from C3A's own baseline supply-chain documentation criteria (SOV-5-01/02/03) rather than a CADA anchor. " + C12_CAVEAT),
        3: ("UA-2", None, "inferred",
            "SEAL-3 ('majority of services designed in the trusted region, no subcontractors in critical services') aligns with CADA UA-2(i)'s SBOM/dependency-transparency bar, a step beyond bare documentation."),
        4: ("UA-4", None, "inferred",
            "SEAL-4 ('trusted-region-certified components, no dependence on outside-region suppliers, complete auditability') matches CADA UA-4(i)'s strictest 'retain effective control over software components' bar, the top of the supply-chain criteria progression."),
    },
    "SOV-6": {
        2: (None, None, "no_mapping",
            "SEAL-2 ('partially interoperable, HPC hosted on-premises') has no CADA UA analog — CADA's SOV-6 criterion (j) addresses only open-source tamper-controls, not interoperability/HPC generally; no source text supports a specific UA-level correspondence for this cell."),
        3: (None, None, "no_mapping",
            "SEAL-3 ('trusted-region and public standards, open-source majority/contributors') similarly has no CADA UA analog for the same reason — CADA's (j) is narrower in scope than ECSF's SOV-6 factors."),
        4: (None, None, "no_mapping",
            "SEAL-4 ('full compliance: open AI, public standard, open source') has no CADA UA analog; CADA's SOV-6 criterion doesn't scale a general open-standards/interoperability requirement across UA levels the way ECSF's SEAL scale does."),
    },
}


def main() -> None:
    domains_out = []
    for dom, seals in DOMAINS.items():
        rows = []
        for level in (0, 1):
            rows.append({
                "seal": level, "cada_ua": None, "c3a_localization": None,
                "confidence": "no_mapping", "justification": NO_SEAL01_NOTE,
            })
        for level in (2, 3, 4):
            cada_ua, c3a_loc, confidence, justification = seals[level]
            rows.append({
                "seal": level, "cada_ua": cada_ua, "c3a_localization": c3a_loc,
                "confidence": confidence, "justification": justification,
            })
        domains_out.append({"sov_domain": dom, "cells": rows})

    out = {
        "note": (
            "SOV-7 (inheritance-only) and SOV-8 (out of scope) are not "
            "included — see DECISIONS.md and CLAUDE.md for why. This "
            "ladder is Phase 3 input for Phase 5's scoring-ceiling design, "
            "not itself a scoring formula."
        ),
        "domains": domains_out,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")

    total_cells = sum(len(d["cells"]) for d in domains_out)
    counts = {"source_anchored": 0, "inferred": 0, "no_mapping": 0}
    for d in domains_out:
        for c in d["cells"]:
            counts[c["confidence"]] += 1
    print(f"Wrote {len(domains_out)} domains, {total_cells} cells -> {OUT}")
    print(f"Confidence breakdown: {counts}")


if __name__ == "__main__":
    main()
