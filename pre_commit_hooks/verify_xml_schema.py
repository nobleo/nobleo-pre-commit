#!/usr/bin/env python3

# Copyright (C) 2026 Nobleo Autonomous Solutions B.V.

"""Verify that XML files with a schema reference validate against that schema."""

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import xmlschema


def find_schema_url(filepath: Path) -> str | None:
    """Extract the schema URL from an XML file.

    Supports:
    - <?xml-model href="..." schematypens="http://www.w3.org/2001/XMLSchema"?>
    - xsi:schemaLocation="namespace schema_url"
    - xsi:noNamespaceSchemaLocation="schema_url"
    """
    try:
        content = filepath.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError) as e:
        print(f'Error reading {filepath}: {e}', file=sys.stderr)
        return None

    # Check for <?xml-model?> processing instruction with XSD schematypens
    match = re.search(
        r'<\?xml-model\s[^?]*href=["\']([^"\']+)["\']'
        r'[^?]*schematypens=["\']http://www\.w3\.org/2001/XMLSchema["\']',
        content,
    ) or re.search(
        r'<\?xml-model\s[^?]*schematypens=["\']http://www\.w3\.org/2001/XMLSchema["\']'
        r'[^?]*href=["\']([^"\']+)["\']',
        content,
    )
    if match:
        return match.group(1)

    # Check for xsi:noNamespaceSchemaLocation or xsi:schemaLocation attributes
    try:
        root = ET.parse(filepath).getroot()
    except ET.ParseError:
        return None

    xsi = 'http://www.w3.org/2001/XMLSchema-instance'
    no_ns_loc = root.get(f'{{{xsi}}}noNamespaceSchemaLocation')
    if no_ns_loc:
        return no_ns_loc.strip()
    schema_loc = root.get(f'{{{xsi}}}schemaLocation')
    if schema_loc:
        parts = schema_loc.split()
        if len(parts) >= 2:
            return parts[1]

    return None


def main() -> int:
    """Main entry point for the pre-commit hook."""
    parser = argparse.ArgumentParser(
        description='Validate XML files against their declared XSD schema'
    )
    parser.add_argument('filenames', nargs='*', type=Path, help='XML files to check')
    args = parser.parse_args()

    all_ok = True
    for filepath in args.filenames:
        if not filepath.exists():
            print(f'File not found: {filepath}', file=sys.stderr)
            all_ok = False
            continue

        schema_url = find_schema_url(filepath)
        if schema_url is None:
            continue

        try:
            schema = xmlschema.XMLSchema(schema_url)
            schema.validate(str(filepath))
        except xmlschema.XMLSchemaValidationError as e:
            all_ok = False
            print(f'{filepath}: {e.reason} (path: {e.path})')
        except xmlschema.XMLSchemaException as e:
            all_ok = False
            print(f'{filepath}: {e}')

    return 0 if all_ok else 1


if __name__ == '__main__':
    exit(main())
