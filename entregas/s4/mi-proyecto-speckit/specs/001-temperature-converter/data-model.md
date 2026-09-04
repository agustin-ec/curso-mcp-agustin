# Data Model: Temperature Unit Converter

**Feature**: `001-temperature-converter`
**Date**: 2026-09-03
**Status**: Completed

## Overview

This document describes the domain entities, enumerations, validation rules, and data transfer structures used in the Temperature Unit Converter feature.

---

## Entities & Value Objects

### 1. `TemperatureScale` (Enumeration)

Represents the physical thermodynamic temperature scale.

| Field / Member | Representation | Allowed Aliases (Case-Insensitive) | Absolute Zero Limit |
| :--- | :--- | :--- | :--- |
| `CELSIUS` | `'C'` | `'c'`, `'celsius'`, `'C'` | `-273.15` |
| `FAHRENHEIT` | `'F'` | `'f'`, `'fahrenheit'`, `'F'` | `-459.67` |
| `KELVIN` | `'K'` | `'k'`, `'kelvin'`, `'K'` | `0.00` |

#### Methods / Parsing
- `parse(value: str) -> TemperatureScale`: Resolves string identifiers (e.g. `"c"`, `"Kelvin"`) to the corresponding enum member. Raises `InvalidScaleError` if unrecognized.

---

### 2. `ConversionRequest` (Value Object / DTO)

Encapsulates the input parameters needed to execute a temperature conversion.

| Field | Type | Validation Rules | Description |
| :--- | :--- | :--- | :--- |
| `value` | `float` | Must be a valid numeric real number | The raw temperature value to convert |
| `from_scale` | `TemperatureScale` | Must be one of `CELSIUS`, `FAHRENHEIT`, `KELVIN` | Source scale |
| `to_scale` | `TemperatureScale` | Must be one of `CELSIUS`, `FAHRENHEIT`, `KELVIN` | Target scale |

#### Validation Rules
- If `from_scale == KELVIN` and `value < 0.0`: Rejection with `AbsoluteZeroError` (`"Kelvin temperature cannot be less than 0 K"`).
- If `from_scale == CELSIUS` and `value < -273.15`: Rejection with `AbsoluteZeroError` (`"Celsius temperature cannot be less than -273.15 °C (below absolute zero)"`).
- If `from_scale == FAHRENHEIT` and `value < -459.67`: Rejection with `AbsoluteZeroError` (`"Fahrenheit temperature cannot be less than -459.67 °F (below absolute zero)"`).

---

### 3. `ConversionResult` (Value Object / Output DTO)

Encapsulates the successful outcome of a conversion.

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `original_value` | `float` | Original numerical input | `100.0` |
| `from_scale` | `TemperatureScale` | Source scale | `TemperatureScale.FAHRENHEIT` |
| `converted_value` | `float` | Result rounded to 2 decimal places | `37.78` |
| `to_scale` | `TemperatureScale` | Target scale | `TemperatureScale.CELSIUS` |
| `formatted` | `str` | Human-readable representation | `"37.78 °C"` |

---

### 4. `ConversionError` (Domain Exception)

Encapsulates error state when validation fails.

| Field | Type | Description |
| :--- | :--- | :--- |
| `error_type` | `str` | `"INVALID_SCALE"`, `"BELOW_ABSOLUTE_ZERO"`, or `"INVALID_VALUE"` |
| `message` | `str` | Detailed, user-friendly description of the error |
| `input_value` | `Any` | The invalid input that triggered the error |

---

## State Lifecycle & Data Flow

```text
[Raw Input: value, from_scale, to_scale]
                   │
                   ▼
       1. Parse & Normalize Units
                   │
                   ▼
     2. Physical Limit Validation (value >= absolute_zero)
        ├── [Fails] ──> Raise AbsoluteZeroError / Return Error Result
        └── [Passes]
                   │
                   ▼
     3. Calculate Direct Conversion Formula
                   │
                   ▼
     4. Round Result to 2 Decimal Places (round half-up)
                   │
                   ▼
[Output: ConversionResult(converted_value, to_scale, formatted)]
```
