# Contract: Command-Line Interface (CLI)

**Feature**: `001-temperature-converter`
**Target Entrypoint**: `python3 -m src.cli`

---

## 1. Command Syntax

```bash
python3 -m src.cli <VALUE> --from <SCALE> --to <SCALE> [--json]
```

Or short flags:
```bash
python3 -m src.cli <VALUE> -f <SCALE> -t <SCALE> [-j]
```

---

## 2. Arguments & Options

| Parameter | Type | Required | Description | Allowed Values |
| :--- | :--- | :--- | :--- | :--- |
| `VALUE` | `float` | Yes | Numeric temperature to convert | Any real number |
| `-f`, `--from` | `string` | Yes | Source temperature scale | `C`, `F`, `K` (case-insensitive) |
| `-t`, `--to` | `string` | Yes | Target temperature scale | `C`, `F`, `K` (case-insensitive) |
| `-j`, `--json` | `flag` | No | Outputs result as structured JSON | `true` / `false` |
| `-h`, `--help` | `flag` | No | Show help message and exit | - |

---

## 3. Standard Output Format

### Text Output (Default)
When run successfully:
```text
37.78 °C
```

### JSON Output (`--json`)
When run successfully:
```json
{
  "status": "success",
  "data": {
    "original_value": 100.0,
    "from_scale": "F",
    "converted_value": 37.78,
    "to_scale": "C",
    "formatted": "37.78 °C"
  }
}
```

---

## 4. Error Output & Exit Codes

### Exit Codes
- `0`: Successful conversion.
- `1`: Validation error (e.g. Kelvin < 0 or below absolute zero).
- `2`: CLI usage / argument syntax error (e.g. missing required argument, non-numeric value).

### Error Output (Text to stderr)
```text
Error: Kelvin temperature cannot be less than 0 K (received: -5)
```

### Error Output (JSON to stdout/stderr with `--json`)
```json
{
  "status": "error",
  "error": {
    "code": "BELOW_ABSOLUTE_ZERO",
    "message": "Kelvin temperature cannot be less than 0 K (received: -5)"
  }
}
```
