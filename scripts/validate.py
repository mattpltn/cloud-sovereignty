#!/usr/bin/env python3
"""CSAT validator: JSON Schema meta-validation + persona-approval gate.

Usage: .venv/bin/python3 scripts/validate.py

Exits non-zero on any failure. See CLAUDE.md "Working rules for Claude Code"
rule 7: no commit with a failing validator.
"""

import glob
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schema"
PERSONAS_DIR = ROOT / "tests" / "personas"
EXTRACTED_DIR = ROOT / "data" / "extracted"
LOCAL_DIR = ROOT / "data" / "local"

# Files in data/extracted that are NOT arrays of control-record.schema.json
# records, and are validated separately (see their own check_* functions).
NON_CONTROL_RECORD_FILES = {
    "ecsf-scoring.json", "ecsf-c3a-hints.json", "ecsf-guidance.json", "ecsf-calculator.json",
    "cada-scope.json", "cada-evidence.json", "cada-act.json",
}

# array of {"id": ...} control records (ecsf-guidance.json/cada-scope.json/
# cada-evidence.json are single nested objects; ecsf-calculator.json's ids
# don't match the verbatim file's finer per-field keys, e.g.
# "sov1-so1-desc"/"sov1-so1-opt1" vs. the record id "sov1-so1"). These are
# excluded from the generic id-set cross-check (check_local_verbatim) —
# see check_verbatim_placeholder_count for their equivalent completeness
# check — but still covered by the (generalized) leak check.
ID_KEYED_VERBATIM_EXCLUSIONS = {"ecsf-guidance.json", "ecsf-calculator.json", "cada-scope.json", "cada-evidence.json"}


def load_schemas() -> tuple[dict[str, dict], Registry]:
    schemas = {}
    resources = []
    for f in sorted(SCHEMA_DIR.glob("*.json")):
        data = json.loads(f.read_text())
        schemas[f.name] = data
        resources.append((data["$id"], Resource.from_contents(data)))
    registry = Registry().with_resources(resources)
    return schemas, registry


def check_schemas_are_valid(schemas: dict[str, dict]) -> list[str]:
    """Every file in /schema must itself be a valid Draft 2020-12 schema."""
    errors = []
    for name, data in schemas.items():
        try:
            Draft202012Validator.check_schema(data)
        except Exception as e:  # noqa: BLE001 - report and continue
            errors.append(f"schema/{name}: invalid JSON Schema — {e}")
    return errors


def check_personas(schemas: dict[str, dict], registry: Registry) -> tuple[list[str], int, int]:
    """Validates every persona fixture and enforces the approval gate:
    status: approved requires approved_by and approved_date (also enforced
    structurally by the schema's if/then, checked again here with a
    clearer error message since this is the rule most likely to be
    violated by hand-editing).
    """
    errors = []
    draft_count = 0
    approved_count = 0
    validator = Draft202012Validator(
        schemas["persona-profile.schema.json"], registry=registry
    )
    for f in sorted(PERSONAS_DIR.glob("*.yaml")):
        data = yaml.safe_load(f.read_text())
        for err in validator.iter_errors(data):
            errors.append(f"tests/personas/{f.name}: {'/'.join(str(p) for p in err.path)}: {err.message}")

        status = data.get("status")
        if status == "approved":
            approved_count += 1
            if not data.get("approved_by") or not data.get("approved_date"):
                errors.append(
                    f"tests/personas/{f.name}: status is approved but missing "
                    "approved_by and/or approved_date (persona-approval gate)"
                )
        elif status == "draft":
            draft_count += 1
        else:
            errors.append(f"tests/personas/{f.name}: unknown status {status!r}")

    return errors, draft_count, approved_count


