#!/usr/bin/env python3
"""
CSV Cleaner - Golden Solution.

Reads a dirty CSV file, applies cleaning rules, and writes a clean CSV.
Usage: python3 cleaner.py <input.csv> <output.csv>

Cleaning rules (applied in order):
1. BOM Removal        - Strip UTF-8 BOM (EF BB BF) if present
2. Whitespace Trimming - Strip leading/trailing whitespace from every field
3. Empty Row Removal   - Remove rows where ALL fields are empty
4. Column Normalization - Pad short rows / truncate long rows to header width
5. Duplicate Removal   - Remove exact duplicate data rows (keep first)
6. Proper CSV Parsing  - Use stdlib csv module for quoted fields, commas, newlines
"""

import csv
import io
import sys


def clean_csv(input_path: str, output_path: str) -> None:
    # 1. Read raw bytes
    with open(input_path, "rb") as f:
        raw = f.read()

    # 2. Strip UTF-8 BOM if present
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]

    # 3. Decode: UTF-8 first, fallback to latin-1 for non-UTF-8 bytes
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")

    # 4. Parse CSV using stdlib (handles quoted fields, multi-line, etc.)
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)

    # Empty file: produce empty output
    if not rows:
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            pass
        return

    # 5. Process header
    header = [h.strip() for h in rows[0]]
    expected_cols = len(header)

    # 6. Process data rows
    seen = set()
    cleaned = [header]

    for row in rows[1:]:
        # 6a. Strip whitespace from every cell
        row = [cell.strip() for cell in row]

        # 6b. Skip completely empty / whitespace-only rows
        if all(cell == "" for cell in row):
            continue

        # 6c. Normalize column count to match header
        if len(row) < expected_cols:
            row.extend([""] * (expected_cols - len(row)))
        elif len(row) > expected_cols:
            row = row[:expected_cols]

        # 6d. Deduplicate (after normalization, keep first occurrence)
        key = tuple(row)
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(row)

    # 7. Write clean UTF-8 CSV output (no BOM)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(cleaned)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.csv> <output.csv>", file=sys.stderr)
        sys.exit(1)
    clean_csv(sys.argv[1], sys.argv[2])
