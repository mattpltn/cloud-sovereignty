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

        public_records = json.loads(public_file.read_text())
        for record in public_records:
            for text in walk_strings(record):
                for span in word_spans(text):
                    if span in leak_spans:
                        errors.append(
                            f"data/extracted/{base_name}: record {record.get('id', '?')!r} "
                            f"contains a >15-word span matching local verbatim text: {span!r}"
                        )
                        break

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
