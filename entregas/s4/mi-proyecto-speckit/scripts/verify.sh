#!/usr/bin/env bash
set -e

echo "=========================================="
echo "Running Temperature Unit Converter Smoke Tests"
echo "=========================================="

echo "[1/7] Running unittest test suite..."
python3 -m unittest discover -s tests -p "test_*.py" -v

echo "[2/7] Testing 0 C -> F (expected 32.00 °F)..."
OUT=$(python3 -m src.cli 0 -f C -t F)
[ "$OUT" = "32.00 °F" ] || { echo "Failed: got $OUT"; exit 1; }

echo "[3/7] Testing 100 F -> C (expected 37.78 °C)..."
OUT=$(python3 -m src.cli 100 -f F -t C)
[ "$OUT" = "37.78 °C" ] || { echo "Failed: got $OUT"; exit 1; }

echo "[4/7] Testing 273.15 K -> C (expected 0.00 °C)..."
OUT=$(python3 -m src.cli 273.15 -f K -t C)
[ "$OUT" = "0.00 °C" ] || { echo "Failed: got $OUT"; exit 1; }

echo "[5/7] Testing 0 K -> C (expected -273.15 °C)..."
OUT=$(python3 -m src.cli 0 -f K -t C)
[ "$OUT" = "-273.15 °C" ] || { echo "Failed: got $OUT"; exit 1; }

echo "[6/7] Testing JSON output mode..."
JSON_OUT=$(python3 -m src.cli 25 -f C -t F --json)
echo "$JSON_OUT" | grep -q '"status": "success"' || { echo "Failed JSON output"; exit 1; }

echo "[7/7] Testing rejection of negative Kelvin (exit code 1 expected)..."
if python3 -m src.cli -10 -f K -t C 2>/dev/null; then
    echo "Failed: negative Kelvin should have exited with code 1"
    exit 1
else
    echo "Correctly rejected negative Kelvin."
fi

echo "=========================================="
echo "ALL QUICKSTART CHECKS PASSED SUCCESSFULLY!"
echo "=========================================="
