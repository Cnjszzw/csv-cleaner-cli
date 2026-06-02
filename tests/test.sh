#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ACTUAL_OUTPUT="/tmp/actual_clean_output.csv"
EXPECTED_OUTPUT="$SCRIPT_DIR/expected_clean.csv"

echo "=== CSV Cleaner Verification ==="

# Step 1: Run the solution on the dirty data
echo "[1/2] Running solution on dirty_data.csv..."
bash "$PROJECT_DIR/solution/solve.sh" \
    "$PROJECT_DIR/environment/dirty_data.csv" \
    "$ACTUAL_OUTPUT"

if [ ! -f "$ACTUAL_OUTPUT" ]; then
    echo "ERROR: Solution did not produce output file: $ACTUAL_OUTPUT"
    exit 1
fi

# Step 2: Compare output against expected clean data
echo "[2/2] Comparing output against expected clean data..."
python3 "$SCRIPT_DIR/test_logic.py" "$EXPECTED_OUTPUT" "$ACTUAL_OUTPUT"

echo "=== All checks passed ==="