def check_extracted_records(schemas: dict[str, dict], registry: Registry) -> tuple[list[str], int]:
    """Validates every raw extraction file in /data/extracted (Phase 2+)
    against control-record.schema.json. Also checks id uniqueness within
    each file, since the schema itself can't enforce that across an array.
    """
    errors = []
    count = 0
    validator = Draft202012Validator(
        schemas["control-record.schema.json"], registry=registry
    )
    for f in sorted(EXTRACTED_DIR.glob("*.json")):
        if f.name in NON_CONTROL_RECORD_FILES:
            continue
        records = json.loads(f.read_text())
        seen_ids = set()
        for i, record in enumerate(records):
            count += 1
            for err in validator.iter_errors(record):
                errors.append(
                    f"data/extracted/{f.name}[{i}] ({record.get('id', '?')}): "
                    f"{'/'.join(str(p) for p in err.path)}: {err.message}"
                )
            rid = record.get("id")
            if rid in seen_ids:
                errors.append(f"data/extracted/{f.name}[{i}]: duplicate id {rid!r}")
            seen_ids.add(rid)
    return errors, count


def check_local_verbatim() -> list[str]:
    """D-009: public extraction files have source_text scrubbed to the
    placeholder LOCAL_VERBATIM_PLACEHOLDER; the real verbatim text lives
    only in data/local/<name>-verbatim.json (git-ignored), keyed by
    record id. When present locally, every record id in the public file
    must have a matching verbatim entry and vice versa. When absent
    (e.g. in CI, which never has data/local/), the check is skipped with
    a printed notice rather than failing — data/local/ is never expected
    to exist there.
    """
    errors = []
    if not LOCAL_DIR.exists():
        print("data/local/ not present — skipping local-verbatim cross-check (expected in CI).")
        return errors

    for verbatim_file in sorted(LOCAL_DIR.glob("*-verbatim.json")):
        base_name = verbatim_file.name.removesuffix("-verbatim.json") + ".json"
        if base_name in ID_KEYED_VERBATIM_EXCLUSIONS:
            continue
        public_file = EXTRACTED_DIR / base_name
        if not public_file.exists():
            errors.append(f"data/local/{verbatim_file.name}: no matching public file data/extracted/{base_name}")
            continue

        verbatim_ids = set(json.loads(verbatim_file.read_text()).keys())
        public_records = json.loads(public_file.read_text())
        public_ids = {r["id"] for r in public_records}

        missing_verbatim = public_ids - verbatim_ids
        for rid in sorted(missing_verbatim):
            errors.append(f"data/extracted/{base_name}: record {rid!r} has no entry in data/local/{verbatim_file.name}")

        orphan_verbatim = verbatim_ids - public_ids
        for rid in sorted(orphan_verbatim):
            errors.append(f"data/local/{verbatim_file.name}: entry {rid!r} has no matching record in data/extracted/{base_name}")

    return errors


def check_verbatim_leak() -> list[str]:
    """D-010 (CR-3): even with source_text scrubbed (D-009), other public
    text fields (e.g. generalized_text, needs_review_note) could leak
    verbatim CC-BY-ND text by accident. When data/local/*-verbatim.json is
    present, assert that no text field in any public /data/extracted file
    equals, or contains a contiguous >15-word span of, any local verbatim
    entry. Skipped (with a printed notice) when the local file is absent,
    since that's always true in CI.
    """
    errors = []
    if not LOCAL_DIR.exists():
        print("data/local/ not present — skipping verbatim-leak check (expected in CI).")
        return errors

    def word_spans(text: str, n: int = 16):
        words = text.split()
        for i in range(len(words) - n + 1):
            yield " ".join(words[i : i + n])

    def walk_strings(value):
        if isinstance(value, str):
            yield value
        elif isinstance(value, dict):
            for v in value.values():
                yield from walk_strings(v)
        elif isinstance(value, list):
            for v in value:
                yield from walk_strings(v)

    for verbatim_file in sorted(LOCAL_DIR.glob("*-verbatim.json")):
        base_name = verbatim_file.name.removesuffix("-verbatim.json") + ".json"
        public_file = EXTRACTED_DIR / base_name
        if not public_file.exists():
            continue

        verbatim_entries = json.loads(verbatim_file.read_text())
        leak_spans = set()
        for entry in verbatim_entries.values():
            for text in walk_strings(entry):
                leak_spans.update(word_spans(text))

        public_data = json.loads(public_file.read_text())
        # Most public files are arrays of {"id": ...} control records;
        # ecsf-guidance.json/cada-scope.json are single nested objects
        # instead. Both are covered: walk_strings already recurses through
        # dicts/lists, so
        # for a bare object we just scan it as one unit rather than
        # per-record.
        records = public_data if isinstance(public_data, list) else [public_data]
        for record in records:
            label = record.get("id", "?") if isinstance(record, dict) else "?"
            for text in walk_strings(record):
                for span in word_spans(text):
                    if span in leak_spans:
                        errors.append(
                            f"data/extracted/{base_name}: record {label!r} "
                            f"contains a >15-word span matching local verbatim text: {span!r}"
                        )
                        break

    return errors


