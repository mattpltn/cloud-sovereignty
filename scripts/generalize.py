#!/usr/bin/env python3
"""Phase 2d-i: the generalization engine.

generalize(text, rules) is a pure, deterministic function: the same
(verbatim text, rule table) always produces the same generalized text,
with no external state — this is what makes scripts/validate.py's
equality check ("generalized_text == generalize(verbatim, rules) for
every generalization_class: direct record") meaningful and idempotent
(re-running this script never changes an already-generalized record).

Usage:
  .venv/bin/python3 scripts/generalize.py <framework> [SOV-domain]

  <framework> is the basename of data/extracted/<framework>.json and
  data/local/<framework>-verbatim.json (e.g. "c3a"). If a SOV-domain
  (e.g. "SOV-1") is given, only records in that domain are processed
  (batch-by-domain, one commit each, per working rule 1); otherwise all
  records in the file are processed.
"""

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
RULES_PATH = ROOT / "data" / "rules" / "generalization-rules.yaml"
EXTRACTED_DIR = ROOT / "data" / "extracted"
LOCAL_DIR = ROOT / "data" / "local"
FR_PENDING = "FR-TRANSLATION-PENDING"


def load_rules(path: Path = RULES_PATH) -> tuple[list[dict], dict[str, dict]]:
    data = yaml.safe_load(path.read_text())
    rules = data["rules"]
    overrides = {o["id"]: o for o in data.get("overrides", [])}
    return rules, overrides


def generalize(text: str, rules: list[dict]) -> str:
    """Applies every rule with a non-null pattern, in list order."""
    for rule in rules:
        pattern = rule.get("pattern")
        if pattern is None:
            continue  # documentation-only rule (R4, R7, R8, R9 in Phase 2d-i)
        text = re.sub(pattern, rule["replacement"], text)
    return text


def generalize_record(record_id: str, verbatim_en: str, rules: list[dict], overrides: dict[str, dict]) -> tuple[str, str | None, str]:
    """Returns (generalized_text_en, generalization_note_en_or_None, generalization_class).

    Checks the overrides table first, by record id, so an overridden
    record's generalized_text IS what this function returns for that
    id. Most overrides stay generalization_class: direct (the override
    IS what this function returns for that id, so the equality check in
    scripts/validate.py still holds); an override may set
    `generalization_class_override` (e.g. "structural_adaptation") when
    the divergence isn't a mechanical rule substitution at all — see
    the rules file's own docstring and csat-sov1-cada-ua3-g (D-017/R8).
    """
    if record_id in overrides:
        override = overrides[record_id]
        gclass = override.get("generalization_class_override", "direct")
        return override["generalized_text"].strip(), override.get("generalization_note", "").strip() or None, gclass
    return generalize(verbatim_en, rules), None, "direct"


def apply_to_file(framework: str, domain: str | None = None) -> int:
    public_path = EXTRACTED_DIR / f"{framework}.json"
    local_path = LOCAL_DIR / f"{framework}-verbatim.json"
    rules, overrides = load_rules()

    public = json.loads(public_path.read_text())
    verbatim = json.loads(local_path.read_text())

    changed = 0
    for record in public:
        if domain is not None and record.get("sov_domain") != domain:
            continue
        rid = record["id"]
        if rid not in verbatim:
            continue  # not this framework's concern here; check_local_verbatim covers completeness
        gen_text, note, gclass = generalize_record(rid, verbatim[rid]["en"], rules, overrides)
        record["generalized_text"] = {"en": gen_text, "fr": FR_PENDING}
        record["generalization_class"] = gclass
        if note:
            record["generalization_note"] = {"en": note, "fr": FR_PENDING}
        changed += 1

    public_path.write_text(json.dumps(public, indent=2, ensure_ascii=False) + "\n")
    return changed


def main() -> None:
    if len(sys.argv) not in (2, 3):
        print("Usage: generalize.py <framework> [SOV-domain]")
        raise SystemExit(1)
    framework = sys.argv[1]
    domain = sys.argv[2] if len(sys.argv) == 3 else None
    changed = apply_to_file(framework, domain)
    scope = f" ({domain})" if domain else ""
    print(f"Generalized {changed} record(s) in {framework}.json{scope}")


if __name__ == "__main__":
    main()
