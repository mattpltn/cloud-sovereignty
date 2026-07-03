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


def main() -> int:
    schemas, registry = load_schemas()

    errors = check_schemas_are_valid(schemas)
    persona_errors, draft_count, approved_count = check_personas(schemas, registry)
    errors.extend(persona_errors)

    # /data/catalog validation is added in Phase 2+ once extraction produces
    # control records to validate against control-record.schema.json.

    print(f"Schemas checked: {len(schemas)}")
    print(f"Personas checked: {draft_count + approved_count} ({draft_count} draft, {approved_count} approved)")

    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
