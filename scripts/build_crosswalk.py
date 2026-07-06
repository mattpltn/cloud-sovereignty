#!/usr/bin/env python3
"""Phase 3: builds data/catalog/crosswalk.json — verified relationships
between ECSF/CADA control records and C3A (and selective direct
ECSF<->CADA links), superseding the unverified Phase 2b
ecsf-c3a-hints.json (kept as a historical artifact, not deleted).

Does not modify c3a.json/ecsf.json/cada.json in any way — this is a
separate linking artifact only, referencing existing ids.

Run: .venv/bin/python3 scripts/build_crosswalk.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "catalog" / "crosswalk.json"

# Each tuple: (source_id, source_fw, target_id_or_None, target_fw_or_None, relation, justification)
LINKS = []


def link(source_id, source_fw, target_id, target_fw, relation, justification):
    LINKS.append((source_id, source_fw, target_id, target_fw, relation, justification))


# ============================================================
# ECSF -> C3A (30 factors; corrects/verifies Phase 2b's unverified hints)
# ============================================================

# SOV-1
link("csat-sov1-ecsf-01", "ECSF", "csat-sov1-03-c1", "C3A", "equivalent",
     "Both require decisive authority/effective control to sit with {TRUSTED_REGION}-based entities.")
link("csat-sov1-ecsf-01", "ECSF", "csat-sov1-03-c2", "C3A", "partially_covers",
     "{NATION} variant of the same effective-control theme, but a stricter, distinct localization tier ECSF's own text doesn't specifically demand — kept a separate catalog entry from -c1 (D-032 fix: an equivalent link to both localization tiers of the same criterion incorrectly merges them into one requirement, losing the C1/C2 distinction).")
link("csat-sov1-ecsf-01", "ECSF", "csat-sov1-01-c1", "C3A", "related",
     "Jurisdiction/contract-governance is a narrower, adjacent concept to 'decisive authority location', not the same claim.")
link("csat-sov1-ecsf-01", "ECSF", "csat-sov1-01-c2", "C3A", "related",
     "{NATION} variant of the same narrower jurisdiction concept.")

link("csat-sov1-ecsf-02", "ECSF", "csat-sov1-04-c", "C3A", "equivalent",
     "Both require advance-notice/assurance mechanisms against undisclosed changes of control.")

link("csat-sov1-ecsf-03", "ECSF", None, None, "no_counterpart",
     "No C3A criterion addresses a provider's financing sources; C3A's SOV-1 criteria are about control/jurisdiction, not capital structure.")
link("csat-sov1-ecsf-04", "ECSF", None, None, "no_counterpart",
     "No C3A criterion addresses investment/jobs/value-creation within the trusted region; an industrial-policy metric, not a technical criterion.")
link("csat-sov1-ecsf-05", "ECSF", None, None, "no_counterpart",
     "No C3A criterion addresses alignment with regional strategic policy initiatives.")

link("csat-sov1-ecsf-06", "ECSF", "csat-sov4-09-c", "C3A", "partially_covers",
     "C3A's disconnect capability addresses surviving an enforced cutoff, a narrower technical case than ECSF's broader 'sustain operations if vendor support withdrawn'.")
link("csat-sov1-ecsf-06", "ECSF", "csat-sov4-10-c", "C3A", "partially_covers",
     "Reconnection-after-disconnect capability is the recovery half of the same narrower technical case.")
link("csat-sov1-ecsf-06", "ECSF", "csat-sov6-02-c", "C3A", "related",
     "Vendor-disruption contingency planning is thematically adjacent but framed around third-party software vendors specifically, not service cease/suspend requests generally.")

# SOV-2
link("csat-sov2-ecsf-01", "ECSF", "csat-sov1-01-c1", "C3A", "equivalent",
     "Both require the provider's operations/contracts to be governed by {TRUSTED_REGION} law.")
link("csat-sov2-ecsf-01", "ECSF", "csat-sov1-01-c2", "C3A", "partially_covers",
     "{NATION} variant of the same jurisdiction theme, but a stricter, distinct localization tier ECSF's own text doesn't specifically demand — kept a separate catalog entry from -c1 (D-032 fix, same over-merge pattern as sov1-03 above).")

link("csat-sov2-ecsf-02", "ECSF", "csat-sov2-01-c", "C3A", "equivalent",
     "Both require identifying/assessing exposure to laws from outside the trusted region with cross-border reach.")

link("csat-sov2-ecsf-03", "ECSF", "csat-sov2-01-c", "C3A", "partially_covers",
     "General non-EU law risk assessment would surface compelled-access risk, but does not specifically require documenting the compulsion channels/mechanisms ECSF asks about.")

link("csat-sov2-ecsf-04", "ECSF", "csat-sov2-01-c", "C3A", "partially_covers",
     "Export-control/international-regime restrictions are a subset of the general non-EU law risk assessment, not a dedicated requirement in C3A.")

link("csat-sov2-ecsf-05", "ECSF", None, None, "no_counterpart",
     "No C3A criterion addresses the jurisdiction where IP is created, registered, or developed.")

# SOV-3
link("csat-sov3-ecsf-01", "ECSF", "csat-sov3-02-c", "C3A", "equivalent",
     "Both require customer-exclusive control over cryptographic key access, excluding the provider.")
link("csat-sov3-ecsf-01", "ECSF", "csat-sov3-02-ac", "C3A", "equivalent",
     "SaaS-scope extension of the same external-key-management requirement.")

link("csat-sov3-ecsf-02", "ECSF", "csat-sov3-04-c", "C3A", "partially_covers",
     "C3A's logging criterion covers data-access visibility well but not AI-model-usage auditability or irreversible-deletion verification, both of which ECSF also requires.")
link("csat-sov3-ecsf-02", "ECSF", "csat-sov3-04-ac1", "C3A", "partially_covers",
     "Real-time API access to logs is part of the covered visibility aspect only.")
link("csat-sov3-ecsf-02", "ECSF", "csat-sov3-04-ac2", "C3A", "partially_covers",
     "Granular filtering is part of the covered visibility aspect only.")

link("csat-sov3-ecsf-03", "ECSF", "csat-sov3-01-c3", "C3A", "equivalent",
     "ECSF's 'strict confinement of storage/processing to {TRUSTED_REGION}, no fallback' is the literal match for c3's customer-data-in-{TRUSTED_REGION} claim.")
link("csat-sov3-ecsf-03", "ECSF", "csat-sov3-01-c1", "C3A", "partially_covers",
     "c1 is a transparency/check-where-stored mechanism, not itself a residency guarantee — a related but distinct, weaker claim than ECSF's confinement requirement (D-032 fix: previously tagged equivalent to all five sov3-01 variants at once, incorrectly merging five distinct requirements into one catalog entry).")
link("csat-sov3-ecsf-03", "ECSF", "csat-sov3-01-c2", "C3A", "partially_covers",
     "c2 covers derived/account data specifically (not customer data), a related but distinct data category from ECSF's general confinement claim (D-032 fix).")
link("csat-sov3-ecsf-03", "ECSF", "csat-sov3-01-c4", "C3A", "partially_covers",
     "c4 is the {NATION} (C2) variant of the same residency theme as c3, a stricter, distinct localization tier ECSF's own text doesn't specifically demand — kept a separate catalog entry from c3 (D-032 fix, same over-merge pattern as sov1-01/sov1-03/sov4-01).")
link("csat-sov3-ecsf-03", "ECSF", "csat-sov3-01-c5", "C3A", "partially_covers",
     "c5 covers provider data specifically (not customer data), a related but distinct data category from ECSF's general confinement claim (D-032 fix).")

link("csat-sov3-ecsf-04", "ECSF", None, None, "no_counterpart",
     "C3A predates AI-specific criteria entirely; no criterion addresses AI model/pipeline governance or non-EU technology-stack dependency for AI.")

# SOV-4
link("csat-sov4-ecsf-01", "ECSF", "csat-sov6-02-c", "C3A", "related",
     "Vendor-disruption contingency implies some substitutability, but C3A has no dedicated workload-portability/migration-ease criterion as ECSF frames it.")

link("csat-sov4-ecsf-02", "ECSF", "csat-sov4-01-c1", "C3A", "partially_covers",
     "Personnel citizenship/residency requirements support EU-operator capacity but do not by themselves guarantee operation 'without non-EU vendor involvement'.")
link("csat-sov4-ecsf-02", "ECSF", "csat-sov4-02-c1", "C3A", "partially_covers",
     "Admin-access-location requirement supports the same capacity claim from a different angle (where access originates, not who performs it).")

link("csat-sov4-ecsf-03", "ECSF", "csat-sov4-01-c1", "C3A", "equivalent",
     "Requiring {TRUSTED_REGION}-citizen, {TRUSTED_REGION}-resident personnel directly ensures an {TRUSTED_REGION}-based talent pool.")
link("csat-sov4-ecsf-03", "ECSF", "csat-sov4-01-c2", "C3A", "partially_covers",
     "{NATION} variant of the same talent-pool theme, but a stricter, distinct localization tier ECSF's own text doesn't specifically demand — kept a separate catalog entry from -c1 (D-032 fix, same over-merge pattern as sov1-01/sov1-03/sov3-01).")
link("csat-sov4-ecsf-03", "ECSF", "csat-sov4-01-c3", "C3A", "partially_covers",
     "Standalone-{TRUSTED_REGION}-organization is a related but genuinely distinct requirement (organizational independence, not personnel citizenship) — not the same claim as -c1/-c2, so not equivalent (D-032 fix: previously merged all three sov4-01 variants into one catalog entry).")

link("csat-sov4-ecsf-04", "ECSF", "csat-sov4-01-c1", "C3A", "partially_covers",
     "Personnel-location requirement covers part of 'support delivered from within the trusted region', combined with a second, distinct C3A criterion (sov4-02) for the admin-access half — neither alone is equivalent to ECSF's combined claim.")
link("csat-sov4-ecsf-04", "ECSF", "csat-sov4-02-c1", "C3A", "partially_covers",
     "Admin-access-location requirement covers the other part of the same combined claim; kept partially_covers (not equivalent) so this doesn't force sov4-01 and sov4-02 — two otherwise-distinct C3A criteria — into the same catalog entry.")

link("csat-sov4-ecsf-05", "ECSF", "csat-sov6-01-c", "C3A", "equivalent",
     "Source-code backup enabling independent development is a direct, strong match for 'full technical documentation, source code, operational know-how'.")

link("csat-sov4-ecsf-06", "ECSF", "csat-sov4-03-c", "C3A", "partially_covers",
     "Connectivity-provider redundancy/independence is a narrow instance of supplier/subcontractor location and control, not the general claim ECSF makes.")
link("csat-sov4-ecsf-06", "ECSF", "csat-sov5-03-c", "C3A", "partially_covers",
     "External-cloud-service-dependency documentation is another narrow instance of the same broader supplier/subcontractor concern.")

# SOV-5
link("csat-sov5-ecsf-01", "ECSF", "csat-sov5-02-c", "C3A", "equivalent",
     "Hardware component country-of-origin documentation is a direct match for geographic source/manufacturing location.")

link("csat-sov5-ecsf-02", "ECSF", "csat-sov5-02-c", "C3A", "partially_covers",
     "Hardware inventory documentation covers hardware generally but doesn't single out embedded firmware as ECSF does.")
link("csat-sov5-ecsf-02", "ECSF", "csat-sov5-01-c", "C3A", "partially_covers",
     "Software inventory documentation covers embedded-code-as-software generally but doesn't single out firmware specifically either.")

link("csat-sov5-ecsf-03", "ECSF", "csat-sov5-01-c", "C3A", "equivalent",
     "Software component country/supplier documentation is a direct match for software origin.")

link("csat-sov5-ecsf-04", "ECSF", "csat-sov5-04-c", "C3A", "partially_covers",
     "Export-restriction risk mitigation overlaps with, but doesn't fully equal, a general 'degree of reliance' assessment.")
link("csat-sov5-ecsf-04", "ECSF", "csat-sov5-01-ac", "C3A", "partially_covers",
     "Software-dependency risk-mitigation process is one supply-chain-layer component of the broader reliance question.")

link("csat-sov5-ecsf-05", "ECSF", "csat-sov5-01-c", "C3A", "equivalent",
     "Software supplier inventory is one of the three inventories collectively implementing full supply-chain visibility.")
link("csat-sov5-ecsf-05", "ECSF", "csat-sov5-02-c", "C3A", "equivalent",
     "Hardware supplier inventory is the second of the three inventories.")
link("csat-sov5-ecsf-05", "ECSF", "csat-sov5-03-c", "C3A", "equivalent",
     "External-service supplier inventory is the third of the three inventories; audit rights specifically are not explicit in C3A's phrasing, a minor gap.")

# SOV-6
link("csat-sov6-ecsf-01", "ECSF", None, None, "no_counterpart",
     "No C3A criterion requires open, non-proprietary API/protocol interoperability as such.")
link("csat-sov6-ecsf-02", "ECSF", None, None, "no_counterpart",
     "No C3A criterion requires open-license software or audit/modify/redistribute rights.")

link("csat-sov6-ecsf-03", "ECSF", "csat-sov4-08-c", "C3A", "equivalent",
     "The Data Flow Diagram requirement is a direct match for architectural documentation, data flows, and dependencies visibility.")

link("csat-sov6-ecsf-04", "ECSF", "csat-sov5-02-c", "C3A", "partially_covers",
     "Hardware component documentation covers general hardware transparency but not HPC/processor/accelerator independence specifically.")

# ============================================================
# CADA -> C3A (40 criteria; UA-1's 7-letter scheme and UA-2/3/4's shared
# 11-letter scheme are mapped once conceptually per letter, applied to
# every level-instance of that letter since the underlying relationship
# to C3A doesn't change across levels, only the requirement's strictness)
# ============================================================

UA1_MAP = {
    "a": ("csat-sov1-02-c1", "equivalent", "Provider established in the trusted region is a direct match for a registered head office there."),
    "b": (None, "no_counterpart", "No C3A criterion requires general infrastructure/asset residency as a standalone claim (C3A's residency criteria are data-specific, SOV-3-01)."),
    "c": ("csat-sov3-01-c3", "equivalent", "Customer data remaining exclusively in the trusted region is the core data-residency claim C3A's SOV-3-01-C3 makes (D-032 fix: previously mistargeted at c1, the transparency/check-where-stored criterion, not the residency-guarantee criterion CADA's text actually matches)."),
    "d": ("csat-sov4-06-c", "partially_covers", "Third-party software risk analysis addresses part of the outsourcing-governance concern, but not operational-support outsourcing generally."),
    "e": (None, "no_counterpart", "C3A extracts no explicit cybersecurity-certification criterion; this routes to SOV-7, inheritance-only per CLAUDE.md."),
    "f": (None, "no_counterpart", "No C3A criterion requires subcontractor transparency/due-diligence/oversight as its own standalone claim."),
    "g": ("csat-sov2-01-c", "partially_covers", "General non-EU-law risk assessment would surface this specific vulnerability-disclosure-law risk, but doesn't require the categorical guarantee CADA demands."),
}

UA_SHARED_MAP = {
    "a": ("csat-sov1-02-c1", "equivalent", "Provider/subcontractor establishment in the trusted region is a direct match for registered head office there."),
    "b": ("csat-sov4-01-c1", "partially_covers", "The personnel-location component matches C3A's citizen/resident requirement; the infrastructure/assets component has no C3A analog."),
    "c": ("csat-sov3-01-c3", "equivalent", "Customer data remaining exclusively in the trusted region is the core data-residency claim (D-032 fix: previously mistargeted at c1; see UA1_MAP's identical fix). Note (catalog-fix review N-1): UA-4's instance of this criterion is narrower than UA-2/UA-3's — it applies only to data identified as sensitive following a risk assessment, not all customer data — but is still the same underlying residency requirement at a stricter assurance tier; the narrower scope is preserved via this record's own assurance_level (UA-4) rather than a different C3A target."),
    "d": ("csat-sov4-01-c1", "equivalent", "Personnel citizenship/residency is the same core requirement; CADA's UA levels add a security-clearance nuance C3A doesn't have."),
    "e": (None, "no_counterpart", "C3A extracts no explicit cybersecurity-certification criterion; routes to SOV-7, inheritance-only per CLAUDE.md."),
    "f": (None, "no_counterpart", "C3A predates AI-specific criteria entirely; no criterion restricts AI training on customer-derived data."),
    "g": ("csat-sov1-03-c1", "equivalent", "Third-country control test is the same core 'who effectively controls the entity' concept C3A's SOV-1-03 addresses; CADA's sub-conditions (i-iv) are additional detail, not a different concept."),
    "h": ("csat-sov4-02-c1", "partially_covers", "Admin-access-location requirement covers part of 'no support outside the trusted region'; CADA's (h) is broader, covering all support/maintenance/monitoring/incident-response."),
    "i": ("csat-sov5-01-c", "partially_covers", "Software inventory/dependency documentation overlaps substantially with SBOM+dependency-list, but CADA additionally requires remote-tamper controls and source-code audits C3A doesn't."),
    "j": ("csat-sov4-06-c", "related", "General third-party software risk analysis is thematically adjacent; C3A has no open-source-specific tamper-control requirement."),
    "k": ("csat-sov1-03-c1", "related", "Both concern corporate-structure sovereignty (control), but CADA's specific subsidiary-separation mechanism has no direct C3A analog."),
}

UA1_LETTER_TO_ID = {
    "a": "csat-sov2-cada-ua1-a", "b": "csat-sov2-cada-ua1-b", "c": "csat-sov3-cada-ua1-c",
    "d": "csat-sov4-cada-ua1-d", "e": "csat-sov7-cada-ua1-e", "f": "csat-sov5-cada-ua1-f",
    "g": "csat-sov2-cada-ua1-g",
}

UA_SHARED_DOMAIN = {
    "a": "sov2", "b": "sov2", "c": "sov3", "d": "sov4", "e": "sov7", "f": "sov3",
    "g": "sov1", "h": "sov4", "i": "sov5", "j": "sov6", "k": "sov2",
}


def cada_id(level, letter):
    if level == 1:
        return UA1_LETTER_TO_ID[letter]
    return f"csat-{UA_SHARED_DOMAIN[letter]}-cada-ua{level}-{letter}"


for letter, (target, relation, note) in UA1_MAP.items():
    sid = cada_id(1, letter)
    target_fw = "C3A" if target else None
    link(sid, "CADA", target, target_fw, relation, note)

for level in (2, 3, 4):
    for letter, (target, relation, note) in UA_SHARED_MAP.items():
        sid = cada_id(level, letter)
        target_fw = "C3A" if target else None
        link(sid, "CADA", target, target_fw, relation, note)


# ============================================================
# ECSF <-> CADA direct links (selective, "where direct" only)
# ============================================================

link("csat-sov3-cada-ua2-f", "CADA", "csat-sov3-ecsf-04", "ECSF", "subsumed_by",
     "CADA's narrow 'no AI training on customer data' rule is one specific instance of ECSF's broader 'AI models/pipelines under trusted-region control' factor — CADA's requirement is subsumed by ECSF's broader ask.")
link("csat-sov3-cada-ua3-f", "CADA", "csat-sov3-ecsf-04", "ECSF", "subsumed_by",
     "Same relationship as the UA-2 instance of this criterion (identical requirement text).")
link("csat-sov3-cada-ua4-f", "CADA", "csat-sov3-ecsf-04", "ECSF", "subsumed_by",
     "Same relationship as the UA-2 instance of this criterion (identical requirement text).")
link("csat-sov6-ecsf-02", "ECSF", "csat-sov6-cada-ua2-j", "CADA", "related",
     "Both concern open-source software, but ECSF asks about licensing/audit-modify-redistribute rights while CADA(j) asks about remote-tamper-prevention controls — different specific asks under the same theme.")
link("csat-sov1-ecsf-02", "ECSF", "csat-sov1-cada-ua2-g", "CADA", "related",
     "Both concern control-change risk, but ECSF's factor is a general 'assurances against change of control' while CADA(g) is specifically about third-country control.")


def main() -> None:
    entries = []
    for i, (sid, sfw, tid, tfw, relation, justification) in enumerate(LINKS, start=1):
        entries.append({
            "id": f"xw-{i:04d}",
            "source_id": sid,
            "source_framework": sfw,
            "target_id": tid,
            "target_framework": tfw,
            "relation": relation,
            "justification": justification,
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"links": entries}, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(entries)} crosswalk links -> {OUT}")


if __name__ == "__main__":
    main()
