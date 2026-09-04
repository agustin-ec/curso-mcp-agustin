# Contract: Python Library Interface

**Feature**: `001-temperature-converter`
**Target Module**: `src.converter`

---

## 1. Module Export Summary

```python
from src.converter import (
    TemperatureScale,
    ConversionResult,
    convert_temperature,
    AbsoluteZeroError,
    InvalidScaleError,
)
```

---

## 2. Public Functions

### `convert_temperature`

Performs conversion of a numeric temperature value between specified scales.

#### Signature
```python
def convert_temperature(
    value: float | int,
    from_scale: str | TemperatureScale,
    to_scale: str | TemperatureScale,
) -> ConversionResult:
    """
    Converts a temperature from one scale to another.

    :param value: Numeric value of the temperature.
    :param from_scale: Source scale ('C', 'F', 'K' or TemperatureScale).
    :param to_scale: Target scale ('C', 'F', 'K' or TemperatureScale).
    :return: ConversionResult containing converted_value rounded to 2 decimal places.
    :raises AbsoluteZeroError: If input temperature is below absolute zero (e.g. Kelvin < 0).
    :raises InvalidScaleError: If from_scale or to_scale is unrecognized.
    :raises TypeError: If value cannot be converted to float.
    """
```

#### Return Value
Returns an instance of `ConversionResult`:
```python
@dataclass(frozen=True)
class ConversionResult:
    original_value: float
    from_scale: TemperatureScale
    converted_value: float
    to_scale: TemperatureScale

    @property
    def formatted(self) -> str:
        """Returns formatted representation, e.g. '37.78 °C' or '300.00 K'."""
        ...
```

---

## 3. Exceptions

```python
class TemperatureError(ValueError):
    """Base exception for temperature conversion domain errors."""

class AbsoluteZeroError(TemperatureError):
    """Raised when an input temperature is below physical absolute zero."""

class InvalidScaleError(TemperatureError):
    """Raised when an unknown temperature scale is specified."""
```

---

## 4. Behavior & Contract Guarantees

1. **Determinism**: For any valid input `(value, from_scale, to_scale)`, calling `convert_temperature` is idempotent and side-effect free.
2. **Rounding**: The returned `converted_value` is always rounded to 2 decimal places using standard mathematical rounding.
3. **Boundary Enforcement**: Any input where `from_scale == 'K'` and `value < 0` MUST raise `AbsoluteZeroError` without performing arithmetic.