def check_verbatim_placeholder_count() -> list[str]:
    """Completeness check for the ID_KEYED_VERBATIM_EXCLUSIONS set
    (ecsf-guidance.json, ecsf-calculator.json, cada-scope.json,
    cada-evidence.json), whose local verbatim keys don't line up with a
    public record id (see that constant's docstring note). Since
    check_local_verbatim's id-set cross-check is skipped for these, this
    instead asserts that the count of SEE-LOCAL-VERBATIM placeholders in
    the public file equals the number of entries in the matching local
    verbatim file — a weaker but shape-agnostic completeness signal that
    catches the same class of drift (a field scrubbed but never isolated,
    or vice versa).
    """
    errors = []
    if not LOCAL_DIR.exists():
        return errors

    def count_placeholders(value) -> int:
        if isinstance(value, str):
            return 1 if value == "SEE-LOCAL-VERBATIM" else 0
        if isinstance(value, dict):
            return sum(count_placeholders(v) for v in value.values())
        if isinstance(value, list):
            return sum(count_placeholders(v) for v in value)
        return 0

    for base_name in sorted(ID_KEYED_VERBATIM_EXCLUSIONS):
        verbatim_file = LOCAL_DIR / (base_name.removesuffix(".json") + "-verbatim.json")
        public_file = EXTRACTED_DIR / base_name
        if not verbatim_file.exists() or not public_file.exists():
            continue

        local_count = len(json.loads(verbatim_file.read_text()))
        public_count = count_placeholders(json.loads(public_file.read_text()))
        if local_count != public_count:
            errors.append(
                f"data/extracted/{base_name}: {public_count} SEE-LOCAL-VERBATIM "
                f"placeholder(s) but data/local/{verbatim_file.name} has "
                f"{local_count} entries — these should match"
            )

    return errors


def check_ecsf_scoring(schemas: dict[str, dict], registry: Registry) -> list[str]:
    """Validates data/extracted/ecsf-scoring.json (Phase 2b) against
    ecsf-scoring.schema.json, if present. Not a control-record array, so
    handled separately from check_extracted_records().
    """
    errors = []
    f = EXTRACTED_DIR / "ecsf-scoring.json"
    if not f.exists():
        return errors
    validator = Draft202012Validator(
        schemas["ecsf-scoring.schema.json"], registry=registry
    )
    data = json.loads(f.read_text())
    for err in validator.iter_errors(data):
        errors.append(f"data/extracted/ecsf-scoring.json: {'/'.join(str(p) for p in err.path)}: {err.message}")
    return errors


