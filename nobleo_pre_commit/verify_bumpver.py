#!/usr/bin/env python3

# Copyright (C) 2025 Nobleo Autonomous Solutions B.V.

from bumpver.cli import cli
from click.testing import CliRunner


def main():
    runner = CliRunner()
    # Try to bump minor version, --minor will be ignored if calver is used
    result = runner.invoke(cli, ['update', '--minor', '--dry', '--no-fetch'])
    if result.exit_code != 0 and 'File not found' not in result.output:
        print(result.output)
        return result.exit_code
    return 0


if __name__ == '__main__':
    exit(main())
