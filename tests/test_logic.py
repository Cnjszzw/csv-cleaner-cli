#!/usr/bin/env python3
"""Compares two CSV files cell-by-cell for exact match.

Usage: python3 test_logic.py <expected.csv> <actual.csv>
Exit codes: 0 = pass, 1 = fail, 2 = usage error
"""

import csv
import sys


def load_csv(path: str) -> list[list[str]]:
    """Load CSV as list of rows, each row as list of strings."""
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        return list(reader)


def validate(expected_path: str, actual_path: str) -> list[str]:
    """Return list of error messages. Empty list means pass."""
    try:
        expected = load_csv(expected_path)
    except FileNotFoundError:
        return [f"Expected output file not found: {expected_path}"]
    except Exception as e:
        return [f"Failed to read expected file {expected_path}: {e}"]

    try:
        actual = load_csv(actual_path)
    except FileNotFoundError:
        return [f"Actual output file not found: {actual_path}"]
    except UnicodeDecodeError as e:
        return [f"Actual output is not valid UTF-8: {e}"]
    except Exception as e:
        return [f"Failed to read actual file {actual_path}: {e}"]

    errors = []

    # Check row count
    if len(expected) != len(actual):
        errors.append(
            f"Row count mismatch: expected {len(expected)}, got {len(actual)}"
        )

    # Check column count in header
    if expected and actual:
        exp_cols = len(expected[0])
        act_cols = len(actual[0])
        if exp_cols != act_cols:
            errors.append(
                f"Column count mismatch: expected {exp_cols} columns, "
                f"got {act_cols} columns"
            )

    # Cell-by-cell comparison (up to min length)
    min_rows = min(len(expected), len(actual))
    for i in range(min_rows):
        exp_row = expected[i]
        act_row = actual[i]
        min_cols = min(len(exp_row), len(act_row))
        for j in range(min_cols):
            if exp_row[j] != act_row[j]:
                errors.append(
                    f"Row {i}, Col {j}: expected {exp_row[j]!r}, "
                    f"got {act_row[j]!r}"
                )

    # Check for extra/missing columns in each row
    for i in range(min_rows):
        if len(expected[i]) > len(actual[i]):
            for j in range(len(actual[i]), len(expected[i])):
                errors.append(
                    f"Row {i}: missing expected column {j}: {expected[i][j]!r}"
                )
        elif len(actual[i]) > len(expected[i]):
            for j in range(len(expected[i]), len(actual[i])):
                errors.append(
                    f"Row {i}: unexpected extra column {j}: {actual[i][j]!r}"
                )

    # Check for extra/missing rows
    if len(expected) > len(actual):
        for i in range(len(actual), len(expected)):
            errors.append(f"Missing row {i}: {expected[i]}")
    elif len(actual) > len(expected):
        for i in range(len(expected), len(actual)):
            errors.append(f"Unexpected extra row {i}: {actual[i]}")

    return errors


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <expected.csv> <actual.csv>",
              file=sys.stderr)
        sys.exit(2)

    errors = validate(sys.argv[1], sys.argv[2])
    if errors:
        print("FAIL: Cleaned output does not match expected output.")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("PASS: Output matches expected clean data exactly.")
        sys.exit(0)