def check_ecsf_c3a_hints() -> list[str]:
    """Validates data/extracted/ecsf-c3a-hints.json (Phase 2b), if present:
    every ecsf record id referenced as a key must exist in ecsf.json, every
    entry must be an object {"coverage": "covered"|"uncovered",
    "c3a_candidates": [...]} (D-013, CR-1 — no bare lists, no "uncovered"
    sentinel), c3a_candidates must be non-empty iff coverage is "covered"
    and empty iff "uncovered", and every referenced c3a id must exist in
    c3a.json. These hints are UNVERIFIED candidates for the Phase 3
    crosswalk, not authoritative — this check only guards against
    typos/dangling ids/malformed entries, not correctness of the mapping
    itself.
    """
    errors = []
    f = EXTRACTED_DIR / "ecsf-c3a-hints.json"
    if not f.exists():
        return errors

    ecsf_file = EXTRACTED_DIR / "ecsf.json"
    c3a_file = EXTRACTED_DIR / "c3a.json"
    ecsf_ids = {r["id"] for r in json.loads(ecsf_file.read_text())} if ecsf_file.exists() else set()
    c3a_ids = {r["id"] for r in json.loads(c3a_file.read_text())} if c3a_file.exists() else set()

    hints = json.loads(f.read_text())
    for ecsf_id, entry in hints.items():
        if ecsf_id not in ecsf_ids:
            errors.append(f"data/extracted/ecsf-c3a-hints.json: key {ecsf_id!r} does not match any id in ecsf.json")

        if not isinstance(entry, dict):
            errors.append(f"data/extracted/ecsf-c3a-hints.json: {ecsf_id!r} entry must be an object with 'coverage' and 'c3a_candidates', not a bare list")
            continue

        coverage = entry.get("coverage")
        candidates = entry.get("c3a_candidates")

        if coverage not in ("covered", "uncovered"):
            errors.append(f"data/extracted/ecsf-c3a-hints.json: {ecsf_id!r} has invalid coverage {coverage!r} (must be 'covered' or 'uncovered')")
            continue

        if not isinstance(candidates, list):
            errors.append(f"data/extracted/ecsf-c3a-hints.json: {ecsf_id!r} c3a_candidates must be a list")
            continue

        if coverage == "covered" and len(candidates) == 0:
            errors.append(f"data/extracted/ecsf-c3a-hints.json: {ecsf_id!r} coverage is 'covered' but c3a_candidates is empty")
        if coverage == "uncovered" and len(candidates) != 0:
            errors.append(f"data/extracted/ecsf-c3a-hints.json: {ecsf_id!r} coverage is 'uncovered' but c3a_candidates is non-empty")

        for c in candidates:
            if c == "uncovered":
                errors.append(f"data/extracted/ecsf-c3a-hints.json: {ecsf_id!r} contains the sentinel string 'uncovered' as a candidate id, which is no longer accepted (use coverage: \"uncovered\" with an empty list)")
                continue
            if c not in c3a_ids:
                errors.append(f"data/extracted/ecsf-c3a-hints.json: {ecsf_id!r} references unknown C3A id {c!r}")

    return errors


def check_ecsf_guidance(schemas: dict[str, dict], registry: Registry) -> list[str]:
    """Validates data/extracted/ecsf-guidance.json (Phase 2b.1) against
    ecsf-guidance.schema.json, if present.
    """
    errors = []
    f = EXTRACTED_DIR / "ecsf-guidance.json"
    if not f.exists():
        return errors
    validator = Draft202012Validator(schemas["ecsf-guidance.schema.json"], registry=registry)
    data = json.loads(f.read_text())
    for err in validator.iter_errors(data):
        errors.append(f"data/extracted/ecsf-guidance.json: {'/'.join(str(p) for p in err.path)}: {err.message}")
    return errors


def check_ecsf_calculator(schemas: dict[str, dict], registry: Registry) -> list[str]:
    """Validates data/extracted/ecsf-calculator.json (Phase 2b.1) against
    ecsf-calculator.schema.json, if present. Also checks that every
    ecsf_factor_hints.ecsf_factor_candidates id exists in ecsf.json, and
    id uniqueness, since the schema itself can't enforce cross-file
    references or array-wide uniqueness.
    """
    errors = []
    f = EXTRACTED_DIR / "ecsf-calculator.json"
    if not f.exists():
        return errors
    validator = Draft202012Validator(schemas["ecsf-calculator.schema.json"], registry=registry)
    data = json.loads(f.read_text())
    for err in validator.iter_errors(data):
        errors.append(f"data/extracted/ecsf-calculator.json: {'/'.join(str(p) for p in err.path)}: {err.message}")

    ecsf_file = EXTRACTED_DIR / "ecsf.json"
    ecsf_ids = {r["id"] for r in json.loads(ecsf_file.read_text())} if ecsf_file.exists() else set()
    seen_ids = set()
    for record in data:
        rid = record.get("id")
        if rid in seen_ids:
            errors.append(f"data/extracted/ecsf-calculator.json: duplicate id {rid!r}")
        seen_ids.add(rid)
        for c in record.get("ecsf_factor_hints", {}).get("ecsf_factor_candidates", []):
            if c not in ecsf_ids:
                errors.append(f"data/extracted/ecsf-calculator.json: {rid!r} references unknown ecsf.json id {c!r}")

    return errors


