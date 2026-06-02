# CSV Cleaner CLI

## Task Description

You are given a dirty CSV file that contains various data quality issues.
Write a Python command-line tool (`cleaner.py`) that reads this file,
cleans it according to the rules below, and outputs a properly formatted
clean CSV file.

## Input/Output Specification

Usage: `python3 cleaner.py <input.csv> <output.csv>`

- `<input.csv>`: Path to a CSV file that may contain data quality issues.
- `<output.csv>`: Path where the cleaned CSV must be written.

## Cleaning Rules (applied in order)

1. **BOM Removal**: If the input file starts with a UTF-8 Byte Order Mark
   (BOM, bytes `EF BB BF`), remove it before parsing.
2. **Whitespace Trimming**: Strip leading and trailing whitespace from every
   field value in every row, including the header row.
3. **Empty Row Removal**: Remove any row where ALL field values are empty
   strings after trimming. The header row is never removed.
4. **Column Count Normalization**:
   - If a data row has fewer columns than the header, pad with empty strings.
   - If a data row has more columns than the header, truncate the extra
     columns (keep only the first N columns matching the header width).
5. **Duplicate Removal**: Remove exact duplicate data rows, keeping only the
   first occurrence. Duplicate detection uses the normalized row content
   (post-trimming, post-column-count-adjustment). The header row is excluded
   from duplicate checking.
6. **Proper CSV Parsing**: Your code must correctly handle CSV fields that
   contain commas, double-quote characters, and newline characters. Use the
   Python standard library `csv` module for correct parsing.

## Encoding

- Input files may contain non-UTF-8 byte sequences. Your code must handle
  them gracefully (e.g., by replacing or falling back to a compatible
  encoding).
- Output must be valid UTF-8 encoded CSV with no BOM.

## Constraints

- Use only Python 3 standard library modules. No external packages
  (pandas, numpy, etc.) are available in the test environment.
- Your script must work with Python 3.11 or later.
- The output must match the expected clean output exactly (cell-by-cell).

## Files Provided

- `environment/dirty_data.csv`: The dirty input file to clean.

## Evaluation

Your solution will be evaluated by running:

```bash
bash solution/solve.sh environment/dirty_data.csv /tmp/output.csv
```

The resulting output file will be compared cell-by-cell against a reference
clean output. Your solution passes if every cell matches exactly.
