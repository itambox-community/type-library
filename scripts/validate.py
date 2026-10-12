#!/usr/bin/env python3
"""Validate catalogue YAML files against the generated schema.

Checks per file under asset-types/:
  1. the YAML parses to a mapping,
  2. manufacturer, model and category are present,
  3. the mapping validates against schema/asset-type.json (which references the
     generated schema copied from a webapp release),
  4. the path is asset-types/<manufacturer>/<model>.yaml.

Usage: validate.py [FILE ...]   (no arguments: every file under asset-types/)
Exit status is 1 when any file has a problem.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schema"
REQUIRED = ("manufacturer", "model", "category")
FORBIDDEN_NAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
UNIT_RE = re.compile(r"^Value in (?P<unit>.+)$")


def build_validator() -> Draft202012Validator:
    generated = json.loads((SCHEMA_DIR / "generated_schema.json").read_text(encoding="utf-8"))
    wrapper = json.loads((SCHEMA_DIR / "asset-type.json").read_text(encoding="utf-8"))
    registry = Registry().with_resources(
        [
            (urljoin(wrapper["$id"], "generated_schema.json"), Resource.from_contents(generated)),
        ]
    )
    return Draft202012Validator(wrapper, registry=registry)


def _spec_schemas() -> dict:
    generated = json.loads((SCHEMA_DIR / "generated_schema.json").read_text(encoding="utf-8"))
    return generated["properties"]["specs"]["properties"]


def describe_error(error, spec_schemas: dict) -> str:
    path = ".".join(str(p) for p in error.absolute_path) or "(file)"
    parts = list(error.absolute_path)
    if len(parts) == 2 and parts[0] == "specs" and error.validator == "pattern":
        key = parts[1]
        match = UNIT_RE.match(spec_schemas.get(key, {}).get("description", ""))
        if match:
            unit = match.group("unit")
            return (
                f"specs.{key}: {error.instance!r} is not valid; expected '<number> {unit}' "
                f"(vocabulary unit only, e.g. '12 {unit}')"
            )
    if error.validator == "additionalProperties" and len(parts) <= 1:
        return f"{path}: {error.message} (only keys of the generated schema are allowed)"
    if error.validator == "enum":
        return f"{path}: {error.instance!r} is not one of {error.validator_value}"
    return f"{path}: {error.message}"


def check_path(path: Path, data: dict) -> list[str]:
    problems = []
    try:
        relative = path.resolve().relative_to(ROOT)
    except ValueError:
        return [f"{path}: file is outside the repository"]
    manufacturer, model = data.get("manufacturer"), data.get("model")
    if not isinstance(manufacturer, str) or not isinstance(model, str):
        return problems
    for label, value in (("manufacturer", manufacturer), ("model", model)):
        if not value.strip() or value != value.strip() or FORBIDDEN_NAME_CHARS.search(value):
            problems.append(
                f"{label}: {value!r} must not be empty, padded with spaces or contain any of < > : \" / \\ | ? * "
            )
    if problems:
        return problems
    expected = Path("asset-types") / manufacturer / f"{model}.yaml"
    if relative != expected:
        problems.append(
            f"path: file is {relative.as_posix()} but manufacturer/model require {expected.as_posix()}"
        )
    return problems


def check_file(path: Path, validator: Draft202012Validator, spec_schemas: dict) -> list[str]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (yaml.YAMLError, UnicodeDecodeError) as exc:
        return [f"invalid YAML: {exc}"]
    if not isinstance(data, dict):
        return ["top level must be a mapping with manufacturer, model, category and specs"]
    problems = [f"{key}: required field is missing" for key in REQUIRED if key not in data]
    errors = sorted(validator.iter_errors(data), key=lambda e: [str(p) for p in e.absolute_path])
    problems.extend(describe_error(e, spec_schemas) for e in errors)
    problems.extend(check_path(path, data))
    return problems


def main(argv: list[str]) -> int:
    validator = build_validator()
    spec_schemas = _spec_schemas()
    if argv:
        files = [Path(a) for a in argv]
    else:
        files = sorted(
            p for p in (ROOT / "asset-types").rglob("*") if p.is_file() and p.suffix in {".yaml", ".yml"}
        )
    stray = [
        p for p in (ROOT / "asset-types").rglob("*") if p.is_file() and p.suffix != ".yaml" and p.name != "README.md"
    ]
    failed = 0
    for path in stray:
        print(f"::error file={path.relative_to(ROOT).as_posix()}::catalogue files must use the .yaml extension")
        failed += 1
    for path in files:
        problems = check_file(path, validator, spec_schemas)
        shown = path.resolve().relative_to(ROOT).as_posix() if path.resolve().is_relative_to(ROOT) else str(path)
        for problem in problems:
            print(f"::error file={shown}::{problem}")
            print(f"{shown}: {problem}")
        failed += bool(problems)
    print(f"checked {len(files)} file(s), {failed} with problems")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