def check_cada_scope() -> list[str]:
    """Structural check for data/extracted/cada-scope.json (Phase 2c),
    if present: not a control-record array, and not validated against a
    dedicated schema (none is authorized for this small file — it just
    carries Annex II's introductory scope statement as file-level
    metadata), so just check the fields the extraction script and any
    downstream reader depend on are present.
    """
    errors = []
    f = EXTRACTED_DIR / "cada-scope.json"
    if not f.exists():
        return errors
    data = json.loads(f.read_text())
    for field in ("document", "annex", "scope_statement", "in_scope", "out_of_scope", "source_pointer"):
        if field not in data:
            errors.append(f"data/extracted/cada-scope.json: missing required field {field!r}")
    return errors


def check_cada_evidence(schemas: dict[str, dict], registry: Registry) -> list[str]:
    """Validates data/extracted/cada-evidence.json (Phase 2c) against
    cada-evidence.schema.json, if present.
    """
    errors = []
    f = EXTRACTED_DIR / "cada-evidence.json"
    if not f.exists():
        return errors
    validator = Draft202012Validator(schemas["cada-evidence.schema.json"], registry=registry)
    data = json.loads(f.read_text())
    for err in validator.iter_errors(data):
        errors.append(f"data/extracted/cada-evidence.json: {'/'.join(str(p) for p in err.path)}: {err.message}")
    return errors


def check_cada_act() -> list[str]:
    """Structural check for data/extracted/cada-act.json (Phase 2c), if
    present. Deliberately NOT validated against control-record.schema.json
    (D-017): these are obligations on the assessing government / plain
    definitions, not provider-facing criteria with a layer/disposition, so
    that schema's shape doesn't fit. No new schema is authorized for this
    file either, so this is a plain structural check instead.
    """
    errors = []
    f = EXTRACTED_DIR / "cada-act.json"
    if not f.exists():
        return errors
    records = json.loads(f.read_text())
    seen_ids = set()
    required = {"id", "derivation", "source_refs", "title", "obligation_text", "source_pointer", "needs_review"}
    for i, r in enumerate(records):
        missing = required - r.keys()
        if missing:
            errors.append(f"data/extracted/cada-act.json[{i}] ({r.get('id', '?')}): missing field(s) {sorted(missing)}")
        if r.get("derivation") != "derived":
            errors.append(f"data/extracted/cada-act.json[{i}] ({r.get('id', '?')}): derivation must be 'derived'")
        if r.get("needs_review") and "needs_review_note" not in r:
            errors.append(f"data/extracted/cada-act.json[{i}] ({r.get('id', '?')}): needs_review is true but needs_review_note is missing")
        rid = r.get("id")
        if rid in seen_ids:
            errors.append(f"data/extracted/cada-act.json: duplicate id {rid!r}")
        seen_ids.add(rid)
    return errors


def main() -> int:
    schemas, registry = load_schemas()

    errors = check_schemas_are_valid(schemas)
    persona_errors, draft_count, approved_count = check_personas(schemas, registry)
    errors.extend(persona_errors)
    extracted_errors, extracted_count = check_extracted_records(schemas, registry)
    errors.extend(extracted_errors)
    errors.extend(check_local_verbatim())
    errors.extend(check_verbatim_leak())
    errors.extend(check_verbatim_placeholder_count())
    errors.extend(check_ecsf_scoring(schemas, registry))
    errors.extend(check_ecsf_c3a_hints())
    errors.extend(check_ecsf_guidance(schemas, registry))
    errors.extend(check_ecsf_calculator(schemas, registry))
    errors.extend(check_cada_scope())
    errors.extend(check_cada_evidence(schemas, registry))
    errors.extend(check_cada_act())

    print(f"Schemas checked: {len(schemas)}")
    print(f"Personas checked: {draft_count + approved_count} ({draft_count} draft, {approved_count} approved)")
    print(f"Extracted control records checked: {extracted_count}")

    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
