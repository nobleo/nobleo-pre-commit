#!/usr/bin/env python3
"""Verify that all packages referenced in ROS2 launch files are declared as dependencies."""

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def find_package_xml(launch_file: Path) -> Path:
    """Recursively search for package.xml from the launch file's directory upwards."""
    # Resolve to absolute path
    current = launch_file.resolve().parent
    while current != current.parent:
        package_xml = current / "package.xml"
        if package_xml.exists():
            return package_xml
        current = current.parent
    raise FileNotFoundError(f"Could not find package.xml for {launch_file}")


def parse_package_xml(package_xml: Path) -> set[str]:
    """Extract all package dependencies from package.xml."""
    try:
        tree = ET.parse(package_xml)
        root = tree.getroot()

        dependencies = set()
        # Look for valid dependencies
        for dep in (
            root.findall(".//name")
            + root.findall(".//depend")
            + root.findall(".//exec_depend")
            + root.findall(".//test_depend")
        ):
            if dep.text:
                dependencies.add(dep.text.strip())
        return dependencies
    except ET.ParseError as e:
        print(f"Error parsing {package_xml}: {e}", file=sys.stderr)
        return set()


def extract_packages_from_launch(launch_file: Path) -> set[str]:
    """Extract all package references from a ROS2 launch file."""
    pkgs = set()

    try:
        tree = ET.parse(launch_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing {launch_file}: {e}", file=sys.stderr)
        return pkgs

    # Find all node elements and extract pkg attribute
    for node in root.findall(".//node"):
        pkg = node.get("pkg")
        if pkg:
            pkgs.add(pkg)

    # Find find_pkg_share() calls in string attributes
    # This catches things like $(find_pkg_share 'some_package') or $(find-pkg-share 'some_package')
    xml_str = ET.tostring(root, encoding='unicode')

    # Pattern for $(find_pkg_share pkg_name) or $(find-pkg-share pkg_name) format used in ROS2 launch files
    # Both underscore and hyphen variants are used
    find_pkg_pattern_ros2 = r"\$\(find[-_]pkg[-_]share\s+([^\)]+)\)"
    for match in re.finditer(find_pkg_pattern_ros2, xml_str):
        pkg = match.group(1).strip().strip("'\"")
        pkgs.add(pkg)

    return pkgs


def verify_launch_file(launch_file: Path) -> list[str]:
    """Verify that all packages in launch file are declared as dependencies.

    Returns a list of error messages. Empty list means no errors.
    """
    errors = []

    try:
        package_xml = find_package_xml(launch_file)
    except FileNotFoundError as e:
        return [str(e)]

    declared_deps = parse_package_xml(package_xml)
    referenced_pkgs = extract_packages_from_launch(launch_file)

    # Find missing dependencies
    missing = referenced_pkgs - declared_deps

    if missing:
        for pkg in sorted(missing):
            errors.append(
                f"{launch_file}: Package '{pkg}' is referenced but not declared "
                f"as <depend>, <exec_depend> or <test_depend> in {package_xml.name}"
            )

    return errors


def main() -> int:
    """Main entry point for the pre-commit hook."""
    parser = argparse.ArgumentParser(
        description="Verify that all packages in ROS2 launch files are declared as dependencies"
    )
    parser.add_argument(
        "filenames", nargs="*", type=Path, help="Launch files to check (*.launch.xml)"
    )

    args = parser.parse_args()

    if not args.filenames:
        return 0

    all_ok = True
    for launch_file in args.filenames:
        # Only process .launch.xml files
        if not launch_file.name.endswith(".launch.xml"):
            continue

        if not launch_file.exists():
            print(f"File not found: {launch_file}", file=sys.stderr)
            all_ok = False
            continue

        errors = verify_launch_file(launch_file)
        if errors:
            all_ok = False
            for error in errors:
                print(error)

    return 0 if all_ok else 1


if __name__ == '__main__':
    exit(main())
