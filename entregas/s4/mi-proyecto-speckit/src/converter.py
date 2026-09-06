"""Temperature conversion domain logic, scales, and data models."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
import math
from typing import Any, Union


class TemperatureError(ValueError):
    """Base exception for temperature conversion domain errors."""


class AbsoluteZeroError(TemperatureError):
    """Raised when an input temperature is below physical absolute zero."""


class InvalidScaleError(TemperatureError):
    """Raised when an unknown temperature scale is specified."""


class TemperatureScale(str, Enum):
    """Supported thermodynamic temperature scales."""

    CELSIUS = "C"
    FAHRENHEIT = "F"
    KELVIN = "K"

    @property
    def symbol(self) -> str:
        """Returns the unit symbol with degree sign where appropriate."""
        if self == TemperatureScale.CELSIUS:
            return "°C"
        elif self == TemperatureScale.FAHRENHEIT:
            return "°F"
        elif self == TemperatureScale.KELVIN:
            return "K"
        return self.value

    @property
    def absolute_zero(self) -> float:
        """Returns the physical lower bound (absolute zero) for this scale."""
        if self == TemperatureScale.CELSIUS:
            return -273.15
        elif self == TemperatureScale.FAHRENHEIT:
            return -459.67
        elif self == TemperatureScale.KELVIN:
            return 0.0
        return 0.0

    @classmethod
    def parse(cls, value: Union[str, TemperatureScale]) -> TemperatureScale:
        """
        Parses a scale identifier string or instance into a valid TemperatureScale.

        Accepts case-insensitive short and long forms:
        - 'c', 'celsius', 'C' -> TemperatureScale.CELSIUS
        - 'f', 'fahrenheit', 'F' -> TemperatureScale.FAHRENHEIT
        - 'k', 'kelvin', 'K' -> TemperatureScale.KELVIN
        """
        if isinstance(value, cls):
            return value

        if not isinstance(value, str):
            raise InvalidScaleError(f"Invalid temperature scale type: {type(value).__name__}")

        normalized = value.strip().upper()
        if normalized in {"C", "CELSIUS"}:
            return cls.CELSIUS
        elif normalized in {"F", "FAHRENHEIT"}:
            return cls.FAHRENHEIT
        elif normalized in {"K", "KELVIN"}:
            return cls.KELVIN

        raise InvalidScaleError(f"Unsupported temperature scale: '{value}'. Expected C, F, or K.")


@dataclass(frozen=True)
class ConversionResult:
    """Immutable data transfer object representing a conversion result."""

    original_value: float
    from_scale: TemperatureScale
    converted_value: float
    to_scale: TemperatureScale

    @property
    def formatted(self) -> str:
        """Returns formatted string output, e.g. '37.78 °C'."""
        return f"{self.converted_value:.2f} {self.to_scale.symbol}"


def round_half_up(val: float, decimals: int = 2) -> float:
    """Rounds a numeric float to specified decimal places using standard round half-up."""
    d = Decimal(str(val)) if abs(val) < 1e12 else Decimal(f"{val:.10f}")
    target_exp = Decimal("1." + "0" * decimals) if decimals > 0 else Decimal("1")
    return float(d.quantize(target_exp, rounding=ROUND_HALF_UP))


def convert_temperature(
    value: Union[float, int],
    from_scale: Union[str, TemperatureScale],
    to_scale: Union[str, TemperatureScale],
) -> ConversionResult:
    """
    Converts a temperature from one scale to another.

    :param value: Numeric value of the temperature.
    :param from_scale: Source scale ('C', 'F', 'K' or TemperatureScale).
    :param to_scale: Target scale ('C', 'F', 'K' or TemperatureScale).
    :return: ConversionResult containing converted_value rounded to 2 decimal places.
    :raises AbsoluteZeroError: If input temperature is below absolute zero.
    :raises InvalidScaleError: If from_scale or to_scale is unrecognized.
    :raises TypeError: If value cannot be parsed as a float.
    """
    source_scale = TemperatureScale.parse(from_scale)
    target_scale = TemperatureScale.parse(to_scale)

    if isinstance(value, bool):
        raise TypeError(f"Temperature value cannot be a boolean, got: {value}")

    try:
        numeric_val = float(value)
    except (ValueError, TypeError) as exc:
        raise TypeError(f"Temperature value must be a valid number, got: {value}") from exc

    if not math.isfinite(numeric_val):
        raise ValueError(f"Temperature value must be a finite number, got: {numeric_val}")

    # Enforce physical thermodynamic boundary (Absolute Zero)
    if source_scale == TemperatureScale.KELVIN and numeric_val < 0.0:
        raise AbsoluteZeroError(
            f"Kelvin temperature cannot be less than 0 K (received: {numeric_val})"
        )
    elif source_scale == TemperatureScale.CELSIUS and numeric_val < -273.15:
        raise AbsoluteZeroError(
            f"Celsius temperature cannot be less than -273.15 °C (below absolute zero, received: {numeric_val})"
        )
    elif source_scale == TemperatureScale.FAHRENHEIT and numeric_val < -459.67:
        raise AbsoluteZeroError(
            f"Fahrenheit temperature cannot be less than -459.67 °F (below absolute zero, received: {numeric_val})"
        )

    # Same scale conversion (Identity)
    if source_scale == target_scale:
        converted = numeric_val
    elif source_scale == TemperatureScale.CELSIUS and target_scale == TemperatureScale.FAHRENHEIT:
        converted = (numeric_val * 9.0 / 5.0) + 32.0
    elif source_scale == TemperatureScale.FAHRENHEIT and target_scale == TemperatureScale.CELSIUS:
        converted = (numeric_val - 32.0) * 5.0 / 9.0
    elif source_scale == TemperatureScale.CELSIUS and target_scale == TemperatureScale.KELVIN:
        converted = numeric_val + 273.15
    elif source_scale == TemperatureScale.KELVIN and target_scale == TemperatureScale.CELSIUS:
        converted = numeric_val - 273.15
    elif source_scale == TemperatureScale.FAHRENHEIT and target_scale == TemperatureScale.KELVIN:
        converted = ((numeric_val - 32.0) * 5.0 / 9.0) + 273.15
    elif source_scale == TemperatureScale.KELVIN and target_scale == TemperatureScale.FAHRENHEIT:
        converted = ((numeric_val - 273.15) * 9.0 / 5.0) + 32.0
    else:
        converted = numeric_val

    rounded_converted = round_half_up(converted, 2)
    return ConversionResult(
        original_value=numeric_val,
        from_scale=source_scale,
        converted_value=rounded_converted,
        to_scale=target_scale,
    )
