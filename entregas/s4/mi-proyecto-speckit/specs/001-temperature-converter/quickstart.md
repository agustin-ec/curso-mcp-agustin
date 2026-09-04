# Quickstart Validation Guide: Temperature Unit Converter

**Feature**: `001-temperature-converter`
**Date**: 2026-09-03
**Status**: Ready for Implementation

---

## Prerequisites

- Python 3.10+ (tested on Python 3.12.3)
- No external pip dependencies required (pure standard library)

---

## Quick Verification Commands

Once implemented, the feature can be verified directly from the terminal.

### 1. Run Automated Test Suite

Run the full test suite (unit tests and boundary contract checks):

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

**Expected Outcome**: All tests pass (`OK`), covering conversions between C, F, K, rounding to 2 decimal places, and absolute zero rejections.

---

### 2. Manual CLI Validation Scenarios

#### Scenario A: Celsius to Fahrenheit (Standard Water Freezing & Boiling)
```bash
python3 -m src.cli 0 -f C -t F
# Expected Output: 32.00 °F

python3 -m src.cli 100 -f C -t F
# Expected Output: 212.00 °F
```

#### Scenario B: Fahrenheit to Celsius with 2 Decimal Rounding
```bash
python3 -m src.cli 100 -f F -t C
# Expected Output: 37.78 °C
```

#### Scenario C: Kelvin to Celsius and Fahrenheit
```bash
python3 -m src.cli 273.15 -f K -t C
# Expected Output: 0.00 °C

python3 -m src.cli 373.15 -f K -t F
# Expected Output: 212.00 °F
```

#### Scenario D: Absolute Zero Boundary (Exact 0 K)
```bash
python3 -m src.cli 0 -f K -t C
# Expected Output: -273.15 °C
```

#### Scenario E: Negative Kelvin Validation (Error Expected)
```bash
python3 -m src.cli -10 -f K -t C
# Expected Exit Code: 1
# Expected Stderr: Error: Kelvin temperature cannot be less than 0 K (received: -10.0)
```

#### Scenario F: JSON Output Flag
```bash
python3 -m src.cli 25 -f C -t F --json
# Expected Output:
# {"status": "success", "data": {"original_value": 25.0, "from_scale": "C", "converted_value": 77.0, "to_scale": "F", "formatted": "77.00 °F"}}
```

---

## Reference Links

- Specification: [spec.md](file:///home/agustin/entorno-desarrollo/certificacion-ia-gen/modulo2-backend/curso-mcp-agustin/entregas/s4/mi-proyecto-speckit/specs/001-temperature-converter/spec.md)
- Data Model: [data-model.md](file:///home/agustin/entorno-desarrollo/certificacion-ia-gen/modulo2-backend/curso-mcp-agustin/entregas/s4/mi-proyecto-speckit/specs/001-temperature-converter/data-model.md)
- Python Contract: [python-api.md](file:///home/agustin/entorno-desarrollo/certificacion-ia-gen/modulo2-backend/curso-mcp-agustin/entregas/s4/mi-proyecto-speckit/specs/001-temperature-converter/contracts/python-api.md)
- CLI Contract: [cli.md](file:///home/agustin/entorno-desarrollo/certificacion-ia-gen/modulo2-backend/curso-mcp-agustin/entregas/s4/mi-proyecto-speckit/specs/001-temperature-converter/contracts/cli.md)
