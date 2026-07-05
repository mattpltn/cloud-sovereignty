#!/usr/bin/env python3
"""Phase 3: builds data/catalog/catalog.json — the master catalog.

One entry per distinct requirement: clusters c3a.json/ecsf.json/cada.json
records via union-find over the crosswalk's "equivalent" and
"subsumed_by" relations only ("partially_covers"/"related" are
cross-references, not identity claims, and do not merge records into
the same entry — see the crosswalk itself for those). Each entry
designates a primary_id by precedence (D-027): C3A id if the cluster
contains one, else ECSF, else CADA.

Also adds one singleton catalog entry per cada-act.json record tagged
addressed_party: government_self (D-030, item 5b) — obligations CADA
places on the assessing government itself (risk assessment,
procurement, open-source-first), not on any provider, so they have no
crosswalk counterpart to cluster against. primary_framework "CADA"
(cada-act.json is CADA-derived commentary, D-017).

Structure only — no record text is read, rewritten, or duplicated here.

Run: .venv/bin/python3 scripts/build_catalog.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_OUT = ROOT / "data" / "catalog" / "catalog.json"
CROSSWALK_IN = ROOT / "data" / "catalog" / "crosswalk.json"
OUT_OF_SCOPE_IN = ROOT / "data" / "catalog" / "out_of_scope.json"


def framework_of(record_id: str, by_framework: dict[str, set[str]]) -> str:
    for fw, ids in by_framework.items():
        if record_id in ids:
            return fw
    raise KeyError(record_id)


def main() -> None:
    c3a = json.loads((ROOT / "data/extracted/c3a.json").read_text())
    ecsf = json.loads((ROOT / "data/extracted/ecsf.json").read_text())
    cada = json.loads((ROOT / "data/extracted/cada.json").read_text())

    records_by_id = {r["id"]: r for r in c3a + ecsf + cada}
    by_framework = {
        "C3A": {r["id"] for r in c3a},
        "ECSF": {r["id"] for r in ecsf},
        "CADA": {r["id"] for r in cada},
    }
    out_of_scope_ids = {e["id"] for e in json.loads(OUT_OF_SCOPE_IN.read_text())["entries"]} if OUT_OF_SCOPE_IN.exists() else set()
    all_ids = [i for i in records_by_id if i not in out_of_scope_ids]

    parent = {i: i for i in all_ids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    links = json.loads(CROSSWALK_IN.read_text())["links"]
    for link in links:
        if link["relation"] in ("equivalent", "subsumed_by") and link["target_id"]:
            union(link["source_id"], link["target_id"])

    clusters: dict[str, list[str]] = {}
    for i in all_ids:
        clusters.setdefault(find(i), []).append(i)

    entries = []
    precedence = {"C3A": 0, "ECSF": 1, "CADA": 2}
    for i, member_ids in enumerate(sorted(clusters.values(), key=lambda c: sorted(c)[0]), start=1):
        members_sorted = sorted(member_ids, key=lambda mid: (precedence[framework_of(mid, by_framework)], mid))
        primary_id = members_sorted[0]
        primary_framework = framework_of(primary_id, by_framework)
        sov_domains = sorted({records_by_id[m]["sov_domain"] for m in member_ids if "sov_domain" in records_by_id[m]})
        entries.append({
            "id": f"cat-{i:04d}",
            "primary_id": primary_id,
            "primary_framework": primary_framework,
            "sov_domains": sov_domains,
            "member_ids": sorted(member_ids),
        })

    cada_act_path = ROOT / "data/extracted/cada-act.json"
    cada_act_self = []
    if cada_act_path.exists():
        cada_act_self = [r for r in json.loads(cada_act_path.read_text())
                         if r.get("addressed_party") == "government_self"]
    for i, r in enumerate(cada_act_self, start=len(entries) + 1):
        entries.append({
            "id": f"cat-{i:04d}",
            "primary_id": r["id"],
            "primary_framework": "CADA",
            "sov_domains": [],
            "member_ids": [r["id"]],
        })

    CATALOG_OUT.parent.mkdir(parents=True, exist_ok=True)
    CATALOG_OUT.write_text(json.dumps({"entries": entries}, indent=2, ensure_ascii=False) + "\n")

    total_records = len(records_by_id)
    print(f"Wrote {len(entries)} catalog entries -> {CATALOG_OUT}")
    print(f"Distinct requirements: {len(entries)} / {total_records} total records "
          f"({len(out_of_scope_ids)} excluded as documented out-of-scope)")
    print(f"Self-directed (government_self) cada-act entries added: {len(cada_act_self)}")
    multi = [e for e in entries if len(e["member_ids"]) > 1]
    print(f"Multi-member entries: {len(multi)}; single-member entries: {len(entries) - len(multi)}")


if __name__ == "__main__":
    main()
