# Copyright (C) 2025 Nobleo Autonomous Solutions B.V.
"""YAML formatter using yamlfix.

Formats YAML files but does NOT add --- if absent (preserves if present).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from yamlfix import fix_code
from yamlfix.model import YamlfixConfig, YamlNodeStyle


def _yamlfix_config() -> YamlfixConfig:
    config = YamlfixConfig()
    config.sequence_style = YamlNodeStyle.KEEP_STYLE
    config.line_length = 256
    config.whitelines = 1
    config.explicit_start = False
    return config


def format_yaml(source: str) -> str:
    """Format YAML source, preserving --- if present but not adding it."""
    if not source:
        return source
    had_explicit_start = source.lstrip().startswith('---')
    result = fix_code(source, _yamlfix_config())
    # Strip trailing whitespace per line
    result = '\n'.join(line.rstrip() for line in result.split('\n'))
    # Restore --- if it was present but got stripped
    if had_explicit_start and not result.lstrip().startswith('---'):
        result = '---\n' + result
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description='Format YAML files')
    parser.add_argument('files', nargs='*', help='YAML files to format')
    args = parser.parse_args()

    if not args.files:
        return 0

    errors = []
    changed = []
    for filepath in args.files:
        path = Path(filepath)
        try:
            original = path.read_text(encoding='utf-8')
            formatted = format_yaml(original)
        except Exception as exc:  # noqa: BLE001
            errors.append(f'{filepath}: {exc}')
            continue
        if formatted != original:
            path.write_text(formatted, encoding='utf-8')
            changed.append(filepath)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
    if changed:
        print('Files reformatted — please re-stage and recommit:')
        for f in changed:
            print(f'  {f}')

    return 1 if errors or changed else 0


if __name__ == '__main__':
    sys.exit(main())
