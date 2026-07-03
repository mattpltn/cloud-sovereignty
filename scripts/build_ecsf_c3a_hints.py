#!/usr/bin/env python3
"""Phase 2b: produces data/extracted/ecsf-c3a-hints.json, a candidate
ECSF-factor -> C3A-criteria coverage map, HINTS ONLY for the Phase 3
crosswalk. Every mapping here is unverified (a thematic reading, not a
cross-checked equivalence) and every ecsf.json record with no plausible
C3A match is given an empty candidate list (coverage: "uncovered") and
gets a needs_review flag on the ecsf.json record itself, per this
phase's instructions.

Each entry is emitted as {"coverage": "covered"|"uncovered",
"c3a_candidates": [...]} (CR-1, phase-2b-review.md) rather than a bare
list with a magic "uncovered" sentinel string.

Does not modify c3a.json or ecsf.json — this file only references their
existing ids; validate.py's check_ecsf_c3a_hints() confirms every
referenced id actually exists in one of those two files.

Run: .venv/bin/python3 scripts/build_ecsf_c3a_hints.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "extracted" / "ecsf-c3a-hints.json"

CANDIDATES = {
    # SOV-1
    "csat-sov1-ecsf-01": ["csat-sov1-01-c1", "csat-sov1-01-c2", "csat-sov1-03-c1", "csat-sov1-03-c2"],
    "csat-sov1-ecsf-02": ["csat-sov1-04-c"],
    "csat-sov1-ecsf-03": [],
    "csat-sov1-ecsf-04": [],
    "csat-sov1-ecsf-05": [],
    "csat-sov1-ecsf-06": ["csat-sov6-02-c", "csat-sov6-02-ac"],
    # SOV-2
    "csat-sov2-ecsf-01": ["csat-sov1-01-c1", "csat-sov1-01-c2"],
    "csat-sov2-ecsf-02": ["csat-sov2-01-c"],
    "csat-sov2-ecsf-03": ["csat-sov2-01-c", "csat-sov2-03-c1", "csat-sov2-03-c2"],
    "csat-sov2-ecsf-04": ["csat-sov2-01-c"],
    "csat-sov2-ecsf-05": [],
    # SOV-3
    "csat-sov3-ecsf-01": ["csat-sov3-02-c", "csat-sov3-02-ac"],
    "csat-sov3-ecsf-02": ["csat-sov3-04-c", "csat-sov3-04-ac1", "csat-sov3-04-ac2"],
    "csat-sov3-ecsf-03": ["csat-sov3-01-c1", "csat-sov3-01-c2", "csat-sov3-01-c3", "csat-sov3-01-c4", "csat-sov3-01-c5"],
    "csat-sov3-ecsf-04": [],
    # SOV-4
    "csat-sov4-ecsf-01": ["csat-sov6-02-c", "csat-sov6-02-ac"],
    "csat-sov4-ecsf-02": ["csat-sov4-01-c1", "csat-sov4-01-c2", "csat-sov4-01-c3", "csat-sov4-02-c1", "csat-sov4-02-c2"],
    "csat-sov4-ecsf-03": ["csat-sov4-01-c1", "csat-sov4-01-c2", "csat-sov4-01-c3"],
    "csat-sov4-ecsf-04": ["csat-sov4-01-c1", "csat-sov4-01-c2", "csat-sov4-01-c3", "csat-sov4-02-c1", "csat-sov4-02-c2"],
    "csat-sov4-ecsf-05": ["csat-sov6-01-c", "csat-sov4-05-ac2"],
    "csat-sov4-ecsf-06": ["csat-sov4-03-c", "csat-sov4-03-ac", "csat-sov5-03-c", "csat-sov5-03-ac"],
    # SOV-5
    "csat-sov5-ecsf-01": ["csat-sov5-02-c", "csat-sov5-02-ac"],
    "csat-sov5-ecsf-02": ["csat-sov5-02-c", "csat-sov5-02-ac", "csat-sov5-01-c"],
    "csat-sov5-ecsf-03": ["csat-sov5-01-c", "csat-sov5-01-ac"],
    "csat-sov5-ecsf-04": ["csat-sov5-04-c", "csat-sov5-01-ac", "csat-sov5-02-ac", "csat-sov5-03-ac"],
    "csat-sov5-ecsf-05": ["csat-sov5-01-c", "csat-sov5-02-c", "csat-sov5-03-c"],
    # SOV-6
    "csat-sov6-ecsf-01": [],
    "csat-sov6-ecsf-02": [],
    "csat-sov6-ecsf-03": ["csat-sov4-08-c", "csat-sov4-08-ac"],
    "csat-sov6-ecsf-04": ["csat-sov5-02-c", "csat-sov5-02-ac"],
}


def main() -> None:
    hints = {
        ecsf_id: {
            "coverage": "covered" if candidates else "uncovered",
            "c3a_candidates": candidates,
        }
        for ecsf_id, candidates in CANDIDATES.items()
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(hints, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(hints)} hint entries -> {OUT}")


if __name__ == "__main__":
    main()
