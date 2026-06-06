#!/usr/bin/env python3
"""Mass update of all user-installed pip packages."""

import subprocess
import sys


def main():
    # Use 'pip list --outdated' to get only packages with newer versions available.
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list", "--outdated"],
        capture_output=True, text=True,
    )

    if result.returncode != 0:
        print("Error running pip list:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)

    lines = result.stdout.strip().splitlines()
    packages = []
    for line in lines[2:]:  # skip header lines
        parts = line.split()
        if len(parts) >= 3:
            packages.append(parts[0])

    if not packages:
        print("No outdated packages found.")
        return

    print(f"Found {len(packages)} outdated package(s):")
    for p in packages:
        print(f"  - {p}")
    print()

    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--upgrade"] + packages,
        capture_output=True, text=True,
    )

    if result.returncode != 0:
        print("Error during upgrade:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)

    print("\nUpgrade complete.")


if __name__ == "__main__":
    main()
