#!/usr/bin/env python3
"""Generate dirty_data.csv with various edge cases for CSV cleaning task."""

import csv
import io
import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "environment", "dirty_data.csv")


def generate():
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")

    # Header
    writer.writerow(["id", "name", "email", "department", "notes"])

    # Row 1: whitespace in all fields, comma inside quoted field
    writer.writerow([
        " 1 ",
        " Alice Johnson ",
        "alice@example.com",
        "Engineering",
        "Senior developer, 5 years experience",
    ])

    # Row 2: unquoted field with literal double-quote, escaped quotes in quoted field
    writer.writerow([
        "2",
        'Bob "The Builder" Smith',
        "bob@example.com",
        "Construction",
        'Prefers ""nail guns"" over hammers',
    ])

    # Row 3: whitespace-only last field
    writer.writerow([
        "3",
        "Charlie Brown",
        "charlie@example.com",
        "Marketing",
        " ",
    ])

    # Row 4: comma inside quoted name field
    writer.writerow([
        "4",
        "Diana, Princess of Themyscira",
        "diana@example.com",
        "Leadership",
        "Amazon warrior",
    ])

    # Row 5: missing columns (only 3 fields instead of 5)
    writer.writerow([
        "5",
        "Eve",
        "eve@example.com",
    ])

    # Row 6: empty line (write nothing)
    writer.writerow([])

    # Row 7-9 (single logical row): multi-line fields in name and notes
    writer.writerow([
        "6",
        "Grace\nHopper",
        "grace@example.com",
        "Research",
        "Developed COBOL;\ninvented compiler",
    ])

    # Row 10: whitespace in unquoted department, comma in quoted notes
    writer.writerow([
        "7",
        "Henry",
        "henry@example.com",
        " Sales ",
        "needs access to, the CRM system",
    ])

    # Row 11: duplicate of Row 1
    writer.writerow([
        " 1 ",
        " Alice Johnson ",
        "alice@example.com",
        "Engineering",
        "Senior developer, 5 years experience",
    ])

    # Row 12: extra column (6 fields instead of 5)
    writer.writerow([
        "8",
        "Isabel",
        "isabel@example.com",
        "HR",
        "extra_field_here",
        "Regular notes",
    ])

    # Row 13: whitespace-only row (all fields empty/whitespace)
    writer.writerow([" ", " ", " ", " ", " "])

    # Row 14: empty name field
    writer.writerow([
        "9",
        "",
        "empty_name@example.com",
        "Engineering",
        "test",
    ])

    # Row 15: comma in quoted name, comma in quoted notes
    writer.writerow([
        "10",
        "Kai, Jr.",
        "kai@example.com",
        "Operations",
        "Has, a comma",
    ])

    csv_text = buf.getvalue()

    # Prepend UTF-8 BOM and write to file
    bom = b"\xef\xbb\xbf"
    with open(OUTPUT_PATH, "wb") as f:
        f.write(bom)
        f.write(csv_text.encode("utf-8"))

    print(f"Generated: {OUTPUT_PATH}")
    print(f"  Total bytes: {os.path.getsize(OUTPUT_PATH)} (including {len(bom)}-byte BOM)")


if __name__ == "__main__":
    generate()
