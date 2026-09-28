#!/usr/bin/env python3
"""Fill a Word template (.docx) with extracted key/value data."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from docxtpl import DocxTemplate
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: docxtpl. Install it with `pip install docxtpl`."
    ) from exc


LINE_PATTERN = re.compile(r"^\s*([^:：]+?)\s*[:：]\s*(.*?)\s*$")


def parse_material_text(content: str) -> dict[str, str]:
    """Extract fields from lines formatted as `字段: 值` or `字段：值`."""
    data: dict[str, str] = {}
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = LINE_PATTERN.match(line)
        if not match:
            continue
        key, value = match.groups()
        data[key.strip()] = value.strip()
    return data


def load_data(data_json: Path | None, material_txt: Path | None) -> dict[str, str]:
    if data_json:
        return json.loads(data_json.read_text(encoding="utf-8"))
    if material_txt:
        return parse_material_text(material_txt.read_text(encoding="utf-8"))
    raise ValueError("Either --data-json or --material-txt must be provided.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fill a .docx template while keeping original template formatting."
    )
    parser.add_argument("--template", required=True, type=Path, help="Input .docx template")
    parser.add_argument("--output", required=True, type=Path, help="Output .docx file")

    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--data-json", type=Path, help="JSON file with template variables")
    source.add_argument(
        "--material-txt",
        type=Path,
        help="Plain-text material with one `字段: 值` per line",
    )

    args = parser.parse_args()

    if not args.template.exists():
        raise SystemExit(f"Template not found: {args.template}")

    data = load_data(args.data_json, args.material_txt)
    if not isinstance(data, dict):
        raise SystemExit("Input data must be a JSON object or parse into key/value pairs.")

    doc = DocxTemplate(str(args.template))
    doc.render(data)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(args.output))

    missing = [k for k, v in data.items() if v is None]
    if missing:
        print(f"Warning: some fields are empty: {', '.join(missing)}", file=sys.stderr)

    print(f"Generated: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
