#!/usr/bin/env python3
"""Validate DMFD Witch localization files without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LOCALIZATION_ROOT = ROOT / "localization"
REFERENCE_LOCALE = "zhs"
PLACEHOLDER_RE = re.compile(r"(?<!\{)\{([^{}\r\n]+)\}(?!\})")


class DuplicateKeyError(ValueError):
    pass


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate key {key!r}")
        result[key] = value
    return result


def load_file(path: Path, errors: list[str]) -> dict[str, str] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys)
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return None

    if not isinstance(data, dict):
        errors.append(f"{path.relative_to(ROOT)}: top-level JSON value must be an object")
        return None

    bad_values = [key for key, value in data.items() if not isinstance(value, str)]
    if bad_values:
        errors.append(
            f"{path.relative_to(ROOT)}: values must be strings; invalid keys: "
            + ", ".join(sorted(bad_values))
        )
        return None
    return data


def placeholder_signatures(value: str) -> Counter[str]:
    signatures: Counter[str] = Counter()
    for match in PLACEHOLDER_RE.finditer(value):
        parts = match.group(1).split(":", 2)
        signature = parts[0] if len(parts) == 1 else f"{parts[0]}:{parts[1]}"
        signatures[signature] += 1
    return signatures


def main() -> int:
    errors: list[str] = []
    reference_dir = LOCALIZATION_ROOT / REFERENCE_LOCALE
    if not reference_dir.is_dir():
        print(f"Missing reference locale: {reference_dir}", file=sys.stderr)
        return 1

    locale_dirs = sorted(path for path in LOCALIZATION_ROOT.iterdir() if path.is_dir())
    if not locale_dirs:
        print("No locale directories found", file=sys.stderr)
        return 1

    reference_files = {path.name for path in reference_dir.glob("*.json")}
    reference_data: dict[str, dict[str, str]] = {}
    for file_name in sorted(reference_files):
        loaded = load_file(reference_dir / file_name, errors)
        if loaded is not None:
            reference_data[file_name] = loaded

    for locale_dir in locale_dirs:
        locale_files = {path.name for path in locale_dir.glob("*.json")}
        missing_files = sorted(reference_files - locale_files)
        extra_files = sorted(locale_files - reference_files)
        if missing_files:
            errors.append(f"{locale_dir.name}: missing files: {', '.join(missing_files)}")
        if extra_files:
            errors.append(f"{locale_dir.name}: extra files: {', '.join(extra_files)}")

        for file_name in sorted(reference_files & locale_files):
            localized = load_file(locale_dir / file_name, errors)
            reference = reference_data.get(file_name)
            if localized is None or reference is None:
                continue

            reference_keys = set(reference)
            localized_keys = set(localized)
            missing_keys = sorted(reference_keys - localized_keys)
            extra_keys = sorted(localized_keys - reference_keys)
            if missing_keys:
                errors.append(
                    f"{locale_dir.name}/{file_name}: missing keys: {', '.join(missing_keys)}"
                )
            if extra_keys:
                errors.append(
                    f"{locale_dir.name}/{file_name}: extra keys: {', '.join(extra_keys)}"
                )

            for key in sorted(reference_keys & localized_keys):
                expected = placeholder_signatures(reference[key])
                actual = placeholder_signatures(localized[key])
                if actual != expected:
                    errors.append(
                        f"{locale_dir.name}/{file_name}:{key}: placeholder mismatch; "
                        f"expected {dict(expected)}, got {dict(actual)}"
                    )

    if errors:
        print("Localization validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    file_count = len(reference_files)
    print(f"Validated {len(locale_dirs)} locales against {REFERENCE_LOCALE} ({file_count} files each).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
